/* ══════════════════════════════════════════════
   NAVIGATION
══════════════════════════════════════════════ */
const TOTAL = 10;
let current = 1;

const dotsEl = document.getElementById('dots');
for (let i = 1; i <= TOTAL; i++) {
  const d = document.createElement('button');
  d.className = 'nav-dot' + (i === 1 ? ' active' : '');
  d.type = 'button';
  d.setAttribute('aria-label', `Go to slide ${i}`);
  d.title = `Go to slide ${i}`;
  d.onclick = () => goTo(i);
  dotsEl.appendChild(d);
}

function goTo(n) {
  document.getElementById('slide-' + current).classList.remove('active');
  current = n;
  document.getElementById('slide-' + current).classList.add('active');
  document.getElementById('counter').textContent = current + ' / ' + TOTAL;
  dotsEl.querySelectorAll('.nav-dot').forEach((d, i) => d.classList.toggle('active', i + 1 === current));
  document.getElementById('prevBtn').disabled = current === 1;
  document.getElementById('nextBtn').disabled = current === TOTAL;
  playClick();
  // Draw canvases when their slides become active
  if (current === 5) { setTimeout(updateTree, 80); }
  if (current === 7) { setTimeout(drawRandomTree, 80); }
  if (current === 8) { setTimeout(drawRealisticTree, 80); }
}

function changeSlide(dir) {
  const n = current + dir;
  if (n >= 1 && n <= TOTAL) goTo(n);
}

document.getElementById('prevBtn').onclick = () => changeSlide(-1);
document.getElementById('nextBtn').onclick = () => changeSlide(1);
document.getElementById('nextBtn').textContent = 'Next →';
document.getElementById('prevBtn').disabled = true;

document.addEventListener('keydown', e => {
  if (document.activeElement.tagName === 'INPUT') return;
  if (e.key === 'ArrowLeft') changeSlide(-1);
  if (e.key === 'ArrowRight') changeSlide(1);
});

/* ══════════════════════════════════════════════
   SOUND DESIGN — Web Audio API
══════════════════════════════════════════════ */
let audioCtx = null;
let soundOn = true;

function getCtx() {
  if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  return audioCtx;
}

// iOS/Safari require a user gesture to start audio.
function unlockAudioOnce() {
  if (!soundOn) return;
  try {
    const ctx = getCtx();
    if (ctx.state === 'suspended') ctx.resume();
  } catch (e) {}
}
window.addEventListener('pointerdown', unlockAudioOnce, { once: true });

function playTone(freq, dur, type = 'sine', vol = 0.07, delay = 0) {
  if (!soundOn) return;
  try {
    const ctx = getCtx();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.type = type;
    osc.frequency.value = freq;
    const t = ctx.currentTime + delay;
    gain.gain.setValueAtTime(0, t);
    gain.gain.linearRampToValueAtTime(vol, t + 0.01);
    gain.gain.exponentialRampToValueAtTime(0.001, t + dur);
    osc.start(t);
    osc.stop(t + dur + 0.01);
  } catch(e) {}
}

function playClick() {
  playTone(420, 0.06, 'sine', 0.05);
}

function playRunStart() {
  [0, 0.07, 0.14].forEach((d, i) => playTone(300 + i * 80, 0.12, 'triangle', 0.04, d));
}

function playLineTick() {
  playTone(660, 0.04, 'triangle', 0.03);
}

function playComplete() {
  [0, 0.1, 0.2].forEach((d, i) => playTone([440, 550, 660][i], 0.18, 'sine', 0.06, d));
}

function playCopy() {
  playTone(880, 0.05, 'triangle', 0.03);
  playTone(1180, 0.06, 'triangle', 0.03, 0.06);
}

document.getElementById('soundBtn').onclick = () => {
  soundOn = !soundOn;
  document.getElementById('soundBtn').textContent = soundOn ? '♪' : '♩';
  if (soundOn) playClick();
};

