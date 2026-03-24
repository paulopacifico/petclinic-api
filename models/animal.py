from datetime import date
from .base import db


class Animal(db.Model):
    __tablename__ = "animais"

    id              = db.Column(db.Integer, primary_key=True)
    nome            = db.Column(db.String(80), nullable=False)
    especie         = db.Column(db.String(40), nullable=False)
    raca            = db.Column(db.String(80), nullable=True)
    sexo            = db.Column(db.String(1), nullable=True)
    peso_kg         = db.Column(db.Float, nullable=True)
    data_nascimento = db.Column(db.Date, nullable=True)
    tutor_id        = db.Column(
        db.Integer,
        db.ForeignKey("tutores.id", ondelete="CASCADE"),
        nullable=False,
    )

    tutor = db.relationship("Tutor", back_populates="animais")
    consultas = db.relationship(
        "Consulta",
        back_populates="animal",
        cascade="all, delete-orphan",
        lazy="select",
        order_by="Consulta.data_consulta.desc()",
    )

    def calcular_idade(self):
        if not self.data_nascimento:
            return None
        hoje = date.today()
        anos = hoje.year - self.data_nascimento.year
        if hoje < self.data_nascimento.replace(year=hoje.year):
            anos -= 1
        meses = (hoje.month - self.data_nascimento.month) % 12
        if anos == 0 and meses == 0:
            return "menos de 1 mês"
        if anos == 0:
            return f"{meses} {'mês' if meses == 1 else 'meses'}"
        if meses == 0:
            return f"{anos} ano{'s' if anos > 1 else ''}"
        return f"{anos} ano{'s' if anos > 1 else ''} e {meses} {'mês' if meses == 1 else 'meses'}"

    def to_dict(self):
        return {
            "id":              self.id,
            "nome":            self.nome,
            "especie":         self.especie,
            "raca":            self.raca,
            "sexo":            self.sexo,
            "peso_kg":         self.peso_kg,
            "data_nascimento": self.data_nascimento.strftime("%d/%m/%Y") if self.data_nascimento else None,
            "idade":           self.calcular_idade(),
            "tutor_id":        self.tutor_id,
            "tutor_nome":      self.tutor.nome if self.tutor else None,
        }
