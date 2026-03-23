from datetime import datetime, timezone
from .base import db


class Consulta(db.Model):
    """
    Representa uma consulta veterinária (prontuário clínico).
    Pertence a um Animal (N:1). Armazena diagnóstico e tratamento
    como Text para comportar descrições clínicas longas.
    """
    __tablename__ = "consultas"

    id             = db.Column(db.Integer,   primary_key=True)
    animal_id      = db.Column(
        db.Integer,
        db.ForeignKey("animais.id", ondelete="CASCADE"),
        nullable=False
    )
    data_consulta  = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    motivo         = db.Column(db.String(200), nullable=False)
    diagnostico    = db.Column(db.Text,        nullable=True)
    tratamento     = db.Column(db.Text,        nullable=True)
    veterinario    = db.Column(db.String(120), nullable=True)

    # Lado N do relacionamento com Animal
    animal = db.relationship("Animal", back_populates="consultas")

    def to_dict(self) -> dict:
        return {
            "id":            self.id,
            "animal_id":     self.animal_id,
            "animal_nome":   self.animal.nome if self.animal else None,
            "data_consulta": self.data_consulta.strftime("%d/%m/%Y %H:%M") if self.data_consulta else None,
            "motivo":        self.motivo,
            "diagnostico":   self.diagnostico,
            "tratamento":    self.tratamento,
            "veterinario":   self.veterinario,
        }

    def __repr__(self):
        return f"<Consulta id={self.id} animal_id={self.animal_id} data={self.data_consulta}>"
