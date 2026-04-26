import streamlit as st
import pandas as pd
import joblib

# ── Load model ──────────────────────────────────────────────────────────────
model        = joblib.load("deploy_fraud_model.pkl")
template_row = joblib.load("deploy_input_template.pkl")
THRESHOLD    = 0.25

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Insurance Fraud Detection",
    page_icon="◎",
    layout="wide",
)

# ── MASTER CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,700;0,9..144,900;1,9..144,400&family=JetBrains+Mono:wght@400;500&display=swap');

/* ══════════════════════════════════════════════
   GLOBAL
══════════════════════════════════════════════ */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #1a1a2e !important;
}

.stApp {
    background: linear-gradient(145deg,
        #e8f4fd 0%,
        #f0e8ff 25%,
        #fce4ec 50%,
        #e8f5e9 75%,
        #fff8e1 100%);
    background-attachment: fixed;
    min-height: 100vh;
}

/* Subtle animated mesh overlay */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 60% 50% at 20% 20%, rgba(167,139,250,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 50% 60% at 80% 70%, rgba(96,165,250,0.10) 0%, transparent 60%),
        radial-gradient(ellipse 40% 40% at 60% 10%, rgba(251,191,36,0.08) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
    animation: meshShift 18s ease-in-out infinite alternate;
}

@keyframes meshShift {
    0%   { opacity: 0.7; transform: scale(1); }
    100% { opacity: 1;   transform: scale(1.04); }
}

.main .block-container {
    padding: 3rem 3rem 6rem;
    max-width: 1200px;
    position: relative;
    z-index: 1;
}

/* ══════════════════════════════════════════════
   ANIMATIONS
══════════════════════════════════════════════ */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes slideRight {
    from { opacity: 0; transform: translateX(-20px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes popIn {
    0%   { opacity: 0; transform: scale(0.88); }
    70%  { transform: scale(1.03); }
    100% { opacity: 1; transform: scale(1); }
}
@keyframes barFill {
    from { width: 0%; }
    to   { width: var(--bar-w); }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position:  200% center; }
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-4px); }
}

/* ══════════════════════════════════════════════
   HEADER
══════════════════════════════════════════════ */
.hdr-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #7c6fcd;
    margin: 0 0 0.7rem;
    animation: fadeUp 0.5s ease both;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.hdr-tag::before {
    content: '';
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #7c6fcd;
    animation: float 2.5s ease-in-out infinite;
}

.hdr-title {
    font-family: 'Fraunces', Georgia, serif;
    font-size: clamp(2.4rem, 4.5vw, 3.6rem);
    font-weight: 900;
    color: #1a1a2e;
    line-height: 1.05;
    margin: 0 0 0.6rem;
    letter-spacing: -1.5px;
    animation: fadeUp 0.55s 0.07s ease both;
}

.hdr-sub {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.9rem;
    font-weight: 300;
    color: #64748b;
    margin: 0 0 2.8rem;
    animation: fadeUp 0.55s 0.14s ease both;
    letter-spacing: 0.01em;
}

.hdr-divider {
    height: 2px;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #fb7185, transparent);
    border-radius: 1px;
    margin-bottom: 0.8rem;
    animation: fadeIn 0.8s 0.2s ease both;
}

/* ══════════════════════════════════════════════
   GLASS CARD — the core component
══════════════════════════════════════════════ */
.glass-panel {
    background: rgba(255, 255, 255, 0.52);
    backdrop-filter: blur(22px) saturate(160%);
    -webkit-backdrop-filter: blur(22px) saturate(160%);
    border: 1.5px solid rgba(255, 255, 255, 0.75);
    border-radius: 20px;
    padding: 1.8rem 2rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow:
        0 4px 24px rgba(124, 111, 205, 0.08),
        0 1px 0 rgba(255,255,255,0.9) inset,
        0 -1px 0 rgba(0,0,0,0.03) inset;
    animation: fadeUp 0.5s 0.2s ease both;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
}
.glass-panel:hover {
    box-shadow:
        0 10px 40px rgba(124, 111, 205, 0.14),
        0 1px 0 rgba(255,255,255,0.9) inset;
    transform: translateY(-2px);
}

.panel-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.64rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #94a3b8;
    margin: 0 0 1.3rem;
    padding-bottom: 0.7rem;
    border-bottom: 1px solid rgba(148, 163, 184, 0.2);
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.panel-title-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    display: inline-block;
    flex-shrink: 0;
}

