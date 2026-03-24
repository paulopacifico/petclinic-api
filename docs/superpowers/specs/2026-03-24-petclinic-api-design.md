# PetClinic API — Backend Design Spec

**Data:** 2026-03-24
**Projeto:** petclinic-api
**Stack:** Python · Flask · Flask-SQLAlchemy · Flask-CORS · Flask-OpenAPI3 · SQLite (pydantic v2)

---

## Problema

Clínicas veterinárias de pequeno e médio porte gerenciam pacientes em papel ou planilhas. Isso causa: histórico clínico perdido, impossibilidade de busca rápida e nenhum registro estruturado de diagnóstico e tratamento.

---

## Solução

API REST documentada com Swagger que serve como back-end de um prontuário eletrônico veterinário. Gerencia tutores, animais e consultas clínicas com relacionamentos em cascata e tratamento diferenciado de datas.

---

## Estrutura de Arquivos

```
petclinic-api/
├── app.py
├── requirements.txt
├── petclinic.db          (gerado em runtime — sqlite:///petclinic.db, caminho relativo)
├── README.md
├── models/
│   ├── __init__.py
│   ├── base.py
│   ├── tutor.py
│   ├── animal.py
│   └── consulta.py
└── routes/
    ├── tutores.py
    ├── animais.py
    └── consultas.py
```

---

## Banco de Dados — 3 tabelas SQLite

### TUTORES
| Campo | Tipo SQLAlchemy | Obrigatório (API) | Observação |
|-------|----------------|-------------------|------------|
| id | Integer PK | — | auto |
| nome | String(120) | sim | |
| telefone | String(20) | sim | |
| email | String(120) | não | |
| cpf | String(14) unique | não | sem validação de formato; qualquer string até 14 chars |
| data_cadastro | **DateTime** | — | setado pelo servidor (ORM default=lambda: datetime.now(timezone.utc)); nunca aceito do cliente |

### ANIMAIS
| Campo | Tipo SQLAlchemy | Obrigatório (API) | Observação |
|-------|----------------|-------------------|------------|
| id | Integer PK | — | auto |
| nome | String(80) | sim | |
| especie | String(40) | sim | |
| raca | String(80) | não | |
| sexo | String(1) | não | aceita apenas `"M"` ou `"F"`; outros valores retornam 400 |
| peso_kg | Float | não | |
| data_nascimento | **Date** (sem hora) | não | formato ISO `YYYY-MM-DD` na entrada |
| tutor_id | Integer FK | sim | |

### CONSULTAS
| Campo | Tipo SQLAlchemy | Obrigatório (API) | Observação |
|-------|----------------|-------------------|------------|
| id | Integer PK | — | auto |
| animal_id | Integer FK | sim | |
| data_consulta | **DateTime** | — | setado pelo servidor (ORM default=lambda: datetime.now(timezone.utc)); nunca aceito do cliente |
| motivo | String(200) | sim | |
| diagnostico | Text | não | |
| tratamento | Text | não | |
| veterinario | String(120) | não | |

### Relacionamentos
- `Tutor` 1:N `Animal` — `cascade="all, delete-orphan"`
- `Animal` 1:N `Consulta` — `cascade="all, delete-orphan"`

### Diferenciação de tipos de data (criatividade técnica)
- `data_cadastro` e `data_consulta` → `db.DateTime` (data + hora, UTC, auto-server)
- `data_nascimento` → `db.Date` (data pura, sem hora, enviada pelo cliente em ISO 8601)
- Idade do animal calculada em Python no `to_dict()` a partir de `date.today()`, retornada como string: `"3 anos e 2 meses"` / `"2 meses"` / `"1 ano"`. Chave JSON: `"idade"`.

---

## Shapes de Request e Response

### Pydantic Request Bodies (POST)

**POST /tutores**
```json
{
  "nome": "string (obrigatório)",
  "telefone": "string (obrigatório)",
  "email": "string (opcional)",
  "cpf": "string (opcional, máx 14 chars)"
}
```

**POST /animais**
```json
{
  "nome": "string (obrigatório)",
  "especie": "string (obrigatório)",
  "tutor_id": "integer (obrigatório)",
  "raca": "string (opcional)",
  "sexo": "'M' ou 'F' (opcional)",
  "peso_kg": "float (opcional)",
  "data_nascimento": "string ISO YYYY-MM-DD (opcional)"
}
```

**POST /consultas**
```json
{
  "animal_id": "integer (obrigatório)",
  "motivo": "string (obrigatório)",
  "diagnostico": "string (opcional)",
  "tratamento": "string (opcional)",
  "veterinario": "string (opcional)"
}
```

### Response shapes (to_dict)

**Tutor**
```json
{
  "id": 1,
  "nome": "João Silva",
  "telefone": "21 99999-0000",
  "email": "joao@email.com",
  "cpf": "123.456.789-00",
  "data_cadastro": "24/03/2026 14:30"
}
```

