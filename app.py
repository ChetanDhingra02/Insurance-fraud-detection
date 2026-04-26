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
        radial-gradient(circle at 12% 20%, rgba(250,204,21,0.13), transparent 28%),
        radial-gradient(circle at 88% 14%, rgba(59,130,246,0.12), transparent 30%),
        linear-gradient(135deg, #f8fafc 0%, #eef2f7 52%, #f7f4ec 100%);
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(90deg, rgba(15,23,42,0.035) 1px, transparent 1px),
        linear-gradient(rgba(15,23,42,0.028) 1px, transparent 1px);
    background-size: 56px 56px;
    pointer-events: none;
}

.main .block-container {
    max-width: 1180px;
    padding: 2.4rem 2.2rem 5rem;
}

[data-testid="stHeader"] {
    background: transparent;
}

.hero {
    background: linear-gradient(135deg, rgba(17,24,39,0.94), rgba(51,65,85,0.92));
    color: white;
    border-radius: 30px;
    padding: 2.4rem;
    margin-bottom: 1.6rem;
    box-shadow: 0 28px 70px rgba(15,23,42,0.22);
    overflow: hidden;
    position: relative;
    animation: riseIn 0.6s ease both;
}

.hero::after {
    content: "";
    position: absolute;
    left: 0;
    right: 0;
    bottom: 26px;
    height: 7px;
    background: repeating-linear-gradient(
        90deg,
        #facc15 0 56px,
        transparent 56px 88px
    );
    opacity: 0.85;
    animation: roadMove 3s linear infinite;
}

@keyframes roadMove {
    from { background-position: 0 0; }
    to { background-position: 176px 0; }
}

.card {
    background: rgba(255,255,255,0.72);
    backdrop-filter: blur(20px) saturate(160%);
    -webkit-backdrop-filter: blur(20px) saturate(160%);
    border: 1px solid rgba(255,255,255,0.72);
    border-radius: 24px;
    padding: 1.5rem 1.6rem;
    margin-bottom: 1.15rem;
    box-shadow:
        0 20px 50px rgba(15,23,42,0.11),
        inset 0 1px 0 rgba(255,255,255,0.8);
    animation: riseIn 0.55s ease both;
    transition: transform 0.22s ease, box-shadow 0.22s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow:
        0 28px 70px rgba(15,23,42,0.15),
        inset 0 1px 0 rgba(255,255,255,0.9);
}

@keyframes riseIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.kicker,
.section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #64748b;
    font-weight: 700;
    margin-bottom: 0.7rem;
}

.hero .kicker {
    color: #cbd5e1;
}

.hero-title {
    font-size: clamp(2.8rem, 5vw, 4.7rem);
    line-height: 0.96;
    font-weight: 900;
    letter-spacing: -0.06em;
    margin: 0;
    color: white;
}

.hero-sub {
    color: #e5e7eb;
    max-width: 780px;
    font-size: 1rem;
    line-height: 1.7;
    margin-top: 1rem;
    margin-bottom: 2rem;
}

.heading {
    font-size: 1.55rem;
    font-weight: 850;
    letter-spacing: -0.04em;
    margin-bottom: 0.45rem;
    color: #0f172a;
}

.note {
    color: #475569;
    font-size: 0.95rem;
    line-height: 1.65;
}

label,
div[data-testid="stWidgetLabel"] p {
    font-weight: 700 !important;
    color: #1f2937 !important;
    font-size: 0.88rem !important;
}

div[data-baseweb="select"] > div,
[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.92) !important;
    border: 1.5px solid rgba(100,116,139,0.35) !important;
    border-radius: 14px !important;
    min-height: 45px !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    font-weight: 600 !important;
    box-shadow: 0 10px 25px rgba(15,23,42,0.06) !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] input,
[data-testid="stNumberInput"] input {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    opacity: 1 !important;
}

div[data-baseweb="select"] svg {
    color: #f59e0b !important;
    opacity: 1 !important;
}

div[data-baseweb="select"] > div:hover,
[data-testid="stNumberInput"] input:focus {
    border-color: rgba(245,158,11,0.8) !important;
    box-shadow:
        0 0 0 4px rgba(245,158,11,0.15),
        0 16px 35px rgba(15,23,42,0.10) !important;
}

[data-baseweb="menu"] {
    background: rgba(255,255,255,0.97) !important;
    color: #111827 !important;
    border-radius: 14px !important;
}

[data-baseweb="option"] {
    color: #111827 !important;
    font-weight: 600 !important;
}

[data-testid="stNumberInput"] button {
    background: #1f2937 !important;
    color: white !important;
    border: none !important;
}

