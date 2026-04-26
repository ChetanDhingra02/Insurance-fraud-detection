import streamlit as st
import joblib
import html as html_mod

# model = joblib.load("deploy_fraud_model.pkl")
# template_row = joblib.load("deploy_input_template.pkl")
THRESHOLD = 0.25

st.set_page_config(
    page_title="ClaimIQ · Fraud Detection",
    page_icon="⬡",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&family=DM+Serif+Display:ital@0;1&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── RESET & BASE ─────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    color: #1a1a2e !important;
}

/* ── PAGE BACKGROUND ──────────────────────────────── */
.stApp {
    background-color: #f5f3ef;
    background-image:
        radial-gradient(ellipse 70% 50% at 0% 0%,   rgba(210,180,140,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 100% 80%, rgba(180,200,220,0.14) 0%, transparent 55%),
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60'%3E%3Ccircle cx='1' cy='1' r='0.8' fill='%231a1a2e' opacity='0.045'/%3E%3C/svg%3E");
    background-size: 100% 100%, 100% 100%, 60px 60px;
    min-height: 100vh;
}

.main .block-container {
    max-width: 1220px;
    padding: 0 2rem 6rem;
    position: relative;
}

[data-testid="stHeader"] { background: transparent !important; }

/* ── CUSTOM TIRE SCROLLBAR ────────────────────────── */
::-webkit-scrollbar { width: 12px; }
::-webkit-scrollbar-track {
    background: #e8e4dc;
    border-left: 1px solid #d6d1c8;
}
::-webkit-scrollbar-thumb {
    background:
        radial-gradient(circle at 50% 50%, #f5f3ef 0 18%, #2d2d2d 19% 38%, #555 39% 55%, #2d2d2d 56% 76%, #f5f3ef 77%),
        #1a1a2e;
    background-size: 12px 12px, 100%;
    background-repeat: repeat-y, no-repeat;
    border-radius: 999px;
    border: 1px solid #3a3a4a;
}
::-webkit-scrollbar-thumb:hover {
    background:
        radial-gradient(circle at 50% 50%, #f5f3ef 0 18%, #facc15 19% 38%, #d97706 39% 55%, #facc15 56% 76%, #f5f3ef 77%),
        #1a1a2e;
    background-size: 12px 12px, 100%;
    background-repeat: repeat-y, no-repeat;
}

/* ── TOP NAVIGATION BAR ───────────────────────────── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.2rem 0 1.4rem;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid rgba(26,26,46,0.10);
    animation: fadeDown 0.5s ease both;
}

.topbar-logo {
    display: flex;
    align-items: center;
    gap: 0.7rem;
}

.topbar-hex {
    width: 36px; height: 36px;
    background: #1a1a2e;
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.topbar-hex::after {
    content: "";
    position: absolute;
    width: 14px; height: 14px;
    background: #d4a847;
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
}

.topbar-name {
    font-family: 'DM Serif Display', serif;
    font-size: 1.35rem;
    color: #1a1a2e;
    letter-spacing: -0.02em;
}

.topbar-name em {
    font-style: italic;
    color: #d4a847;
}

.topbar-pills {
    display: flex;
    gap: 0.6rem;
}

.topbar-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 0.32rem 0.75rem;
    border-radius: 999px;
    border: 1px solid rgba(26,26,46,0.14);
    color: #5a5a7a;
    background: rgba(255,255,255,0.60);
}

.topbar-pill.active {
    background: #1a1a2e;
    color: #f5f3ef;
    border-color: #1a1a2e;
}

/* ── HERO SECTION ─────────────────────────────────── */
.hero-section {
    padding: 3.5rem 0 3rem;
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 2rem;
    align-items: end;
    border-bottom: 1px solid rgba(26,26,46,0.10);
    margin-bottom: 2.5rem;
    animation: fadeDown 0.6s ease 0.05s both;
}

.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.70rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #d4a847;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

.hero-eyebrow::before {
    content: "";
    display: inline-block;
    width: 28px; height: 1px;
    background: #d4a847;
}

.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2.8rem, 5vw, 4.6rem);
    line-height: 0.95;
    letter-spacing: -0.03em;
    color: #1a1a2e;
    margin-bottom: 1.3rem;
}

.hero-title em {
    font-style: italic;
    color: #d4a847;
}

.hero-sub {
    font-size: 1rem;
    font-weight: 300;
    line-height: 1.75;
    color: #5a5a7a;
    max-width: 540px;
}

.hero-stats {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    align-items: flex-end;
    padding-bottom: 0.4rem;
}

.hero-stat {
    text-align: right;
}

.hero-stat-val {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #1a1a2e;
    line-height: 1;
    letter-spacing: -0.04em;
}

.hero-stat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    color: #9090aa;
    margin-top: 0.2rem;
}

