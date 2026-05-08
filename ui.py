import html as html_mod
import streamlit as st

from config import THRESHOLD


def esc(x):
    return html_mod.escape(str(x))


def rh(content: str) -> None:
    st.markdown(content, unsafe_allow_html=True)


def bi_val(label: str) -> int:
    return {"None": 0, "One reported injury": 1, "Multiple / serious injuries": 2}[label]


def wi_val(label: str) -> int:
    return {"No witnesses": 0, "One witness": 1, "Two witnesses": 2, "Three or more witnesses": 3}[label]


def risk_meta(p: float):
    if p < 0.25:
        return "b-low", "Low Risk", "var(--aurora-g)", "var(--aurora-g)"
    if p < 0.50:
        return "b-med", "Medium Risk", "var(--gold)", "var(--gold)"
    return "b-high", "High Risk", "var(--aurora-r)", "var(--aurora-r)"


def action_meta(p: float):
    if p >= 0.50:
        return (
            "Send for Manual Investigation",
            "Score significantly elevated. Assign to a specialist before any payout is authorised.",
        )
    if p >= THRESHOLD:
        return (
            "Flag for Secondary Review",
            "Score exceeds operating threshold. Route to supervisor review and collect supporting documentation.",
        )
    return (
        "Process Normally",
        "No elevated fraud signal detected. Claim may proceed through the standard processing route.",
    )


def render_header() -> None:
    rh("""
<div class="hdr">
  <div class="hdr-l">
    <div class="hdr-icon">
      <svg viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M7 1L1.5 3.5V7c0 2.8 2 5.3 5.5 5.9C10.5 12.3 12.5 9.8 12.5 7V3.5L7 1z"
              fill="white" fill-opacity="0.97"/>
        <path d="M4.5 7l2 2 3-3" stroke="#2bb5a0" stroke-width="1.6"
              stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
    <span class="hdr-name">Shield</span>
    <div class="hdr-divider"></div>
    <span class="hdr-sub">Insurance Fraud Intelligence</span>
  </div>
  <div class="hdr-r">
    <span class="chip chip-live"><span class="live-dot"></span>Model Active</span>
    <span class="chip">Random Forest</span>
    <span class="chip">Threshold 25%</span>
  </div>
</div>
""")


def render_hero() -> None:
    rh("""
<div class="hero">
  <div>
    <div class="hero-title">Fraud Risk <span>Assessment</span></div>
    <div class="hero-desc">Score claims in real time using 12 ML features across incident, policy, and financial data.</div>
  </div>
  <div class="hero-pills">
    <div class="hpill"><span class="hpill-v">12</span><span class="hpill-l">Features</span></div>
    <div class="hpill"><span class="hpill-v">91%</span><span class="hpill-l">Precision</span></div>
    <div class="hpill"><span class="hpill-v">RF</span><span class="hpill-l">Algorithm</span></div>
  </div>
</div>
""")


def render_incident_card() -> None:
    rh("""<div class="card">
  <div class="ctag">01 · Incident</div>
  <div class="ctitle">Vehicle Incident Details</div>
  <div class="cnote">Collision type, damage severity, injuries and witnesses.</div>
</div>""")


def render_financial_card() -> None:
    rh("""<div class="card">
  <div class="ctag">02 · Financials</div>
  <div class="ctitle">Policy &amp; Claim Amounts</div>
  <div class="cnote">Claim breakdown, annual premium and deductible.</div>
</div>""")


