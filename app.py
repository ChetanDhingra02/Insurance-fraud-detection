import streamlit as st
import html as html_mod

THRESHOLD = 0.25

st.set_page_config(
    page_title="Shield · Fraud Detection",
    page_icon="🛡",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Outfit:wght@300;400;500;600;700&family=Geist+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
    color: #111118 !important;
}

/* ── PAGE BACKGROUND — soft warm mesh ─────────────── */
.stApp {
    background-color: #fafaf8;
    background-image:
        radial-gradient(ellipse 60% 50% at 20% 0%,   rgba(234,179,8,0.09)  0%, transparent 55%),
        radial-gradient(ellipse 50% 40% at 85% 15%,  rgba(16,185,129,0.07) 0%, transparent 50%),
        radial-gradient(ellipse 40% 60% at 60% 95%,  rgba(239,68,68,0.05)  0%, transparent 50%);
}

.main .block-container {
    max-width: 1200px;
    padding: 0 2.2rem 6rem;
}
[data-testid="stHeader"] { background: transparent !important; }

/* ── TIRE SCROLLBAR — elegant version ─────────────── */
::-webkit-scrollbar { width: 10px; }
::-webkit-scrollbar-track { background: #f0f0ec; }
::-webkit-scrollbar-thumb {
    background: #111118;
    border-radius: 999px;
    border: 2px solid #f0f0ec;
    background-image: radial-gradient(
        circle at 50% 50%,
        #fafaf8 0% 18%,
        #111118 19% 36%,
        #3f3f52 37% 52%,
        #111118 53% 70%,
        #fafaf8 71% 100%
    );
    background-clip: padding-box;
}
::-webkit-scrollbar-thumb:hover {
    background-image: radial-gradient(
        circle at 50% 50%,
        #fafaf8 0% 18%,
        #111118 19% 36%,
        #eab308 37% 52%,
        #111118 53% 70%,
        #fafaf8 71% 100%
    );
    background-clip: padding-box;
}

/* ── HEADER — slim, premium ───────────────────────── */
.hdr {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.0rem 0 1.0rem;
    border-bottom: 1px solid rgba(17,17,24,0.08);
    margin-bottom: 0;
    animation: hdrIn 0.5s ease both;
    position: relative;
}

/* animated road stripe — thin amber dashes */
.hdr-road {
    position: absolute;
    bottom: -1px; left: 0; right: 0;
    height: 2px; overflow: hidden;
}
.hdr-road::after {
    content: "";
    display: block; height: 100%;
    background: repeating-linear-gradient(
        90deg,
        #111118 0px, #111118 32px,
        transparent 32px, transparent 48px
    );
    animation: roadRun 1.4s linear infinite;
}
@keyframes roadRun {
    from { transform: translateX(0); }
    to   { transform: translateX(-48px); }
}

@keyframes hdrIn {
    from { opacity: 0; transform: translateY(-10px); }
    to   { opacity: 1; transform: translateY(0); }
}

.hdr-logo {
    display: flex; align-items: center; gap: 0.6rem;
}

.hdr-shield {
    width: 30px; height: 30px;
    background: #111118;
    border-radius: 8px 8px 14px 14px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.hdr-shield::after {
    content: "";
    width: 10px; height: 10px;
    border-radius: 3px 3px 8px 8px;
    background: #eab308;
}

.hdr-name {
    font-family: 'Outfit', sans-serif;
    font-size: 1.0rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #111118;
}

.hdr-chips {
    display: flex; align-items: center; gap: 0.45rem;
}

.chip {
    font-family: 'Geist Mono', monospace;
    font-size: 0.62rem;
    font-weight: 400;
    letter-spacing: 0.05em;
    padding: 0.26rem 0.62rem;
    border-radius: 6px;
    color: #6b6b7e;
    background: rgba(17,17,24,0.05);
    border: 1px solid rgba(17,17,24,0.08);
    white-space: nowrap;
}
.chip-dark {
    background: #111118; color: #fafaf8;
    border-color: #111118;
    display: flex; align-items: center; gap: 5px;
}
.chip-dot {
    width: 5px; height: 5px; border-radius: 50%;
    background: #4ade80;
    animation: dotPulse 2s ease-in-out infinite;
}
@keyframes dotPulse {
    0%,100% { opacity:1; transform:scale(1); }
    50%      { opacity:0.3; transform:scale(0.55); }
}

/* ── HERO — compact editorial strip ──────────────── */
.hero {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 3rem;
    align-items: center;
    padding: 2.2rem 0 2.0rem;
    border-bottom: 1px solid rgba(17,17,24,0.07);
    margin-bottom: 2rem;
    animation: hdrIn 0.55s ease 0.06s both;
}

.hero-eyebrow {
    font-family: 'Geist Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #9090a0;
    margin-bottom: 0.8rem;
    display: flex; align-items: center; gap: 7px;
}
.hero-eyebrow span {
    display: inline-block;
    width: 18px; height: 1.5px;
    background: #9090a0; border-radius: 2px;
}

.hero-title {
    font-family: 'Instrument Serif', serif;
    font-size: clamp(2.0rem, 3.6vw, 3.1rem);
    font-weight: 400;
    line-height: 1.12;
    letter-spacing: -0.025em;
    color: #111118;
    margin-bottom: 0.9rem;
}
.hero-title em {
    font-style: italic;
    color: #111118;
}

.hero-desc {
    font-size: 0.90rem;
    font-weight: 300;
    line-height: 1.72;
    color: #6b6b7e;
    max-width: 440px;
}

.hero-stats {
    display: flex;
    gap: 0;
    align-items: stretch;
    border: 1px solid rgba(17,17,24,0.08);
    border-radius: 16px;
    overflow: hidden;
    background: rgba(255,255,255,0.70);
    backdrop-filter: blur(10px);
}
.hstat {
    padding: 1.1rem 1.4rem;
    text-align: center;
    border-right: 1px solid rgba(17,17,24,0.07);
    min-width: 80px;
}
.hstat:last-child { border-right: none; }
.hstat-val {
    font-family: 'Instrument Serif', serif;
    font-size: 1.85rem;
    font-weight: 400;
    color: #111118;
    line-height: 1;
    letter-spacing: -0.04em;
}
.hstat-label {
    font-family: 'Geist Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #a0a0b0;
    margin-top: 0.3rem;
}

/* ── CARDS ────────────────────────────────────────── */
.card {
    background: rgba(255,255,255,0.82);
    border: 1px solid rgba(17,17,24,0.07);
    border-radius: 20px;
    padding: 1.5rem 1.6rem;
    margin-bottom: 1.0rem;
    backdrop-filter: blur(16px) saturate(140%);
    -webkit-backdrop-filter: blur(16px) saturate(140%);
    position: relative; overflow: hidden;
    box-shadow: 0 1px 3px rgba(17,17,24,0.04), 0 6px 20px rgba(17,17,24,0.05);
    transition: transform 0.28s cubic-bezier(0.22,1,0.36,1), box-shadow 0.28s ease, border-color 0.22s ease;
    animation: cardUp 0.50s cubic-bezier(0.22,1,0.36,1) both;
}

/* top road stripe on hover */
.card::before {
    content: "";
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: repeating-linear-gradient(90deg,
        #111118 0px, #111118 28px, transparent 28px, transparent 42px);
    opacity: 0; transition: opacity 0.22s ease;
    animation: roadRun 1.4s linear infinite;
}
.card:hover { transform: translateY(-4px) scale(1.002); border-color: rgba(17,17,24,0.14); box-shadow: 0 2px 6px rgba(17,17,24,0.05), 0 18px 44px rgba(17,17,24,0.09); }
.card:hover::before { opacity: 1; }

@keyframes cardUp {
    from { opacity:0; transform:translateY(16px); }
    to   { opacity:1; transform:translateY(0); }
}
.card:nth-child(2){animation-delay:0.06s;}
.card:nth-child(3){animation-delay:0.12s;}

.card-eyebrow {
    font-family: 'Geist Mono', monospace;
    font-size: 0.60rem; letter-spacing: 0.14em;
    text-transform: uppercase; color: #b0b0be;
    margin-bottom: 0.38rem;
    display: flex; align-items: center; gap: 7px;
}
.card-eyebrow::after {
    content: ""; flex: 1; height: 1px;
    background: rgba(17,17,24,0.06);
}
.card-title {
    font-family: 'Instrument Serif', serif;
    font-size: 1.25rem; font-weight: 400;
    letter-spacing: -0.02em; color: #111118;
    margin-bottom: 0.25rem;
}
.card-note {
    font-size: 0.83rem; font-weight: 300;
    color: #8a8a9a; line-height: 1.58;
    margin-bottom: 1.0rem; padding-bottom: 0.85rem;
    border-bottom: 1px solid rgba(17,17,24,0.05);
}

/* ── STREAMLIT WIDGET OVERRIDES ───────────────────── */
label, div[data-testid="stWidgetLabel"] p {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500 !important; font-size: 0.83rem !important;
    color: #3a3a4e !important;
}

div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.95) !important;
    border: 1px solid rgba(17,17,24,0.11) !important;
    border-radius: 10px !important; min-height: 42px !important;
    color: #111118 !important; -webkit-text-fill-color: #111118 !important;
    font-weight: 500 !important; font-size: 0.87rem !important;
    box-shadow: 0 1px 3px rgba(17,17,24,0.05) !important;
    transition: border-color 0.18s, box-shadow 0.18s !important;
}
div[data-baseweb="select"] span, div[data-baseweb="select"] input {
    color: #111118 !important; -webkit-text-fill-color: #111118 !important; opacity: 1 !important;
}
div[data-baseweb="select"] svg { color: #eab308 !important; }
div[data-baseweb="select"] > div:hover {
    border-color: rgba(234,179,8,0.50) !important;
    box-shadow: 0 0 0 3px rgba(234,179,8,0.09) !important;
}
[data-baseweb="menu"], [data-baseweb="popover"] > div {
    background: #ffffff !important; border: 1px solid rgba(17,17,24,0.09) !important;
    border-radius: 12px !important; box-shadow: 0 12px 36px rgba(17,17,24,0.12) !important;
}
[data-baseweb="option"] {
    color: #111118 !important; font-weight: 500 !important; font-size: 0.86rem !important;
    border-radius: 6px !important; margin: 2px 6px !important;
}
[data-baseweb="option"]:hover, [data-baseweb="option"][aria-selected="true"] {
    background: rgba(234,179,8,0.10) !important;
}

[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.95) !important;
    border: 1px solid rgba(17,17,24,0.11) !important;
    border-radius: 10px !important; color: #111118 !important;
    -webkit-text-fill-color: #111118 !important; font-weight: 500 !important;
    font-size: 0.87rem !important; box-shadow: 0 1px 3px rgba(17,17,24,0.05) !important;
    transition: border-color 0.18s, box-shadow 0.18s !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: rgba(234,179,8,0.55) !important;
    box-shadow: 0 0 0 3px rgba(234,179,8,0.10) !important; outline: none !important;
}
[data-testid="stNumberInput"] button {
    background: rgba(17,17,24,0.05) !important; color: #3a3a4e !important;
    border: 1px solid rgba(17,17,24,0.08) !important; border-radius: 7px !important;
    font-weight: 700 !important; transition: all 0.15s !important;
}
[data-testid="stNumberInput"] button:hover {
    background: rgba(234,179,8,0.14) !important; border-color: rgba(234,179,8,0.28) !important;
}

/* slider — clean minimal thumb, tire tread rings */
[data-testid="stSlider"] [role="slider"],
[data-testid="stSelectSlider"] [role="slider"] {
    width: 22px !important; height: 22px !important;
    background:
        radial-gradient(circle at 50% 50%,
            #fafaf8 0% 16%,
            #111118 17% 34%,
            #444452 35% 51%,
            #111118 52% 68%,
            #fafaf8 69% 100%) !important;
    border: 2.5px solid #ffffff !important;
    box-shadow: 0 0 0 1.5px #111118, 0 3px 10px rgba(17,17,24,0.22) !important;
    transition: box-shadow 0.18s ease, transform 0.18s ease !important;
}
[data-testid="stSlider"] [role="slider"]:hover,
[data-testid="stSelectSlider"] [role="slider"]:hover {
    box-shadow: 0 0 0 1.5px #111118, 0 0 0 5px rgba(234,179,8,0.22), 0 4px 14px rgba(17,17,24,0.25) !important;
    transform: scale(1.1) !important;
}

/* ── 3D RUN BUTTON ────────────────────────────────── */
div.stButton > button {
    background: #111118 !important;
    color: #fafaf8 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2.0rem !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.90rem !important;
    letter-spacing: 0.01em !important;
    /* 3D effect: layered box shadows */
    box-shadow:
        0 1px 0 rgba(255,255,255,0.08) inset,
        0 -1px 0 rgba(0,0,0,0.3) inset,
        0 4px 0 #000000,
        0 6px 16px rgba(17,17,24,0.30) !important;
    transform: translateY(0px) !important;
    transition:
        transform 0.14s cubic-bezier(0.22,1,0.36,1),
        box-shadow 0.14s cubic-bezier(0.22,1,0.36,1) !important;
    position: relative; overflow: hidden;
}
div.stButton > button::after {
    content: "";
    position: absolute; top: 0; left: -100%;
    width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    transform: skewX(-20deg);
    animation: shimmer 3.5s ease-in-out infinite 1s;
}
@keyframes shimmer {
    0%   { left: -100%; }
    50%  { left: 140%; }
    100% { left: 140%; }
}
div.stButton > button:hover {
    box-shadow:
        0 1px 0 rgba(255,255,255,0.08) inset,
        0 -1px 0 rgba(0,0,0,0.3) inset,
        0 6px 0 #000000,
        0 10px 28px rgba(17,17,24,0.36) !important;
    transform: translateY(-2px) !important;
}
div.stButton > button:active {
    box-shadow:
        0 1px 0 rgba(255,255,255,0.08) inset,
        0 -1px 0 rgba(0,0,0,0.3) inset,
        0 1px 0 #000000,
        0 3px 8px rgba(17,17,24,0.22) !important;
    transform: translateY(3px) !important;
}

/* ── RESULTS ──────────────────────────────────────── */
.results-bar {
    display: flex; align-items: center; gap: 1rem;
    margin: 2rem 0 1.7rem;
    animation: fadeUp 0.35s ease both;
}
.results-line { flex:1; height:1px; background: rgba(17,17,24,0.07); }
.results-tag {
    font-family:'Geist Mono',monospace; font-size:0.62rem;
    letter-spacing:0.14em; text-transform:uppercase; color:#b0b0be;
    white-space:nowrap;
}

@keyframes fadeUp {
    from { opacity:0; transform:translateY(8px); }
    to   { opacity:1; transform:translateY(0); }
}

/* Score */
.score-wrap { margin:1.1rem 0 0.7rem; animation: popIn 0.65s cubic-bezier(0.22,1,0.36,1) 0.08s both; }
@keyframes popIn {
    from { opacity:0; transform:scale(0.72) translateY(8px); }
    to   { opacity:1; transform:scale(1) translateY(0); }
}
.score-num {
    font-family:'Instrument Serif',serif;
    font-size:6.2rem; font-weight:400;
    line-height:0.88; letter-spacing:-0.06em;
    display:flex; align-items:flex-start;
}
.score-pct {
    font-size:2.2rem; opacity:0.35;
    margin-top:0.6rem; font-style:italic;
}
.score-sub {
    font-family:'Geist Mono',monospace;
    font-size:0.63rem; letter-spacing:0.12em;
    text-transform:uppercase; margin-top:0.4rem;
}
.c-low  { color:#16a34a; }
.c-med  { color:#d97706; }
.c-high { color:#dc2626; }

/* Progress bar */
.pbar { height:6px; border-radius:999px; background:rgba(17,17,24,0.07); overflow:hidden; margin:0.9rem 0 0.4rem; }
.pbar-fill {
    height:100%; border-radius:999px;
    animation: growBar 1.1s cubic-bezier(0.22,1,0.36,1) both;
    position:relative;
}
.pbar-fill::after {
    content:""; position:absolute; top:0; left:0; right:0; height:50%;
    background:rgba(255,255,255,0.38); border-radius:999px;
}
@keyframes growBar { from { width:0%; } }

/* Gauge */
.gauge {
    margin-top:0.95rem; background:rgba(17,17,24,0.03);
    border:1px solid rgba(17,17,24,0.06); border-radius:12px;
    padding:0.8rem 0.9rem 0.6rem;
}
.gauge-bar {
    height:11px; border-radius:999px; position:relative; overflow:visible;
    background:linear-gradient(90deg,
        #4ade80 0%, #a3e635 22%, #fde68a 40%, #fb923c 58%, #f87171 76%, #ef4444 100%);
    box-shadow: inset 0 1.5px 3px rgba(0,0,0,0.08);
}
.gauge-pin {
    position:absolute; top:50%; left:0%;
    transform: translateX(-50%) translateY(-50%);
    width:4px; height:22px;
    background:#111118; border-radius:999px;
    box-shadow: 0 0 0 2px #fff, 0 0 0 3.5px rgba(17,17,24,0.18), 0 3px 9px rgba(17,17,24,0.28);
    animation: pinDrop 0.8s cubic-bezier(0.22,1,0.36,1) 0.18s both;
}
@keyframes pinDrop {
    from { opacity:0; transform:translateX(-50%) translateY(-50%) scaleY(0); }
    to   { opacity:1; transform:translateX(-50%) translateY(-50%) scaleY(1); }
}
.gauge-lbls {
    display:flex; justify-content:space-between; margin-top:0.42rem;
}
.gauge-lbl { font-family:'Geist Mono',monospace; font-size:0.58rem; color:#b0b0be; letter-spacing:0.04em; }

/* Badge */
.badge {
    display:inline-flex; align-items:center; gap:6px;
    border-radius:999px; padding:0.38rem 0.85rem;
    font-weight:600; font-size:0.76rem; letter-spacing:0.02em;
    border:1px solid; margin-top:0.9rem;
    animation: fadeUp 0.4s ease 0.28s both;
}
.badge-dot { width:6px; height:6px; border-radius:50%; background:currentColor; animation: dotPulse 2s ease-in-out infinite; }
.badge-low  { background:#f0fdf4; color:#15803d; border-color:#bbf7d0; }
.badge-med  { background:#fffbeb; color:#b45309; border-color:#fcd34d; }
.badge-high { background:#fef2f2; color:#b91c1c; border-color:#fecaca; }

/* Metric rows */
.mrow { display:flex; justify-content:space-between; align-items:center; padding:0.56rem 0; border-bottom:1px solid rgba(17,17,24,0.05); gap:1rem; }
.mrow:last-child { border-bottom:none; }
.mrow-k { font-family:'Geist Mono',monospace; font-size:0.65rem; letter-spacing:0.07em; text-transform:uppercase; color:#a0a0b0; }
.mrow-v { font-weight:600; font-size:0.86rem; color:#111118; text-align:right; }

/* Action callout */
.action-callout {
    margin:1.0rem 0; border-radius:12px; padding:1.0rem 1.1rem;
    background:rgba(17,17,24,0.03);
    border:1px solid rgba(17,17,24,0.08);
    border-left:3px solid #111118;
    animation: fadeUp 0.45s ease 0.18s both;
}
.action-title { font-family:'Instrument Serif',serif; font-size:1.0rem; font-weight:400; color:#111118; margin-bottom:0.38rem; }
.action-desc  { font-size:0.82rem; font-weight:300; color:#6b6b7e; line-height:1.65; }

/* Drivers */
.driver { display:flex; gap:0.8rem; align-items:flex-start; padding:0.75rem 0; border-bottom:1px solid rgba(17,17,24,0.05); animation: fadeUp 0.38s ease both; }
.driver:last-child { border-bottom:none; }
.driver-idx { font-family:'Geist Mono',monospace; font-size:0.62rem; font-weight:500; width:24px; height:24px; border-radius:7px; background:rgba(17,17,24,0.06); border:1px solid rgba(17,17,24,0.09); color:#6b6b7e; display:flex; align-items:center; justify-content:center; flex-shrink:0; margin-top:1px; }
.driver-title { font-weight:600; font-size:0.86rem; color:#111118; margin-bottom:0.15rem; }
.driver-desc  { font-size:0.80rem; font-weight:300; color:#8a8a9a; line-height:1.55; }

.driver:nth-child(1){animation-delay:0.05s;}
.driver:nth-child(2){animation-delay:0.10s;}
.driver:nth-child(3){animation-delay:0.15s;}
.driver:nth-child(4){animation-delay:0.20s;}
.driver:nth-child(5){animation-delay:0.25s;}
.driver:nth-child(6){animation-delay:0.30s;}
.driver:nth-child(7){animation-delay:0.35s;}

.footer {
    text-align:center; font-family:'Geist Mono',monospace;
    font-size:0.60rem; letter-spacing:0.09em; text-transform:uppercase;
    color:#c0c0cc; margin-top:3rem; padding-top:1.2rem;
    border-top:1px solid rgba(17,17,24,0.06);
}
</style>
""", unsafe_allow_html=True)


def esc(x): return html_mod.escape(str(x))
def rh(c):  st.markdown(c, unsafe_allow_html=True)

def bi_val(l): return {"None":0,"One reported injury":1,"Multiple / serious injuries":2}[l]
def wi_val(l): return {"No witnesses":0,"One witness":1,"Two witnesses":2,"Three or more witnesses":3}[l]

def risk_meta(p):
    if p < 0.25: return "low",  "Low Risk",    "badge-low",  "c-low",  "#22c55e"
    if p < 0.50: return "med",  "Medium Risk", "badge-med",  "c-med",  "#f59e0b"
    return               "high", "High Risk",   "badge-high", "c-high", "#ef4444"

def action_meta(p):
    if p >= 0.50:
        return "Send for Manual Investigation", \
               "Score is significantly elevated. Assign to an investigator before any payout is issued."
    if p >= THRESHOLD:
        return "Flag for Secondary Review", \
               "Score exceeds the operating threshold. Route to supervisor review and request supporting documentation."
    return "Process Normally", \
           "No elevated fraud signal detected. Claim may proceed through the standard processing route."


# ── HEADER ───────────────────────────────────────────────────────────────────
rh("""
<div class="hdr">
  <div class="hdr-logo">
    <div class="hdr-shield"></div>
    <span class="hdr-name">Shield · Insurance Fraud Detection</span>
  </div>
  <div class="hdr-chips">
    <span class="chip chip-dark"><span class="chip-dot"></span>Model Ready</span>
    <span class="chip">Random Forest</span>
    <span class="chip">Threshold 25%</span>
    <span class="chip">v2.4</span>
  </div>
  <div class="hdr-road"></div>
</div>
""")

# ── HERO ──────────────────────────────────────────────────────────────────────
rh("""
<div class="hero">
  <div>
    <div class="hero-eyebrow"><span></span>Auto Insurance · ML Risk Scoring</div>
    <h1 class="hero-title">Insurance <em>Fraud</em><br>Detection</h1>
    <p class="hero-desc">
      ML-powered triage for vehicle claims — scoring fraud risk
      from incident details, policy data, and financial signals.
    </p>
  </div>
  <div class="hero-stats">
    <div class="hstat">
      <div class="hstat-val">12</div>
      <div class="hstat-label">Features</div>
    </div>
    <div class="hstat">
      <div class="hstat-val">25%</div>
      <div class="hstat-label">Threshold</div>
    </div>
    <div class="hstat">
      <div class="hstat-val">RF</div>
      <div class="hstat-label">Algorithm</div>
    </div>
  </div>
</div>
""")

# ── INPUTS ────────────────────────────────────────────────────────────────────
left, right = st.columns(2, gap="large")

with left:
    rh("""<div class="card">
  <div class="card-eyebrow">01 · Incident profile</div>
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
  <div class="card-eyebrow">02 · Financial profile</div>
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

# ── RESULTS ───────────────────────────────────────────────────────────────────
if predict:
    import random
    fraud_prob = random.uniform(0.05, 0.92)   # DEMO — replace with model.predict_proba(...)

    fraud_pred = int(fraud_prob >= THRESHOLD)
    risk_cls, risk_label, badge_cls, text_cls, risk_color = risk_meta(fraud_prob)
    action_title, action_desc = action_meta(fraud_prob)

    pct  = round(fraud_prob * 100, 1)
    verdict     = "Likely Fraudulent" if fraud_pred == 1 else "Likely Legitimate"
    marker_left = min(max(pct, 2), 97)
    delta       = abs(pct - THRESHOLD * 100)
    cpr         = (total_claim_amount / policy_annual_premium) if policy_annual_premium else 0

    rh("""<div class="results-bar">
  <div class="results-line"></div>
  <span class="results-tag">Assessment Results</span>
  <div class="results-line"></div>
</div>""")

    r_col, a_col = st.columns(2, gap="large")

    with r_col:
        rh(f"""<div class="card">
  <div class="card-eyebrow">03 · Model output</div>
  <div class="card-title">Fraud Probability Score</div>

  <div class="score-wrap">
    <div class="score-num {text_cls}">{pct:.0f}<span class="score-pct">%</span></div>
    <div class="score-sub {text_cls}">Estimated fraud probability</div>
  </div>

  <div class="pbar">
    <div class="pbar-fill" style="width:{pct}%; background:linear-gradient(90deg,{risk_color}88,{risk_color});"></div>
  </div>

  <div class="gauge">
    <div class="gauge-bar">
      <div class="gauge-pin" style="left:{marker_left}%;"></div>
    </div>
    <div class="gauge-lbls">
      <span class="gauge-lbl">0%</span>
      <span class="gauge-lbl">25%</span>
      <span class="gauge-lbl">50%</span>
      <span class="gauge-lbl">75%</span>
      <span class="gauge-lbl">100%</span>
    </div>
  </div>

  <div style="margin-top:1.0rem;">
    <div class="mrow"><span class="mrow-k">Threshold</span><span class="mrow-v">{int(THRESHOLD*100)}%</span></div>
    <div class="mrow"><span class="mrow-k">Delta</span><span class="mrow-v">{delta:.1f} pp</span></div>
    <div class="mrow"><span class="mrow-k">Verdict</span><span class="mrow-v {text_cls}">{esc(verdict)}</span></div>
  </div>

  <span class="badge {badge_cls}"><span class="badge-dot"></span>{esc(risk_label)}</span>
</div>""")

    with a_col:
        rh(f"""<div class="card">
  <div class="card-eyebrow">04 · Claim routing</div>
  <div class="card-title">Recommended Handling</div>

  <div class="action-callout">
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

    # ── DRIVERS ──────────────────────────────────────────────────────────────
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
  <div class="driver-idx">—</div>
  <div><div class="driver-title">No major signals triggered</div>
  <div class="driver-desc">Entered values did not activate primary review flags.</div></div>
</div>"""
    else:
        d_html = "".join(f"""<div class="driver">
  <div class="driver-idx">{str(i).zfill(2)}</div>
  <div><div class="driver-title">{esc(t)}</div>
  <div class="driver-desc">{esc(d)}</div></div>
</div>""" for i,(t,d) in enumerate(drivers,1))

    rh(f"""<div class="card">
  <div class="card-eyebrow">05 · Review signals</div>
  <div class="card-title">Key Factors Behind the Recommendation</div>
  <div class="card-note">Informational signals to support triage — not deterministic decisions.</div>
  {d_html}
</div>""")

rh("""<div class="footer">Shield · Portfolio Demonstration · Triage support only — not automatic denial or approval</div>""")