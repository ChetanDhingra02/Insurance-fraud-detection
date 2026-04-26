import streamlit as st
import pandas as pd
import joblib

# ── Load model ──────────────────────────────────────────────────────────────
model        = joblib.load("deploy_fraud_model.pkl")
template_row = joblib.load("deploy_input_template.pkl")
THRESHOLD    = 0.25

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Insurance Fraud Detection",
    page_icon="◎",
    layout="wide",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400;500&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #111;
}

.stApp {
    background: #faf9f6;
}

.main .block-container {
    padding: 3rem 3.5rem 6rem;
    max-width: 1180px;
}

/* ── Animations ── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(22px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes slideIn {
    from { opacity: 0; transform: translateX(-18px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes drawLine {
    from { width: 0; }
    to   { width: 100%; }
}
@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50%       { transform: scale(1.04); }
}
@keyframes tickerIn {
    from { opacity: 0; transform: scale(0.82); }
    to   { opacity: 1; transform: scale(1); }
}

/* ── Header ── */
.hdr-tag {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #999;
    margin: 0 0 0.6rem;
    animation: fadeUp 0.5s ease both;
}

.hdr-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(2.6rem, 5vw, 4rem);
    font-weight: 900;
    color: #111;
    line-height: 1.0;
    margin: 0 0 0.5rem;
    letter-spacing: -1.5px;
    animation: fadeUp 0.55s 0.08s ease both;
}

.hdr-rule {
    height: 3px;
    background: #111;
    margin: 0.9rem 0 0.7rem;
    animation: drawLine 0.7s 0.2s ease both;
    transform-origin: left;
}

.hdr-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    font-weight: 300;
    color: #777;
    letter-spacing: 0.02em;
    margin: 0 0 2.5rem;
    animation: fadeUp 0.55s 0.18s ease both;
}

/* ── Section titles ── */
.sec-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #aaa;
    margin: 0 0 1.1rem;
    padding-bottom: 0.55rem;
    border-bottom: 1.5px solid #e8e8e4;
}

/* ── Input cards ── */
.input-card {
    background: #fff;
    border: 1.5px solid #e5e5e0;
    border-radius: 3px;
    padding: 1.6rem 1.8rem 1.2rem;
    margin-bottom: 1rem;
    animation: fadeUp 0.5s 0.25s ease both;
    transition: border-color 0.2s;
}
.input-card:hover { border-color: #bbb; }

/* ── Widget label overrides ── */
label,
.stSlider label,
.stSelectbox label,
.stNumberInput label,
.stSelectSlider label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    color: #555 !important;
    letter-spacing: 0.03em !important;
    text-transform: none !important;
    margin-bottom: 0.15rem !important;
}

