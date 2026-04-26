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
    page_icon="📊",
    layout="wide",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    color: #111827 !important;
}

.stApp {
    background:
        radial-gradient(circle at 12% 15%, rgba(95,143,50,0.08), transparent 26%),
        radial-gradient(circle at 88% 22%, rgba(59,130,246,0.06), transparent 26%),
        #f8f5ec;
}

.main .block-container {
    max-width: 1180px;
    padding: 2.6rem 2.2rem 5rem;
}

[data-testid="stHeader"] {
    background: transparent;
}

.hero, .card {
    background: #fffdf8;
    border: 1.5px solid #1f2937;
    border-radius: 20px;
    box-shadow: 4px 4px 0 rgba(31,41,55,0.12);
}

.hero {
    padding: 2rem;
    margin-bottom: 1.4rem;
}

.card {
    padding: 1.35rem 1.45rem;
    margin-bottom: 1rem;
}

.kicker, .section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #6b7280;
    font-weight: 600;
    margin-bottom: 0.6rem;
}

.hero-title {
    font-size: clamp(2.4rem, 5vw, 4rem);
    line-height: 1;
    font-weight: 800;
    letter-spacing: -0.045em;
    margin: 0;
    color: #111827;
}

.hero-sub, .note {
    color: #4b5563;
    font-size: 0.95rem;
    line-height: 1.65;
}

.heading {
    font-size: 1.55rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 0.45rem;
    color: #111827;
}

.dot-row {
    display: flex;
    gap: 0.45rem;
    margin-top: 1rem;
}

.dot {
    width: 11px;
    height: 11px;
    border-radius: 50%;
}

