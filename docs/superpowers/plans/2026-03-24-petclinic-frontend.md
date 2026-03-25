# PetClinic App — Frontend Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a SPA em HTML/CSS/JavaScript puro que consuma todas as 11 rotas da PetClinic API e abra diretamente via `index.html` no browser, sem servidor.

**Architecture:** Hash routing (`#home`, `#tutores`, `#animais`, `#consultas`) com `hashchange` event para navegação. `api.js` centraliza todos os fetches. `app.js` contém renderização e event listeners. Bootstrap 5 via CDN + `style.css` customizado.

**Tech Stack:** HTML5, CSS3, JavaScript ES6+, Bootstrap 5.3 (CDN), PetClinic API em `http://localhost:5001`

---

## File Map

| Arquivo | Responsabilidade |
|---------|-----------------|
| `index.html` | Estrutura base da SPA, importa Bootstrap CDN, `style.css`, `api.js`, `app.js` |
| `css/style.css` | Estilos customizados: dashboard cards, lista tutores, cards animais/consultas, feedback messages |
| `js/api.js` | Uma função por rota da API (11 funções fetch), constante `API_BASE` |
| `js/app.js` | Hash router, funções de renderização por seção, event delegation |
| `README.md` | Título, descrição, como usar (abrir index.html), URL da API |

---

## Task 1: Estrutura do repositório e index.html base

**Files:**
- Create: `index.html`
- Create: `css/style.css` (vazio por enquanto)
- Create: `js/api.js` (vazio por enquanto)
- Create: `js/app.js` (vazio por enquanto)

- [ ] **Step 1: Criar diretórios**

```bash
mkdir petclinic-app
cd petclinic-app
mkdir css js
git init
```

- [ ] **Step 2: Criar index.html**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PetClinic Manager</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>

  <nav class="navbar navbar-dark bg-primary">
    <div class="container-fluid">
      <a class="navbar-brand fw-bold" href="#home">🐾 PetClinic Manager</a>
      <div class="nav-links">
        <a href="#tutores" class="nav-link text-white">Tutores</a>
        <a href="#animais" class="nav-link text-white">Animais</a>
        <a href="#consultas" class="nav-link text-white">Consultas</a>
      </div>
    </div>
  </nav>

  <div class="container py-4" id="app">
    <!-- conteúdo renderizado via JS -->
  </div>

  <script src="js/api.js"></script>
  <script src="js/app.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

- [ ] **Step 3: Criar arquivos vazios**

```bash
touch css/style.css js/api.js js/app.js
```

- [ ] **Step 4: Criar .gitignore**

```
.DS_Store
```

- [ ] **Step 5: Verificar no browser**

Abrir `index.html` diretamente no browser. Resultado esperado: navbar azul com "🐾 PetClinic Manager" visível, área vazia abaixo.

- [ ] **Step 6: Commit**

```bash
git add index.html css/style.css js/api.js js/app.js .gitignore
git commit -m "chore: estrutura inicial do projeto frontend"
```

---

## Task 2: api.js — funções fetch para todas as 11 rotas

**Files:**
- Modify: `js/api.js`

- [ ] **Step 1: Escrever api.js completo**

```javascript
const API_BASE = 'http://localhost:5001';

async function getTutores() {
  const r = await fetch(`${API_BASE}/tutores`);
  return r.json();
}

async function getTutor(id) {
  const r = await fetch(`${API_BASE}/tutores/${id}`);
  return r.json();
}

async function postTutor(dados) {
  const r = await fetch(`${API_BASE}/tutores`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dados)
  });
  return r.json();
}

async function deleteTutor(id) {
  const r = await fetch(`${API_BASE}/tutores/${id}`, { method: 'DELETE' });
  return r.json();
}

async function getAnimaisTutor(tutorId) {
  const r = await fetch(`${API_BASE}/tutores/${tutorId}/animais`);
  return r.json();
}

async function getAnimais(especie = '') {
  const url = especie
    ? `${API_BASE}/animais?especie=${encodeURIComponent(especie)}`
    : `${API_BASE}/animais`;
  const r = await fetch(url);
  return r.json();
}

async function getAnimal(id) {
  const r = await fetch(`${API_BASE}/animais/${id}`);
  return r.json();
}

async function postAnimal(dados) {
  const r = await fetch(`${API_BASE}/animais`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dados)
  });
  return r.json();
}

async function deleteAnimal(id) {
  const r = await fetch(`${API_BASE}/animais/${id}`, { method: 'DELETE' });
  return r.json();
}

async function getConsultasAnimal(animalId) {
  const r = await fetch(`${API_BASE}/animais/${animalId}/consultas`);
  return r.json();
}

async function postConsulta(dados) {
  const r = await fetch(`${API_BASE}/consultas`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dados)
  });
  return r.json();
}
```

