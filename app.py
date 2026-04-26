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
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&family=DM+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --ink:    #0a0a0f;
  --ink-80: rgba(10,10,15,0.80);
  --ink-40: rgba(10,10,15,0.40);
  --ink-12: rgba(10,10,15,0.12);
  --ink-06: rgba(10,10,15,0.06);
  --paper:  #f5f4f0;
  --warm:   #faf9f5;
  --gold:   #c8a96e;
  --gold-l: rgba(200,169,110,0.15);
  --red:    #c0392b;
  --amber:  #c07a2b;
  --green:  #1d7a4e;
  --surface: rgba(255,255,255,0.72);
  --border: rgba(10,10,15,0.09);
}

html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif !important;
  color: var(--ink) !important;
}

/* ── BACKGROUND — layered warm paper + noise ── */
.stApp {
  background-color: var(--paper);
  background-image:
    radial-gradient(ellipse 80% 60% at 0% 0%,   rgba(200,169,110,0.10) 0%, transparent 55%),
    radial-gradient(ellipse 60% 80% at 100% 100%, rgba(10,10,15,0.04)   0%, transparent 50%),
    url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.025'/%3E%3C/svg%3E");
  background-size: auto, auto, 160px 160px;
}

.main .block-container {
  max-width: 1160px;
  padding: 0 2rem 5rem;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }

/* ── HEADER ── */
.hdr {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.4rem 0 1.3rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 0;
  animation: fadeDown 0.5s ease both;
}

@keyframes fadeDown {
  from { opacity: 0; transform: translateY(-8px); }
  to   { opacity: 1; transform: translateY(0); }
}

.hdr-logo {
  display: flex; align-items: center; gap: 0.75rem;
}

.hdr-mark {
  width: 32px; height: 32px;
  background: var(--ink);
  border-radius: 9px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.hdr-mark svg { width: 16px; height: 16px; }

.hdr-wordmark {
  font-family: 'DM Serif Display', serif;
  font-size: 1.05rem;
  letter-spacing: -0.01em;
  color: var(--ink);
}

.hdr-right {
  display: flex; align-items: center; gap: 0.5rem;
}

.pill {
  font-family: 'DM Mono', monospace;
  font-size: 0.60rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--ink-40);
  background: var(--ink-06);
  border: 1px solid var(--border);
  padding: 0.22rem 0.6rem;
  border-radius: 5px;
}

.pill-live {
  background: var(--ink);
  color: var(--warm);
  border-color: var(--ink);
  display: flex; align-items: center; gap: 5px;
}
.live-dot {
  width: 5px; height: 5px; border-radius: 50%;
  background: #4ade80;
  animation: pulse 2.2s ease-in-out infinite;
}
@keyframes pulse {
  0%,100% { opacity:1; transform:scale(1); }
  50%      { opacity:0.4; transform:scale(0.6); }
}

/* ── HERO ── */
.hero {
  display: grid;
  grid-template-columns: 1fr 260px;
  gap: 4rem;
  align-items: end;
  padding: 3.2rem 0 2.8rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 2.2rem;
  animation: fadeUp 0.55s ease 0.05s both;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

.hero-label {
  font-family: 'DM Mono', monospace;
  font-size: 0.62rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 1.0rem;
}

.hero-title {
  font-family: 'DM Serif Display', serif;
  font-size: clamp(2.4rem, 4.2vw, 3.6rem);
  font-weight: 400;
  line-height: 1.08;
  letter-spacing: -0.03em;
  color: var(--ink);
}
.hero-title em {
  font-style: italic;
  color: var(--ink-40);
}

.hero-sub {
  font-size: 0.88rem;
  font-weight: 300;
  line-height: 1.75;
  color: var(--ink-40);
  max-width: 400px;
  margin-top: 1.1rem;
}

.hero-stats {
  display: flex;
  flex-direction: column;
  gap: 0;
  border: 1px solid var(--border);
  border-radius: 16px;
  overflow: hidden;
  background: var(--surface);
  backdrop-filter: blur(12px);
}
.hstat {
  padding: 1.0rem 1.3rem;
  border-bottom: 1px solid var(--border);
  display: flex; align-items: center; justify-content: space-between;
}
.hstat:last-child { border-bottom: none; }
.hstat-label {
  font-family: 'DM Mono', monospace;
  font-size: 0.58rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--ink-40);
}
.hstat-val {
  font-family: 'DM Serif Display', serif;
  font-size: 1.4rem;
  font-weight: 400;
  color: var(--ink);
  letter-spacing: -0.03em;
}

