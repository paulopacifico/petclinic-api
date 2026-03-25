from typing import Optional
from datetime import date
from flask import jsonify
from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel
from models.base import db
from models.animal import Animal
from models.tutor import Tutor

tag = Tag(name="Animais", description="Gerenciamento de animais e histórico clínico")
bp_animais = APIBlueprint("animais", __name__, url_prefix="/animais")


class AnimalBody(BaseModel):
    nome: str
    especie: str
    tutor_id: int
    raca: Optional[str] = None
    sexo: Optional[str] = None
    peso_kg: Optional[float] = None
    data_nascimento: Optional[date] = None


class AnimalPath(BaseModel):
    animal_id: int


class AnimalQuery(BaseModel):
    especie: Optional[str] = None


@bp_animais.post("", tags=[tag])
def cadastrar_animal(body: AnimalBody):
    if not body.nome.strip() or not body.especie.strip():
        return jsonify({"erro": "Campos obrigatórios ausentes: nome, especie"}), 400

    if body.sexo and body.sexo.upper() not in ("M", "F"):
        return jsonify({"erro": "Campo sexo aceita apenas 'M' ou 'F'."}), 400

    tutor = db.session.get(Tutor, body.tutor_id)
    if not tutor:
        return jsonify({"erro": f"Tutor id={body.tutor_id} não encontrado."}), 404

    animal = Animal(
        nome=body.nome.strip(),
        especie=body.especie.strip(),
        tutor_id=body.tutor_id,
        raca=body.raca.strip() if body.raca else None,
        sexo=body.sexo.upper() if body.sexo else None,
        peso_kg=body.peso_kg,
        data_nascimento=body.data_nascimento,
    )
    db.session.add(animal)
    db.session.commit()
    return jsonify({"mensagem": "Animal cadastrado com sucesso.", "animal": animal.to_dict()}), 201


@bp_animais.get("", tags=[tag])
def listar_animais(query: AnimalQuery):
    q = db.session.query(Animal).order_by(Animal.nome)
    if query.especie:
        q = q.filter(Animal.especie.ilike(query.especie))
    animais = q.all()
    return jsonify({"total": len(animais), "animais": [a.to_dict() for a in animais]}), 200


@bp_animais.get("/<int:animal_id>", tags=[tag])
def buscar_animal(path: AnimalPath):
    animal = db.session.get(Animal, path.animal_id)
    if not animal:
        return jsonify({"erro": f"Animal id={path.animal_id} não encontrado."}), 404
    return jsonify(animal.to_dict()), 200


@bp_animais.delete("/<int:animal_id>", tags=[tag])
def deletar_animal(path: AnimalPath):
    animal = db.session.get(Animal, path.animal_id)
    if not animal:
        return jsonify({"erro": f"Animal id={path.animal_id} não encontrado."}), 404
    nome = animal.nome
    db.session.delete(animal)
    db.session.commit()
    return jsonify({"mensagem": f"Animal '{nome}' (id={path.animal_id}) removido com sucesso.", "id_removido": path.animal_id}), 200


@bp_animais.get("/<int:animal_id>/consultas", tags=[tag])
def listar_consultas_animal(path: AnimalPath):
    animal = db.session.get(Animal, path.animal_id)
    if not animal:
        return jsonify({"erro": f"Animal id={path.animal_id} não encontrado."}), 404
    return jsonify({"animal_id": path.animal_id, "animal_nome": animal.nome, "consultas": [c.to_dict() for c in animal.consultas]}), 200
