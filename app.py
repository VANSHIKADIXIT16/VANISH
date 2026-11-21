
import streamlit as st
import pandas as pd
from datetime import datetime

# ----------------------------------
# VANISH - Main Application
# ----------------------------------

st.set_page_config(
    page_title="VANISH | Digital Forensics",
    page_icon="🔐",
    layout="wide"
)

# ----------------------------------
# Custom Styling
# ----------------------------------

st.markdown("""
<style>
    .stApp {
        background-color: #0b1220;
        color: #ffffff;
    }

    [data-testid="stSidebar"] {
        background-color: #111c2e;
    }

    .main-title {
        font-size: 38px;
        font-weight: 800;
        color: #55c7ed;
    }

    .subtitle {
        font-size: 15px;
        color: #aab8ca;
    }

    .metric-card {
        background-color: #17263a;
        border: 1px solid #29425e;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 10px;
    }

    .metric-label {
        color: #aab8ca;
        font-size: 14px;
    }

    .metric-value {
        color: #ffffff;
        font-size: 29px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# ----------------------------------
# Sidebar Navigation
# ----------------------------------

st.sidebar.title("🔐 VANISH")
st.sidebar.caption("Digital Forensic Audit Platform")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "Evidence Collection",
        "SHA-256 Integrity Verification",
        "Erasure Verification",
        "AI Analysis",
        "Cloud Audit",
        "Forensic Reports"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "VANISH 1.0\n\n"
    "Verification and Audit of Networked "
    "Information Sanitisation and Handling"
)


# ----------------------------------
# Dashboard
# ----------------------------------

if page == "Dashboard":

    st.markdown(
        '<div class="main-title">VANISH</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Digital Forensic Erasure Verification System'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.success("VANISH forensic auditing workspace is ready.")

    st.subheader("System Overview")

    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        ("Files Scanned", "0"),
        ("Evidence Collected", "0"),
        ("Residual Files", "0"),
        ("Audit Status", "Ready")
    ]

    for column, (label, value) in zip(
        [col1, col2, col3, col4], metrics
    ):
        with column:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    st.subheader("Recent Audit Activity")

    activity = pd.DataFrame({
        "Activity": [
            "VANISH application started",
            "Forensic workspace initialised",
            "Dashboard loaded"
        ],
        "Status": [
            "Successful",
            "Successful",
            "Successful"
        ]
    })

    st.dataframe(
        activity,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Dashboard currently uses demonstration data. "
        "Live forensic statistics will be connected "
        "in subsequent development stages."
    )


# ----------------------------------
# Evidence Collection
# ----------------------------------

elif page == "Evidence Collection":

    st.title("📁 Evidence Collection")

    st.write(
        "This module will scan authorised test folders "
        "and collect file metadata."
    )

    st.info("Evidence collection engine: Coming in Day 2.")

    st.write("Planned features:")
    st.write("- Folder selection")
    st.write("- File metadata extraction")
    st.write("- Evidence timestamps")
    st.write("- SHA-256 evidence records")


# ----------------------------------
# SHA-256 Verification
# ----------------------------------

elif page == "SHA-256 Integrity Verification":

    st.title("🔏 SHA-256 Integrity Verification")

    st.write(
        "This module will calculate and compare "
        "cryptographic hashes of collected evidence."
    )

    st.info("Hash verification engine: Coming in Day 3.")


# ----------------------------------
# Erasure Verification
# ----------------------------------

elif page == "Erasure Verification":

    st.title("🔍 Erasure Verification")

    st.write("VANISH will classify evidence into four outcomes.")

    results = {
        "Verified": "All defined checks passed within scope.",
        "Partially Verified": "Some checks passed, but evidence is incomplete.",
        "Failed": "Evidence contradicts the erasure claim.",
        "Inconclusive": "Insufficient evidence for a conclusion."
    }

    for status, description in results.items():
        with st.expander(status):
            st.write(description)

    st.info("Decision engine: Coming in Day 3.")


# ----------------------------------
# AI Analysis
# ----------------------------------

elif page == "AI Analysis":

    st.title("🤖 AI-Assisted Analysis")

    st.write(
        "AI will explain forensic findings and "
        "identify missing evidence."
    )

    st.info("AI analysis module: Coming in Day 4.")


# ----------------------------------
# Cloud Audit
# ----------------------------------

elif page == "Cloud Audit":

    st.title("☁️ Cloud Evidence Audit")

    st.write(
        "This module will analyse authorised cloud "
        "metadata and deletion-related records."
    )

    st.info("Cloud audit module: Coming in Day 4.")


# ----------------------------------
# Forensic Reports
# ----------------------------------

elif page == "Forensic Reports":

    st.title("📄 Forensic Reports")

    st.write(
        "This module will generate downloadable "
        "forensic audit reports in PDF format."
    )

    st.info("PDF reporting module: Coming in Day 5.")


# ----------------------------------
# Footer
# ----------------------------------

st.sidebar.divider()

st.sidebar.caption(
    "VANISH Research Prototype | Version 1.0"
)

st.sidebar.caption(
    f"Session: {datetime.now().strftime('%d-%m-%Y %H:%M')}"
)
