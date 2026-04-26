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
    page_title="Fraud Detection",
    page_icon="🛡",
    layout="wide"
)

# ----------------------------
# CSS — Glassmorphism + hand-drawn sketch hybrid
# ----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;500;600;700&family=Syne:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 35%, #24243e 65%, #0d1b2a 100%);
    min-height: 100vh;
}

.stApp::before {
    content: '';
    position: fixed;
    top: -30%; left: -20%;
    width: 70%; height: 70%;
    background: radial-gradient(ellipse, rgba(120,80,255,0.18) 0%, transparent 70%);
    border-radius: 50%;
    animation: blob1 12s ease-in-out infinite alternate;
    pointer-events: none; z-index: 0;
}

.stApp::after {
    content: '';
    position: fixed;
    bottom: -20%; right: -15%;
    width: 60%; height: 60%;
    background: radial-gradient(ellipse, rgba(0,200,180,0.12) 0%, transparent 70%);
    border-radius: 50%;
    animation: blob2 15s ease-in-out infinite alternate;
    pointer-events: none; z-index: 0;
}

@keyframes blob1 {
    0%   { transform: translate(0,0) scale(1); }
    100% { transform: translate(8%,12%) scale(1.1); }
}

@keyframes blob2 {
    0%   { transform: translate(0,0) scale(1); }
    100% { transform: translate(-10%,-8%) scale(1.15); }
}

.main .block-container {
    padding: 2.5rem 2.8rem 5rem 2.8rem;
    max-width: 1220px;
    position: relative; z-index: 1;
}

.page-eyebrow {
    font-family: 'Caveat', cursive;
    font-size: 1.1rem;
    color: rgba(160,220,255,0.7);
    margin: 0 0 0.3rem 0;
}

.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    color: #fff;
    margin: 0 0 0.5rem 0;
    letter-spacing: -1px;
    line-height: 1.05;
    text-shadow: 0 2px 30px rgba(120,80,255,0.35);
}

.page-subtitle {
    font-family: 'Caveat', cursive;
    font-size: 1.05rem;
    color: rgba(200,210,255,0.55);
    margin: 0;
}

.title-underline {
    width: 120px; height: 4px;
    margin: 0.7rem 0 2rem 0;
    background: none;
    border-bottom: 3px solid rgba(130,100,255,0.7);
    border-radius: 0 0 50% 50% / 0 0 8px 8px;
    position: relative;
}

.title-underline::after {
    content: '';
    position: absolute;
    bottom: -6px; left: 10px;
    width: 80px;
    border-bottom: 2px solid rgba(0,220,200,0.4);
    border-radius: 0 0 50% 50% / 0 0 6px 6px;
}

.glass-card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1.5px solid rgba(255,255,255,0.10);
    border-radius: 20px;
    padding: 1.6rem 1.8rem 1.4rem;
    margin-bottom: 1rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.08);
    position: relative; overflow: hidden;
}

.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
}

.sketch-label {
    font-family: 'Caveat', cursive;
    font-size: 1.05rem;
    font-weight: 600;
    color: rgba(160,220,255,0.75);
    letter-spacing: 0.04em;
    margin: 0 0 1.1rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.sketch-label::after {
    content: '';
    flex: 1; height: 1.5px;
    background: linear-gradient(90deg, rgba(160,220,255,0.3), transparent);
    border-radius: 1px;
}

label, .stSlider label, .stSelectbox label,
.stNumberInput label, .stSelectSlider label {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    color: rgba(200,210,255,0.65) !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}

div.stButton > button {
    background: linear-gradient(135deg, rgba(110,80,230,0.8), rgba(0,180,160,0.7)) !important;
    color: #fff !important;
    border: 1.5px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    padding: 0.7rem 2.5rem !important;
    box-shadow: 0 4px 20px rgba(110,80,230,0.3) !important;
    transition: all 0.2s ease !important;
    margin-top: 0.5rem !important;
}

div.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 28px rgba(110,80,230,0.45) !important;
}

.result-glass {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1.5px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 2rem 2.2rem;
    box-shadow: 0 8px 40px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.1);
    position: relative; overflow: hidden;
    margin-bottom: 1rem;
}

