import streamlit as st
import joblib
import html as html_mod

# model = joblib.load("deploy_fraud_model.pkl")
# template_row = joblib.load("deploy_input_template.pkl")
THRESHOLD = 0.25

st.set_page_config(
    page_title="Fraud Detection · Insurance ML",
    page_icon="🛡",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #0f0f14 !important;
}

/* ── PAGE BASE ─────────────────────────────────────── */
.stApp {
    background: #f7f8fc;
    background-image:
        radial-gradient(ellipse 80% 40% at 50% -10%, rgba(99,102,241,0.07) 0%, transparent 65%),
        linear-gradient(180deg, #ffffff 0%, #f7f8fc 100%);
}

.main .block-container {
    max-width: 1240px;
    padding: 0 2rem 5rem;
    position: relative;
}

[data-testid="stHeader"] { background: transparent !important; }

/* ── TIRE SCROLLBAR ─────────────────────────────────── */
::-webkit-scrollbar { width: 14px; }
::-webkit-scrollbar-track { background: #e8eaf2; }
::-webkit-scrollbar-thumb {
    border-radius: 999px;
    border: 3px solid #e8eaf2;
    background:
        radial-gradient(circle at 50% 50%,
            #f7f8fc 0%   15%,
            #1a1a2e 16%  32%,
            #6366f1 33%  50%,
            #1a1a2e 51%  67%,
            #f7f8fc 68%  100%),
        #1a1a2e;
    background-clip: padding-box;
}
::-webkit-scrollbar-thumb:hover {
    background:
        radial-gradient(circle at 50% 50%,
            #f7f8fc 0%   15%,
            #1a1a2e 16%  32%,
            #6366f1 33%  50%,
            #1a1a2e 51%  67%,
            #f7f8fc 68%  100%),
        #6366f1;
    background-clip: padding-box;
}

/* ── TOP HEADER BAR ────────────────────────────────── */
.site-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.1rem 0;
    border-bottom: 1px solid rgba(15,15,20,0.08);
    margin-bottom: 0;
    animation: slideDown 0.5s cubic-bezier(0.22,1,0.36,1) both;
    position: relative;
    overflow: hidden;
}

/* ANIMATED ROAD STRIPE in the header bottom */
.site-header::after {
    content: "";
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: repeating-linear-gradient(
        90deg,
        #6366f1 0px, #6366f1 40px,
        transparent 40px, transparent 60px
    );
    animation: roadScroll 1.6s linear infinite;
}

@keyframes roadScroll {
    from { background-position: 0 0; }
    to   { background-position: 100px 0; }
}

.header-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.header-icon {
    width: 34px; height: 34px;
    background: #0f0f14;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    position: relative;
    flex-shrink: 0;
}

.header-icon::after {
    content: "";
    width: 12px; height: 12px;
    border-radius: 3px;
    background: #6366f1;
    position: absolute;
    animation: iconPulse 3s ease-in-out infinite;
}

@keyframes iconPulse {
    0%,100% { transform: scale(1) rotate(0deg); background: #6366f1; }
    50%      { transform: scale(0.85) rotate(45deg); background: #818cf8; }
}

.header-wordmark {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #0f0f14;
}

.header-wordmark span {
    color: #6366f1;
}

.header-meta {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.meta-chip {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    font-weight: 400;
    letter-spacing: 0.04em;
    padding: 0.28rem 0.65rem;
    border-radius: 6px;
    border: 1px solid rgba(15,15,20,0.10);
    color: #5a5a7a;
    background: rgba(255,255,255,0.80);
    white-space: nowrap;
}

.meta-chip.live {
    background: #0f0f14;
    color: #f7f8fc;
    border-color: #0f0f14;
    display: flex; align-items: center; gap: 5px;
}

.live-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #4ade80;
    animation: livePulse 1.8s ease-in-out infinite;
}

@keyframes livePulse {
    0%,100% { opacity: 1; transform: scale(1); }
    50%      { opacity: 0.4; transform: scale(0.6); }
}

/* ── HERO ──────────────────────────────────────────── */
.hero {
    padding: 2.8rem 0 2.4rem;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 2rem;
    border-bottom: 1px solid rgba(15,15,20,0.07);
    margin-bottom: 2.2rem;
    animation: slideDown 0.55s cubic-bezier(0.22,1,0.36,1) 0.05s both;
}

.hero-left {}

.hero-tag {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #6366f1;
    margin-bottom: 1rem;
    display: flex; align-items: center; gap: 8px;
}

.hero-tag::before {
    content: "";
    display: block;
    width: 22px; height: 2px;
    background: #6366f1;
    border-radius: 2px;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.2rem, 4vw, 3.6rem);
    font-weight: 800;
    letter-spacing: -0.045em;
    line-height: 1.0;
    color: #0f0f14;
    margin-bottom: 1rem;
}

.hero-title .accent { color: #6366f1; }

.hero-desc {
    font-size: 0.93rem;
    font-weight: 400;
    line-height: 1.7;
    color: #6b6b85;
    max-width: 480px;
}

.hero-right {
    display: flex;
    gap: 1.4rem;
    align-items: flex-start;
    padding-top: 0.3rem;
    flex-shrink: 0;
}

.hero-stat {
    text-align: right;
    padding: 0 1.4rem;
    border-right: 1px solid rgba(15,15,20,0.08);
}
.hero-stat:last-child { border-right: none; padding-right: 0; }

.hero-stat-val {
    font-family: 'Syne', sans-serif;
    font-size: 1.9rem;
    font-weight: 800;
    color: #0f0f14;
    letter-spacing: -0.04em;
    line-height: 1;
}

.hero-stat-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.60rem;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    color: #9090aa;
    margin-top: 0.25rem;
}

/* ── CARDS ─────────────────────────────────────────── */
.card {
    background: #ffffff;
    border: 1px solid rgba(15,15,20,0.08);
    border-radius: 18px;
    padding: 1.5rem 1.6rem 1.2rem;
    margin-bottom: 1.1rem;
    position: relative;
    overflow: hidden;
    transition:
        transform 0.28s cubic-bezier(0.22,1,0.36,1),
        box-shadow 0.28s ease,
        border-color 0.22s ease;
    box-shadow: 0 1px 3px rgba(15,15,20,0.04), 0 6px 24px rgba(15,15,20,0.05);
    animation: riseUp 0.50s cubic-bezier(0.22,1,0.36,1) both;
}

/* Animated road stripe on each card top */
.card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: repeating-linear-gradient(
        90deg,
        #6366f1 0px, #6366f1 36px,
        #e0e0f0 36px, #e0e0f0 54px
    );
    background-size: 200% 100%;
    opacity: 0;
    transition: opacity 0.25s ease;
    animation: roadScroll 1.6s linear infinite;
}

.card:hover { transform: translateY(-4px); border-color: rgba(99,102,241,0.25); box-shadow: 0 2px 6px rgba(15,15,20,0.04), 0 16px 44px rgba(99,102,241,0.10); }
.card:hover::before { opacity: 1; }

@keyframes riseUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}

.card:nth-child(2) { animation-delay: 0.06s; }
.card:nth-child(3) { animation-delay: 0.12s; }

.card-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #9090aa;
    margin-bottom: 0.4rem;
    display: flex; align-items: center; gap: 8px;
}
.card-label::after {
    content: ""; flex: 1;
    height: 1px; background: rgba(15,15,20,0.06);
}

.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #0f0f14;
    margin-bottom: 0.25rem;
}