/* ══════════════════════════════════════════════
   THEME — light/dark toggle with persistence
══════════════════════════════════════════════ */
function getSystemTheme() {
  return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function getSavedTheme() {
  const t = localStorage.getItem('theme');
  return (t === 'light' || t === 'dark') ? t : null;
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  const btn = document.getElementById('themeBtn');
  if (btn) btn.textContent = theme === 'dark' ? '☀︎' : '☾';
}

applyTheme(getSavedTheme() || getSystemTheme());

document.getElementById('themeBtn').onclick = () => {
  const currentTheme = document.documentElement.getAttribute('data-theme') || getSystemTheme();
  const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
  localStorage.setItem('theme', nextTheme);
  applyTheme(nextTheme);
  playClick();
};

if (window.matchMedia) {
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener?.('change', () => {
    if (!getSavedTheme()) applyTheme(getSystemTheme());
  });
}

/* ══════════════════════════════════════════════
   UTILITY
══════════════════════════════════════════════ */
function $(id) { return document.getElementById(id); }

function cssVar(name, fallback) {
  const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return v || fallback;
}

/* ══════════════════════════════════════════════
   WASM (tiny helper module)
══════════════════════════════════════════════ */
let wasmAdd = null;

async function loadWasm() {
  try {
    const url = 'core.wasm';
    let instance;
    if ('instantiateStreaming' in WebAssembly) {
      const res = await fetch(url);
      instance = (await WebAssembly.instantiateStreaming(res, {})).instance;
    } else {
      const buf = await (await fetch(url)).arrayBuffer();
      instance = (await WebAssembly.instantiate(buf, {})).instance;
    }
    if (instance?.exports?.add) wasmAdd = instance.exports.add;
  } catch (e) {
    wasmAdd = null;
  }
}

function clearOutput(outId, statId) {
  $(outId).innerHTML = '<div class="pg-empty">Click Run to execute</div>';
  $(statId).textContent = 'Ready';
}

function copyCode(btn) {
  const block = btn.closest('.code-block');
  const code = block.cloneNode(true);
  code.querySelector('.code-header')?.remove();
  navigator.clipboard.writeText(code.textContent.trim()).then(() => {
    btn.textContent = '✓ Copied';
    playCopy();
    setTimeout(() => btn.textContent = 'Copy', 1200);
  });
}

async function animateLines(lines, outEl, statEl, delay = 120) {
  outEl.innerHTML = '';
  const total = lines.length;
  const chunk = Math.max(1, Math.floor(240 / Math.max(1, delay))); // bigger delay => smaller chunk
  let i = 0;

  // Render in chunks (avoids hundreds of awaited timers).
  while (i < total) {
    await new Promise(r => setTimeout(r, delay));
    const end = Math.min(total, i + chunk);
    const frag = document.createDocumentFragment();
    for (; i < end; i++) {
      const div = document.createElement('div');
      div.innerHTML = lines[i];
      frag.appendChild(div);
      if (i % 3 === 0) playLineTick();
    }
    outEl.appendChild(frag);
    outEl.scrollTop = outEl.scrollHeight;
  }

  playComplete();
  if (statEl) statEl.innerHTML = `<strong>${total}</strong> lines output`;
}

/* ══════════════════════════════════════════════
   HERO BACKGROUND — animated fractal tree
══════════════════════════════════════════════ */
(function() {
  const c = document.getElementById('heroBg');
  if (!c) return;
  const ctx = c.getContext('2d');
  let W, H, rng;
  let frame = 0;

  function resize() {
    W = c.width = c.offsetWidth;
    H = c.height = c.offsetHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  function lcg(seed) {
    let s = seed | 1;
    return () => { s = (1664525 * s + 1013904223) >>> 0; return s / 4294967296; };
  }

  function branch(x, y, len, angle, depth, rng) {
    if (depth <= 0 || len < 3) return;
    const x2 = x + Math.cos(angle) * len;
    const y2 = y + Math.sin(angle) * len;
    ctx.globalAlpha = 0.12 + depth * 0.04;
    ctx.lineWidth = Math.max(0.5, depth * 0.4);
    ctx.strokeStyle = depth <= 2 ? '#78c44a' : '#2d5a1b';
    ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x2, y2); ctx.stroke();
    const a = 0.42 + rng() * 0.08;
    const jit = (rng() - 0.5) * 0.3;
    branch(x2, y2, len * 0.72, angle - a + jit, depth - 1, rng);
    branch(x2, y2, len * 0.72, angle + a + jit, depth - 1, rng);
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    const t = frame * 0.004;
    const numTrees = 4;
    for (let i = 0; i < numTrees; i++) {
      const rx = lcg(i * 997 + 1);
      const x = (0.15 + i * 0.23 + Math.sin(t + i) * 0.04) * W;
      const baseLen = (0.08 + rx() * 0.06) * H;
      rng = lcg(i * 137 + Math.floor(frame / 120));
      branch(x, H, baseLen, -Math.PI / 2 + Math.sin(t * 0.7 + i) * 0.05, 9, rng);
    }
    frame++;
    requestAnimationFrame(draw);
  }
  draw();
})();

/* ══════════════════════════════════════════════
   SLIDE 2 — COUNTDOWN RUNNER
══════════════════════════════════════════════ */
$('cdRun').onclick = async function() {
  const n = Math.min(20, Math.max(1, parseInt($('cdInput').value) || 5));
  $('cdStat').textContent = 'Running…';
  playRunStart();
  const lines = [];
  function cd(k, depth) {
    if (k <= 0) { lines.push(`<div class="pg-output-line"><span class="stars">Blastoff! 🚀</span><span class="call">── base case at depth ${depth}</span></div>`); return; }
    lines.push(`<div class="pg-output-line"><span style="color:var(--g3);font-weight:500;">${k}</span><span class="call pg-stack-indicator">${' ▷'.repeat(Math.min(depth, 10))} countdown(${k})</span></div>`);
    cd(k - 1, depth + 1);
  }
  cd(n, 0);
  await animateLines(lines, $('cdOut'), $('cdStat'), 130);
};

/* ══════════════════════════════════════════════
   SLIDE 3 — STAR TRIANGLE
══════════════════════════════════════════════ */
$('stRun').onclick = async function() {
  const n = Math.min(15, Math.max(1, parseInt($('stInput').value) || 5));
  $('stStat').textContent = 'Running…';
  playRunStart();
  const lines = [];
  function st(k, depth) {
    if (k <= 0) return;
    const indent = '  '.repeat(depth);
    lines.push(`<div class="pg-output-line">
      <span class="stars">${'★'.repeat(k)}</span>
      <span class="call">${indent}startriangle(${k})</span>
    </div>`);
    st(k - 1, depth + 1);
  }
  st(n, 0);
  await animateLines(lines, $('stOut'), $('stStat'), 120);
};

/* ══════════════════════════════════════════════
   SLIDE 3 — TRIANGULAR NUMBER
══════════════════════════════════════════════ */
$('tnRun').onclick = async function() {
  const n = Math.min(20, Math.max(1, parseInt($('tnInput').value) || 6));
  $('tnStat').textContent = 'Running…';
  playRunStart();

  // Build call chain
  const callStack = [];
  function tn(k) { callStack.push(k); return k <= 0 ? 0 : k + tn(k - 1); }
  const result = tn(n);

  const lines = [];
  // Show expansion
  let expansion = callStack.map(k => `T(${k})`).join(' + ');
  lines.push(`<div class="fib-eq-line"><span class="fib-call">T(${n})</span><span>=</span><span>${expansion}</span></div>`);

  // Show numeric values
  let numParts = callStack.map((k, i) => {
    const val = callStack.slice(i).reduce((a, b) => a + b, 0);
    return `<span class="fib-num">${k}</span>`;
  });
  lines.push(`<div class="fib-eq-line">${numParts.join('<span> + </span>')}<span> = </span><span class="fib-result">${result}</span></div>`);

  // Show result
  lines.push(`<div class="fib-eq-line" style="margin-top:6px;"><span style="color:var(--txt3)">Sum 1 to ${n} =</span><span class="fib-result" style="font-size:15px;padding:2px 10px;">${result}</span></div>`);

  await animateLines(lines, $('tnOut'), $('tnStat'), 200);
};

/* ══════════════════════════════════════════════
   SLIDE 4 — FIBONACCI TRACER
══════════════════════════════════════════════ */
$('fibRun').onclick = async function() {
  const n = Math.min(15, Math.max(1, parseInt($('fibInput').value) || 8));
  $('fibStat').textContent = 'Running…';
  playRunStart();

  // Fast + accurate: dynamic programming (no exponential recursion lag).
  const F = Array(Math.max(3, n + 1)).fill(0);
  F[1] = 1; F[2] = 1;
  for (let k = 3; k <= n; k++) F[k] = F[k - 1] + F[k - 2];

  const lines = [];
  lines.push(`<div class="fib-eq-line"><span class="fib-call">Base cases:</span><span>F(1)=1, F(2)=1</span></div>`);
  for (let k = 3; k <= n; k++) {
    lines.push(`<div class="fib-eq-line">
      <span class="fib-call">F(${k})</span><span>=</span>
      <span>F(${k-1}) + F(${k-2})</span><span>=</span>
      <span class="fib-num">${F[k-1]}</span><span>+</span><span class="fib-num">${F[k-2]}</span>
      <span class="fib-result">${F[k]}</span>
    </div>`);
  }

  lines.push(`<div class="fib-eq-line" style="margin-top:8px;border-top:0.5px solid var(--border);padding-top:8px;">
    <span style="color:var(--txt2)">fibonacci(${n}) =</span>
    <span class="fib-result" style="font-size:16px;padding:2px 12px;">${F[n]}</span>
    <span style="color:var(--txt3);font-size:10px;">(computed in ${Math.max(0, n - 2)} steps)</span>
  </div>`);

  await animateLines(lines, $('fibOut'), $('fibStat'), 70);
};

/* ══════════════════════════════════════════════
   FRACTAL TREE ENGINE
══════════════════════════════════════════════ */
let treeMode = 'clean';

function setTreeMode(m) {
  treeMode = m;
  ['clean','random','realistic'].forEach(x => $('mode'+x.charAt(0).toUpperCase()+x.slice(1)).classList.toggle('active', x === m));
  $('noisePanelWrap').style.display = (m === 'clean') ? 'none' : '';
  updateTree();
}

function makeRng(seed) {
  let s = (seed >>> 0) || 1;
  return () => { s = (1664525 * s + 1013904223) >>> 0; return s / 4294967296; };
}

function drawFractalTree(canvas, opts) {
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;
  ctx.clearRect(0, 0, W, H);
  ctx.fillStyle = cssVar('--cream', '#f8f5ed');
  ctx.fillRect(0, 0, W, H);

  const { depth, angle, scale, trunk, mode, noise, seed } = opts;
  const rng = makeRng(seed);
  let calls = 0;

  function branch(x, y, len, dir, n) {
    if (n <= 0 || len < 1.5) return;
    calls++;
    const x2 = x + Math.cos(dir) * len;
    const y2 = y + Math.sin(dir) * len;

    if (mode === 'realistic') {
      ctx.lineWidth = Math.max(0.5, n * 1.1);
      if (n <= 2) ctx.strokeStyle = '#2d5a1b';
      else if (n <= 4) ctx.strokeStyle = '#3d7a24';
      else ctx.strokeStyle = '#7a4a28';
    } else {
      ctx.lineWidth = Math.max(0.5, n * 0.65);
      ctx.strokeStyle = n <= 2 ? '#4a8a2a' : '#5a3418';
    }

    ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x2, y2); ctx.stroke();

    let aJit = 0, sJit = 1;
    if (mode !== 'clean' && noise > 0) {
      const nf = noise / 100;
      aJit = (rng() * 2 - 1) * 22 * nf;
      sJit = (1 - 0.25 * nf) + rng() * 0.5 * nf;
    }
    const a = (angle * Math.PI / 180) + (aJit * Math.PI / 180);
    branch(x2, y2, len * scale * sJit, dir - a, n - 1);
    branch(x2, y2, len * scale * sJit, dir + a, n - 1);
  }

  const t0 = performance.now();
  branch(W / 2, H - 20, trunk, -Math.PI / 2, depth);
  const ms = Math.round(performance.now() - t0);
  return { calls, ms };
}

