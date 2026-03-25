from typing import Optional
from flask import jsonify
from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel
from models.base import db
from models.tutor import Tutor

tag = Tag(name="Tutores", description="Gerenciamento de tutores e seus animais")
bp_tutores = APIBlueprint("tutores", __name__, url_prefix="/tutores")


class TutorBody(BaseModel):
    nome: str
    telefone: str
    email: Optional[str] = None
    cpf: Optional[str] = None


class TutorPath(BaseModel):
    tutor_id: int


@bp_tutores.post("", tags=[tag])
def cadastrar_tutor(body: TutorBody):
    if not body.nome.strip() or not body.telefone.strip():
        return jsonify({"erro": "Campos obrigatórios ausentes: nome, telefone"}), 400

    cpf = body.cpf.strip() if body.cpf else None
    if cpf and db.session.query(Tutor).filter_by(cpf=cpf).first():
        return jsonify({"erro": f"CPF '{cpf}' já cadastrado."}), 409

    tutor = Tutor(
        nome=body.nome.strip(),
        telefone=body.telefone.strip(),
        email=body.email.strip() if body.email else None,
        cpf=cpf,
    )
    db.session.add(tutor)
    db.session.commit()
    return jsonify({"mensagem": "Tutor cadastrado com sucesso.", "tutor": tutor.to_dict()}), 201


@bp_tutores.get("", tags=[tag])
def listar_tutores():
    tutores = db.session.query(Tutor).order_by(Tutor.nome).all()
    return jsonify({"total": len(tutores), "tutores": [t.to_dict() for t in tutores]}), 200


@bp_tutores.get("/<int:tutor_id>", tags=[tag])
def buscar_tutor(path: TutorPath):
    tutor = db.session.get(Tutor, path.tutor_id)
    if not tutor:
        return jsonify({"erro": f"Tutor id={path.tutor_id} não encontrado."}), 404
    return jsonify(tutor.to_dict()), 200


@bp_tutores.delete("/<int:tutor_id>", tags=[tag])
def deletar_tutor(path: TutorPath):
    tutor = db.session.get(Tutor, path.tutor_id)
    if not tutor:
        return jsonify({"erro": f"Tutor id={path.tutor_id} não encontrado."}), 404
    nome = tutor.nome
    db.session.delete(tutor)
    db.session.commit()
    return jsonify({"mensagem": f"Tutor '{nome}' (id={path.tutor_id}) removido com sucesso.", "id_removido": path.tutor_id}), 200


@bp_tutores.get("/<int:tutor_id>/animais", tags=[tag])
def listar_animais_tutor(path: TutorPath):
    tutor = db.session.get(Tutor, path.tutor_id)
    if not tutor:
        return jsonify({"erro": f"Tutor id={path.tutor_id} não encontrado."}), 404
    return jsonify({"tutor_id": path.tutor_id, "tutor_nome": tutor.nome, "animais": [a.to_dict() for a in tutor.animais]}), 200
