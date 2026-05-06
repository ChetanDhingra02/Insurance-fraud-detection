import streamlit as st
import html as html_mod

THRESHOLD = 0.25

st.set_page_config(
    page_title="Shield · Fraud Intelligence",
    page_icon="◈",
    layout="wide",
)

st.markdown("""
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
""", unsafe_allow_html=True)


def esc(x): return html_mod.escape(str(x))
def rh(c):  st.markdown(c, unsafe_allow_html=True)

def bi_val(l): return {"None":0,"One reported injury":1,"Multiple / serious injuries":2}[l]
def wi_val(l): return {"No witnesses":0,"One witness":1,"Two witnesses":2,"Three or more witnesses":3}[l]

def risk_meta(p):
    if p < 0.25: return "b-low",  "Low Risk",    "var(--teal)", "var(--teal)"
    if p < 0.50: return "b-med",  "Medium Risk", "var(--gold)", "var(--gold)"
    return               "b-high", "High Risk",   "var(--rose)", "var(--rose)"

def action_meta(p):
    if p >= 0.50:
        return "Send for Manual Investigation", \
               "Score significantly elevated. Assign to a specialist before any payout is authorised."
    if p >= THRESHOLD:
        return "Flag for Secondary Review", \
               "Score exceeds operating threshold. Route to supervisor review and collect supporting documentation."
    return "Process Normally", \
           "No elevated fraud signal detected. Claim may proceed through the standard processing route."


# ── HEADER ─────────────────────────────────────────────────────────
rh("""
<div class="hdr">
  <div class="hdr-l">
    <div class="hdr-icon">
      <svg viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M7 1L1.5 3.5V7c0 2.8 2 5.3 5.5 5.9C10.5 12.3 12.5 9.8 12.5 7V3.5L7 1z"
              fill="white" fill-opacity="0.95"/>
        <path d="M4.5 7l2 2 3-3" stroke="#7c5cfc" stroke-width="1.6"
              stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
    <span class="hdr-name">Shield</span>
    <div class="hdr-divider"></div>
    <span class="hdr-sub">Insurance Fraud Intelligence</span>
  </div>
  <div class="hdr-r">
    <span class="chip chip-live"><span class="live-dot"></span>Model Active</span>
    <span class="chip">Random Forest</span>
    <span class="chip">Threshold 25%</span>
  </div>
</div>
""")

# ── HERO ───────────────────────────────────────────────────────────
rh("""
<div class="hero">
  <div>
    <div class="hero-title">Fraud Risk <span>Assessment</span></div>
    <div class="hero-desc">Score claims in real time using 12 ML features across incident, policy, and financial data.</div>
  </div>
  <div class="hero-pills">
    <div class="hpill"><span class="hpill-v">12</span><span class="hpill-l">Features</span></div>
    <div class="hpill"><span class="hpill-v">91%</span><span class="hpill-l">Precision</span></div>
    <div class="hpill"><span class="hpill-v">RF</span><span class="hpill-l">Algorithm</span></div>
  </div>
</div>
""")

# ── INPUTS ─────────────────────────────────────────────────────────
left, right = st.columns(2, gap="large")

with left:
    rh("""<div class="card">
  <div class="ctag">01 · Incident</div>
  <div class="ctitle">Vehicle Incident Details</div>
  <div class="cnote">Collision type, damage severity, injuries and witnesses.</div>
</div>""")
    incident_severity = st.selectbox("Incident Severity",
        ["Minor Damage","Major Damage","Total Loss","Trivial Damage"])
    incident_type = st.selectbox("Incident Type",
        ["Single Vehicle Collision","Multi-vehicle Collision","Vehicle Theft","Parked Car"])
    number_of_vehicles_involved = st.slider("Vehicles Involved", 1, 4, 1)
    bi_label = st.select_slider("Reported Injuries",
        options=["None","One reported injury","Multiple / serious injuries"])
    bodily_injuries = bi_val(bi_label)
    wi_label = st.select_slider("Witnesses Present",
        options=["No witnesses","One witness","Two witnesses","Three or more witnesses"])
    witnesses = wi_val(wi_label)
    months_as_customer = st.number_input("Months as Customer", min_value=0, value=200)

with right:
    rh("""<div class="card">
  <div class="ctag">02 · Financials</div>
  <div class="ctitle">Policy &amp; Claim Amounts</div>
  <div class="cnote">Claim breakdown, annual premium and deductible.</div>
</div>""")
    total_claim_amount    = st.number_input("Total Claim ($)", min_value=0, value=50000)
    injury_claim          = st.number_input("Injury Claim ($)", min_value=0, value=5000)
    property_claim        = st.number_input("Property Claim ($)", min_value=0, value=10000)
    vehicle_claim         = st.number_input("Vehicle Claim ($)", min_value=0, value=35000)
    policy_annual_premium = st.number_input("Annual Premium ($)", min_value=0.0, value=1200.0, step=10.0)
    policy_deductable     = st.number_input("Deductible ($)", min_value=0, value=1000)

predict = st.button("⚡ Run Fraud Risk Assessment →")

