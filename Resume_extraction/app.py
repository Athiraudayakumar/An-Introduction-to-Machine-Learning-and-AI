import streamlit as st

from resume_parser import (
    process_resume
)

from embedding import (
    intelligent_search
)

from chatbot import (
    initialize_chatbot,
    run_chatbot
)


# ============================================================
# STREAMLIT CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Resume Intelligence System",
    layout="wide"
)

st.title("AI Resume Intelligence System")


# ============================================================
# SESSION STATE
# ============================================================

initialize_chatbot()


# ============================================================
# UPLOAD RESUME
# ============================================================

st.sidebar.header("Upload Resume")

uploaded_file = st.sidebar.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)


if uploaded_file:

    with open(uploaded_file.name, "wb") as f:

        f.write(uploaded_file.getbuffer())

    st.sidebar.success("Resume Uploaded")

    if st.sidebar.button("Process Resume"):

        with st.spinner("Processing Resume..."):

            extracted_data = process_resume(
                uploaded_file.name
            )

            st.session_state.extracted_data = (
                extracted_data
            )

            st.session_state.resume_processed = True

        st.success("Resume Processed Successfully")


# ============================================================
# CHATBOT VERIFICATION
# ============================================================

if st.session_state.resume_processed:

    st.header("Candidate Verification")

    run_chatbot()


# ============================================================
# FINAL PROFILE
# ============================================================

if st.session_state.extracted_data:

    st.subheader("Final Candidate Profile")

    st.json(
        st.session_state.extracted_data
    )


# ============================================================
# RECRUITER SEARCH
# ============================================================

st.header("Recruiter Search")

query = st.text_input(
    "Search Candidates",
    placeholder="Find Spark engineers in Bangalore"
)

if st.button("Search"):

    results = intelligent_search(query)

    for result in results:

        st.markdown("---")

        st.write(
            f"### {result['name']}"
        )

        st.write(
            f"Location: {result['location']}"
        )

        st.write(
            f"Email: {result['email']}"
        )

        st.write(
            f"Phone: {result['phone']}"
        )

        st.write(
            f"Score: {round(result['score'], 3)}"
        )

        st.write(
            result["text"]
        )