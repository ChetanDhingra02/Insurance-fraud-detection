import streamlit as st


# ─────────────────────────────────────────────────────────────────────────────
# Fixed aurora night-sky theme for Streamlit.
#
# Key fixes vs the previous version:
#  1. Canvas stays position:fixed (correct) but ALL Streamlit wrapper divs now
#     get an explicit z-index > 0 so they stack above the canvas layer (z:-1).
#  2. ctx.roundRect polyfill added — older Chrome / Edge builds don't support
#     the native API and throw "ctx.roundRect is not a function".
#  3. The canvas is appended to document.body (not insertBefore firstChild)
#     so Streamlit's own DOM mutations don't accidentally remove it.
#  4. A MutationObserver re-checks the canvas is still in the DOM every time
#     Streamlit re-renders and re-injects it if it gets wiped.
# ─────────────────────────────────────────────────────────────────────────────

THEME = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;500;600;700;800&display=swap');
:root {
  --bg:         #04080f;
  --ink:        #dff2ec;
  --ink-70:     rgba(223,242,236,0.72);
  --ink-40:     rgba(223,242,236,0.42);
  --ink-15:     rgba(223,242,236,0.15);
  --ink-08:     rgba(223,242,236,0.08);
  --aurora-g:   #3adb8a;
  --aurora-g-l: rgba(58,219,138,0.18);
  --aurora-t:   #2be8c8;
  --aurora-b:   #5ab4ff;
  --aurora-v:   #a078ff;
  --aurora-r:   #ff7eb3;
  --gold:       #ffc060;
  --gold-l:     rgba(255,192,96,0.18);
  --border:     rgba(58,219,138,0.16);
  --radius:     18px;
}