/* ── SECTION LABELS ───────────────────────────────── */
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #9090aa;
    font-weight: 500;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.section-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: rgba(26,26,46,0.08);
}

/* ── CARDS ────────────────────────────────────────── */
.card {
    background: rgba(255,255,255,0.72);
    border: 1px solid rgba(26,26,46,0.09);
    border-radius: 20px;
    padding: 1.6rem 1.7rem;
    margin-bottom: 1.1rem;
    backdrop-filter: blur(12px) saturate(150%);
    -webkit-backdrop-filter: blur(12px) saturate(150%);
    position: relative;
    overflow: hidden;
    transition:
        transform 0.30s cubic-bezier(0.22,1,0.36,1),
        box-shadow 0.30s ease,
        border-color 0.25s ease;
    box-shadow:
        0 1px 2px rgba(26,26,46,0.05),
        0 8px 32px rgba(26,26,46,0.06),
        inset 0 1px 0 rgba(255,255,255,0.90);
    animation: riseCard 0.55s cubic-bezier(0.22,1,0.36,1) both;
}

.card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #d4a847, #e8c56a, #d4a847);
    background-size: 200% 100%;
    opacity: 0;
    transition: opacity 0.25s ease;
    animation: shimmerBar 3s linear infinite;
}

@keyframes shimmerBar {
    0%   { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

.card:hover {
    transform: translateY(-5px);
    border-color: rgba(212,168,71,0.28);
    box-shadow:
        0 1px 2px rgba(26,26,46,0.04),
        0 20px 50px rgba(26,26,46,0.10),
        0 0 0 1px rgba(212,168,71,0.10),
        inset 0 1px 0 rgba(255,255,255,0.95);
}

.card:hover::before { opacity: 1; }

@keyframes riseCard {
    from { opacity: 0; transform: translateY(22px); }
    to   { opacity: 1; transform: translateY(0); }
}

.card:nth-child(2) { animation-delay: 0.07s; }
.card:nth-child(3) { animation-delay: 0.14s; }

.card-heading {
    font-family: 'DM Serif Display', serif;
    font-size: 1.35rem;
    color: #1a1a2e;
    letter-spacing: -0.02em;
    margin-bottom: 0.3rem;
    line-height: 1.2;
}

.card-note {
    font-size: 0.88rem;
    font-weight: 300;
    color: #7a7a9a;
    line-height: 1.60;
    margin-bottom: 1.2rem;
    padding-bottom: 1.0rem;
    border-bottom: 1px solid rgba(26,26,46,0.07);
}

/* ── STREAMLIT INPUT OVERRIDES ────────────────────── */
label,
div[data-testid="stWidgetLabel"] p {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.84rem !important;
    color: #3a3a5c !important;
    letter-spacing: 0.005em !important;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.85) !important;
    border: 1px solid rgba(26,26,46,0.14) !important;
    border-radius: 12px !important;
    min-height: 44px !important;
    color: #1a1a2e !important;
    -webkit-text-fill-color: #1a1a2e !important;
    font-weight: 500 !important;
    font-size: 0.90rem !important;
    box-shadow: 0 2px 8px rgba(26,26,46,0.06), inset 0 1px 0 rgba(255,255,255,0.9) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] input {
    color: #1a1a2e !important;
    -webkit-text-fill-color: #1a1a2e !important;
    opacity: 1 !important;
}

div[data-baseweb="select"] svg { color: #d4a847 !important; }

div[data-baseweb="select"] > div:hover {
    border-color: rgba(212,168,71,0.50) !important;
    box-shadow: 0 0 0 3px rgba(212,168,71,0.10), 0 4px 14px rgba(26,26,46,0.08) !important;
}

[data-baseweb="menu"], [data-baseweb="popover"] > div {
    background: rgba(250,248,244,0.98) !important;
    border: 1px solid rgba(26,26,46,0.10) !important;
    border-radius: 14px !important;
    box-shadow: 0 12px 40px rgba(26,26,46,0.14) !important;
    backdrop-filter: blur(16px) !important;
}

[data-baseweb="option"] {
    color: #1a1a2e !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    border-radius: 8px !important;
    margin: 2px 6px !important;
}

[data-baseweb="option"]:hover,
[data-baseweb="option"][aria-selected="true"] {
    background: rgba(212,168,71,0.12) !important;
    color: #1a1a2e !important;
}

/* Number input */
[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.85) !important;
    border: 1px solid rgba(26,26,46,0.14) !important;
    border-radius: 12px !important;
    color: #1a1a2e !important;
    -webkit-text-fill-color: #1a1a2e !important;
    font-weight: 500 !important;
    font-size: 0.90rem !important;
    box-shadow: 0 2px 8px rgba(26,26,46,0.06), inset 0 1px 0 rgba(255,255,255,0.9) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

[data-testid="stNumberInput"] input:focus {
    border-color: rgba(212,168,71,0.55) !important;
    box-shadow: 0 0 0 3px rgba(212,168,71,0.12), 0 4px 14px rgba(26,26,46,0.08) !important;
    outline: none !important;
}

[data-testid="stNumberInput"] button {
    background: rgba(26,26,46,0.06) !important;
    color: #3a3a5c !important;
    border: 1px solid rgba(26,26,46,0.08) !important;
    border-radius: 9px !important;
    transition: all 0.15s ease !important;
}

[data-testid="stNumberInput"] button:hover {
    background: rgba(212,168,71,0.15) !important;
    border-color: rgba(212,168,71,0.30) !important;
    color: #1a1a2e !important;
}

/* Slider thumb */
[data-testid="stSlider"] [role="slider"],
[data-testid="stSelectSlider"] [role="slider"] {
    background:
        radial-gradient(circle at 50% 50%,
            #f5f3ef 0 16%,
            #1a1a2e 17% 34%,
            #4a4a6a 35% 54%,
            #1a1a2e 55% 72%,
            #f5f3ef 73%) !important;
    border: 2.5px solid #1a1a2e !important;
    width: 22px !important;
    height: 22px !important;
    box-shadow: 0 3px 10px rgba(26,26,46,0.30) !important;
    transition: box-shadow 0.2s ease, transform 0.15s ease !important;
}

[data-testid="stSlider"] [role="slider"]:hover,
[data-testid="stSelectSlider"] [role="slider"]:hover {
    box-shadow:
        0 0 0 6px rgba(212,168,71,0.18),
        0 4px 14px rgba(26,26,46,0.30) !important;
    transform: scale(1.08) !important;
}

/* Slider track fill */
[data-testid="stSlider"] [data-baseweb="slider"] > div > div > div:nth-child(2),
[data-testid="stSelectSlider"] [data-baseweb="slider"] > div > div > div:nth-child(2) {
    background: linear-gradient(90deg, #d4a847, #e8c56a) !important;
    border-radius: 999px !important;
}

/* ── RUN BUTTON ───────────────────────────────────── */
div.stButton > button {
    background: #1a1a2e !important;
    color: #f5f3ef !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.88rem 2.2rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.01em !important;
    box-shadow:
        0 1px 2px rgba(26,26,46,0.15),
        0 10px 30px rgba(26,26,46,0.22),
        inset 0 1px 0 rgba(255,255,255,0.10) !important;
    position: relative;
    overflow: hidden;
    transition: transform 0.22s cubic-bezier(0.22,1,0.36,1), box-shadow 0.22s ease !important;
}

div.stButton > button::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.07) 0%, transparent 60%);
    pointer-events: none;
}

div.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow:
        0 1px 2px rgba(26,26,46,0.12),
        0 18px 42px rgba(26,26,46,0.28),
        inset 0 1px 0 rgba(255,255,255,0.12) !important;
}

