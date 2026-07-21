
import streamlit as st
import ast
import plotly.graph_objects as go

from ai_analyzer import analyze_scam


# =====================================================
# SESSION STATISTICS
# =====================================================

if "total_scans" not in st.session_state:
    st.session_state.total_scans = 0

if "high_risk_scans" not in st.session_state:
    st.session_state.high_risk_scans = 0

if "safe_scans" not in st.session_state:
    st.session_state.safe_scans = 0


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="ScamShield AI",
    page_icon="🛡️",
    layout="wide"
)


# =====================================================
# DARK CYBERSECURITY THEME
# =====================================================

st.markdown("""
<style>

.stApp {
    background-color: #0b1120;
    color: #e2e8f0;
}

.block-container {
    padding-top: 2rem;
}

/* Hero Section */
.hero {
    padding: 30px;
    border-radius: 18px;
    background: linear-gradient(135deg, #111827, #172554);
    border: 1px solid #1e40af;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 42px;
    color: #38bdf8;
    margin-bottom: 5px;
}

.hero p {
    font-size: 18px;
    color: #cbd5e1;
}

/* Attack Chain */
.attack-step {
    padding: 15px;
    margin: 8px 0;
    border-left: 5px solid #38bdf8;
    background: linear-gradient(90deg, #172554, #111827);
    border-radius: 8px;
    font-size: 18px;
    color: #e0f2fe;
}

/* Safety Checklist */
.safety-step {
    padding: 12px;
    margin: 6px 0;
    background-color: #111827;
    border: 1px solid #334155;
    border-radius: 8px;
    font-size: 16px;
    color: #cbd5e1;
}

/* Text Area */
textarea {
    background-color: #111827 !important;
    color: #f8fafc !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #2563eb, #0891b2);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px;
    font-size: 17px;
    font-weight: bold;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #1d4ed8, #0e7490);
}

/* Metrics */
[data-testid="stMetric"] {
    background-color: #111827;
    border: 1px solid #334155;
    padding: 15px;
    border-radius: 12px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Selectbox */
[data-baseweb="select"] > div {
    background-color: #111827;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="hero">

<h1>🛡️ ScamShield AI</h1>

<p>
Explainable AI-powered fraud intelligence for detecting,
understanding, and preventing digital scams.
</p>

</div>
""", unsafe_allow_html=True)


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🛡️ ScamShield AI")

    st.markdown("---")

    st.markdown("### Platform")

    st.write("🔍 Threat Analyzer")
    st.write("🧠 Explainable AI")
    st.write("📊 Risk Intelligence")
    st.write("🛡️ Victim Protection")

    st.markdown("---")

    st.info(
        "ScamShield AI analyzes suspicious communications "
        "and explains the manipulation tactics used by scammers."
    )


# =====================================================
# DEMO SCENARIOS
# =====================================================

st.subheader("⚡ Try a Demo Scenario")

demo_options = {

    "Select a scenario": "",

    "🔴 Digital Arrest Scam":
    """This is an officer from the CBI Cyber Crime Department.
Your Aadhaar card has been used in a money laundering case.
You are under digital arrest. Do not disconnect this video call.
Transfer ₹50,000 immediately or you will be arrested today.""",

    "🔴 Investment Scam":
    """Our AI trading platform guarantees 300% returns in just 7 days.
Deposit ₹10,000 now and our expert team will manage your investment.
This opportunity is available only for the next 2 hours.
Guaranteed profit with zero risk.""",

    "🟠 Job Scam":
    """Congratulations! You have been selected for a work-from-home job
with a salary of ₹80,000 per month.
Pay a refundable registration fee of ₹4,999 today to confirm your position.""",

    "🔴 Bank/KYC Phishing":
    """URGENT: Your bank account will be blocked today because your KYC has expired.
Click this link immediately to update your KYC.
Enter your account number, ATM PIN and OTP to verify your identity.""",

    "🟢 Normal Message":
    """Your order has been shipped and is expected to arrive tomorrow between
10 AM and 2 PM. You can track your delivery through the official shopping application."""
}


selected_demo = st.selectbox(
    "Choose a sample threat to test the system",
    list(demo_options.keys())
)


# =====================================================
# MESSAGE INPUT
# =====================================================

if selected_demo != "Select a scenario":

    message = st.text_area(
        "Message to analyze",
        value=demo_options[selected_demo],
        height=180
    )

else:

    message = st.text_area(
        "🔍 Paste a suspicious SMS, email, WhatsApp message, or call transcript",
        height=180,
        placeholder="Paste suspicious communication here..."
    )


# =====================================================
# ANALYZE BUTTON
# =====================================================

