# PetClinic API — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a REST API Flask/SQLite com Swagger para prontuário eletrônico veterinário — tutores, animais e consultas, do zero, sem comentários no código.

**Architecture:** App factory em `app.py` usando `flask-openapi3` (`OpenAPI` substitui `Flask`). Três `APIBlueprint` em `routes/`. Três models SQLAlchemy em `models/`. Pydantic v2 para schemas de request/response documentados no Swagger.

**Tech Stack:** Python 3.10+, Flask 3.0.3, Flask-SQLAlchemy 3.1.1, Flask-CORS 4.0.1, Flask-OpenAPI3 3.1.0, Pydantic 2.7.4, SQLite

---

## File Map

| Arquivo | Responsabilidade |
|---------|-----------------|
| `requirements.txt` | Dependências de runtime |
| `models/base.py` | Instância `db = SQLAlchemy()` |
| `models/__init__.py` | Importa Tutor, Animal, Consulta (registra com ORM) |
| `models/tutor.py` | Model Tutor + `to_dict()` |
| `models/animal.py` | Model Animal + `calcular_idade()` + `to_dict()` |
| `models/consulta.py` | Model Consulta + `to_dict()` |
| `app.py` | `create_app()` factory, CORS, Swagger, error handlers, `db.create_all()` |
| `routes/tutores.py` | `bp_tutores`: POST/GET/GET‹id›/DELETE‹id›/GET‹id›/animais |
| `routes/animais.py` | `bp_animais`: POST/GET/GET‹id›/DELETE‹id›/GET‹id›/consultas |
| `routes/consultas.py` | `bp_consultas`: POST /consultas |
| `README.md` | Título, problema, instalação, execução, Swagger link |

---

## Task 1: requirements.txt e estrutura de diretórios

**Files:**
- Create: `requirements.txt`
- Create: `models/__init__.py` (vazio por enquanto)
- Create: `routes/__init__.py` (vazio)

- [ ] **Step 1: Escrever requirements.txt**

```
flask==3.0.3
flask-cors==4.0.1
flask-sqlalchemy==3.1.1
flask-openapi3==3.1.0
pydantic==2.7.4
```

Salvar em `/Users/paidoboris/Desktop/petclinic-api/requirements.txt`

- [ ] **Step 2: Criar diretórios e arquivos vazios**

```bash
mkdir -p /Users/paidoboris/Desktop/petclinic-api/models
mkdir -p /Users/paidoboris/Desktop/petclinic-api/routes
touch /Users/paidoboris/Desktop/petclinic-api/models/__init__.py
touch /Users/paidoboris/Desktop/petclinic-api/routes/__init__.py
```

- [ ] **Step 3: Instalar dependências**

```bash
cd /Users/paidoboris/Desktop/petclinic-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Resultado esperado: instalação sem erros, `flask-openapi3` e `pydantic` listados.

- [ ] **Step 4: Commit**

```bash
git -C /Users/paidoboris/Desktop/petclinic-api add requirements.txt models/__init__.py routes/__init__.py
git -C /Users/paidoboris/Desktop/petclinic-api commit -m "chore: setup inicial do projeto"
```

---

## Task 2: models/base.py

**Files:**
- Create: `models/base.py`

- [ ] **Step 1: Criar models/base.py**

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

Salvar em `models/base.py`.

- [ ] **Step 2: Commit**

```bash
git -C /Users/paidoboris/Desktop/petclinic-api add models/base.py
git -C /Users/paidoboris/Desktop/petclinic-api commit -m "feat: instância SQLAlchemy em models/base.py"
```

---

## Task 3: models/tutor.py

**Files:**
- Create: `models/tutor.py`

- [ ] **Step 1: Criar models/tutor.py**

```python
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
```

- [ ] **Step 2: Commit**

```bash
git -C /Users/paidoboris/Desktop/petclinic-api add models/tutor.py
git -C /Users/paidoboris/Desktop/petclinic-api commit -m "feat: model Tutor com relacionamento cascade"
```

---

## Task 4: models/animal.py

**Files:**
- Create: `models/animal.py`

- [ ] **Step 1: Criar models/animal.py**

```python
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
```

- [ ] **Step 2: Commit**

```bash
git -C /Users/paidoboris/Desktop/petclinic-api add models/animal.py
git -C /Users/paidoboris/Desktop/petclinic-api commit -m "feat: model Animal com data_nascimento (Date) e calcular_idade"
```

---

## Task 5: models/consulta.py + models/\_\_init\_\_.py

**Files:**
- Create: `models/consulta.py`
- Modify: `models/__init__.py`

- [ ] **Step 1: Criar models/consulta.py**

```python
from datetime import datetime, timezone
from .base import db