/* Input elements */
[data-baseweb="select"] > div,
[data-testid="stNumberInput"] input {
    border-radius: 3px !important;
    border-color: #ddd !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    background: #faf9f6 !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-baseweb="select"] > div:focus-within,
[data-testid="stNumberInput"] input:focus {
    border-color: #111 !important;
    box-shadow: 0 0 0 2px rgba(17,17,17,0.08) !important;
}

/* Slider thumb */
[data-testid="stSlider"] [role="slider"] {
    background: #111 !important;
    border-color: #111 !important;
}

/* ── CTA button ── */
div.stButton > button {
    background: #111 !important;
    color: #faf9f6 !important;
    border: 2px solid #111 !important;
    border-radius: 3px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.65rem 2.2rem !important;
    margin-top: 0.8rem !important;
    transition: background 0.18s, color 0.18s, transform 0.12s !important;
    cursor: pointer !important;
}
div.stButton > button:hover {
    background: #faf9f6 !important;
    color: #111 !important;
    transform: translateY(-1px) !important;
}
div.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── Result area ── */
.result-wrap {
    animation: fadeUp 0.5s ease both;
    margin: 1.2rem 0 0;
}

/* Big probability ticker */
.prob-ticker-wrap {
    padding: 2rem 2.2rem 1.8rem;
    background: #fff;
    border: 1.5px solid #e5e5e0;
    border-radius: 3px;
    position: relative;
    overflow: hidden;
}

.prob-ticker-wrap::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 5px;
}
.prob-ticker-wrap.low::before    { background: #3ecf8e; }
.prob-ticker-wrap.medium::before { background: #f6a623; }
.prob-ticker-wrap.high::before   { background: #e74c3c; }

.prob-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #aaa;
    margin: 0 0 0.4rem;
}

.prob-number {
    font-family: 'Playfair Display', serif;
    font-size: 5.5rem;
    font-weight: 900;
    line-height: 1;
    margin: 0;
    letter-spacing: -3px;
    animation: tickerIn 0.55s cubic-bezier(0.22,1,0.36,1) both;
}
.prob-number.low    { color: #3ecf8e; }
.prob-number.medium { color: #f6a623; }
.prob-number.high   { color: #e74c3c; }

.prob-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    font-weight: 500;
    color: #111;
    margin: 0.5rem 0 0;
}

.prob-threshold {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #bbb;
    margin: 0.35rem 0 0;
    letter-spacing: 0.04em;
}

/* Risk pill */
.risk-pill {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.28rem 0.85rem;
    border-radius: 999px;
    border: 1.5px solid;
    margin-top: 0.9rem;
}
.pill-low    { color: #1a9362; background: #edfaf4; border-color: #3ecf8e; }
.pill-medium { color: #9a6200; background: #fff8ed; border-color: #f6a623; }
.pill-high   { color: #c0392b; background: #fef0ef; border-color: #e74c3c; }

/* Action card */
.action-card {
    background: #fff;
    border: 1.5px solid #e5e5e0;
    border-radius: 3px;
    padding: 1.8rem 2rem;
    height: 100%;
    box-sizing: border-box;
    animation: fadeUp 0.5s 0.1s ease both;
    position: relative;
    overflow: hidden;
}
.action-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
}
.action-card.low::after    { background: #3ecf8e; }
.action-card.medium::after { background: #f6a623; }
.action-card.high::after   { background: #e74c3c; }

.action-mono {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #aaa;
    margin: 0 0 0.6rem;
}
.action-headline {
    font-family: 'Playfair Display', serif;
    font-size: 1.55rem;
    font-weight: 700;
    line-height: 1.2;
    color: #111;
    margin: 0 0 0.8rem;
}
.action-desc {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    font-weight: 300;
    color: #666;
    line-height: 1.7;
    margin: 0;
}

/* ── Separator ── */
.sep {
    border: none;
    border-top: 1.5px solid #e8e8e4;
    margin: 2.2rem 0;
}

/* ── Chart block ── */
.chart-card {
    background: #fff;
    border: 1.5px solid #e5e5e0;
    border-radius: 3px;
    padding: 1.6rem 1.8rem 1.8rem;
    animation: fadeUp 0.5s 0.2s ease both;
}

.chart-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #aaa;
    margin: 0 0 0.8rem;
}

/* ── Drivers ── */
.drivers-card {
    background: #fff;
    border: 1.5px solid #e5e5e0;
    border-radius: 3px;
    padding: 1.6rem 1.8rem;
    animation: fadeUp 0.5s 0.28s ease both;
}

.driver-item {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 0.7rem 0;
    border-bottom: 1px solid #f0f0eb;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.86rem;
    color: #444;
    line-height: 1.55;
    animation: slideIn 0.4s ease both;
}
.driver-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #111;
    flex-shrink: 0;
    margin-top: 0.38rem;
}

/* model info */
.minfo-table {
    margin-top: 1.4rem;
    border-top: 1.5px solid #e8e8e4;
    padding-top: 1rem;
}
.minfo-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 0.3rem 0;
    border-bottom: 1px solid #f2f2ee;
    font-size: 0.8rem;
}
.minfo-k {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #bbb;
    letter-spacing: 0.04em;
}
.minfo-v {
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    color: #444;
    font-size: 0.8rem;
}

/* ── Footer ── */
.footer {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.08em;
    color: #ccc;
    text-align: center;
    margin-top: 3rem;
    padding-top: 1.2rem;
    border-top: 1px solid #eee;
}

/* ── Progress bar ── */
.pbar-track {
    width: 100%;
    height: 5px;
    background: #f0f0eb;
    border-radius: 2px;
    margin: 1rem 0 0.3rem;
    overflow: hidden;
}
.pbar-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 1.2s cubic-bezier(0.22,1,0.36,1);
}

hr { border: none; border-top: 1.5px solid #e8e8e4; margin: 2rem 0; }
</style>
""", unsafe_allow_html=True)


# ── Helpers (LOGIC UNCHANGED) ────────────────────────────────────────────────
def bodily_injuries_label_to_value(label):
    return {"None": 0, "One reported injury": 1, "Multiple / serious injuries": 2}[label]

def witnesses_label_to_value(label):
    return {"No witnesses": 0, "One witness": 1, "Two witnesses": 2, "Three or more witnesses": 3}[label]

def risk_info(fraud_prob):
    if fraud_prob < 0.25:
        return "Low Risk",    "low",    "pill-low"
    elif fraud_prob < 0.50:
        return "Medium Risk", "medium", "pill-medium"
    return "High Risk",       "high",   "pill-high"

def action_info(fraud_prob):
    if fraud_prob >= 0.50:
        return "high",   "Send for Manual Investigation", \
               "The model score exceeds 50%. This claim requires a full investigator review before any payout is processed. Do not proceed automatically."
    elif fraud_prob >= THRESHOLD:
        return "medium", "Flag for Secondary Review", \
               "The score is above the decision threshold. Route for a supervisor spot-check and additional documentation before proceeding."
    return "low",    "Process Normally", \
           "No elevated risk signals detected. This claim may proceed through the standard workflow without additional review steps."


# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<p class="hdr-tag">◎ ML Risk Scoring &nbsp;·&nbsp; Portfolio Project</p>
<h1 class="hdr-title">Insurance Fraud<br>Detection</h1>
<div class="hdr-rule"></div>
<p class="hdr-sub">Random Forest classifier &nbsp;·&nbsp; threshold-tuned for recall &nbsp;·&nbsp; 12-feature deployment model</p>
""", unsafe_allow_html=True)


# ── Inputs ────────────────────────────────────────────────────────────────────
col_l, col_r = st.columns([1, 1], gap="large")

with col_l:
    st.markdown('<div class="input-card"><p class="sec-title">01 &nbsp; Incident Details</p>', unsafe_allow_html=True)

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
        "Witnesses Present",
        options=["No witnesses", "One witness", "Two witnesses", "Three or more witnesses"],
        value="One witness"
    )
    witnesses = witnesses_label_to_value(witnesses_label)
    months_as_customer = st.number_input("Months as Customer", min_value=0, value=200)

    st.markdown('</div>', unsafe_allow_html=True)

with col_r:
    st.markdown('<div class="input-card"><p class="sec-title">02 &nbsp; Claim & Policy Details</p>', unsafe_allow_html=True)

    total_claim_amount    = st.number_input("Total Claim Amount ($)",  min_value=0,   value=50000)
    injury_claim          = st.number_input("Injury Claim ($)",        min_value=0,   value=5000)
    property_claim        = st.number_input("Property Claim ($)",      min_value=0,   value=10000)
    vehicle_claim         = st.number_input("Vehicle Claim ($)",       min_value=0,   value=35000)
    policy_annual_premium = st.number_input("Annual Premium ($)",      min_value=0.0, value=1200.0, step=10.0)
    policy_deductable     = st.number_input("Policy Deductable ($)",   min_value=0,   value=1000)

    st.markdown('</div>', unsafe_allow_html=True)

predict = st.button("RUN ASSESSMENT →")


# ── Prediction block (LOGIC UNCHANGED) ───────────────────────────────────────
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

    risk_label, risk_cls, pill_cls  = risk_info(fraud_prob)
    action_cls, action_hl, action_d = action_info(fraud_prob)
    verdict = "Likely Fraudulent" if fraud_pred == 1 else "Likely Legitimate"

    pct       = round(fraud_prob * 100, 1)
    pct_disp  = f"{pct:.0f}%"
    bar_color = {"low": "#3ecf8e", "medium": "#f6a623", "high": "#e74c3c"}[risk_cls]

    # ── Section divider
    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown('<p class="sec-title">03 &nbsp; Model Output</p>', unsafe_allow_html=True)

    # ── Result row ──
    res_col, act_col = st.columns([1, 1], gap="large")

    with res_col:
        st.markdown(f"""
        <div class="prob-ticker-wrap {risk_cls}">
            <p class="prob-eyebrow">Fraud Probability Score</p>
            <p class="prob-number {risk_cls}">{pct_disp}</p>
            <div class="pbar-track">
                <div class="pbar-fill" style="width:{pct}%; background:{bar_color};"></div>
            </div>
            <p class="prob-threshold">Decision threshold · {int(THRESHOLD*100)}%</p>
            <p class="prob-label">{verdict}</p>
            <span class="{pill_cls} risk-pill">{risk_label}</span>
        </div>
        """, unsafe_allow_html=True)

    with act_col:
        st.markdown(f"""
        <div class="action-card {action_cls}">
            <p class="action-mono">Recommended Action</p>
            <p class="action-headline">{action_hl}</p>
            <p class="action-desc">{action_d}</p>
        </div>
        """, unsafe_allow_html=True)

    # ── Charts + Drivers ──
    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown('<p class="sec-title">04 &nbsp; Claim Analysis & Risk Drivers</p>', unsafe_allow_html=True)

    ch_col, dr_col = st.columns([1.2, 0.8], gap="large")

    other = max(0, total_claim_amount - injury_claim - property_claim - vehicle_claim)

    with ch_col:
        # chartosaur color palette — vivid, distinct
        chart_html = f"""
<div style="font-family:'DM Sans',sans-serif;">

  <p style="font-family:'DM Mono',monospace; font-size:0.65rem; letter-spacing:0.18em;
            text-transform:uppercase; color:#aaa; margin:0 0 0.9rem;">
    Claim composition
  </p>

  <div style="position:relative; width:100%; height:210px;">
    <canvas id="claimChart" role="img"
      aria-label="Claim composition bar chart: Injury ${injury_claim:,}, Property ${property_claim:,}, Vehicle ${vehicle_claim:,}, Other ${other:,}">
      Injury ${injury_claim:,} · Property ${property_claim:,} · Vehicle ${vehicle_claim:,} · Other ${other:,}
    </canvas>
  </div>

  <div style="display:flex; flex-wrap:wrap; gap:14px; margin:1rem 0 1.6rem; font-size:11px;
              font-family:'DM Mono',monospace; color:#888; letter-spacing:0.05em;">
    <span style="display:flex;align-items:center;gap:5px;">
      <span style="width:10px;height:10px;background:#e74c3c;border-radius:50%;"></span>Injury
    </span>
    <span style="display:flex;align-items:center;gap:5px;">
      <span style="width:10px;height:10px;background:#f6a623;border-radius:50%;"></span>Property
    </span>
    <span style="display:flex;align-items:center;gap:5px;">
      <span style="width:10px;height:10px;background:#3498db;border-radius:50%;"></span>Vehicle
    </span>
    <span style="display:flex;align-items:center;gap:5px;">
      <span style="width:10px;height:10px;background:#bdc3c7;border-radius:50%;"></span>Other
    </span>
  </div>

  <p style="font-family:'DM Mono',monospace; font-size:0.65rem; letter-spacing:0.18em;
            text-transform:uppercase; color:#aaa; margin:0 0 0.8rem;">
    Fraud score vs threshold
  </p>

  <div style="position:relative; width:100%; height:80px;">
    <canvas id="gaugeChart" role="img"
      aria-label="Horizontal gauge: model score {pct}%, threshold {int(THRESHOLD*100)}%">
      Model score {pct}% vs threshold {int(THRESHOLD*100)}%
    </canvas>
  </div>

</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<script>
(function() {{
  const tickCfg = {{
    color: '#aaa',
    font: {{ family: "'DM Mono', monospace", size: 10 }}
  }};
  const gridCfg = {{ color: '#f0f0eb' }};

  /* ── Claim bar chart ── */
  new Chart(document.getElementById('claimChart'), {{
    type: 'bar',
    data: {{
      labels: ['Injury', 'Property', 'Vehicle', 'Other'],
      datasets: [{{
        label: 'Amount ($)',
        data: [{injury_claim}, {property_claim}, {vehicle_claim}, {other}],
        backgroundColor: ['#e74c3c', '#f6a623', '#3498db', '#dce0e0'],
        borderWidth: 0,
        borderRadius: 2,
      }}]
    }},
    options: {{
      responsive: true,
      maintainAspectRatio: false,
      animation: {{
        duration: 900,
        easing: 'easeOutQuart',
        delay: (ctx) => ctx.dataIndex * 120,
      }},
      plugins: {{
        legend: {{ display: false }},
        tooltip: {{
          backgroundColor: '#111',
          titleFont: {{ family: "'DM Mono', monospace", size: 11 }},
          bodyFont:  {{ family: "'DM Sans', sans-serif",  size: 12 }},
          padding: 10,
          callbacks: {{
            label: (c) => '  $' + c.raw.toLocaleString()
          }}
        }}
      }},
      scales: {{
        x: {{
          grid:   {{ display: false }},
          ticks:  tickCfg,
          border: {{ display: false }}
        }},
        y: {{
          grid:   gridCfg,
          ticks:  {{ ...tickCfg, callback: (v) => '$' + v.toLocaleString() }},
          border: {{ display: false }}
        }}
      }}
    }}
  }});

  /* ── Gauge horizontal bar ── */
  new Chart(document.getElementById('gaugeChart'), {{
    type: 'bar',
    data: {{
      labels: ['Score', 'Threshold'],
      datasets: [{{
        data: [{pct}, {round(THRESHOLD*100,1)}],
        backgroundColor: ['{bar_color}', '#dce0e0'],
        borderWidth: 0,
        borderRadius: 3,
      }}]
    }},
    options: {{
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      animation: {{
        duration: 1100,
        easing: 'easeOutExpo',
        delay: (ctx) => ctx.dataIndex * 180,
      }},
      plugins: {{
        legend: {{ display: false }},
        tooltip: {{
          backgroundColor: '#111',
          titleFont: {{ family: "'DM Mono', monospace", size: 11 }},
          bodyFont:  {{ family: "'DM Sans', sans-serif",  size: 12 }},
          padding: 10,
          callbacks: {{ label: (c) => '  ' + c.raw + '%' }}
        }}
      }},
      scales: {{
        x: {{
          max: 100,
          grid:   gridCfg,
          ticks:  {{ ...tickCfg, callback: (v) => v + '%' }},
          border: {{ display: false }}
        }},
        y: {{
          grid:   {{ display: false }},
          ticks:  tickCfg,
          border: {{ display: false }}
        }}
      }}
    }}
  }});
}})();
</script>
"""
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.components.v1.html(chart_html, height=430)
        st.markdown('</div>', unsafe_allow_html=True)

    with dr_col:
        st.markdown('<div class="drivers-card">', unsafe_allow_html=True)
        st.markdown('<p class="sec-title">Risk Drivers</p>', unsafe_allow_html=True)

        risk_drivers = []
        if incident_severity in ["Major Damage", "Total Loss"]:
            risk_drivers.append(("High incident severity", "Strongly associated with elevated fraud risk across the training set."))
        if total_claim_amount >= 60000:
            risk_drivers.append(("Large total claim", "Amount exceeds the high-risk threshold of $60,000."))
        if number_of_vehicles_involved >= 2:
            risk_drivers.append(("Multiple vehicles", "Complex multi-vehicle incidents show higher fraud rates."))
        if bodily_injuries >= 1:
            risk_drivers.append(("Reported bodily injuries", "Injury claims are correlated with higher fraud incidence."))
        if witnesses >= 2:
            risk_drivers.append(("High witness count", "An unusually high number of witnesses may indicate staging."))
        if months_as_customer < 24:
            risk_drivers.append(("Short customer tenure", "Policy age under 24 months is a mild risk signal."))

        if not risk_drivers:
            st.markdown("""
            <div class="driver-item" style="border-bottom:none; color:#3ecf8e;">
                <div class="driver-dot" style="background:#3ecf8e; margin-top:0.35rem;"></div>
                <span>No major risk indicators triggered by the entered values.</span>
            </div>""", unsafe_allow_html=True)
        else:
            for i, (title, desc) in enumerate(risk_drivers):
                delay = i * 0.06
                st.markdown(f"""
                <div class="driver-item" style="animation-delay:{delay}s;">
                    <div class="driver-dot"></div>
                    <div>
                        <div style="font-weight:500; color:#111; margin-bottom:0.15rem;
                                    font-family:'DM Sans',sans-serif; font-size:0.85rem;">
                            {title}
                        </div>
                        <div style="font-size:0.8rem; color:#888; line-height:1.5;">{desc}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="minfo-table">
          <div class="minfo-row">
            <span class="minfo-k">Model type</span>
            <span class="minfo-v">Random Forest</span>
          </div>
          <div class="minfo-row">
            <span class="minfo-k">Optimisation</span>
            <span class="minfo-v">Threshold → recall</span>
          </div>
          <div class="minfo-row">
            <span class="minfo-k">Feature set</span>
            <span class="minfo-v">12 inputs (reduced)</span>
          </div>
          <div class="minfo-row" style="border-bottom:none;">
            <span class="minfo-k">Purpose</span>
            <span class="minfo-v">Portfolio demo</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <p class="footer">
        ◎ &nbsp; Portfolio demonstration &nbsp;·&nbsp; supports human review, not a replacement for professional investigation
    </p>""", unsafe_allow_html=True)