import streamlit as st
import joblib
import html

# ── Load model ──────────────────────────────────────────────────────────────
model = joblib.load("deploy_fraud_model.pkl")
template_row = joblib.load("deploy_input_template.pkl")
THRESHOLD = 0.25

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Insurance Fraud Detection",
    page_icon="🚗",
    layout="wide",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    color: #111827 !important;
}

.stApp {
    background:
        radial-gradient(circle at 12% 18%, rgba(220, 38, 38, 0.16), transparent 28%),
        radial-gradient(circle at 88% 12%, rgba(37, 99, 235, 0.16), transparent 30%),
        radial-gradient(circle at 70% 90%, rgba(15, 23, 42, 0.08), transparent 30%),
        linear-gradient(135deg, #f8fafc 0%, #eef2f7 48%, #f8f5f0 100%);
    overflow-x: hidden;
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(90deg, rgba(15,23,42,0.045) 1px, transparent 1px),
        linear-gradient(rgba(15,23,42,0.035) 1px, transparent 1px);
    background-size: 54px 54px;
    pointer-events: none;
    z-index: 0;
}

.stApp::after {
    content: "";
    position: fixed;
    width: 520px;
    height: 520px;
    left: -160px;
    top: 140px;
    background: radial-gradient(circle, rgba(220,38,38,0.14), transparent 65%);
    filter: blur(10px);
    animation: ambientMove 12s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}

@keyframes ambientMove {
    from { transform: translate3d(0,0,0) scale(1); }
    to { transform: translate3d(180px,90px,0) scale(1.18); }
}

.main .block-container {
    max-width: 1180px;
    padding: 2.5rem 2.2rem 5rem;
    position: relative;
    z-index: 1;
}

[data-testid="stHeader"] {
    background: transparent;
}

.hero,
.card {
    background: rgba(255, 255, 255, 0.58);
    backdrop-filter: blur(24px) saturate(170%);
    -webkit-backdrop-filter: blur(24px) saturate(170%);
    border: 1px solid rgba(255,255,255,0.72);
    box-shadow:
        0 24px 70px rgba(15,23,42,0.14),
        inset 0 1px 0 rgba(255,255,255,0.75),
        inset 0 -1px 0 rgba(15,23,42,0.05);
    transition:
        transform 0.28s ease,
        box-shadow 0.28s ease,
        border-color 0.28s ease;
}

.hero {
    border-radius: 30px;
    padding: 2.35rem;
    margin-bottom: 1.5rem;
    color: #111827;
    position: relative;
    overflow: hidden;
    animation: riseIn 0.65s ease both;
}

.hero:hover,
.card:hover {
    transform: translateY(-5px) perspective(900px) rotateX(1.2deg);
    box-shadow:
        0 34px 90px rgba(15,23,42,0.18),
        inset 0 1px 0 rgba(255,255,255,0.85);
}

.hero::after {
    content: "";
    position: absolute;
    right: -75px;
    top: -85px;
    width: 290px;
    height: 290px;
    border-radius: 50%;
    border: 34px solid rgba(15,23,42,0.055);
}

.card {
    border-radius: 24px;
    padding: 1.5rem 1.6rem;
    margin-bottom: 1.15rem;
    animation: riseIn 0.55s ease both;
}

@keyframes riseIn {
    from { opacity: 0; transform: translateY(22px) scale(0.985); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}

.kicker,
.section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #64748b;
    font-weight: 700;
    margin-bottom: 0.72rem;
}

.hero-title {
    font-size: clamp(2.75rem, 5vw, 4.6rem);
    line-height: 0.96;
    font-weight: 900;
    letter-spacing: -0.06em;
    margin: 0;
    color: #0f172a;
}

.hero-sub,
.note {
    color: #475569;
    font-size: 0.97rem;
    line-height: 1.7;
}

.heading {
    font-size: 1.58rem;
    font-weight: 850;
    letter-spacing: -0.04em;
    margin-bottom: 0.45rem;
    color: #0f172a;
}

.road-rule {
    height: 7px;
    margin-top: 1.25rem;
    border-radius: 999px;
    background: repeating-linear-gradient(
        90deg,
        #dc2626 0 42px,
        transparent 42px 66px
    );
    opacity: 0.72;
    animation: roadMove 2.8s linear infinite;
}

@keyframes roadMove {
    from { background-position: 0 0; }
    to { background-position: 132px 0; }
}

label,
div[data-testid="stWidgetLabel"] p {
    font-weight: 700 !important;
    color: #1f2937 !important;
    font-size: 0.88rem !important;
}

div[data-baseweb="select"] > div,
[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.82) !important;
    border: 1.5px solid rgba(100,116,139,0.35) !important;
    border-radius: 14px !important;
    min-height: 45px !important;
    color: #111827 !important;
    font-weight: 600 !important;
    box-shadow:
        0 10px 25px rgba(15,23,42,0.06),
        inset 0 1px 0 rgba(255,255,255,0.75) !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] div,