function updateTree() {
  const canvas = $('treeMain');
  const depth = parseInt($('s_depth').value);
  const angle = parseInt($('s_angle').value);
  const scale = parseFloat($('s_scale').value);
  const trunk = parseInt($('s_trunk').value);
  const noise = parseInt($('s_noise')?.value || '40');
  const seed = parseInt($('s_seed')?.value || '42');

  $('v_depth').textContent = depth;
  $('v_angle').textContent = angle + '°';
  $('v_scale').textContent = scale.toFixed(2);
  $('v_trunk').textContent = trunk + 'px';
  $('v_noise').textContent = noise + '%';
  $('v_seed').textContent = seed;

  const { calls, ms } = drawFractalTree(canvas, { depth, angle, scale, trunk, mode: treeMode, noise, seed });
  const pow2 = depth >= 0 && depth < 31 ? (1 << depth) : Math.pow(2, depth);
  const branches = wasmAdd ? wasmAdd(pow2 | 0, -1) : (pow2 - 1);
  $('treeStats').innerHTML = `Branches: ${branches.toLocaleString()}<br>Calls: ${calls.toLocaleString()}<br>Time: ${ms}ms`;
}

function randomizeTree() {
  $('s_depth').value = 6 + Math.floor(Math.random() * 6);
  $('s_angle').value = 15 + Math.floor(Math.random() * 40);
  $('s_scale').value = (0.58 + Math.random() * 0.28).toFixed(2);
  $('s_trunk').value = 80 + Math.floor(Math.random() * 80);
  $('s_noise').value = Math.floor(Math.random() * 80);
  $('s_seed').value = Math.floor(Math.random() * 9999);
  playClick();
  updateTree();
}

