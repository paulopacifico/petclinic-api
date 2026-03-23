from flask import Blueprint, request, jsonify
from models.base import db
from models.tutor import Tutor

bp_tutores = Blueprint("tutores", __name__, url_prefix="/tutores")


# ─────────────────────────────────────────────────────────────────────────── #
#  POST /tutores  — cadastrar novo tutor
# ─────────────────────────────────────────────────────────────────────────── #
@bp_tutores.route("", methods=["POST"])
def cadastrar_tutor():
    """
    Recebe JSON com os dados do tutor e persiste no banco.
    Campos obrigatórios: nome, telefone
    Campos opcionais : email, cpf
    """
    dados = request.get_json(silent=True)

    # ── Validação de payload ─────────────────────────────────────────────── #
    if not dados:
        return jsonify({
            "erro": "Corpo da requisição ausente ou não é JSON válido."
        }), 400

    campos_obrigatorios = ["nome", "telefone"]
    ausentes = [c for c in campos_obrigatorios if not dados.get(c, "").strip()]
    if ausentes:
        return jsonify({
            "erro": f"Campo(s) obrigatório(s) ausente(s): {', '.join(ausentes)}"
        }), 400

    # ── Unicidade de CPF ─────────────────────────────────────────────────── #
    cpf = dados.get("cpf", "").strip() or None
    if cpf and db.session.query(Tutor).filter_by(cpf=cpf).first():
        return jsonify({
            "erro": f"CPF '{cpf}' já cadastrado no sistema."
        }), 409      # 409 Conflict — semântica correta para duplicata

    # ── Persistência ─────────────────────────────────────────────────────── #
    try:
        tutor = Tutor(
            nome     = dados["nome"].strip(),
            telefone = dados["telefone"].strip(),
            email    = dados.get("email", "").strip() or None,
            cpf      = cpf,
        )
        db.session.add(tutor)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro interno ao salvar tutor: {str(e)}"}), 500

    return jsonify({
        "mensagem": "Tutor cadastrado com sucesso.",
        "tutor": tutor.to_dict()
    }), 201   # 201 Created — obrigatório no POST bem-sucedido


# ─────────────────────────────────────────────────────────────────────────── #
#  GET /tutores  — listar todos os tutores
# ─────────────────────────────────────────────────────────────────────────── #
@bp_tutores.route("", methods=["GET"])
def listar_tutores():
    """
    Retorna todos os tutores.
    Query param opcional: ?nome=maria  (busca parcial, case-insensitive)
    """
    filtro_nome = request.args.get("nome", "").strip()

    query = db.session.query(Tutor).order_by(Tutor.nome)

    if filtro_nome:
        query = query.filter(Tutor.nome.ilike(f"%{filtro_nome}%"))

    tutores = query.all()

    return jsonify({
        "total": len(tutores),
        "tutores": [t.to_dict() for t in tutores]
    }), 200


# ─────────────────────────────────────────────────────────────────────────── #
#  GET /tutores/<id>  — buscar tutor por ID
# ─────────────────────────────────────────────────────────────────────────── #
@bp_tutores.route("/<int:tutor_id>", methods=["GET"])
def buscar_tutor(tutor_id):
    """
    Retorna um tutor pelo ID.
    Query param opcional: ?animais=true  (inclui lista de animais)
    """
    tutor = db.session.get(Tutor, tutor_id)

    if not tutor:
        return jsonify({
            "erro": f"Tutor com id={tutor_id} não encontrado."
        }), 404

    incluir_animais = request.args.get("animais", "").lower() == "true"

    return jsonify(tutor.to_dict(incluir_animais=incluir_animais)), 200


# ─────────────────────────────────────────────────────────────────────────── #
#  DELETE /tutores/<id>  — remover tutor
# ─────────────────────────────────────────────────────────────────────────── #
@bp_tutores.route("/<int:tutor_id>", methods=["DELETE"])
def deletar_tutor(tutor_id):
    """
    Remove o tutor e, em cascata (definido no model), todos os seus
    animais e as consultas vinculadas a esses animais.
    """
    tutor = db.session.get(Tutor, tutor_id)

    if not tutor:
        return jsonify({
            "erro": f"Tutor com id={tutor_id} não encontrado."
        }), 404

    nome = tutor.nome   # guarda antes de deletar para incluir na resposta

    try:
        db.session.delete(tutor)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro interno ao remover tutor: {str(e)}"}), 500

    return jsonify({
        "mensagem": f"Tutor '{nome}' (id={tutor_id}) removido com sucesso.",
        "id_removido": tutor_id
    }), 200