if st.button(
    "🚨 ANALYZE THREAT",
    use_container_width=True
):

    if not message.strip():

        st.warning("Please enter a suspicious message first.")

    else:

        with st.spinner("🧠 AI is analyzing the threat..."):

            try:

                # AI ANALYSIS
                result = analyze_scam(message)


                # Convert string dictionary into Python dictionary
                if isinstance(result, str):

                    result = ast.literal_eval(result)


                # Update statistics
                st.session_state.total_scans += 1

                risk_level = result["risk_level"].upper()


                if risk_level in ["HIGH", "CRITICAL"]:

                    st.session_state.high_risk_scans += 1


                elif risk_level == "LOW":

                    st.session_state.safe_scans += 1


                st.divider()


                # =====================================================
                # THREAT INTELLIGENCE REPORT
                # =====================================================

                st.subheader("🔎 Threat Intelligence Report")


                # =====================================================
                # SCAN OVERVIEW
                # =====================================================

                st.subheader("📊 Scan Overview")

                overview_col1, overview_col2, overview_col3 = st.columns(3)


                with overview_col1:

                    st.metric(
                        "🔍 Total Scans",
                        st.session_state.total_scans
                    )


                with overview_col2:

                    st.metric(
                        "🚨 High/Critical Threats",
                        st.session_state.high_risk_scans
                    )


                with overview_col3:

                    st.metric(
                        "🟢 Safe Messages",
                        st.session_state.safe_scans
                    )


                st.divider()


                # =====================================================
                # KEY THREAT METRICS
                # =====================================================

                col1, col2, col3 = st.columns(3)


                with col1:

                    st.metric(
                        "🚨 Risk Level",
                        result["risk_level"]
                    )


                with col2:

                    st.metric(
                        "📊 Risk Score",
                        f'{result["risk_score"]}/100'
                    )


                with col3:

                    st.metric(
                        "🏷️ Scam Category",
                        result["category"]
                    )


                # =====================================================
                # RISK GAUGE
                # =====================================================

                st.divider()

                st.subheader("📊 Threat Severity")


                fig = go.Figure(
                    go.Indicator(
                        mode="gauge+number",
                        value=result["risk_score"],
                        title={
                            "text": "Scam Risk Score"
                        },
                        gauge={
                            "axis": {
                                "range": [0, 100]
                            },
                            "steps": [
                                {
                                    "range": [0, 30]
                                },
                                {
                                    "range": [30, 70]
                                },
                                {
                                    "range": [70, 100]
                                }
                            ]
                        }
                    )
                )


                fig.update_layout(

                    paper_bgcolor="#0b1120",

                    font={
                        "color": "#e2e8f0"
                    }

                )


                st.plotly_chart(
                    fig,
                    use_container_width=True
                )


                # =====================================================
                # SCAM ATTACK CHAIN
                # =====================================================

                st.divider()

                st.subheader("🧠 Scam Attack Chain")


                st.caption(
                    "ScamShield AI maps the manipulation strategy used by the scammer."
                )


                category = result["category"].lower().strip()


                if any(
                    word in category
                    for word in [
                        "investment",
                        "invest",
                        "trading",
                        "crypto"
                    ]
                ):

                    attack_chain = [

                        "🎭 Fake Investment Opportunity",
                        "💰 Promise of Guaranteed Returns",
                        "⏰ Limited-Time Pressure",
                        "💸 Request for Money Transfer",
                        "🎯 Potential Financial Loss"

                    ]


                elif any(
                    word in category
                    for word in [
                        "digital arrest",
                        "arrest",
                        "impersonation",
                        "authority"
                    ]
                ):

                    attack_chain = [

                        "🎭 Authority Impersonation",
                        "😨 Fear of Arrest",
                        "📵 Victim Isolation",
                        "⏰ Urgent Payment Demand",
                        "💸 Financial Extortion"

                    ]


                elif any(
                    word in category
                    for word in [
                        "job",
                        "employment",
                        "work from home",
                        "recruitment"
                    ]
                ):

                    attack_chain = [

                        "💼 Fake Job Offer",
                        "💰 Unrealistic Salary Promise",
                        "🧾 Registration Fee Demand",
                        "⏰ Urgency Pressure",
                        "💸 Financial Loss"

                    ]


                elif any(
                    word in category
                    for word in [
                        "upi",
                        "payment",
                        "lottery",
                        "prize",
                        "reward"
                    ]
                ):

                    attack_chain = [

                        "🎁 Fake Reward or Payment Request",
                        "🔗 Malicious Payment Link",
                        "🔐 OTP or Payment Manipulation",
                        "💸 Unauthorized Transaction",
                        "🎯 Financial Loss"

                    ]


                elif any(
                    word in category
                    for word in [
                        "phishing",
                        "kyc",
                        "bank",
                        "account"
                    ]
                ):

                    attack_chain = [

                        "🏦 Bank or Organization Impersonation",
                        "⚠️ Fake Account Problem",
                        "⏰ Urgency Pressure",
                        "🔗 Malicious Link or Data Request",
                        "🔐 Credential Theft"

                    ]


                else:

                    attack_chain = [

                        "📩 Suspicious Communication",
                        "⚠️ Deception or Manipulation",
                        "⏰ Urgency Pressure",
                        "💰 Request for Money or Data",
                        "🎯 Potential Victimization"

                    ]


                for i, step in enumerate(attack_chain):

                    st.markdown(
                        f"""
                        <div class="attack-step">
                        <b>Step {i + 1}</b> → {step}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                # =====================================================
                # DETECTED RED FLAGS
                # =====================================================

                st.divider()

                st.subheader("🚩 Detected Threat Signals")


                for flag in result["red_flags"]:

                    st.warning(
                        f"⚠️ {flag}"
                    )


                # =====================================================
                # EXPLAINABLE AI
                # =====================================================

                st.subheader("🧠 Why Was This Flagged?")


                st.info(
                    result["explanation"]
                )


                # =====================================================
                # RECOMMENDED PROTECTION
                # =====================================================

                st.subheader("🛡️ Recommended Protection")


                st.success(
                    result["recommended_action"]
                )


                # =====================================================
                # SAFETY CHECKLIST
                # =====================================================

                st.divider()

                st.subheader("🛡️ Immediate Safety Checklist")


                safety_steps = [

                    "❌ Do not transfer money",
                    "❌ Do not share OTP, PIN, passwords, or sensitive personal information",
                    "📵 Disconnect suspicious calls",
                    "📞 Verify the claim through official channels",
                    "📸 Save screenshots and evidence",
                    "🚨 Report the incident to the appropriate cybercrime authorities"

                ]


                for step in safety_steps:

                    st.markdown(
                        f"""
                        <div class="safety-step">
                        {step}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


            except Exception as e:

                st.error(
                    f"Error while analyzing the message: {e}"
                )

