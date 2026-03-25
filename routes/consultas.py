from typing import Optional
from flask import jsonify
from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel
from models.base import db
from models.consulta import Consulta
from models.animal import Animal

tag = Tag(name="Consultas", description="Registro de consultas clínicas")
bp_consultas = APIBlueprint("consultas", __name__, url_prefix="/consultas")


class ConsultaBody(BaseModel):
    animal_id: int
    motivo: str
    diagnostico: Optional[str] = None
    tratamento: Optional[str] = None
    veterinario: Optional[str] = None


@bp_consultas.post("", tags=[tag])
def registrar_consulta(body: ConsultaBody):
    if not body.motivo.strip():
        return jsonify({"erro": "Campo obrigatório ausente: motivo"}), 400

    animal = db.session.get(Animal, body.animal_id)
    if not animal:
        return jsonify({"erro": f"Animal id={body.animal_id} não encontrado."}), 404

    consulta = Consulta(
        animal_id=body.animal_id,
        motivo=body.motivo.strip(),
        diagnostico=body.diagnostico,
        tratamento=body.tratamento,
        veterinario=body.veterinario,
    )
    db.session.add(consulta)
    db.session.commit()
    return jsonify({"mensagem": "Consulta registrada com sucesso.", "consulta": consulta.to_dict()}), 201