.card-sub {
    font-size: 0.84rem;
    font-weight: 400;
    color: #8a8aa8;
    line-height: 1.55;
    margin-bottom: 1.0rem;
    padding-bottom: 0.9rem;
    border-bottom: 1px solid rgba(15,15,20,0.05);
}

/* ── STREAMLIT WIDGETS ─────────────────────────────── */
label, div[data-testid="stWidgetLabel"] p {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.83rem !important;
    color: #3a3a52 !important;
}

div[data-baseweb="select"] > div {
    background: #fafbff !important;
    border: 1px solid rgba(15,15,20,0.12) !important;
    border-radius: 10px !important;
    min-height: 42px !important;
    color: #0f0f14 !important;
    -webkit-text-fill-color: #0f0f14 !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    box-shadow: 0 1px 4px rgba(15,15,20,0.05) !important;
    transition: border-color 0.18s ease, box-shadow 0.18s ease !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] input {
    color: #0f0f14 !important;
    -webkit-text-fill-color: #0f0f14 !important;
    opacity: 1 !important;
}

div[data-baseweb="select"] svg { color: #6366f1 !important; }

div[data-baseweb="select"] > div:hover {
    border-color: rgba(99,102,241,0.45) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.10) !important;
}

[data-baseweb="menu"], [data-baseweb="popover"] > div {
    background: #ffffff !important;
    border: 1px solid rgba(15,15,20,0.09) !important;
    border-radius: 12px !important;
    box-shadow: 0 12px 36px rgba(15,15,20,0.12) !important;
}