def render_results(fraud_prob: float, inputs: dict) -> None:
    fraud_pred = int(fraud_prob >= THRESHOLD)
    badge_cls, risk_label, text_col, bar_col = risk_meta(fraud_prob)
    action_title, action_desc = action_meta(fraud_prob)

    pct = round(fraud_prob * 100, 1)
    verdict = "Likely Fraudulent" if fraud_pred else "Likely Legitimate"
    pin_pct = min(max(pct, 2), 97)
    delta = abs(pct - THRESHOLD * 100)
    cpr = (inputs["total_claim_amount"] / inputs["policy_annual_premium"]) if inputs["policy_annual_premium"] else 0

    rh("""<div class="results-bar">
  <div class="results-line"></div>
  <span class="results-tag">Assessment Results</span>
  <div class="results-line"></div>
</div>""")

    rc, ac = st.columns(2, gap="large")

    with rc:
        rh(f"""<div class="card">
  <div class="ctag">03 · Model Output</div>
  <div class="ctitle">Fraud Probability Score</div>

  <div class="score-block">
    <div class="score-val" style="color:{text_col};">{pct:.0f}<span class="score-pct">%</span></div>
    <div class="score-label" style="color:{text_col};">Estimated fraud probability</div>
  </div>

  <div class="ptrack">
    <div class="ptrack-fill" style="width:{pct}%;background:{bar_col};--clr:{bar_col};"></div>
  </div>

  <div class="gauge">
    <div class="gauge-bar">
      <div class="gauge-pin" style="left:{pin_pct}%;"></div>
    </div>
    <div class="gauge-ticks">
      <span class="gauge-tick">0%</span>
      <span class="gauge-tick">25%</span>
      <span class="gauge-tick">50%</span>
      <span class="gauge-tick">75%</span>
      <span class="gauge-tick">100%</span>
    </div>
  </div>

  <div style="margin-top:0.95rem;">
    <div class="mrow"><span class="mk">Threshold</span><span class="mv">25%</span></div>
    <div class="mrow"><span class="mk">Delta from threshold</span><span class="mv">{delta:.1f} pp</span></div>
    <div class="mrow"><span class="mk">Verdict</span><span class="mv" style="color:{text_col};">{esc(verdict)}</span></div>
  </div>

  <span class="badge {badge_cls}"><span class="bdot"></span>{esc(risk_label)}</span>
</div>""")

    with ac:
        rh(f"""<div class="card">
  <div class="ctag">04 · Routing</div>
  <div class="ctitle">Recommended Action</div>

  <div class="action">
    <div class="action-t">{esc(action_title)}</div>
    <div class="action-d">{esc(action_desc)}</div>
  </div>

  <div class="mrow"><span class="mk">Incident type</span><span class="mv">{esc(inputs['incident_type'])}</span></div>
  <div class="mrow"><span class="mk">Severity</span><span class="mv">{esc(inputs['incident_severity'])}</span></div>
  <div class="mrow"><span class="mk">Total claimed</span><span class="mv">${inputs['total_claim_amount']:,}</span></div>
  <div class="mrow"><span class="mk">Claim-to-premium</span><span class="mv">{cpr:.1f}×</span></div>
  <div class="mrow"><span class="mk">Customer tenure</span><span class="mv">{inputs['months_as_customer']} months</span></div>
</div>""")

    render_driver_signals(inputs, cpr)


def render_driver_signals(inputs: dict, cpr: float) -> None:
    drivers = []
    if inputs["incident_severity"] in ["Major Damage", "Total Loss"]:
        drivers.append(("Severe vehicle damage", "Major damage or total loss significantly elevates review complexity."))
    if inputs["total_claim_amount"] >= 60000:
        drivers.append(("High claim amount", f"${inputs['total_claim_amount']:,} exceeds the $60k high-value threshold."))
    if inputs["number_of_vehicles_involved"] >= 2:
        drivers.append(("Multi-vehicle incident", "Multi-vehicle collisions require additional validation steps."))
    if inputs["bodily_injuries"] >= 1:
        drivers.append(("Injury component present", "Bodily injury claims require stronger supporting documentation."))
    if inputs["witnesses"] >= 2:
        drivers.append((f"{inputs['witnesses']} witnesses present", "Elevated witness count increases investigation complexity."))
    if inputs["months_as_customer"] < 24:
        drivers.append(("Short customer tenure", f"{inputs['months_as_customer']} months on policy — a mild but notable signal."))
    if cpr > 30:
        drivers.append(("High claim-to-premium ratio", f"Claim is {cpr:.0f}× the annual premium — statistically unusual."))

    d_html = "".join(
        f"""<div class="driver">
  <div class="driver-n">{str(i).zfill(2)}</div>
  <div><div class="driver-t">{esc(t)}</div><div class="driver-d">{esc(d)}</div></div>
</div>"""
        for i, (t, d) in enumerate(drivers, 1)
    ) if drivers else """
<div class="driver">
  <div class="driver-n">—</div>
  <div><div class="driver-t">No major signals triggered</div>
  <div class="driver-d">Entered values did not activate any primary review flags.</div></div>
</div>"""

    rh(f"""<div class="card">
  <div class="ctag">05 · Signals</div>
  <div class="ctitle">Key Risk Factors</div>
  <div class="cnote">Informational signals supporting triage — not deterministic decisions.</div>
  {d_html}
</div>""")


def render_footer() -> None:
    rh("""<div class="footer">Shield · Portfolio Demonstration · Triage support only — not automatic denial or approval</div>""")