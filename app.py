import streamlit as st
import joblib
import html

# model = joblib.load("deploy_fraud_model.pkl")
# template_row = joblib.load("deploy_input_template.pkl")
THRESHOLD = 0.25

st.set_page_config(
    page_title="Insurance Fraud Detection",
    page_icon="🚗",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    color: #e2e8f0 !important;
}

/* ── DARK ATMOSPHERIC BACKGROUND ─────────────────── */
.stApp {
    background:
        radial-gradient(ellipse 80% 60% at 10% 0%,   rgba(250,204,21,0.08)  0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 90% 10%,  rgba(59,130,246,0.10)  0%, transparent 55%),
        radial-gradient(ellipse 50% 40% at 50% 100%, rgba(139,92,246,0.07)  0%, transparent 50%),
        linear-gradient(160deg, #080c14 0%, #0d1520 40%, #0a1118 70%, #06090f 100%);
    min-height: 100vh;
}

/* Subtle animated grain overlay */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(ellipse at 20% 30%, rgba(250,204,21,0.04) 0%, transparent 40%),
        radial-gradient(ellipse at 80% 70%, rgba(59,130,246,0.05) 0%, transparent 40%),
        linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px),
        linear-gradient(rgba(255,255,255,0.012) 1px, transparent 1px);
    background-size: 100% 100%, 100% 100%, 60px 60px, 60px 60px;
    pointer-events: none;
    z-index: 0;
    animation: bgPulse 12s ease-in-out infinite alternate;
}

@keyframes bgPulse {
    from { opacity: 0.7; }
    to   { opacity: 1.0; }
}

.main .block-container {
    max-width: 1200px;
    padding: 2rem 2.2rem 6rem;
    position: relative;
    z-index: 1;
}

[data-testid="stHeader"] { background: transparent; }

/* ── GLASS MIXIN ──────────────────────────────────── */
.glass {
    background: linear-gradient(135deg,
        rgba(255,255,255,0.06) 0%,
        rgba(255,255,255,0.02) 50%,
        rgba(255,255,255,0.04) 100%);
    backdrop-filter: blur(24px) saturate(180%) brightness(1.05);
    -webkit-backdrop-filter: blur(24px) saturate(180%) brightness(1.05);
    border: 1px solid rgba(255,255,255,0.10);
    border-top: 1px solid rgba(255,255,255,0.18);
    border-left: 1px solid rgba(255,255,255,0.12);
    box-shadow:
        0 0 0 1px rgba(255,255,255,0.03) inset,
        0 32px 80px rgba(0,0,0,0.50),
        0 8px 24px rgba(0,0,0,0.35),
        0 2px 6px rgba(0,0,0,0.20);
}

/* ── HERO ─────────────────────────────────────────── */
.hero {
    border-radius: 32px;
    padding: 3rem 3rem 2.5rem;
    margin-bottom: 1.8rem;
    overflow: hidden;
    position: relative;
    animation: riseIn 0.7s cubic-bezier(0.22,1,0.36,1) both;
    background: linear-gradient(135deg,
        rgba(255,255,255,0.07) 0%,
        rgba(255,255,255,0.02) 50%,
        rgba(255,255,255,0.05) 100%);
    backdrop-filter: blur(32px) saturate(200%);
    -webkit-backdrop-filter: blur(32px) saturate(200%);
    border: 1px solid rgba(255,255,255,0.12);
    border-top: 1px solid rgba(255,255,255,0.22);
    box-shadow:
        0 0 0 1px rgba(255,255,255,0.04) inset,
        0 40px 100px rgba(0,0,0,0.60),
        0 1px 0 rgba(255,255,255,0.08) inset;
}

/* Floating ambient orbs inside hero */
.hero::before {
    content: "";
    position: absolute;
    top: -80px; right: -60px;
    width: 340px; height: 340px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(250,204,21,0.14) 0%, transparent 70%);
    animation: orbFloat 8s ease-in-out infinite;
    pointer-events: none;
}

.hero::after {
    content: "";
    position: absolute;
    bottom: -60px; left: -40px;
    width: 260px; height: 260px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(59,130,246,0.12) 0%, transparent 70%);
    animation: orbFloat 10s ease-in-out infinite reverse;
    pointer-events: none;
}

/* Animated road stripe at bottom of hero */
.hero-road {
    position: absolute;
    left: 0; right: 0; bottom: 20px;
    height: 6px;
    overflow: hidden;
    border-radius: 0 0 32px 32px;
}

