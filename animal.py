from datetime import date, datetime, timezone
from .base import db


class Animal(db.Model):
    """
    Representa o paciente veterinário.
    Pertence a um Tutor (N:1) e pode ter várias Consultas (1:N).
    """
    __tablename__ = "animais"

    # Espécies válidas — usado para validação antes de persistir
    ESPECIES_VALIDAS = ["cachorro", "gato", "ave", "roedor", "réptil", "outro"]

    id              = db.Column(db.Integer, primary_key=True)
    nome            = db.Column(db.String(80),  nullable=False)
    especie         = db.Column(db.String(40),  nullable=False)
    raca            = db.Column(db.String(80),  nullable=True)
    sexo            = db.Column(db.String(1),   nullable=True)   # 'M' ou 'F'
    peso_kg         = db.Column(db.Float,       nullable=True)
    data_nascimento = db.Column(db.Date,        nullable=True)   # date (sem hora)
    tutor_id        = db.Column(
        db.Integer,
        db.ForeignKey("tutores.id", ondelete="CASCADE"),
        nullable=False
    )

    # Lado N do relacionamento com Tutor
    tutor = db.relationship("Tutor", back_populates="animais")

    # Relacionamento 1:N com Consulta
    consultas = db.relationship(
        "Consulta",
        back_populates="animal",
        cascade="all, delete-orphan",
        lazy="select",
        order_by="Consulta.data_consulta.desc()"
    )

    def calcular_idade(self) -> str | None:
        """
        Retorna a idade do animal formatada (ex: '3 anos e 2 meses').
        Calculado em Python a partir de data_nascimento — demonstra
        tratamento de datas além do simples armazenamento.
        """
        if not self.data_nascimento:
            return None

        hoje = date.today()
        anos = hoje.year - self.data_nascimento.year

        # Ajusta se o aniversário ainda não ocorreu este ano
        aniversario_esse_ano = self.data_nascimento.replace(year=hoje.year)
        if hoje < aniversario_esse_ano:
            anos -= 1

        # Calcula meses restantes após os anos completos
        meses = (hoje.month - self.data_nascimento.month) % 12

        if anos == 0:
            return f"{meses} meses"
        if meses == 0:
            return f"{anos} ano{'s' if anos > 1 else ''}"
        return f"{anos} ano{'s' if anos > 1 else ''} e {meses} meses"

    def to_dict(self, incluir_consultas: bool = False) -> dict:
        dados = {
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
        if incluir_consultas:
            dados["consultas"] = [c.to_dict() for c in self.consultas]
        return dados

    def __repr__(self):
        return f"<Animal id={self.id} nome={self.nome!r} especie={self.especie!r}>"