div.stButton > button:active {
    transform: translateY(0px) scale(0.985) !important;
}

/* ── FADE ANIMATIONS ──────────────────────────────── */
@keyframes fadeDown {
    from { opacity: 0; transform: translateY(-14px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── RESULT ZONE ──────────────────────────────────── */
.results-divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 2rem 0 1.8rem;
    animation: fadeUp 0.4s ease both;
}

.results-divider-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(26,26,46,0.12), transparent);
}

.results-divider-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #9090aa;
    white-space: nowrap;
}

/* Score display */
.score-block {
    margin: 1.3rem 0 0.8rem;
    animation: scoreReveal 0.7s cubic-bezier(0.22,1,0.36,1) both 0.1s;
}

@keyframes scoreReveal {
    from { opacity: 0; transform: scale(0.80) translateY(10px); }
    to   { opacity: 1; transform: scale(1) translateY(0); }
}

.score-num {
    font-family: 'DM Serif Display', serif;
    font-size: 6rem;
    line-height: 0.9;
    letter-spacing: -0.05em;
    color: #1a1a2e;
    display: flex;
    align-items: flex-start;
    gap: 0.1em;
}

.score-pct {
    font-size: 2.2rem;
    opacity: 0.45;
    margin-top: 0.5rem;
    font-style: italic;
}