class Consulta(db.Model):
    __tablename__ = "consultas"

    id            = db.Column(db.Integer, primary_key=True)
    animal_id     = db.Column(
        db.Integer,
        db.ForeignKey("animais.id", ondelete="CASCADE"),
        nullable=False,
    )
    data_consulta = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    motivo        = db.Column(db.String(200), nullable=False)
    diagnostico   = db.Column(db.Text, nullable=True)
    tratamento    = db.Column(db.Text, nullable=True)
    veterinario   = db.Column(db.String(120), nullable=True)

    animal = db.relationship("Animal", back_populates="consultas")

    def to_dict(self):
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
```

- [ ] **Step 2: Atualizar models/\_\_init\_\_.py**

```python
from .tutor import Tutor
from .animal import Animal
from .consulta import Consulta

__all__ = ["Tutor", "Animal", "Consulta"]
```

- [ ] **Step 3: Commit**

```bash
git -C /Users/paidoboris/Desktop/petclinic-api add models/consulta.py models/__init__.py
git -C /Users/paidoboris/Desktop/petclinic-api commit -m "feat: model Consulta e registro dos três models"
```

---

## Task 6: app.py

**Files:**
- Create: `app.py`

Nota: `flask-openapi3` requer `OpenAPI` no lugar de `Flask`. Blueprints devem ser `APIBlueprint` e registrados com `app.register_api()`, não `register_blueprint()`.

- [ ] **Step 1: Criar app.py**

```python
from flask import jsonify
from flask_openapi3 import OpenAPI, Info
from flask_cors import CORS
from models.base import db
import models

info = Info(title="PetClinic API", version="1.0.0", description="Prontuário eletrônico veterinário")


def create_app():
    app = OpenAPI(__name__, info=info)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///petclinic.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.json.sort_keys = False

    db.init_app(app)
    CORS(app)

    from routes.tutores import bp_tutores
    from routes.animais import bp_animais
    from routes.consultas import bp_consultas

    app.register_api(bp_tutores)
    app.register_api(bp_animais)
    app.register_api(bp_consultas)

    @app.errorhandler(404)
    def nao_encontrado(e):
        return jsonify({"erro": "Rota não encontrada."}), 404

    @app.errorhandler(405)
    def metodo_nao_permitido(e):
        return jsonify({"erro": "Método HTTP não permitido nesta rota."}), 405

    @app.errorhandler(500)
    def erro_interno(e):
        return jsonify({"erro": "Erro interno no servidor."}), 500

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

- [ ] **Step 2: Verificar que o app sobe (as rotas ainda não existem, mas o app deve iniciar)**

Neste passo as rotas ainda não existem — o `from routes.tutores import bp_tutores` vai falhar. Crie os três arquivos de rotas como stubs temporários antes de rodar:

Criar `routes/tutores.py` stub:
```python
from flask_openapi3 import APIBlueprint
bp_tutores = APIBlueprint("tutores", __name__, url_prefix="/tutores")
```

Criar `routes/animais.py` stub:
```python
from flask_openapi3 import APIBlueprint
bp_animais = APIBlueprint("animais", __name__, url_prefix="/animais")
```