[data-testid="stNumberInput"] button:hover {
    background: #f59e0b !important;
}

[data-testid="stSlider"] [role="slider"],
[data-testid="stSelectSlider"] [role="slider"] {
    background:
        radial-gradient(circle, #f8fafc 0 13%, #111827 14% 34%, #475569 35% 58%, #111827 59% 100%) !important;
    border: 3px solid #ffffff !important;
    width: 25px !important;
    height: 25px !important;
    box-shadow: 0 5px 14px rgba(15,23,42,0.34) !important;
}

div.stButton > button {
    background: linear-gradient(135deg, #f59e0b, #d97706) !important;
    color: #111827 !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 0.9rem 2rem !important;
    font-weight: 850 !important;
    font-size: 0.98rem !important;
    box-shadow: 0 18px 38px rgba(217,119,6,0.28);
    transition: 0.2s ease-in-out;
}

div.stButton > button:hover {
    transform: translateY(-3px) scale(1.01);
    box-shadow: 0 24px 48px rgba(217,119,6,0.36);
}

.score {
    font-size: 5rem;
    line-height: 1;
    font-weight: 900;
    letter-spacing: -0.07em;
    margin: 0.35rem 0 0.8rem;
}

.low-text { color: #15803d; }
.medium-text { color: #d97706; }
.high-text { color: #dc2626; }

.badge {
    display: inline-flex;
    border-radius: 999px;
    padding: 0.42rem 0.95rem;
    font-weight: 800;
    font-size: 0.84rem;
}

.badge-low { background: #dcfce7; color: #166534; }
.badge-medium { background: #fef3c7; color: #92400e; }
.badge-high { background: #fee2e2; color: #991b1b; }

.progress-wrap {
    background: rgba(226,232,240,0.9);
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
    padding: 0.62rem 0;
    gap: 1rem;
}

.metric-k {
    color: #64748b;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.76rem;
}

.metric-v {
    font-weight: 800;
    text-align: right;
    color: #111827;
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

.gauge-wrap {
    margin-top: 1.1rem;
    background: rgba(15,23,42,0.04);
    border-radius: 20px;
    padding: 1rem;
}

.gauge-track {
    height: 18px;
    border-radius: 999px;
    background: linear-gradient(90deg, #22c55e 0%, #facc15 45%, #f97316 70%, #ef4444 100%);
    position: relative;
    overflow: hidden;
}

.gauge-marker {
    position: absolute;
    top: -7px;
    width: 8px;
    height: 32px;
    border-radius: 999px;
    background: #111827;
    box-shadow: 0 5px 14px rgba(15,23,42,0.35);
    animation: markerPop 0.8s ease both;
}

@keyframes markerPop {
    from { transform: scaleY(0); opacity: 0; }
    to { transform: scaleY(1); opacity: 1; }
}

.gauge-labels {
    display: flex;
    justify-content: space-between;
    color: #64748b;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    margin-top: 0.5rem;
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


render_html("""
<div class="hero">
  <div class="kicker">Auto Insurance Claims · Fraud Risk Scoring</div>
  <h1 class="hero-title">Insurance Fraud<br>Detection</h1>
  <p class="hero-sub">
    A portfolio machine-learning app for triaging vehicle insurance claims using claim details,
    policy information, and incident-level risk signals.
  </p>
</div>
""")


left, right = st.columns(2, gap="large")

with left:
    render_html("""
<div class="card">
  <div class="section-label">01 · Incident profile</div>
  <div class="heading">Vehicle incident details</div>
  <div class="note">Describe the collision, damage severity, injuries, witnesses, and customer tenure.</div>
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
    marker_left = min(max(pct, 1), 98)

    st.markdown("<br>", unsafe_allow_html=True)

    result_col, action_col = st.columns(2, gap="large")

    with result_col:
        render_html(f"""
<div class="card">
  <div class="section-label">03 · Model output</div>
  <div class="heading">Fraud probability score</div>
  <div class="note">The model estimates how strongly the claim resembles a fraud-risk case.</div>

  <div class="score {text_cls}">{pct:.0f}%</div>

  <div class="progress-wrap">
    <div class="progress-fill" style="width:{pct}%; background:{risk_color};"></div>
  </div>

  <div class="gauge-wrap">
    <div class="gauge-track">
      <div class="gauge-marker" style="left:{marker_left}%;"></div>
    </div>
    <div class="gauge-labels">
      <span>Low</span>
      <span>Review</span>
      <span>High</span>
    </div>
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

  <h3 style="margin-top:1rem; font-size:1.35rem; color:#111827;">{esc(action_title)}</h3>
  <p style="color:#475569; line-height:1.7;">{esc(action_desc)}</p>

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