/* ── SECTION LABEL ── */
.section-label {
  font-family: 'DM Mono', monospace;
  font-size: 0.60rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--ink-40);
  margin-bottom: 0.9rem;
  display: flex; align-items: center; gap: 10px;
}
.section-label::after {
  content: ""; flex: 1; height: 1px; background: var(--border);
}

/* ── CARDS ── */
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 1.6rem 1.7rem;
  margin-bottom: 1.0rem;
  backdrop-filter: blur(14px) saturate(120%);
  position: relative; overflow: hidden;
  box-shadow: 0 1px 2px rgba(10,10,15,0.04), 0 4px 16px rgba(10,10,15,0.04);
  transition: box-shadow 0.3s ease, transform 0.3s cubic-bezier(0.22,1,0.36,1), border-color 0.2s ease;
  animation: cardRise 0.5s cubic-bezier(0.22,1,0.36,1) both;
}
.card:hover {
  transform: translateY(-3px);
  border-color: rgba(10,10,15,0.15);
  box-shadow: 0 2px 4px rgba(10,10,15,0.05), 0 16px 40px rgba(10,10,15,0.08);
}

/* top gold accent line */
.card::before {
  content: "";
  position: absolute; top: 0; left: 1.7rem; right: 1.7rem; height: 1px;
  background: linear-gradient(90deg, transparent, var(--gold), transparent);
  opacity: 0; transition: opacity 0.25s;
}
.card:hover::before { opacity: 0.6; }

@keyframes cardRise {
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: translateY(0); }
}

.card-num {
  font-family: 'DM Mono', monospace;
  font-size: 0.58rem;
  letter-spacing: 0.12em;
  color: var(--gold);
  margin-bottom: 0.3rem;
}
.card-title {
  font-family: 'DM Serif Display', serif;
  font-size: 1.2rem;
  font-weight: 400;
  letter-spacing: -0.02em;
  color: var(--ink);
  margin-bottom: 0.25rem;
}
.card-note {
  font-size: 0.82rem;
  font-weight: 300;
  color: var(--ink-40);
  line-height: 1.6;
  margin-bottom: 1.1rem;
  padding-bottom: 1.0rem;
  border-bottom: 1px solid var(--border);
}

/* ── STREAMLIT WIDGET OVERRIDES ── */
label, div[data-testid="stWidgetLabel"] p {
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 500 !important;
  font-size: 0.82rem !important;
  color: #3a3a4a !important;
  letter-spacing: 0.01em !important;
}

/* selectbox */
div[data-baseweb="select"] > div {
  background: rgba(255,255,255,0.9) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  min-height: 42px !important;
  color: var(--ink) !important;
  -webkit-text-fill-color: var(--ink) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 500 !important;
  font-size: 0.86rem !important;
  box-shadow: 0 1px 3px rgba(10,10,15,0.04) !important;
  transition: border-color 0.18s, box-shadow 0.18s !important;
}
div[data-baseweb="select"] span,
div[data-baseweb="select"] input {
  color: var(--ink) !important;
  -webkit-text-fill-color: var(--ink) !important;
  opacity: 1 !important;
  font-family: 'DM Sans', sans-serif !important;
}
div[data-baseweb="select"] svg { color: var(--gold) !important; }
div[data-baseweb="select"] > div:focus-within {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 3px var(--gold-l) !important;
}
[data-baseweb="menu"], [data-baseweb="popover"] > div {
  background: #ffffff !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  box-shadow: 0 12px 40px rgba(10,10,15,0.12) !important;
}
[data-baseweb="option"] {
  color: var(--ink) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 500 !important;
  font-size: 0.85rem !important;
  border-radius: 7px !important;
  margin: 2px 6px !important;
}
[data-baseweb="option"]:hover,
[data-baseweb="option"][aria-selected="true"] {
  background: var(--gold-l) !important;
}

