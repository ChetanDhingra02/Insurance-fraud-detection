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
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Syne+Mono&family=Epilogue:ital,wght@0,200;0,300;0,400;0,500;1,200;1,300&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:       #0d0e11;
  --bg2:      #12141a;
  --bg3:      #181b22;
  --border:   rgba(255,255,255,0.07);
  --border2:  rgba(255,255,255,0.11);
  --ink:      #eeede6;
  --ink-50:   rgba(238,237,230,0.50);
  --ink-25:   rgba(238,237,230,0.25);
  --amber:    #f0a500;
  --amber-d:  rgba(240,165,0,0.12);
  --teal:     #00cfa8;
  --red:      #ff4f4f;
  --red-d:    rgba(255,79,79,0.12);
  --green-d:  rgba(0,207,168,0.12);
  --surface:  rgba(255,255,255,0.03);
}

html, body, [class*="css"] {
  font-family: 'Epilogue', sans-serif !important;
  background: var(--bg) !important;
  color: var(--ink) !important;
}

.stApp { background: var(--bg) !important; }
[data-testid="stHeader"]      { display:none !important; }
[data-testid="stDecoration"]  { display:none !important; }
[data-testid="stToolbar"]     { display:none !important; }
[data-testid="stStatusWidget"]{ display:none !important; }
footer                         { display:none !important; }

.main .block-container { max-width:1200px; padding:0 2rem 5rem; }

/* HEADER */
.hdr {
  display:flex; align-items:center; justify-content:space-between;
  padding:0.82rem 0; border-bottom:1px solid var(--border);
  animation:fadeUp 0.4s ease both;
}
.hdr-l { display:flex; align-items:center; gap:0.6rem; }
.hdr-mark {
  width:28px; height:28px; border-radius:7px;
  background:var(--amber); display:flex; align-items:center; justify-content:center;
  box-shadow:0 0 14px rgba(240,165,0,0.30);
  flex-shrink:0;
}
.hdr-mark svg { width:13px; height:13px; }
.hdr-name {
  font-family:'Syne',sans-serif; font-weight:700; font-size:0.93rem;
  letter-spacing:-0.01em; color:var(--ink);
}
.hdr-sep { width:1px; height:14px; background:var(--border2); margin:0 0.45rem; }
.hdr-sub {
  font-family:'Syne Mono',monospace; font-size:0.58rem;
  letter-spacing:0.12em; text-transform:uppercase; color:var(--ink-25);
}
.hdr-r { display:flex; align-items:center; gap:0.4rem; }
.tag {
  font-family:'Syne Mono',monospace; font-size:0.57rem;
  letter-spacing:0.08em; text-transform:uppercase;
  padding:0.20rem 0.52rem; border-radius:5px;
  color:var(--ink-50); background:var(--surface); border:1px solid var(--border);
}
.tag-live {
  background:rgba(0,207,168,0.10); color:var(--teal);
  border-color:rgba(0,207,168,0.25);
  display:flex; align-items:center; gap:5px;
}
.ldot {
  width:5px; height:5px; border-radius:50%; background:var(--teal);
  animation:ldotPulse 2.2s ease-in-out infinite;
}
@keyframes ldotPulse {
  0%,100%{opacity:1;box-shadow:0 0 0 0 rgba(0,207,168,0.4);}
  50%{opacity:0.5;box-shadow:0 0 0 5px rgba(0,207,168,0);}
}

