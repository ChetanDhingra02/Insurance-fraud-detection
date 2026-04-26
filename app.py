import streamlit as st
import pandas as pd
import joblib
import json

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
    page_title="Fraud Detection",
    page_icon="🛡",
    layout="wide"
)

# ----------------------------
# Custom CSS — Editorial minimal, chartosaur-inspired
# ----------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: #f9f8f6;
    }

    .main .block-container {
        padding: 2.5rem 2.5rem 4rem 2.5rem;
        max-width: 1200px;
    }

    /* ---- Top header ---- */
    .page-header {
        border-bottom: 2px solid #111;
        padding-bottom: 1.2rem;
        margin-bottom: 2.4rem;
    }

    .page-header h1 {
        font-family: 'DM Serif Display', serif;
        font-size: 2.6rem;
        font-weight: 400;
        color: #111;
        letter-spacing: -0.5px;
        margin: 0 0 0.3rem 0;
        line-height: 1.1;
    }

    .page-header p {
        font-size: 0.95rem;
        color: #666;
        margin: 0;
        font-weight: 300;
    }

    .tag-pill {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        background: #111;
        color: #f9f8f6;
        padding: 0.2rem 0.6rem;
        border-radius: 2px;
        margin-bottom: 0.6rem;
    }

    /* ---- Section labels ---- */
    .section-label {
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #999;
        margin-bottom: 1rem;
        border-bottom: 1px solid #e5e5e5;
        padding-bottom: 0.5rem;
    }

    /* ---- Input panels ---- */
    .input-panel {
        background: #fff;
        border: 1px solid #e8e8e8;
        border-radius: 4px;
        padding: 1.4rem 1.4rem 1rem 1.4rem;
        margin-bottom: 1rem;
    }

    /* ---- Result area ---- */
    .result-strip {
        background: #111;
        border-radius: 4px;
        padding: 1.8rem 2rem;
        margin: 1.6rem 0 1rem 0;
        display: flex;
        align-items: flex-start;
        gap: 3rem;
    }

    .result-main-number {
        font-family: 'DM Serif Display', serif;
        font-size: 4rem;
        color: #fff;
        line-height: 1;
        margin: 0;
    }

    .result-label {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #888;
        margin-bottom: 0.3rem;
    }

    .result-verdict {
        font-size: 1.1rem;
        font-weight: 500;
        color: #fff;
        margin-top: 0.4rem;
    }

    /* ---- Risk badge ---- */
    .risk-badge-low {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #166534;
        background: #dcfce7;
        padding: 0.3rem 0.8rem;
        border-radius: 2px;
        display: inline-block;
    }

    .risk-badge-medium {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #854d0e;
        background: #fef9c3;
        padding: 0.3rem 0.8rem;
        border-radius: 2px;
        display: inline-block;
    }

    .risk-badge-high {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #991b1b;
        background: #fee2e2;
        padding: 0.3rem 0.8rem;
        border-radius: 2px;
        display: inline-block;
    }

    /* ---- Action card ---- */
    .action-card {
        padding: 1rem 1.2rem;
        border-left: 3px solid #111;
        background: #fff;
        border-radius: 0 4px 4px 0;
        margin-top: 0.8rem;
    }

    .action-card.flag {
        border-left-color: #d97706;
    }

    .action-card.investigate {
        border-left-color: #dc2626;
    }

    .action-card.ok {
        border-left-color: #16a34a;
    }

    .action-card p {
        margin: 0;
        font-size: 0.9rem;
        color: #333;
    }

    .action-card strong {
        font-weight: 600;
        display: block;
        margin-bottom: 0.2rem;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #888;
    }

    /* ---- Driver bullets ---- */
    .driver-item {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 0.7rem 0;
        border-bottom: 1px solid #f0f0f0;
        font-size: 0.9rem;
        color: #333;
    }

    .driver-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #111;
        flex-shrink: 0;
        margin-top: 0.35rem;
    }

    /* ---- Chart container ---- */
    .chart-container {
        background: #fff;
        border: 1px solid #e8e8e8;
        border-radius: 4px;
        padding: 1.4rem;
        margin-top: 1rem;
    }

    /* ---- Predict button ---- */
    div.stButton > button {
        background: #111 !important;
        color: #f9f8f6 !important;
        border: none !important;
        border-radius: 3px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.05em !important;
        padding: 0.6rem 2rem !important;
        margin-top: 0.4rem !important;
        transition: background 0.15s ease !important;
    }

    div.stButton > button:hover {
        background: #333 !important;
    }

    /* ---- Streamlit widget overrides ---- */
    label {
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        color: #444 !important;
        letter-spacing: 0.01em !important;
    }

    .stSelectbox > div > div,
    .stNumberInput > div > div > input,
    .stSlider > div > div > div > div {
        border-radius: 3px !important;
    }

    h2, h3 {
        font-family: 'DM Serif Display', serif;
        font-weight: 400;
        color: #111;
    }

    .stInfo, .stWarning, .stError, .stSuccess {
        border-radius: 3px !important;
        font-size: 0.88rem !important;
    }

    hr {
        border: none;
        border-top: 1px solid #e5e5e5;
        margin: 1.8rem 0;
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
        return '<span class="risk-badge-low">Low Risk</span>'
    elif risk_band == "Medium Risk":
        return '<span class="risk-badge-medium">Medium Risk</span>'
    return '<span class="risk-badge-high">High Risk</span>'


def action_class(fraud_prob):
    if fraud_prob >= 0.50:
        return "investigate"
    elif fraud_prob >= THRESHOLD:
        return "flag"
    return "ok"


def action_text(fraud_prob):
    if fraud_prob >= 0.50:
        return ("Send for manual investigation",
                "Probability exceeds 50%. This claim requires full investigator review before any payout is processed.")
    elif fraud_prob >= THRESHOLD:
        return ("Flag for secondary review",
                "Probability is above the threshold. Route for a supervisor spot-check before proceeding.")
    return ("Process normally",
            "No major risk indicators. Claim may proceed through standard workflow.")


# ----------------------------
# Page header
# ----------------------------
st.markdown("""
<div class="page-header">
    <div class="tag-pill">Portfolio · ML Risk Scoring</div>
    <h1>Insurance Fraud Detection</h1>
    <p>Random Forest classifier · Threshold-tuned for recall · Demonstration model</p>
</div>
""", unsafe_allow_html=True)


# ----------------------------
# Input layout
# ----------------------------
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown('<div class="input-panel">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Incident Details</p>', unsafe_allow_html=True)

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
        min_value=1, max_value=4, value=1
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
        min_value=0, value=200
    )
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="input-panel">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Claim & Policy Details</p>', unsafe_allow_html=True)

    total_claim_amount = st.number_input(
        "Total Claim Amount ($)",
        min_value=0, value=50000
    )

    injury_claim = st.number_input(
        "Injury Claim ($)",
        min_value=0, value=5000
    )

    property_claim = st.number_input(
        "Property Claim ($)",
        min_value=0, value=10000
    )

    vehicle_claim = st.number_input(
        "Vehicle Claim ($)",
        min_value=0, value=35000
    )

    policy_annual_premium = st.number_input(
        "Policy Annual Premium ($)",
        min_value=0.0, value=1200.0, step=10.0
    )

    policy_deductable = st.number_input(
        "Policy Deductable ($)",
        min_value=0, value=1000
    )
    st.markdown('</div>', unsafe_allow_html=True)