.result-glass::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 180px; height: 180px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(130,100,255,0.15), transparent 70%);
}

.result-big-number {
    font-family: 'Syne', sans-serif;
    font-size: 4.5rem;
    font-weight: 800;
    color: #fff;
    line-height: 1;
    margin: 0;
    text-shadow: 0 0 40px rgba(130,100,255,0.5);
    letter-spacing: -2px;
}

.result-sketch-label {
    font-family: 'Caveat', cursive;
    font-size: 1rem;
    color: rgba(180,200,255,0.6);
    margin: 0 0 0.3rem 0;
}

.result-verdict {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #fff;
    margin: 0.5rem 0 0 0;
}

.badge-low {
    display: inline-block;
    font-family: 'Caveat', cursive; font-size: 1rem; font-weight: 700;
    color: #6ee7b7;
    background: rgba(110,231,183,0.1);
    border: 1.5px solid rgba(110,231,183,0.35);
    border-radius: 999px; padding: 0.2rem 1rem;
}

.badge-medium {
    display: inline-block;
    font-family: 'Caveat', cursive; font-size: 1rem; font-weight: 700;
    color: #fcd34d;
    background: rgba(252,211,77,0.1);
    border: 1.5px solid rgba(252,211,77,0.35);
    border-radius: 999px; padding: 0.2rem 1rem;
}

.badge-high {
    display: inline-block;
    font-family: 'Caveat', cursive; font-size: 1rem; font-weight: 700;
    color: #fca5a5;
    background: rgba(252,165,165,0.1);
    border: 1.5px solid rgba(252,165,165,0.35);
    border-radius: 999px; padding: 0.2rem 1rem;
}

.action-glass {
    backdrop-filter: blur(16px);
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.2);
    height: 100%; box-sizing: border-box;
}

.action-title {
    font-family: 'Caveat', cursive;
    font-size: 0.9rem; font-weight: 600;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: rgba(160,200,255,0.6);
    margin: 0 0 0.5rem 0;
}

.action-text {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem; font-weight: 700;
    margin: 0 0 0.5rem 0;
}

.action-desc {
    font-family: 'Syne', sans-serif;
    font-size: 0.83rem;
    color: rgba(200,210,255,0.6);
    margin: 0; line-height: 1.6;
}

.driver-row {
    display: flex; align-items: flex-start; gap: 0.8rem;
    padding: 0.65rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-family: 'Syne', sans-serif;
    font-size: 0.83rem;
    color: rgba(200,215,255,0.75);
    line-height: 1.5;
}

.driver-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: rgba(130,100,255,0.8);
    flex-shrink: 0; margin-top: 0.38rem;
    box-shadow: 0 0 6px rgba(130,100,255,0.6);
}

.model-info {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-top: 1.4rem;
}

.model-row {
    display: flex; justify-content: space-between;
    padding: 0.3rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}

.model-key {
    font-family: 'Caveat', cursive; font-size: 0.95rem;
    color: rgba(160,200,255,0.5);
}

.model-val {
    font-family: 'Syne', sans-serif; font-weight: 500;
    color: rgba(220,230,255,0.75); font-size: 0.78rem;
}

hr {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.07);
    margin: 2rem 0;
}

[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.06) !important;
    border-color: rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #fff !important;
}

[data-baseweb="select"] svg { color: rgba(200,210,255,0.5) !important; }
[data-baseweb="option"] { background: #1a1a3e !important; color: #fff !important; }
[data-baseweb="option"]:hover { background: rgba(130,100,255,0.3) !important; }

[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.06) !important;
    border: 1.5px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #fff !important;
}

[data-testid="stNumberInput"] button {
    background: rgba(255,255,255,0.06) !important;
    border-color: rgba(255,255,255,0.12) !important;
    color: rgba(200,210,255,0.6) !important;
}