div[data-baseweb="select"] input,
[data-testid="stNumberInput"] input,
input {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    opacity: 1 !important;
}

[data-testid="stNumberInput"] input::placeholder,
input::placeholder {
    color: #64748b !important;
    -webkit-text-fill-color: #64748b !important;
    opacity: 0.75 !important;
}

div[data-baseweb="select"] svg {
    color: #dc2626 !important;
    opacity: 1 !important;
    width: 20px !important;
    height: 20px !important;
}

div[data-baseweb="select"] > div::after {
    content: "▾";
    color: #dc2626;
    font-size: 1rem;
    font-weight: 900;
    margin-right: 0.4rem;
}

div[data-baseweb="select"] > div:hover,
[data-testid="stNumberInput"] input:focus {
    border-color: rgba(220,38,38,0.75) !important;
    box-shadow:
        0 0 0 4px rgba(220,38,38,0.12),
        0 16px 35px rgba(15,23,42,0.10) !important;
}

[data-baseweb="menu"] {
    background: rgba(255,255,255,0.96) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(148,163,184,0.35) !important;
    border-radius: 14px !important;
    box-shadow: 0 18px 45px rgba(15,23,42,0.18) !important;
}

[data-baseweb="option"] {
    color: #111827 !important;
    font-weight: 600 !important;
}

[data-baseweb="option"]:hover {
    background: rgba(220,38,38,0.08) !important;
}

[data-testid="stNumberInput"] button {
    background: #1f2937 !important;
    color: white !important;
    border: none !important;
}

[data-testid="stNumberInput"] button:hover {
    background: #dc2626 !important;
}