.score-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 0.4rem;
    font-weight: 500;
}

.col-low    { color: #2d8a4e; }
.col-medium { color: #c97316; }
.col-high   { color: #c42b2b; }

/* Progress bar */
.pbar-wrap {
    height: 8px;
    border-radius: 999px;
    background: rgba(26,26,46,0.08);
    overflow: hidden;
    margin: 1rem 0 0.5rem;
    box-shadow: inset 0 1px 3px rgba(26,26,46,0.10);
}

.pbar-fill {
    height: 100%;
    border-radius: 999px;
    animation: growBar 1.2s cubic-bezier(0.22,1,0.36,1) both;
    position: relative;
}

.pbar-fill::after {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 50%;
    background: rgba(255,255,255,0.40);
    border-radius: 999px;
}

@keyframes growBar {
    from { width: 0%; }
}

/* Gauge */
.gauge-outer {
    margin-top: 1.1rem;
    background: rgba(26,26,46,0.04);
    border: 1px solid rgba(26,26,46,0.07);
    border-radius: 16px;
    padding: 0.9rem 1rem 0.7rem;
}

.gauge-track {
    height: 14px;
    border-radius: 999px;
    background: linear-gradient(90deg,
        #4ade80 0%, #86efac 22%,
        #fcd34d 38%, #fb923c 55%,
        #f87171 72%, #dc2626 100%);
    position: relative;
    box-shadow: inset 0 2px 3px rgba(0,0,0,0.08);
    overflow: visible;
}

.gauge-needle {
    position: absolute;
    top: 50%;
    transform: translateX(-50%) translateY(-50%);
    width: 5px;
    height: 28px;
    background: #1a1a2e;
    border-radius: 999px;
    box-shadow:
        0 0 0 2.5px rgba(255,255,255,0.90),
        0 0 0 4px rgba(26,26,46,0.15),
        0 4px 12px rgba(26,26,46,0.30);
    animation: needleDrop 0.9s cubic-bezier(0.22,1,0.36,1) both 0.2s;
}

@keyframes needleDrop {
    from { opacity: 0; height: 0; }
    to   { opacity: 1; height: 28px; }
}

.gauge-ticks {
    display: flex;
    justify-content: space-between;
    margin-top: 0.5rem;
}

.gauge-tick {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
}

.gauge-tick-mark {
    width: 1px;
    height: 6px;
    background: rgba(26,26,46,0.20);
}

.gauge-tick-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.60rem;
    color: #9090aa;
    letter-spacing: 0.04em;
}

/* Badge */
.verdict-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    border-radius: 999px;
    padding: 0.44rem 1.0rem;
    font-weight: 600;
    font-size: 0.80rem;
    letter-spacing: 0.02em;
    border: 1px solid;
    margin-top: 1rem;
    animation: fadeUp 0.4s ease both 0.35s;
}

.badge-low    { background: #f0fdf4; color: #166534; border-color: #bbf7d0; }
.badge-medium { background: #fff7ed; color: #9a3412; border-color: #fed7aa; }
.badge-high   { background: #fef2f2; color: #991b1b; border-color: #fecaca; }

.badge-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: currentColor;
    animation: pulseDot 2s ease-in-out infinite;
}

@keyframes pulseDot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(0.7); }
}

/* Metric rows */
.mrow {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.60rem 0;
    border-bottom: 1px solid rgba(26,26,46,0.06);
    gap: 1rem;
}
.mrow:last-child { border-bottom: none; }

.mrow-k {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.70rem;
    letter-spacing: 0.06em;
    color: #9090aa;
    text-transform: uppercase;
}

.mrow-v {
    font-weight: 600;
    font-size: 0.88rem;
    color: #1a1a2e;
    text-align: right;
}

/* Action card inner box */
.action-box {
    margin: 1.2rem 0;
    border-radius: 14px;
    padding: 1.1rem 1.2rem;
    border-left: 3px solid;
    background: rgba(255,255,255,0.55);
    border-color: #d4a847;
    animation: fadeUp 0.5s ease both 0.25s;
}

.action-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.15rem;
    color: #1a1a2e;
    margin-bottom: 0.45rem;
    letter-spacing: -0.02em;
}

.action-desc {
    font-size: 0.87rem;
    font-weight: 300;
    color: #5a5a7a;
    line-height: 1.68;
}

/* Drivers */
.driver-item {
    display: flex;
    gap: 0.9rem;
    align-items: flex-start;
    padding: 0.85rem 0;
    border-bottom: 1px solid rgba(26,26,46,0.06);
    animation: fadeUp 0.4s ease both;
}

.driver-item:last-child { border-bottom: none; }

.driver-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    width: 24px; height: 24px;
    border-radius: 8px;
    background: rgba(26,26,46,0.06);
    border: 1px solid rgba(26,26,46,0.10);
    color: #5a5a7a;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 2px;
}