/* ══════════════════════════════════════════════
   STREAMLIT WIDGET OVERRIDES — HIGH CONTRAST
══════════════════════════════════════════════ */

/* ALL labels — dark, readable */
label,
.stSelectbox > label,
.stNumberInput > label,
.stSlider > label,
.stSelectSlider > label,
div[data-testid="stWidgetLabel"] > label,
div[data-testid="stWidgetLabel"] p {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    color: #374151 !important;
    letter-spacing: 0.01em !important;
    text-transform: none !important;
    margin-bottom: 0.2rem !important;
}

/* Selectbox container */
div[data-baseweb="select"] {
    border-radius: 12px !important;
}
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.88) !important;
    border: 2px solid rgba(148,163,184,0.45) !important;
    border-radius: 12px !important;
    color: #1a1a2e !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    min-height: 46px !important;
    padding-left: 14px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    cursor: pointer !important;
}
div[data-baseweb="select"] > div:hover {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.15) !important;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: #7c6fcd !important;
    box-shadow: 0 0 0 3px rgba(124,111,205,0.2) !important;
}

/* Dropdown chevron — make it visible */
div[data-baseweb="select"] svg {
    color: #7c6fcd !important;
    opacity: 1 !important;
    width: 18px !important;
    height: 18px !important;
}

/* Selected text value inside select */
div[data-baseweb="select"] [data-testid="stMarkdownContainer"] p,
div[data-baseweb="select"] span,
div[data-baseweb="select"] div {
    color: #1a1a2e !important;
    font-weight: 500 !important;
}

/* Dropdown menu options */
[data-baseweb="menu"] {
    background: rgba(255,255,255,0.97) !important;
    border: 1.5px solid rgba(167,139,250,0.3) !important;
    border-radius: 12px !important;
    box-shadow: 0 16px 40px rgba(0,0,0,0.12) !important;
    backdrop-filter: blur(20px) !important;
}
[data-baseweb="option"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.88rem !important;
    color: #1a1a2e !important;
    padding: 10px 16px !important;
    transition: background 0.15s !important;
}
[data-baseweb="option"]:hover,
[data-baseweb="option"][aria-selected="true"] {
    background: rgba(167,139,250,0.15) !important;
    color: #5b21b6 !important;
}

/* Number inputs */
[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.88) !important;
    border: 2px solid rgba(148,163,184,0.45) !important;
    border-radius: 12px !important;
    color: #1a1a2e !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    height: 46px !important;
    padding-left: 14px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: #7c6fcd !important;
    box-shadow: 0 0 0 3px rgba(124,111,205,0.2) !important;
    outline: none !important;
}
[data-testid="stNumberInput"] input::placeholder {
    color: #94a3b8 !important;
}
[data-testid="stNumberInput"] button {
    background: rgba(255,255,255,0.7) !important;
    border: 1.5px solid rgba(148,163,184,0.3) !important;
    color: #7c6fcd !important;
    border-radius: 8px !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
}
[data-testid="stNumberInput"] button:hover {
    background: rgba(167,139,250,0.2) !important;
    border-color: #a78bfa !important;
}

/* Sliders */
[data-testid="stSlider"] [role="slider"] {
    background: #7c6fcd !important;
    border: 2px solid white !important;
    box-shadow: 0 2px 8px rgba(124,111,205,0.4) !important;
}
[data-testid="stSlider"] [data-testid="stTickBarMin"],
[data-testid="stSlider"] [data-testid="stTickBarMax"] {
    color: #94a3b8 !important;
    font-size: 0.75rem !important;
}