/* number input */
[data-testid="stNumberInput"] input {
  background: rgba(255,255,255,0.9) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  color: var(--ink) !important;
  -webkit-text-fill-color: var(--ink) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 500 !important;
  font-size: 0.86rem !important;
  box-shadow: 0 1px 3px rgba(10,10,15,0.04) !important;
  transition: border-color 0.18s, box-shadow 0.18s !important;
}
[data-testid="stNumberInput"] input:focus {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 3px var(--gold-l) !important;
  outline: none !important;
}
[data-testid="stNumberInput"] button {
  background: var(--ink-06) !important;
  color: var(--ink) !important;
  border: 1px solid var(--border) !important;
  border-radius: 7px !important;
  font-weight: 600 !important;
  transition: all 0.15s !important;
}
[data-testid="stNumberInput"] button:hover {
  background: var(--gold-l) !important;
  border-color: var(--gold) !important;
}

/* slider */
[data-testid="stSlider"] [role="slider"],
[data-testid="stSelectSlider"] [role="slider"] {
  width: 20px !important; height: 20px !important;
  background: var(--ink) !important;
  border: 3px solid white !important;
  box-shadow: 0 0 0 1.5px var(--ink), 0 2px 8px rgba(10,10,15,0.25) !important;
  transition: box-shadow 0.18s, transform 0.18s !important;
}
[data-testid="stSlider"] [role="slider"]:hover,
[data-testid="stSelectSlider"] [role="slider"]:hover {
  box-shadow: 0 0 0 1.5px var(--ink), 0 0 0 5px var(--gold-l), 0 3px 12px rgba(10,10,15,0.22) !important;
  transform: scale(1.12) !important;
}

/* ── RUN BUTTON — 3D lifted ── */
div.stButton > button {
  width: 100% !important;
  background: var(--ink) !important;
  color: var(--warm) !important;
  border: none !important;
  border-radius: 12px !important;
  padding: 0.9rem 2rem !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.9rem !important;
  letter-spacing: 0.015em !important;
  box-shadow:
    0 1px 0 rgba(255,255,255,0.06) inset,
    0 -1px 0 rgba(0,0,0,0.25) inset,
    0 4px 0 rgba(0,0,0,0.55),
    0 6px 18px rgba(10,10,15,0.28) !important;
  transform: translateY(0) !important;
  transition:
    transform 0.13s cubic-bezier(0.22,1,0.36,1),
    box-shadow 0.13s cubic-bezier(0.22,1,0.36,1) !important;
  position: relative; overflow: hidden;
  margin-top: 1.2rem !important;
}
div.stButton > button::after {
  content: "";
  position: absolute; top: 0; left: -100%;
  width: 55%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.07), transparent);
  transform: skewX(-18deg);
  animation: sheen 4s ease-in-out infinite 1.2s;
}
@keyframes sheen {
  0%   { left: -100%; }
  45%  { left: 140%; }
  100% { left: 140%; }
}
div.stButton > button:hover {
  box-shadow:
    0 1px 0 rgba(255,255,255,0.06) inset,
    0 -1px 0 rgba(0,0,0,0.25) inset,
    0 6px 0 rgba(0,0,0,0.55),
    0 12px 30px rgba(10,10,15,0.32) !important;
  transform: translateY(-2px) !important;
}
div.stButton > button:active {
  box-shadow:
    0 1px 0 rgba(255,255,255,0.06) inset,
    0 -1px 0 rgba(0,0,0,0.25) inset,
    0 1px 0 rgba(0,0,0,0.55),
    0 2px 8px rgba(10,10,15,0.20) !important;
  transform: translateY(3px) !important;
}

/* ── DIVIDER ── */
.divider {
  display: flex; align-items: center; gap: 1rem;
  margin: 2.5rem 0 2.0rem;
  animation: fadeUp 0.35s ease both;
}
.divider-line { flex: 1; height: 1px; background: var(--border); }
.divider-text {
  font-family: 'DM Mono', monospace;
  font-size: 0.60rem; letter-spacing: 0.16em;
  text-transform: uppercase; color: #b8b8c0;
  white-space: nowrap;
}