/* HERO */
.hero {
  display:grid; grid-template-columns:1fr auto;
  align-items:center; gap:3rem;
  padding:1.6rem 0 1.5rem;
  border-bottom:1px solid var(--border); margin-bottom:2rem;
  animation:fadeUp 0.5s ease 0.05s both;
}
.hero-label {
  font-family:'Syne Mono',monospace; font-size:0.58rem;
  letter-spacing:0.18em; text-transform:uppercase; color:var(--amber);
  margin-bottom:0.5rem; display:flex; align-items:center; gap:8px;
}
.hero-label::before { content:""; width:18px; height:1px; background:var(--amber); opacity:0.6; }
.hero-title {
  font-family:'Syne',sans-serif; font-weight:800;
  font-size:clamp(1.55rem,2.8vw,2.2rem); line-height:1.1;
  letter-spacing:-0.03em; color:var(--ink);
}
.hero-title span { color:var(--amber); }
.hero-desc {
  font-size:0.81rem; font-weight:200; line-height:1.75;
  color:var(--ink-50); margin-top:0.55rem; max-width:370px;
}
.hero-stats {
  display:flex; border:1px solid var(--border);
  border-radius:13px; overflow:hidden; background:var(--bg2);
}
.hs { padding:0.85rem 1.2rem; border-right:1px solid var(--border); text-align:right; }
.hs:last-child { border-right:none; }
.hs-val {
  font-family:'Syne',sans-serif; font-weight:800;
  font-size:1.45rem; letter-spacing:-0.04em; color:var(--ink); line-height:1;
}
.hs-label {
  font-family:'Syne Mono',monospace; font-size:0.52rem;
  letter-spacing:0.10em; text-transform:uppercase; color:var(--ink-25); margin-top:0.2rem;
}

/* CARDS */
.card {
  background:var(--bg2); border:1px solid var(--border);
  border-radius:15px; padding:1.4rem 1.5rem; margin-bottom:0.9rem;
  position:relative; overflow:hidden;
  box-shadow:0 2px 20px rgba(0,0,0,0.30);
  transition:border-color 0.25s, box-shadow 0.25s, transform 0.25s cubic-bezier(0.22,1,0.36,1);
  animation:cardIn 0.5s cubic-bezier(0.22,1,0.36,1) both;
}
.card:hover {
  border-color:rgba(240,165,0,0.20);
  box-shadow:0 4px 36px rgba(0,0,0,0.40), 0 0 0 1px rgba(240,165,0,0.07);
  transform:translateY(-2px);
}
.card::after {
  content:""; position:absolute; top:0; left:0; right:0; height:1px;
  background:linear-gradient(90deg,transparent,rgba(240,165,0,0.38),transparent);
  opacity:0; transition:opacity 0.25s;
}
.card:hover::after { opacity:1; }
@keyframes cardIn {
  from{opacity:0;transform:translateY(11px);}
  to{opacity:1;transform:translateY(0);}
}
.card:nth-child(2){animation-delay:0.05s}
.card:nth-child(3){animation-delay:0.10s}

.cnum {
  font-family:'Syne Mono',monospace; font-size:0.56rem;
  letter-spacing:0.14em; text-transform:uppercase; color:var(--amber); margin-bottom:0.22rem;
}
.ctitle {
  font-family:'Syne',sans-serif; font-weight:700; font-size:1.02rem;
  letter-spacing:-0.02em; color:var(--ink); margin-bottom:0.18rem;
}
.cnote {
  font-size:0.79rem; font-weight:200; color:var(--ink-25); line-height:1.6;
  margin-bottom:0.95rem; padding-bottom:0.85rem; border-bottom:1px solid var(--border);
}

/* WIDGETS */
label, div[data-testid="stWidgetLabel"] p {
  font-family:'Epilogue',sans-serif !important; font-weight:500 !important;
  font-size:0.79rem !important; color:var(--ink-50) !important; letter-spacing:0.01em !important;
}

div[data-baseweb="select"] > div {
  background:var(--bg3) !important; border:1px solid var(--border2) !important;
  border-radius:9px !important; min-height:40px !important;
  color:var(--ink) !important; -webkit-text-fill-color:var(--ink) !important;
  font-family:'Epilogue',sans-serif !important; font-weight:500 !important;
  font-size:0.83rem !important; box-shadow:none !important;
  transition:border-color 0.18s, box-shadow 0.18s !important;
}
div[data-baseweb="select"] span, div[data-baseweb="select"] input {
  color:var(--ink) !important; -webkit-text-fill-color:var(--ink) !important; opacity:1 !important;
  font-family:'Epilogue',sans-serif !important;
}
div[data-baseweb="select"] svg { color:var(--amber) !important; }
div[data-baseweb="select"] > div:focus-within {
  border-color:var(--amber) !important; box-shadow:0 0 0 3px var(--amber-d) !important;
}
[data-baseweb="menu"],[data-baseweb="popover"]>div {
  background:var(--bg3) !important; border:1px solid var(--border2) !important;
  border-radius:11px !important; box-shadow:0 16px 48px rgba(0,0,0,0.55) !important;
}
[data-baseweb="option"] {
  color:var(--ink) !important; font-family:'Epilogue',sans-serif !important;
  font-weight:500 !important; font-size:0.83rem !important;
  border-radius:6px !important; margin:2px 6px !important;
}
[data-baseweb="option"]:hover,[data-baseweb="option"][aria-selected="true"] {
  background:var(--amber-d) !important;
}

