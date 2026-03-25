# PetClinic App — Frontend Design Spec

**Data:** 2026-03-24
**Projeto:** petclinic-app (repositório separado)
**Stack:** HTML5 + CSS3 + JavaScript puro (sem frameworks JS)
**Estilo:** Clean & Profissional — azul/branco
**Layout:** Dashboard com cards de acesso rápido

---

## Problema

O backend PetClinic API já está implementado e funcional. É necessário um frontend SPA que consuma todas as 11 rotas da API para gerenciar tutores, animais e consultas clínicas veterinárias.

---

## Restrições Obrigatórias (MVP PUC)

- **Sem frameworks JS** — proibido Angular, Vue, React (penalização de 1,5 pt)
- **Abre via index.html** — sem servidor local, sem extensões (penalização de 2 pts)
- **Bootstrap via CDN** permitido + CSS customizado obrigatório
- **Exibir dados em lista ou cards**
- **Chamar todas as rotas da API**
- **Repositório público separado no GitHub** com README.md

---

## Estrutura de Arquivos

```
petclinic-app/
├── index.html       — SPA única
├── css/
│   └── style.css    — estilos customizados (complementa Bootstrap)
├── js/
│   ├── api.js       — funções fetch para cada rota da API
│   └── app.js       — navegação, renderização, event listeners
└── README.md
```

---

## Seções da SPA

### Home — Dashboard
- 3 cards clicáveis: Tutores, Animais, Consultas
- Cada card exibe contador em tempo real (GET /tutores, GET /animais)
- Cores distintas por seção: azul (tutores), verde (animais), roxo (consultas)
- Clique no card navega para a seção correspondente

### Seção Tutores
- Lista de tutores (nome, telefone, CPF, data de cadastro)
- Botão "Novo Tutor" abre formulário inline (nome, telefone, email, CPF)
- Cada item: botão "Ver Animais" e botão "Excluir" (com confirmação)
- "Ver Animais" expande inline a lista de animais do tutor

### Seção Animais
- Cards com: nome, espécie, raça, idade calculada, nome do tutor
- Filtro por espécie (campo de texto + botão buscar)
- Botão "Novo Animal" com formulário (todos os campos do model)
- Cada card: botão "Ver Consultas" e botão "Excluir"
- "Ver Consultas" exibe lista de consultas do animal em modal ou expansão inline

### Seção Consultas
- Formulário de nova consulta (select de animal por ID/nome, motivo obrigatório, diagnóstico, tratamento, veterinário)
- Lista das consultas registradas exibida em cards (animal, data, motivo, veterinário)

---

## Rotas da API Cobertas

| Rota | Método | Onde chamada |
|------|--------|-------------|
| `/tutores` | GET | Dashboard (contador) + listagem Tutores |
| `/tutores` | POST | Formulário novo tutor |
| `/tutores/:id` | GET | Detalhe do tutor |
| `/tutores/:id` | DELETE | Botão excluir tutor |
| `/tutores/:id/animais` | GET | Botão "Ver Animais" |
| `/animais` | GET | Dashboard (contador) + listagem Animais |
| `/animais` | POST | Formulário novo animal |
| `/animais/:id` | GET | Detalhe do animal |
| `/animais/:id` | DELETE | Botão excluir animal |
| `/animais/:id/consultas` | GET | Botão "Ver Consultas" |
| `/consultas` | POST | Formulário nova consulta |

---

## API Base URL

```javascript
const API_BASE = 'http://localhost:5001';
```

Configurável no topo de `api.js` para facilitar troca de ambiente.

---

## Navegação SPA

Implementada via hash routing (`window.location.hash`):
- `#home` — Dashboard
- `#tutores` — Seção tutores
- `#animais` — Seção animais
- `#consultas` — Seção consultas

`window.addEventListener('hashchange', render)` troca o conteúdo visível sem recarregar a página.

---

## Feedback ao Usuário

- Loading state durante fetch (spinner ou texto "Carregando...")
- Mensagens de sucesso inline após POST (verde)
- Mensagens de erro inline após falha (vermelho, exibe `erro` do JSON)
- Confirmação antes de DELETE ("Tem certeza?")

---

## README.md do Frontend

Conterá: título, descrição, pré-requisitos (apenas browser moderno), como usar (abrir index.html), URL da API necessária, estrutura de arquivos.