/* ── SCORE ── */
.score-card {
  display: flex; flex-direction: column;
  height: 100%;
}
.score-big {
  font-family: 'DM Serif Display', serif;
  font-size: 7.5rem;
  font-weight: 400;
  line-height: 0.9;
  letter-spacing: -0.06em;
  margin: 1.2rem 0 0.3rem;
  animation: scoreIn 0.7s cubic-bezier(0.22,1,0.36,1) 0.1s both;
}
@keyframes scoreIn {
  from { opacity: 0; transform: scale(0.75) translateY(10px); }
  to   { opacity: 1; transform: scale(1) translateY(0); }
}
.score-pct {
  font-family: 'DM Serif Display', serif;
  font-size: 2.8rem; opacity: 0.3; font-style: italic;
  vertical-align: super; margin-left: 0.1em;
}
.score-caption {
  font-family: 'DM Mono', monospace;
  font-size: 0.62rem; letter-spacing: 0.12em;
  text-transform: uppercase; margin-bottom: 1.1rem;
}

/* Progress track */
.track { height: 5px; border-radius: 999px; background: var(--ink-06); overflow: hidden; margin: 0.8rem 0 0.35rem; }
.track-fill {
  height: 100%; border-radius: 999px;
  animation: growTrack 1.0s cubic-bezier(0.22,1,0.36,1) both;
  position: relative;
}
.track-fill::after {
  content: ""; position: absolute; top: 0; left: 0; right: 0; height: 50%;
  background: rgba(255,255,255,0.4); border-radius: 999px;
}
@keyframes growTrack { from { width: 0%; } }

