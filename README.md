# 🤖 FRC Concept Scorer

App para ajudar equipes de FRC a escolher o melhor conceito de robô pra próxima temporada, usando pontuação ponderada em múltiplos critérios.

## Como funciona

Cada conceito recebe notas de 0-10 em 4 critérios:
- **Potencial de pontos** (maior = melhor)
- **Complexidade** (menor = melhor)
- **Risco** (menor = melhor)
- **Recursos necessários** (menor = melhor)

O app calcula um **score final** (média ponderada) e mostra um ranking. Você pode ajustar os pesos pra refletir o que importa mais pra sua equipe.

## Demo online

Acesse via GitHub Pages: **https://franco12345.github.io/frc-concept-scorer/**

## Rodar localmente

### App web estático (igual ao que está no GitHub Pages)

```bash
python -m http.server 8000
# abre http://localhost:8000/templates/index.html
```

Ou abra `templates/index.html` direto no navegador — funciona offline (dados no localStorage).

### Servidor Flask (dev)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python app.py
# abre http://localhost:5050
```

## Testes

```bash
pytest test_scorer.py -v
# ou sem pytest: python test_scorer.py
```

## CI/CD

- Todo PR/push em `main` roda **ruff** (lint) + **pytest** (testes).
- Push direto em `main` que passa no CI faz **deploy automático** no GitHub Pages.
- Workflow: `.github/workflows/ci.yml`

## Estrutura

```
app.py               # Flask dev server (opcional, dados em data.json)
scorer.py            # Lógica pura de scoring (compartilhada com JS)
static/app.js        # Versão client-side (localStorage, sem backend)
static/style.css     # Visual
templates/index.html # UI
test_scorer.py       # Testes da lógica
.github/workflows/   # CI/CD
```

## Próximas ideias

- 📊 Radar chart por conceito
- 🗳️ Votação por membro da equipe
- 📤 Exportar ranking como CSV/Markdown
- � PWA pra usar offline na reunião