[data-baseweb="option"] {
    color: #0f0f14 !important;
    font-weight: 500 !important;
    font-size: 0.87rem !important;
    border-radius: 6px !important;
    margin: 2px 6px !important;
}

[data-baseweb="option"]:hover,
[data-baseweb="option"][aria-selected="true"] {
    background: rgba(99,102,241,0.09) !important;
    color: #4f46e5 !important;
}

[data-testid="stNumberInput"] input {
    background: #fafbff !important;
    border: 1px solid rgba(15,15,20,0.12) !important;
    border-radius: 10px !important;
    color: #0f0f14 !important;
    -webkit-text-fill-color: #0f0f14 !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    box-shadow: 0 1px 4px rgba(15,15,20,0.05) !important;
    transition: border-color 0.18s, box-shadow 0.18s !important;
}

[data-testid="stNumberInput"] input:focus {
    border-color: rgba(99,102,241,0.50) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.10) !important;
    outline: none !important;
}

[data-testid="stNumberInput"] button {
    background: #f0f1fb !important;
    color: #4f46e5 !important;
    border: 1px solid rgba(99,102,241,0.15) !important;
    border-radius: 7px !important;
    font-weight: 700 !important;
    transition: background 0.15s !important;
}
[data-testid="stNumberInput"] button:hover {
    background: rgba(99,102,241,0.15) !important;
}

/* Slider — clean thumb, no broken patterns */
[data-testid="stSlider"] [role="slider"],
[data-testid="stSelectSlider"] [role="slider"] {
    background: #0f0f14 !important;
    border: 3px solid #ffffff !important;
    width: 20px !important; height: 20px !important;
    box-shadow: 0 0 0 2px #6366f1, 0 4px 12px rgba(15,15,20,0.25) !important;
    transition: box-shadow 0.18s ease !important;
}

[data-testid="stSlider"] [role="slider"]:hover,
[data-testid="stSelectSlider"] [role="slider"]:hover {
    box-shadow: 0 0 0 5px rgba(99,102,241,0.22), 0 5px 16px rgba(15,15,20,0.28) !important;
}

/* slider fill track */
div[data-testid="stSlider"] > div > div > div > div:nth-child(1) > div,
div[data-testid="stSelectSlider"] > div > div > div > div:nth-child(1) > div {
    background: linear-gradient(90deg, #6366f1, #818cf8) !important;
}

/* ── RUN BUTTON ────────────────────────────────────── */
div.stButton > button {
    background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.82rem 2.0rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.01em !important;
    box-shadow: 0 4px 16px rgba(99,102,241,0.35), 0 1px 3px rgba(15,15,20,0.10) !important;
    transition: transform 0.22s cubic-bezier(0.22,1,0.36,1), box-shadow 0.22s ease !important;
    position: relative; overflow: hidden;
}
div.stButton > button::after {
    content: "";
    position: absolute; inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, transparent 60%);
    pointer-events: none;
}
div.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 28px rgba(99,102,241,0.42), 0 2px 6px rgba(15,15,20,0.10) !important;
}
div.stButton > button:active { transform: translateY(0) scale(0.98) !important; }

