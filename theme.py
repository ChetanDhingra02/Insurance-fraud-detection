import streamlit as st
import streamlit.components.v1 as components


# ── CSS only — st.markdown handles <style> tags safely ────────────────────────
THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,300;1,400&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:         #060d1a;
  --bg2:        #0b1628;
  --bg3:        #0d1e35;
  --white:      #ffffff;
  --ink:        #e8f4f0;
  --ink-70:     rgba(232,244,240,0.75);
  --ink-40:     rgba(232,244,240,0.45);
  --ink-15:     rgba(232,244,240,0.15);
  --ink-08:     rgba(232,244,240,0.08);
  --aurora-g:   #3adb8a;
  --aurora-g-l: rgba(58,219,138,0.18);
  --aurora-g-ll:rgba(58,219,138,0.09);
  --aurora-t:   #2be8c8;
  --aurora-t-l: rgba(43,232,200,0.18);
  --aurora-b:   #5ab4ff;
  --aurora-b-l: rgba(90,180,255,0.18);
  --aurora-v:   #a078ff;
  --aurora-v-l: rgba(160,120,255,0.18);
  --aurora-v-ll:rgba(160,120,255,0.09);
  --aurora-r:   #ff7eb3;
  --aurora-r-l: rgba(255,126,179,0.18);
  --gold:       #ffc060;
  --gold-l:     rgba(255,192,96,0.18);
  --border:     rgba(58,219,138,0.18);
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
.hdr-icon { width:32px; height:32px; border-radius:10px; background:linear-gradient(135deg,#3adb8a,#2be8c8); display:flex; align-items:center; justify-content:center; box-shadow:0 2px 14px rgba(58,219,138,0.55),0 4px 30px rgba(43,232,200,0.25); flex-shrink:0; animation:iconPulse 4s ease-in-out infinite; }
@keyframes iconPulse { 0%,100%{box-shadow:0 2px 14px rgba(58,219,138,0.55),0 4px 30px rgba(43,232,200,0.25);} 50%{box-shadow:0 2px 28px rgba(58,219,138,0.90),0 4px 55px rgba(90,180,255,0.40);} }
.hdr-icon svg { width:15px; height:15px; }
.hdr-name { font-size:1.0rem; font-weight:800; letter-spacing:-0.02em; background:linear-gradient(135deg,#3adb8a,#2be8c8); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.hdr-divider { width:1px; height:14px; background:var(--border); margin:0 0.3rem; }
.hdr-sub { font-size:0.78rem; font-weight:500; color:var(--ink-40); }
.hdr-r { display:flex; align-items:center; gap:0.4rem; }
.chip { font-size:0.70rem; font-weight:600; padding:0.22rem 0.65rem; border-radius:99px; background:rgba(255,255,255,0.06); color:var(--ink-70); border:1px solid var(--border); }
.chip-live { background:var(--aurora-g-l); color:var(--aurora-g); border-color:rgba(58,219,138,0.40); display:flex; align-items:center; gap:5px; }
.live-dot { width:5px; height:5px; border-radius:50%; background:var(--aurora-g); animation:glow 2.4s ease-in-out infinite; }
@keyframes glow { 0%,100%{box-shadow:0 0 0 0 rgba(58,219,138,0.8);} 50%{box-shadow:0 0 0 6px rgba(58,219,138,0);} }

/* HERO */
.hero { display:flex; align-items:center; justify-content:space-between; gap:2rem; padding:1.6rem 0 1.5rem; border-bottom:1.5px solid var(--border); margin-bottom:2rem; animation:fadeUp 0.55s cubic-bezier(0.22,1,0.36,1) 0.08s both; }
@keyframes fadeUp { from{opacity:0;transform:translateY(12px);} to{opacity:1;transform:translateY(0);} }
.hero-title { font-size:1.45rem; font-weight:800; letter-spacing:-0.03em; line-height:1; color:var(--ink); }
.hero-title span { background:linear-gradient(135deg,#3adb8a,#5ab4ff); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.hero-desc { font-size:0.82rem; color:var(--ink-40); line-height:1.55; max-width:340px; border-left:2.5px solid var(--border); padding-left:0.85rem; margin-top:0.5rem; }
.hero-pills { display:flex; gap:0.4rem; flex-shrink:0; }
.hpill { font-size:0.72rem; font-weight:700; padding:0.35rem 0.8rem; border-radius:12px; color:var(--ink); background:rgba(255,255,255,0.05); border:1.5px solid var(--border); display:flex; flex-direction:column; align-items:center; gap:1px; box-shadow:0 2px 12px rgba(58,219,138,0.15); transition:box-shadow 0.2s,border-color 0.2s; }
.hpill:hover { box-shadow:0 4px 28px rgba(58,219,138,0.40); border-color:#3adb8a; }
.hpill-v { font-size:1.1rem; font-weight:800; letter-spacing:-0.02em; color:#3adb8a; }
.hpill-l { font-size:0.60rem; font-weight:600; color:var(--ink-40); text-transform:uppercase; letter-spacing:0.07em; }

/* CARDS */
.card { background:rgba(255,255,255,0.04); border:1.5px solid var(--border); border-radius:var(--radius); padding:1.4rem 1.5rem; margin-bottom:0.9rem; box-shadow:0 2px 20px rgba(0,0,0,0.40),inset 0 1px 0 rgba(255,255,255,0.06); transition:box-shadow 0.3s,border-color 0.25s,transform 0.25s cubic-bezier(0.22,1,0.36,1); animation:cardUp 0.48s cubic-bezier(0.22,1,0.36,1) both; position:relative; overflow:hidden; backdrop-filter:blur(12px); }
.card::before { content:""; position:absolute; top:0; left:0; right:0; height:2px; background:linear-gradient(90deg,transparent,#3adb8a,#2be8c8,#5ab4ff,#a078ff,transparent); opacity:0; transition:opacity 0.3s; }
.card:hover { box-shadow:0 8px 40px rgba(58,219,138,0.20),0 2px 10px rgba(90,180,255,0.15); border-color:rgba(58,219,138,0.38); transform:translateY(-2px); }
.card:hover::before { opacity:1; }
@keyframes cardUp { from{opacity:0;transform:translateY(14px);} to{opacity:1;transform:translateY(0);} }
.card::after { content:""; position:absolute; width:260px; height:260px; border-radius:50%; background:radial-gradient(circle,rgba(58,219,138,0.06) 0%,transparent 70%); top:-80px; right:-80px; pointer-events:none; }
.ctag { font-size:0.65rem; font-weight:700; letter-spacing:0.10em; text-transform:uppercase; color:#2be8c8; margin-bottom:0.22rem; }
.ctitle { font-size:1.0rem; font-weight:800; letter-spacing:-0.02em; color:var(--ink); margin-bottom:0.16rem; }
.cnote { font-size:0.79rem; color:var(--ink-40); line-height:1.55; margin-bottom:0.95rem; padding-bottom:0.85rem; border-bottom:1px solid var(--border); }

/* WIDGETS — dark overrides */
label, div[data-testid="stWidgetLabel"] p { font-family:'Nunito',sans-serif !important; font-size:0.80rem !important; font-weight:700 !important; color:var(--ink-70) !important; letter-spacing:-0.01em !important; }
div[data-baseweb="select"] > div { background:rgba(255,255,255,0.06) !important; border:1.5px solid var(--border) !important; border-radius:10px !important; min-height:40px !important; color:var(--ink) !important; -webkit-text-fill-color:var(--ink) !important; font-family:'Nunito',sans-serif !important; font-size:0.83rem !important; font-weight:600 !important; transition:border-color 0.18s,box-shadow 0.18s !important; }
div[data-baseweb="select"] span,div[data-baseweb="select"] input { color:var(--ink) !important; -webkit-text-fill-color:var(--ink) !important; opacity:1 !important; font-family:'Nunito',sans-serif !important; }
div[data-baseweb="select"] svg { color:#3adb8a !important; }
div[data-baseweb="select"] > div:focus-within { border-color:#3adb8a !important; box-shadow:0 0 0 3px rgba(58,219,138,0.20),0 0 22px rgba(58,219,138,0.18) !important; }
[data-baseweb="menu"],[data-baseweb="popover"]>div { background:rgba(11,22,40,0.97) !important; border:1.5px solid var(--border) !important; border-radius:14px !important; box-shadow:0 20px 60px rgba(0,0,0,0.55),0 0 35px rgba(58,219,138,0.12) !important; }
[data-baseweb="option"] { color:var(--ink) !important; font-family:'Nunito',sans-serif !important; font-weight:600 !important; font-size:0.83rem !important; border-radius:7px !important; margin:2px 6px !important; background:transparent !important; }
[data-baseweb="option"]:hover,[data-baseweb="option"][aria-selected="true"] { background:rgba(58,219,138,0.15) !important; color:#3adb8a !important; }
[data-testid="stNumberInput"] input { background:rgba(255,255,255,0.06) !important; border:1.5px solid var(--border) !important; border-radius:10px !important; color:var(--ink) !important; -webkit-text-fill-color:var(--ink) !important; font-family:'Nunito',sans-serif !important; font-weight:600 !important; font-size:0.83rem !important; transition:border-color 0.18s,box-shadow 0.18s !important; }
[data-testid="stNumberInput"] input:focus { border-color:#3adb8a !important; box-shadow:0 0 0 3px rgba(58,219,138,0.20),0 0 20px rgba(58,219,138,0.16) !important; outline:none !important; }
[data-testid="stNumberInput"] button { background:rgba(255,255,255,0.06) !important; color:var(--ink-40) !important; border:1.5px solid var(--border) !important; border-radius:8px !important; font-weight:700 !important; transition:all 0.15s !important; }
[data-testid="stNumberInput"] button:hover { background:rgba(58,219,138,0.15) !important; border-color:rgba(58,219,138,0.5) !important; color:#3adb8a !important; }
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"],[data-testid="stSelectSlider"] [data-baseweb="slider"] [role="slider"] { width:22px !important; height:22px !important; background:#0b1628 !important; border:2.5px solid #3adb8a !important; border-radius:50% !important; box-shadow:0 0 0 4px rgba(58,219,138,0.20),0 2px 14px rgba(58,219,138,0.50) !important; transition:box-shadow 0.18s,transform 0.18s !important; }
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"]:hover,[data-testid="stSelectSlider"] [data-baseweb="slider"] [role="slider"]:hover { box-shadow:0 0 0 7px rgba(58,219,138,0.20),0 2px 24px rgba(58,219,138,0.65) !important; transform:scale(1.12) !important; }
[data-testid="stSlider"] p,[data-testid="stSelectSlider"] p { color:#3adb8a !important; font-weight:700 !important; font-size:0.78rem !important; }

/* BUTTON */
div.stButton > button { width:100% !important; background:linear-gradient(135deg,#3adb8a,#2be8c8) !important; color:#060d1a !important; border:none !important; border-radius:14px !important; padding:0.88rem 2rem !important; font-family:'Nunito',sans-serif !important; font-weight:800 !important; font-size:0.90rem !important; letter-spacing:-0.01em !important; box-shadow:0 4px 0 rgba(20,80,55,0.50),0 8px 32px rgba(58,219,138,0.45) !important; transform:translateY(0) !important; transition:transform 0.13s cubic-bezier(0.22,1,0.36,1),box-shadow 0.13s !important; margin-top:1.1rem !important; }
div.stButton > button:hover { box-shadow:0 6px 0 rgba(20,80,55,0.50),0 14px 44px rgba(58,219,138,0.65) !important; transform:translateY(-2px) !important; }
div.stButton > button:active { box-shadow:0 1px 0 rgba(20,80,55,0.50),0 3px 12px rgba(58,219,138,0.25) !important; transform:translateY(3px) !important; }

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
.gauge { background:rgba(255,255,255,0.04); border:1.5px solid var(--border); border-radius:12px; padding:0.78rem 0.9rem 0.65rem; margin-top:0.8rem; }
.gauge-bar { height:7px; border-radius:999px; position:relative; background:linear-gradient(90deg,#3adb8a 0%,#2be8c8 30%,#5ab4ff 60%,#a078ff 80%,#ff7eb3 100%); box-shadow:0 2px 16px rgba(58,219,138,0.40); }
.gauge-pin { position:absolute; top:50%; width:15px; height:15px; background:#0b1628; border:2.5px solid #3adb8a; border-radius:50%; box-shadow:0 0 14px rgba(58,219,138,0.75),0 1px 5px rgba(0,0,0,0.40); transform:translateX(-50%) translateY(-50%); animation:pinPop 0.65s cubic-bezier(0.34,1.56,0.64,1) 0.2s both; }
@keyframes pinPop { from{opacity:0;transform:translateX(-50%) translateY(-50%) scale(0);} to{opacity:1;transform:translateX(-50%) translateY(-50%) scale(1);} }
.gauge-ticks { display:flex; justify-content:space-between; margin-top:0.45rem; }
.gauge-tick { font-size:0.62rem; font-weight:600; color:var(--ink-40); }
.badge { display:inline-flex; align-items:center; gap:6px; border-radius:8px; padding:0.32rem 0.75rem; font-size:0.70rem; font-weight:800; letter-spacing:0.04em; text-transform:uppercase; border:1.5px solid; margin-top:0.9rem; animation:fadeUp 0.4s ease 0.3s both; }
.bdot { width:5px; height:5px; border-radius:50%; background:currentColor; animation:glow 2s ease-in-out infinite; }
.b-low  { color:#3adb8a; border-color:rgba(58,219,138,0.40);  background:rgba(58,219,138,0.12); }
.b-med  { color:#ffc060; border-color:rgba(255,192,96,0.40);  background:rgba(255,192,96,0.12); }
.b-high { color:#ff7eb3; border-color:rgba(255,126,179,0.40); background:rgba(255,126,179,0.12); }
.mrow { display:flex; justify-content:space-between; align-items:center; padding:0.52rem 0; border-bottom:1px solid var(--border); gap:1rem; }
.mrow:last-child { border-bottom:none; }
.mk { font-size:0.72rem; font-weight:600; color:var(--ink-40); }
.mv { font-size:0.83rem; font-weight:800; color:var(--ink); text-align:right; }
.action { border-radius:12px; padding:0.95rem 1.1rem; margin:0.9rem 0; background:rgba(58,219,138,0.08); border:1.5px solid rgba(58,219,138,0.22); animation:fadeUp 0.4s ease 0.15s both; }
.action-t { font-size:0.90rem; font-weight:800; color:#3adb8a; margin-bottom:0.25rem; }
.action-d { font-size:0.79rem; color:var(--ink-40); line-height:1.6; }
.driver { display:flex; gap:0.8rem; align-items:flex-start; padding:0.75rem 0; border-bottom:1px solid var(--border); animation:fadeUp 0.38s ease both; }
.driver:last-child { border-bottom:none; }
.driver-n { font-size:0.62rem; font-weight:800; width:22px; height:22px; border-radius:6px; background:rgba(58,219,138,0.08); border:1.5px solid rgba(58,219,138,0.22); color:#3adb8a; display:flex; align-items:center; justify-content:center; flex-shrink:0; margin-top:1px; }
.driver-t { font-size:0.83rem; font-weight:800; color:var(--ink); margin-bottom:0.1rem; }
.driver-d { font-size:0.77rem; color:var(--ink-40); line-height:1.55; }
.driver:nth-child(1){animation-delay:.04s}.driver:nth-child(2){animation-delay:.08s}
.driver:nth-child(3){animation-delay:.12s}.driver:nth-child(4){animation-delay:.16s}
.driver:nth-child(5){animation-delay:.20s}.driver:nth-child(6){animation-delay:.24s}
.driver:nth-child(7){animation-delay:.28s}
.footer { text-align:center; margin-top:3rem; padding-top:1.2rem; border-top:1.5px solid var(--border); font-size:0.68rem; color:var(--ink-40); }
</style>
"""

# ── Decorative aurora layer ────────────────────────────────────────────────────
# Rendered in a real iframe — script/filter/SVG all safe here.
# height=320 gives it real screen estate. The margin hack below collapses
# Streamlit's dead space so the app content follows directly after.
AURORA_DECORATION = """<!DOCTYPE html>
<html>
<head>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
html, body { background:#060d1a; overflow:hidden; width:100%; height:100%; }

.star { position:fixed; border-radius:50%; background:white; pointer-events:none; animation:twinkle var(--td,3s) ease-in-out infinite var(--tdelay,0s); }
@keyframes twinkle { 0%,100%{opacity:var(--tmin,0.2);transform:scale(1);} 50%{opacity:var(--tmax,0.9);transform:scale(1.3);} }

/* screen blend = additive glow on dark background — this is the key difference from multiply */
.aurora { position:fixed; border-radius:60% 40% 55% 45% / 40% 60% 40% 60%; filter:blur(38px); opacity:0; pointer-events:none; mix-blend-mode:screen; animation:sway var(--dur,18s) ease-in-out infinite var(--dly,0s); }
@keyframes sway {
  0%   { opacity:0;               transform:translateY(0) scaleX(1); }
  12%  { opacity:var(--pk,0.55); }
  45%  { opacity:var(--pk,0.55);  transform:translateY(var(--up,-22px)) scaleX(1.07); }
  78%  { opacity:var(--pk,0.55);  transform:translateY(var(--dn,10px))  scaleX(0.96); }
  90%  { opacity:0; }
  100% { opacity:0;               transform:translateY(0) scaleX(1); }
}

.wisp { position:fixed; top:0; left:-320px; pointer-events:none; opacity:0; animation:drift var(--wdur,32s) linear infinite var(--wdly,0s); }
@keyframes drift { 0%{left:-320px;opacity:0;} 8%{opacity:0.55;} 88%{opacity:0.55;} 100%{left:110vw;opacity:0;} }

.deer { position:fixed; bottom:60px; right:-280px; pointer-events:none; opacity:0; animation:deerWalk 28s linear infinite 4s; }
@keyframes deerWalk { 0%{right:-280px;opacity:0;} 6%{opacity:0.30;} 88%{opacity:0.30;} 100%{right:110vw;opacity:0;} }
.deer-fl { transform-origin:50px 78px;  animation:legSwing  0.7s ease-in-out infinite alternate; }
.deer-bl { transform-origin:155px 78px; animation:legSwing  0.7s ease-in-out infinite alternate-reverse; }
.deer-fr { transform-origin:60px 78px;  animation:legSwing2 0.7s ease-in-out infinite alternate-reverse; }
.deer-br { transform-origin:148px 78px; animation:legSwing2 0.7s ease-in-out infinite alternate; }
@keyframes legSwing  { from{transform:rotate(-14deg);} to{transform:rotate(14deg);} }
@keyframes legSwing2 { from{transform:rotate(-10deg);} to{transform:rotate(12deg);} }
.deer-body { animation:deerBob 1.4s ease-in-out infinite; }
@keyframes deerBob { 0%,100%{transform:translateY(0);} 50%{transform:translateY(-3px);} }

.flake { position:fixed; border-radius:50%; pointer-events:none; opacity:0; animation:fall var(--fd,12s) linear infinite var(--fdelay,0s); }
@keyframes fall { 0%{transform:translateY(-10px) translateX(0);opacity:0;} 8%{opacity:var(--fop,0.55);} 85%{opacity:var(--fop,0.55);} 100%{transform:translateY(105vh) translateX(var(--fdx,20px));opacity:0;} }
</style>
</head>
<body>

<div class="aurora" style="width:800px;height:360px;top:-80px;left:2%;  background:radial-gradient(ellipse,#00ff88 0%,#00d4aa 50%,transparent 80%);--dur:20s;--dly:0s; --pk:0.50;--up:-24px;--dn:12px;"></div>
<div class="aurora" style="width:680px;height:300px;top:-40px;left:30%; background:radial-gradient(ellipse,#60b0ff 0%,#8844ff 55%,transparent 80%);--dur:26s;--dly:-9s; --pk:0.42;--up:-18px;--dn:16px;"></div>
<div class="aurora" style="width:560px;height:260px;top:0px;  left:60%; background:radial-gradient(ellipse,#00e8ff 0%,#3a8aff 60%,transparent 80%);--dur:23s;--dly:-15s;--pk:0.38;--up:-14px;--dn:10px;"></div>
<div class="aurora" style="width:900px;height:220px;top:120px;left:-10%;background:radial-gradient(ellipse,#00ffcc 0%,#00aa66 60%,transparent 80%);--dur:30s;--dly:-6s; --pk:0.28;--up:-10px;--dn:6px;"></div>
<div class="aurora" style="width:420px;height:200px;top:-20px;left:78%; background:radial-gradient(ellipse,#ff66cc 0%,#aa44ff 60%,transparent 80%);--dur:19s;--dly:-11s;--pk:0.30;--up:-16px;--dn:8px;"></div>

<div class="wisp" style="top:40px;--wdur:34s;--wdly:10s;">
  <svg width="300" height="100" viewBox="0 0 300 100" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M10 60 Q80 18 160 38 Q220 52 290 30" stroke="#00ff88" stroke-width="24" stroke-linecap="round" fill="none" opacity="0.38"/>
    <path d="M10 72 Q90 32 170 52 Q230 64 290 44" stroke="#5ab4ff" stroke-width="16" stroke-linecap="round" fill="none" opacity="0.30"/>
    <path d="M30 80 Q100 46 175 60 Q240 72 290 54" stroke="#a078ff" stroke-width="10" stroke-linecap="round" fill="none" opacity="0.26"/>
    <path d="M15 58 Q85 20 162 40 Q222 54 288 32" stroke="#00e8ff" stroke-width="2.5" stroke-linecap="round" fill="none" opacity="0.60"/>
  </svg>
</div>

<div class="deer">
  <svg width="240" height="130" viewBox="0 0 240 130" fill="none" xmlns="http://www.w3.org/2000/svg">
    <g opacity="0.88">
      <path d="M82 42 C78 30 68 18 60 10" stroke="#2be8c8" stroke-width="3.5" stroke-linecap="round" fill="none"/>
      <path d="M78 35 C70 28 62 26 55 22" stroke="#2be8c8" stroke-width="2.5" stroke-linecap="round" fill="none"/>
      <path d="M74 28 C72 20 74 14 76 8"  stroke="#2be8c8" stroke-width="2"   stroke-linecap="round" fill="none"/>
      <path d="M98 42 C102 30 112 18 120 10" stroke="#2be8c8" stroke-width="3.5" stroke-linecap="round" fill="none"/>
      <path d="M102 35 C110 28 118 26 125 22" stroke="#2be8c8" stroke-width="2.5" stroke-linecap="round" fill="none"/>
      <path d="M106 28 C108 20 106 14 104 8"  stroke="#2be8c8" stroke-width="2"   stroke-linecap="round" fill="none"/>
    </g>
    <g class="deer-body">
      <ellipse cx="100" cy="72" rx="52" ry="28" fill="#1a3a4a" opacity="0.95"/>
      <ellipse cx="100" cy="80" rx="30" ry="15" fill="#234a5a" opacity="0.70"/>
      <path d="M78 52 Q82 38 90 36 Q100 34 104 40 L104 55 Q96 60 86 58Z" fill="#1a3a4a" opacity="0.95"/>
      <ellipse cx="94" cy="34" rx="18" ry="14" fill="#1a3a4a" opacity="0.98"/>
      <circle  cx="100" cy="30" r="3.5" fill="#e8f4f0"/>
      <circle  cx="101.2" cy="29" r="1.2" fill="#2be8c8" opacity="0.9"/>
      <ellipse cx="150" cy="66" rx="8"  ry="6"  fill="#2be8c8" opacity="0.55"/>
      <g class="deer-fl"><rect x="74"  y="90" width="8" height="32" rx="4" fill="#1a3a4a" opacity="0.90"/><ellipse cx="78"  cy="122" rx="5" ry="3" fill="#0d2535"/></g>
      <g class="deer-fr"><rect x="88"  y="90" width="8" height="32" rx="4" fill="#1a3a4a" opacity="0.90"/><ellipse cx="92"  cy="122" rx="5" ry="3" fill="#0d2535"/></g>
      <g class="deer-bl"><rect x="110" y="90" width="8" height="32" rx="4" fill="#1a3a4a" opacity="0.90"/><ellipse cx="114" cy="122" rx="5" ry="3" fill="#0d2535"/></g>
      <g class="deer-br"><rect x="124" y="90" width="8" height="32" rx="4" fill="#1a3a4a" opacity="0.90"/><ellipse cx="128" cy="122" rx="5" ry="3" fill="#0d2535"/></g>
    </g>
  </svg>
</div>

<script>
(function() {
  // 120 twinkling stars
  for (var i = 0; i < 120; i++) {
    var s = document.createElement('div');
    s.className = 'star';
    var sz = Math.random() * 2.2 + 0.5;
    s.style.width  = sz + 'px';
    s.style.height = sz + 'px';
    s.style.left   = (Math.random() * 100).toFixed(2) + 'vw';
    s.style.top    = (Math.random() * 100).toFixed(2) + 'vh';
    s.style.setProperty('--td',     (Math.random() * 4 + 1.5).toFixed(1) + 's');
    s.style.setProperty('--tdelay', '-' + (Math.random() * 6).toFixed(1) + 's');
    s.style.setProperty('--tmin',   (Math.random() * 0.15 + 0.10).toFixed(2));
    s.style.setProperty('--tmax',   (Math.random() * 0.45 + 0.55).toFixed(2));
    document.body.appendChild(s);
  }
  // Falling aurora particles
  var cols = ['#3adb8a','#2be8c8','#5ab4ff','#a078ff','#ff7eb3','#00e8ff'];
  for (var j = 0; j < 45; j++) {
    var p = document.createElement('div');
    p.className = 'flake';
    var fsz = Math.random() * 3 + 1.5;
    p.style.width      = fsz + 'px';
    p.style.height     = fsz + 'px';
    p.style.left       = (Math.random() * 100).toFixed(1) + 'vw';
    p.style.top        = '-10px';
    p.style.background = cols[Math.floor(Math.random() * cols.length)];
    p.style.setProperty('--fd',     (Math.random() * 14 + 8).toFixed(1) + 's');
    p.style.setProperty('--fdelay', '-' + (Math.random() * 20).toFixed(1) + 's');
    p.style.setProperty('--fop',    (Math.random() * 0.50 + 0.25).toFixed(2));
    p.style.setProperty('--fdx',    (Math.random() * 70 - 35).toFixed(0) + 'px');
    document.body.appendChild(p);
  }
})();
</script>
</body>
</html>"""


def render_theme() -> None:
    # 1. Inject all CSS (safe — Streamlit handles bare <style> blocks)
    st.markdown(THEME_CSS, unsafe_allow_html=True)

    # 2. Aurora sky in a real iframe (height=320 gives it actual pixels)
    components.html(AURORA_DECORATION, height=320, scrolling=False)

    # 3. Collapse the physical gap the iframe leaves in Streamlit's layout.
    #    The iframe sits at the top of the page; we pull everything after it
    #    back up with a negative margin so it overlaps — the aurora becomes
    #    a true background layer behind the rest of the app content.
    st.markdown(
        """<style>
        div[data-testid="stHtml"] > iframe { display:block; margin-bottom:-330px !important; }
        </style>""",
        unsafe_allow_html=True,
    )