predict = st.button("Run Fraud Assessment →")


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

    # ---- Result strip ----
    verdict_text = "Likely Fraudulent" if fraud_pred == 1 else "Likely Legitimate"
    action_cls = action_class(fraud_prob)
    action_title, action_desc = action_text(fraud_prob)

    st.markdown("---")

    res_col, act_col = st.columns([1, 1], gap="large")

    with res_col:
        st.markdown('<p class="section-label">Model Output</p>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="result-strip">
            <div>
                <p class="result-label">Fraud probability</p>
                <p class="result-main-number">{fraud_prob:.0%}</p>
                <p style="font-size:0.72rem; color:#666; margin:0.3rem 0 0 0;">Threshold: {THRESHOLD:.0%}</p>
            </div>
            <div style="padding-top:0.2rem;">
                <p class="result-label">Classification</p>
                <p class="result-verdict">{verdict_text}</p>
                <div style="margin-top:0.6rem;">{risk_badge_html(risk_band)}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with act_col:
        st.markdown('<p class="section-label">Recommended Action</p>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="margin-top: 0.6rem;">
            <div class="action-card {action_cls}">
                <strong>Action</strong>
                <p style="font-size:1rem; font-weight:600; color:#111; margin-bottom:0.4rem;">{action_title}</p>
                <p>{action_desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ---- Claim breakdown chart + risk drivers ----
    st.markdown("---")
    chart_col, drivers_col = st.columns([1.1, 0.9], gap="large")

    with chart_col:
        st.markdown('<p class="section-label">Claim Breakdown</p>', unsafe_allow_html=True)

        # Chart.js embedded via HTML component
        non_claim = max(0, total_claim_amount - injury_claim - property_claim - vehicle_claim)
        chart_data = {
            "injury": injury_claim,
            "property": property_claim,
            "vehicle": vehicle_claim,
            "other": non_claim,
            "fraud_prob": round(fraud_prob * 100, 1),
            "threshold": round(THRESHOLD * 100, 1),
        }

        chart_html = f"""
        <div style="font-family:'DM Sans',sans-serif; padding:0.2rem 0 1rem 0;">

            <!-- Claim composition bar chart -->
            <p style="font-size:0.72rem; font-weight:600; letter-spacing:0.1em; text-transform:uppercase; color:#999; margin:0 0 1rem 0;">Claim composition</p>
            <div style="position:relative; width:100%; height:220px;">
                <canvas id="claimChart" role="img" aria-label="Bar chart showing claim composition split by injury, property, vehicle, and other amounts.">
                    Injury: ${chart_data['injury']:,}, Property: ${chart_data['property']:,}, Vehicle: ${chart_data['vehicle']:,}, Other: ${chart_data['other']:,}
                </canvas>
            </div>

            <!-- Probability gauge -->
            <p style="font-size:0.72rem; font-weight:600; letter-spacing:0.1em; text-transform:uppercase; color:#999; margin:1.6rem 0 0.8rem 0;">Fraud probability vs threshold</p>
            <div style="position:relative; width:100%; height:80px;">
                <canvas id="probChart" role="img" aria-label="Horizontal bar showing fraud probability {chart_data['fraud_prob']}% against threshold of {chart_data['threshold']}%.">
                    Fraud probability: {chart_data['fraud_prob']}%, Threshold: {chart_data['threshold']}%
                </canvas>
            </div>
        </div>

        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
        <script>
        (function() {{
            const claimCtx = document.getElementById('claimChart');
            new Chart(claimCtx, {{
                type: 'bar',
                data: {{
                    labels: ['Injury', 'Property', 'Vehicle', 'Other'],
                    datasets: [{{
                        label: 'Amount ($)',
                        data: [{chart_data['injury']}, {chart_data['property']}, {chart_data['vehicle']}, {chart_data['other']}],
                        backgroundColor: ['#e97b5b', '#5b8fe9', '#5bc4a1', '#c4b5a1'],
                        borderWidth: 0,
                        borderRadius: 2,
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{
                            callbacks: {{
                                label: (ctx) => ' $' + ctx.raw.toLocaleString()
                            }}
                        }}
                    }},
                    scales: {{
                        x: {{
                            grid: {{ display: false }},
                            ticks: {{ font: {{ family: 'DM Sans', size: 11 }}, color: '#666' }}
                        }},
                        y: {{
                            grid: {{ color: '#f0f0f0' }},
                            ticks: {{
                                font: {{ family: 'DM Sans', size: 11 }},
                                color: '#666',
                                callback: (v) => '$' + v.toLocaleString()
                            }},
                            border: {{ display: false }}
                        }}
                    }}
                }}
            }});

            const probCtx = document.getElementById('probChart');
            new Chart(probCtx, {{
                type: 'bar',
                data: {{
                    labels: ['Probability', 'Threshold'],
                    datasets: [{{
                        label: '%',
                        data: [{chart_data['fraud_prob']}, {chart_data['threshold']}],
                        backgroundColor: ['{
                            "#dc2626" if fraud_prob >= 0.5 else "#d97706" if fraud_prob >= THRESHOLD else "#16a34a"
                        }', '#d1d5db'],
                        borderWidth: 0,
                        borderRadius: 2,
                    }}]
                }},
                options: {{
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{
                            callbacks: {{
                                label: (ctx) => ' ' + ctx.raw + '%'
                            }}
                        }}
                    }},
                    scales: {{
                        x: {{
                            max: 100,
                            grid: {{ color: '#f0f0f0' }},
                            ticks: {{ font: {{ family: 'DM Sans', size: 11 }}, color: '#666', callback: (v) => v + '%' }},
                            border: {{ display: false }}
                        }},
                        y: {{
                            grid: {{ display: false }},
                            ticks: {{ font: {{ family: 'DM Sans', size: 11 }}, color: '#555' }}
                        }}
                    }}
                }}
            }});
        }})();
        </script>
        """

        st.components.v1.html(chart_html, height=430)

    with drivers_col:
        st.markdown('<p class="section-label">Key Risk Drivers</p>', unsafe_allow_html=True)

        risk_drivers = []

        if incident_severity in ["Major Damage", "Total Loss"]:
            risk_drivers.append("High incident severity is associated with elevated fraud risk.")

        if total_claim_amount >= 60000:
            risk_drivers.append("Large total claim amount exceeds the high-risk threshold.")

        if number_of_vehicles_involved >= 2:
            risk_drivers.append("Multiple vehicles involved indicates a more complex claim pattern.")

        if bodily_injuries >= 1:
            risk_drivers.append("Reported bodily injuries are correlated with higher fraud incidence.")

        if witnesses >= 2:
            risk_drivers.append("High witness count may be associated with staged incidents.")

        if months_as_customer < 24:
            risk_drivers.append("Short customer tenure is a mild risk signal.")

        st.markdown('<div style="margin-top:0.4rem;">', unsafe_allow_html=True)

        if len(risk_drivers) == 0:
            st.markdown("""
            <div class="driver-item" style="border-bottom:none; color:#666;">
                <div class="driver-dot" style="background:#16a34a;"></div>
                <span>No major risk indicators detected from the provided inputs.</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            for item in risk_drivers:
                st.markdown(f"""
                <div class="driver-item">
                    <div class="driver-dot"></div>
                    <span>{item}</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Model info block
        st.markdown("""
        <div style="margin-top:2rem; padding:1rem 1.2rem; background:#fff; border:1px solid #e8e8e8; border-radius:4px;">
            <p style="font-size:0.68rem; font-weight:600; letter-spacing:0.1em; text-transform:uppercase; color:#999; margin:0 0 0.7rem 0;">About this model</p>
            <table style="font-size:0.82rem; color:#444; width:100%; border-collapse:collapse;">
                <tr><td style="color:#999; padding:0.25rem 0; width:45%;">Type</td><td>Random Forest</td></tr>
                <tr><td style="color:#999; padding:0.25rem 0;">Tuning</td><td>Threshold optimised for recall</td></tr>
                <tr><td style="color:#999; padding:0.25rem 0;">Features</td><td>Reduced set — 12 inputs</td></tr>
                <tr><td style="color:#999; padding:0.25rem 0;">Purpose</td><td>Portfolio demonstration</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <p style="font-size:0.78rem; color:#aaa; margin-top:2rem; text-align:center;">
        This tool is a portfolio demonstration and is intended to support human review, not replace professional investigation.
    </p>
    """, unsafe_allow_html=True)