.driver-title {
    font-weight: 600;
    font-size: 0.88rem;
    color: #1a1a2e;
    margin-bottom: 0.18rem;
}

.driver-desc {
    font-size: 0.83rem;
    font-weight: 300;
    color: #7a7a9a;
    line-height: 1.55;
}

/* Footer */
.footer {
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #b0b0c8;
    margin-top: 3rem;
    padding-top: 1.4rem;
    border-top: 1px solid rgba(26,26,46,0.07);
}
</style>
""", unsafe_allow_html=True)


def esc(x):
    return html_mod.escape(str(x))


def rh(code):
    st.markdown(code, unsafe_allow_html=True)


def bodily_injuries_label_to_value(label):
    return {"None": 0, "One reported injury": 1, "Multiple / serious injuries": 2}[label]


def witnesses_label_to_value(label):
    return {"No witnesses": 0, "One witness": 1, "Two witnesses": 2, "Three or more witnesses": 3}[label]


def risk_meta(p):
    if p < 0.25:
        return "low",    "Low Risk",    "badge-low",    "col-low",    "#22c55e"
    elif p < 0.50:
        return "medium", "Medium Risk", "badge-medium", "col-medium", "#f97316"
    return     "high",   "High Risk",   "badge-high",   "col-high",   "#ef4444"


def action_meta(p):
    if p >= 0.50:
        return "Send for Manual Investigation", \
               "Score is elevated. This claim warrants investigator review before any payout is issued."
    elif p >= THRESHOLD:
        return "Flag for Secondary Review", \
               "Score exceeds the operating threshold. Route for supervisor review and request supporting documents."
    return "Process Normally", \
           "No elevated fraud signal detected. This claim can proceed through the standard processing route."


# ── TOP BAR ─────────────────────────────────────────────────────────────────
rh("""
<div class="topbar">
  <div class="topbar-logo">
    <div class="topbar-hex"></div>
    <span class="topbar-name">Claim<em>IQ</em></span>
  </div>
  <div class="topbar-pills">
    <span class="topbar-pill active">Fraud Detection</span>
    <span class="topbar-pill">v2.4.1</span>
    <span class="topbar-pill">Random Forest</span>
  </div>
</div>
""")

# ── HERO ─────────────────────────────────────────────────────────────────────
rh("""
<div class="hero-section">
  <div>
    <div class="hero-eyebrow">Auto Insurance · Fraud Risk Scoring</div>
    <h1 class="hero-title">Insurance<br><em>Fraud</em><br>Detection</h1>
    <p class="hero-sub">
      A machine-learning triage tool for vehicle insurance claims —
      scoring fraud risk in real time from claim details, policy data,
      and incident-level signals.
    </p>
  </div>
  <div class="hero-stats">
    <div class="hero-stat">
      <div class="hero-stat-val">12</div>
      <div class="hero-stat-label">Model Features</div>
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

# ── INPUT COLUMNS ────────────────────────────────────────────────────────────
left, right = st.columns(2, gap="large")