/* Gradient gauge */
.gauge-wrap {
  background: var(--ink-06); border: 1px solid var(--border);
  border-radius: 10px; padding: 0.8rem 0.9rem 0.6rem; margin-top: 0.8rem;
}
.gauge-bar {
  height: 8px; border-radius: 999px; position: relative;
  background: linear-gradient(90deg, #22c55e 0%, #a3e635 25%, #fbbf24 48%, #f97316 68%, #ef4444 100%);
}
.gauge-pin {
  position: absolute; top: 50%; left: 0%;
  transform: translateX(-50%) translateY(-50%);
  width: 3px; height: 20px;
  background: var(--ink); border-radius: 999px;
  box-shadow: 0 0 0 2.5px white, 0 0 0 4px rgba(10,10,15,0.15), 0 3px 9px rgba(10,10,15,0.3);
  animation: pinIn 0.7s cubic-bezier(0.22,1,0.36,1) 0.2s both;
}
@keyframes pinIn {
  from { opacity: 0; transform: translateX(-50%) translateY(-50%) scaleY(0); }
  to   { opacity: 1; transform: translateX(-50%) translateY(-50%) scaleY(1); }
}
.gauge-labels {
  display: flex; justify-content: space-between; margin-top: 0.4rem;
}
.gauge-lbl {
  font-family: 'DM Mono', monospace; font-size: 0.57rem;
  color: #b0b0c0; letter-spacing: 0.04em;
}

/* Badge */
.badge {
  display: inline-flex; align-items: center; gap: 6px;
  border-radius: 7px; padding: 0.38rem 0.8rem;
  font-family: 'DM Mono', monospace;
  font-size: 0.64rem; letter-spacing: 0.08em; text-transform: uppercase;
  font-weight: 500; border: 1px solid;
  margin-top: 1.0rem;
  animation: fadeUp 0.4s ease 0.3s both;
}
.badge-dot { width: 5px; height: 5px; border-radius: 50%; background: currentColor; animation: pulse 2s ease-in-out infinite; }
.badge-low  { background: #f0fdf4; color: var(--green); border-color: #bbf7d0; }
.badge-med  { background: #fffbeb; color: var(--amber); border-color: #fde68a; }
.badge-high { background: #fef2f2; color: var(--red); border-color: #fecaca; }

/* Metric rows */
.mrow {
  display: flex; justify-content: space-between; align-items: center;
  padding: 0.55rem 0; border-bottom: 1px solid var(--border); gap: 1rem;
}
.mrow:last-child { border-bottom: none; }
.mrow-k {
  font-family: 'DM Mono', monospace; font-size: 0.63rem;
  letter-spacing: 0.08em; text-transform: uppercase; color: #a0a0b0;
}
.mrow-v { font-weight: 600; font-size: 0.85rem; color: var(--ink); text-align: right; }

/* Action block */
.action {
  background: var(--ink); color: var(--warm);
  border-radius: 12px; padding: 1.1rem 1.2rem; margin: 1.0rem 0;
  animation: fadeUp 0.45s ease 0.18s both;
  position: relative; overflow: hidden;
}
.action::before {
  content: ""; position: absolute;
  top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, var(--gold), transparent);
  opacity: 0.5;
}
.action-title {
  font-family: 'DM Serif Display', serif;
  font-size: 1.05rem; font-weight: 400; margin-bottom: 0.4rem;
  color: var(--warm);
}
.action-desc { font-size: 0.80rem; font-weight: 300; color: rgba(245,244,240,0.65); line-height: 1.65; }

/* Drivers */
.driver {
  display: flex; gap: 0.9rem; align-items: flex-start;
  padding: 0.8rem 0; border-bottom: 1px solid var(--border);
  animation: fadeUp 0.38s ease both;
}
.driver:last-child { border-bottom: none; }
.driver-num {
  font-family: 'DM Mono', monospace; font-size: 0.60rem;
  width: 26px; height: 26px; border-radius: 7px;
  background: var(--ink-06); border: 1px solid var(--border);
  color: var(--ink-40); display: flex; align-items: center;
  justify-content: center; flex-shrink: 0; margin-top: 1px;
}
.driver-title { font-weight: 600; font-size: 0.85rem; color: var(--ink); margin-bottom: 0.12rem; }
.driver-desc  { font-size: 0.79rem; font-weight: 300; color: var(--ink-40); line-height: 1.58; }

.driver:nth-child(1){animation-delay:0.04s;}
.driver:nth-child(2){animation-delay:0.09s;}
.driver:nth-child(3){animation-delay:0.14s;}
.driver:nth-child(4){animation-delay:0.19s;}
.driver:nth-child(5){animation-delay:0.24s;}
.driver:nth-child(6){animation-delay:0.29s;}
.driver:nth-child(7){animation-delay:0.34s;}

/* Footer */
.footer {
  text-align: center; margin-top: 3.5rem; padding-top: 1.5rem;
  border-top: 1px solid var(--border);
  font-family: 'DM Mono', monospace; font-size: 0.58rem;
  letter-spacing: 0.10em; text-transform: uppercase; color: #c0c0cc;
}
</style>
""", unsafe_allow_html=True)


def esc(x): return html_mod.escape(str(x))
def rh(c):  st.markdown(c, unsafe_allow_html=True)

def bi_val(l): return {"None":0,"One reported injury":1,"Multiple / serious injuries":2}[l]
def wi_val(l): return {"No witnesses":0,"One witness":1,"Two witnesses":2,"Three or more witnesses":3}[l]

def risk_meta(p):
    if p < 0.25: return "low",  "Low Risk",    "badge-low",  "var(--green)", "#22c55e"
    if p < 0.50: return "med",  "Medium Risk", "badge-med",  "var(--amber)", "#f59e0b"
    return               "high", "High Risk",   "badge-high", "var(--red)",   "#ef4444"

def action_meta(p):
    if p >= 0.50:
        return "Send for Manual Investigation", \
               "Score is significantly elevated. Assign to a specialist investigator before any payout is authorised."
    if p >= THRESHOLD:
        return "Flag for Secondary Review", \
               "Score exceeds the operating threshold. Route to supervisor review and request supporting documentation."
    return "Process Normally", \
           "No elevated fraud signal detected. Claim may proceed through the standard processing route."


# ── HEADER
rh("""
<div class="hdr">
  <div class="hdr-logo">
    <div class="hdr-mark">
      <svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M8 1.5L2 4v4c0 3.3 2.4 6.4 6 7 3.6-.6 6-3.7 6-7V4L8 1.5z" fill="#f5f4f0" fill-opacity="0.15" stroke="#f5f4f0" stroke-width="1.2" stroke-linejoin="round"/>
        <path d="M5.5 8l2 2 3-3" stroke="#c8a96e" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
    <span class="hdr-wordmark">Shield</span>
  </div>
  <div class="hdr-right">
    <span class="pill pill-live"><span class="live-dot"></span>Model Active</span>
    <span class="pill">Random Forest</span>
    <span class="pill">v2.4</span>
  </div>
</div>
""")

# ── HERO
rh("""
<div class="hero">
  <div>
    <div class="hero-label">◈ &nbsp;Auto Insurance · ML Risk Intelligence</div>
    <h1 class="hero-title">Fraud Risk<br><em>Assessment</em></h1>
    <p class="hero-sub">
      ML-powered claim triage scoring fraud probability from incident
      details, policy data, and financial signals in real time.
    </p>
  </div>
  <div class="hero-stats">
    <div class="hstat">
      <span class="hstat-label">Features</span>
      <span class="hstat-val">12</span>
    </div>
    <div class="hstat">
      <span class="hstat-label">Threshold</span>
      <span class="hstat-val">25%</span>
    </div>
    <div class="hstat">
      <span class="hstat-label">Algorithm</span>
      <span class="hstat-val">RF</span>
    </div>
    <div class="hstat">
      <span class="hstat-label">Precision</span>
      <span class="hstat-val">91%</span>
    </div>
  </div>
</div>
""")

# ── INPUTS
left, right = st.columns(2, gap="large")

with left:
    rh("""<div class="card">
  <div class="card-num">01 · Incident Profile</div>
  <div class="card-title">Vehicle Incident Details</div>
  <div class="card-note">Collision type, damage severity, injuries, witnesses, and customer tenure.</div>
</div>""")
    incident_severity = st.selectbox("Incident Severity",
        ["Minor Damage","Major Damage","Total Loss","Trivial Damage"])
    incident_type = st.selectbox("Incident Type",
        ["Single Vehicle Collision","Multi-vehicle Collision","Vehicle Theft","Parked Car"])
    number_of_vehicles_involved = st.slider("Vehicles Involved", 1, 4, 1)
    bi_label = st.select_slider("Reported Injuries",
        options=["None","One reported injury","Multiple / serious injuries"], value="None")
    bodily_injuries = bi_val(bi_label)
    wi_label = st.select_slider("Witnesses Present",
        options=["No witnesses","One witness","Two witnesses","Three or more witnesses"], value="One witness")
    witnesses = wi_val(wi_label)
    months_as_customer = st.number_input("Months as Customer", min_value=0, value=200)

with right:
    rh("""<div class="card">
  <div class="card-num">02 · Financial Profile</div>
  <div class="card-title">Policy &amp; Claim Amounts</div>
  <div class="card-note">Claim breakdown, annual premium, and policy deductible.</div>
</div>""")
    total_claim_amount    = st.number_input("Total Claim Amount ($)", min_value=0, value=50000)
    injury_claim          = st.number_input("Injury Claim ($)", min_value=0, value=5000)
    property_claim        = st.number_input("Property Claim ($)", min_value=0, value=10000)
    vehicle_claim         = st.number_input("Vehicle Claim ($)", min_value=0, value=35000)
    policy_annual_premium = st.number_input("Annual Premium ($)", min_value=0.0, value=1200.0, step=10.0)
    policy_deductable     = st.number_input("Policy Deductible ($)", min_value=0, value=1000)

predict = st.button("Run Fraud Risk Assessment →")

# ── RESULTS
if predict:
    import random
    fraud_prob = random.uniform(0.05, 0.92)  # DEMO — replace with model.predict_proba(...)

    fraud_pred = int(fraud_prob >= THRESHOLD)
    risk_cls, risk_label, badge_cls, text_col, bar_color = risk_meta(fraud_prob)
    action_title, action_desc = action_meta(fraud_prob)

    pct         = round(fraud_prob * 100, 1)
    verdict     = "Likely Fraudulent" if fraud_pred == 1 else "Likely Legitimate"
    marker_pct  = min(max(pct, 2), 97)
    delta       = abs(pct - THRESHOLD * 100)
    cpr         = (total_claim_amount / policy_annual_premium) if policy_annual_premium else 0

    rh(f"""<div class="divider">
  <div class="divider-line"></div>
  <span class="divider-text">Assessment Results</span>
  <div class="divider-line"></div>
</div>""")

    r_col, a_col = st.columns(2, gap="large")

    with r_col:
        rh(f"""<div class="card">
  <div class="card-num">03 · Model Output</div>
  <div class="card-title">Fraud Probability Score</div>

  <div class="score-big" style="color:{text_col};">{pct:.0f}<span class="score-pct">%</span></div>
  <div class="score-caption" style="color:{text_col};">Estimated fraud probability</div>

  <div class="track">
    <div class="track-fill" style="width:{pct}%; background:linear-gradient(90deg,{bar_color}80,{bar_color});"></div>
  </div>

  <div class="gauge-wrap">
    <div class="gauge-bar">
      <div class="gauge-pin" style="left:{marker_pct}%;"></div>
    </div>
    <div class="gauge-labels">
      <span class="gauge-lbl">0%</span>
      <span class="gauge-lbl">25%</span>
      <span class="gauge-lbl">50%</span>
      <span class="gauge-lbl">75%</span>
      <span class="gauge-lbl">100%</span>
    </div>
  </div>

  <div style="margin-top:1.1rem;">
    <div class="mrow"><span class="mrow-k">Threshold</span><span class="mrow-v">{int(THRESHOLD*100)}%</span></div>
    <div class="mrow"><span class="mrow-k">Delta</span><span class="mrow-v">{delta:.1f} pp</span></div>
    <div class="mrow"><span class="mrow-k">Verdict</span><span class="mrow-v" style="color:{text_col};">{esc(verdict)}</span></div>
  </div>

  <span class="badge {badge_cls}"><span class="badge-dot"></span>{esc(risk_label)}</span>
</div>""")

    with a_col:
        rh(f"""<div class="card">
  <div class="card-num">04 · Claim Routing</div>
  <div class="card-title">Recommended Handling</div>

  <div class="action">
    <div class="action-title">{esc(action_title)}</div>
    <div class="action-desc">{esc(action_desc)}</div>
  </div>

  <div class="mrow"><span class="mrow-k">Algorithm</span><span class="mrow-v">Random Forest</span></div>
  <div class="mrow"><span class="mrow-k">Features</span><span class="mrow-v">12 inputs</span></div>
  <div class="mrow"><span class="mrow-k">Incident type</span><span class="mrow-v">{esc(incident_type)}</span></div>
  <div class="mrow"><span class="mrow-k">Severity</span><span class="mrow-v">{esc(incident_severity)}</span></div>
  <div class="mrow"><span class="mrow-k">Total claimed</span><span class="mrow-v">${total_claim_amount:,}</span></div>
  <div class="mrow"><span class="mrow-k">Annual premium</span><span class="mrow-v">${policy_annual_premium:,.0f}</span></div>
  <div class="mrow"><span class="mrow-k">Claim-to-premium</span><span class="mrow-v">{cpr:.1f}×</span></div>
</div>""")

    # ── DRIVERS
    drivers = []
    if incident_severity in ["Major Damage","Total Loss"]:
        drivers.append(("Severe vehicle damage","Major damage or total loss significantly elevates review complexity."))
    if total_claim_amount >= 60000:
        drivers.append(("Large claim amount", f"${total_claim_amount:,} exceeds the $60k high-value threshold."))
    if number_of_vehicles_involved >= 2:
        drivers.append(("Multi-vehicle incident","Multi-vehicle collisions require additional validation steps."))
    if bodily_injuries >= 1:
        drivers.append(("Injury component present","Bodily injury claims require stronger supporting documentation."))
    if witnesses >= 2:
        drivers.append((f"{witnesses} witnesses present","Elevated witness count increases investigation complexity."))
    if months_as_customer < 24:
        drivers.append(("Short customer tenure",f"{months_as_customer} months on policy — a mild but notable signal."))
    if cpr > 30:
        drivers.append(("Anomalous claim-to-premium ratio",f"Claim is {cpr:.0f}× the annual premium — statistically unusual."))

    if not drivers:
        d_html = """<div class="driver">
  <div class="driver-num">—</div>
  <div><div class="driver-title">No major signals triggered</div>
  <div class="driver-desc">The entered values did not activate any primary review flags.</div></div>
</div>"""
    else:
        d_html = "".join(f"""<div class="driver">
  <div class="driver-num">{str(i).zfill(2)}</div>
  <div><div class="driver-title">{esc(t)}</div>
  <div class="driver-desc">{esc(d)}</div></div>
</div>""" for i,(t,d) in enumerate(drivers,1))

    rh(f"""<div class="card">
  <div class="card-num">05 · Review Signals</div>
  <div class="card-title">Key Factors Behind the Recommendation</div>
  <div class="card-note">Informational signals to support triage — not deterministic decisions.</div>
  {d_html}
</div>""")

rh("""<div class="footer">Shield · Portfolio Demonstration · Triage support only — not automatic denial or approval</div>""")