/* ── FADE ANIMATIONS ───────────────────────────────── */
@keyframes slideDown {
    from { opacity: 0; transform: translateY(-12px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── RESULTS ───────────────────────────────────────── */
.section-divider {
    display: flex; align-items: center; gap: 1rem;
    margin: 2rem 0 1.8rem;
    animation: fadeIn 0.35s ease both;
}
.divider-line { flex: 1; height: 1px; background: rgba(15,15,20,0.07); }
.divider-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem; letter-spacing: 0.14em;
    text-transform: uppercase; color: #9090aa;
    white-space: nowrap;
}

/* Score */
.score-wrap {
    margin: 1.2rem 0 0.8rem;
    animation: popIn 0.65s cubic-bezier(0.22,1,0.36,1) 0.08s both;
}
@keyframes popIn {
    from { opacity: 0; transform: scale(0.75); }
    to   { opacity: 1; transform: scale(1); }
}

.score-number {
    font-family: 'Syne', sans-serif;
    font-size: 5.5rem;
    font-weight: 800;
    letter-spacing: -0.06em;
    line-height: 0.9;
    display: flex; align-items: flex-start;
}
.score-pct {
    font-size: 2rem;
    margin-top: 0.5rem;
    opacity: 0.4;
    font-weight: 600;
}
.score-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    font-weight: 400;
    margin-top: 0.35rem;
}
.c-low    { color: #16a34a; }
.c-med    { color: #d97706; }
.c-high   { color: #dc2626; }

/* Progress */
.pbar-track {
    height: 7px; border-radius: 999px;
    background: rgba(15,15,20,0.07);
    overflow: hidden; margin: 1rem 0 0.4rem;
    box-shadow: inset 0 1px 2px rgba(15,15,20,0.08);
}
.pbar-fill {
    height: 100%; border-radius: 999px;
    animation: growBar 1.1s cubic-bezier(0.22,1,0.36,1) both;
    position: relative;
}
.pbar-fill::after {
    content: ""; position: absolute;
    top: 0; left: 0; right: 0; height: 50%;
    background: rgba(255,255,255,0.35); border-radius: 999px;
}
@keyframes growBar { from { width: 0%; } }

/* Gauge */
.gauge-wrap {
    margin-top: 1.1rem;
    background: #f7f8fc;
    border: 1px solid rgba(15,15,20,0.06);
    border-radius: 14px;
    padding: 0.85rem 0.95rem 0.7rem;
}
.gauge-track {
    height: 12px; border-radius: 999px;
    background: linear-gradient(90deg,
        #4ade80 0%, #86efac 20%,
        #fde68a 38%, #fb923c 56%,
        #fca5a5 72%, #ef4444 100%);
    position: relative;
    box-shadow: inset 0 2px 3px rgba(0,0,0,0.07);
    overflow: visible;
}
.gauge-needle {
    position: absolute; top: 50%;
    transform: translateX(-50%) translateY(-50%);
    width: 4px; height: 24px;
    background: #0f0f14; border-radius: 999px;
    box-shadow: 0 0 0 2px #fff, 0 0 0 3.5px rgba(15,15,20,0.20), 0 4px 10px rgba(15,15,20,0.28);
    animation: needleIn 0.8s cubic-bezier(0.22,1,0.36,1) 0.2s both;
}
@keyframes needleIn {
    from { opacity: 0; transform: translateX(-50%) translateY(-50%) scaleY(0); }
    to   { opacity: 1; transform: translateX(-50%) translateY(-50%) scaleY(1); }
}
.gauge-labels {
    display: flex; justify-content: space-between;
    margin-top: 0.45rem;
}
.gauge-lbl {
    font-family: 'Space Mono', monospace;
    font-size: 0.60rem; color: #9090aa; letter-spacing: 0.04em;
}

/* Badge */
.verdict-badge {
    display: inline-flex; align-items: center;
    gap: 6px; border-radius: 999px;
    padding: 0.4rem 0.9rem; font-weight: 600;
    font-size: 0.78rem; letter-spacing: 0.02em;
    border: 1px solid; margin-top: 1rem;
    animation: fadeIn 0.4s ease 0.3s both;
}
.badge-low  { background:#f0fdf4; color:#15803d; border-color:#bbf7d0; }
.badge-med  { background:#fffbeb; color:#b45309; border-color:#fde68a; }
.badge-high { background:#fef2f2; color:#b91c1c; border-color:#fecaca; }
.badge-pulse {
    width:7px; height:7px; border-radius:50%;
    background: currentColor;
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
    0%,100% { opacity:1; transform:scale(1); }
    50%      { opacity:0.4; transform:scale(0.65); }
}

/* Metric rows */
.mrow {
    display:flex; justify-content:space-between; align-items:center;
    padding:0.58rem 0; border-bottom:1px solid rgba(15,15,20,0.05); gap:1rem;
}
.mrow:last-child { border-bottom:none; }
.mrow-k {
    font-family:'Space Mono',monospace;
    font-size:0.67rem; letter-spacing:0.07em;
    text-transform:uppercase; color:#9090aa;
}
.mrow-v { font-weight:600; font-size:0.87rem; color:#0f0f14; text-align:right; }

/* Action box */
.action-box {
    margin:1.1rem 0; border-radius:12px;
    padding:1.0rem 1.1rem;
    background: linear-gradient(135deg, rgba(99,102,241,0.06) 0%, rgba(99,102,241,0.02) 100%);
    border:1px solid rgba(99,102,241,0.18);
    border-left:3px solid #6366f1;
    animation: fadeIn 0.45s ease 0.2s both;
}
.action-title {
    font-family:'Syne',sans-serif;
    font-size:1.05rem; font-weight:700;
    color:#0f0f14; letter-spacing:-0.02em; margin-bottom:0.4rem;
}
.action-desc { font-size:0.84rem; font-weight:400; color:#6b6b85; line-height:1.65; }

/* Driver items */
.driver {
    display:flex; gap:0.85rem; align-items:flex-start;
    padding:0.80rem 0; border-bottom:1px solid rgba(15,15,20,0.05);
    animation: fadeIn 0.4s ease both;
}
.driver:last-child { border-bottom:none; }
.driver-num {
    font-family:'Space Mono',monospace; font-size:0.62rem; font-weight:700;
    width:26px; height:26px; border-radius:8px;
    background:#f0f1fb; border:1px solid rgba(99,102,241,0.18);
    color:#6366f1; display:flex; align-items:center; justify-content:center;
    flex-shrink:0; margin-top:1px;
}
.driver-title { font-weight:600; font-size:0.87rem; color:#0f0f14; margin-bottom:0.15rem; }
.driver-desc  { font-size:0.81rem; font-weight:400; color:#8a8aa8; line-height:1.55; }

/* Footer */
.page-footer {
    text-align:center;
    font-family:'Space Mono',monospace;
    font-size:0.63rem; letter-spacing:0.09em; text-transform:uppercase;
    color:#b0b0c8; margin-top:3rem; padding-top:1.4rem;
    border-top:1px solid rgba(15,15,20,0.06);
}

/* Stagger delays for drivers */
.driver:nth-child(1){animation-delay:0.05s;}
.driver:nth-child(2){animation-delay:0.10s;}
.driver:nth-child(3){animation-delay:0.15s;}
.driver:nth-child(4){animation-delay:0.20s;}
.driver:nth-child(5){animation-delay:0.25s;}
.driver:nth-child(6){animation-delay:0.30s;}
.driver:nth-child(7){animation-delay:0.35s;}
</style>
""", unsafe_allow_html=True)


def esc(x): return html_mod.escape(str(x))
def rh(c): st.markdown(c, unsafe_allow_html=True)

def bi_val(l): return {"None":0,"One reported injury":1,"Multiple / serious injuries":2}[l]
def wi_val(l): return {"No witnesses":0,"One witness":1,"Two witnesses":2,"Three or more witnesses":3}[l]

def risk_meta(p):
    if p < 0.25: return "low",  "Low Risk",    "badge-low",  "c-low",  "#22c55e"
    if p < 0.50: return "med",  "Medium Risk",  "badge-med",  "c-med",  "#f59e0b"
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
<div class="site-header">
  <div class="header-brand">
    <div class="header-icon"></div>
    <span class="header-wordmark">Fraud<span>IQ</span></span>
  </div>
  <div class="header-meta">
    <span class="meta-chip live"><span class="live-dot"></span>Model Ready</span>
    <span class="meta-chip">Random Forest</span>
    <span class="meta-chip">Threshold 25%</span>
    <span class="meta-chip">v2.4.1</span>
  </div>
</div>
""")

# ── HERO ──────────────────────────────────────────────────────────────────────
rh("""
<div class="hero">
  <div class="hero-left">
    <div class="hero-tag">Auto Insurance · ML Risk Scoring</div>
    <h1 class="hero-title">Insurance<br><span class="accent">Fraud</span><br>Detection</h1>
    <p class="hero-desc">
      ML-powered triage for vehicle insurance claims — scoring fraud risk
      from incident, policy, and financial signals in real time.
    </p>
  </div>
  <div class="hero-right">
    <div class="hero-stat">
      <div class="hero-stat-val">12</div>
      <div class="hero-stat-label">Features</div>
    </div>
    <div class="hero-stat">
      <div class="hero-stat-val">25%</div>
      <div class="hero-stat-label">Threshold</div>
    </div>
    <div class="hero-stat">
      <div class="hero-stat-val">RF</div>
      <div class="hero-stat-label">Algorithm</div>
    </div>
  </div>
</div>
""")

# ── INPUTS ────────────────────────────────────────────────────────────────────
left, right = st.columns(2, gap="large")

with left:
    rh("""<div class="card">
  <div class="card-label">01 · Incident profile</div>
  <div class="card-title">Vehicle Incident Details</div>
  <div class="card-sub">Collision type, damage severity, injuries, witnesses, and tenure.</div>
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
  <div class="card-label">02 · Financial profile</div>
  <div class="card-title">Policy &amp; Claim Amounts</div>
  <div class="card-sub">Claim breakdown, annual premium, and policy deductible.</div>
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
    # ── Swap for real model ──────────────────────────────────────────────────
    import random
    fraud_prob = random.uniform(0.05, 0.92)
    # input_data = template_row.copy()
    # ... populate columns ...
    # fraud_prob = model.predict_proba(input_data)[0, 1]
    # ─────────────────────────────────────────────────────────────────────────

    fraud_pred = int(fraud_prob >= THRESHOLD)
    risk_cls, risk_label, badge_cls, text_cls, risk_color = risk_meta(fraud_prob)
    action_title, action_desc = action_meta(fraud_prob)

    pct         = round(fraud_prob * 100, 1)
    verdict     = "Likely Fraudulent" if fraud_pred == 1 else "Likely Legitimate"
    marker_left = min(max(pct, 2), 97)
    delta       = abs(pct - THRESHOLD * 100)
    cpr         = (total_claim_amount / policy_annual_premium) if policy_annual_premium else 0

    rh("""<div class="section-divider">
  <div class="divider-line"></div>
  <span class="divider-label">Assessment Results</span>
  <div class="divider-line"></div>
</div>""")

    r_col, a_col = st.columns(2, gap="large")

    with r_col:
        rh(f"""<div class="card">
  <div class="card-label">03 · Model output</div>
  <div class="card-title">Fraud Probability Score</div>

  <div class="score-wrap">
    <div class="score-number {text_cls}">
      {pct:.0f}<span class="score-pct">%</span>
    </div>
    <div class="score-label {text_cls}">Estimated fraud probability</div>
  </div>

  <div class="pbar-track">
    <div class="pbar-fill" style="width:{pct}%; background:linear-gradient(90deg,{risk_color}99,{risk_color});"></div>
  </div>

  <div class="gauge-wrap">
    <div class="gauge-track">
      <div class="gauge-needle" style="left:{marker_left}%;"></div>
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
    <div class="mrow"><span class="mrow-k">Delta from threshold</span><span class="mrow-v">{delta:.1f} pp</span></div>
    <div class="mrow"><span class="mrow-k">Verdict</span><span class="mrow-v {text_cls}">{esc(verdict)}</span></div>
  </div>

  <span class="verdict-badge {badge_cls}">
    <span class="badge-pulse"></span>{esc(risk_label)}
  </span>
</div>""")

    with a_col:
        rh(f"""<div class="card">
  <div class="card-label">04 · Claim routing</div>
  <div class="card-title">Recommended Handling</div>

  <div class="action-box">
    <div class="action-title">{esc(action_title)}</div>
    <div class="action-desc">{esc(action_desc)}</div>
  </div>

  <div class="mrow"><span class="mrow-k">Algorithm</span><span class="mrow-v">Random Forest</span></div>
  <div class="mrow"><span class="mrow-k">Features used</span><span class="mrow-v">12 inputs</span></div>
  <div class="mrow"><span class="mrow-k">Incident type</span><span class="mrow-v">{esc(incident_type)}</span></div>
  <div class="mrow"><span class="mrow-k">Severity</span><span class="mrow-v">{esc(incident_severity)}</span></div>
  <div class="mrow"><span class="mrow-k">Total claimed</span><span class="mrow-v">${total_claim_amount:,}</span></div>
  <div class="mrow"><span class="mrow-k">Annual premium</span><span class="mrow-v">${policy_annual_premium:,.0f}</span></div>
  <div class="mrow"><span class="mrow-k">Claim-to-premium ratio</span><span class="mrow-v">{cpr:.1f}×</span></div>
</div>""")

    # ── DRIVERS ──────────────────────────────────────────────────────────────
    drivers = []
    if incident_severity in ["Major Damage","Total Loss"]:
        drivers.append(("Severe vehicle damage","Major damage or total loss increases review complexity significantly."))
    if total_claim_amount >= 60000:
        drivers.append(("Large claim amount", f"${total_claim_amount:,} exceeds the $60k high-value threshold."))
    if number_of_vehicles_involved >= 2:
        drivers.append(("Multi-vehicle incident","Multi-vehicle collisions require additional validation steps."))
    if bodily_injuries >= 1:
        drivers.append(("Injury component","Bodily injury claims require stronger supporting documentation."))
    if witnesses >= 2:
        drivers.append((f"{witnesses} witnesses present","Elevated witness count affects investigation priority."))
    if months_as_customer < 24:
        drivers.append(("Short customer tenure",f"{months_as_customer} months on policy — a mild but notable signal."))
    if cpr > 30:
        drivers.append(("High claim-to-premium ratio",f"Claim is {cpr:.0f}× the annual premium — statistically anomalous."))

    if not drivers:
        drivers_html = """<div class="driver">
  <div class="driver-num">—</div>
  <div>
    <div class="driver-title">No major signals triggered</div>
    <div class="driver-desc">Entered values did not activate primary review flags.</div>
  </div>
</div>"""
    else:
        drivers_html = "".join(f"""<div class="driver">
  <div class="driver-num">{str(i).zfill(2)}</div>
  <div>
    <div class="driver-title">{esc(t)}</div>
    <div class="driver-desc">{esc(d)}</div>
  </div>
</div>""" for i,(t,d) in enumerate(drivers,1))

    rh(f"""<div class="card">
  <div class="card-label">05 · Review signals</div>
  <div class="card-title">Key Factors Behind the Recommendation</div>
  <div class="card-sub">Informational signals — not deterministic. Support triage, not automatic decisions.</div>
  {drivers_html}
</div>""")

rh("""<div class="page-footer">
  Portfolio Demonstration · Supports human triage — not automatic denial or approval
</div>""")