/* ── Global font / colour resets ── */
html, body, [class*="css"] { font-family:'Nunito',sans-serif !important; color:var(--ink) !important; }
html { background:#04080f !important; }
body { background:transparent !important; }

/* ── Make every Streamlit layer transparent so the canvas shows through ── */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stMain"],
.main,
[data-testid="block-container"],
.block-container,
section[data-testid="stSidebar"],
[data-testid="stVerticalBlock"] {
  background: transparent !important;
}

/* ── Ensure Streamlit content stacks ABOVE the canvas (z-index:-1) ── */
/* The canvas sits at z-index:-1; everything that should appear on top needs
   an explicit stacking context with z >= 0.                              */
.stApp                              { position: relative; z-index: 0; }
[data-testid="stAppViewContainer"]  { position: relative; z-index: 0; }
[data-testid="stMain"]              { position: relative; z-index: 0; }
.main                               { position: relative; z-index: 0; }
[data-testid="block-container"],
.block-container                    { position: relative; z-index: 0; }

/* ── Hide Streamlit chrome ── */
[data-testid="stHeader"],
[data-testid="stDecoration"],
[data-testid="stToolbar"],
[data-testid="stStatusWidget"],
footer { display:none !important; }

.main .block-container { max-width:1160px; padding:0 2rem 6rem; }

/* ══════════════════════════════════════════════════════════════════════════
   UI COMPONENT STYLES  (unchanged from original)
   ══════════════════════════════════════════════════════════════════════════ */

.hdr { display:flex; align-items:center; justify-content:space-between; padding:1.1rem 0 1.0rem; border-bottom:1.5px solid var(--border); animation:slideDown 0.5s cubic-bezier(0.22,1,0.36,1) both; }
@keyframes slideDown { from{opacity:0;transform:translateY(-8px)} to{opacity:1;transform:translateY(0)} }
.hdr-l { display:flex; align-items:center; gap:0.6rem; }
.hdr-icon { width:32px; height:32px; border-radius:10px; background:linear-gradient(135deg,#3adb8a,#2be8c8); display:flex; align-items:center; justify-content:center; box-shadow:0 2px 18px rgba(58,219,138,0.65),0 4px 36px rgba(43,232,200,0.30); flex-shrink:0; animation:iconPulse 4s ease-in-out infinite; }
@keyframes iconPulse { 0%,100%{box-shadow:0 2px 18px rgba(58,219,138,0.65),0 4px 36px rgba(43,232,200,0.30)} 50%{box-shadow:0 2px 32px rgba(58,219,138,1.0),0 4px 60px rgba(90,180,255,0.50)} }
.hdr-icon svg { width:15px; height:15px; }
.hdr-name { font-size:1.0rem; font-weight:800; letter-spacing:-0.02em; background:linear-gradient(135deg,#3adb8a,#2be8c8); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.hdr-divider { width:1px; height:14px; background:var(--border); margin:0 0.3rem; }
.hdr-sub { font-size:0.78rem; font-weight:500; color:var(--ink-40); }
.hdr-r { display:flex; align-items:center; gap:0.4rem; }
.chip { font-size:0.70rem; font-weight:600; padding:0.22rem 0.65rem; border-radius:99px; background:rgba(255,255,255,0.07); color:var(--ink-70); border:1px solid var(--border); }
.chip-live { background:rgba(58,219,138,0.14); color:#3adb8a; border-color:rgba(58,219,138,0.40); display:flex; align-items:center; gap:5px; }
.live-dot { width:5px; height:5px; border-radius:50%; background:#3adb8a; animation:livePulse 2.4s ease-in-out infinite; }
@keyframes livePulse { 0%,100%{box-shadow:0 0 0 0 rgba(58,219,138,0.8)} 50%{box-shadow:0 0 0 6px rgba(58,219,138,0)} }
.hero { display:flex; align-items:center; justify-content:space-between; gap:2rem; padding:1.6rem 0 1.5rem; border-bottom:1.5px solid var(--border); margin-bottom:2rem; animation:fadeUp 0.55s cubic-bezier(0.22,1,0.36,1) 0.08s both; }
@keyframes fadeUp { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }
.hero-title { font-size:1.45rem; font-weight:800; letter-spacing:-0.03em; line-height:1; color:var(--ink); }
.hero-title span { background:linear-gradient(135deg,#3adb8a,#5ab4ff); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.hero-desc { font-size:0.82rem; color:var(--ink-40); line-height:1.55; max-width:340px; border-left:2.5px solid var(--border); padding-left:0.85rem; margin-top:0.5rem; }
.hero-pills { display:flex; gap:0.4rem; flex-shrink:0; }
.hpill { font-size:0.72rem; font-weight:700; padding:0.35rem 0.8rem; border-radius:12px; color:var(--ink); background:rgba(255,255,255,0.06); border:1.5px solid var(--border); display:flex; flex-direction:column; align-items:center; gap:1px; box-shadow:0 2px 14px rgba(58,219,138,0.18); transition:box-shadow 0.2s,border-color 0.2s; }
.hpill:hover { box-shadow:0 4px 30px rgba(58,219,138,0.45); border-color:#3adb8a; }
.hpill-v { font-size:1.1rem; font-weight:800; letter-spacing:-0.02em; color:#3adb8a; }
.hpill-l { font-size:0.60rem; font-weight:600; color:var(--ink-40); text-transform:uppercase; letter-spacing:0.07em; }
.card { background:rgba(4,8,15,0.72); border:1.5px solid var(--border); border-radius:var(--radius); padding:1.4rem 1.5rem; margin-bottom:0.9rem; box-shadow:0 4px 28px rgba(0,0,0,0.55),inset 0 1px 0 rgba(255,255,255,0.06); transition:box-shadow 0.3s,border-color 0.25s,transform 0.25s cubic-bezier(0.22,1,0.36,1); animation:cardUp 0.48s cubic-bezier(0.22,1,0.36,1) both; position:relative; overflow:hidden; backdrop-filter:blur(18px); -webkit-backdrop-filter:blur(18px); }
.card::before { content:""; position:absolute; top:0; left:0; right:0; height:2px; background:linear-gradient(90deg,transparent,#3adb8a,#2be8c8,#5ab4ff,#a078ff,transparent); opacity:0; transition:opacity 0.3s; }
.card:hover { box-shadow:0 10px 48px rgba(58,219,138,0.22),0 2px 12px rgba(90,180,255,0.18); border-color:rgba(58,219,138,0.40); transform:translateY(-2px); }
.card:hover::before { opacity:1; }
@keyframes cardUp { from{opacity:0;transform:translateY(14px)} to{opacity:1;transform:translateY(0)} }
.card::after { content:""; position:absolute; width:260px; height:260px; border-radius:50%; background:radial-gradient(circle,rgba(58,219,138,0.07) 0%,transparent 70%); top:-80px; right:-80px; pointer-events:none; }
.ctag { font-size:0.65rem; font-weight:700; letter-spacing:0.10em; text-transform:uppercase; color:#2be8c8; margin-bottom:0.22rem; }
.ctitle { font-size:1.0rem; font-weight:800; letter-spacing:-0.02em; color:var(--ink); margin-bottom:0.16rem; }
.cnote { font-size:0.79rem; color:var(--ink-40); line-height:1.55; margin-bottom:0.95rem; padding-bottom:0.85rem; border-bottom:1px solid var(--border); }
label,div[data-testid="stWidgetLabel"] p { font-family:'Nunito',sans-serif !important; font-size:0.80rem !important; font-weight:700 !important; color:var(--ink-70) !important; letter-spacing:-0.01em !important; }
div[data-baseweb="select"]>div { background:rgba(4,8,15,0.80) !important; border:1.5px solid var(--border) !important; border-radius:10px !important; min-height:40px !important; color:var(--ink) !important; -webkit-text-fill-color:var(--ink) !important; font-family:'Nunito',sans-serif !important; font-size:0.83rem !important; font-weight:600 !important; }
div[data-baseweb="select"] span,div[data-baseweb="select"] input { color:var(--ink) !important; -webkit-text-fill-color:var(--ink) !important; font-family:'Nunito',sans-serif !important; }
div[data-baseweb="select"] svg { color:#3adb8a !important; }
div[data-baseweb="select"]>div:focus-within { border-color:#3adb8a !important; box-shadow:0 0 0 3px rgba(58,219,138,0.22) !important; }
[data-baseweb="menu"],[data-baseweb="popover"]>div { background:rgba(4,8,15,0.97) !important; border:1.5px solid var(--border) !important; border-radius:14px !important; box-shadow:0 20px 60px rgba(0,0,0,0.70) !important; }
[data-baseweb="option"] { color:var(--ink) !important; font-family:'Nunito',sans-serif !important; font-weight:600 !important; font-size:0.83rem !important; border-radius:7px !important; margin:2px 6px !important; background:transparent !important; }
[data-baseweb="option"]:hover,[data-baseweb="option"][aria-selected="true"] { background:rgba(58,219,138,0.15) !important; color:#3adb8a !important; }
[data-testid="stNumberInput"] input { background:rgba(4,8,15,0.80) !important; border:1.5px solid var(--border) !important; border-radius:10px !important; color:var(--ink) !important; -webkit-text-fill-color:var(--ink) !important; font-family:'Nunito',sans-serif !important; font-weight:600 !important; font-size:0.83rem !important; }
[data-testid="stNumberInput"] input:focus { border-color:#3adb8a !important; box-shadow:0 0 0 3px rgba(58,219,138,0.22) !important; outline:none !important; }
[data-testid="stNumberInput"] button { background:rgba(4,8,15,0.80) !important; color:var(--ink-40) !important; border:1.5px solid var(--border) !important; border-radius:8px !important; font-weight:700 !important; }
[data-testid="stNumberInput"] button:hover { background:rgba(58,219,138,0.15) !important; border-color:rgba(58,219,138,0.5) !important; color:#3adb8a !important; }
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] { width:22px !important; height:22px !important; background:#04080f !important; border:2.5px solid #3adb8a !important; border-radius:50% !important; box-shadow:0 0 0 4px rgba(58,219,138,0.22),0 2px 16px rgba(58,219,138,0.55) !important; }
[data-testid="stSlider"] p { color:#3adb8a !important; font-weight:700 !important; font-size:0.78rem !important; }
div.stButton>button { width:100% !important; background:linear-gradient(135deg,#3adb8a,#2be8c8) !important; color:#04080f !important; border:none !important; border-radius:14px !important; padding:0.88rem 2rem !important; font-family:'Nunito',sans-serif !important; font-weight:800 !important; font-size:0.90rem !important; box-shadow:0 4px 0 rgba(10,60,40,0.55),0 8px 36px rgba(58,219,138,0.50) !important; transform:translateY(0) !important; transition:transform 0.13s,box-shadow 0.13s !important; margin-top:1.1rem !important; }
div.stButton>button:hover { box-shadow:0 6px 0 rgba(10,60,40,0.55),0 14px 48px rgba(58,219,138,0.70) !important; transform:translateY(-2px) !important; }
div.stButton>button:active { box-shadow:0 1px 0 rgba(10,60,40,0.55),0 3px 12px rgba(58,219,138,0.28) !important; transform:translateY(3px) !important; }
.results-bar { display:flex; align-items:center; gap:0.8rem; margin:2rem 0 1.6rem; }
.results-line { flex:1; height:1.5px; background:var(--border); }
.results-tag { font-size:0.68rem; font-weight:700; letter-spacing:0.10em; text-transform:uppercase; color:var(--ink-40); white-space:nowrap; }
.score-block { padding:1.4rem 0 0.6rem; animation:popIn 0.6s cubic-bezier(0.22,1,0.36,1) 0.06s both; }
@keyframes popIn { from{opacity:0;transform:scale(0.80)} to{opacity:1;transform:scale(1)} }
.score-val { font-size:5.5rem; font-weight:800; letter-spacing:-0.06em; line-height:1; display:inline-flex; align-items:flex-start; gap:4px; }
.score-pct { font-size:2rem; font-weight:400; opacity:0.30; margin-top:0.7rem; }
.score-label { font-size:0.72rem; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; margin-top:0.25rem; opacity:0.55; }
.ptrack { height:5px; border-radius:999px; background:var(--ink-08); overflow:hidden; margin:0.8rem 0 0.3rem; }
.ptrack-fill { height:100%; border-radius:999px; animation:grow 1.0s cubic-bezier(0.22,1,0.36,1) both; }
@keyframes grow { from{width:0%} }
.gauge { background:rgba(4,8,15,0.60); border:1.5px solid var(--border); border-radius:12px; padding:0.78rem 0.9rem 0.65rem; margin-top:0.8rem; }
.gauge-bar { height:7px; border-radius:999px; position:relative; background:linear-gradient(90deg,#3adb8a 0%,#2be8c8 30%,#5ab4ff 60%,#a078ff 80%,#ff7eb3 100%); box-shadow:0 2px 18px rgba(58,219,138,0.45); }
.gauge-pin { position:absolute; top:50%; width:15px; height:15px; background:#04080f; border:2.5px solid #3adb8a; border-radius:50%; box-shadow:0 0 16px rgba(58,219,138,0.80); transform:translateX(-50%) translateY(-50%); animation:pinPop 0.65s cubic-bezier(0.34,1.56,0.64,1) 0.2s both; }
@keyframes pinPop { from{opacity:0;transform:translateX(-50%) translateY(-50%) scale(0)} to{opacity:1;transform:translateX(-50%) translateY(-50%) scale(1)} }
.gauge-ticks { display:flex; justify-content:space-between; margin-top:0.45rem; }
.gauge-tick { font-size:0.62rem; font-weight:600; color:var(--ink-40); }
.badge { display:inline-flex; align-items:center; gap:6px; border-radius:8px; padding:0.32rem 0.75rem; font-size:0.70rem; font-weight:800; letter-spacing:0.04em; text-transform:uppercase; border:1.5px solid; margin-top:0.9rem; }
.bdot { width:5px; height:5px; border-radius:50%; background:currentColor; }
.b-low  { color:#3adb8a; border-color:rgba(58,219,138,0.40); background:rgba(58,219,138,0.12); }
.b-med  { color:#ffc060; border-color:rgba(255,192,96,0.40); background:rgba(255,192,96,0.12); }
.b-high { color:#ff7eb3; border-color:rgba(255,126,179,0.40); background:rgba(255,126,179,0.12); }
.mrow { display:flex; justify-content:space-between; align-items:center; padding:0.52rem 0; border-bottom:1px solid var(--border); gap:1rem; }
.mrow:last-child { border-bottom:none; }
.mk { font-size:0.72rem; font-weight:600; color:var(--ink-40); }
.mv { font-size:0.83rem; font-weight:800; color:var(--ink); text-align:right; }
.action { border-radius:12px; padding:0.95rem 1.1rem; margin:0.9rem 0; background:rgba(58,219,138,0.08); border:1.5px solid rgba(58,219,138,0.22); }
.action-t { font-size:0.90rem; font-weight:800; color:#3adb8a; margin-bottom:0.25rem; }
.action-d { font-size:0.79rem; color:var(--ink-40); line-height:1.6; }
.driver { display:flex; gap:0.8rem; align-items:flex-start; padding:0.75rem 0; border-bottom:1px solid var(--border); }
.driver:last-child { border-bottom:none; }
.driver-n { font-size:0.62rem; font-weight:800; width:22px; height:22px; border-radius:6px; background:rgba(58,219,138,0.08); border:1.5px solid rgba(58,219,138,0.22); color:#3adb8a; display:flex; align-items:center; justify-content:center; flex-shrink:0; margin-top:1px; }
.driver-t { font-size:0.83rem; font-weight:800; color:var(--ink); margin-bottom:0.1rem; }
.driver-d { font-size:0.77rem; color:var(--ink-40); line-height:1.55; }
.footer { text-align:center; margin-top:3rem; padding-top:1.2rem; border-top:1.5px solid var(--border); font-size:0.68rem; color:var(--ink); }
</style>

<!-- Canvas animation lives in a <template> so Streamlit's HTML sanitiser
     leaves the raw JS completely untouched.                               -->
<template id="__aurora_tpl__">
(function () {
  if (window.__aurora_running__) return;
  window.__aurora_running__ = true;

  /* ─── ctx.roundRect polyfill (not available in all Chromium builds) ─── */
  if (!CanvasRenderingContext2D.prototype.roundRect) {
    CanvasRenderingContext2D.prototype.roundRect = function(x, y, w, h, r) {
      var rad = Array.isArray(r) ? r[0] : (r || 0);
      this.beginPath();
      this.moveTo(x + rad, y);
      this.lineTo(x + w - rad, y);
      this.quadraticCurveTo(x + w, y, x + w, y + rad);
      this.lineTo(x + w, y + h - rad);
      this.quadraticCurveTo(x + w, y + h, x + w - rad, y + h);
      this.lineTo(x + rad, y + h);
      this.quadraticCurveTo(x, y + h, x, y + h - rad);
      this.lineTo(x, y + rad);
      this.quadraticCurveTo(x, y, x + rad, y);
      this.closePath();
      return this;
    };
  }

  /* ─── Inject transparency styles so canvas shows through ─── */
  var s = document.createElement('style');
  s.id = '__aurora_styles__';
  s.textContent = [
    'html{background:#04080f!important}',
    'body{background:transparent!important}',
    /* Make every Streamlit wrapper transparent but keep it above the canvas */
    '.stApp,[data-testid="stAppViewContainer"],[data-testid="stAppViewBlockContainer"],[data-testid="stMain"],.main,[data-testid="block-container"],.block-container{background:transparent!important;position:relative;z-index:0;}',
    /* The canvas sits at z-index:0 on body — body itself has no stacking context,
       so fixed children at z:-1 go behind everything. We use z:0 on canvas and
       rely on pointer-events:none so it never blocks clicks.              */
  ].join('');
  document.head.appendChild(s);

  /* ─── Create the canvas ─── */
  function mountCanvas() {
    var existing = document.getElementById('__night_sky__');
    if (existing) return existing;
    var cv = document.createElement('canvas');
    cv.id = '__night_sky__';
    /* position:fixed keeps it covering the full viewport as you scroll.
       z-index:-1 pushes it behind Streamlit's z-index:0 content layers. */
    cv.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:-1;display:block;';
    document.body.appendChild(cv);
    return cv;
  }

  var cv = mountCanvas();
  var ctx = cv.getContext('2d');
  var W, H;

  function resize() { W = cv.width = window.innerWidth; H = cv.height = window.innerHeight; }
  resize();
  window.addEventListener('resize', resize);

  /* ─── Re-mount canvas if Streamlit's React re-render removes it ─── */
  var obs = new MutationObserver(function() {
    if (!document.getElementById('__night_sky__')) {
      cv = mountCanvas();
      ctx = cv.getContext('2d');
      resize();
    }
  });
  obs.observe(document.body, { childList: true });

  /* ─── Stars ─── */
  var stars = [];
  for (var i = 0; i < 260; i++) {
    stars.push({
      x: Math.random(), y: Math.random() * 0.75,
      r: Math.random() * 1.4 + 0.3,
      base: Math.random() * 0.5 + 0.25,
      spd: Math.random() * 0.8 + 0.3,
      ph: Math.random() * Math.PI * 2
    });
  }

  /* ─── Aurora bands ─── */
  var bands = [
    {cx:0.12,w:0.55,y:0.18,h:0.22,c1:'#00ff88',c2:'#00ccaa',dur:22,ph:0.0},
    {cx:0.40,w:0.48,y:0.12,h:0.20,c1:'#5599ff',c2:'#8833ff',dur:28,ph:1.8},
    {cx:0.68,w:0.42,y:0.15,h:0.18,c1:'#00ddff',c2:'#3366ff',dur:24,ph:3.5},
    {cx:0.82,w:0.32,y:0.10,h:0.16,c1:'#ff55bb',c2:'#8833ff',dur:19,ph:5.2},
    {cx:0.25,w:0.60,y:0.28,h:0.14,c1:'#00ffbb',c2:'#00aa55',dur:32,ph:2.6},
  ];

  /* ─── Snow ─── */
  var snowCols = ['#b8eedd','#8ecfff','#c8b8ff','#ffc8e8','#ffffff'];
  var flakes = [];
  for (var j = 0; j < 90; j++) flakes.push(mkFlake(false));
  function mkFlake(top) {
    return {
      x: Math.random(), y: top ? -0.02 : Math.random(),
      r: Math.random() * 2.2 + 0.8,
      vx: (Math.random() - 0.5) * 0.00015,
      vy: Math.random() * 0.00025 + 0.00008,
      op: Math.random() * 0.55 + 0.20,
      col: snowCols[Math.floor(Math.random() * snowCols.length)]
    };
  }

  /* ─── Car ─── */
  var carX = -0.18, CAR_SPEED = 0.00018, lastT = 0;

  /* Helper: hex colour → rgba string */
  function ha(hex, a) {
    var r = parseInt(hex.slice(1,3),16),
        g = parseInt(hex.slice(3,5),16),
        b = parseInt(hex.slice(5,7),16);
    return 'rgba('+r+','+g+','+b+','+a.toFixed(3)+')';
  }

  /* ─── Draw functions ─── */
  function drawSky() {
    var bg = ctx.createLinearGradient(0,0,0,H);
    bg.addColorStop(0,'#02040c');
    bg.addColorStop(0.6,'#04080f');
    bg.addColorStop(1,'#060c18');
    ctx.fillStyle = bg; ctx.fillRect(0,0,W,H);
  }

  function drawAurora(t) {
    ctx.save(); ctx.globalCompositeOperation = 'screen';
    bands.forEach(function(b) {
      var sway = Math.sin(t / (b.dur * 1000) * Math.PI * 2 + b.ph);
      var cy = (b.y + sway * 0.04) * H, cx = b.cx * W, rw = b.w * W, rh = b.h * H;
      var peak = 0.38 + Math.sin(t / (b.dur * 800) + b.ph + 1) * 0.14;
      var g = ctx.createRadialGradient(cx,cy,0,cx,cy,rw*0.7);
      g.addColorStop(0, ha(b.c1, peak));
      g.addColorStop(0.4, ha(b.c2, peak * 0.65));
      g.addColorStop(1, ha(b.c2, 0));
      ctx.filter = 'blur(28px)';
      ctx.beginPath(); ctx.ellipse(cx,cy,rw*0.7,rh*0.9,0,0,Math.PI*2);
      ctx.fillStyle = g; ctx.fill();
    });
    ctx.filter = 'none'; ctx.globalCompositeOperation = 'source-over'; ctx.restore();
  }

  function drawStars(t) {
    stars.forEach(function(s) {
      var op = Math.max(0, Math.min(1, s.base + Math.sin(t/1000*s.spd*Math.PI*2+s.ph)*0.28));
      ctx.beginPath(); ctx.arc(s.x*W, s.y*H, s.r, 0, Math.PI*2);
      ctx.fillStyle = 'rgba(255,255,255,'+op+')'; ctx.fill();
      if (s.r > 1.1 && op > 0.55) {
        ctx.strokeStyle = 'rgba(255,255,255,'+(op*0.35)+')'; ctx.lineWidth = 0.5;
        ctx.beginPath();
        ctx.moveTo(s.x*W - s.r*2.5, s.y*H); ctx.lineTo(s.x*W + s.r*2.5, s.y*H);
        ctx.moveTo(s.x*W, s.y*H - s.r*2.5); ctx.lineTo(s.x*W, s.y*H + s.r*2.5);
        ctx.stroke();
      }
    });
  }

  function drawSnow(dt) {
    flakes.forEach(function(f,i) {
      f.x += f.vx * dt; f.y += f.vy * dt;
      if (f.y > 1.02) flakes[i] = mkFlake(true);
      ctx.beginPath(); ctx.arc(f.x*W, f.y*H, f.r, 0, Math.PI*2);
      ctx.fillStyle = f.col; ctx.globalAlpha = f.op; ctx.fill(); ctx.globalAlpha = 1;
    });
  }

  function drawRoad() {
    var ry = H * 0.90, rh = H * 0.10;
    var rg = ctx.createLinearGradient(0,ry,0,ry+rh);
    rg.addColorStop(0,'#0a1020'); rg.addColorStop(1,'#060c18');
    ctx.fillStyle = rg; ctx.fillRect(0,ry,W,rh);
    /* Horizon edge */
    ctx.strokeStyle = 'rgba(58,219,138,0.18)'; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(0,ry); ctx.lineTo(W,ry); ctx.stroke();
    /* Centre dashes */
    ctx.setLineDash([W*0.04, W*0.03]);
    ctx.strokeStyle = 'rgba(255,255,255,0.08)'; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(0,ry+rh*0.5); ctx.lineTo(W,ry+rh*0.5); ctx.stroke();
    ctx.setLineDash([]);
  }

  function drawCar(dt) {
    carX += CAR_SPEED * dt;
    if (carX > 1.18) carX = -0.18;

    var cx = carX * W, ry = H * 0.90, cw = W * 0.10, ch = cw * 0.38, cy = ry - ch * 0.5;

    /* Headlight cone (in front of car — right side) */
    var hl = ctx.createRadialGradient(cx+cw*0.52,cy+ch*0.5,0, cx+cw*0.52,cy+ch*0.5,cw*1.6);
    hl.addColorStop(0,'rgba(220,240,255,0.22)');
    hl.addColorStop(0.3,'rgba(180,220,255,0.10)');
    hl.addColorStop(1,'rgba(100,180,255,0)');
    ctx.fillStyle = hl;
    ctx.beginPath();
    ctx.moveTo(cx+cw*0.52, cy+ch*0.25);
    ctx.lineTo(cx+cw*0.52, cy+ch*0.75);
    ctx.lineTo(cx+cw*2.1,  cy+ch*1.1);
    ctx.lineTo(cx+cw*2.1,  cy-ch*0.1);
    ctx.closePath(); ctx.fill();

    /* Ground shadow */
    ctx.fillStyle = 'rgba(0,0,0,0.22)';
    ctx.beginPath(); ctx.ellipse(cx+cw*0.5, ry+2, cw*0.45, 4, 0, 0, Math.PI*2); ctx.fill();

    /* Car body — use polyfilled roundRect */
    var bg = ctx.createLinearGradient(cx, cy, cx, cy+ch);
    bg.addColorStop(0,'#1a2a3a'); bg.addColorStop(1,'#0a1520');
    ctx.fillStyle = bg;
    ctx.beginPath(); ctx.roundRect(cx, cy+ch*0.3, cw, ch*0.7, [3,3,5,5]); ctx.fill();

    /* Cabin */
    ctx.fillStyle = '#0d1e2e';
    ctx.beginPath(); ctx.roundRect(cx+cw*0.18, cy, cw*0.62, ch*0.42, [4,4,2,2]); ctx.fill();

    /* Windows */
    ctx.fillStyle = 'rgba(58,219,138,0.12)';
    ctx.beginPath(); ctx.roundRect(cx+cw*0.22, cy+ch*0.04, cw*0.25, ch*0.30, 2); ctx.fill();
    ctx.fillStyle = 'rgba(90,180,255,0.12)';
    ctx.beginPath(); ctx.roundRect(cx+cw*0.52, cy+ch*0.04, cw*0.22, ch*0.30, 2); ctx.fill();

    /* Wheels */
    [0.16, 0.76].forEach(function(wf) {
      var wx = cx + cw*wf, wy = cy + ch;
      ctx.beginPath(); ctx.arc(wx,wy,ch*0.28,0,Math.PI*2); ctx.fillStyle='#0a0f18'; ctx.fill();
      ctx.beginPath(); ctx.arc(wx,wy,ch*0.14,0,Math.PI*2); ctx.fillStyle='#1e3040'; ctx.fill();
      ctx.beginPath(); ctx.arc(wx,wy,ch*0.10,0,Math.PI*2);
      ctx.strokeStyle='rgba(58,219,138,0.35)'; ctx.lineWidth=1; ctx.stroke();
    });

    /* Headlights */
    ctx.beginPath(); ctx.ellipse(cx+cw*0.96, cy+ch*0.50, 4, 3, 0, 0, Math.PI*2);
    ctx.fillStyle='#ddeeff'; ctx.fill();
    ctx.beginPath(); ctx.ellipse(cx+cw*0.96, cy+ch*0.50, 7, 5, 0, 0, Math.PI*2);
    ctx.fillStyle='rgba(200,230,255,0.25)'; ctx.fill();

    /* Tail lights */
    ctx.beginPath(); ctx.ellipse(cx+cw*0.04, cy+ch*0.50, 4, 3, 0, 0, Math.PI*2);
    ctx.fillStyle='#ff2244'; ctx.fill();
    ctx.beginPath(); ctx.ellipse(cx+cw*0.04, cy+ch*0.50, 7, 5, 0, 0, Math.PI*2);
    ctx.fillStyle='rgba(255,30,60,0.20)'; ctx.fill();
  }

  /* ─── Main render loop ─── */
  function loop(t) {
    var dt = Math.min(t - lastT, 100); lastT = t;
    drawSky(); drawAurora(t); drawStars(t); drawSnow(dt); drawRoad(); drawCar(dt);
    requestAnimationFrame(loop);
  }
  requestAnimationFrame(function(t) { lastT = t; requestAnimationFrame(loop); });
})();
</template>

<!-- Tiny SVG bootstrapper: fires in the real page context, grabs the
     template JS and appends it as a real <script> to <head>.
     The __aurora_boot__ guard prevents double-injection on Streamlit reruns. -->
<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0"
     onload="(function(){
       if(window.__aurora_boot__) return;
       window.__aurora_boot__=true;
       var tpl=document.getElementById('__aurora_tpl__');
       if(!tpl) return;
       var sc=document.createElement('script');
       sc.textContent=tpl.innerHTML;
       document.head.appendChild(sc);
     })()">
</svg>
"""


def render_theme() -> None:
    st.markdown(THEME, unsafe_allow_html=True)