/* Select slider */
[data-testid="stSelectSlider"] [role="slider"] {
    background: #7c6fcd !important;
    border: 2px solid white !important;
    box-shadow: 0 2px 8px rgba(124,111,205,0.4) !important;
}
[data-testid="stSelectSlider"] p {
    color: #374151 !important;
    font-size: 0.8rem !important;
}

/* ══════════════════════════════════════════════
   CTA BUTTON
══════════════════════════════════════════════ */
div.stButton > button {
    background: linear-gradient(135deg, #7c6fcd 0%, #a78bfa 50%, #60a5fa 100%) !important;
    background-size: 200% 200% !important;
    color: #fff !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    padding: 0.75rem 2.8rem !important;
    margin-top: 0.6rem !important;
    box-shadow: 0 4px 20px rgba(124,111,205,0.35) !important;
    transition: transform 0.18s, box-shadow 0.18s, background-position 0.4s !important;
    cursor: pointer !important;
    animation: fadeIn 0.5s 0.35s ease both !important;
}
div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 32px rgba(124,111,205,0.45) !important;
    background-position: right center !important;
}
div.stButton > button:active {
    transform: translateY(0) scale(0.98) !important;
}

/* ══════════════════════════════════════════════
   RESULT COMPONENTS
══════════════════════════════════════════════ */

/* Big score card */
.score-card {
    background: rgba(255,255,255,0.6);
    backdrop-filter: blur(24px) saturate(160%);
    -webkit-backdrop-filter: blur(24px) saturate(160%);
    border: 1.5px solid rgba(255,255,255,0.8);
    border-radius: 22px;
    padding: 2.2rem 2.4rem 2rem;
    box-shadow: 0 8px 40px rgba(0,0,0,0.08), 0 1px 0 rgba(255,255,255,0.95) inset;
    position: relative;
    overflow: hidden;
    animation: popIn 0.6s cubic-bezier(0.22,1,0.36,1) both;
}

