# Importa todos os models para garantir que o SQLAlchemy os registre
# antes de db.create_all() ser chamado no app.py.
from .tutor import Tutor
from .animal import Animal
from .consulta import Consulta
