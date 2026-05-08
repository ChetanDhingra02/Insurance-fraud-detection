import streamlit as st

from config import PAGE_ICON, PAGE_TITLE
from model_utils import load_artifacts, make_input_dataframe, predict_fraud_probability
from theme import render_theme
from ui import (
    bi_val,
    render_financial_card,
    render_footer,
    render_header,
    render_hero,
    render_incident_card,
    render_results,
    wi_val,
)


st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
)

render_theme()
render_header()
render_hero()

left, right = st.columns(2, gap="large")

with left:
    render_incident_card()
    incident_severity = st.selectbox(
        "Incident Severity",
        ["Minor Damage", "Major Damage", "Total Loss", "Trivial Damage"],
    )
    incident_type = st.selectbox(
        "Incident Type",
        ["Single Vehicle Collision", "Multi-vehicle Collision", "Vehicle Theft", "Parked Car"],
    )
    number_of_vehicles_involved = st.slider("Vehicles Involved", 1, 4, 1)
    bi_label = st.select_slider(
        "Reported Injuries",
        options=["None", "One reported injury", "Multiple / serious injuries"],
    )
    bodily_injuries = bi_val(bi_label)
    wi_label = st.select_slider(
        "Witnesses Present",
        options=["No witnesses", "One witness", "Two witnesses", "Three or more witnesses"],
    )
    witnesses = wi_val(wi_label)
    months_as_customer = st.number_input("Months as Customer", min_value=0, value=200)

with right:
    render_financial_card()
    total_claim_amount = st.number_input("Total Claim ($)", min_value=0, value=50000)
    injury_claim = st.number_input("Injury Claim ($)", min_value=0, value=5000)
    property_claim = st.number_input("Property Claim ($)", min_value=0, value=10000)
    vehicle_claim = st.number_input("Vehicle Claim ($)", min_value=0, value=35000)
    policy_annual_premium = st.number_input("Annual Premium ($)", min_value=0.0, value=1200.0, step=10.0)
    policy_deductable = st.number_input("Deductible ($)", min_value=0, value=1000)

predict = st.button("⚡ Run Fraud Risk Assessment →")

if predict:
    input_values = {
        "incident_severity": incident_severity,
        "incident_type": incident_type,
        "number_of_vehicles_involved": number_of_vehicles_involved,
        "bodily_injuries": bodily_injuries,
        "witnesses": witnesses,
        "months_as_customer": months_as_customer,
        "total_claim_amount": total_claim_amount,
        "injury_claim": injury_claim,
        "property_claim": property_claim,
        "vehicle_claim": vehicle_claim,
        "policy_annual_premium": policy_annual_premium,
        "policy_deductable": policy_deductable,
    }

    try:
        model, template = load_artifacts()
        input_df = make_input_dataframe(template, model, input_values)
        fraud_prob = predict_fraud_probability(model, input_df)
        fraud_prob = min(max(float(fraud_prob), 0.0), 1.0)
    except Exception as e:
        st.error(f"Model could not run: {e}")
        st.stop()

    render_results(fraud_prob, input_values)

render_footer()