.score-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    border-radius: 22px 22px 0 0;
}
.score-card.low::before    { background: linear-gradient(90deg, #34d399, #6ee7b7); }
.score-card.medium::before { background: linear-gradient(90deg, #fbbf24, #fde68a); }
.score-card.high::before   { background: linear-gradient(90deg, #f87171, #fca5a5); }

.score-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #94a3b8;
    margin: 0 0 0.5rem;
}

.score-number {
    font-family: 'Fraunces', serif;
    font-size: 6rem;
    font-weight: 900;
    line-height: 1;
    margin: 0;
    letter-spacing: -3px;
    animation: popIn 0.65s 0.1s cubic-bezier(0.22,1,0.36,1) both;
}
.score-number.low    { color: #059669; }
.score-number.medium { color: #d97706; }
.score-number.high   { color: #dc2626; }

/* Animated progress bar */
.prog-track {
    width: 100%;
    height: 6px;
    background: rgba(148,163,184,0.18);
    border-radius: 3px;
    margin: 1.1rem 0 0.4rem;
    overflow: hidden;
}
.prog-fill {
    height: 100%;
    border-radius: 3px;
    animation: progAnim 1.2s cubic-bezier(0.22,1,0.36,1) both;
    animation-delay: 0.15s;
}
.prog-fill.low    { background: linear-gradient(90deg, #34d399, #6ee7b7); }
.prog-fill.medium { background: linear-gradient(90deg, #fbbf24, #fde68a); }
.prog-fill.high   { background: linear-gradient(90deg, #f87171, #fca5a5); }

@keyframes progAnim {
    from { width: 0%; }
}

.prog-labels {
    display: flex;
    justify-content: space-between;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: #94a3b8;
    letter-spacing: 0.06em;
    margin-bottom: 0.9rem;
}

.score-verdict {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #1a1a2e;
    margin: 0 0 0.6rem;
}

/* Risk badge */
.risk-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.3rem 0.9rem;
    border-radius: 999px;
    letter-spacing: 0.03em;
}
.risk-badge::before {
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    flex-shrink: 0;
}
.badge-low    { color: #065f46; background: #d1fae5; }
.badge-low::before    { background: #059669; }
.badge-medium { color: #92400e; background: #fef3c7; }
.badge-medium::before { background: #d97706; }
.badge-high   { color: #991b1b; background: #fee2e2; }
.badge-high::before   { background: #dc2626; }

/* Action card */
.action-card {
    background: rgba(255,255,255,0.6);
    backdrop-filter: blur(24px) saturate(160%);
    -webkit-backdrop-filter: blur(24px) saturate(160%);
    border: 1.5px solid rgba(255,255,255,0.8);
    border-radius: 22px;
    padding: 2.2rem 2.2rem;
    box-shadow: 0 8px 40px rgba(0,0,0,0.08), 0 1px 0 rgba(255,255,255,0.95) inset;
    animation: popIn 0.6s 0.1s cubic-bezier(0.22,1,0.36,1) both;
    height: 100%;
    box-sizing: border-box;
}

.action-chip {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.22rem 0.7rem;
    border-radius: 6px;
    margin-bottom: 0.9rem;
}
.chip-low    { background: #d1fae5; color: #065f46; }
.chip-medium { background: #fef3c7; color: #92400e; }
.chip-high   { background: #fee2e2; color: #991b1b; }

.action-headline {
    font-family: 'Fraunces', serif;
    font-size: 1.55rem;
    font-weight: 700;
    color: #1a1a2e;
    line-height: 1.2;
    margin: 0 0 0.9rem;
}

.action-desc {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.88rem;
    font-weight: 400;
    color: #4b5563;
    line-height: 1.75;
    margin: 0;
}

/* ══════════════════════════════════════════════
   CHART & DRIVERS
══════════════════════════════════════════════ */
.chart-glass {
    background: rgba(255,255,255,0.6);
    backdrop-filter: blur(22px) saturate(150%);
    -webkit-backdrop-filter: blur(22px) saturate(150%);
    border: 1.5px solid rgba(255,255,255,0.8);
    border-radius: 20px;
    padding: 1.8rem 2rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06), 0 1px 0 rgba(255,255,255,0.9) inset;
    animation: fadeUp 0.5s 0.25s ease both;
}

.drivers-glass {
    background: rgba(255,255,255,0.6);
    backdrop-filter: blur(22px) saturate(150%);
    -webkit-backdrop-filter: blur(22px) saturate(150%);
    border: 1.5px solid rgba(255,255,255,0.8);
    border-radius: 20px;
    padding: 1.8rem 2rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06), 0 1px 0 rgba(255,255,255,0.9) inset;
    animation: fadeUp 0.5s 0.3s ease both;
}

.driver-item {
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
    padding: 0.75rem 0;
    border-bottom: 1px solid rgba(148,163,184,0.12);
    animation: slideRight 0.4s ease both;
}
.driver-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: linear-gradient(135deg, #a78bfa, #7c6fcd);
    flex-shrink: 0;
    margin-top: 0.42rem;
    box-shadow: 0 0 6px rgba(167,139,250,0.5);
}
.driver-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
    color: #1a1a2e;
    margin-bottom: 0.15rem;
}
.driver-desc {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.78rem;
    color: #64748b;
    line-height: 1.5;
}

.minfo {
    margin-top: 1.4rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(148,163,184,0.15);
}
.minfo-row {
    display: flex;
    justify-content: space-between;
    padding: 0.3rem 0;
    border-bottom: 1px solid rgba(148,163,184,0.08);
}
.minfo-k {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #94a3b8;
    letter-spacing: 0.04em;
}
.minfo-v {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.8rem;
    font-weight: 500;
    color: #374151;
}

.section-sep {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(148,163,184,0.25), transparent);
    margin: 2rem 0;
    animation: fadeIn 0.5s ease both;
}

.sec-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #94a3b8;
    margin: 0 0 1.2rem;
    animation: fadeUp 0.4s ease both;
}

.footer-note {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    color: #94a3b8;
    text-align: center;
    margin-top: 3rem;
    padding-top: 1.2rem;
    border-top: 1px solid rgba(148,163,184,0.15);
    animation: fadeIn 0.5s 0.4s ease both;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers (LOGIC UNCHANGED) ─────────────────────────────────────────────────
def bodily_injuries_label_to_value(label):
    return {"None": 0, "One reported injury": 1, "Multiple / serious injuries": 2}[label]

def witnesses_label_to_value(label):
    return {"No witnesses": 0, "One witness": 1, "Two witnesses": 2, "Three or more witnesses": 3}[label]

def risk_meta(fraud_prob):
    if fraud_prob < 0.25:
        return "low",    "Low Risk",    "badge-low",    "chip-low"
    elif fraud_prob < 0.50:
        return "medium", "Medium Risk", "badge-medium", "chip-medium"
    return "high",   "High Risk",   "badge-high",   "chip-high"

def action_meta(fraud_prob):
    if fraud_prob >= 0.50:
        return "high",   "Send for Manual Investigation", \
               "The model score exceeds 50%. This claim requires a full investigator review before any payout is processed. Do not proceed automatically."
    elif fraud_prob >= THRESHOLD:
        return "medium", "Flag for Secondary Review", \
               "The score is above the decision threshold. Route for a supervisor spot-check and request additional documentation before proceeding."
    return "low",    "Process Normally", \
           "No elevated risk signals detected. This claim may proceed through the standard workflow without additional review steps."


# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hdr-tag">ML Risk Scoring &nbsp;·&nbsp; Portfolio Project</div>
<h1 class="hdr-title">Insurance Fraud<br>Detection</h1>
<div class="hdr-divider"></div>
<p class="hdr-sub">Random Forest classifier &nbsp;·&nbsp; threshold-tuned for recall &nbsp;·&nbsp; 12-feature deployment model</p>
""", unsafe_allow_html=True)


# ── INPUTS ────────────────────────────────────────────────────────────────────
col_l, col_r = st.columns([1, 1], gap="large")

with col_l:
    st.markdown("""
    <div class="glass-panel">
      <div class="panel-title">
        <span class="panel-title-dot" style="background:linear-gradient(135deg,#a78bfa,#7c6fcd);"></span>
        01 &nbsp; Incident Details
      </div>
    </div>
    """, unsafe_allow_html=True)

    incident_severity = st.selectbox(
        "Incident Severity",
        ["Minor Damage", "Major Damage", "Total Loss", "Trivial Damage"],
        help="Select the severity level of the reported incident"
    )
    incident_type = st.selectbox(
        "Incident Type",
        ["Single Vehicle Collision", "Multi-vehicle Collision", "Vehicle Theft", "Parked Car"],
        help="Select the type of incident that occurred"
    )
    number_of_vehicles_involved = st.slider(
        "Vehicles Involved", min_value=1, max_value=4, value=1
    )
    bodily_injuries_label = st.select_slider(
        "Reported Injuries",
        options=["None", "One reported injury", "Multiple / serious injuries"],
        value="None"
    )
    bodily_injuries = bodily_injuries_label_to_value(bodily_injuries_label)
    witnesses_label = st.select_slider(
        "Witnesses Present",
        options=["No witnesses", "One witness", "Two witnesses", "Three or more witnesses"],
        value="One witness"
    )
    witnesses = witnesses_label_to_value(witnesses_label)
    months_as_customer = st.number_input(
        "Months as Customer", min_value=0, value=200,
        help="How long has this policy holder been a customer?"
    )

with col_r:
    st.markdown("""
    <div class="glass-panel">
      <div class="panel-title">
        <span class="panel-title-dot" style="background:linear-gradient(135deg,#60a5fa,#38bdf8);"></span>
        02 &nbsp; Claim & Policy Details
      </div>
    </div>
    """, unsafe_allow_html=True)

    total_claim_amount    = st.number_input("Total Claim Amount ($)",  min_value=0,   value=50000)
    injury_claim          = st.number_input("Injury Claim ($)",        min_value=0,   value=5000)
    property_claim        = st.number_input("Property Claim ($)",      min_value=0,   value=10000)
    vehicle_claim         = st.number_input("Vehicle Claim ($)",       min_value=0,   value=35000)
    policy_annual_premium = st.number_input("Annual Premium ($)",      min_value=0.0, value=1200.0, step=10.0)
    policy_deductable     = st.number_input("Policy Deductable ($)",   min_value=0,   value=1000)

predict = st.button("◎  Run Fraud Assessment")


# ── PREDICTION (LOGIC UNCHANGED) ─────────────────────────────────────────────
if predict:
    input_data = template_row.copy()
    input_data.loc[:, "incident_severity"]           = incident_severity
    input_data.loc[:, "incident_type"]               = incident_type
    input_data.loc[:, "number_of_vehicles_involved"] = number_of_vehicles_involved
    input_data.loc[:, "bodily_injuries"]             = bodily_injuries
    input_data.loc[:, "witnesses"]                   = witnesses
    input_data.loc[:, "months_as_customer"]          = months_as_customer
    input_data.loc[:, "total_claim_amount"]          = total_claim_amount
    input_data.loc[:, "injury_claim"]                = injury_claim
    input_data.loc[:, "property_claim"]              = property_claim
    input_data.loc[:, "vehicle_claim"]               = vehicle_claim
    input_data.loc[:, "policy_annual_premium"]       = policy_annual_premium
    input_data.loc[:, "policy_deductable"]           = policy_deductable

    fraud_prob = model.predict_proba(input_data)[0, 1]
    fraud_pred = int(fraud_prob >= THRESHOLD)

    risk_cls, risk_label, badge_cls, chip_cls = risk_meta(fraud_prob)
    action_cls, action_hl, action_d           = action_meta(fraud_prob)
    verdict   = "Likely Fraudulent" if fraud_pred == 1 else "Likely Legitimate"
    pct       = round(fraud_prob * 100, 1)
    bar_colors = {
        "low":    "linear-gradient(90deg, #34d399, #6ee7b7)",
        "medium": "linear-gradient(90deg, #fbbf24, #fde68a)",
        "high":   "linear-gradient(90deg, #f87171, #fca5a5)",
    }
    bar_gradient = bar_colors[risk_cls]

    # ── Section 03: Results
    st.markdown('<div class="section-sep"></div>', unsafe_allow_html=True)
    st.markdown('<p class="sec-header">03 &nbsp; Model Output</p>', unsafe_allow_html=True)

    res_col, act_col = st.columns([1, 1], gap="large")

    with res_col:
        st.markdown(f"""
        <div class="score-card {risk_cls}">
            <p class="score-eyebrow">Fraud Probability Score</p>
            <p class="score-number {risk_cls}">{pct:.0f}%</p>

            <div class="prog-track">
                <div class="prog-fill {risk_cls}" style="width:{pct}%;"></div>
            </div>
            <div class="prog-labels">
                <span>0%</span>
                <span>Threshold {int(THRESHOLD*100)}%</span>
                <span>100%</span>
            </div>

            <p class="score-verdict">{verdict}</p>
            <span class="risk-badge {badge_cls}">{risk_label}</span>
        </div>
        """, unsafe_allow_html=True)

    with act_col:
        st.markdown(f"""
        <div class="action-card">
            <span class="action-chip {chip_cls}">Recommended Action</span>
            <p class="action-headline">{action_hl}</p>
            <p class="action-desc">{action_d}</p>
        </div>
        """, unsafe_allow_html=True)

    # ── Section 04: Charts + Drivers
    st.markdown('<div class="section-sep"></div>', unsafe_allow_html=True)
    st.markdown('<p class="sec-header">04 &nbsp; Claim Analysis & Risk Drivers</p>', unsafe_allow_html=True)

    ch_col, dr_col = st.columns([1.2, 0.8], gap="large")
    other = max(0, total_claim_amount - injury_claim - property_claim - vehicle_claim)

    with ch_col:
        score_color = {
            "low":    "#34d399",
            "medium": "#fbbf24",
            "high":   "#f87171",
        }[risk_cls]

        chart_html = f"""
<style>
  body {{ margin:0; padding:0; }}
  .cl {{ font-family:'JetBrains Mono',monospace; font-size:0.62rem;
         letter-spacing:0.18em; text-transform:uppercase; color:#94a3b8;
         margin:0 0 0.8rem; }}
  .legend {{ display:flex; flex-wrap:wrap; gap:12px; margin:0.7rem 0 1.5rem;
             font-family:'Plus Jakarta Sans',sans-serif; font-size:11px; color:#64748b; }}
  .leg-item {{ display:flex; align-items:center; gap:5px; }}
  .leg-dot  {{ width:9px; height:9px; border-radius:50%; flex-shrink:0; }}
</style>

<p class="cl">Claim Composition</p>
<div style="position:relative;width:100%;height:200px;">
  <canvas id="claimChart" role="img"
    aria-label="Bar chart: Injury ${injury_claim:,}, Property ${property_claim:,}, Vehicle ${vehicle_claim:,}, Other ${other:,}">
    Injury ${injury_claim:,} · Property ${property_claim:,} · Vehicle ${vehicle_claim:,} · Other ${other:,}
  </canvas>
</div>

<div class="legend">
  <div class="leg-item"><div class="leg-dot" style="background:#fb7185;"></div>Injury</div>
  <div class="leg-item"><div class="leg-dot" style="background:#fbbf24;"></div>Property</div>
  <div class="leg-item"><div class="leg-dot" style="background:#60a5fa;"></div>Vehicle</div>
  <div class="leg-item"><div class="leg-dot" style="background:#cbd5e1;"></div>Other</div>
</div>

<p class="cl">Score vs Threshold</p>
<div style="position:relative;width:100%;height:72px;">
  <canvas id="gaugeChart" role="img"
    aria-label="Horizontal bar: score {pct:.0f}% vs threshold {int(THRESHOLD*100)}%">
    Score {pct:.0f}% · Threshold {int(THRESHOLD*100)}%
  </canvas>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<script>
(function() {{
  const T = {{ color:'#94a3b8', font:{{ family:"'Plus Jakarta Sans',sans-serif", size:11 }} }};
  const G = {{ color:'rgba(148,163,184,0.15)' }};

  new Chart(document.getElementById('claimChart'), {{
    type: 'bar',
    data: {{
      labels: ['Injury', 'Property', 'Vehicle', 'Other'],
      datasets: [{{
        data: [{injury_claim}, {property_claim}, {vehicle_claim}, {other}],
        backgroundColor: ['rgba(251,113,133,0.75)','rgba(251,191,36,0.75)','rgba(96,165,250,0.75)','rgba(203,213,225,0.6)'],
        borderColor:     ['#fb7185','#fbbf24','#60a5fa','#cbd5e1'],
        borderWidth: 1.5,
        borderRadius: 8,
        borderSkipped: false,
      }}]
    }},
    options: {{
      responsive: true, maintainAspectRatio: false,
      animation: {{
        duration: 900,
        easing: 'easeOutQuart',
        delay: (ctx) => ctx.dataIndex * 110,
      }},
      plugins: {{
        legend: {{ display: false }},
        tooltip: {{
          backgroundColor: 'rgba(26,26,46,0.92)',
          titleColor: '#94a3b8',
          bodyColor: '#f1f5f9',
          titleFont: {{ family:"'JetBrains Mono',monospace", size:11 }},
          bodyFont:  {{ family:"'Plus Jakarta Sans',sans-serif", size:12 }},
          padding: 12,
          cornerRadius: 10,
          callbacks: {{ label: (c) => '  $' + c.raw.toLocaleString() }}
        }}
      }},
      scales: {{
        x: {{ grid: {{ display:false }}, ticks: T, border: {{ display:false }} }},
        y: {{ grid: G, ticks: {{ ...T, callback:(v) => '$'+v.toLocaleString() }}, border: {{ display:false }} }}
      }}
    }}
  }});

  new Chart(document.getElementById('gaugeChart'), {{
    type: 'bar',
    data: {{
      labels: ['Model score', 'Threshold'],
      datasets: [{{
        data: [{pct:.1f}, {round(THRESHOLD*100,1)}],
        backgroundColor: ['{score_color}88', 'rgba(203,213,225,0.5)'],
        borderColor:     ['{score_color}', '#cbd5e1'],
        borderWidth: 1.5,
        borderRadius: 6,
        borderSkipped: false,
      }}]
    }},
    options: {{
      indexAxis: 'y', responsive: true, maintainAspectRatio: false,
      animation: {{ duration: 1100, easing: 'easeOutExpo', delay: (ctx) => ctx.dataIndex * 200 }},
      plugins: {{
        legend: {{ display: false }},
        tooltip: {{
          backgroundColor: 'rgba(26,26,46,0.92)',
          titleColor: '#94a3b8', bodyColor: '#f1f5f9',
          titleFont: {{ family:"'JetBrains Mono',monospace", size:11 }},
          bodyFont:  {{ family:"'Plus Jakarta Sans',sans-serif", size:12 }},
          padding: 12, cornerRadius: 10,
          callbacks: {{ label: (c) => '  ' + c.raw + '%' }}
        }}
      }},
      scales: {{
        x: {{ max: 100, grid: G, ticks: {{ ...T, callback:(v) => v+'%' }}, border: {{ display:false }} }},
        y: {{ grid: {{ display:false }}, ticks: T, border: {{ display:false }} }}
      }}
    }}
  }});
}})();
</script>
"""
        st.markdown('<div class="chart-glass">', unsafe_allow_html=True)
        st.components.v1.html(chart_html, height=420)
        st.markdown('</div>', unsafe_allow_html=True)

    with dr_col:
        st.markdown('<div class="drivers-glass">', unsafe_allow_html=True)
        st.markdown('<p class="panel-title" style="margin-bottom:1.1rem;"><span class="panel-title-dot" style="background:linear-gradient(135deg,#a78bfa,#7c6fcd);width:7px;height:7px;border-radius:50%;display:inline-block;margin-right:0.5rem;"></span>Risk Drivers</p>', unsafe_allow_html=True)

        risk_drivers = []
        if incident_severity in ["Major Damage", "Total Loss"]:
            risk_drivers.append(("High incident severity", "Strongly associated with elevated fraud risk across the training set."))
        if total_claim_amount >= 60000:
            risk_drivers.append(("Large total claim", "Amount exceeds the high-risk threshold of $60,000."))
        if number_of_vehicles_involved >= 2:
            risk_drivers.append(("Multiple vehicles", "Complex multi-vehicle incidents show higher fraud rates."))
        if bodily_injuries >= 1:
            risk_drivers.append(("Reported bodily injuries", "Injury claims are correlated with higher fraud incidence."))
        if witnesses >= 2:
            risk_drivers.append(("High witness count", "An unusually high number of witnesses may indicate staging."))
        if months_as_customer < 24:
            risk_drivers.append(("Short customer tenure", "Policy age under 24 months is a mild risk signal."))

        if not risk_drivers:
            st.markdown("""
            <div class="driver-item" style="border-bottom:none;">
                <div class="driver-dot" style="background:#34d399; box-shadow:0 0 6px rgba(52,211,153,0.5);"></div>
                <div>
                    <div class="driver-title" style="color:#059669;">No major risk indicators</div>
                    <div class="driver-desc">No high-risk triggers detected from the entered values.</div>
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            for i, (title, desc) in enumerate(risk_drivers):
                st.markdown(f"""
                <div class="driver-item" style="animation-delay:{i*0.07}s;">
                    <div class="driver-dot"></div>
                    <div>
                        <div class="driver-title">{title}</div>
                        <div class="driver-desc">{desc}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="minfo">
            <div class="minfo-row"><span class="minfo-k">Model</span><span class="minfo-v">Random Forest</span></div>
            <div class="minfo-row"><span class="minfo-k">Tuning</span><span class="minfo-v">Threshold → recall</span></div>
            <div class="minfo-row"><span class="minfo-k">Features</span><span class="minfo-v">12 inputs (reduced)</span></div>
            <div class="minfo-row" style="border-bottom:none;"><span class="minfo-k">Purpose</span><span class="minfo-v">Portfolio demo</span></div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <p class="footer-note">
        ◎ &nbsp; Portfolio demonstration &nbsp;·&nbsp; supports human review — not a replacement for professional investigation
    </p>""", unsafe_allow_html=True)