.hero-road::after {
    content: "";
    display: block;
    height: 100%;
    background: repeating-linear-gradient(
        90deg,
        rgba(250,204,21,0.70) 0 52px,
        transparent 52px 80px
    );
    animation: roadMove 2.4s linear infinite;
}

@keyframes roadMove {
    from { transform: translateX(0); }
    to   { transform: translateX(-80px); }
}

@keyframes orbFloat {
    0%, 100% { transform: translate(0,0) scale(1); }
    33%       { transform: translate(20px,-15px) scale(1.05); }
    66%       { transform: translate(-10px,10px) scale(0.97); }
}

@keyframes riseIn {
    from { opacity: 0; transform: translateY(28px) scale(0.98); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}

.kicker, .section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.70rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: rgba(250,204,21,0.75);
    font-weight: 600;
    margin-bottom: 0.8rem;
}

.hero-title {
    font-size: clamp(2.6rem, 5vw, 4.4rem);
    line-height: 0.94;
    font-weight: 900;
    letter-spacing: -0.055em;
    margin: 0;
    color: #f8fafc;
    text-shadow: 0 0 60px rgba(250,204,21,0.15);
}

.hero-title span {
    background: linear-gradient(135deg, #facc15 0%, #f59e0b 50%, #fbbf24 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-sub {
    color: rgba(203,213,225,0.80);
    max-width: 680px;
    font-size: 1rem;
    line-height: 1.75;
    margin-top: 1.1rem;
    margin-bottom: 2rem;
    font-weight: 400;
}

/* ── CARDS ────────────────────────────────────────── */
.card {
    border-radius: 24px;
    padding: 1.7rem 1.8rem;
    margin-bottom: 1.2rem;
    animation: riseIn 0.55s cubic-bezier(0.22,1,0.36,1) both;
    transition:
        transform 0.28s cubic-bezier(0.22,1,0.36,1),
        box-shadow 0.28s ease,
        border-color 0.28s ease;
    background: linear-gradient(135deg,
        rgba(255,255,255,0.065) 0%,
        rgba(255,255,255,0.02)  60%,
        rgba(255,255,255,0.04)  100%);
    backdrop-filter: blur(20px) saturate(160%);
    -webkit-backdrop-filter: blur(20px) saturate(160%);
    border: 1px solid rgba(255,255,255,0.09);
    border-top: 1px solid rgba(255,255,255,0.16);
    box-shadow:
        0 0 0 1px rgba(255,255,255,0.025) inset,
        0 24px 60px rgba(0,0,0,0.45),
        0 4px 12px rgba(0,0,0,0.25);
    position: relative;
    overflow: hidden;
}

.card::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: linear-gradient(135deg,
        rgba(255,255,255,0.04) 0%,
        transparent 50%);
    pointer-events: none;
}

.card:hover {
    transform: translateY(-6px) rotateX(1deg);
    border-color: rgba(250,204,21,0.22);
    box-shadow:
        0 0 0 1px rgba(250,204,21,0.08) inset,
        0 36px 80px rgba(0,0,0,0.55),
        0 0 40px rgba(250,204,21,0.06),
        0 4px 16px rgba(0,0,0,0.30);
}

.heading {
    font-size: 1.45rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    margin-bottom: 0.4rem;
    color: #f1f5f9;
}

.note {
    color: rgba(148,163,184,0.85);
    font-size: 0.92rem;
    line-height: 1.65;
}

/* ── STREAMLIT INPUTS ─────────────────────────────── */
label,
div[data-testid="stWidgetLabel"] p {
    font-weight: 600 !important;
    color: #cbd5e1 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.01em !important;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background: rgba(15,23,42,0.70) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 14px !important;
    min-height: 46px !important;
    color: #e2e8f0 !important;
    -webkit-text-fill-color: #e2e8f0 !important;
    font-weight: 500 !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.35) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    backdrop-filter: blur(12px) !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] input {
    color: #e2e8f0 !important;
    -webkit-text-fill-color: #e2e8f0 !important;
    opacity: 1 !important;
}