**Animal** (sempre inclui tutor_id e tutor_nome inline; nunca embed completo do Tutor)
```json
{
  "id": 1,
  "nome": "Rex",
  "especie": "cachorro",
  "raca": "Labrador",
  "sexo": "M",
  "peso_kg": 28.5,
  "data_nascimento": "10/05/2022",
  "idade": "3 anos e 10 meses",
  "tutor_id": 1,
  "tutor_nome": "João Silva"
}
```

Campos opcionais ausentes (`raca`, `sexo`, `peso_kg`, `data_nascimento`, `idade`) são sempre incluídos no JSON com valor `null` quando não fornecidos. Nenhum campo é omitido.

**Consulta**
```json
{
  "id": 1,
  "animal_id": 1,
  "animal_nome": "Rex",
  "data_consulta": "24/03/2026 14:30",
  "motivo": "Vacina anual",
  "diagnostico": "Animal saudável",
  "tratamento": "Vacina V10 aplicada",
  "veterinario": "Dra. Ana Lima"
}
```

### Response de erro (todos os handlers)
```json
{ "erro": "mensagem descritiva" }
```

### Response de DELETE (200 OK com body)
DELETE retorna 200 (intencional — body contém confirmação para o frontend):
```json
{ "mensagem": "Tutor 'João Silva' (id=1) removido com sucesso.", "id_removido": 1 }
```

---

## Rotas da API

### Tutores — `routes/tutores.py` (Blueprint `bp_tutores`, prefix `/tutores`)
| Método | Rota | Status |
|--------|------|--------|
| POST | `/tutores` | 201 / 400 / 409 |
| GET | `/tutores` | 200 |
| GET | `/tutores/<id>` | 200 / 404 |
| DELETE | `/tutores/<id>` | 200 / 404 |

### Animais — `routes/animais.py` (Blueprint `bp_animais`, prefix `/animais`)
| Método | Rota | Status | Detalhe |
|--------|------|--------|---------|
| POST | `/animais` | 201 / 400 / 404 | 404 se tutor_id não existe |
| GET | `/animais` | 200 | suporta `?especie=cachorro` — exact match case-insensitive (`ilike`) |
| GET | `/animais/<id>` | 200 / 404 | inclui tutor_id e tutor_nome inline |
| DELETE | `/animais/<id>` | 200 / 404 | |
| GET | `/animais/<id>/consultas` | 200 / 404 | registrada aqui; URL compatível com prefix `/animais` |

### Tutores (rotas extras em `routes/tutores.py`)
| Método | Rota | Status | Detalhe |
|--------|------|--------|---------|
| GET | `/tutores/<id>/animais` | 200 / 404 | registrada em `bp_tutores` (prefix `/tutores`) — URL compatível |

### Consultas — `routes/consultas.py` (Blueprint `bp_consultas`, prefix `/consultas`)
| Método | Rota | Status | Detalhe |
|--------|------|--------|---------|
| POST | `/consultas` | 201 / 400 / 404 | 404 se animal_id não existe |

Nota de implementação: cada rota pertence ao blueprint cujo `url_prefix` é compatível com o início da URL. Não há override de prefixo necessário.

---

## Configuração do App (`app.py`)

- App factory `create_app()`
- `SQLALCHEMY_DATABASE_URI = "sqlite:///petclinic.db"` (caminho relativo à raiz)
- CORS global com `flask-cors`
- `app.json.sort_keys = False`
- `db.create_all()` no contexto do app
- Error handlers globais: 404, 405, 500 — todos retornam `{"erro": "..."}` com status correspondente
- Swagger acessível em `http://localhost:5000/openapi/swagger`

---

## Dependências (`requirements.txt`)

```
flask==3.0.3
flask-cors==4.0.1
flask-sqlalchemy==3.1.1
flask-openapi3==3.1.0
pydantic==2.7.4
```

Nota: `flask-openapi3` 3.x requer pydantic v2. Usar API pydantic v2 (`model_fields`, `model_config`, etc.).

---

## Restrições de Nota Atendidas

| Requisito | Como atendido |
|-----------|--------------|
| 4+ rotas Flask/Python | 11 rotas |
| Pelo menos 1 POST | POST /tutores, /animais, /consultas |
| SQLite com tabela | 3 tabelas relacionadas |
| Swagger completo | flask-openapi3 + schemas Pydantic com request/response/status codes |
| Criatividade | datas diferenciadas (DateTime vs Date), idade calculada em Python, filtro espécie, JOIN animal+tutor, cascade delete, 3 tabelas, 11 rotas |
| Organização | modular com Blueprints, app factory |

---

## README.md

Conterá: título, descrição do problema resolvido, pré-requisitos (Python 3.10+), instalação (`pip install -r requirements.txt`), inicialização (`python app.py`), link do Swagger (`http://localhost:5000/openapi/swagger`), estrutura de pastas.