- [ ] **Step 2: Verificar no console do browser**

Abrir `index.html`, abrir DevTools > Console, digitar:
```javascript
getTutores().then(console.log)
```
Resultado esperado: `{total: 0, tutores: []}` (ou dados existentes se API tiver dados).

Se aparecer erro CORS: verificar se o backend está rodando em `http://localhost:5001`.

- [ ] **Step 3: Commit**

```bash
git add js/api.js
git commit -m "feat: api.js com as 11 funções fetch da PetClinic API"
```

---

## Task 3: css/style.css — estilos customizados

**Files:**
- Modify: `css/style.css`

- [ ] **Step 1: Escrever style.css**

```css
/* Layout geral */
body {
  background-color: #f0f4f8;
  font-family: 'Segoe UI', system-ui, sans-serif;
}

.navbar .nav-links {
  display: flex;
  gap: 8px;
}

/* Dashboard cards */
.dashboard-card {
  border: none;
  border-radius: 12px;
  padding: 28px 24px;
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
  text-decoration: none;
  display: block;
}

.dashboard-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.dashboard-card .counter {
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 4px;
}

.dashboard-card .label {
  font-size: 1rem;
  opacity: 0.85;
}

.card-tutores { background: #1d4ed8; color: white; }
.card-animais { background: #15803d; color: white; }
.card-consultas { background: #7e22ce; color: white; }

/* Seção header */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

/* Tutor list item */
.tutor-item {
  background: white;
  border-radius: 8px;
  padding: 14px 16px;
  margin-bottom: 10px;
  border-left: 4px solid #1d4ed8;
  display: flex;
  align-items: center;
  gap: 12px;
}

.tutor-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #dbeafe;
  color: #1d4ed8;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.tutor-info { flex: 1; }
.tutor-info .nome { font-weight: 600; color: #1e3a5f; }
.tutor-info .detalhe { font-size: 0.82rem; color: #6b7280; }

.tutor-actions { display: flex; gap: 6px; }

.animais-expandidos {
  background: #eff6ff;
  border-radius: 0 0 8px 8px;
  padding: 10px 16px;
  margin-top: -10px;
  margin-bottom: 10px;
  display: none;
}

.animais-expandidos.aberto { display: block; }

/* Animal cards */
.animal-card {
  background: white;
  border-radius: 10px;
  padding: 16px;
  border-top: 4px solid #15803d;
  height: 100%;
}

.animal-card .especie-badge {
  background: #dcfce7;
  color: #15803d;
  font-size: 0.75rem;
  padding: 2px 8px;
  border-radius: 20px;
  font-weight: 600;
}

.animal-card .idade {
  font-size: 0.8rem;
  color: #6b7280;
}

/* Consulta cards */
.consulta-card {
  background: white;
  border-radius: 10px;
  padding: 16px;
  border-left: 4px solid #7e22ce;
  margin-bottom: 12px;
}

.consulta-card .data {
  font-size: 0.78rem;
  color: #9ca3af;
}

/* Formulário inline */
.form-inline-box {
  background: white;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 20px;
  border: 2px dashed #bfdbfe;
  display: none;
}

.form-inline-box.aberto { display: block; }

/* Feedback messages */
.feedback {
  padding: 10px 14px;
  border-radius: 6px;
  margin-bottom: 12px;
  font-size: 0.88rem;
  display: none;
}

.feedback.sucesso { background: #dcfce7; color: #15803d; display: block; }
.feedback.erro { background: #fee2e2; color: #b91c1c; display: block; }

/* Loading */
.loading {
  text-align: center;
  padding: 40px;
  color: #9ca3af;
}
```

- [ ] **Step 2: Verificar no browser**

Reabrir `index.html`. Navbar deve estar estilizada. Não há mais conteúdo a verificar ainda.

- [ ] **Step 3: Commit**