with left:
    rh("""
<div class="card">
  <div class="section-label">01 · Incident profile</div>
  <div class="card-heading">Vehicle Incident Details</div>
  <div class="card-note">Describe the collision type, damage severity, injuries, and witness count.</div>
</div>
""")
    incident_severity = st.selectbox("Incident Severity",
        ["Minor Damage", "Major Damage", "Total Loss", "Trivial Damage"])
    incident_type = st.selectbox("Incident Type",
        ["Single Vehicle Collision", "Multi-vehicle Collision", "Vehicle Theft", "Parked Car"])
    number_of_vehicles_involved = st.slider("Vehicles Involved", 1, 4, 1)
    bodily_injuries_label = st.select_slider("Reported Injuries",
        options=["None", "One reported injury", "Multiple / serious injuries"], value="None")
    bodily_injuries = bodily_injuries_label_to_value(bodily_injuries_label)
    witnesses_label = st.select_slider("Witnesses Present",
        options=["No witnesses", "One witness", "Two witnesses", "Three or more witnesses"], value="One witness")
    witnesses = witnesses_label_to_value(witnesses_label)
    months_as_customer = st.number_input("Months as Customer", min_value=0, value=200)

with right:
    rh("""
<div class="card">
  <div class="section-label">02 · Financial profile</div>
  <div class="card-heading">Policy &amp; Claim Amounts</div>
  <div class="card-note">Enter the claim breakdown, annual premium, and policy deductible.</div>
</div>
""")
    total_claim_amount    = st.number_input("Total Claim Amount ($)", min_value=0, value=50000)
    injury_claim          = st.number_input("Injury Claim ($)", min_value=0, value=5000)
    property_claim        = st.number_input("Property Claim ($)", min_value=0, value=10000)
    vehicle_claim         = st.number_input("Vehicle Claim ($)", min_value=0, value=35000)
    policy_annual_premium = st.number_input("Annual Premium ($)", min_value=0.0, value=1200.0, step=10.0)
    policy_deductable     = st.number_input("Policy Deductible ($)", min_value=0, value=1000)

predict = st.button("Run Fraud Risk Assessment →")

