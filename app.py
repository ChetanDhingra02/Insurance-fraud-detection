import streamlit as st
import pandas as pd
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

# ── Theme CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Gaegu:wght@400;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    color: #111827 !important;
}

.stApp {
    background:
        radial-gradient(circle at 15% 12%, rgba(239, 68, 68, 0.05), transparent 26%),
        radial-gradient(circle at 88% 20%, rgba(34, 197, 94, 0.06), transparent 24%),
        radial-gradient(circle at 70% 85%, rgba(59, 130, 246, 0.06), transparent 24%),
        #faf8f1;
}

.main .block-container {
    max-width: 1180px;
    padding: 2.8rem 2.3rem 5rem;
}

[data-testid="stHeader"] {
    background: transparent;
}

.story-shell {
    background: rgba(255,255,255,0.72);
    border: 2px solid #111827;
    border-radius: 28px;
    padding: 2rem 2rem 1.6rem;
    box-shadow: 8px 8px 0 rgba(17,24,39,0.13);
    margin-bottom: 1.5rem;
}

.kicker {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.74rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 0.55rem;
}

.hero-title {
    font-family: 'Gaegu', cursive;
    font-size: clamp(3.1rem, 7vw, 5.2rem);
    line-height: 0.88;
    font-weight: 700;
    margin: 0;
    color: #111827;
}

.hero-sub {
    max-width: 780px;
    color: #4b5563;
    font-size: 1rem;
    line-height: 1.7;
    margin-top: 1rem;
}

.story-card {
    background: #ffffff;
    border: 2px solid #111827;
    border-radius: 22px;
    padding: 1.4rem 1.45rem;
    box-shadow: 5px 5px 0 rgba(17,24,39,0.11);
    margin-bottom: 1rem;
}

.story-heading {
    font-family: 'Gaegu', cursive;
    font-size: 2.35rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.75rem;
}

.story-note {
    color: #6b7280;
    font-size: 0.9rem;
    line-height: 1.55;
    margin-bottom: 1rem;
}

.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: #6b7280;
    margin-bottom: 0.8rem;
}

.dot-row {
    display: flex;
    gap: 0.55rem;
    margin: 1rem 0 0.3rem;
}

.dot {
    width: 13px;
    height: 13px;
    border-radius: 50%;
    border: 2px solid #111827;
}