```bash
git add css/style.css
git commit -m "feat: estilos customizados — dashboard, tutores, animais, consultas"
```

---

## Task 4: app.js — hash router e seção Home (dashboard)

**Files:**
- Modify: `js/app.js`

- [ ] **Step 1: Escrever o router e a seção Home**

```javascript
const app = document.getElementById('app');

function mostrarFeedback(el, msg, tipo) {
  el.className = `feedback ${tipo}`;
  el.textContent = msg;
  setTimeout(() => { el.className = 'feedback'; }, 4000);
}

async function renderHome() {
  app.innerHTML = '<div class="loading">Carregando...</div>';
  const [tutoresData, animaisData] = await Promise.all([
    getTutores(),
    getAnimais()
  ]);
  const totalTutores = tutoresData.total ?? 0;
  const totalAnimais = animaisData.total ?? 0;

  app.innerHTML = `
    <h4 class="mb-4 text-secondary">Painel de Controle</h4>
    <div class="row g-4">
      <div class="col-md-4">
        <a href="#tutores" class="dashboard-card card-tutores">
          <div class="counter">${totalTutores}</div>
          <div class="label">👥 Tutores cadastrados</div>
        </a>
      </div>
      <div class="col-md-4">
        <a href="#animais" class="dashboard-card card-animais">
          <div class="counter">${totalAnimais}</div>
          <div class="label">🐾 Animais pacientes</div>
        </a>
      </div>
      <div class="col-md-4">
        <a href="#consultas" class="dashboard-card card-consultas">
          <div class="counter">+</div>
          <div class="label">📋 Registrar consulta</div>
        </a>
      </div>
    </div>
  `;
}

async function render() {
  const hash = window.location.hash || '#home';
  if (hash === '#home' || hash === '#') return renderHome();
  if (hash === '#tutores') return renderTutores();
  if (hash === '#animais') return renderAnimais();
  if (hash === '#consultas') return renderConsultas();
  return renderHome();
}

window.addEventListener('hashchange', render);
window.addEventListener('load', render);
```

- [ ] **Step 2: Verificar no browser**

Abrir `index.html` com backend rodando (`python app.py` no repo `petclinic-api`). Resultado esperado: dashboard com 3 cards coloridos mostrando contadores reais da API. Clicar nos links da navbar deve mudar o hash (haverá erro de `renderTutores is not defined` — normal, ainda não implementado).

- [ ] **Step 3: Commit**

```bash
git add js/app.js
git commit -m "feat: hash router e dashboard com contadores da API"
```

---

## Task 5: Seção Tutores

**Files:**
- Modify: `js/app.js` (adicionar `renderTutores` e funções auxiliares)

- [ ] **Step 1: Adicionar renderTutores ao app.js**

Adicionar no final do `js/app.js`:

```javascript
async function renderTutores() {
  app.innerHTML = '<div class="loading">Carregando tutores...</div>';
  const data = await getTutores();

  app.innerHTML = `
    <div class="section-header">
      <h4 class="mb-0">👥 Tutores</h4>
      <button class="btn btn-primary btn-sm" onclick="toggleForm('form-tutor')">+ Novo Tutor</button>
    </div>

    <div id="feedback-tutor" class="feedback"></div>

    <div class="form-inline-box" id="form-tutor">
      <h6 class="mb-3">Cadastrar Tutor</h6>
      <div class="row g-2">
        <div class="col-md-6">
          <input type="text" class="form-control form-control-sm" id="t-nome" placeholder="Nome *">
        </div>
        <div class="col-md-6">
          <input type="text" class="form-control form-control-sm" id="t-tel" placeholder="Telefone *">
        </div>
        <div class="col-md-6">
          <input type="email" class="form-control form-control-sm" id="t-email" placeholder="E-mail">
        </div>
        <div class="col-md-6">
          <input type="text" class="form-control form-control-sm" id="t-cpf" placeholder="CPF">
        </div>
      </div>
      <button class="btn btn-success btn-sm mt-3" onclick="salvarTutor()">Salvar</button>
    </div>

    <div id="lista-tutores">
      ${data.tutores.length === 0
        ? '<p class="text-muted">Nenhum tutor cadastrado.</p>'
        : data.tutores.map(t => renderTutorItem(t)).join('')}
    </div>
  `;
}

function renderTutorItem(t) {
  const inicial = t.nome.charAt(0).toUpperCase();
  return `
    <div class="tutor-item" id="tutor-${t.id}">
      <div class="tutor-avatar">${inicial}</div>
      <div class="tutor-info">
        <div class="nome">${t.nome}</div>
        <div class="detalhe">${t.telefone}${t.cpf ? ' · CPF: ' + t.cpf : ''}</div>
      </div>
      <div class="tutor-actions">
        <button class="btn btn-outline-primary btn-sm" onclick="verAnimaisTutor(${t.id})">Ver animais</button>
        <button class="btn btn-outline-danger btn-sm" onclick="excluirTutor(${t.id}, '${t.nome.replace(/'/g, "\\'")}')">Excluir</button>
      </div>
    </div>
    <div class="animais-expandidos" id="animais-tutor-${t.id}"></div>
  `;
}

function toggleForm(id) {
  const el = document.getElementById(id);
  el.classList.toggle('aberto');
}

async function salvarTutor() {
  const nome = document.getElementById('t-nome').value.trim();
  const telefone = document.getElementById('t-tel').value.trim();
  const email = document.getElementById('t-email').value.trim();
  const cpf = document.getElementById('t-cpf').value.trim();
  const fb = document.getElementById('feedback-tutor');

  if (!nome || !telefone) {
    return mostrarFeedback(fb, 'Nome e telefone são obrigatórios.', 'erro');
  }

  const dados = { nome, telefone };
  if (email) dados.email = email;
  if (cpf) dados.cpf = cpf;

  const res = await postTutor(dados);
  if (res.erro) return mostrarFeedback(fb, res.erro, 'erro');

  mostrarFeedback(fb, `Tutor "${res.tutor.nome}" cadastrado com sucesso!`, 'sucesso');
  renderTutores();
}

async function excluirTutor(id, nome) {
  if (!confirm(`Excluir tutor "${nome}" e todos os seus animais?`)) return;
  const res = await deleteTutor(id);
  if (res.erro) return alert(res.erro);
  renderTutores();
}

async function verAnimaisTutor(tutorId) {
  const container = document.getElementById(`animais-tutor-${tutorId}`);
  if (container.classList.contains('aberto')) {
    container.classList.remove('aberto');
    return;
  }
  container.innerHTML = 'Carregando...';
  container.classList.add('aberto');
  const data = await getAnimaisTutor(tutorId);
  if (!data.animais || data.animais.length === 0) {
    container.innerHTML = '<small class="text-muted">Nenhum animal cadastrado para este tutor.</small>';
    return;
  }
  container.innerHTML = data.animais.map(a =>
    `<span class="badge bg-primary me-1 mb-1">${a.nome} (${a.especie})</span>`
  ).join('');
}
```

- [ ] **Step 2: Verificar no browser**

Navegar para `#tutores`. Resultado esperado:
- Lista de tutores (ou mensagem vazia)
- Botão "+ Novo Tutor" abre formulário
- Cadastrar tutor → aparece na lista
- "Ver animais" → expande badges de animais
- "Excluir" → pede confirmação e remove

- [ ] **Step 3: Commit**

```bash
git add js/app.js
git commit -m "feat: seção Tutores — listagem, cadastro, exclusão e ver animais"
```

---

## Task 6: Seção Animais

**Files:**
- Modify: `js/app.js`

- [ ] **Step 1: Adicionar renderAnimais ao app.js**

Adicionar no final do `js/app.js`:

```javascript
async function renderAnimais(filtroEspecie = '') {
  app.innerHTML = '<div class="loading">Carregando animais...</div>';
  const data = await getAnimais(filtroEspecie);

  app.innerHTML = `
    <div class="section-header">
      <h4 class="mb-0">🐾 Animais</h4>
      <button class="btn btn-success btn-sm" onclick="toggleForm('form-animal')">+ Novo Animal</button>
    </div>

    <div id="feedback-animal" class="feedback"></div>

    <div class="form-inline-box" id="form-animal">
      <h6 class="mb-3">Cadastrar Animal</h6>
      <div class="row g-2">
        <div class="col-md-4">
          <input type="text" class="form-control form-control-sm" id="a-nome" placeholder="Nome *">
        </div>
        <div class="col-md-4">
          <input type="text" class="form-control form-control-sm" id="a-especie" placeholder="Espécie *">
        </div>
        <div class="col-md-4">
          <input type="number" class="form-control form-control-sm" id="a-tutor" placeholder="ID do Tutor *">
        </div>
        <div class="col-md-4">
          <input type="text" class="form-control form-control-sm" id="a-raca" placeholder="Raça">
        </div>
        <div class="col-md-2">
          <select class="form-select form-select-sm" id="a-sexo">
            <option value="">Sexo</option>
            <option value="M">M</option>
            <option value="F">F</option>
          </select>
        </div>
        <div class="col-md-3">
          <input type="number" step="0.1" class="form-control form-control-sm" id="a-peso" placeholder="Peso (kg)">
        </div>
        <div class="col-md-3">
          <input type="date" class="form-control form-control-sm" id="a-nasc">
        </div>
      </div>
      <button class="btn btn-success btn-sm mt-3" onclick="salvarAnimal()">Salvar</button>
    </div>

    <div class="d-flex gap-2 mb-3">
      <input type="text" class="form-control form-control-sm w-auto" id="filtro-especie"
             placeholder="Filtrar por espécie" value="${filtroEspecie}">
      <button class="btn btn-outline-secondary btn-sm" onclick="filtrarAnimais()">Buscar</button>
      ${filtroEspecie ? '<button class="btn btn-link btn-sm" onclick="renderAnimais()">Limpar</button>' : ''}
    </div>

    <div class="row g-3" id="lista-animais">
      ${data.animais.length === 0
        ? '<div class="col"><p class="text-muted">Nenhum animal encontrado.</p></div>'
        : data.animais.map(a => `
          <div class="col-md-4">
            <div class="animal-card">
              <div class="d-flex justify-content-between align-items-start mb-2">
                <strong>${a.nome}</strong>
                <span class="especie-badge">${a.especie}</span>
              </div>
              ${a.raca ? `<div class="text-muted small">${a.raca}</div>` : ''}
              <div class="idade">${a.idade ?? ''} ${a.peso_kg ? '· ' + a.peso_kg + ' kg' : ''}</div>
              <div class="small text-muted mt-1">Tutor: ${a.tutor_nome}</div>
              <div class="d-flex gap-2 mt-3">
                <button class="btn btn-outline-success btn-sm flex-fill" onclick="verConsultasAnimal(${a.id}, '${a.nome.replace(/'/g, "\\'")}')">Consultas</button>
                <button class="btn btn-outline-danger btn-sm" onclick="excluirAnimal(${a.id}, '${a.nome.replace(/'/g, "\\'")}')">✕</button>
              </div>
            </div>
          </div>
        `).join('')}
    </div>
  `;
}

function filtrarAnimais() {
  const especie = document.getElementById('filtro-especie').value.trim();
  renderAnimais(especie);
}

async function salvarAnimal() {
  const nome = document.getElementById('a-nome').value.trim();
  const especie = document.getElementById('a-especie').value.trim();
  const tutor_id = parseInt(document.getElementById('a-tutor').value);
  const fb = document.getElementById('feedback-animal');

  if (!nome || !especie || !tutor_id) {
    return mostrarFeedback(fb, 'Nome, espécie e ID do tutor são obrigatórios.', 'erro');
  }

  const dados = { nome, especie, tutor_id };
  const raca = document.getElementById('a-raca').value.trim();
  const sexo = document.getElementById('a-sexo').value;
  const peso = document.getElementById('a-peso').value;
  const nasc = document.getElementById('a-nasc').value;
  if (raca) dados.raca = raca;
  if (sexo) dados.sexo = sexo;
  if (peso) dados.peso_kg = parseFloat(peso);
  if (nasc) dados.data_nascimento = nasc;

  const res = await postAnimal(dados);
  if (res.erro) return mostrarFeedback(fb, res.erro, 'erro');

  mostrarFeedback(fb, `Animal "${res.animal.nome}" cadastrado com sucesso!`, 'sucesso');
  renderAnimais();
}

async function excluirAnimal(id, nome) {
  if (!confirm(`Excluir animal "${nome}"?`)) return;
  const res = await deleteAnimal(id);
  if (res.erro) return alert(res.erro);
  renderAnimais();
}

async function verConsultasAnimal(animalId, nomeAnimal) {
  const data = await getConsultasAnimal(animalId);
  const consultas = data.consultas ?? [];
  const msg = consultas.length === 0
    ? `${nomeAnimal} não tem consultas registradas.`
    : consultas.map(c =>
        `• ${c.data_consulta} — ${c.motivo}${c.veterinario ? ' (' + c.veterinario + ')' : ''}`
      ).join('\n');
  alert(msg);
}
```

