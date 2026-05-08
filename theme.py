import streamlit as st
import streamlit.components.v1 as components


# ── CSS only — st.markdown handles <style> tags safely ────────────────────────
THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,300;1,400&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:         #eaf4f0;
  --bg2:        #f4faf7;
  --bg3:        #dff0ea;
  --white:      #ffffff;
  --ink:        #1a3330;
  --ink-70:     rgba(26,51,48,0.70);
  --ink-40:     rgba(26,51,48,0.42);
  --ink-15:     rgba(26,51,48,0.15);
  --ink-08:     rgba(26,51,48,0.08);
  --aurora-g:   #3aab7b;
  --aurora-g-l: rgba(58,171,123,0.18);
  --aurora-g-ll:rgba(58,171,123,0.09);
  --aurora-t:   #2bb5a0;
  --aurora-t-l: rgba(43,181,160,0.18);
  --aurora-b:   #5a86c8;
  --aurora-b-l: rgba(90,134,200,0.18);
  --aurora-v:   #7c68c2;
  --aurora-v-l: rgba(124,104,194,0.18);
  --aurora-v-ll:rgba(124,104,194,0.09);
  --aurora-r:   #c86a7c;
  --aurora-r-l: rgba(200,106,124,0.18);
  --gold:       #d4913a;
  --gold-l:     rgba(212,145,58,0.18);
  --border:     rgba(58,171,123,0.22);
  --radius:     18px;
}

