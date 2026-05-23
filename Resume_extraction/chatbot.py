import streamlit as st


# ============================================================
# REQUIRED FIELDS
# ============================================================

REQUIRED_FIELDS = [

    "Full Name",

    "Email",

    "Phone Number",

    "Location",

    "Total Experience",

    "Technical Skills"
]


# ============================================================
# SESSION INITIALIZATION
# ============================================================

def initialize_chatbot():

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = []

    if "missing_fields" not in st.session_state:

        st.session_state.missing_fields = []

    if "current_question" not in st.session_state:

        st.session_state.current_question = None

    if "resume_processed" not in st.session_state:

        st.session_state.resume_processed = False

    if "extracted_data" not in st.session_state:

        st.session_state.extracted_data = {}


# ============================================================
# FIND MISSING FIELDS
# ============================================================

def find_missing_fields(
    extracted_data
):

    missing = []

    for field in REQUIRED_FIELDS:

        if (

            field not in extracted_data

            or not extracted_data[field]
        ):

            missing.append(field)

    return missing


# ============================================================
# CHATBOT ENGINE
# ============================================================

def run_chatbot():

    if not st.session_state.missing_fields:

        st.session_state.missing_fields = (

            find_missing_fields(
                st.session_state.extracted_data
            )
        )

    # --------------------------------------------------------

    if (

        st.session_state.missing_fields

        and not st.session_state.current_question
    ):

        next_field = (

            st.session_state
            .missing_fields[0]
        )

        st.session_state.current_question = (
            next_field
        )

        st.session_state.chat_history.append(

            (
                "assistant",

                f"Please provide your {next_field}"
            )
        )

    # --------------------------------------------------------

    for role, message in (

        st.session_state.chat_history
    ):

        with st.chat_message(role):

            st.markdown(message)

    # --------------------------------------------------------

    if st.session_state.current_question:

        user_input = st.chat_input(
            "Type your answer..."
        )

        if user_input:

            st.session_state.chat_history.append(

                (
                    "user",
                    user_input
                )
            )

            field = (
                st.session_state
                .current_question
            )

            st.session_state.extracted_data[
                field
            ] = user_input

            st.session_state.missing_fields.pop(
                0
            )

            # NEXT QUESTION

            if st.session_state.missing_fields:

                next_field = (

                    st.session_state
                    .missing_fields[0]
                )

                st.session_state.current_question = (
                    next_field
                )

                st.session_state.chat_history.append(

                    (
                        "assistant",

                        f"Please provide your {next_field}"
                    )
                )

            else:

                st.session_state.current_question = None

                st.session_state.chat_history.append(

                    (
                        "assistant",

                        "Your profile is complete."
                    )
                )

            st.rerun()