# ── RESULTS ──────────────────────────────────────────────────────────────────
if predict:
    # ── Swap this block for real model call ──────────────────────────────
    import random
    fraud_prob = random.uniform(0.05, 0.92)   # DEMO ONLY
    # input_data = template_row.copy()
    # ... set columns ...
    # fraud_prob = model.predict_proba(input_data)[0, 1]
    # ─────────────────────────────────────────────────────────────────────

    fraud_pred = int(fraud_prob >= THRESHOLD)
    risk_cls, risk_label, badge_cls, text_cls, risk_color = risk_meta(fraud_prob)
    action_title, action_desc = action_meta(fraud_prob)

    pct         = round(fraud_prob * 100, 1)
    verdict     = "Likely Fraudulent" if fraud_pred == 1 else "Likely Legitimate"
    marker_left = min(max(pct, 2), 97)
    delta       = abs(pct - THRESHOLD * 100)

    rh("""
<div class="results-divider">
  <div class="results-divider-line"></div>
  <span class="results-divider-label">Assessment Results</span>
  <div class="results-divider-line"></div>
</div>
""")

    r_col, a_col = st.columns(2, gap="large")

    with r_col:
        rh(f"""
<div class="card">
  <div class="section-label">03 · Model output</div>
  <div class="card-heading">Fraud Probability Score</div>

  <div class="score-block">
    <div class="score-num {text_cls}">
      {pct:.0f}<span class="score-pct">%</span>
    </div>
    <div class="score-sub {text_cls}">Fraud probability</div>
  </div>

  <div class="pbar-wrap">
    <div class="pbar-fill" style="width:{pct}%; background:linear-gradient(90deg, {risk_color}cc, {risk_color});"></div>
  </div>

  <div class="gauge-outer">
    <div class="gauge-track">
      <div class="gauge-needle" style="left:{marker_left}%;"></div>
    </div>
    <div class="gauge-ticks">
      <div class="gauge-tick"><div class="gauge-tick-mark"></div><span class="gauge-tick-label">0%</span></div>
      <div class="gauge-tick"><div class="gauge-tick-mark"></div><span class="gauge-tick-label">25%</span></div>
      <div class="gauge-tick"><div class="gauge-tick-mark"></div><span class="gauge-tick-label">50%</span></div>
      <div class="gauge-tick"><div class="gauge-tick-mark"></div><span class="gauge-tick-label">75%</span></div>
      <div class="gauge-tick"><div class="gauge-tick-mark"></div><span class="gauge-tick-label">100%</span></div>
    </div>
  </div>

  <div style="margin-top:1.1rem;">
    <div class="mrow">
      <span class="mrow-k">Threshold</span>
      <span class="mrow-v">{int(THRESHOLD*100)}%</span>
    </div>
    <div class="mrow">
      <span class="mrow-k">Delta from threshold</span>
      <span class="mrow-v">{delta:.1f} pp</span>
    </div>
    <div class="mrow">
      <span class="mrow-k">Verdict</span>
      <span class="mrow-v {text_cls}">{esc(verdict)}</span>
    </div>
  </div>

  <div>
    <span class="verdict-badge {badge_cls}">
      <span class="badge-dot"></span>
      {esc(risk_label)}
    </span>
  </div>
</div>
""")

    with a_col:
        rh(f"""
<div class="card">
  <div class="section-label">04 · Claim routing</div>
  <div class="card-heading">Recommended Handling</div>

  <div class="action-box">
    <div class="action-title">{esc(action_title)}</div>
    <div class="action-desc">{esc(action_desc)}</div>
  </div>

  <div class="mrow">
    <span class="mrow-k">Algorithm</span>
    <span class="mrow-v">Random Forest</span>
  </div>
  <div class="mrow">
    <span class="mrow-k">Features used</span>
    <span class="mrow-v">12 inputs</span>
  </div>
  <div class="mrow">
    <span class="mrow-k">Incident type</span>
    <span class="mrow-v">{esc(incident_type)}</span>
  </div>
  <div class="mrow">
    <span class="mrow-k">Severity</span>
    <span class="mrow-v">{esc(incident_severity)}</span>
  </div>
  <div class="mrow">
    <span class="mrow-k">Total claimed</span>
    <span class="mrow-v">${total_claim_amount:,}</span>
  </div>
  <div class="mrow">
    <span class="mrow-k">Annual premium</span>
    <span class="mrow-v">${policy_annual_premium:,.0f}</span>
  </div>
  <div class="mrow">
    <span class="mrow-k">Claim-to-premium ratio</span>
    <span class="mrow-v">{(total_claim_amount/policy_annual_premium if policy_annual_premium else 0):.1f}×</span>
  </div>
</div>
""")

    # ── DRIVERS ──────────────────────────────────────────────────────────
    drivers = []
    if incident_severity in ["Major Damage", "Total Loss"]:
        drivers.append(("Severe vehicle damage",
            "Major damage or total loss elevates claim complexity and review need."))
    if total_claim_amount >= 60000:
        drivers.append(("Large claim amount",
            f"Total of ${total_claim_amount:,} exceeds the $60,000 high-value threshold."))
    if number_of_vehicles_involved >= 2:
        drivers.append(("Multi-vehicle incident",
            "Multi-vehicle incidents require additional validation and documentation."))
    if bodily_injuries >= 1:
        drivers.append(("Injury component present",
            "Bodily injury claims typically require more supporting evidence."))
    if witnesses >= 2:
        drivers.append((f"{witnesses} witnesses present",
            "High witness count can affect investigation complexity and priority."))
    if months_as_customer < 24:
        drivers.append(("Short customer tenure",
            f"{months_as_customer} months on policy — a mild but notable review signal."))
    if policy_annual_premium > 0 and (total_claim_amount / policy_annual_premium) > 30:
        drivers.append(("High claim-to-premium ratio",
            f"Claim is {total_claim_amount/policy_annual_premium:.0f}× the annual premium — statistically unusual."))

    if not drivers:
        drivers_html = """
<div class="driver-item">
  <div class="driver-num">—</div>
  <div>
    <div class="driver-title">No major signals triggered</div>
    <div class="driver-desc">The entered values did not activate primary rule-based review flags.</div>
  </div>
</div>
"""
    else:
        drivers_html = ""
        for i, (t, d) in enumerate(drivers, 1):
            drivers_html += f"""
<div class="driver-item" style="animation-delay:{0.06*i}s">
  <div class="driver-num">0{i}</div>
  <div>
    <div class="driver-title">{esc(t)}</div>
    <div class="driver-desc">{esc(d)}</div>
  </div>
</div>
"""

    rh(f"""
<div class="card">
  <div class="section-label">05 · Review signals</div>
  <div class="card-heading">Key Factors Behind the Recommendation</div>
  <div class="card-note">These signals explain which inputs influenced the routing decision. They are informational, not deterministic.</div>
  {drivers_html}
</div>
""")

rh("""
<div class="footer">
  ClaimIQ · Portfolio Demonstration · Supports human triage — not automatic denial or approval
</div>
""")