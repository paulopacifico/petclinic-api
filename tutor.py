from datetime import datetime, timezone
from .base import db


class Tutor(db.Model):
    """
    Representa o responsável legal pelo animal.
    Um tutor pode ter zero ou mais animais cadastrados (1:N com Animal).
    """
    __tablename__ = "tutores"

    id           = db.Column(db.Integer, primary_key=True)
    nome         = db.Column(db.String(120), nullable=False)
    telefone     = db.Column(db.String(20),  nullable=False)
    email        = db.Column(db.String(120), nullable=True)
    cpf          = db.Column(db.String(14),  nullable=True, unique=True)
    data_cadastro = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    # Relacionamento 1:N com Animal.
    # cascade="all, delete-orphan" garante que ao deletar um tutor,
    # todos os seus animais (e as consultas deles) são removidos em cascata.
    animais = db.relationship(
        "Animal",
        back_populates="tutor",
        cascade="all, delete-orphan",
        lazy="select"
    )

    def to_dict(self, incluir_animais: bool = False) -> dict:
        """Serializa o objeto para dicionário (usado nas respostas JSON)."""
        dados = {
            "id":            self.id,
            "nome":          self.nome,
            "telefone":      self.telefone,
            "email":         self.email,
            "cpf":           self.cpf,
            "data_cadastro": self.data_cadastro.strftime("%d/%m/%Y %H:%M") if self.data_cadastro else None,
        }
        if incluir_animais:
            dados["animais"] = [a.to_dict() for a in self.animais]
        return dados

    def __repr__(self):
        return f"<Tutor id={self.id} nome={self.nome!r}>"