html, body, [class*="css"] {
  font-family: 'Nunito', sans-serif !important;
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

/* HEADER */
.hdr { display:flex; align-items:center; justify-content:space-between; padding:1.1rem 0 1.0rem; border-bottom:1.5px solid var(--border); animation:slideDown 0.5s cubic-bezier(0.22,1,0.36,1) both; }
@keyframes slideDown { from{opacity:0;transform:translateY(-8px);} to{opacity:1;transform:translateY(0);} }
.hdr-l { display:flex; align-items:center; gap:0.6rem; }
.hdr-icon { width:32px; height:32px; border-radius:10px; background:linear-gradient(135deg,#3aab7b,#2bb5a0); display:flex; align-items:center; justify-content:center; box-shadow:0 2px 14px rgba(58,171,123,0.45),0 4px 30px rgba(43,181,160,0.18); flex-shrink:0; animation:iconPulse 4s ease-in-out infinite; }
@keyframes iconPulse { 0%,100%{box-shadow:0 2px 14px rgba(58,171,123,0.45),0 4px 30px rgba(43,181,160,0.18);} 50%{box-shadow:0 2px 22px rgba(58,171,123,0.75),0 4px 50px rgba(90,134,200,0.28);} }
.hdr-icon svg { width:15px; height:15px; }
.hdr-name { font-size:1.0rem; font-weight:800; letter-spacing:-0.02em; background:linear-gradient(135deg,#3aab7b,#2bb5a0); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.hdr-divider { width:1px; height:14px; background:var(--border); margin:0 0.3rem; }
.hdr-sub { font-size:0.78rem; font-weight:500; color:var(--ink-40); }
.hdr-r { display:flex; align-items:center; gap:0.4rem; }
.chip { font-size:0.70rem; font-weight:600; padding:0.22rem 0.65rem; border-radius:99px; background:rgba(255,255,255,0.65); color:var(--ink-70); border:1px solid var(--border); }
.chip-live { background:var(--aurora-g-l); color:var(--aurora-g); border-color:rgba(58,171,123,0.40); display:flex; align-items:center; gap:5px; }
.live-dot { width:5px; height:5px; border-radius:50%; background:var(--aurora-g); animation:glow 2.4s ease-in-out infinite; }
@keyframes glow { 0%,100%{box-shadow:0 0 0 0 rgba(58,171,123,0.7);} 50%{box-shadow:0 0 0 5px rgba(58,171,123,0);} }

/* HERO */
.hero { display:flex; align-items:center; justify-content:space-between; gap:2rem; padding:1.6rem 0 1.5rem; border-bottom:1.5px solid var(--border); margin-bottom:2rem; animation:fadeUp 0.55s cubic-bezier(0.22,1,0.36,1) 0.08s both; }
@keyframes fadeUp { from{opacity:0;transform:translateY(12px);} to{opacity:1;transform:translateY(0);} }
.hero-title { font-size:1.45rem; font-weight:800; letter-spacing:-0.03em; line-height:1; color:var(--ink); }
.hero-title span { background:linear-gradient(135deg,#3aab7b,#5a86c8); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.hero-desc { font-size:0.82rem; color:var(--ink-40); line-height:1.55; max-width:340px; border-left:2.5px solid var(--border); padding-left:0.85rem; margin-top:0.5rem; }
.hero-pills { display:flex; gap:0.4rem; flex-shrink:0; }
.hpill { font-size:0.72rem; font-weight:700; padding:0.35rem 0.8rem; border-radius:12px; color:var(--ink); background:rgba(255,255,255,0.70); border:1.5px solid var(--border); display:flex; flex-direction:column; align-items:center; gap:1px; box-shadow:0 2px 10px rgba(58,171,123,0.12); transition:box-shadow 0.2s,border-color 0.2s; }
.hpill:hover { box-shadow:0 4px 22px rgba(58,171,123,0.30); border-color:#3aab7b; }
.hpill-v { font-size:1.1rem; font-weight:800; letter-spacing:-0.02em; color:#3aab7b; }
.hpill-l { font-size:0.60rem; font-weight:600; color:var(--ink-40); text-transform:uppercase; letter-spacing:0.07em; }

/* CARDS */
.card { background:rgba(255,255,255,0.72); border:1.5px solid var(--border); border-radius:var(--radius); padding:1.4rem 1.5rem; margin-bottom:0.9rem; box-shadow:0 2px 12px rgba(58,171,123,0.08),inset 0 1px 0 rgba(255,255,255,0.9); transition:box-shadow 0.3s,border-color 0.25s,transform 0.25s cubic-bezier(0.22,1,0.36,1); animation:cardUp 0.48s cubic-bezier(0.22,1,0.36,1) both; position:relative; overflow:hidden; }
.card::before { content:""; position:absolute; top:0; left:0; right:0; height:2px; background:linear-gradient(90deg,transparent,#3aab7b,#2bb5a0,#5a86c8,transparent); opacity:0; transition:opacity 0.3s; }
.card:hover { box-shadow:0 6px 32px rgba(58,171,123,0.18),0 2px 8px rgba(90,134,200,0.10); border-color:rgba(58,171,123,0.42); transform:translateY(-2px); }
.card:hover::before { opacity:1; }
@keyframes cardUp { from{opacity:0;transform:translateY(14px);} to{opacity:1;transform:translateY(0);} }
.card::after { content:""; position:absolute; width:220px; height:220px; border-radius:50%; background:radial-gradient(circle,rgba(58,171,123,0.05) 0%,transparent 70%); top:-70px; right:-70px; pointer-events:none; }
.ctag { font-size:0.65rem; font-weight:700; letter-spacing:0.10em; text-transform:uppercase; color:#2bb5a0; margin-bottom:0.22rem; }
.ctitle { font-size:1.0rem; font-weight:800; letter-spacing:-0.02em; color:var(--ink); margin-bottom:0.16rem; }
.cnote { font-size:0.79rem; color:var(--ink-40); line-height:1.55; margin-bottom:0.95rem; padding-bottom:0.85rem; border-bottom:1px solid var(--border); }

/* WIDGETS */
label, div[data-testid="stWidgetLabel"] p { font-family:'Nunito',sans-serif !important; font-size:0.80rem !important; font-weight:700 !important; color:var(--ink-70) !important; letter-spacing:-0.01em !important; }
div[data-baseweb="select"] > div { background:rgba(255,255,255,0.80) !important; border:1.5px solid var(--border) !important; border-radius:10px !important; min-height:40px !important; color:var(--ink) !important; -webkit-text-fill-color:var(--ink) !important; font-family:'Nunito',sans-serif !important; font-size:0.83rem !important; font-weight:600 !important; transition:border-color 0.18s,box-shadow 0.18s !important; }
div[data-baseweb="select"] span,div[data-baseweb="select"] input { color:var(--ink) !important; -webkit-text-fill-color:var(--ink) !important; opacity:1 !important; font-family:'Nunito',sans-serif !important; }
div[data-baseweb="select"] svg { color:#3aab7b !important; }
div[data-baseweb="select"] > div:focus-within { border-color:#3aab7b !important; box-shadow:0 0 0 3px rgba(58,171,123,0.18),0 0 18px rgba(58,171,123,0.15) !important; }
[data-baseweb="menu"],[data-baseweb="popover"]>div { background:rgba(244,250,247,0.97) !important; border:1.5px solid var(--border) !important; border-radius:14px !important; box-shadow:0 16px 50px rgba(26,51,48,0.14),0 0 30px rgba(58,171,123,0.10) !important; }
[data-baseweb="option"] { color:var(--ink) !important; font-family:'Nunito',sans-serif !important; font-weight:600 !important; font-size:0.83rem !important; border-radius:7px !important; margin:2px 6px !important; background:transparent !important; }
[data-baseweb="option"]:hover,[data-baseweb="option"][aria-selected="true"] { background:rgba(58,171,123,0.18) !important; color:#3aab7b !important; }
[data-testid="stNumberInput"] input { background:rgba(255,255,255,0.80) !important; border:1.5px solid var(--border) !important; border-radius:10px !important; color:var(--ink) !important; -webkit-text-fill-color:var(--ink) !important; font-family:'Nunito',sans-serif !important; font-weight:600 !important; font-size:0.83rem !important; transition:border-color 0.18s,box-shadow 0.18s !important; }
[data-testid="stNumberInput"] input:focus { border-color:#3aab7b !important; box-shadow:0 0 0 3px rgba(58,171,123,0.18),0 0 18px rgba(58,171,123,0.15) !important; outline:none !important; }
[data-testid="stNumberInput"] button { background:rgba(255,255,255,0.80) !important; color:var(--ink-40) !important; border:1.5px solid var(--border) !important; border-radius:8px !important; font-weight:700 !important; transition:all 0.15s !important; }
[data-testid="stNumberInput"] button:hover { background:rgba(58,171,123,0.18) !important; border-color:rgba(58,171,123,0.5) !important; color:#3aab7b !important; }
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"],[data-testid="stSelectSlider"] [data-baseweb="slider"] [role="slider"] { width:22px !important; height:22px !important; background:white !important; border:2.5px solid #3aab7b !important; border-radius:50% !important; box-shadow:0 0 0 4px rgba(58,171,123,0.18),0 2px 12px rgba(58,171,123,0.40) !important; transition:box-shadow 0.18s,transform 0.18s !important; }
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"]:hover,[data-testid="stSelectSlider"] [data-baseweb="slider"] [role="slider"]:hover { box-shadow:0 0 0 7px rgba(58,171,123,0.18),0 2px 20px rgba(58,171,123,0.55) !important; transform:scale(1.12) !important; }
[data-testid="stSlider"] p,[data-testid="stSelectSlider"] p { color:#3aab7b !important; font-weight:700 !important; font-size:0.78rem !important; }

/* BUTTON */
div.stButton > button { width:100% !important; background:linear-gradient(135deg,#3aab7b,#2bb5a0) !important; color:white !important; border:none !important; border-radius:14px !important; padding:0.88rem 2rem !important; font-family:'Nunito',sans-serif !important; font-weight:800 !important; font-size:0.90rem !important; letter-spacing:-0.01em !important; box-shadow:0 4px 0 rgba(30,100,80,0.30),0 8px 28px rgba(58,171,123,0.38) !important; transform:translateY(0) !important; transition:transform 0.13s cubic-bezier(0.22,1,0.36,1),box-shadow 0.13s !important; position:relative; overflow:hidden; margin-top:1.1rem !important; }
div.stButton > button:hover { box-shadow:0 6px 0 rgba(30,100,80,0.30),0 14px 38px rgba(58,171,123,0.55) !important; transform:translateY(-2px) !important; }
div.stButton > button:active { box-shadow:0 1px 0 rgba(30,100,80,0.30),0 3px 10px rgba(58,171,123,0.22) !important; transform:translateY(3px) !important; }

/* RESULTS */
.results-bar { display:flex; align-items:center; gap:0.8rem; margin:2rem 0 1.6rem; animation:fadeUp 0.35s ease both; }
.results-line { flex:1; height:1.5px; background:var(--border); }
.results-tag { font-size:0.68rem; font-weight:700; letter-spacing:0.10em; text-transform:uppercase; color:var(--ink-40); white-space:nowrap; }
.score-block { padding:1.4rem 0 0.6rem; animation:popIn 0.6s cubic-bezier(0.22,1,0.36,1) 0.06s both; }
@keyframes popIn { from{opacity:0;transform:scale(0.80);} to{opacity:1;transform:scale(1);} }
.score-val { font-size:5.5rem; font-weight:800; letter-spacing:-0.06em; line-height:1; display:inline-flex; align-items:flex-start; gap:4px; }
.score-pct { font-size:2rem; font-weight:400; opacity:0.30; margin-top:0.7rem; }
.score-label { font-size:0.72rem; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; margin-top:0.25rem; opacity:0.55; }
.ptrack { height:5px; border-radius:999px; background:var(--ink-08); overflow:hidden; margin:0.8rem 0 0.3rem; }
.ptrack-fill { height:100%; border-radius:999px; animation:grow 1.0s cubic-bezier(0.22,1,0.36,1) both; }
@keyframes grow { from{width:0%} }
.gauge { background:rgba(255,255,255,0.65); border:1.5px solid var(--border); border-radius:12px; padding:0.78rem 0.9rem 0.65rem; margin-top:0.8rem; }
.gauge-bar { height:7px; border-radius:999px; position:relative; background:linear-gradient(90deg,#3aab7b 0%,#2bb5a0 30%,#5a86c8 60%,#7c68c2 80%,#c86a7c 100%); box-shadow:0 2px 12px rgba(58,171,123,0.28); }
.gauge-pin { position:absolute; top:50%; width:15px; height:15px; background:white; border:2.5px solid #3aab7b; border-radius:50%; box-shadow:0 0 10px rgba(58,171,123,0.6),0 1px 5px rgba(0,0,0,0.18); transform:translateX(-50%) translateY(-50%); animation:pinPop 0.65s cubic-bezier(0.34,1.56,0.64,1) 0.2s both; }
@keyframes pinPop { from{opacity:0;transform:translateX(-50%) translateY(-50%) scale(0);} to{opacity:1;transform:translateX(-50%) translateY(-50%) scale(1);} }
.gauge-ticks { display:flex; justify-content:space-between; margin-top:0.45rem; }
.gauge-tick { font-size:0.62rem; font-weight:600; color:var(--ink-40); }
.badge { display:inline-flex; align-items:center; gap:6px; border-radius:8px; padding:0.32rem 0.75rem; font-size:0.70rem; font-weight:800; letter-spacing:0.04em; text-transform:uppercase; border:1.5px solid; margin-top:0.9rem; animation:fadeUp 0.4s ease 0.3s both; }
.bdot { width:5px; height:5px; border-radius:50%; background:currentColor; animation:glow 2s ease-in-out infinite; }
.b-low  { color:#3aab7b; border-color:rgba(58,171,123,0.40);  background:rgba(58,171,123,0.18); }
.b-med  { color:#d4913a; border-color:rgba(212,145,58,0.40);  background:rgba(212,145,58,0.18); }
.b-high { color:#c86a7c; border-color:rgba(200,106,124,0.40); background:rgba(200,106,124,0.18); }
.mrow { display:flex; justify-content:space-between; align-items:center; padding:0.52rem 0; border-bottom:1px solid var(--border); gap:1rem; }
.mrow:last-child { border-bottom:none; }
.mk { font-size:0.72rem; font-weight:600; color:var(--ink-40); }
.mv { font-size:0.83rem; font-weight:800; color:var(--ink); text-align:right; }
.action { border-radius:12px; padding:0.95rem 1.1rem; margin:0.9rem 0; background:rgba(58,171,123,0.09); border:1.5px solid rgba(58,171,123,0.18); animation:fadeUp 0.4s ease 0.15s both; }
.action-t { font-size:0.90rem; font-weight:800; color:#3aab7b; margin-bottom:0.25rem; }
.action-d { font-size:0.79rem; color:var(--ink-40); line-height:1.6; }
.driver { display:flex; gap:0.8rem; align-items:flex-start; padding:0.75rem 0; border-bottom:1px solid var(--border); animation:fadeUp 0.38s ease both; }
.driver:last-child { border-bottom:none; }
.driver-n { font-size:0.62rem; font-weight:800; width:22px; height:22px; border-radius:6px; background:rgba(58,171,123,0.09); border:1.5px solid rgba(58,171,123,0.18); color:#3aab7b; display:flex; align-items:center; justify-content:center; flex-shrink:0; margin-top:1px; }
.driver-t { font-size:0.83rem; font-weight:800; color:var(--ink); margin-bottom:0.1rem; }
.driver-d { font-size:0.77rem; color:var(--ink-40); line-height:1.55; }
.driver:nth-child(1){animation-delay:.04s}.driver:nth-child(2){animation-delay:.08s}
.driver:nth-child(3){animation-delay:.12s}.driver:nth-child(4){animation-delay:.16s}
.driver:nth-child(5){animation-delay:.20s}.driver:nth-child(6){animation-delay:.24s}
.driver:nth-child(7){animation-delay:.28s}
.footer { text-align:center; margin-top:3rem; padding-top:1.2rem; border-top:1.5px solid var(--border); font-size:0.68rem; color:var(--ink-40); }
</style>
"""

# ── Decorative layer — full HTML document rendered in an iframe ───────────────
# st.components.v1.html() creates a real iframe, bypassing React's DOM entirely.
# <script>, SVG, CSS filters — all work here without any sanitisation.
AURORA_DECORATION = """<!DOCTYPE html>
<html>
<head>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
html, body { background:transparent; overflow:hidden; width:100%; height:100%; }

.aurora-curtain {
  position:fixed; border-radius:60% 40% 55% 45% / 40% 60% 40% 60%;
  filter:blur(32px); opacity:0; pointer-events:none; mix-blend-mode:multiply;
  animation:auroraSway var(--dur,18s) ease-in-out infinite var(--dly,0s);
}
@keyframes auroraSway {
  0%   { opacity:0; transform:translateY(0) scaleX(1); }
  12%  { opacity:var(--peak,0.28); }
  45%  { opacity:var(--peak,0.28); transform:translateY(var(--lift,-18px)) scaleX(1.06); }
  78%  { opacity:var(--peak,0.28); transform:translateY(var(--lift2,8px)) scaleX(0.97); }
  90%  { opacity:0; }
  100% { opacity:0; transform:translateY(0) scaleX(1); }
}

.float-deer { position:fixed; bottom:80px; right:-260px; pointer-events:none; opacity:0; animation:deerWalk 26s linear infinite 3s; }
@keyframes deerWalk { 0%{right:-260px;opacity:0;} 6%{opacity:0.22;} 88%{opacity:0.22;} 100%{right:110vw;opacity:0;} }
.deer-fl { transform-origin:50px 78px; animation:legSwing  0.7s ease-in-out infinite alternate; }
.deer-bl { transform-origin:155px 78px; animation:legSwing  0.7s ease-in-out infinite alternate-reverse; }
.deer-fr { transform-origin:60px 78px;  animation:legSwing2 0.7s ease-in-out infinite alternate-reverse; }
.deer-br { transform-origin:148px 78px; animation:legSwing2 0.7s ease-in-out infinite alternate; }
@keyframes legSwing  { from{transform:rotate(-14deg);} to{transform:rotate(14deg);} }
@keyframes legSwing2 { from{transform:rotate(-10deg);} to{transform:rotate(12deg);} }
.deer-body { animation:deerBob 1.4s ease-in-out infinite; }
@keyframes deerBob { 0%,100%{transform:translateY(0);} 50%{transform:translateY(-3px);} }

.float-wisp { position:fixed; top:80px; left:-280px; pointer-events:none; opacity:0; animation:wispDrift 30s ease-in-out infinite 8s; }
@keyframes wispDrift {
  0%   { left:-280px; opacity:0;    transform:translateY(0) rotate(-4deg); }
  10%  { opacity:0.18; }
  50%  { left:48%;    opacity:0.18; transform:translateY(-22px) rotate(4deg); }
  90%  { opacity:0.18; }
  100% { left:110vw;  opacity:0;    transform:translateY(0) rotate(-4deg); }
}

.snow { position:fixed; border-radius:50%; pointer-events:none; opacity:0; animation:snowfall var(--sd,12s) linear infinite var(--sdelay,0s); }
@keyframes snowfall {
  0%   { transform:translateY(-10px) translateX(0); opacity:0; }
  8%   { opacity:var(--sop,0.55); }
  85%  { opacity:var(--sop,0.55); }
  100% { transform:translateY(105vh) translateX(var(--dx,20px)); opacity:0; }
}
</style>
</head>
<body>

<div class="aurora-curtain" style="width:700px;height:320px;top:-60px;left:5%;background:radial-gradient(ellipse,#5cca9a 0%,#2bb5a0 50%,transparent 80%);--dur:20s;--dly:0s;--peak:0.22;--lift:-20px;--lift2:10px;"></div>
<div class="aurora-curtain" style="width:600px;height:280px;top:-20px;left:38%;background:radial-gradient(ellipse,#7caee8 0%,#7c68c2 55%,transparent 80%);--dur:25s;--dly:-8s;--peak:0.18;--lift:-14px;--lift2:16px;"></div>
<div class="aurora-curtain" style="width:500px;height:240px;top:10px;left:65%;background:radial-gradient(ellipse,#3aab7b 0%,#5a86c8 60%,transparent 80%);--dur:22s;--dly:-14s;--peak:0.16;--lift:-10px;--lift2:12px;"></div>
<div class="aurora-curtain" style="width:800px;height:200px;top:100px;left:-8%;background:radial-gradient(ellipse,#2bb5a0 0%,#3aab7b 60%,transparent 80%);--dur:28s;--dly:-5s;--peak:0.12;--lift:-8px;--lift2:6px;"></div>

<div class="float-deer">
<svg width="240" height="130" viewBox="0 0 240 130" fill="none" xmlns="http://www.w3.org/2000/svg">
  <g opacity="0.92">
    <path d="M82 42 C78 30 68 18 60 10" stroke="#5a3a1a" stroke-width="3.5" stroke-linecap="round" fill="none"/>
    <path d="M78 35 C70 28 62 26 55 22" stroke="#5a3a1a" stroke-width="2.5" stroke-linecap="round" fill="none"/>
    <path d="M74 28 C72 20 74 14 76 8"  stroke="#5a3a1a" stroke-width="2"   stroke-linecap="round" fill="none"/>
    <path d="M98 42 C102 30 112 18 120 10" stroke="#5a3a1a" stroke-width="3.5" stroke-linecap="round" fill="none"/>
    <path d="M102 35 C110 28 118 26 125 22" stroke="#5a3a1a" stroke-width="2.5" stroke-linecap="round" fill="none"/>
    <path d="M106 28 C108 20 106 14 104 8"  stroke="#5a3a1a" stroke-width="2"   stroke-linecap="round" fill="none"/>
  </g>
  <g class="deer-body">
    <ellipse cx="100" cy="72" rx="52" ry="28" fill="#c8956a" opacity="0.92"/>
    <ellipse cx="100" cy="80" rx="30" ry="15" fill="#ddb896" opacity="0.70"/>
    <path d="M78 52 Q82 38 90 36 Q100 34 104 40 L104 55 Q96 60 86 58Z" fill="#c8956a" opacity="0.92"/>
    <ellipse cx="94" cy="34" rx="18" ry="14" fill="#c8956a" opacity="0.95"/>
    <ellipse cx="88" cy="40" rx="8"  ry="5"  fill="#b07850" opacity="0.80"/>
    <circle  cx="100" cy="30" r="3.5" fill="#2a1a0a"/>
    <circle  cx="101.2" cy="29" r="1.2" fill="white" opacity="0.8"/>
    <ellipse cx="112" cy="26" rx="7" ry="4"   fill="#c8956a" transform="rotate(-30 112 26)"/>
    <ellipse cx="112" cy="26" rx="4" ry="2.5" fill="#e8b08a" opacity="0.6" transform="rotate(-30 112 26)"/>
    <ellipse cx="83"  cy="42" rx="3" ry="2"   fill="#8a4a30"/>
    <ellipse cx="100" cy="56" rx="12" ry="9"  fill="#e8d0b8" opacity="0.50"/>
    <ellipse cx="150" cy="66" rx="8"  ry="6"  fill="#f0e4d8" opacity="0.85"/>
    <g class="deer-fl"><rect x="74"  y="90" width="8" height="32" rx="4" fill="#a07045" opacity="0.90"/><ellipse cx="78"  cy="122" rx="5" ry="3" fill="#5a3a1a"/></g>
    <g class="deer-fr"><rect x="88"  y="90" width="8" height="32" rx="4" fill="#a07045" opacity="0.90"/><ellipse cx="92"  cy="122" rx="5" ry="3" fill="#5a3a1a"/></g>
    <g class="deer-bl"><rect x="110" y="90" width="8" height="32" rx="4" fill="#a07045" opacity="0.90"/><ellipse cx="114" cy="122" rx="5" ry="3" fill="#5a3a1a"/></g>
    <g class="deer-br"><rect x="124" y="90" width="8" height="32" rx="4" fill="#a07045" opacity="0.90"/><ellipse cx="128" cy="122" rx="5" ry="3" fill="#5a3a1a"/></g>
    <ellipse cx="115" cy="60" rx="30" ry="10" fill="#3aab7b" opacity="0.28"/>
    <ellipse cx="125" cy="62" rx="18" ry="7"  fill="#5a86c8" opacity="0.20"/>
  </g>
</svg>
</div>

<div class="float-wisp">
<svg width="260" height="90" viewBox="0 0 260 90" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M10 55 Q60 20 130 35 Q190 50 250 28" stroke="#3aab7b" stroke-width="22" stroke-linecap="round" fill="none" opacity="0.32"/>
  <path d="M10 65 Q70 30 140 48 Q200 62 250 42" stroke="#5a86c8" stroke-width="16" stroke-linecap="round" fill="none" opacity="0.26"/>
  <path d="M30 72 Q90 42 150 56 Q210 68 250 50" stroke="#7c68c2" stroke-width="10" stroke-linecap="round" fill="none" opacity="0.22"/>
  <path d="M20 54 Q80 22 140 38 Q195 52 248 32" stroke="#2bb5a0" stroke-width="2"   stroke-linecap="round" fill="none" opacity="0.55"/>
  <path d="M25 62 Q85 34 145 50 Q200 62 248 44" stroke="#5a86c8" stroke-width="1.5" stroke-linecap="round" fill="none" opacity="0.42"/>
</svg>
</div>

<script>
(function() {
  var colors = ['#3aab7b','#2bb5a0','#5a86c8','#7c68c2','#c8e8d8'];
  for (var i = 0; i < 40; i++) {
    var p = document.createElement('div');
    p.className = 'snow';
    var sz = Math.random() * 3 + 1.5;
    var col = colors[Math.floor(Math.random() * colors.length)];
    p.style.width = sz + 'px';
    p.style.height = sz + 'px';
    p.style.left = (Math.random() * 100).toFixed(1) + 'vw';
    p.style.top = '-10px';
    p.style.background = col;
    p.style.setProperty('--sd',     (Math.random() * 14 + 8).toFixed(1) + 's');
    p.style.setProperty('--sdelay', '-' + (Math.random() * 20).toFixed(1) + 's');
    p.style.setProperty('--sop',    (Math.random() * 0.45 + 0.20).toFixed(2));
    p.style.setProperty('--dx',     (Math.random() * 60 - 30).toFixed(0) + 'px');
    document.body.appendChild(p);
  }
})();
</script>
</body>
</html>"""


def render_theme() -> None:
    # Inject CSS via st.markdown — Streamlit handles <style> blocks safely
    st.markdown(THEME_CSS, unsafe_allow_html=True)
    # Inject decorative animations in a real iframe — bypasses React entirely
    components.html(AURORA_DECORATION, height=0, scrolling=False)