from datetime import datetime, timezone
from .base import db


class Tutor(db.Model):
    __tablename__ = "tutores"

    id            = db.Column(db.Integer, primary_key=True)
    nome          = db.Column(db.String(120), nullable=False)
    telefone      = db.Column(db.String(20), nullable=False)
    email         = db.Column(db.String(120), nullable=True)
    cpf           = db.Column(db.String(14), nullable=True, unique=True)
    data_cadastro = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    animais = db.relationship(
        "Animal",
        back_populates="tutor",
        cascade="all, delete-orphan",
        lazy="select",
    )

    def to_dict(self):
        return {
            "id":            self.id,
            "nome":          self.nome,
            "telefone":      self.telefone,
            "email":         self.email,
            "cpf":           self.cpf,
            "data_cadastro": self.data_cadastro.strftime("%d/%m/%Y %H:%M") if self.data_cadastro else None,
        }
