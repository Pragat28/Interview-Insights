import streamlit as st

from generate_answer import generate_answer


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Interview Insights",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# SESSION STATE
# =========================================================

if "query" not in st.session_state:
    st.session_state["query"] = ""

if "history" not in st.session_state:
    st.session_state["history"] = []


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 50% 0%,
                rgba(99, 102, 241, 0.08),
                transparent 35%
            );
    }


    /* =====================================================
       HERO
       ===================================================== */

    .hero {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem 1rem;
    }

    .hero-badge {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        border-radius: 999px;
        background: rgba(99, 102, 241, 0.10);
        border: 1px solid rgba(99, 102, 241, 0.22);
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    .hero-title {
        font-size: clamp(2.4rem, 5vw, 4.2rem);
        line-height: 1.05;
        font-weight: 800;
        letter-spacing: -0.045em;
        margin: 0;
    }

    .hero-title span {
        background: linear-gradient(
            90deg,
            #6366f1,
            #8b5cf6
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        max-width: 680px;
        margin: 1rem auto 0 auto;
        font-size: 1.05rem;
        line-height: 1.7;
        opacity: 0.68;
    }


    /* =====================================================
       SEARCH
       ===================================================== */

    .search-label {
        font-size: 0.85rem;
        font-weight: 650;
        margin-bottom: 0.45rem;
        opacity: 0.8;
    }

    div[data-testid="stTextInput"] input {
        height: 3.2rem;
        border-radius: 12px;
        font-size: 1rem;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 1px #6366f1;
    }

    .search-hint {
        text-align: center;
        font-size: 0.78rem;
        opacity: 0.45;
        margin-top: 0.55rem;
    }


    /* =====================================================
       EXAMPLES
       ===================================================== */

    .section-heading {
        font-size: 1.15rem;
        font-weight: 700;
        margin-top: 2.5rem;
        margin-bottom: 0.9rem;
    }

    .example-description {
        font-size: 0.88rem;
        opacity: 0.55;
        margin-bottom: 1rem;
    }

    div.stButton > button {
        border-radius: 11px;
        min-height: 2.8rem;
        font-weight: 500;
        transition: all 0.15s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-1px);
        border-color: rgba(99, 102, 241, 0.5);
    }


    /* =====================================================
       ANSWER
       ===================================================== */

    .answer-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-top: 2.8rem;
        margin-bottom: 0.8rem;
    }

    .answer-icon {
        width: 34px;
        height: 34px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        background: rgba(99, 102, 241, 0.12);
        font-size: 1rem;
    }

    .answer-title {
        font-size: 1.2rem;
        font-weight: 700;
    }

    .answer-card {
        border: 1px solid rgba(128, 128, 128, 0.18);
        border-radius: 18px;
        padding: 1.6rem 1.8rem;
        background: rgba(128, 128, 128, 0.035);
        line-height: 1.75;
    }


    /* =====================================================
       METADATA
       ===================================================== */

    .metadata-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin-top: 1rem;
    }

    .metadata-pill {
        padding: 0.3rem 0.65rem;
        border-radius: 999px;
        border: 1px solid rgba(128, 128, 128, 0.22);
        font-size: 0.76rem;
        opacity: 0.8;
    }


    /* =====================================================
       SOURCE CARDS
       ===================================================== */

    .source-card {
        border: 1px solid rgba(128, 128, 128, 0.18);
        border-radius: 14px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.7rem;
        background: rgba(128, 128, 128, 0.025);
    }

    .source-company {
        font-size: 0.92rem;
        font-weight: 700;
    }

    .source-role {
        font-size: 0.8rem;
        opacity: 0.55;
        margin-top: 0.15rem;
    }

    .source-score {
        font-size: 0.75rem;
        opacity: 0.45;
    }


    /* =====================================================
       EMPTY STATE
       ===================================================== */

    .empty-card {
        text-align: center;
        padding: 2.2rem 1rem;
        border: 1px dashed rgba(128, 128, 128, 0.28);
        border-radius: 18px;
        margin-top: 2rem;
    }

    .empty-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }

    .empty-title {
        font-size: 1.05rem;
        font-weight: 650;
    }

    .empty-text {
        opacity: 0.55;
        font-size: 0.88rem;
        margin-top: 0.35rem;
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .footer {
        text-align: center;
        margin-top: 4rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(128, 128, 128, 0.12);
        font-size: 0.78rem;
        opacity: 0.45;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(128, 128, 128, 0.12);
    }

    .sidebar-title {
        font-size: 1.15rem;
        font-weight: 750;
        margin-bottom: 0.3rem;
    }

    .sidebar-text {
        font-size: 0.82rem;
        line-height: 1.6;
        opacity: 0.6;
    }

    .pipeline-step {
        padding: 0.65rem 0;
        border-bottom: 1px solid rgba(128, 128, 128, 0.10);
        font-size: 0.82rem;
    }

    .pipeline-number {
        display: inline-flex;
        width: 24px;
        height: 24px;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        background: rgba(99, 102, 241, 0.12);
        margin-right: 0.45rem;
        font-size: 0.72rem;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🎯 Interview Insights</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-text">
            A student-focused search system for discovering
            real internship and placement experiences.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("###")

    st.markdown("**How it works**")

    steps = [
        ("1", "Understand", "Detect the intent of your question"),
        ("2", "Filter", "Identify the relevant company"),
        ("3", "Retrieve", "Find relevant student experiences"),
        ("4", "Answer", "Generate a grounded response"),
    ]

    for number, title, description in steps:

        st.markdown(
            f"""
            <div class="pipeline-step">
                <span class="pipeline-number">{number}</span>
                <strong>{title}</strong><br>
                <span style="opacity:0.5;margin-left:2.1rem;">
                    {description}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("###")

    st.markdown("**What you can ask**")

    st.caption(
        "• Preparation\n\n"
        "• Interview questions\n\n"
        "• Selection process\n\n"
        "• Online tests\n\n"
        "• DSA / DBMS / OS / OOPS\n\n"
        "• Projects\n\n"
        "• Eligibility\n\n"
        "• Compensation\n\n"
        "• Advice"
    )


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-badge">
            ✦ Student-powered interview knowledge
        </div>

        <h1 class="hero-title">
            Learn from <span>real experiences.</span>
        </h1>

        <div class="hero-subtitle">
            Search internship and placement experiences shared by
            students. Ask about companies, interviews, tests,
            preparation, topics and more.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SEARCH AREA
# =========================================================

st.markdown(
    '<div class="search-label">Ask anything about placements</div>',
    unsafe_allow_html=True,
)

query = st.text_input(
    "Ask anything",
    value=st.session_state["query"],
    placeholder="e.g. What DSA topics were asked at BNY?",
    label_visibility="collapsed",
)

st.session_state["query"] = query

ask_clicked = st.button(
    "🔍  Search experiences",
    type="primary",
    use_container_width=True,
)

st.markdown(
    """
    <div class="search-hint">
        Ask naturally — you don't need to know the exact company or category.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# EXAMPLE QUESTIONS
# =========================================================

st.markdown(
    '<div class="section-heading">💡 Explore the experiences</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="example-description">'
    'Not sure what to ask? Try one of these.'
    '</div>',
    unsafe_allow_html=True,
)

example_questions = [
    "How should I prepare for BNY?",
    "What questions were asked in BNY technical interviews?",
    "What is the selection process for Wells Fargo?",
    "What stipend does BNY Mellon offer?",
    "What DSA topics were asked?",
    "What projects were discussed during interviews?",
]

cols = st.columns(2)

for index, example in enumerate(example_questions):

    with cols[index % 2]:

        if st.button(
            example,
            key=f"example_{index}",
            use_container_width=True,
        ):

            st.session_state["query"] = example
            st.rerun()


# =========================================================
# PROCESS QUERY
# =========================================================

if ask_clicked:

    if not query.strip():

        st.warning("Enter a question first.")

    else:

        with st.spinner("Searching student experiences..."):

            try:

                result = generate_answer(query)

            except Exception as error:

                st.error(
                    "Something went wrong while processing your question."
                )

                st.exception(error)

                result = None


        if result:

            # =================================================
            # UNKNOWN COMPANY
            # =================================================

            if (
                result.get("candidate_count", 0) == 0
                and not result.get("company")
            ):

                st.markdown(
                    """
                    <div class="empty-card">

                        <div class="empty-icon">🔎</div>

                        <div class="empty-title">
                            No experiences found
                        </div>

                        <div class="empty-text">
                            We couldn't find experiences matching the
                            company in your question.
                            Try another company or ask a general question.
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            else:

                # =================================================
                # SAVE HISTORY
                # =================================================

                if query not in st.session_state["history"]:

                    st.session_state["history"].insert(
                        0,
                        query
                    )

                    st.session_state["history"] = (
                        st.session_state["history"][:5]
                    )


                # =================================================
                # ANSWER HEADER
                # =================================================

                st.markdown(
                    """
                    <div class="answer-header">

                        <div class="answer-icon">
                            ✦
                        </div>

                        <div class="answer-title">
                            Answer
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )


                # =================================================
                # ANSWER
                # =================================================

                st.markdown(
                    '<div class="answer-card">',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    result.get(
                        "answer",
                        "No answer was generated."
                    )
                )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True,
                )


                # =================================================
                # METADATA
                # =================================================

                companies_found = result.get(
                    "company",
                    []
                )

                query_types = result.get(
                    "query_types",
                    []
                )

                if companies_found or query_types:

                    pills = ""

                    for company in companies_found:

                        pills += (
                            f'<span class="metadata-pill">'
                            f'🏢 {company}'
                            f'</span>'
                        )

                    for query_type in query_types:

                        pills += (
                            f'<span class="metadata-pill">'
                            f'#{query_type}'
                            f'</span>'
                        )

                    st.markdown(
                        f'<div class="metadata-row">{pills}</div>',
                        unsafe_allow_html=True,
                    )


                # =================================================
                # SOURCES
                # =================================================

                results = result.get(
                    "results",
                    []
                )

                if results:

                    st.markdown(
                        '<div class="section-heading">'
                        '📚 Retrieved experiences'
                        '</div>',
                        unsafe_allow_html=True,
                    )

                    st.caption(
                        "These student experiences were used to "
                        "construct the answer."
                    )

                    for source in results:

                        experience_id = source.get(
                            "experience_id",
                            "Unknown"
                        )

                        company = source.get(
                            "company",
                            "Unknown company"
                        )

                        role = source.get(
                            "role",
                            ""
                        )

                        score = source.get(
                            "similarity"
                        )

                        score_text = ""

                        if score is not None:

                            score_text = (
                                f" · relevance "
                                f"{float(score):.2f}"
                            )

                        with st.expander(
                            f"🏢 {company}  ·  {experience_id}"
                        ):

                            if role:

                                st.markdown(
                                    f"**Role:** {role}"
                                )

                            if score_text:

                                st.caption(
                                    score_text
                                )

                            document_text = source.get(
                                "document_text",
                                ""
                            )

                            if document_text:

                                st.write(
                                    document_text
                                )


                # =================================================
                # TECHNICAL DETAILS
                # =================================================

                with st.expander(
                    "⚙️ Search details"
                ):

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.metric(
                            "Candidates",
                            result.get(
                                "candidate_count",
                                0
                            ),
                        )

                    with col2:

                        st.metric(
                            "Retrieved",
                            result.get(
                                "retrieved_count",
                                len(results)
                            ),
                        )

                    with col3:

                        st.metric(
                            "Intents",
                            len(query_types),
                        )


                    fields = result.get(
                        "fields",
                        []
                    )

                    if fields:

                        st.markdown(
                            "**Fields used for retrieval**"
                        )

                        st.write(
                            ", ".join(fields)
                        )


# =========================================================
# RECENT QUESTIONS
# =========================================================

if st.session_state["history"]:

    st.markdown(
        '<div class="section-heading">'
        '🕘 Recent questions'
        '</div>',
        unsafe_allow_html=True,
    )

    for previous_query in st.session_state["history"]:

        if st.button(
            previous_query,
            key=f"history_{previous_query}",
            use_container_width=True,
        ):

            st.session_state["query"] = previous_query
            st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        Interview Insights · Built from student-reported experiences
    </div>
    """,
    unsafe_allow_html=True,
)