Criar `routes/consultas.py` stub:
```python
from flask_openapi3 import APIBlueprint
bp_consultas = APIBlueprint("consultas", __name__, url_prefix="/consultas")
```

Rodar:
```bash
cd /Users/paidoboris/Desktop/petclinic-api
source .venv/bin/activate
python app.py
```

Resultado esperado: `* Running on http://127.0.0.1:5000` sem erros. `petclinic.db` criado. Swagger em `http://localhost:5000/openapi/swagger`.

- [ ] **Step 3: Commit**

```bash
git -C /Users/paidoboris/Desktop/petclinic-api add app.py routes/tutores.py routes/animais.py routes/consultas.py
git -C /Users/paidoboris/Desktop/petclinic-api commit -m "feat: app factory com OpenAPI, CORS e error handlers"
```

---

## Task 7: routes/tutores.py (5 rotas)

**Files:**
- Modify: `routes/tutores.py` (substituir stub)

Schemas Pydantic ficam no próprio arquivo de rotas.

- [ ] **Step 1: Escrever routes/tutores.py completo**

```python
from flask import jsonify
from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel
from models.base import db
from models.tutor import Tutor
from models.animal import Animal

tag = Tag(name="Tutores", description="Gerenciamento de tutores e seus animais")
bp_tutores = APIBlueprint("tutores", __name__, url_prefix="/tutores")


class TutorBody(BaseModel):
    nome: str
    telefone: str
    email: str | None = None
    cpf: str | None = None


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
```

- [ ] **Step 2: Verificar no Swagger**

```bash
python app.py
```

Abrir `http://localhost:5000/openapi/swagger` — verificar que as 5 rotas de tutores aparecem documentadas.

Testar via Swagger:
1. `POST /tutores` com `{"nome": "Maria", "telefone": "21 9999-0000"}`  → 201
2. `GET /tutores` → 200, lista com 1 tutor
3. `GET /tutores/1` → 200, tutor retornado
4. `GET /tutores/999` → 404
5. `GET /tutores/1/animais` → 200, `"animais": []`
6. `DELETE /tutores/1` → 200

- [ ] **Step 3: Commit**

```bash
git -C /Users/paidoboris/Desktop/petclinic-api add routes/tutores.py
git -C /Users/paidoboris/Desktop/petclinic-api commit -m "feat: rotas de tutores com Swagger (POST, GET, DELETE)"
```

---

## Task 8: routes/animais.py (5 rotas)

**Files:**
- Modify: `routes/animais.py` (substituir stub)

- [ ] **Step 1: Escrever routes/animais.py completo**

```python
from datetime import date
from flask import jsonify, request
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
    raca: str | None = None
    sexo: str | None = None
    peso_kg: float | None = None
    data_nascimento: date | None = None


class AnimalPath(BaseModel):
    animal_id: int


class AnimalQuery(BaseModel):
    especie: str | None = None


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
```

- [ ] **Step 2: Verificar no Swagger**

Reiniciar o servidor e testar:
1. `POST /tutores` para criar tutor (id=1)
2. `POST /animais` com `{"nome": "Rex", "especie": "cachorro", "tutor_id": 1, "data_nascimento": "2022-05-10"}` → 201, campo `"idade"` calculado
3. `GET /animais?especie=cachorro` → 200, filtra corretamente
4. `GET /animais/1` → 200, inclui `tutor_nome`
5. `GET /animais/1/consultas` → 200, `"consultas": []`
6. `DELETE /animais/1` → 200

- [ ] **Step 3: Commit**

```bash
git -C /Users/paidoboris/Desktop/petclinic-api add routes/animais.py
git -C /Users/paidoboris/Desktop/petclinic-api commit -m "feat: rotas de animais com filtro por espécie e histórico"
```

---

## Task 9: routes/consultas.py (1 rota)

**Files:**
- Modify: `routes/consultas.py` (substituir stub)

- [ ] **Step 1: Escrever routes/consultas.py completo**