[data-testid="stSlider"] [role="slider"],
[data-testid="stSelectSlider"] [role="slider"] {
    background:
        radial-gradient(circle, #f8fafc 0 13%, #111827 14% 34%, #475569 35% 58%, #111827 59% 100%) !important;
    border: 3px solid #ffffff !important;
    width: 25px !important;
    height: 25px !important;
    box-shadow:
        0 5px 14px rgba(15,23,42,0.34),
        0 0 0 4px rgba(220,38,38,0.10) !important;
    transition: transform 0.18s ease !important;
}

[data-testid="stSlider"] [role="slider"]:hover,
[data-testid="stSelectSlider"] [role="slider"]:hover {
    transform: scale(1.12);
}

div.stButton > button {
    background: linear-gradient(135deg, #ef4444, #991b1b) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.45) !important;
    border-radius: 16px !important;
    padding: 0.9rem 2rem !important;
    font-weight: 850 !important;
    font-size: 0.98rem !important;
    box-shadow:
        0 16px 34px rgba(220,38,38,0.30),
        inset 0 1px 0 rgba(255,255,255,0.35);
    transition: all 0.2s ease-in-out;
}

div.stButton > button:hover {
    transform: translateY(-3px) scale(1.015);
    box-shadow:
        0 24px 48px rgba(220,38,38,0.40),
        inset 0 1px 0 rgba(255,255,255,0.45);
}

.score {
    font-size: 4.8rem;
    line-height: 1;
    font-weight: 900;
    letter-spacing: -0.07em;
    margin: 0.4rem 0 0.7rem;
}

.low-text { color: #15803d; }
.medium-text { color: #d97706; }
.high-text { color: #dc2626; animation: pulseRisk 1.8s infinite; }

@keyframes pulseRisk {
    0%, 100% { filter: drop-shadow(0 0 0 rgba(220,38,38,0)); }
    50% { filter: drop-shadow(0 0 12px rgba(220,38,38,0.22)); }
}

.badge {
    display: inline-flex;
    border-radius: 999px;
    padding: 0.4rem 0.9rem;
    font-weight: 800;
    font-size: 0.82rem;
}

.badge-low { background: #dcfce7; color: #166534; }
.badge-medium { background: #fef3c7; color: #92400e; }
.badge-high { background: #fee2e2; color: #991b1b; }

.progress-wrap {
    background: rgba(226,232,240,0.85);
    border-radius: 999px;
    height: 14px;
    overflow: hidden;
    margin: 1rem 0 0.5rem;
}

.progress-fill {
    height: 100%;
    border-radius: 999px;
    animation: grow 0.95s ease-out both;
}

@keyframes grow {
    from { width: 0%; }
}

.metric-row {
    display: flex;
    justify-content: space-between;
    border-bottom: 1px solid rgba(203,213,225,0.75);
    padding: 0.6rem 0;
    gap: 1rem;
}

.metric-k {
    color: #64748b;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.76rem;
}

.metric-v {
    font-weight: 750;
    text-align: right;
}

.driver {
    border-bottom: 1px solid rgba(203,213,225,0.75);
    padding: 0.75rem 0;
}

.driver-title {
    font-weight: 800;
    color: #111827;
}

.driver-desc {
    color: #64748b;
    font-size: 0.86rem;
    line-height: 1.55;
}

.footer-note {
    text-align: center;
    color: #64748b;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)


# ── Helper functions ─────────────────────────────────────────────────────────
def esc(x):
    return html.escape(str(x))


def render_html(code):
    st.markdown(code, unsafe_allow_html=True)


def bodily_injuries_label_to_value(label):
    return {
        "None": 0,
        "One reported injury": 1,
        "Multiple / serious injuries": 2,
    }[label]


def witnesses_label_to_value(label):
    return {
        "No witnesses": 0,
        "One witness": 1,
        "Two witnesses": 2,
        "Three or more witnesses": 3,
    }[label]


def risk_meta(fraud_prob):
    if fraud_prob < 0.25:
        return "low", "Low Risk", "badge-low", "low-text", "#16a34a"
    elif fraud_prob < 0.50:
        return "medium", "Medium Risk", "badge-medium", "medium-text", "#f97316"
    return "high", "High Risk", "badge-high", "high-text", "#dc2626"


def action_meta(fraud_prob):
    if fraud_prob >= 0.50:
        return (
            "Manual investigation required",
            "This claim should be reviewed by an investigator before payout."
        )
    elif fraud_prob >= THRESHOLD:
        return (
            "Secondary review recommended",
            "The score is above the operating threshold. Request supporting documents before approval."
        )
    return (
        "Standard processing route",
        "No elevated fraud signal was detected from the entered claim details."
    )


# ── Header ───────────────────────────────────────────────────────────────────
render_html("""
<div class="hero">
  <div class="kicker">Auto Insurance Claims · Fraud Risk Scoring</div>
  <h1 class="hero-title">Insurance Fraud<br>Detection</h1>
  <p class="hero-sub">
    A portfolio machine-learning app for triaging vehicle insurance claims using claim details,
    policy information, and incident-level risk signals.
  </p>
  <div class="road-rule"></div>
</div>
""")


# ── Inputs ───────────────────────────────────────────────────────────────────
left, right = st.columns(2, gap="large")

with left:
    render_html("""
<div class="card">
  <div class="section-label">01 · Incident profile</div>
  <div class="heading">Vehicle incident details</div>
  <div class="note">Describe the reported collision, damage severity, injuries, witnesses, and customer tenure.</div>
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

    number_of_vehicles_involved = st.slider(
        "Vehicles Involved",
        min_value=1,
        max_value=4,
        value=1,
    )

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

    months_as_customer = st.number_input(
        "Months as Customer",
        min_value=0,
        value=200,
    )

with right:
    render_html("""
<div class="card">
  <div class="section-label">02 · Policy and claim amount</div>
  <div class="heading">Claim financial profile</div>
  <div class="note">Enter the claim amount, sub-claims, premium, and deductible used by the model.</div>
</div>
""")

    total_claim_amount = st.number_input("Total Claim Amount ($)", min_value=0, value=50000)
    injury_claim = st.number_input("Injury Claim ($)", min_value=0, value=5000)
    property_claim = st.number_input("Property Claim ($)", min_value=0, value=10000)
    vehicle_claim = st.number_input("Vehicle Claim ($)", min_value=0, value=35000)
    policy_annual_premium = st.number_input("Annual Premium ($)", min_value=0.0, value=1200.0, step=10.0)
    policy_deductable = st.number_input("Policy Deductible ($)", min_value=0, value=1000)

predict = st.button("Run claim risk assessment →")


# ── Prediction ───────────────────────────────────────────────────────────────
if predict:
    input_data = template_row.copy()

    input_data.loc[:, "incident_severity"] = incident_severity
    input_data.loc[:, "incident_type"] = incident_type
    input_data.loc[:, "number_of_vehicles_involved"] = number_of_vehicles_involved
    input_data.loc[:, "bodily_injuries"] = bodily_injuries
    input_data.loc[:, "witnesses"] = witnesses
    input_data.loc[:, "months_as_customer"] = months_as_customer
    input_data.loc[:, "total_claim_amount"] = total_claim_amount
    input_data.loc[:, "injury_claim"] = injury_claim
    input_data.loc[:, "property_claim"] = property_claim
    input_data.loc[:, "vehicle_claim"] = vehicle_claim
    input_data.loc[:, "policy_annual_premium"] = policy_annual_premium
    input_data.loc[:, "policy_deductable"] = policy_deductable

    fraud_prob = model.predict_proba(input_data)[0, 1]
    fraud_pred = int(fraud_prob >= THRESHOLD)

    risk_cls, risk_label, badge_cls, text_cls, risk_color = risk_meta(fraud_prob)
    action_title, action_desc = action_meta(fraud_prob)

    pct = round(fraud_prob * 100, 1)
    verdict = "Likely Fraudulent" if fraud_pred == 1 else "Likely Legitimate"

    st.markdown("<br>", unsafe_allow_html=True)

    result_col, action_col = st.columns(2, gap="large")

    with result_col:
        render_html(f"""
<div class="card">
  <div class="section-label">03 · Model output</div>
  <div class="heading">Fraud probability score</div>
  <div class="note">The model estimates how strongly the entered claim resembles a fraud-risk case.</div>

  <div class="score {text_cls}">{pct:.0f}%</div>

  <div class="progress-wrap">
    <div class="progress-fill" style="width:{pct}%; background:{risk_color};"></div>
  </div>

  <div class="metric-row">
    <span class="metric-k">Decision threshold</span>
    <span class="metric-v">{int(THRESHOLD * 100)}%</span>
  </div>

  <div class="metric-row">
    <span class="metric-k">Prediction</span>
    <span class="metric-v">{esc(verdict)}</span>
  </div>

  <br>
  <span class="badge {badge_cls}">● {esc(risk_label)}</span>
</div>
""")

    with action_col:
        render_html(f"""
<div class="card">
  <div class="section-label">04 · Claim routing</div>
  <div class="heading">Recommended handling path</div>
  <div class="note">The output supports triage and does not replace professional investigation.</div>

  <h3 style="margin-top:1rem; font-size:1.35rem;">{esc(action_title)}</h3>
  <p style="color:#4b5563; line-height:1.7;">{esc(action_desc)}</p>

  <div class="metric-row">
    <span class="metric-k">Model</span>
    <span class="metric-v">Random Forest</span>
  </div>

  <div class="metric-row">
    <span class="metric-k">Features</span>
    <span class="metric-v">12 deployment inputs</span>
  </div>

  <div class="metric-row">
    <span class="metric-k">Use case</span>
    <span class="metric-v">Claim triage</span>
  </div>
</div>
""")

    risk_drivers = []

    if incident_severity in ["Major Damage", "Total Loss"]:
        risk_drivers.append((
            "Severe vehicle damage",
            "Major damage or total loss can increase the need for manual claim review."
        ))

    if total_claim_amount >= 60000:
        risk_drivers.append((
            "Large claim amount",
            "The total claim amount is above $60,000."
        ))

    if number_of_vehicles_involved >= 2:
        risk_drivers.append((
            "Multi-vehicle incident",
            "Multi-vehicle incidents are more complex and may require additional validation."
        ))

    if bodily_injuries >= 1:
        risk_drivers.append((
            "Injury component present",
            "Bodily injury claims often require more supporting documentation."
        ))

    if witnesses >= 2:
        risk_drivers.append((
            "Multiple witnesses",
            "The number of witnesses can affect claim investigation priority."
        ))

    if months_as_customer < 24:
        risk_drivers.append((
            "Short customer history",
            "A shorter policy history can be a mild review signal."
        ))

    if not risk_drivers:
        drivers_html = """
<div class="driver">
  <div class="driver-title">No major review triggers</div>
  <div class="driver-desc">The entered values did not activate the main rule-based risk notes.</div>
</div>
"""
    else:
        drivers_html = ""
        for title, desc in risk_drivers:
            drivers_html += f"""
<div class="driver">
  <div class="driver-title">{esc(title)}</div>
  <div class="driver-desc">{esc(desc)}</div>
</div>
"""

    render_html(f"""
<div class="card">
  <div class="section-label">05 · Review signals</div>
  <div class="heading">Key factors behind the recommendation</div>
  <div class="note">These notes explain which entered values may have influenced the routing decision.</div>
  {drivers_html}
</div>
""")

    render_html("""
<p class="footer-note">
Portfolio demonstration · Supports claim triage and human review, not automatic denial or approval.
</p>
""")