div[data-baseweb="select"] svg { color: #facc15 !important; }

div[data-baseweb="select"] > div:hover {
    border-color: rgba(250,204,21,0.45) !important;
    box-shadow:
        0 0 0 3px rgba(250,204,21,0.10),
        0 8px 24px rgba(0,0,0,0.40) !important;
}

/* Dropdown menu */
[data-baseweb="menu"],
[data-baseweb="popover"] > div {
    background: rgba(10,16,26,0.95) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 14px !important;
    backdrop-filter: blur(24px) !important;
    box-shadow: 0 24px 60px rgba(0,0,0,0.65) !important;
}

[data-baseweb="option"] {
    color: #e2e8f0 !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
    margin: 2px 6px !important;
}

[data-baseweb="option"]:hover {
    background: rgba(250,204,21,0.12) !important;
}

/* Number input */
[data-testid="stNumberInput"] input {
    background: rgba(15,23,42,0.70) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 14px !important;
    color: #e2e8f0 !important;
    -webkit-text-fill-color: #e2e8f0 !important;
    font-weight: 500 !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.30) !important;
    backdrop-filter: blur(12px) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

[data-testid="stNumberInput"] input:focus {
    border-color: rgba(250,204,21,0.50) !important;
    box-shadow:
        0 0 0 3px rgba(250,204,21,0.12),
        0 8px 24px rgba(0,0,0,0.40) !important;
    outline: none !important;
}

[data-testid="stNumberInput"] button {
    background: rgba(30,41,59,0.80) !important;
    color: #facc15 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    transition: background 0.15s ease !important;
}

[data-testid="stNumberInput"] button:hover {
    background: rgba(250,204,21,0.18) !important;
    border-color: rgba(250,204,21,0.35) !important;
}

/* Slider */
[data-testid="stSlider"] [role="slider"],
[data-testid="stSelectSlider"] [role="slider"] {
    background: radial-gradient(circle, #facc15 0 30%, #d97706 70%) !important;
    border: 3px solid rgba(255,255,255,0.90) !important;
    width: 22px !important;
    height: 22px !important;
    box-shadow:
        0 0 0 4px rgba(250,204,21,0.25),
        0 6px 18px rgba(0,0,0,0.50) !important;
    transition: box-shadow 0.2s ease !important;
}

[data-testid="stSlider"] [role="slider"]:hover,
[data-testid="stSelectSlider"] [role="slider"]:hover {
    box-shadow:
        0 0 0 7px rgba(250,204,21,0.20),
        0 8px 24px rgba(0,0,0,0.60) !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] > div > div > div:first-child,
[data-testid="stSelectSlider"] [data-baseweb="slider"] > div > div > div:first-child {
    background: rgba(30,41,59,0.80) !important;
}

/* ── RUN BUTTON ───────────────────────────────────── */
div.stButton > button {
    background: linear-gradient(135deg, #facc15 0%, #f59e0b 50%, #d97706 100%) !important;
    color: #111827 !important;
    border: none !important;
    border-radius: 18px !important;
    padding: 0.95rem 2.4rem !important;
    font-weight: 800 !important;
    font-size: 0.96rem !important;
    letter-spacing: 0.01em !important;
    box-shadow:
        0 0 0 1px rgba(250,204,21,0.30) inset,
        0 20px 44px rgba(217,119,6,0.35),
        0 0 60px rgba(250,204,21,0.12) !important;
    transition:
        transform 0.22s cubic-bezier(0.22,1,0.36,1),
        box-shadow 0.22s ease !important;
    position: relative;
    overflow: hidden;
}

div.stButton > button::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.22) 0%, transparent 60%);
    border-radius: inherit;
    pointer-events: none;
}

div.stButton > button:hover {
    transform: translateY(-4px) scale(1.01) !important;
    box-shadow:
        0 0 0 1px rgba(250,204,21,0.35) inset,
        0 28px 56px rgba(217,119,6,0.45),
        0 0 80px rgba(250,204,21,0.18) !important;
}

div.stButton > button:active {
    transform: translateY(-1px) scale(0.99) !important;
}

/* ── RESULT SCORES & BADGES ───────────────────────── */
.score {
    font-size: 5.5rem;
    line-height: 1;
    font-weight: 900;
    letter-spacing: -0.07em;
    margin: 0.4rem 0 0.9rem;
    filter: drop-shadow(0 0 30px currentColor);
    animation: scorePop 0.6s cubic-bezier(0.22,1,0.36,1) both 0.1s;
}

@keyframes scorePop {
    from { transform: scale(0.7); opacity: 0; }
    to   { transform: scale(1); opacity: 1; }
}