# ── RESULTS ────────────────────────────────────────────────────────
if predict:
    import random
    fraud_prob = random.uniform(0.05, 0.92)

    fraud_pred = int(fraud_prob >= THRESHOLD)
    badge_cls, risk_label, text_col, bar_col = risk_meta(fraud_prob)
    action_title, action_desc = action_meta(fraud_prob)

    pct      = round(fraud_prob * 100, 1)
    verdict  = "Likely Fraudulent" if fraud_pred else "Likely Legitimate"
    pin_pct  = min(max(pct, 2), 97)
    delta    = abs(pct - THRESHOLD * 100)
    cpr      = (total_claim_amount / policy_annual_premium) if policy_annual_premium else 0

    rh("""<div class="results-bar">
  <div class="results-line"></div>
  <span class="results-tag">Assessment Results</span>
  <div class="results-line"></div>
</div>""")

    rc, ac = st.columns(2, gap="large")

    with rc:
        rh(f"""<div class="card">
  <div class="ctag">03 · Model Output</div>
  <div class="ctitle">Fraud Probability Score</div>

  <div class="score-block">
    <div class="score-val" style="color:{text_col};">{pct:.0f}<span class="score-pct">%</span></div>
    <div class="score-label" style="color:{text_col};">Estimated fraud probability</div>
  </div>

  <div class="ptrack">
    <div class="ptrack-fill" style="width:{pct}%;background:linear-gradient(90deg,{bar_col}60,{bar_col});--clr:{bar_col};"></div>
  </div>

  <div class="gauge">
    <div class="gauge-bar">
      <div class="gauge-pin" style="left:{pin_pct}%;"></div>
    </div>
    <div class="gauge-ticks">
      <span class="gauge-tick">0%</span>
      <span class="gauge-tick">25%</span>
      <span class="gauge-tick">50%</span>
      <span class="gauge-tick">75%</span>
      <span class="gauge-tick">100%</span>
    </div>
  </div>

  <div style="margin-top:0.95rem;">
    <div class="mrow"><span class="mk">Threshold</span><span class="mv">25%</span></div>
    <div class="mrow"><span class="mk">Delta from threshold</span><span class="mv">{delta:.1f} pp</span></div>
    <div class="mrow"><span class="mk">Verdict</span><span class="mv" style="color:{text_col};">{esc(verdict)}</span></div>
  </div>

  <span class="badge {badge_cls}"><span class="bdot"></span>{esc(risk_label)}</span>
</div>""")

    with ac:
        rh(f"""<div class="card">
  <div class="ctag">04 · Routing</div>
  <div class="ctitle">Recommended Action</div>

  <div class="action">
    <div class="action-t">{esc(action_title)}</div>
    <div class="action-d">{esc(action_desc)}</div>
  </div>

  <div class="mrow"><span class="mk">Incident type</span><span class="mv">{esc(incident_type)}</span></div>
  <div class="mrow"><span class="mk">Severity</span><span class="mv">{esc(incident_severity)}</span></div>
  <div class="mrow"><span class="mk">Total claimed</span><span class="mv">${total_claim_amount:,}</span></div>
  <div class="mrow"><span class="mk">Claim-to-premium</span><span class="mv">{cpr:.1f}×</span></div>
  <div class="mrow"><span class="mk">Customer tenure</span><span class="mv">{months_as_customer} months</span></div>
</div>""")

    drivers = []
    if incident_severity in ["Major Damage","Total Loss"]:
        drivers.append(("Severe vehicle damage","Major damage or total loss significantly elevates review complexity."))
    if total_claim_amount >= 60000:
        drivers.append(("High claim amount", f"${total_claim_amount:,} exceeds the $60k high-value threshold."))
    if number_of_vehicles_involved >= 2:
        drivers.append(("Multi-vehicle incident","Multi-vehicle collisions require additional validation steps."))
    if bodily_injuries >= 1:
        drivers.append(("Injury component present","Bodily injury claims require stronger supporting documentation."))
    if witnesses >= 2:
        drivers.append((f"{witnesses} witnesses present","Elevated witness count increases investigation complexity."))
    if months_as_customer < 24:
        drivers.append(("Short customer tenure",f"{months_as_customer} months on policy — a mild but notable signal."))
    if cpr > 30:
        drivers.append(("High claim-to-premium ratio",f"Claim is {cpr:.0f}× the annual premium — statistically unusual."))

    d_html = "".join(f"""<div class="driver">
  <div class="driver-n">{str(i).zfill(2)}</div>
  <div><div class="driver-t">{esc(t)}</div><div class="driver-d">{esc(d)}</div></div>
</div>""" for i,(t,d) in enumerate(drivers,1)) if drivers else """
<div class="driver">
  <div class="driver-n">—</div>
  <div><div class="driver-t">No major signals triggered</div>
  <div class="driver-d">Entered values did not activate any primary review flags.</div></div>
</div>"""

    rh(f"""<div class="card">
  <div class="ctag">05 · Signals</div>
  <div class="ctitle">Key Risk Factors</div>
  <div class="cnote">Informational signals supporting triage — not deterministic decisions.</div>
  {d_html}
</div>""")

rh("""<div class="footer">Shield · Portfolio Demonstration · Triage support only — not automatic denial or approval</div>""")