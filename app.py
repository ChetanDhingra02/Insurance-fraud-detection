import streamlit as st
import pandas as pd
import joblib

# ----------------------------
# Load model and template
# ----------------------------
model = joblib.load("deploy_fraud_model.pkl")
template_row = joblib.load("deploy_input_template.pkl")

THRESHOLD = 0.25

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="Insurance Fraud Detection",
    page_icon="🚗",
    layout="wide"
)

# ----------------------------
# Custom CSS
# ----------------------------
st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }

    .hero-card {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        padding: 1.5rem 1.5rem 1.2rem 1.5rem;
        border-radius: 18px;
        color: white;
        margin-bottom: 1.2rem;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    }

    .section-card {
        background: rgba(255,255,255,0.03);
        padding: 1rem 1rem 0.8rem 1rem;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 1rem;
    }

    .result-box {
        padding: 1rem;
        border-radius: 16px;
        margin-top: 0.8rem;
        margin-bottom: 0.8rem;
        border: 1px solid rgba(255,255,255,0.06);
        background: rgba(255,255,255,0.03);
    }

    .badge-low {
        display: inline-block;
        padding: 0.35rem 0.8rem;
        border-radius: 999px;
        background: rgba(34,197,94,0.15);
        color: #22c55e;
        font-weight: 600;
    }

    .badge-medium {
        display: inline-block;
        padding: 0.35rem 0.8rem;
        border-radius: 999px;
        background: rgba(250,204,21,0.15);
        color: #facc15;
        font-weight: 600;
    }

    .badge-high {
        display: inline-block;
        padding: 0.35rem 0.8rem;
        border-radius: 999px;
        background: rgba(239,68,68,0.15);
        color: #ef4444;
        font-weight: 600;
    }

    .small-note {
        font-size: 0.92rem;
        opacity: 0.85;
    }

    .driver-box {
        background: rgba(255,255,255,0.03);
        padding: 0.85rem 1rem;
        border-radius: 14px;
        border-left: 4px solid #3b82f6;
        margin-bottom: 0.6rem;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Helper functions
# ----------------------------
def bodily_injuries_label_to_value(label: str) -> int:
    mapping = {
        "None": 0,
        "One reported injury": 1,
        "Multiple / serious injuries": 2
    }
    return mapping[label]

def witnesses_label_to_value(label: str) -> int:
    mapping = {
        "No witnesses": 0,
        "One witness": 1,
        "Two witnesses": 2,
        "Three or more witnesses": 3
    }
    return mapping[label]

def risk_badge_html(risk_band: str) -> str:
    if risk_band == "Low Risk":
        return '<span class="badge-low">Low Risk</span>'
    elif risk_band == "Medium Risk":
        return '<span class="badge-medium">Medium Risk</span>'
    return '<span class="badge-high">High Risk</span>'

# ----------------------------
# Header
# ----------------------------
st.markdown("""
<div class="hero-card">
    <h1 style="margin-bottom:0.4rem;">🚗 Insurance Fraud Detection App</h1>
    <p style="margin-top:0; font-size:1.02rem;">
        Estimate fraud risk from claim and incident details using a deployment-friendly machine learning model.
    </p>
    <p class="small-note" style="margin-bottom:0;">
        Built as a portfolio demonstration using a simplified Random Forest pipeline with threshold tuning.
    </p>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# Input layout
# ----------------------------
left, right = st.columns([1, 1])

with left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Incident Details")

    incident_severity = st.selectbox(
        "Incident Severity",
        ["Minor Damage", "Major Damage", "Total Loss", "Trivial Damage"]
    )

    incident_type = st.selectbox(
        "Incident Type",
        ["Single Vehicle Collision", "Multi-vehicle Collision", "Vehicle Theft", "Parked Car"]
    )

    number_of_vehicles_involved = st.slider(
        "Number of Vehicles Involved",
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
        "Witnesses",
        options=["No witnesses", "One witness", "Two witnesses", "Three or more witnesses"],
        value="One witness"
    )
    witnesses = witnesses_label_to_value(witnesses_label)

    months_as_customer = st.number_input(
        "Months as Customer",
        min_value=0,
        value=200
    )
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Claim and Policy Details")

    total_claim_amount = st.number_input(
        "Total Claim Amount",
        min_value=0,
        value=50000
    )

    injury_claim = st.number_input(
        "Injury Claim",
        min_value=0,
        value=5000
    )

    property_claim = st.number_input(
        "Property Claim",
        min_value=0,
        value=10000
    )

    vehicle_claim = st.number_input(
        "Vehicle Claim",
        min_value=0,
        value=35000
    )

    policy_annual_premium = st.number_input(
        "Policy Annual Premium",
        min_value=0.0,
        value=1200.0,
        step=10.0
    )

    policy_deductable = st.number_input(
        "Policy Deductable",
        min_value=0,
        value=1000
    )
    st.markdown('</div>', unsafe_allow_html=True)

predict = st.button("Predict Fraud Risk", use_container_width=False)

# ----------------------------
# Prediction block
# ----------------------------
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

    if fraud_prob < 0.25:
        risk_band = "Low Risk"
    elif fraud_prob < 0.50:
        risk_band = "Medium Risk"
    else:
        risk_band = "High Risk"

    st.markdown("---")
    st.subheader("Prediction Result")

    result_col1, result_col2 = st.columns([1, 1])

    with result_col1:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.metric("Fraud Probability", f"{fraud_prob:.2%}")
        st.progress(float(fraud_prob))
        st.write(f"Decision Threshold: **{THRESHOLD}**")
        st.markdown(f"Risk Band: {risk_badge_html(risk_band)}", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with result_col2:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)

        if fraud_pred == 1:
            st.error("Potentially Fraudulent Claim")
        else:
            st.success("Likely Non-Fraudulent Claim")

        st.markdown("### Recommended Action")
        if fraud_prob >= 0.50:
            st.error("🚨 Send for manual investigation")
        elif fraud_prob >= THRESHOLD:
            st.warning("⚠️ Flag for review")
        else:
            st.success("✅ Process normally")

        st.markdown('</div>', unsafe_allow_html=True)

    # ----------------------------
    # Key risk drivers
    # ----------------------------
    st.markdown("### Key Risk Drivers")

    risk_drivers = []

    if incident_severity in ["Major Damage", "Total Loss"]:
        risk_drivers.append("High incident severity increases fraud risk.")

    if total_claim_amount >= 60000:
        risk_drivers.append("Large total claim amount increases suspicion.")

    if number_of_vehicles_involved >= 2:
        risk_drivers.append("Multiple vehicles involved may indicate a more complex claim.")

    if bodily_injuries >= 1:
        risk_drivers.append("Reported bodily injuries are associated with higher fraud risk.")

    if witnesses >= 2:
        risk_drivers.append("A higher number of witnesses may be associated with suspicious claims.")

    if months_as_customer < 24:
        risk_drivers.append("Shorter customer history may slightly increase risk.")

    if len(risk_drivers) == 0:
        st.markdown('<div class="driver-box">No major high-risk indicators were triggered from the selected inputs.</div>', unsafe_allow_html=True)
    else:
        for item in risk_drivers:
            st.markdown(f'<div class="driver-box">{item}</div>', unsafe_allow_html=True)

    # ----------------------------
    # Model summary
    # ----------------------------
    st.markdown("### About This Model")
    st.markdown("""
    <div class="result-box">
        <b>Model type:</b> Random Forest<br>
        <b>Deployment version:</b> Reduced-feature model for easier input collection<br>
        <b>Optimization goal:</b> Improve fraud recall through threshold tuning<br>
        <b>Purpose:</b> Portfolio demonstration for risk scoring and decision support
    </div>
    """, unsafe_allow_html=True)

    st.info("This app is a portfolio demonstration and should support review, not replace professional investigation.")