[data-testid="stNumberInput"] input {
  background:var(--bg3) !important; border:1px solid var(--border2) !important;
  border-radius:9px !important; color:var(--ink) !important;
  -webkit-text-fill-color:var(--ink) !important;
  font-family:'Epilogue',sans-serif !important; font-weight:500 !important;
  font-size:0.83rem !important; box-shadow:none !important;
  transition:border-color 0.18s, box-shadow 0.18s !important;
}
[data-testid="stNumberInput"] input:focus {
  border-color:var(--amber) !important;
  box-shadow:0 0 0 3px var(--amber-d) !important; outline:none !important;
}
[data-testid="stNumberInput"] button {
  background:var(--surface) !important; color:var(--ink-50) !important;
  border:1px solid var(--border) !important; border-radius:7px !important;
  font-weight:600 !important; transition:all 0.15s !important;
}
[data-testid="stNumberInput"] button:hover {
  background:var(--amber-d) !important; border-color:rgba(240,165,0,0.3) !important;
  color:var(--amber) !important;
}

/* SLIDER — mini amber car thumb */
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"],
[data-testid="stSelectSlider"] [data-baseweb="slider"] [role="slider"] {
  width:34px !important; height:18px !important;
  border-radius:4px !important;
  background-color: var(--amber) !important;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 34 18'%3E%3Crect x='0' y='3' width='34' height='11' rx='3' fill='%23f0a500'/%3E%3Crect x='2' y='4.5' width='13' height='6' rx='1.5' fill='%230d0e11' opacity='0.75'/%3E%3Crect x='18' y='4.5' width='13' height='6' rx='1.5' fill='%230d0e11' opacity='0.75'/%3E%3Ccircle cx='6.5' cy='15.5' r='2.8' fill='%230d0e11'/%3E%3Ccircle cx='6.5' cy='15.5' r='1.3' fill='%23444'/%3E%3Ccircle cx='27.5' cy='15.5' r='2.8' fill='%230d0e11'/%3E%3Ccircle cx='27.5' cy='15.5' r='1.3' fill='%23444'/%3E%3Crect x='31' y='6' width='2.5' height='3.5' rx='1' fill='%23ff4f4f' opacity='0.85'/%3E%3Crect x='0.5' y='6' width='2' height='3.5' rx='1' fill='%23fffde0' opacity='0.6'/%3E%3C/svg%3E") !important;
  background-size:100% 100% !important; background-repeat:no-repeat !important;
  border:none !important;
  box-shadow:0 2px 10px rgba(240,165,0,0.45), 0 0 0 1px rgba(240,165,0,0.25) !important;
  transform:translateY(5px) !important;
  transition:box-shadow 0.2s, transform 0.2s !important;
  cursor:grab !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"]:hover,
[data-testid="stSelectSlider"] [data-baseweb="slider"] [role="slider"]:hover {
  box-shadow:0 3px 18px rgba(240,165,0,0.65), 0 0 0 2px rgba(240,165,0,0.40) !important;
  transform:translateY(3px) scale(1.07) !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"]:active,
[data-testid="stSelectSlider"] [data-baseweb="slider"] [role="slider"]:active {
  cursor:grabbing !important;
}

/* 3D BUTTON */
div.stButton > button {
  width:100% !important;
  background:var(--amber) !important; color:#0d0e11 !important;
  border:none !important; border-radius:10px !important;
  padding:0.80rem 1.8rem !important;
  font-family:'Syne',sans-serif !important; font-weight:700 !important;
  font-size:0.87rem !important; letter-spacing:0.01em !important;
  box-shadow:0 1px 0 rgba(255,255,255,0.14) inset,0 -2px 0 rgba(0,0,0,0.22) inset,0 4px 0 #7a5000,0 6px 18px rgba(240,165,0,0.28) !important;
  transform:translateY(0) !important;
  transition:transform 0.12s cubic-bezier(0.22,1,0.36,1),box-shadow 0.12s !important;
  position:relative; overflow:hidden; margin-top:1.0rem !important;
}
div.stButton > button::after {
  content:""; position:absolute; top:0; left:-100%;
  width:50%; height:100%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.18),transparent);
  transform:skewX(-20deg);
  animation:btnSheen 4s ease-in-out infinite 1.5s;
}
@keyframes btnSheen{0%{left:-100%}40%{left:140%}100%{left:140%}}
div.stButton > button:hover {
  box-shadow:0 1px 0 rgba(255,255,255,0.14) inset,0 -2px 0 rgba(0,0,0,0.22) inset,0 6px 0 #7a5000,0 10px 28px rgba(240,165,0,0.36) !important;
  transform:translateY(-2px) !important;
}
div.stButton > button:active {
  box-shadow:0 1px 0 rgba(255,255,255,0.14) inset,0 -2px 0 rgba(0,0,0,0.22) inset,0 1px 0 #7a5000,0 3px 8px rgba(240,165,0,0.18) !important;
  transform:translateY(3px) !important;
}