.footer-note {
    font-family: 'Caveat', cursive; font-size: 0.95rem;
    color: rgba(160,180,255,0.35);
    text-align: center; margin-top: 2.5rem;
}
</style>
""", unsafe_allow_html=True)


# ----------------------------
# Helpers  (LOGIC UNCHANGED)
# ----------------------------
def bodily_injuries_label_to_value(label: str) -> int:
    return {"None": 0, "One reported injury": 1, "Multiple / serious injuries": 2}[label]


def witnesses_label_to_value(label: str) -> int:
    return {"No witnesses": 0, "One witness": 1, "Two witnesses": 2, "Three or more witnesses": 3}[label]


def risk_badge_html(risk_band: str) -> str:
    if risk_band == "Low Risk":
        return '<span class="badge-low">✓  Low Risk</span>'
    elif risk_band == "Medium Risk":
        return '<span class="badge-medium">~  Medium Risk</span>'
    return '<span class="badge-high">!  High Risk</span>'


def action_info(fraud_prob):
    if fraud_prob >= 0.50:
        return ("rgba(252,165,165,0.12)", "rgba(252,165,165,0.4)", "#fca5a5",
                "Send for Manual Investigation",
                "Probability exceeds 50%. Full investigator review required before any payout is processed.")
    elif fraud_prob >= THRESHOLD:
        return ("rgba(252,211,77,0.12)", "rgba(252,211,77,0.4)", "#fcd34d",
                "Flag for Secondary Review",
                "Above threshold. Route for a supervisor spot-check before proceeding.")
    return ("rgba(110,231,183,0.12)", "rgba(110,231,183,0.4)", "#6ee7b7",
            "Process Normally",
            "No major risk indicators detected. Claim may proceed through the standard workflow.")


# ----------------------------
# Header
# ----------------------------
st.markdown("""
<p class="page-eyebrow">✦ ML Risk Scoring · Portfolio Demo</p>
<h1 class="page-title">Insurance Fraud<br>Detection</h1>
<div class="title-underline"></div>
<p class="page-subtitle">Random Forest · threshold-tuned for recall · 12-feature deployment model</p>
<br>
""", unsafe_allow_html=True)


# ----------------------------
# Input panels
# ----------------------------
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown('<div class="glass-card"><p class="sketch-label">Incident Details</p>', unsafe_allow_html=True)

    incident_severity = st.selectbox(
        "Incident Severity",
        ["Minor Damage", "Major Damage", "Total Loss", "Trivial Damage"]
    )
    incident_type = st.selectbox(
        "Incident Type",
        ["Single Vehicle Collision", "Multi-vehicle Collision", "Vehicle Theft", "Parked Car"]
    )
    number_of_vehicles_involved = st.slider("Vehicles Involved", 1, 4, 1)
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
    months_as_customer = st.number_input("Months as Customer", min_value=0, value=200)

    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="glass-card"><p class="sketch-label">Claim & Policy Details</p>', unsafe_allow_html=True)

    total_claim_amount  = st.number_input("Total Claim Amount ($)",  min_value=0,   value=50000)
    injury_claim        = st.number_input("Injury Claim ($)",        min_value=0,   value=5000)
    property_claim      = st.number_input("Property Claim ($)",      min_value=0,   value=10000)
    vehicle_claim       = st.number_input("Vehicle Claim ($)",       min_value=0,   value=35000)
    policy_annual_premium = st.number_input("Annual Premium ($)",    min_value=0.0, value=1200.0, step=10.0)
    policy_deductable   = st.number_input("Policy Deductable ($)",   min_value=0,   value=1000)

    st.markdown('</div>', unsafe_allow_html=True)


predict = st.button("⟢  Run Fraud Assessment")


# ----------------------------
# Prediction  (LOGIC UNCHANGED)
# ----------------------------
if predict:
    input_data = template_row.copy()
    input_data.loc[:, "incident_severity"]           = incident_severity
    input_data.loc[:, "incident_type"]               = incident_type
    input_data.loc[:, "number_of_vehicles_involved"] = number_of_vehicles_involved
    input_data.loc[:, "bodily_injuries"]             = bodily_injuries
    input_data.loc[:, "witnesses"]                   = witnesses
    input_data.loc[:, "months_as_customer"]          = months_as_customer
    input_data.loc[:, "total_claim_amount"]          = total_claim_amount
    input_data.loc[:, "injury_claim"]                = injury_claim
    input_data.loc[:, "property_claim"]              = property_claim
    input_data.loc[:, "vehicle_claim"]               = vehicle_claim
    input_data.loc[:, "policy_annual_premium"]       = policy_annual_premium
    input_data.loc[:, "policy_deductable"]           = policy_deductable

    fraud_prob = model.predict_proba(input_data)[0, 1]
    fraud_pred = int(fraud_prob >= THRESHOLD)

    if fraud_prob < 0.25:
        risk_band = "Low Risk"
    elif fraud_prob < 0.50:
        risk_band = "Medium Risk"
    else:
        risk_band = "High Risk"

    bg_c, border_c, text_c, action_title, action_desc = action_info(fraud_prob)
    verdict_text = "Likely Fraudulent" if fraud_pred == 1 else "Likely Legitimate"

    gauge_color = (
        "#6ee7b7" if fraud_prob < THRESHOLD else
        "#fcd34d" if fraud_prob < 0.50 else
        "#fca5a5"
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Result + Action row ──
    res_col, act_col = st.columns([1, 1], gap="large")

    with res_col:
        st.markdown(f"""
        <div class="result-glass">
            <p class="result-sketch-label">fraud probability</p>
            <p class="result-big-number">{fraud_prob:.0%}</p>
            <p style="font-family:'Caveat',cursive; font-size:0.88rem;
                      color:rgba(180,200,255,0.4); margin:0.2rem 0 0.9rem;">
                decision threshold · {THRESHOLD:.0%}
            </p>
            {risk_badge_html(risk_band)}
            <p class="result-verdict">{verdict_text}</p>
        </div>
        """, unsafe_allow_html=True)

    with act_col:
        st.markdown(f"""
        <div class="action-glass" style="background:{bg_c}; border:1.5px solid {border_c};">
            <p class="action-title">Recommended Action</p>
            <p class="action-text" style="color:{text_c};">{action_title}</p>
            <p class="action-desc">{action_desc}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Chart + Drivers row ──
    chart_col, drivers_col = st.columns([1.15, 0.85], gap="large")

    with chart_col:
        other = max(0, total_claim_amount - injury_claim - property_claim - vehicle_claim)

        chart_html = f"""
<style>
  .clabel {{
    font-family:'Caveat',cursive;
    font-size:1rem;
    color:rgba(160,220,255,0.7);
    margin:0 0 0.7rem 0;
  }}
</style>
<div>
  <p class="clabel">✦ claim breakdown</p>
  <div style="position:relative;width:100%;height:190px;">
    <canvas id="claimChart" role="img"
      aria-label="Claim breakdown: Injury ${injury_claim:,}, Property ${property_claim:,}, Vehicle ${vehicle_claim:,}, Other ${other:,}">
      Injury ${injury_claim:,} · Property ${property_claim:,} · Vehicle ${vehicle_claim:,} · Other ${other:,}
    </canvas>
  </div>
  <p class="clabel" style="margin-top:1.5rem;">✦ probability vs threshold</p>
  <div style="position:relative;width:100%;height:65px;">
    <canvas id="probChart" role="img"
      aria-label="Fraud probability {fraud_prob:.0%} vs threshold {THRESHOLD:.0%}">
      Fraud {fraud_prob:.0%} · Threshold {THRESHOLD:.0%}
    </canvas>
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<script>
(function(){{
  const T = {{ color:'rgba(200,215,255,0.5)', font:{{ family:'Syne,sans-serif', size:11 }} }};
  const G = {{ color:'rgba(255,255,255,0.06)' }};

  new Chart(document.getElementById('claimChart'), {{
    type:'bar',
    data:{{
      labels:['Injury','Property','Vehicle','Other'],
      datasets:[{{
        data:[{injury_claim},{property_claim},{vehicle_claim},{other}],
        backgroundColor:['rgba(130,100,255,0.6)','rgba(0,200,180,0.55)','rgba(255,140,90,0.55)','rgba(200,200,255,0.2)'],
        borderColor:['rgba(160,130,255,0.9)','rgba(0,230,210,0.9)','rgba(255,170,120,0.9)','rgba(220,220,255,0.35)'],
        borderWidth:1.5, borderRadius:6
      }}]
    }},
    options:{{
      responsive:true, maintainAspectRatio:false,
      plugins:{{ legend:{{ display:false }}, tooltip:{{ callbacks:{{ label:(c)=>' $'+c.raw.toLocaleString() }} }} }},
      scales:{{
        x:{{ grid:{{ display:false }}, ticks:T, border:{{ display:false }} }},
        y:{{ grid:G, ticks:{{ ...T, callback:(v)=>'$'+v.toLocaleString() }}, border:{{ display:false }} }}
      }}
    }}
  }});

  new Chart(document.getElementById('probChart'), {{
    type:'bar',
    data:{{
      labels:['Model score','Threshold'],
      datasets:[{{
        data:[{round(fraud_prob*100,1)},{round(THRESHOLD*100,1)}],
        backgroundColor:['{gauge_color}44','rgba(255,255,255,0.1)'],
        borderColor:['{gauge_color}','rgba(255,255,255,0.25)'],
        borderWidth:1.5, borderRadius:6
      }}]
    }},
    options:{{
      indexAxis:'y', responsive:true, maintainAspectRatio:false,
      plugins:{{ legend:{{ display:false }}, tooltip:{{ callbacks:{{ label:(c)=>' '+c.raw+'%' }} }} }},
      scales:{{
        x:{{ max:100, grid:G, ticks:{{ ...T, callback:(v)=>v+'%' }}, border:{{ display:false }} }},
        y:{{ grid:{{ display:false }}, ticks:T, border:{{ display:false }} }}
      }}
    }}
  }});
}})();
</script>
"""
        st.markdown('<div class="glass-card" style="padding:1.4rem 1.6rem 1.8rem;">', unsafe_allow_html=True)
        st.components.v1.html(chart_html, height=370)
        st.markdown('</div>', unsafe_allow_html=True)

    with drivers_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p class="sketch-label">Key Risk Drivers</p>', unsafe_allow_html=True)

        risk_drivers = []
        if incident_severity in ["Major Damage", "Total Loss"]:
            risk_drivers.append("High incident severity is correlated with elevated fraud risk.")
        if total_claim_amount >= 60000:
            risk_drivers.append("Total claim amount exceeds the high-risk threshold.")
        if number_of_vehicles_involved >= 2:
            risk_drivers.append("Multiple vehicles indicate a more complex claim pattern.")
        if bodily_injuries >= 1:
            risk_drivers.append("Reported bodily injuries are correlated with higher fraud incidence.")
        if witnesses >= 2:
            risk_drivers.append("High witness count may indicate a staged incident.")
        if months_as_customer < 24:
            risk_drivers.append("Short customer tenure is a mild elevated-risk signal.")

        if not risk_drivers:
            st.markdown("""
            <div class="driver-row" style="border-bottom:none;">
                <div class="driver-dot" style="background:rgba(110,231,183,0.8); box-shadow:0 0 6px rgba(110,231,183,0.5);"></div>
                <span style="color:rgba(110,231,183,0.7);">No major risk indicators detected.</span>
            </div>""", unsafe_allow_html=True)
        else:
            for d in risk_drivers:
                st.markdown(f"""
                <div class="driver-row">
                    <div class="driver-dot"></div>
                    <span>{d}</span>
                </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="model-info">
            <div class="model-row"><span class="model-key">Type</span><span class="model-val">Random Forest</span></div>
            <div class="model-row"><span class="model-key">Tuning</span><span class="model-val">Threshold → recall</span></div>
            <div class="model-row"><span class="model-key">Features</span><span class="model-val">12 inputs (reduced)</span></div>
            <div class="model-row" style="border-bottom:none;"><span class="model-key">Purpose</span><span class="model-val">Portfolio demo</span></div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <p class="footer-note">
        ✦ Portfolio demonstration — supports human review, does not replace professional investigation ✦
    </p>""", unsafe_allow_html=True)