.red { background: #ef4444; }
.orange { background: #f97316; }
.green { background: #22c55e; }
.blue { background: #38bdf8; }
.purple { background: #a855f7; }

label,
div[data-testid="stWidgetLabel"] p {
    font-weight: 650 !important;
    color: #111827 !important;
    font-size: 0.86rem !important;
}

div[data-baseweb="select"] > div,
[data-testid="stNumberInput"] input {
    background: #ffffff !important;
    border: 1.5px solid #d1d5db !important;
    border-radius: 10px !important;
    min-height: 42px !important;
    box-shadow: none !important;
}

div[data-baseweb="select"] > div:hover,
[data-testid="stNumberInput"] input:focus {
    border-color: #5f8f32 !important;
    box-shadow: 0 0 0 3px rgba(95,143,50,0.15) !important;
}

[data-testid="stSlider"] [role="slider"],
[data-testid="stSelectSlider"] [role="slider"] {
    background: #5f8f32 !important;
    border: 2px solid white !important;
}

div.stButton > button {
    background: #5f8f32 !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.8rem 1.8rem !important;
    font-weight: 750 !important;
    font-size: 0.95rem !important;
    box-shadow: 0 8px 20px rgba(95,143,50,0.22);
    transition: 0.15s ease-in-out;
}

div.stButton > button:hover {
    background: #4f7d28 !important;
    transform: translateY(-1px);
}

.score {
    font-size: 4.6rem;
    line-height: 1;
    font-weight: 800;
    letter-spacing: -0.06em;
    margin: 0.4rem 0 0.7rem;
}

.low-text { color: #15803d; }
.medium-text { color: #d97706; }
.high-text { color: #dc2626; }

.badge {
    display: inline-flex;
    border-radius: 999px;
    padding: 0.35rem 0.85rem;
    font-weight: 750;
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
    margin: 1rem 0 0.4rem;
}

.progress-fill {
    height: 100%;
    border-radius: 999px;
}

.metric-row {
    display: flex;
    justify-content: space-between;
    border-bottom: 1px solid #e5e7eb;
    padding: 0.55rem 0;
    gap: 1rem;
}

.metric-k {
    color: #6b7280;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.76rem;
}

.metric-v {
    font-weight: 700;
    text-align: right;
}

.bar-row {
    display: grid;
    grid-template-columns: 90px 1fr 90px;
    gap: 0.8rem;
    align-items: center;
    margin-bottom: 0.85rem;
}

.bar-track {
    height: 18px;
    background: #f3f4f6;
    border-radius: 999px;
    overflow: hidden;
    border: 1px solid #d1d5db;
}

.bar-fill {
    height: 100%;
    border-radius: 999px;
}

.driver {
    border-bottom: 1px solid #e5e7eb;
    padding: 0.72rem 0;
}

.driver-title {
    font-weight: 750;
    color: #111827;
}

.driver-desc {
    color: #6b7280;
    font-size: 0.86rem;
    line-height: 1.5;
}

.footer-note {
    text-align: center;
    color: #6b7280;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)


# ── Helper functions ─────────────────────────────────────────────────────────
def esc(x):
    return html.escape(str(x))


def money(x):
    return f"${x:,.0f}"


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
        return "low", "Low Risk", "badge-low", "low-text", "#22c55e"
    elif fraud_prob < 0.50:
        return "medium", "Medium Risk", "badge-medium", "medium-text", "#f97316"
    return "high", "High Risk", "badge-high", "high-text", "#ef4444"


def action_meta(fraud_prob):
    if fraud_prob >= 0.50:
        return (
            "Send for Manual Investigation",
            "The score is high. This claim should be reviewed by an investigator before payout."
        )
    elif fraud_prob >= THRESHOLD:
        return (
            "Flag for Secondary Review",
            "The score is above the decision threshold. Request supporting documentation and supervisor review."
        )
    return (
        "Process Normally",
        "No elevated risk signal was detected. The claim may proceed through the standard workflow."
    )


def make_bar(label, value, width, color):
    return (
        f'<div class="bar-row">'
        f'<div><b>{esc(label)}</b></div>'
        f'<div class="bar-track"><div class="bar-fill" style="width:{width}%; background:{color};"></div></div>'
        f'<div>{money(value)}</div>'
        f'</div>'
    )


# ── Header ───────────────────────────────────────────────────────────────────
render_html("""
<div class="hero">
  <div class="kicker">Machine Learning Portfolio Project</div>
  <h1 class="hero-title">Insurance Fraud<br>Detection</h1>
  <p class="hero-sub">
    A clean claim-risk scoring app that turns claim details into a fraud probability,
    risk band, and recommended review action.
  </p>
  <div class="dot-row">
    <div class="dot red"></div>
    <div class="dot orange"></div>
    <div class="dot green"></div>
    <div class="dot blue"></div>
    <div class="dot purple"></div>
  </div>
</div>
""")


# ── Inputs ───────────────────────────────────────────────────────────────────
left, right = st.columns(2, gap="large")

with left:
    render_html("""
<div class="card">
  <div class="section-label">01 · Incident details</div>
  <div class="heading">Show the claim event</div>
  <div class="note">These fields describe what happened during the reported incident.</div>
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
  <div class="section-label">02 · Policy and claim values</div>
  <div class="heading">Show the money data</div>
  <div class="note">These inputs describe the size and structure of the insurance claim.</div>
</div>
""")

    total_claim_amount = st.number_input("Total Claim Amount ($)", min_value=0, value=50000)
    injury_claim = st.number_input("Injury Claim ($)", min_value=0, value=5000)
    property_claim = st.number_input("Property Claim ($)", min_value=0, value=10000)
    vehicle_claim = st.number_input("Vehicle Claim ($)", min_value=0, value=35000)
    policy_annual_premium = st.number_input("Annual Premium ($)", min_value=0.0, value=1200.0, step=10.0)
    policy_deductable = st.number_input("Policy Deductable ($)", min_value=0, value=1000)

predict = st.button("Run Fraud Assessment →")


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
  <div class="heading">Show the fraud risk</div>
  <div class="note">The model converts the claim information into a fraud probability score.</div>
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
  <div class="section-label">04 · Recommended decision</div>
  <div class="heading">Show the action</div>
  <div class="note">The app does not replace human review. It supports triage and prioritization.</div>
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
    <span class="metric-k">Purpose</span>
    <span class="metric-v">Portfolio demo</span>
  </div>
</div>
""")

    other = max(0, total_claim_amount - injury_claim - property_claim - vehicle_claim)
    max_claim = max(injury_claim, property_claim, vehicle_claim, other, 1)

    injury_w = round(injury_claim / max_claim * 100, 1)
    property_w = round(property_claim / max_claim * 100, 1)
    vehicle_w = round(vehicle_claim / max_claim * 100, 1)
    other_w = round(other / max_claim * 100, 1)

    st.markdown("<br>", unsafe_allow_html=True)

    chart_col, driver_col = st.columns([1.2, 0.8], gap="large")

    with chart_col:
        bars_html = (
            make_bar("Injury", injury_claim, injury_w, "#ef4444") +
            make_bar("Property", property_claim, property_w, "#f97316") +
            make_bar("Vehicle", vehicle_claim, vehicle_w, "#38bdf8") +
            make_bar("Other", other, other_w, "#a855f7")
        )

        render_html(f"""
<div class="card">
  <div class="section-label">05 · Claim composition</div>
  <div class="heading">Show the data clearly</div>
  <div class="note">The claim is broken into injury, property, vehicle, and remaining claim amount.</div>
  {bars_html}
</div>
""")

    with driver_col:
        risk_drivers = []

        if incident_severity in ["Major Damage", "Total Loss"]:
            risk_drivers.append(("High incident severity", "Major damage or total loss can increase claim risk."))

        if total_claim_amount >= 60000:
            risk_drivers.append(("Large total claim", "The total claim amount is above $60,000."))

        if number_of_vehicles_involved >= 2:
            risk_drivers.append(("Multiple vehicles involved", "Multi-vehicle claims can be more complex to validate."))

        if bodily_injuries >= 1:
            risk_drivers.append(("Reported bodily injuries", "Injury-related claims may require additional verification."))

        if witnesses >= 2:
            risk_drivers.append(("High witness count", "A high witness count can be a useful review signal."))

        if months_as_customer < 24:
            risk_drivers.append(("Short customer tenure", "Newer policies may require closer claim review."))

        if not risk_drivers:
            drivers_html = """
<div class="driver">
  <div class="driver-title">No major risk indicators</div>
  <div class="driver-desc">The entered values did not trigger the main rule-based risk notes.</div>
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
  <div class="section-label">06 · Risk drivers</div>
  <div class="heading">Show the why</div>
  <div class="note">These notes explain which entered values may have contributed to the review decision.</div>
  {drivers_html}
</div>
""")

    render_html("""
<p class="footer-note">
Portfolio demonstration · The model supports human review and should not be used as the only decision-maker.
</p>
""")