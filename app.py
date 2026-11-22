from modules.verification_engine import evaluate_erasure
from modules.hash_verifier import verify_all_evidence
from pathlib import Path
import pandas as pd

from modules.evidence_collector import (
    scan_folder,
    get_all_evidence,
    ALLOWED_ROOT,
    initialise_database
)
import streamlit as st
import pandas as pd
from datetime import datetime
initialise_database()

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

    evidence_count = len(get_all_evidence())
    integrity_count = len(st.session_state.get("hash_results", []))
    erasure_result = st.session_state.get("erasure_result")
    erasure_status = (
        erasure_result.get("status", "Not assessed")
        if erasure_result else "Not assessed"
    )
    metrics = [
        ("Evidence Records", evidence_count),
        ("Integrity Checks", integrity_count),
        ("Erasure Assessment", erasure_status),
        ("System Status", "Ready")
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
# SHA-256 INTEGRITY VERIFICATION
# ----------------------------------

elif page == "SHA-256 Integrity Verification":

    st.title("🔏 SHA-256 Integrity Verification")

    st.write(
        "Compare previously collected SHA-256 hashes "
        "against the current contents of evidence files."
    )

    if st.button("🔍 Verify Evidence Integrity"):

        with st.spinner("Verifying evidence hashes..."):

            results = verify_all_evidence()

        if results:

            st.session_state["hash_results"] = results

            st.success(
                f"Verification completed for {len(results)} records."
            )

        else:

            st.warning("No stored evidence records found.")

    results = st.session_state.get("hash_results", [])

    if results:

        df = pd.DataFrame(results)

        st.subheader("Integrity Verification Results")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        match_count = sum(
            r["integrity_status"] == "MATCH"
            for r in results
        )

        modified_count = sum(
            r["integrity_status"] == "MODIFIED"
            for r in results
        )

        missing_count = sum(
            r["integrity_status"] == "MISSING"
            for r in results
        )

        error_count = sum(
            r["integrity_status"] in ["ERROR", "UNSTABLE"]
            for r in results
        )

        st.divider()

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Matching", match_count)
        c2.metric("Modified", modified_count)
        c3.metric("Missing", missing_count)
        c4.metric("Errors / Unstable", error_count)

        st.caption(
            "A matching hash establishes content consistency "
            "with the recorded baseline, not proof of secure erasure."
        )


# ----------------------------------
# EVIDENCE COLLECTION
# ----------------------------------

elif page == "Evidence Collection":

    st.title("📁 Evidence Collection")

    st.write(
        "Scan authorised test folders and collect "
        "digital forensic evidence."
    )

    st.info(
        f"Authorised evidence directory: {ALLOWED_ROOT}"
    )

    # Choose a folder inside the evidence directory
    folder_input = st.text_input(
        "Enter test folder path",
        value=str(ALLOWED_ROOT / "test_files")
    )

    if st.button("🔍 Start Forensic Scan"):

        try:

            with st.spinner(
                "Collecting forensic evidence..."
            ):

                records = scan_folder(folder_input)

            st.success(
                f"Scan completed! {len(records)} "
                "file records processed."
            )

            if records:

                df = pd.DataFrame(records)

                st.subheader("Collected Evidence")

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )

                successful = sum(
                    r["collection_status"] == "COLLECTED"
                    for r in records
                )

                failed = sum(
                    r["collection_status"] == "ERROR"
                    for r in records
                )

                unstable = sum(
                    r["collection_status"] == "UNSTABLE"
                    for r in records
                )

                col1, col2, col3 = st.columns(3)

                col1.metric("Collected", successful)
                col2.metric("Errors", failed)
                col3.metric("Unstable", unstable)

            else:

                st.warning(
                    "No files were found in this folder."
                )

        except (ValueError, OSError) as error:

            st.error(f"Scan could not be completed: {error}")

    # Display previous evidence records
    st.divider()

    st.subheader("Previously Collected Evidence")

    previous_records = get_all_evidence()

    if previous_records:

        previous_df = pd.DataFrame(previous_records)

        st.dataframe(
            previous_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No evidence has been collected yet.")


# ----------------------------------
# ERASURE VERIFICATION
# ----------------------------------

elif page == "Erasure Verification":

    st.title("🔍 Erasure Verification Engine")

    st.write(
        "Evaluate whether available forensic evidence "
        "supports a digital erasure claim."
    )

    st.warning(
        "A missing file does not independently prove "
        "permanent or secure erasure."
    )

    target_path = st.text_input(
        "Target file path",
        value=str(
            ALLOWED_ROOT / "test_files" / "confidential.txt"
        )
    )

    st.subheader("Evidence Coverage")

    st.caption(
        "These checkboxes are analyst attestations. "
        "They do not perform automatic backup or cloud scans."
    )

    backup_checked = st.checkbox(
        "I have completed and documented the relevant backup checks."
    )

    cloud_checked = st.checkbox(
        "I have completed and documented the relevant cloud checks."
    )

    if st.button("⚖️ Evaluate Erasure Claim"):

        # Get current integrity results
        integrity_results = verify_all_evidence()

        result = evaluate_erasure(
            target_path=target_path,
            integrity_results=integrity_results,
            backup_checked=backup_checked,
            cloud_checked=cloud_checked
        )

        st.session_state["erasure_result"] = result

    result = st.session_state.get("erasure_result")

    if result:

        st.divider()

        st.subheader("Forensic Assessment")

        status = result["status"]

        if status == "VERIFIED":

            st.success("VERIFIED")

        elif status == "PARTIALLY VERIFIED":

            st.warning("PARTIALLY VERIFIED")

        elif status == "FAILED":

            st.error("FAILED")

        else:

            st.info("INCONCLUSIVE")

        st.write("**Reason for classification:**")

        st.write(result["reason"])

        st.caption(
            "Assessment is restricted to the documented "
            "investigation scope. It does not establish "
            "the absence of every possible copy."
        )


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
