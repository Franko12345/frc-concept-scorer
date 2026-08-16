// Client-side port of scorer.py — used by GitHub Pages deploy (no backend).
// Persistence: localStorage. Logic MUST stay in sync with scorer.py.
const STORAGE_KEY = "frc-concept-scorer-v1";

const INVERTED = {
  pontos_potenciais: false,
  complexidade: true,
  risco: true,
  recursos: true,
};

const DEFAULT_WEIGHTS = {
  pontos_potenciais: 1.0,
  complexidade: 1.0,
  risco: 1.0,
  recursos: 1.0,
};

function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch (_) {}
  return { concepts: [], weights: { ...DEFAULT_WEIGHTS } };
}

function save(state) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function scoreConcept(concept, weights) {
  let total = 0, wsum = 0;
  for (const [key, raw] of Object.entries(concept.scores)) {
    let v = parseFloat(raw);
    if (INVERTED[key]) v = 10 - v;
    const w = parseFloat(weights[key] ?? 1.0);
    total += v * w;
    wsum += w;
  }
  return wsum ? Math.round((total / wsum) * 100) / 100 : 0;
}

function ranked(state) {
  return state.concepts
    .map(c => ({ ...c, score: scoreConcept(c, state.weights) }))
    .sort((a, b) => b.score - a.score);
}

function esc(s) {
  return String(s ?? "").replace(/[&<>"]/g, c =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])
  );
}

function render() {
  const state = load();

  // weights form
  const wf = document.getElementById("weights-form");
  for (const k of Object.keys(DEFAULT_WEIGHTS)) {
    if (state.weights[k] !== undefined) wf.elements[k].value = state.weights[k];
  }

  // ranking table
  const tbody = document.getElementById("rank-body");
  const empty = document.getElementById("empty-msg");
  tbody.innerHTML = "";
  const rows = ranked(state);
  empty.hidden = rows.length > 0;
  rows.forEach((c, i) => {
    const medal = i === 0 ? "🥇 " : i === 1 ? "🥈 " : i === 2 ? "🥉 " : "";
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${i + 1}</td>
      <td><b>${medal}${esc(c.name)}</b><br><small>${esc(c.description || "")}</small></td>
      <td>${c.scores.pontos_potenciais}</td>
      <td>${c.scores.complexidade}</td>
      <td>${c.scores.risco}</td>
      <td>${c.scores.recursos}</td>
      <td><b>${c.score}</b></td>
      <td><button class="del" data-idx="${state.concepts.indexOf(c)}">✕</button></td>
    `;
    tbody.appendChild(tr);
  });
  // Safe: esc() escapes & < > " before innerHTML; no other user data goes into HTML.
  tbody.querySelectorAll(".del").forEach(b =>
    b.onclick = () => {
      const idx = parseInt(b.dataset.idx, 10);
      const s = load();
      if (idx >= 0 && idx < s.concepts.length) {
        s.concepts.splice(idx, 1);
        save(s);
        render();
      }
    }
  );
}

document.getElementById("add-form").addEventListener("submit", e => {
  e.preventDefault();
  const f = e.target;
  const name = f.name.value.trim();
  const description = f.description.value.trim();
  const scores = {};
  for (const k of Object.keys(DEFAULT_WEIGHTS)) {
    const v = parseFloat(f[k].value);
    if (!Number.isFinite(v) || v < 0 || v > 10) {
      alert(`Nota "${k}" deve estar entre 0 e 10.`);
      return;
    }
    scores[k] = v;
  }
  if (!name) {
    alert("Nome do conceito é obrigatório.");
    return;
  }
  const s = load();
  s.concepts.push({ name, description, scores });
  save(s);
  f.reset();
  render();
});

document.getElementById("weights-form").addEventListener("submit", e => {
  e.preventDefault();
  const s = load();
  for (const inp of e.target.querySelectorAll("input")) {
    const v = parseFloat(inp.value);
    s.weights[inp.name] = Number.isFinite(v) ? v : 1.0;
  }
  save(s);
  render();
});

render();
