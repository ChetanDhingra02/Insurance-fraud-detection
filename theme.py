import streamlit as st


THEME_HTML = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:         #0b0e1a;
  --bg2:        #111528;
  --bg3:        #181d35;
  --white:      #f0eeff;
  --ink:        #f0eeff;
  --ink-70:     rgba(240,238,255,0.70);
  --ink-40:     rgba(240,238,255,0.40);
  --ink-15:     rgba(240,238,255,0.15);
  --ink-08:     rgba(240,238,255,0.08);

  /* Cosmic palette */
  --violet:     #a78bfa;
  --violet-d:   #7c5cfc;
  --violet-l:   rgba(167,139,250,0.18);
  --violet-ll:  rgba(167,139,250,0.08);
  --magenta:    #f472b6;
  --magenta-l:  rgba(244,114,182,0.18);
  --teal:       #2dd4bf;
  --teal-l:     rgba(45,212,191,0.18);
  --gold:       #fbbf24;
  --gold-l:     rgba(251,191,36,0.18);
  --rose:       #fb7185;
  --rose-l:     rgba(251,113,133,0.18);
  --sky:        #60a5fa;
  --sky-l:      rgba(96,165,250,0.18);

  --border:     rgba(167,139,250,0.18);
  --radius:     16px;
}

html, body, [class*="css"] {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  background: var(--bg) !important;
  color: var(--ink) !important;
}

.stApp { background: var(--bg) !important; }
[data-testid="stHeader"]       { display:none !important; }
[data-testid="stDecoration"]   { display:none !important; }
[data-testid="stToolbar"]      { display:none !important; }
[data-testid="stStatusWidget"] { display:none !important; }
footer                          { display:none !important; }

.main .block-container { max-width:1160px; padding:0 2rem 6rem; }

/* ═══════════════════════════
   STAR LAYER — fixed but pointer-events:none
═══════════════════════════ */
#shield-star-layer {
  position:fixed; top:0; left:0; width:100%; height:100%;
  pointer-events:none !important; z-index:0; overflow:hidden;
}
.star {
  position:absolute; border-radius:50%;
  background:white; pointer-events:none !important;
  animation: twinkle var(--d,3s) ease-in-out infinite var(--delay,0s);
}
@keyframes twinkle {
  0%,100%{opacity:var(--lo,0.1);transform:scale(1);}
  50%{opacity:var(--hi,0.7);transform:scale(1.4);}
}

/* ═══════════════════════════
   FLOATING CAR — fixed, fully non-interactive
═══════════════════════════ */
.float-car {
  position:fixed; bottom:60px; right:-300px;
  z-index:0; pointer-events:none !important; opacity:0;
  animation: carDrive 20s linear infinite 2s;
}
.float-car, .float-car * { pointer-events:none !important; }
@keyframes carDrive {
  0%   { right:-300px; opacity:0; }
  5%   { opacity:0.18; }
  90%  { opacity:0.18; }
  100% { right:110vw; opacity:0; }
}

.float-shield {
  position:fixed; top:130px; left:-120px;
  z-index:0; pointer-events:none !important; opacity:0;
  animation: shieldFloat 24s ease-in-out infinite 6s;
}
.float-shield, .float-shield * { pointer-events:none !important; }
@keyframes shieldFloat {
  0%   { left:-120px; opacity:0; }
  8%   { opacity:0.10; }
  50%  { left:46%; opacity:0.10; }
  92%  { opacity:0.10; }
  100% { left:110vw; opacity:0; }
}