- [ ] **Step 2: Verificar no browser**

Navegar para `#animais`. Resultado esperado:
- Cards de animais com espécie, idade, tutor
- Filtro por espécie funciona
- Formulário de novo animal com todos os campos
- Botão "Consultas" exibe alert com histórico
- "✕" exclui com confirmação

- [ ] **Step 3: Commit**

```bash
git add js/app.js
git commit -m "feat: seção Animais — cards, filtro por espécie, cadastro e exclusão"
```

---

## Task 7: Seção Consultas

**Files:**
- Modify: `js/app.js`

- [ ] **Step 1: Adicionar renderConsultas ao app.js**

Adicionar no final do `js/app.js`:

```javascript
async function renderConsultas() {
  app.innerHTML = '<div class="loading">Carregando...</div>';
  const animaisData = await getAnimais();

  app.innerHTML = `
    <div class="section-header">
      <h4 class="mb-0">📋 Registrar Consulta</h4>
    </div>

    <div id="feedback-consulta" class="feedback"></div>

    <div class="form-inline-box aberto" id="form-consulta">
      <div class="row g-2">
        <div class="col-md-4">
          <label class="form-label small">Animal *</label>
          <select class="form-select form-select-sm" id="c-animal">
            <option value="">Selecione...</option>
            ${animaisData.animais.map(a =>
              `<option value="${a.id}">${a.nome} (${a.especie})</option>`
            ).join('')}
          </select>
        </div>
        <div class="col-md-8">
          <label class="form-label small">Motivo *</label>
          <input type="text" class="form-control form-control-sm" id="c-motivo" placeholder="Motivo da consulta">
        </div>
        <div class="col-md-6">
          <label class="form-label small">Diagnóstico</label>
          <textarea class="form-control form-control-sm" id="c-diagnostico" rows="2"></textarea>
        </div>
        <div class="col-md-6">
          <label class="form-label small">Tratamento</label>
          <textarea class="form-control form-control-sm" id="c-tratamento" rows="2"></textarea>
        </div>
        <div class="col-md-6">
          <label class="form-label small">Veterinário</label>
          <input type="text" class="form-control form-control-sm" id="c-vet" placeholder="Nome do veterinário">
        </div>
      </div>
      <button class="btn btn-purple btn-sm mt-3" style="background:#7e22ce;color:white" onclick="salvarConsulta()">
        Registrar Consulta
      </button>
    </div>

    <div id="lista-consultas-recentes"></div>
  `;

  if (animaisData.animais.length > 0) {
    carregarConsultasRecentes(animaisData.animais);
  }
}

async function carregarConsultasRecentes(animais) {
  const container = document.getElementById('lista-consultas-recentes');
  if (!container) return;
  container.innerHTML = '<h6 class="mt-4 mb-3 text-secondary">Consultas por animal:</h6>';

  for (const animal of animais.slice(0, 5)) {
    const data = await getConsultasAnimal(animal.id);
    if (data.consultas && data.consultas.length > 0) {
      data.consultas.slice(0, 2).forEach(c => {
        container.innerHTML += `
          <div class="consulta-card">
            <div class="d-flex justify-content-between">
              <strong>${animal.nome}</strong>
              <span class="data">${c.data_consulta}</span>
            </div>
            <div class="mt-1">${c.motivo}</div>
            ${c.veterinario ? `<div class="small text-muted">${c.veterinario}</div>` : ''}
            ${c.diagnostico ? `<div class="small mt-1 text-secondary">${c.diagnostico}</div>` : ''}
          </div>
        `;
      });
    }
  }

  if (container.children.length === 1) {
    container.innerHTML += '<p class="text-muted">Nenhuma consulta registrada ainda.</p>';
  }
}

async function salvarConsulta() {
  const animal_id = parseInt(document.getElementById('c-animal').value);
  const motivo = document.getElementById('c-motivo').value.trim();
  const fb = document.getElementById('feedback-consulta');

  if (!animal_id || !motivo) {
    return mostrarFeedback(fb, 'Animal e motivo são obrigatórios.', 'erro');
  }

  const dados = { animal_id, motivo };
  const diag = document.getElementById('c-diagnostico').value.trim();
  const trat = document.getElementById('c-tratamento').value.trim();
  const vet = document.getElementById('c-vet').value.trim();
  if (diag) dados.diagnostico = diag;
  if (trat) dados.tratamento = trat;
  if (vet) dados.veterinario = vet;

  const res = await postConsulta(dados);
  if (res.erro) return mostrarFeedback(fb, res.erro, 'erro');

  mostrarFeedback(fb, 'Consulta registrada com sucesso!', 'sucesso');
  document.getElementById('c-animal').value = '';
  document.getElementById('c-motivo').value = '';
  document.getElementById('c-diagnostico').value = '';
  document.getElementById('c-tratamento').value = '';
  document.getElementById('c-vet').value = '';
  carregarConsultasRecentes((await getAnimais()).animais);
}
```