// Hide noise panel initially for clean mode
document.addEventListener('DOMContentLoaded', () => {
  if ($('noisePanelWrap')) $('noisePanelWrap').style.display = 'none';
});

/* ══════════════════════════════════════════════
   SLIDE 7 — RANDOM TREE
══════════════════════════════════════════════ */
function drawRandomTree() {
  const canvas = $('rndTree');
  if (!canvas) return;
  const seed = Math.floor(Math.random() * 9999);
  drawFractalTree(canvas, { depth: 10, angle: 28, scale: 0.74, trunk: 90, mode: 'random', noise: 70, seed });
}

/* ══════════════════════════════════════════════
   SLIDE 8 — REALISTIC TREE
══════════════════════════════════════════════ */
function drawRealisticTree() {
  const canvas = $('realisticTree');
  if (!canvas) return;
  const seed = Math.floor(Math.random() * 9999);
  drawFractalTree(canvas, { depth: 11, angle: 26, scale: 0.76, trunk: 110, mode: 'realistic', noise: 65, seed });
}

/* ══════════════════════════════════════════════
   INIT
══════════════════════════════════════════════ */
window.addEventListener('DOMContentLoaded', () => {
  if ($('noisePanelWrap')) $('noisePanelWrap').style.display = 'none';
  loadWasm();
  updateTree();
});
