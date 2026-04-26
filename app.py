import streamlit as st
import joblib
import html

model = joblib.load("deploy_fraud_model.pkl")
template_row = joblib.load("deploy_input_template.pkl")
THRESHOLD = 0.25

st.set_page_config(
    page_title="Insurance Fraud Detection",
    page_icon="🚗",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    color: #111827 !important;
}

.stApp {
    background:
        radial-gradient(circle at 12% 18%, rgba(220, 38, 38, 0.10), transparent 26%),
        radial-gradient(circle at 82% 16%, rgba(37, 99, 235, 0.10), transparent 28%),
        linear-gradient(135deg, #f6f7f9 0%, #eef1f5 100%);
}

/* subtle road lines */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(90deg, rgba(17,24,39,0.045) 1px, transparent 1px),
        linear-gradient(rgba(17,24,39,0.035) 1px, transparent 1px);
    background-size: 56px 56px;
    pointer-events: none;
}

.main .block-container {
    max-width: 1180px;
    padding: 2.5rem 2.2rem 5rem;
}

[data-testid="stHeader"] {
    background: transparent;
}

.hero {
    background: linear-gradient(135deg, #111827 0%, #1f2937 58%, #334155 100%);
    border-radius: 28px;
    padding: 2.3rem;
    margin-bottom: 1.5rem;
    color: white;
    box-shadow: 0 22px 60px rgba(15,23,42,0.24);
    position: relative;
    overflow: hidden;
    animation: fadeUp 0.55s ease both;
}

.hero::after {
    content: "";
    position: absolute;
    right: -80px;
    top: -80px;
    width: 300px;
    height: 300px;
    border: 34px solid rgba(255,255,255,0.06);
    border-radius: 50%;
}

.kicker {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.73rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #cbd5e1;
    font-weight: 600;
    margin-bottom: 0.7rem;
}

.hero-title {
    font-size: clamp(2.7rem, 5vw, 4.6rem);
    line-height: 0.96;
    font-weight: 900;
    letter-spacing: -0.055em;
    margin: 0;
    color: white;
}

.hero-sub {
    max-width: 780px;
    color: #d1d5db;
    font-size: 1rem;
    line-height: 1.7;
    margin-top: 1rem;
}

.card {
    background: rgba(255,255,255,0.82);
    backdrop-filter: blur(18px);
    border: 1px solid rgba(148,163,184,0.45);
    border-radius: 22px;
    padding: 1.45rem 1.55rem;
    margin-bottom: 1.1rem;
    box-shadow: 0 18px 42px rgba(15,23,42,0.10);
    animation: fadeUp 0.5s ease both;
    transition: transform 0.22s ease, box-shadow 0.22s ease;
}

.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 24px 54px rgba(15,23,42,0.14);
}

.section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #64748b;
    font-weight: 600;
    margin-bottom: 0.6rem;
}

.heading {
    font-size: 1.55rem;
    font-weight: 850;
    letter-spacing: -0.035em;
    margin-bottom: 0.45rem;
    color: #111827;
}

.note {
    color: #64748b;
    font-size: 0.94rem;
    line-height: 1.65;
}

.road-rule {
    height: 7px;
    margin-top: 1.2rem;
    border-radius: 999px;
    background: repeating-linear-gradient(
        90deg,
        #facc15 0 42px,
        transparent 42px 66px
    );
    opacity: 0.85;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(18px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(220,38,38,0.22); }
    50% { box-shadow: 0 0 0 9px rgba(220,38,38,0.02); }
}

/* Inputs */
label,
div[data-testid="stWidgetLabel"] p {
    font-weight: 700 !important;
    color: #111827 !important;
    font-size: 0.86rem !important;
}

div[data-baseweb="select"] > div,
[data-testid="stNumberInput"] input {
    background: #ffffff !important;
    border: 1.5px solid #d1d5db !important;
    border-radius: 12px !important;
    min-height: 43px !important;
}

div[data-baseweb="select"] > div:hover,
[data-testid="stNumberInput"] input:focus {
    border-color: #dc2626 !important;
    box-shadow: 0 0 0 3px rgba(220,38,38,0.13) !important;
}

/* tire-like slider knob */
[data-testid="stSlider"] [role="slider"],
[data-testid="stSelectSlider"] [role="slider"] {
    background: radial-gradient(circle, #111827 0 32%, #374151 33% 58%, #111827 59% 100%) !important;
    border: 3px solid #ffffff !important;
    width: 24px !important;
    height: 24px !important;
    box-shadow: 0 4px 12px rgba(17,24,39,0.32) !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] > div,
[data-testid="stSelectSlider"] [data-baseweb="slider"] > div {
    color: #dc2626 !important;
}

div.stButton > button {
    background: linear-gradient(135deg, #dc2626, #991b1b) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.85rem 1.9rem !important;
    font-weight: 800 !important;
    font-size: 0.96rem !important;
    box-shadow: 0 12px 28px rgba(220,38,38,0.28);
    transition: 0.18s ease-in-out;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 18px 38px rgba(220,38,38,0.35);
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
.high-text { color: #dc2626; animation: pulse 1.8s infinite; }

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
    background: #e5e7eb;
    border-radius: 999px;
    height: 14px;
    overflow: hidden;
    margin: 1rem 0 0.5rem;
}

.progress-fill {
    height: 100%;
    border-radius: 999px;
    animation: grow 0.9s ease-out both;
}

@keyframes grow {
    from { width: 0%; }
}

.metric-row {
    display: flex;
    justify-content: space-between;
    border-bottom: 1px solid #e5e7eb;
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
    border-bottom: 1px solid #e5e7eb;
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
        ["Minor Damage", "Major Damage", "Total Loss", "Trivial Damage"]
    )

    incident_type = st.selectbox(
        "Incident Type",
        ["Single Vehicle Collision", "Multi-vehicle Collision", "Vehicle Theft", "Parked Car"]
    )

    number_of_vehicles_involved = st.slider(
        "Vehicles Involved",
        min_value=1,
        max_value=4,
        value=1
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
        "Months as Customer",
        min_value=0,
        value=200
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
        risk_drivers.append(("Severe vehicle damage", "Major damage or total loss can increase the need for manual claim review."))

    if total_claim_amount >= 60000:
        risk_drivers.append(("Large claim amount", "The total claim amount is above $60,000."))

    if number_of_vehicles_involved >= 2:
        risk_drivers.append(("Multi-vehicle incident", "Multi-vehicle incidents are more complex and may require additional validation."))

    if bodily_injuries >= 1:
        risk_drivers.append(("Injury component present", "Bodily injury claims often require more supporting documentation."))

    if witnesses >= 2:
        risk_drivers.append(("Multiple witnesses", "The number of witnesses can affect claim investigation priority."))

    if months_as_customer < 24:
        risk_drivers.append(("Short customer history", "A shorter policy history can be a mild review signal."))

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