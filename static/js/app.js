// ─── Debounced predict ───────────────────────────────────
let _timer = null;
function schedulePredict() {
  clearTimeout(_timer);
  _timer = setTimeout(predictRisk, 350);
}

// ─── Collect form values ──────────────────────────────────
function getFormValues() {
  const cb = id => document.getElementById(id)?.checked || false;
  const sl = id => parseFloat(document.getElementById(id)?.value || 0);
  const se = id => parseInt(document.getElementById(id)?.value || 0);
  return {
    high_bp:      cb('high_bp'),
    high_chol:    cb('high_chol'),
    smoker:       cb('smoker'),
    phys_activity:cb('phys_activity'),
    fruits:       cb('fruits'),
    veggies:      cb('veggies'),
    hvy_alcohol:  cb('hvy_alcohol'),
    diff_walk:    cb('diff_walk'),
    bmi:          sl('bmi'),
    gen_hlth:     se('gen_hlth'),
    age:          se('age'),
    education:    se('education'),
    income:       se('income'),
  };
}

// ─── AJAX predict ─────────────────────────────────────────
async function predictRisk() {
  const data = getFormValues();
  try {
    const res  = await fetch('/api/predict', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(data),
    });
    const json = await res.json();
    updateGauge(json.pct, json.color);
    updateBadge(json.level, json.color);
    updateInterp(json.interp, json.color, json.demo);
  } catch(e) {
    console.error('Predict error:', e);
  }
}

// ─── Update gauge ─────────────────────────────────────────
function updateGauge(pct, color) {
  const el = document.getElementById('gauge');
  if (!el) return;
  const colors = { low:'#86efac', mod:'#fcd34d', high:'#fca5a5' };
  const fill   = colors[color] || '#9CD5FF';
  el.style.background = `conic-gradient(${fill} ${pct}%, #e2e8f0 0%)`;
  const pctEl = document.getElementById('gauge-pct');
  if (pctEl) pctEl.textContent = pct.toFixed(1) + '%';
}

// ─── Update risk badge ────────────────────────────────────
function updateBadge(level, color) {
  const el = document.getElementById('risk-badge');
  if (!el) return;
  el.textContent = level;
  el.className   = 'badge badge-' + color;
}

// ─── Update interpretation box ────────────────────────────
function updateInterp(text, color, demo) {
  const box = document.getElementById('interp-box');
  if (!box) return;
  const bgs = { low:'#dcfce7', mod:'#fef3c7', high:'#fee2e2' };
  box.style.background = bgs[color] || '#fef3c7';
  box.textContent      = text;

  const note = document.getElementById('demo-note');
  if (note) note.className = demo ? 'mt-3 text-xs text-slate-400' : 'hidden';
}

// ─── Side insight cards ───────────────────────────────────
function updateSidecards() {
  const bmi = parseFloat(document.getElementById('bmi')?.value || 25);
  const bp  = document.getElementById('high_bp')?.checked;
  const age = parseInt(document.getElementById('age')?.value || 5);
  const ageLabels = ['','18-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-64','65-69','70-74','75-79','80+'];

  const bmiEl = document.getElementById('bmi-badge');
  if (bmiEl) bmiEl.textContent = bmi < 18.5 ? 'Underweight' : bmi < 25 ? 'Normal' : bmi < 30 ? 'Overweight' : 'Obese';

  const bpEl = document.getElementById('bp-badge');
  if (bpEl) bpEl.textContent = bp ? '⚠ High' : '✓ Normal';

  const ageEl = document.getElementById('age-badge');
  if (ageEl) ageEl.textContent = ageLabels[age] || '—';
}