- [ ] **Step 2: Verificar no browser**

Navegar para `#consultas`. Resultado esperado:
- Formulário com select de animais populado
- Registrar consulta → mensagem de sucesso
- Lista de consultas recentes por animal aparece abaixo

- [ ] **Step 3: Commit**

```bash
git add js/app.js
git commit -m "feat: seção Consultas — formulário e histórico por animal"
```

---

## Task 8: README.md e commit final

**Files:**
- Create: `README.md`

- [ ] **Step 1: Criar README.md**

```markdown
# PetClinic Manager — Frontend

Interface web para o sistema de prontuário eletrônico veterinário PetClinic. Permite gerenciar tutores, animais e consultas clínicas consumindo a PetClinic API.

## Pré-requisitos

- Browser moderno (Chrome, Firefox, Edge, Safari)
- [PetClinic API](https://github.com/paulopacifico/petclinic-api) rodando em `http://localhost:5001`

## Como usar

1. Clone este repositório:
   ```bash
   git clone <url-deste-repositorio>
   cd petclinic-app
   ```

2. Inicie a PetClinic API (em outro terminal):
   ```bash
   cd petclinic-api
   source .venv/bin/activate
   python app.py
   ```

3. Abra `index.html` diretamente no browser — sem servidor necessário.

## Funcionalidades

| Seção | O que faz |
|-------|-----------|
| Dashboard | Contadores em tempo real de tutores e animais |
| Tutores | Listar, cadastrar, excluir tutores e ver seus animais |
| Animais | Cards de pacientes, filtro por espécie, cadastrar, excluir |
| Consultas | Registrar nova consulta, histórico por animal |

## Estrutura do projeto

```
petclinic-app/
├── index.html       — SPA principal
├── css/
│   └── style.css    — estilos customizados
├── js/
│   ├── api.js       — funções de acesso à API (11 rotas)
│   └── app.js       — navegação e renderização
└── README.md
```

## Rotas da API utilizadas

`GET /tutores` · `POST /tutores` · `GET /tutores/:id` · `DELETE /tutores/:id` · `GET /tutores/:id/animais` · `GET /animais` · `POST /animais` · `GET /animais/:id` · `DELETE /animais/:id` · `GET /animais/:id/consultas` · `POST /consultas`
```

- [ ] **Step 2: Verificar fluxo completo**

Com a API rodando, testar o fluxo ponta a ponta:
1. Home mostra contadores
2. Cadastrar tutor → aparece na lista
3. Cadastrar animal vinculado ao tutor
4. Filtrar animais por espécie
5. Registrar consulta para o animal
6. Ver consultas do animal
7. Excluir animal → some da lista
8. Excluir tutor → some da lista

- [ ] **Step 3: Commit final**

```bash
git add README.md
git commit -m "docs: README com instruções de uso e estrutura do projeto"
```

- [ ] **Step 4: Push para o repositório criado no GitHub**

```bash
git remote add origin <url-do-repo-petclinic-app>
git push -u origin main
```

---

## Checklist Final — Requisitos MVP PUC

- [ ] SPA em HTML + CSS + JavaScript (sem Angular/Vue/React)
- [ ] Abre via `index.html` diretamente no browser
- [ ] Bootstrap CDN + CSS customizado em `style.css`
- [ ] Elementos exibidos em lista (tutores) e cards (animais, consultas)
- [ ] Todas as 11 rotas da API chamadas
- [ ] Repositório público no GitHub com README.md
- [ ] Repositório separado do backend