.red { background: #ef4444; }
.orange { background: #f97316; }
.green { background: #22c55e; }
.blue { background: #38bdf8; }
.purple { background: #a855f7; }

label,
div[data-testid="stWidgetLabel"] p {
    font-weight: 700 !important;
    color: #111827 !important;
    font-size: 0.88rem !important;
}

div[data-baseweb="select"] > div,
[data-testid="stNumberInput"] input {
    background: #fffdf8 !important;
    border: 2px solid #111827 !important;
    border-radius: 14px !important;
    min-height: 44px !important;
    box-shadow: 3px 3px 0 rgba(17,24,39,0.10);
}

div[data-baseweb="select"] > div:hover,
[data-testid="stNumberInput"] input:focus {
    box-shadow: 4px 4px 0 rgba(17,24,39,0.16) !important;
    border-color: #111827 !important;
}

[data-testid="stSlider"] [role="slider"],
[data-testid="stSelectSlider"] [role="slider"] {
    background: #6a9f37 !important;
    border: 2px solid #111827 !important;
}

div.stButton > button {
    background: #6a9f37 !important;
    color: white !important;
    border: 2px solid #111827 !important;
    border-radius: 18px !important;
    padding: 0.85rem 2.4rem !important;
    font-weight: 800 !important;
    font-size: 1rem !important;
    box-shadow: 5px 5px 0 rgba(17,24,39,0.20);
    transition: 0.15s ease-in-out;
}

div.stButton > button:hover {
    transform: translate(-2px, -2px);
    box-shadow: 7px 7px 0 rgba(17,24,39,0.22);
}

.result-score {
    font-family: 'Gaegu', cursive;
    font-size: 6rem;
    line-height: 0.85;
    font-weight: 700;
    margin: 0.4rem 0 0.7rem;
}

.low-text { color: #15803d; }
.medium-text { color: #d97706; }
.high-text { color: #dc2626; }

.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    border: 2px solid #111827;
    border-radius: 999px;
    padding: 0.35rem 0.8rem;
    font-weight: 800;
    font-size: 0.82rem;
    box-shadow: 3px 3px 0 rgba(17,24,39,0.12);
}

.badge-low { background: #dcfce7; color: #166534; }
.badge-medium { background: #fef3c7; color: #92400e; }
.badge-high { background: #fee2e2; color: #991b1b; }

.progress-wrap {
    background: #f3f4f6;
    border: 2px solid #111827;
    border-radius: 999px;
    height: 20px;
    overflow: hidden;
    margin: 1rem 0 0.4rem;
}

.progress-fill {
    height: 100%;
    border-right: 2px solid #111827;
}

.driver {
    border-bottom: 1px dashed #9ca3af;
    padding: 0.72rem 0;
}

.driver-title {
    font-weight: 800;
    color: #111827;
    margin-bottom: 0.18rem;
}

.driver-desc {
    color: #6b7280;
    font-size: 0.86rem;
    line-height: 1.5;
}

.metric-row {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    border-bottom: 1px dashed #d1d5db;
    padding: 0.5rem 0;
}

.metric-k {
    color: #6b7280;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
}

.metric-v {
    font-weight: 800;
    text-align: right;
}

.axis-box {
    border-left: 3px solid #111827;
    border-bottom: 3px solid #111827;
    padding: 1.2rem 0.8rem 0.8rem 1rem;
    min-height: 220px;
}

.bar-row {
    display: grid;
    grid-template-columns: 95px 1fr 80px;
    gap: 0.8rem;
    align-items: center;
    margin-bottom: 1rem;
    font-size: 0.86rem;
}

.bar-track {
    background: #f3f4f6;
    border: 2px solid #111827;
    border-radius: 999px;
    overflow: hidden;
    height: 23px;
}

.bar-fill {
    height: 100%;
    border-right: 2px solid #111827;
}

.footer-note {
    text-align: center;
    color: #6b7280;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────────────────────────
def bodily_injuries_label_to_value(label):
    return {
        "None": 0,
        "One reported injury": 1,
        "Multiple / serious injuries": 2
    }[label]


def witnesses_label_to_value(label):
    return {
        "No witnesses": 0,
        "One witness": 1,
        "Two witnesses": 2,
        "Three or more witnesses": 3
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


def money(x):
    return f"${x:,.0f}"


def safe_text(x):
    return html.escape(str(x))


def bar(width, color):
    width = max(0, min(100, width))
    return f"""
    <div class="bar-track">
        <div class="bar-fill" style="width:{width}%; background:{color};"></div>
    </div>
    """


# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="story-shell">
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
""", unsafe_allow_html=True)


# ── Inputs ───────────────────────────────────────────────────────────────────
left, right = st.columns(2, gap="large")

with left:
    st.markdown("""
    <div class="story-card">
        <div class="section-label">01 · Incident details</div>
        <div class="story-heading">Show the claim event</div>
        <div class="story-note">
            These fields describe what happened during the reported incident.
        </div>
    </div>
    """, unsafe_allow_html=True)

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
    st.markdown("""
    <div class="story-card">
        <div class="section-label">02 · Policy and claim values</div>
        <div class="story-heading">Show the money data</div>
        <div class="story-note">
            These inputs describe the size and structure of the insurance claim.
        </div>
    </div>
    """, unsafe_allow_html=True)

    total_claim_amount = st.number_input(
        "Total Claim Amount ($)",
        min_value=0,
        value=50000
    )

    injury_claim = st.number_input(
        "Injury Claim ($)",
        min_value=0,
        value=5000
    )

    property_claim = st.number_input(
        "Property Claim ($)",
        min_value=0,
        value=10000
    )

    vehicle_claim = st.number_input(
        "Vehicle Claim ($)",
        min_value=0,
        value=35000
    )

    policy_annual_premium = st.number_input(
        "Annual Premium ($)",
        min_value=0.0,
        value=1200.0,
        step=10.0
    )

    policy_deductable = st.number_input(
        "Policy Deductable ($)",
        min_value=0,
        value=1000
    )

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

    result_col, action_col = st.columns([1, 1], gap="large")

    with result_col:
        st.markdown(f"""
        <div class="story-card">
            <div class="section-label">03 · Model output</div>
            <div class="story-heading">Show the fraud risk</div>
            <div class="story-note">
                The model converts the claim information into a fraud probability score.
            </div>

            <p class="result-score {text_cls}">{pct:.0f}%</p>

            <div class="progress-wrap">
                <div class="progress-fill" style="width:{pct}%; background:{risk_color};"></div>
            </div>

            <div class="metric-row">
                <span class="metric-k">Decision threshold</span>
                <span class="metric-v">{int(THRESHOLD * 100)}%</span>
            </div>
            <div class="metric-row">
                <span class="metric-k">Prediction</span>
                <span class="metric-v">{safe_text(verdict)}</span>
            </div>

            <br>
            <span class="badge {badge_cls}">● {safe_text(risk_label)}</span>
        </div>
        """, unsafe_allow_html=True)

    with action_col:
        st.markdown(f"""
        <div class="story-card">
            <div class="section-label">04 · Recommended decision</div>
            <div class="story-heading">Show the action</div>
            <div class="story-note">
                The app does not replace human review. It supports triage and prioritization.
            </div>

            <h3 style="margin-top:1rem; font-size:1.45rem;">{safe_text(action_title)}</h3>
            <p style="color:#4b5563; line-height:1.7;">{safe_text(action_desc)}</p>

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
        """, unsafe_allow_html=True)

    # ── Claim composition chart ───────────────────────────────────────────────
    other = max(0, total_claim_amount - injury_claim - property_claim - vehicle_claim)
    max_claim = max(injury_claim, property_claim, vehicle_claim, other, 1)

    injury_w = injury_claim / max_claim * 100
    property_w = property_claim / max_claim * 100
    vehicle_w = vehicle_claim / max_claim * 100
    other_w = other / max_claim * 100

    st.markdown("<br>", unsafe_allow_html=True)

    chart_col, driver_col = st.columns([1.2, 0.8], gap="large")

    with chart_col:
        st.markdown(f"""
        <div class="story-card">
            <div class="section-label">05 · Claim composition</div>
            <div class="story-heading">Show the data clearly</div>
            <div class="story-note">
                The claim is broken into injury, property, vehicle, and remaining claim amount.
            </div>

            <div class="axis-box">
                <div class="bar-row">
                    <div><b>Injury</b></div>
                    {bar(injury_w, "#ef4444")}
                    <div>{money(injury_claim)}</div>
                </div>

                <div class="bar-row">
                    <div><b>Property</b></div>
                    {bar(property_w, "#f97316")}
                    <div>{money(property_claim)}</div>
                </div>

                <div class="bar-row">
                    <div><b>Vehicle</b></div>
                    {bar(vehicle_w, "#38bdf8")}
                    <div>{money(vehicle_claim)}</div>
                </div>

                <div class="bar-row">
                    <div><b>Other</b></div>
                    {bar(other_w, "#a855f7")}
                    <div>{money(other)}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with driver_col:
        risk_drivers = []

        if incident_severity in ["Major Damage", "Total Loss"]:
            risk_drivers.append((
                "High incident severity",
                "Major damage or total loss can increase claim risk."
            ))

        if total_claim_amount >= 60000:
            risk_drivers.append((
                "Large total claim",
                "The total claim amount is above $60,000."
            ))

        if number_of_vehicles_involved >= 2:
            risk_drivers.append((
                "Multiple vehicles involved",
                "Multi-vehicle claims can be more complex to validate."
            ))

        if bodily_injuries >= 1:
            risk_drivers.append((
                "Reported bodily injuries",
                "Injury-related claims may require additional verification."
            ))

        if witnesses >= 2:
            risk_drivers.append((
                "High witness count",
                "A high witness count can be a useful review signal."
            ))

        if months_as_customer < 24:
            risk_drivers.append((
                "Short customer tenure",
                "Newer policies may require closer claim review."
            ))

        driver_html = ""

        if not risk_drivers:
            driver_html = """
            <div class="driver">
                <div class="driver-title">No major risk indicators</div>
                <div class="driver-desc">The entered values did not trigger the main rule-based risk notes.</div>
            </div>
            """
        else:
            for title, desc in risk_drivers:
                driver_html += f"""
                <div class="driver">
                    <div class="driver-title">{safe_text(title)}</div>
                    <div class="driver-desc">{safe_text(desc)}</div>
                </div>
                """

        st.markdown(f"""
        <div class="story-card">
            <div class="section-label">06 · Risk drivers</div>
            <div class="story-heading">Show the why</div>
            <div class="story-note">
                These notes explain which entered values may have contributed to the review decision.
            </div>
            {driver_html}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <p class="footer-note">
        Portfolio demonstration · The model supports human review and should not be used as the only decision-maker.
    </p>
    """, unsafe_allow_html=True)