```python
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
    diagnostico: str | None = None
    tratamento: str | None = None
    veterinario: str | None = None


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
```

- [ ] **Step 2: Verificar fluxo completo no Swagger**

Testar o fluxo ponta a ponta:
1. `POST /tutores` → cria tutor (id=1)
2. `POST /animais` → cria animal vinculado ao tutor (id=1)
3. `POST /consultas` com `{"animal_id": 1, "motivo": "Vacina anual", "veterinario": "Dr. João"}` → 201
4. `GET /animais/1/consultas` → retorna a consulta registrada com `data_consulta` preenchida automaticamente
5. `GET /tutores/1/animais` → retorna o animal com dados do tutor
6. `DELETE /tutores/1` → remove tutor + cascata remove animal + consulta (verificar com `GET /animais/1` → 404)

- [ ] **Step 3: Commit**

```bash
git -C /Users/paidoboris/Desktop/petclinic-api add routes/consultas.py
git -C /Users/paidoboris/Desktop/petclinic-api commit -m "feat: rota POST /consultas — prontuário clínico completo"
```

---

## Task 10: README.md + commit final

**Files:**
- Create: `README.md`

- [ ] **Step 1: Criar README.md**

```markdown
# PetClinic API

API REST para gerenciamento de prontuários eletrônicos veterinários. Permite cadastrar tutores, seus animais e o histórico de consultas clínicas de cada paciente.

## Problema

Clínicas veterinárias de pequeno e médio porte gerenciam pacientes em papel ou planilhas, causando perda de histórico clínico e impossibilidade de busca rápida por paciente.

## Pré-requisitos

- Python 3.10 ou superior
- pip

## Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd petclinic-api

# Crie e ative o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt
```

## Execução

```bash
python app.py
```

A API estará disponível em `http://localhost:5000`.

## Documentação Swagger

Acesse `http://localhost:5000/openapi/swagger` para a documentação interativa de todas as rotas.

## Rotas disponíveis

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/tutores` | Cadastra novo tutor |
| GET | `/tutores` | Lista todos os tutores |
| GET | `/tutores/<id>` | Busca tutor por ID |
| DELETE | `/tutores/<id>` | Remove tutor (e seus animais) |
| GET | `/tutores/<id>/animais` | Lista animais de um tutor |
| POST | `/animais` | Cadastra animal vinculado a tutor |
| GET | `/animais` | Lista animais (filtrável por `?especie=`) |
| GET | `/animais/<id>` | Busca animal com dados do tutor |
| DELETE | `/animais/<id>` | Remove animal (e suas consultas) |
| GET | `/animais/<id>/consultas` | Histórico clínico do animal |
| POST | `/consultas` | Registra nova consulta clínica |

## Estrutura do projeto

```
petclinic-api/
├── app.py
├── requirements.txt
├── models/
│   ├── base.py
│   ├── tutor.py
│   ├── animal.py
│   └── consulta.py
└── routes/
    ├── tutores.py
    ├── animais.py
    └── consultas.py
```
```

- [ ] **Step 2: Commit final**

```bash
git -C /Users/paidoboris/Desktop/petclinic-api add README.md
git -C /Users/paidoboris/Desktop/petclinic-api commit -m "docs: README com instruções de instalação e execução"
```

- [ ] **Step 3: Verificação final**

Confirmar que todos os requisitos estão cobertos:
- [ ] Mínimo 4 rotas Flask/Python com pelo menos 1 POST → 11 rotas, 3 POSTs
- [ ] SQLite com tabelas → 3 tabelas
- [ ] Swagger acessível em `/openapi/swagger`
- [ ] Cascade delete funcionando (DELETE tutor remove animais e consultas)
- [ ] `data_nascimento` como `Date`, `data_consulta`/`data_cadastro` como `DateTime`
- [ ] Idade calculada no `to_dict()` do Animal
- [ ] CORS habilitado (`flask-cors`)
- [ ] README com título, descrição, instalação, execução
