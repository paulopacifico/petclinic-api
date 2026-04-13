# PetClinic API

API REST para gerenciamento de prontuários eletrônicos veterinários. Permite cadastrar tutores, seus animais e o histórico de consultas clínicas de cada paciente.

## Problema

Clínicas veterinárias de pequeno e médio porte gerenciam pacientes em papel ou planilhas, causando perda de histórico clínico e impossibilidade de busca rápida por paciente.

## Pré-requisitos

- Python 3.9 ou superior
- pip

## Instalação

```bash
# Clone o repositório
git clone https://github.com/paulopacifico/petclinic-api
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

A API estará disponível em `http://localhost:5001`.

## Documentação Swagger

Acesse `http://localhost:5001/openapi/swagger` para a documentação interativa de todas as rotas.

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