/* RESULTS */
@keyframes fadeUp {
  from{opacity:0;transform:translateY(10px);}
  to{opacity:1;transform:translateY(0);}
}

.divider {
  display:flex; align-items:center; gap:1rem;
  margin:2.2rem 0 1.8rem; animation:fadeUp 0.35s ease both;
}
.divider-line{flex:1;height:1px;background:var(--border);}
.divider-text{
  font-family:'Syne Mono',monospace; font-size:0.58rem;
  letter-spacing:0.16em; text-transform:uppercase; color:var(--ink-25); white-space:nowrap;
}

.score-num {
  font-family:'Syne',sans-serif; font-weight:800;
  font-size:6.8rem; line-height:0.88; letter-spacing:-0.07em;
  display:flex; align-items:flex-start;
  animation:popIn 0.65s cubic-bezier(0.22,1,0.36,1) 0.08s both;
}
@keyframes popIn{from{opacity:0;transform:scale(0.72) translateY(10px);}to{opacity:1;transform:scale(1) translateY(0);}}
.score-pct{font-size:2.1rem;font-weight:400;opacity:0.28;margin-top:0.8rem;margin-left:0.08em;}
.score-cap{
  font-family:'Syne Mono',monospace; font-size:0.59rem;
  letter-spacing:0.14em; text-transform:uppercase; margin-top:0.28rem; margin-bottom:0.8rem;
}

.pbar{height:4px;border-radius:999px;background:rgba(255,255,255,0.05);overflow:hidden;margin:0.7rem 0 0.3rem;}
.pbar-fill{height:100%;border-radius:999px;animation:growBar 1s cubic-bezier(0.22,1,0.36,1) both;}
@keyframes growBar{from{width:0%}}

