# PetClinic API

Back-end do sistema de prontuário eletrônico veterinário PetClinic Manager.
Permite cadastrar tutores, animais e consultas clínicas por meio de uma API REST documentada com Swagger.

## Tecnologias

- Python 3.11+
- Flask 3.0
- Flask-SQLAlchemy (ORM)
- Flask-OpenAPI3 (Swagger UI)
- Flask-CORS
- SQLite

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/petclinic-api.git
cd petclinic-api
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## Como executar

```bash
python app.py
```

A API estará disponível em: `http://localhost:5000`

A documentação Swagger estará em: `http://localhost:5000/openapi/swagger`

## Estrutura do projeto

```
petclinic-api/
├── app.py              # Ponto de entrada e factory da aplicação
├── models/
│   ├── __init__.py     # Registra todos os models
│   ├── base.py         # Instância compartilhada do SQLAlchemy
│   ├── tutor.py        # Model Tutor
│   ├── animal.py       # Model Animal
│   └── consulta.py     # Model Consulta
├── routes/             # Blueprints com as rotas (Fases 2 e 3)
├── requirements.txt
└── petclinic.db        # Gerado automaticamente na primeira execução
```

## Tabelas do banco de dados

| Tabela | Descrição |
|---|---|
| `tutores` | Responsáveis legais pelos animais |
| `animais` | Pacientes veterinários vinculados a um tutor |
| `consultas` | Prontuário clínico de cada animal |