.low-text    { color: #4ade80; }
.medium-text { color: #fb923c; }
.high-text   { color: #f87171; }

.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    border-radius: 999px;
    padding: 0.46rem 1rem;
    font-weight: 700;
    font-size: 0.82rem;
    border: 1px solid;
    letter-spacing: 0.02em;
}

.badge-low    { background: rgba(74,222,128,0.12); color: #4ade80; border-color: rgba(74,222,128,0.30); }
.badge-medium { background: rgba(251,146,60,0.12); color: #fb923c; border-color: rgba(251,146,60,0.30); }
.badge-high   { background: rgba(248,113,113,0.12); color: #f87171; border-color: rgba(248,113,113,0.30); }

/* ── PROGRESS BAR ─────────────────────────────────── */
.progress-wrap {
    background: rgba(255,255,255,0.07);
    border-radius: 999px;
    height: 10px;
    overflow: hidden;
    margin: 1rem 0 0.6rem;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.30);
}

.progress-fill {
    height: 100%;
    border-radius: 999px;
    position: relative;
    animation: grow 1.1s cubic-bezier(0.22,1,0.36,1) both;
    box-shadow: 0 0 16px currentColor;
}

.progress-fill::after {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 50%;
    background: rgba(255,255,255,0.30);
    border-radius: 999px;
}

@keyframes grow {
    from { width: 0%; }
}

/* ── RISK GAUGE ───────────────────────────────────── */
.gauge-wrap {
    margin-top: 1.2rem;
    background: rgba(0,0,0,0.25);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 1.1rem 1.1rem 0.8rem;
    box-shadow: inset 0 2px 8px rgba(0,0,0,0.25);
}

.gauge-track {
    height: 16px;
    border-radius: 999px;
    background: linear-gradient(90deg,
        #22d3ee 0%,
        #4ade80 18%,
        #a3e635 35%,
        #facc15 50%,
        #fb923c 68%,
        #f87171 85%,
        #ef4444 100%);
    position: relative;
    box-shadow:
        0 0 20px rgba(250,204,21,0.20),
        inset 0 2px 4px rgba(0,0,0,0.20);
}

.gauge-marker {
    position: absolute;
    top: 50%;
    transform: translateX(-50%) translateY(-50%);
    width: 6px;
    height: 30px;
    border-radius: 999px;
    background: #f8fafc;
    box-shadow:
        0 0 0 3px rgba(248,250,252,0.25),
        0 6px 20px rgba(0,0,0,0.60);
    animation: markerSlide 1.0s cubic-bezier(0.22,1,0.36,1) both 0.15s;
}

@keyframes markerSlide {
    from { opacity: 0; transform: translateX(-50%) translateY(-50%) scaleY(0); }
    to   { opacity: 1; transform: translateX(-50%) translateY(-50%) scaleY(1); }
}

.gauge-labels {
    display: flex;
    justify-content: space-between;
    color: rgba(148,163,184,0.75);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    margin-top: 0.55rem;
    letter-spacing: 0.06em;
}

/* ── METRIC ROWS ──────────────────────────────────── */
.metric-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    padding: 0.65rem 0;
    gap: 1rem;
    transition: background 0.15s ease;
}

.metric-row:last-child { border-bottom: none; }

.metric-k {
    color: rgba(148,163,184,0.80);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.73rem;
    letter-spacing: 0.05em;
}

.metric-v {
    font-weight: 700;
    text-align: right;
    color: #e2e8f0;
    font-size: 0.90rem;
}

/* ── DRIVER CARDS ─────────────────────────────────── */
.driver {
    border-bottom: 1px solid rgba(255,255,255,0.06);
    padding: 0.85rem 0;
    display: flex;
    gap: 0.9rem;
    align-items: flex-start;
}

.driver:last-child { border-bottom: none; }

.driver-icon {
    width: 32px;
    height: 32px;
    border-radius: 10px;
    background: rgba(250,204,21,0.12);
    border: 1px solid rgba(250,204,21,0.22);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
    margin-top: 2px;
}

.driver-title {
    font-weight: 700;
    color: #f1f5f9;
    font-size: 0.92rem;
    margin-bottom: 0.2rem;
}

.driver-desc {
    color: rgba(148,163,184,0.80);
    font-size: 0.84rem;
    line-height: 1.55;
}

/* ── DIVIDER ──────────────────────────────────────── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    margin: 0.6rem 0 1.2rem;
}

/* ── FOOTER ───────────────────────────────────────── */
.footer-note {
    text-align: center;
    color: rgba(100,116,139,0.70);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.70rem;
    margin-top: 2.5rem;
    letter-spacing: 0.05em;
}

/* ── STAGGER ANIMATION DELAYS ─────────────────────── */
.card:nth-child(2) { animation-delay: 0.08s; }
.card:nth-child(3) { animation-delay: 0.16s; }

/* Fix streamlit white column backgrounds */
section[data-testid="stSidebar"],
.css-1d391kg, .css-hxt7ib {
    background: transparent !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.03); }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); border-radius: 999px; }
</style>
""", unsafe_allow_html=True)


def esc(x):
    return html.escape(str(x))


def render_html(code):
    st.markdown(code, unsafe_allow_html=True)


def bodily_injuries_label_to_value(label):
    return {"None": 0, "One reported injury": 1, "Multiple / serious injuries": 2}[label]


def witnesses_label_to_value(label):
    return {
        "No witnesses": 0, "One witness": 1,
        "Two witnesses": 2, "Three or more witnesses": 3
    }[label]


def risk_meta(fraud_prob):
    if fraud_prob < 0.25:
        return "low", "Low Risk", "badge-low", "low-text", "#4ade80"
    elif fraud_prob < 0.50:
        return "medium", "Medium Risk", "badge-medium", "medium-text", "#fb923c"
    return "high", "High Risk", "badge-high", "high-text", "#f87171"


def action_meta(fraud_prob):
    if fraud_prob >= 0.50:
        return (
            "Send for Manual Investigation",
            "The model score is high. This claim should be reviewed by an investigator before payout."
        )
    elif fraud_prob >= THRESHOLD:
        return (
            "Flag for Secondary Review",
            "The score is above the operating threshold. Route this claim for supervisor review and request supporting documents."
        )
    return (
        "Process Normally",
        "No elevated fraud signal was detected. This claim can continue through the standard processing route."
    )


# ── HERO ────────────────────────────────────────────────────────────────────
render_html("""
<div class="hero">
  <div class="hero-road"></div>
  <div class="kicker">⬡ Auto Insurance Claims · Fraud Risk Scoring</div>
  <h1 class="hero-title">Insurance <span>Fraud</span><br>Detection</h1>
  <p class="hero-sub">
    A machine-learning triage tool for vehicle insurance claims — scoring risk from
    claim details, policy data, and incident-level signals in real time.
  </p>
  <div style="display:flex; gap:1.4rem; flex-wrap:wrap; margin-top:0.5rem;">
    <div style="display:flex; align-items:center; gap:0.5rem; color:rgba(203,213,225,0.65); font-size:0.82rem; font-family:'IBM Plex Mono',monospace;">
      <span style="width:8px;height:8px;border-radius:50%;background:#4ade80;box-shadow:0 0 8px #4ade80;display:inline-block;"></span>
      Random Forest · 12 features
    </div>
    <div style="display:flex; align-items:center; gap:0.5rem; color:rgba(203,213,225,0.65); font-size:0.82rem; font-family:'IBM Plex Mono',monospace;">
      <span style="width:8px;height:8px;border-radius:50%;background:#facc15;box-shadow:0 0 8px #facc15;display:inline-block;"></span>
      Threshold 25%
    </div>
    <div style="display:flex; align-items:center; gap:0.5rem; color:rgba(203,213,225,0.65); font-size:0.82rem; font-family:'IBM Plex Mono',monospace;">
      <span style="width:8px;height:8px;border-radius:50%;background:#818cf8;box-shadow:0 0 8px #818cf8;display:inline-block;"></span>
      Triage · not auto-denial
    </div>
  </div>
</div>
""")

# ── INPUT COLUMNS ────────────────────────────────────────────────────────────
left, right = st.columns(2, gap="large")

with left:
    render_html("""
<div class="card">
  <div class="section-label">01 · Incident profile</div>
  <div class="heading">Vehicle Incident Details</div>
  <div class="note">Describe the collision, damage severity, injuries, witnesses, and customer tenure.</div>
  <div class="divider"></div>
</div>
""")

    incident_severity = st.selectbox(
        "Incident Severity",
        ["Minor Damage", "Major Damage", "Total Loss", "Trivial Damage"],
    )
    incident_type = st.selectbox(
        "Incident Type",
        ["Single Vehicle Collision", "Multi-vehicle Collision", "Vehicle Theft", "Parked Car"],
    )
    number_of_vehicles_involved = st.slider("Vehicles Involved", 1, 4, 1)
    bodily_injuries_label = st.select_slider(
        "Reported Injuries",
        options=["None", "One reported injury", "Multiple / serious injuries"],
        value="None",
    )
    bodily_injuries = bodily_injuries_label_to_value(bodily_injuries_label)
    witnesses_label = st.select_slider(
        "Witnesses Present",
        options=["No witnesses", "One witness", "Two witnesses", "Three or more witnesses"],
        value="One witness",
    )
    witnesses = witnesses_label_to_value(witnesses_label)
    months_as_customer = st.number_input("Months as Customer", min_value=0, value=200)

with right:
    render_html("""
<div class="card">
  <div class="section-label">02 · Policy & Claim Amount</div>
  <div class="heading">Claim Financial Profile</div>
  <div class="note">Enter the claim amount, sub-claims, premium, and deductible used by the model.</div>
  <div class="divider"></div>
</div>
""")

    total_claim_amount    = st.number_input("Total Claim Amount ($)", min_value=0, value=50000)
    injury_claim          = st.number_input("Injury Claim ($)", min_value=0, value=5000)
    property_claim        = st.number_input("Property Claim ($)", min_value=0, value=10000)
    vehicle_claim         = st.number_input("Vehicle Claim ($)", min_value=0, value=35000)
    policy_annual_premium = st.number_input("Annual Premium ($)", min_value=0.0, value=1200.0, step=10.0)
    policy_deductable     = st.number_input("Policy Deductible ($)", min_value=0, value=1000)

predict = st.button("Run claim risk assessment →")

# ── RESULTS ──────────────────────────────────────────────────────────────────
if predict:
    # ── Replace with real model call ──────────────────────────────────────
    # input_data = template_row.copy()
    # input_data.loc[:, "incident_severity"] = incident_severity
    # ...
    # fraud_prob = model.predict_proba(input_data)[0, 1]
    import random
    fraud_prob = random.uniform(0.05, 0.95)   # DEMO — remove when real model is wired
    # ─────────────────────────────────────────────────────────────────────

    fraud_pred = int(fraud_prob >= THRESHOLD)
    risk_cls, risk_label, badge_cls, text_cls, risk_color = risk_meta(fraud_prob)
    action_title, action_desc = action_meta(fraud_prob)

    pct         = round(fraud_prob * 100, 1)
    verdict     = "Likely Fraudulent" if fraud_pred == 1 else "Likely Legitimate"
    marker_left = min(max(pct, 2), 97)

    st.markdown("<br>", unsafe_allow_html=True)
    result_col, action_col = st.columns(2, gap="large")

    # Determine verdict icon
    verdict_icon = "⬆" if fraud_pred == 1 else "✓"

    with result_col:
        render_html(f"""
<div class="card">
  <div class="section-label">03 · Model Output</div>
  <div class="heading">Fraud Probability Score</div>
  <div class="note">Estimated likelihood this claim matches a fraud-risk pattern.</div>

  <div class="score {text_cls}" style="margin-top:1.2rem;">{pct:.0f}<span style="font-size:2.4rem; opacity:0.6;">%</span></div>

  <div class="progress-wrap">
    <div class="progress-fill" style="width:{pct}%; background:{risk_color}; color:{risk_color};"></div>
  </div>

  <div class="gauge-wrap">
    <div class="gauge-track">
      <div class="gauge-marker" style="left:{marker_left}%;"></div>
    </div>
    <div class="gauge-labels">
      <span>0% · Low</span>
      <span>25% · Review</span>
      <span>50% · High</span>
      <span>100%</span>
    </div>
  </div>

  <div style="margin-top:1.2rem;">
    <div class="metric-row">
      <span class="metric-k">decision threshold</span>
      <span class="metric-v">{int(THRESHOLD * 100)}%</span>
    </div>
    <div class="metric-row">
      <span class="metric-k">prediction</span>
      <span class="metric-v" style="color:{risk_color};">{esc(verdict)}</span>
    </div>
    <div class="metric-row">
      <span class="metric-k">confidence delta</span>
      <span class="metric-v">{abs(pct - THRESHOLD*100):.1f}pp from threshold</span>
    </div>
  </div>

  <div style="margin-top:1.1rem;">
    <span class="badge {badge_cls}">
      <span style="width:7px;height:7px;border-radius:50%;background:currentColor;display:inline-block;box-shadow:0 0 6px currentColor;"></span>
      {esc(risk_label)}
    </span>
  </div>
</div>
""")

    with action_col:
        # Pick icon based on routing
        routing_icons = {
            "Send for Manual Investigation": "⚑",
            "Flag for Secondary Review": "◈",
            "Process Normally": "✓",
        }
        r_icon = routing_icons.get(action_title, "→")

        render_html(f"""
<div class="card">
  <div class="section-label">04 · Claim Routing</div>
  <div class="heading">Recommended Handling</div>
  <div class="note">The output supports triage and does not replace professional investigation.</div>

  <div style="
    margin-top:1.3rem;
    background: rgba(250,204,21,0.06);
    border: 1px solid rgba(250,204,21,0.18);
    border-radius: 18px;
    padding: 1.2rem 1.3rem;
    position: relative;
    overflow: hidden;
  ">
    <div style="
      position:absolute; top:-24px; right:-18px;
      font-size: 5rem;
      opacity: 0.06;
      font-weight: 900;
      line-height:1;
      user-select:none;
    ">{r_icon}</div>
    <div style="font-size:1.15rem; font-weight:800; color:#fde68a; margin-bottom:0.5rem;">{esc(action_title)}</div>
    <div style="color:rgba(203,213,225,0.80); line-height:1.70; font-size:0.91rem;">{esc(action_desc)}</div>
  </div>

  <div style="margin-top:1.2rem;">
    <div class="metric-row">
      <span class="metric-k">model</span>
      <span class="metric-v">Random Forest</span>
    </div>
    <div class="metric-row">
      <span class="metric-k">features</span>
      <span class="metric-v">12 deployment inputs</span>
    </div>
    <div class="metric-row">
      <span class="metric-k">use case</span>
      <span class="metric-v">Claim triage</span>
    </div>
    <div class="metric-row">
      <span class="metric-k">incident type</span>
      <span class="metric-v">{esc(incident_type)}</span>
    </div>
    <div class="metric-row">
      <span class="metric-k">total claimed</span>
      <span class="metric-v">${total_claim_amount:,}</span>
    </div>
  </div>
</div>
""")

    # ── RISK DRIVERS ──────────────────────────────────────────────────────
    risk_drivers = []
    if incident_severity in ["Major Damage", "Total Loss"]:
        risk_drivers.append(("🚗", "Severe vehicle damage",
            "Major damage or total loss can increase the need for manual claim review."))
    if total_claim_amount >= 60000:
        risk_drivers.append(("💰", "Large claim amount",
            f"The total claim of ${total_claim_amount:,} is above the $60,000 high-value threshold."))
    if number_of_vehicles_involved >= 2:
        risk_drivers.append(("🔗", "Multi-vehicle incident",
            "Multi-vehicle incidents are more complex and may require additional validation."))
    if bodily_injuries >= 1:
        risk_drivers.append(("⚕", "Injury component present",
            "Bodily injury claims often require more supporting documentation."))
    if witnesses >= 2:
        risk_drivers.append(("👁", "Multiple witnesses",
            f"{witnesses} witnesses present — this can affect investigation priority."))
    if months_as_customer < 24:
        risk_drivers.append(("📋", "Short customer history",
            f"Only {months_as_customer} months as a customer — a mild but notable review signal."))

    if not risk_drivers:
        drivers_html = """
<div class="driver">
  <div class="driver-icon">✓</div>
  <div>
    <div class="driver-title">No major review triggers</div>
    <div class="driver-desc">The entered values did not activate the main rule-based risk signals.</div>
  </div>
</div>
"""
    else:
        drivers_html = ""
        for icon, title, desc in risk_drivers:
            drivers_html += f"""
<div class="driver">
  <div class="driver-icon">{icon}</div>
  <div>
    <div class="driver-title">{esc(title)}</div>
    <div class="driver-desc">{esc(desc)}</div>
  </div>
</div>
"""

    render_html(f"""
<div class="card">
  <div class="section-label">05 · Review Signals</div>
  <div class="heading">Key Factors Behind the Recommendation</div>
  <div class="note">These notes explain which entered values influenced the routing decision.</div>
  <div class="divider"></div>
  {drivers_html}
</div>
""")

render_html("""
<p class="footer-note">
  Portfolio demonstration · Supports claim triage and human review — not automatic denial or approval.
</p>
""")