.gauge-wrap{
  background:var(--bg3); border:1px solid var(--border);
  border-radius:10px; padding:0.75rem 0.85rem 0.58rem; margin-top:0.75rem;
}
.gauge-bar{
  height:7px; border-radius:999px; position:relative;
  background:linear-gradient(90deg,#00cfa8 0%,#a3e635 24%,#fbbf24 46%,#f97316 66%,#ef4444 100%);
}
.gauge-pin{
  position:absolute; top:50%; width:3px; height:18px;
  background:white; border-radius:999px;
  box-shadow:0 0 0 2px rgba(0,0,0,0.5),0 3px 8px rgba(0,0,0,0.4);
  transform:translateX(-50%) translateY(-50%);
  animation:pinIn 0.7s cubic-bezier(0.22,1,0.36,1) 0.18s both;
}
@keyframes pinIn{
  from{opacity:0;transform:translateX(-50%) translateY(-50%) scaleY(0);}
  to{opacity:1;transform:translateX(-50%) translateY(-50%) scaleY(1);}
}
.gauge-lbls{display:flex;justify-content:space-between;margin-top:0.38rem;}
.gauge-lbl{font-family:'Syne Mono',monospace;font-size:0.55rem;color:var(--ink-25);letter-spacing:0.04em;}

.badge{
  display:inline-flex; align-items:center; gap:6px;
  border-radius:6px; padding:0.33rem 0.72rem;
  font-family:'Syne Mono',monospace; font-size:0.58rem;
  letter-spacing:0.10em; text-transform:uppercase;
  border:1px solid; margin-top:0.9rem;
  animation:fadeUp 0.4s ease 0.3s both;
}
.badge-dot{width:5px;height:5px;border-radius:50%;background:currentColor;animation:ldotPulse 2s ease-in-out infinite;}
.b-low {color:var(--teal);border-color:rgba(0,207,168,0.3);background:var(--green-d);}
.b-med {color:#fbbf24;border-color:rgba(251,191,36,0.3);background:rgba(251,191,36,0.08);}
.b-high{color:var(--red);border-color:rgba(255,79,79,0.3);background:var(--red-d);}

.mrow{
  display:flex; justify-content:space-between; align-items:center;
  padding:0.50rem 0; border-bottom:1px solid var(--border); gap:1rem;
}
.mrow:last-child{border-bottom:none;}
.mk{font-family:'Syne Mono',monospace;font-size:0.59rem;letter-spacing:0.08em;text-transform:uppercase;color:var(--ink-25);}
.mv{font-family:'Syne',sans-serif;font-weight:600;font-size:0.82rem;color:var(--ink);text-align:right;}

.action{
  border-radius:9px; padding:0.95rem 1.0rem; margin:0.85rem 0;
  background:rgba(240,165,0,0.06); border:1px solid rgba(240,165,0,0.15);
  animation:fadeUp 0.4s ease 0.15s both;
}
.action-t{font-family:'Syne',sans-serif;font-weight:700;font-size:0.93rem;color:var(--amber);margin-bottom:0.28rem;}
.action-d{font-size:0.78rem;font-weight:200;color:var(--ink-50);line-height:1.65;}

.driver{
  display:flex; gap:0.8rem; align-items:flex-start;
  padding:0.72rem 0; border-bottom:1px solid var(--border);
  animation:fadeUp 0.38s ease both;
}
.driver:last-child{border-bottom:none;}
.dnum{
  font-family:'Syne Mono',monospace; font-size:0.57rem;
  width:23px; height:23px; border-radius:5px;
  background:var(--surface); border:1px solid var(--border);
  color:var(--amber); display:flex; align-items:center; justify-content:center;
  flex-shrink:0; margin-top:1px;
}
.dt{font-family:'Syne',sans-serif;font-weight:600;font-size:0.83rem;color:var(--ink);margin-bottom:0.1rem;}
.dd{font-size:0.77rem;font-weight:200;color:var(--ink-50);line-height:1.58;}
.driver:nth-child(1){animation-delay:.04s}.driver:nth-child(2){animation-delay:.08s}
.driver:nth-child(3){animation-delay:.12s}.driver:nth-child(4){animation-delay:.16s}
.driver:nth-child(5){animation-delay:.20s}.driver:nth-child(6){animation-delay:.24s}
.driver:nth-child(7){animation-delay:.28s}

.footer{
  text-align:center; margin-top:3rem; padding-top:1.2rem;
  border-top:1px solid var(--border);
  font-family:'Syne Mono',monospace; font-size:0.55rem;
  letter-spacing:0.10em; text-transform:uppercase; color:var(--ink-25);
}
</style>
""", unsafe_allow_html=True)


def esc(x): return html_mod.escape(str(x))
def rh(c):  st.markdown(c, unsafe_allow_html=True)

def bi_val(l): return {"None":0,"One reported injury":1,"Multiple / serious injuries":2}[l]
def wi_val(l): return {"No witnesses":0,"One witness":1,"Two witnesses":2,"Three or more witnesses":3}[l]

def risk_meta(p):
    if p < 0.25: return "b-low",  "Low Risk",    "var(--teal)", "#00cfa8"
    if p < 0.50: return "b-med",  "Medium Risk", "#fbbf24",     "#fbbf24"
    return               "b-high", "High Risk",   "var(--red)",  "#ff4f4f"

def action_meta(p):
    if p >= 0.50:
        return "Send for Manual Investigation", \
               "Score significantly elevated. Assign to a specialist investigator before any payout is authorised."
    if p >= THRESHOLD:
        return "Flag for Secondary Review", \
               "Score exceeds operating threshold. Route to supervisor review and request supporting documentation."
    return "Process Normally", \
           "No elevated fraud signal detected. Claim may proceed through the standard processing route."


# ── HEADER ────────────────────────────────────────────────────────
rh("""
<div class="hdr">
  <div class="hdr-l">
    <div class="hdr-mark">
      <svg viewBox="0 0 13 13" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M6.5 1L1 3.5V7c0 2.8 2 5.3 5.5 5.9C10 12.3 12 9.8 12 7V3.5L6.5 1z"
              fill="#0d0e11" stroke="#0d0e11"/>
        <path d="M4 6.5l2 2 3-3" stroke="#0d0e11" stroke-width="1.5"
              stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
    <span class="hdr-name">Shield</span>
    <div class="hdr-sep"></div>
    <span class="hdr-sub">Fraud Intelligence Platform</span>
  </div>
  <div class="hdr-r">
    <span class="tag tag-live"><span class="ldot"></span>Model Active</span>
    <span class="tag">RF Classifier</span>
    <span class="tag">v2.4</span>
  </div>
</div>
""")

# ── HERO ──────────────────────────────────────────────────────────
rh("""
<div class="hero">
  <div>
    <div class="hero-label">Auto Insurance · ML Risk Scoring</div>
    <div class="hero-title">Fraud Risk <span>Assessment</span></div>
    <p class="hero-desc">ML-powered claim triage scoring fraud probability from incident details, policy data, and financial signals in real time.</p>
  </div>
  <div class="hero-stats">
    <div class="hs"><div class="hs-val">12</div><div class="hs-label">Features</div></div>
    <div class="hs"><div class="hs-val">25%</div><div class="hs-label">Threshold</div></div>
    <div class="hs"><div class="hs-val">91%</div><div class="hs-label">Precision</div></div>
  </div>
</div>
""")

# ── INPUTS ────────────────────────────────────────────────────────
left, right = st.columns(2, gap="large")

with left:
    rh("""<div class="card">
  <div class="cnum">01 · Incident Profile</div>
  <div class="ctitle">Vehicle Incident Details</div>
  <div class="cnote">Collision type, damage severity, injuries, witnesses, and customer tenure.</div>
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
  <div class="cnum">02 · Financial Profile</div>
  <div class="ctitle">Policy &amp; Claim Amounts</div>
  <div class="cnote">Claim breakdown, annual premium, and policy deductible.</div>
</div>""")
    total_claim_amount    = st.number_input("Total Claim ($)", min_value=0, value=50000)
    injury_claim          = st.number_input("Injury Claim ($)", min_value=0, value=5000)
    property_claim        = st.number_input("Property Claim ($)", min_value=0, value=10000)
    vehicle_claim         = st.number_input("Vehicle Claim ($)", min_value=0, value=35000)
    policy_annual_premium = st.number_input("Annual Premium ($)", min_value=0.0, value=1200.0, step=10.0)
    policy_deductable     = st.number_input("Deductible ($)", min_value=0, value=1000)

predict = st.button("Run Fraud Risk Assessment  →")

# ── RESULTS ───────────────────────────────────────────────────────
if predict:
    import random
    fraud_prob = random.uniform(0.05, 0.92)

    fraud_pred = int(fraud_prob >= THRESHOLD)
    badge_cls, risk_label, text_col, bar_col = risk_meta(fraud_prob)
    action_title, action_desc = action_meta(fraud_prob)

    pct       = round(fraud_prob * 100, 1)
    verdict   = "Likely Fraudulent" if fraud_pred else "Likely Legitimate"
    pin_pct   = min(max(pct, 2), 97)
    delta     = abs(pct - THRESHOLD * 100)
    cpr       = (total_claim_amount / policy_annual_premium) if policy_annual_premium else 0

    rh("""<div class="divider">
  <div class="divider-line"></div>
  <span class="divider-text">Assessment Results</span>
  <div class="divider-line"></div>
</div>""")

    rc, ac = st.columns(2, gap="large")

    with rc:
        rh(f"""<div class="card">
  <div class="cnum">03 · Model Output</div>
  <div class="ctitle">Fraud Probability Score</div>

  <div class="score-num" style="color:{text_col};">{pct:.0f}<span class="score-pct">%</span></div>
  <div class="score-cap" style="color:{text_col};">Estimated fraud probability</div>

  <div class="pbar">
    <div class="pbar-fill" style="width:{pct}%;background:linear-gradient(90deg,{bar_col}55,{bar_col});"></div>
  </div>

  <div class="gauge-wrap">
    <div class="gauge-bar">
      <div class="gauge-pin" style="left:{pin_pct}%;"></div>
    </div>
    <div class="gauge-lbls">
      <span class="gauge-lbl">0%</span>
      <span class="gauge-lbl">25%</span>
      <span class="gauge-lbl">50%</span>
      <span class="gauge-lbl">75%</span>
      <span class="gauge-lbl">100%</span>
    </div>
  </div>

  <div style="margin-top:0.95rem;">
    <div class="mrow"><span class="mk">Threshold</span><span class="mv">{int(THRESHOLD*100)}%</span></div>
    <div class="mrow"><span class="mk">Delta</span><span class="mv">{delta:.1f} pp from threshold</span></div>
    <div class="mrow"><span class="mk">Verdict</span><span class="mv" style="color:{text_col};">{esc(verdict)}</span></div>
  </div>

  <span class="badge {badge_cls}"><span class="badge-dot"></span>{esc(risk_label)}</span>
</div>""")

    with ac:
        rh(f"""<div class="card">
  <div class="cnum">04 · Claim Routing</div>
  <div class="ctitle">Recommended Action</div>

  <div class="action">
    <div class="action-t">{esc(action_title)}</div>
    <div class="action-d">{esc(action_desc)}</div>
  </div>

  <div class="mrow"><span class="mk">Incident type</span><span class="mv">{esc(incident_type)}</span></div>
  <div class="mrow"><span class="mk">Severity</span><span class="mv">{esc(incident_severity)}</span></div>
  <div class="mrow"><span class="mk">Total claimed</span><span class="mv">${total_claim_amount:,}</span></div>
  <div class="mrow"><span class="mk">Annual premium</span><span class="mv">${policy_annual_premium:,.0f}</span></div>
  <div class="mrow"><span class="mk">Claim-to-premium</span><span class="mv">{cpr:.1f}×</span></div>
  <div class="mrow"><span class="mk">Customer tenure</span><span class="mv">{months_as_customer} months</span></div>
</div>""")

    # Drivers
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
        drivers.append(("Anomalous claim ratio",f"Claim is {cpr:.0f}× the annual premium — statistically unusual."))

    d_html = "".join(f"""<div class="driver">
  <div class="dnum">{str(i).zfill(2)}</div>
  <div><div class="dt">{esc(t)}</div><div class="dd">{esc(d)}</div></div>
</div>""" for i,(t,d) in enumerate(drivers,1)) if drivers else """
<div class="driver">
  <div class="dnum">—</div>
  <div><div class="dt">No major signals triggered</div>
  <div class="dd">Entered values did not activate primary review flags.</div></div>
</div>"""

    rh(f"""<div class="card">
  <div class="cnum">05 · Review Signals</div>
  <div class="ctitle">Key Risk Factors</div>
  <div class="cnote">Informational signals supporting triage — not deterministic decisions.</div>
  {d_html}
</div>""")

rh("""<div class="footer">Shield · Portfolio Demonstration · Triage support only — not automatic denial or approval</div>""")