/* ═══════════════════════════
   HEADER
═══════════════════════════ */
.hdr {
  display:flex; align-items:center; justify-content:space-between;
  padding:1.1rem 0 1.0rem;
  border-bottom:1px solid var(--border);
  animation:slideDown 0.5s cubic-bezier(0.22,1,0.36,1) both;
}
@keyframes slideDown {
  from{opacity:0;transform:translateY(-8px);}
  to{opacity:1;transform:translateY(0);}
}
.hdr-l { display:flex; align-items:center; gap:0.6rem; }
.hdr-icon {
  width:32px; height:32px; border-radius:10px;
  background:linear-gradient(135deg,var(--violet-d),var(--magenta));
  display:flex; align-items:center; justify-content:center;
  box-shadow:0 0 18px rgba(167,139,250,0.55), 0 0 40px rgba(167,139,250,0.22);
  flex-shrink:0;
  animation:iconPulse 3s ease-in-out infinite;
}
@keyframes iconPulse {
  0%,100%{box-shadow:0 0 18px rgba(167,139,250,0.55),0 0 40px rgba(167,139,250,0.22);}
  50%{box-shadow:0 0 28px rgba(167,139,250,0.85),0 0 60px rgba(244,114,182,0.30);}
}
.hdr-icon svg { width:15px; height:15px; }
.hdr-name {
  font-size:1.0rem; font-weight:700;
  letter-spacing:-0.02em;
  background:linear-gradient(135deg,var(--violet),var(--magenta));
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.hdr-divider { width:1px; height:14px; background:var(--border); margin:0 0.3rem; }
.hdr-sub { font-size:0.78rem; font-weight:400; color:var(--ink-40); }

.hdr-r { display:flex; align-items:center; gap:0.4rem; }
.chip {
  font-size:0.70rem; font-weight:500;
  padding:0.22rem 0.65rem; border-radius:99px;
  background:var(--ink-08); color:var(--ink-70);
  border:1px solid var(--border); letter-spacing:0;
}
.chip-live {
  background:var(--teal-l); color:var(--teal);
  border-color:rgba(45,212,191,0.35);
  display:flex; align-items:center; gap:5px;
}
.live-dot {
  width:5px; height:5px; border-radius:50%;
  background:var(--teal);
  animation:glow 2.2s ease-in-out infinite;
}
@keyframes glow {
  0%,100%{box-shadow:0 0 0 0 rgba(45,212,191,0.6);}
  50%{box-shadow:0 0 0 5px rgba(45,212,191,0);}
}

/* ═══════════════════════════
   HERO
═══════════════════════════ */
.hero {
  display:flex; align-items:center; justify-content:space-between;
  gap:2rem; padding:1.6rem 0 1.5rem;
  border-bottom:1px solid var(--border); margin-bottom:2rem;
  animation:fadeUp 0.55s cubic-bezier(0.22,1,0.36,1) 0.08s both;
}
@keyframes fadeUp {
  from{opacity:0;transform:translateY(12px);}
  to{opacity:1;transform:translateY(0);}
}
.hero-title {
  font-size:1.45rem; font-weight:700;
  letter-spacing:-0.03em; line-height:1;
  color:var(--white);
}
.hero-title span {
  background:linear-gradient(135deg,var(--violet),var(--magenta));
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.hero-desc {
  font-size:0.82rem; color:var(--ink-40);
  line-height:1.55; max-width:340px;
  border-left:2px solid var(--border); padding-left:0.85rem; margin-top:0.5rem;
}
.hero-pills { display:flex; gap:0.4rem; flex-shrink:0; }
.hpill {
  font-size:0.72rem; font-weight:600;
  padding:0.35rem 0.8rem; border-radius:10px;
  color:var(--ink); background:var(--bg3);
  border:1px solid var(--border);
  display:flex; flex-direction:column; align-items:center; gap:1px;
  box-shadow:0 0 16px rgba(167,139,250,0.10);
  transition:box-shadow 0.2s,border-color 0.2s;
}
.hpill:hover { box-shadow:0 0 24px rgba(167,139,250,0.28); border-color:var(--violet); }
.hpill-v { font-size:1.1rem; font-weight:800; letter-spacing:-0.02em; color:var(--violet); }
.hpill-l { font-size:0.60rem; font-weight:500; color:var(--ink-40); text-transform:uppercase; letter-spacing:0.06em; }

/* ═══════════════════════════
   CARDS
═══════════════════════════ */
.card {
  background:var(--bg2);
  border:1px solid var(--border);
  border-radius:var(--radius);
  padding:1.4rem 1.5rem;
  margin-bottom:0.9rem;
  box-shadow:0 0 0 1px rgba(167,139,250,0.05),inset 0 1px 0 rgba(240,238,255,0.03);
  transition:box-shadow 0.3s ease,border-color 0.25s,transform 0.25s cubic-bezier(0.22,1,0.36,1);
  animation:cardUp 0.48s cubic-bezier(0.22,1,0.36,1) both;
  position:relative; overflow:hidden;
}
.card::before {
  content:""; position:absolute; top:0; left:0; right:0;
  height:1px;
  background:linear-gradient(90deg,transparent,var(--violet),var(--magenta),var(--teal),transparent);
  opacity:0; transition:opacity 0.3s;
}
.card:hover {
  box-shadow:0 0 40px rgba(167,139,250,0.14),0 0 80px rgba(167,139,250,0.07);
  border-color:rgba(167,139,250,0.38);
  transform:translateY(-2px);
}
.card:hover::before { opacity:1; }
@keyframes cardUp {
  from{opacity:0;transform:translateY(14px);}
  to{opacity:1;transform:translateY(0);}
}

/* glowing orb inside card */
.card::after {
  content:""; position:absolute;
  width:200px; height:200px; border-radius:50%;
  background:radial-gradient(circle,rgba(167,139,250,0.06) 0%,transparent 70%);
  top:-60px; right:-60px; pointer-events:none;
}

.ctag {
  font-size:0.65rem; font-weight:600; letter-spacing:0.10em;
  text-transform:uppercase; color:var(--magenta);
  margin-bottom:0.22rem;
}
.ctitle {
  font-size:1.0rem; font-weight:700;
  letter-spacing:-0.02em; color:var(--white);
  margin-bottom:0.16rem;
}
.cnote {
  font-size:0.79rem; color:var(--ink-40);
  line-height:1.55; margin-bottom:0.95rem;
  padding-bottom:0.85rem; border-bottom:1px solid var(--border);
}

/* ═══════════════════════════
   WIDGETS
═══════════════════════════ */
label, div[data-testid="stWidgetLabel"] p {
  font-family:'Plus Jakarta Sans',sans-serif !important;
  font-size:0.80rem !important; font-weight:600 !important;
  color:var(--ink-70) !important; letter-spacing:-0.01em !important;
}
div[data-baseweb="select"] > div {
  background:var(--bg3) !important; border:1px solid var(--border) !important;
  border-radius:10px !important; min-height:40px !important;
  color:var(--ink) !important; -webkit-text-fill-color:var(--ink) !important;
  font-family:'Plus Jakarta Sans',sans-serif !important;
  font-size:0.83rem !important; font-weight:500 !important;
  transition:border-color 0.18s,box-shadow 0.18s !important;
}
div[data-baseweb="select"] span,div[data-baseweb="select"] input {
  color:var(--ink) !important; -webkit-text-fill-color:var(--ink) !important;
  opacity:1 !important; font-family:'Plus Jakarta Sans',sans-serif !important;
}
div[data-baseweb="select"] svg { color:var(--violet) !important; }
div[data-baseweb="select"] > div:focus-within {
  border-color:var(--violet) !important;
  box-shadow:0 0 0 3px var(--violet-l), 0 0 20px rgba(167,139,250,0.18) !important;
}
[data-baseweb="menu"],[data-baseweb="popover"]>div {
  background:var(--bg3) !important; border:1px solid var(--border) !important;
  border-radius:12px !important;
  box-shadow:0 16px 50px rgba(0,0,0,0.6),0 0 40px rgba(167,139,250,0.12) !important;
}
[data-baseweb="option"] {
  color:var(--ink) !important; font-family:'Plus Jakarta Sans',sans-serif !important;
  font-weight:500 !important; font-size:0.83rem !important;
  border-radius:7px !important; margin:2px 6px !important;
  background:transparent !important;
}
[data-baseweb="option"]:hover,[data-baseweb="option"][aria-selected="true"] {
  background:var(--violet-ll) !important; color:var(--violet) !important;
}

[data-testid="stNumberInput"] input {
  background:var(--bg3) !important; border:1px solid var(--border) !important;
  border-radius:10px !important; color:var(--ink) !important;
  -webkit-text-fill-color:var(--ink) !important;
  font-family:'Plus Jakarta Sans',sans-serif !important;
  font-weight:500 !important; font-size:0.83rem !important;
  transition:border-color 0.18s,box-shadow 0.18s !important;
}
[data-testid="stNumberInput"] input:focus {
  border-color:var(--violet) !important;
  box-shadow:0 0 0 3px var(--violet-l),0 0 20px rgba(167,139,250,0.18) !important;
  outline:none !important;
}
[data-testid="stNumberInput"] button {
  background:var(--bg3) !important; color:var(--ink-40) !important;
  border:1px solid var(--border) !important; border-radius:8px !important;
  font-weight:600 !important; transition:all 0.15s !important;
}
[data-testid="stNumberInput"] button:hover {
  background:var(--violet-l) !important; border-color:rgba(167,139,250,0.5) !important;
  color:var(--violet) !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"],
[data-testid="stSelectSlider"] [data-baseweb="slider"] [role="slider"] {
  width:22px !important; height:22px !important;
  background:var(--bg2) !important;
  border:2.5px solid var(--violet) !important;
  border-radius:50% !important;
  box-shadow:0 0 0 4px var(--violet-l),0 0 14px rgba(167,139,250,0.45) !important;
  transition:box-shadow 0.18s,transform 0.18s !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"]:hover,
[data-testid="stSelectSlider"] [data-baseweb="slider"] [role="slider"]:hover {
  box-shadow:0 0 0 7px var(--violet-l),0 0 22px rgba(167,139,250,0.60) !important;
  transform:scale(1.12) !important;
}
[data-testid="stSlider"] p,[data-testid="stSelectSlider"] p {
  color:var(--violet) !important; font-weight:600 !important; font-size:0.78rem !important;
}

/* ═══════════════════════════
   BUTTON
═══════════════════════════ */
div.stButton > button {
  width:100% !important;
  background:linear-gradient(135deg,var(--violet-d),var(--magenta)) !important;
  color:white !important; border:none !important;
  border-radius:14px !important; padding:0.88rem 2rem !important;
  font-family:'Plus Jakarta Sans',sans-serif !important;
  font-weight:700 !important; font-size:0.90rem !important;
  letter-spacing:-0.01em !important;
  box-shadow:0 4px 0 rgba(100,40,180,0.50),0 8px 30px rgba(167,139,250,0.40) !important;
  transform:translateY(0) !important;
  transition:transform 0.13s cubic-bezier(0.22,1,0.36,1),box-shadow 0.13s !important;
  position:relative; overflow:hidden; margin-top:1.1rem !important;
}
div.stButton > button::after {
  content:""; position:absolute; top:0; left:-120%;
  width:60%; height:100%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.25),transparent);
  transform:skewX(-20deg);
  animation:sheen 3.5s ease-in-out infinite 0.8s;
}
@keyframes sheen{0%{left:-120%}35%{left:140%}100%{left:140%}}
div.stButton > button:hover {
  box-shadow:0 6px 0 rgba(100,40,180,0.50),0 14px 40px rgba(167,139,250,0.55) !important;
  transform:translateY(-2px) !important;
}
div.stButton > button:active {
  box-shadow:0 1px 0 rgba(100,40,180,0.50),0 3px 10px rgba(167,139,250,0.22) !important;
  transform:translateY(3px) !important;
}

/* ═══════════════════════════
   RESULTS
═══════════════════════════ */
.results-bar {
  display:flex; align-items:center; gap:0.8rem;
  margin:2rem 0 1.6rem;
  animation:fadeUp 0.35s ease both;
}
.results-line{flex:1;height:1px;background:var(--border);}
.results-tag{
  font-size:0.68rem; font-weight:600; letter-spacing:0.10em;
  text-transform:uppercase; color:var(--ink-40); white-space:nowrap;
}

.score-block { padding:1.4rem 0 0.6rem; animation:popIn 0.6s cubic-bezier(0.22,1,0.36,1) 0.06s both; }
@keyframes popIn{from{opacity:0;transform:scale(0.80);}to{opacity:1;transform:scale(1);}}
.score-val {
  font-size:5.5rem; font-weight:800;
  letter-spacing:-0.06em; line-height:1;
  display:inline-flex; align-items:flex-start; gap:4px;
}
.score-pct { font-size:2rem; font-weight:400; opacity:0.30; margin-top:0.7rem; }
.score-label {
  font-size:0.72rem; font-weight:600; letter-spacing:0.06em;
  text-transform:uppercase; margin-top:0.25rem; opacity:0.55;
}

.ptrack { height:5px; border-radius:999px; background:var(--ink-08); overflow:hidden; margin:0.8rem 0 0.3rem; }
.ptrack-fill {
  height:100%; border-radius:999px;
  animation:grow 1.0s cubic-bezier(0.22,1,0.36,1) both;
  box-shadow:0 0 12px var(--clr,rgba(167,139,250,0.8));
}
@keyframes grow{from{width:0%}}

.gauge {
  background:var(--bg3); border:1px solid var(--border);
  border-radius:10px; padding:0.78rem 0.9rem 0.65rem; margin-top:0.8rem;
}
.gauge-bar {
  height:7px; border-radius:999px; position:relative;
  background:linear-gradient(90deg,#2dd4bf 0%,#a78bfa 35%,#fbbf24 60%,#fb7185 100%);
  box-shadow:0 0 18px rgba(167,139,250,0.35);
}
.gauge-pin {
  position:absolute; top:50%; width:15px; height:15px;
  background:var(--bg2); border:2.5px solid white; border-radius:50%;
  box-shadow:0 0 10px rgba(240,238,255,0.7),0 1px 5px rgba(0,0,0,0.5);
  transform:translateX(-50%) translateY(-50%);
  animation:pinPop 0.65s cubic-bezier(0.34,1.56,0.64,1) 0.2s both;
}
@keyframes pinPop{from{opacity:0;transform:translateX(-50%) translateY(-50%) scale(0);}to{opacity:1;transform:translateX(-50%) translateY(-50%) scale(1);}}
.gauge-ticks { display:flex; justify-content:space-between; margin-top:0.45rem; }
.gauge-tick { font-size:0.62rem; font-weight:500; color:var(--ink-40); }

.badge {
  display:inline-flex; align-items:center; gap:6px;
  border-radius:8px; padding:0.32rem 0.75rem;
  font-size:0.70rem; font-weight:700;
  letter-spacing:0.04em; text-transform:uppercase;
  border:1px solid; margin-top:0.9rem;
  animation:fadeUp 0.4s ease 0.3s both;
}
.bdot{width:5px;height:5px;border-radius:50%;background:currentColor;animation:glow 2s ease-in-out infinite;}
.b-low  {color:var(--teal);border-color:rgba(45,212,191,0.35);background:var(--teal-l);}
.b-med  {color:var(--gold);border-color:rgba(251,191,36,0.35);background:var(--gold-l);}
.b-high {color:var(--rose);border-color:rgba(251,113,133,0.35);background:var(--rose-l);}

.mrow{
  display:flex; justify-content:space-between; align-items:center;
  padding:0.52rem 0; border-bottom:1px solid var(--border); gap:1rem;
}
.mrow:last-child{border-bottom:none;}
.mk{font-size:0.72rem;font-weight:500;color:var(--ink-40);}
.mv{font-size:0.83rem;font-weight:700;color:var(--white);text-align:right;}

.action {
  border-radius:10px; padding:0.95rem 1.1rem; margin:0.9rem 0;
  background:var(--violet-ll); border:1px solid var(--violet-l);
  animation:fadeUp 0.4s ease 0.15s both;
}
.action-t{font-size:0.90rem;font-weight:700;color:var(--violet);margin-bottom:0.25rem;}
.action-d{font-size:0.79rem;color:var(--ink-40);line-height:1.6;}

.driver{
  display:flex; gap:0.8rem; align-items:flex-start;
  padding:0.75rem 0; border-bottom:1px solid var(--border);
  animation:fadeUp 0.38s ease both;
}
.driver:last-child{border-bottom:none;}
.driver-n{
  font-size:0.62rem; font-weight:700;
  width:22px; height:22px; border-radius:6px;
  background:var(--violet-ll); border:1px solid var(--violet-l);
  color:var(--violet); display:flex; align-items:center; justify-content:center;
  flex-shrink:0; margin-top:1px;
}
.driver-t{font-size:0.83rem;font-weight:700;color:var(--white);margin-bottom:0.1rem;}
.driver-d{font-size:0.77rem;color:var(--ink-40);line-height:1.55;}
.driver:nth-child(1){animation-delay:.04s}.driver:nth-child(2){animation-delay:.08s}
.driver:nth-child(3){animation-delay:.12s}.driver:nth-child(4){animation-delay:.16s}
.driver:nth-child(5){animation-delay:.20s}.driver:nth-child(6){animation-delay:.24s}
.driver:nth-child(7){animation-delay:.28s}

.footer{
  text-align:center; margin-top:3rem; padding-top:1.2rem;
  border-top:1px solid var(--border);
  font-size:0.68rem; color:var(--ink-40);
}
</style>

<!-- Floating car SVG -->
<div class="float-car">
<svg width="280" height="120" viewBox="0 0 280 120" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- car body -->
  <rect x="20" y="55" width="240" height="50" rx="12" fill="#a78bfa" opacity="0.9"/>
  <!-- cabin -->
  <path d="M60 55 Q75 20 120 18 L200 18 Q225 18 240 40 L240 55Z" fill="#c4b5fd"/>
  <!-- windows -->
  <rect x="75" y="24" width="55" height="28" rx="5" fill="#0b0e1a" opacity="0.8"/>
  <rect x="140" y="24" width="55" height="28" rx="5" fill="#0b0e1a" opacity="0.8"/>
  <!-- wheels -->
  <circle cx="72" cy="105" r="22" fill="#1e1b4b"/>
  <circle cx="72" cy="105" r="14" fill="#4c1d95"/>
  <circle cx="72" cy="105" r="6" fill="#a78bfa"/>
  <circle cx="208" cy="105" r="22" fill="#1e1b4b"/>
  <circle cx="208" cy="105" r="14" fill="#4c1d95"/>
  <circle cx="208" cy="105" r="6" fill="#a78bfa"/>
  <!-- headlight -->
  <ellipse cx="258" cy="73" rx="8" ry="5" fill="#fbbf24" opacity="0.9"/>
  <ellipse cx="258" cy="73" rx="18" ry="3" fill="#fbbf24" opacity="0.2"/>
  <!-- shield logo on door -->
  <path d="M135 62 L155 62 L155 85 Q145 92 135 85 Z" fill="#f472b6" opacity="0.7"/>
  <path d="M140 72 L143 75 L150 68" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- speed lines -->
  <line x1="0" y1="70" x2="18" y2="70" stroke="#a78bfa" stroke-width="1.5" opacity="0.6"/>
  <line x1="0" y1="78" x2="14" y2="78" stroke="#f472b6" stroke-width="1" opacity="0.4"/>
  <line x1="0" y1="62" x2="10" y2="62" stroke="#2dd4bf" stroke-width="1" opacity="0.4"/>
</svg>
</div>

<!-- Floating shield SVG -->
<div class="float-shield">
<svg width="120" height="140" viewBox="0 0 120 140" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="glow2">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <path d="M60 8 L10 28 L10 70 Q10 110 60 130 Q110 110 110 70 L110 28 Z"
        fill="#7c5cfc" opacity="0.7" filter="url(#glow2)"/>
  <path d="M60 20 L22 36 L22 70 Q22 100 60 118 Q98 100 98 70 L98 36 Z"
        fill="#a78bfa" opacity="0.5"/>
  <path d="M38 70 L52 84 L82 54" stroke="white" stroke-width="5"
        stroke-linecap="round" stroke-linejoin="round" opacity="0.9"/>
</svg>
</div>

<!-- Star particles -->
<script>
(function(){
  const count=55;
  for(let i=0;i<count;i++){
    const s=document.createElement('div');
    s.className='star';
    const sz=Math.random()*2.2+0.6;
    s.style.cssText=`
      width:${sz}px;height:${sz}px;
      left:${Math.random()*100}vw;
      top:${Math.random()*100}vh;
      --d:${(Math.random()*4+2).toFixed(1)}s;
      --delay:-${(Math.random()*6).toFixed(1)}s;
      --lo:${(Math.random()*0.08+0.04).toFixed(2)};
      --hi:${(Math.random()*0.55+0.25).toFixed(2)};
      opacity:0.1;
    `;
    document.body.appendChild(s);
  }
})();
</script>
"""


def render_theme() -> None:
    st.markdown(THEME_HTML, unsafe_allow_html=True)
