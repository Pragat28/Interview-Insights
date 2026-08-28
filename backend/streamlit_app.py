import streamlit as st

from generate_answer import generate_answer


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Interview Insights — Case Archive",
    page_icon="🗂️",
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

if "answer" not in st.session_state:
    st.session_state["answer"] = None


# =========================================================
# CUSTOM CSS
# =========================================================

st.html("""
<style>

@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=Source+Sans+3:wght@400;500;600;700&display=swap');

:root {
    --ink: #14181f;
    --paper: #1d2330;
    --paper-raised: #242b3a;
    --stamp-red: #c0392b;
    --stamp-red-dim: rgba(192, 57, 43, 0.35);
    --file-gold: #c9a227;
    --text-hi: #ede9e0;
    --text-lo: #8a92a3;
    --rule: rgba(237, 233, 224, 0.12);
}

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
}

.stApp {
    background: var(--ink);
}

.block-container {
    max-width: 1180px;
    padding-top: 1.6rem;
    padding-bottom: 5rem;
}

h1, h2, h3, .mono {
    font-family: 'IBM Plex Mono', monospace;
}


/* =========================================================
   FOLDER TAB STRIP
   ========================================================= */

.tab-strip {
    display: flex;
    align-items: flex-end;
    gap: 0.4rem;
    margin-bottom: 0;
    border-bottom: 1px solid var(--rule);
}

.tab-strip .tab {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    padding: 0.5rem 1.1rem;
    border: 1px solid var(--rule);
    border-bottom: none;
    border-radius: 8px 8px 0 0;
    color: var(--text-lo);
    background: rgba(237, 233, 224, 0.02);
}

.tab-strip .tab.active {
    color: var(--text-hi);
    background: var(--paper);
    border-color: var(--rule);
}


/* =========================================================
   CASE HEADER / HERO
   ========================================================= */

.case-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 2rem;
    padding: 2.4rem 0 2rem 0;
    border-bottom: 1px dashed var(--rule);
    margin-bottom: 2.2rem;
}

.case-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    color: var(--file-gold);
    text-transform: uppercase;
    margin-bottom: 0.9rem;
}

.case-title {
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    font-size: clamp(2rem, 4vw, 3.1rem);
    line-height: 1.08;
    letter-spacing: -0.01em;
    color: var(--text-hi);
    margin: 0;
    max-width: 620px;
}

.case-title .accent {
    color: var(--stamp-red);
}

.case-subtitle {
    max-width: 560px;
    margin-top: 1rem;
    font-size: 1rem;
    line-height: 1.65;
    color: var(--text-lo);
}

.case-stamp {
    flex-shrink: 0;
    width: 108px;
    height: 108px;
    border: 2.5px solid var(--stamp-red);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transform: rotate(-9deg);
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    color: var(--stamp-red);
    text-align: center;
    line-height: 1.4;
    opacity: 0.85;
}

@media (max-width: 700px) {
    .case-header { flex-direction: column; }
    .case-stamp { align-self: flex-end; }
}


/* =========================================================
   REQUEST SLIP (SEARCH)
   ========================================================= */

.slip-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.06em;
    color: var(--text-lo);
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.slip-label span {
    color: var(--file-gold);
}

div[data-testid="stTextInput"] input {
    height: 3.1rem;
    border-radius: 4px;
    font-size: 1rem;
    background: var(--paper);
    border: 1px solid var(--rule);
    color: var(--text-hi);
    font-family: 'Source Sans 3', sans-serif;
}

div[data-testid="stTextInput"] input:focus {
    border-color: var(--stamp-red);
    box-shadow: 0 0 0 1px var(--stamp-red-dim);
}

/* =========================================================
   BUTTONS
   ========================================================= */

div.stButton > button {
    border-radius: 4px;
    min-height: 2.8rem;
    font-weight: 600;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    letter-spacing: 0.02em;
    transition: all 0.12s ease;
    background: var(--paper);
    border: 1px solid var(--rule);
    color: var(--text-hi);
}

div.stButton > button:hover {
    border-color: var(--file-gold);
    color: var(--file-gold);
}

div.stButton > button[kind="primary"] {
    background: var(--stamp-red);
    border: 1px solid var(--stamp-red);
    color: #fff;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    font-size: 0.8rem;
}

div.stButton > button[kind="primary"]:hover {
    background: #a5352a;
    border-color: #a5352a;
    color: #fff;
}


/* =========================================================
   SECTION HEADINGS
   ========================================================= */

.section-heading {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-hi);
    font-weight: 600;
    margin-top: 2.6rem;
    margin-bottom: 0.3rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.section-heading::before {
    content: "";
    width: 3px;
    height: 0.95rem;
    background: var(--stamp-red);
    display: inline-block;
}

.example-description {
    font-size: 0.88rem;
    color: var(--text-lo);
    margin-bottom: 1rem;
}


/* =========================================================
   CASE BRIEF (ANSWER)
   ========================================================= */

.case-brief {
    border-left: 3px solid var(--stamp-red);
    background: var(--paper);
    padding: 1.4rem 1.6rem;
    border-radius: 0 8px 8px 0;
    margin-top: 0.6rem;
}

.brief-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--stamp-red);
    margin-bottom: 0.6rem;
}

.case-brief .brief-body {
    color: var(--text-hi);
    font-size: 0.98rem;
    line-height: 1.7;
}

.case-brief p { margin-bottom: 0.7rem; }


/* =========================================================
   METADATA / TAGS
   ========================================================= */

.metadata-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 1rem;
}

.tag-company {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.03em;
    padding: 0.32rem 0.7rem;
    border-radius: 3px;
    border: 1px solid rgba(201, 162, 39, 0.4);
    color: var(--file-gold);
    background: rgba(201, 162, 39, 0.07);
}

.tag-topic {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.03em;
    padding: 0.32rem 0.7rem;
    border-radius: 3px;
    border: 1px solid var(--rule);
    color: var(--text-lo);
}


/* =========================================================
   FIELD REPORT CARDS (SOURCES)
   ========================================================= */

div[data-testid="stExpander"] {
    border: 1px solid var(--rule);
    border-radius: 6px;
    background: var(--paper);
    margin-bottom: 0.6rem;
}

div[data-testid="stExpander"] summary {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    color: var(--text-hi);
}

div[data-testid="stExpander"] summary:hover {
    color: var(--file-gold);
}


/* =========================================================
   EMPTY STATE — CASE UNSOLVED
   ========================================================= */

.empty-card {
    text-align: left;
    padding: 1.8rem 1.8rem;
    border: 1px dashed var(--rule);
    border-left: 3px solid var(--stamp-red);
    border-radius: 0 8px 8px 0;
    margin-top: 1.5rem;
    background: var(--paper);
}

.empty-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--stamp-red);
    font-weight: 700;
}

.empty-text {
    color: var(--text-lo);
    font-size: 0.9rem;
    margin-top: 0.5rem;
    line-height: 1.6;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    margin-top: 4rem;
    padding-top: 1.4rem;
    border-top: 1px solid var(--rule);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.04em;
    color: var(--text-lo);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.footer .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--stamp-red);
    display: inline-block;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {
    background: var(--paper);
    border-right: 1px solid var(--rule);
}

.sidebar-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--file-gold);
    margin-bottom: 0.3rem;
}

.sidebar-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-hi);
    margin-bottom: 0.6rem;
}

.sidebar-text {
    font-size: 0.85rem;
    line-height: 1.6;
    color: var(--text-lo);
}

.log-line {
    padding: 0.6rem 0;
    border-bottom: 1px solid var(--rule);
    font-size: 0.82rem;
    color: var(--text-hi);
    display: flex;
    gap: 0.6rem;
}

.log-number {
    font-family: 'IBM Plex Mono', monospace;
    color: var(--stamp-red);
    font-weight: 700;
    flex-shrink: 0;
}

.log-line-text { color: var(--text-lo); }

</style>
""")


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.html("""
    <div class="sidebar-tag">Case archive</div>
    <div class="sidebar-title">🗂️ Interview Insights</div>
    <div class="sidebar-text">
        A shared archive of real internship and placement interview
        reports, filed by students who sat in the room before you.
    </div>
    """)

    st.markdown("###")

    st.markdown("**How a query is processed**")

    steps = [
        ("01", "Read", "Parse the intent of your question"),
        ("02", "Match", "Identify the relevant company"),
        ("03", "Pull", "Retrieve matching field reports"),
        ("04", "Brief", "Generate a grounded answer"),
    ]

    for number, title, description in steps:
        st.html(f"""
        <div class="log-line">
            <span class="log-number">{number}</span>
            <span><strong>{title}</strong><br>
            <span class="log-line-text">{description}</span></span>
        </div>
        """)

    st.markdown("###")

    st.markdown("**What you can file a query about**")

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
# CASE HEADER
# =========================================================

st.html("""
<div class="tab-strip">
    <div class="tab active">📁 archive</div>
    <div class="tab">query log</div>
</div>

<div class="case-header">
    <div>
        <div class="case-eyebrow">Case archive · Student-filed reports</div>
        <h1 class="case-title">What actually happened<br>in the <span class="accent">interview room.</span></h1>
        <div class="case-subtitle">
            Every answer here is built from real interview reports filed by
            students — companies, questions, tests, prep, and advice, all
            searchable in plain language.
        </div>
    </div>
    <div class="case-stamp">OPEN<br>CASE</div>
</div>
""")


# =========================================================
# SEARCH AREA
# =========================================================

st.html("""
<div class="slip-label">File your <span>query</span></div>
""")

query = st.text_input(
    "Ask anything",
    value=st.session_state["query"],
    placeholder="e.g. What DSA topics were asked at BNY?",
    label_visibility="collapsed",
)

st.session_state["query"] = query


ask_clicked = st.button(
    "🔍  Search the archive",
    type="primary",
    use_container_width=True,
)


# =========================================================
# PROCESS QUERY (rendered immediately below the search box,
# so the answer never requires scrolling past the examples)
# =========================================================

if ask_clicked:

    if not query.strip():
        st.warning("Enter a question first.")

    else:

        with st.spinner("Pulling matching field reports..."):

            try:
                result = generate_answer(query)
            except Exception as error:
                st.error("Something went wrong while processing your question.")
                st.exception(error)
                result = None

        if result:

            # =================================================
            # UNKNOWN COMPANY
            # =================================================

            if result.get("candidate_count", 0) == 0 and not result.get("company"):

                st.html("""
                <div class="empty-card">
                    <div class="empty-title">⚠ Case unsolved</div>
                    <div class="empty-text">
                        No filed reports matched the company in your question.
                        Try another company, or broaden your query.
                    </div>
                </div>
                """)

            else:

                # =================================================
                # SAVE HISTORY
                # =================================================

                if query not in st.session_state["history"]:
                    st.session_state["history"].insert(0, query)
                    st.session_state["history"] = st.session_state["history"][:5]

                # =================================================
                # ANSWER
                # =================================================

                st.html("""<div class="section-heading">Case brief</div>""")

                answer_text = result.get("answer", "No answer was generated.")

                st.html(f"""
                <div class="case-brief">
                    <div class="brief-eyebrow">✦ Answer, from filed reports</div>
                </div>
                """)

                st.markdown(answer_text)

                # =================================================
                # METADATA
                # =================================================

                companies_found = result.get("company", [])
                query_types = result.get("query_types", [])

                if companies_found or query_types:

                    tags_html = "".join(
                        f'<span class="tag-company">🏢 {c}</span>' for c in companies_found
                    ) + "".join(
                        f'<span class="tag-topic">#{q}</span>' for q in query_types
                    )

                    st.html(f'<div class="metadata-row">{tags_html}</div>')

                # =================================================
                # SOURCES
                # =================================================

                results = result.get("results", [])

                if results:

                    st.html("""
                    <div class="section-heading">Field reports retrieved</div>
                    """)

                    st.caption("Each answer above is built from these filed reports.")

                    for source in results:

                        experience_id = source.get("experience_id", "Unknown")
                        company = source.get("company", "Unknown company")
                        role = source.get("role", "")
                        score = source.get("similarity", None)

                        with st.expander(f"🏢 {company}  ·  Report {experience_id}"):

                            if role:
                                st.markdown(f"**Role:** {role}")

                            if score is not None:
                                st.caption(f"Relevance: {float(score):.2f}")

                            document_text = source.get("document_text", "")

                            if document_text:
                                st.write(document_text)


# =========================================================
# EXAMPLE QUESTIONS
# =========================================================

st.html("""
<div class="section-heading">Common queries</div>
<div class="example-description">Not sure where to start? Pull one of these.</div>
""")


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
        if st.button(example, key=f"example_{index}", use_container_width=True):
            st.session_state["query"] = example
            st.rerun()


# =========================================================
# RECENT QUESTIONS
# =========================================================

if st.session_state["history"]:

    st.html("""<div class="section-heading">Recent inquiries</div>""")

    for index, previous_query in enumerate(st.session_state["history"]):
        if st.button(previous_query, key=f"history_{index}", use_container_width=True):
            st.session_state["query"] = previous_query
            st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.html("""
<div class="footer">
    <span class="dot"></span>
    ARCHIVE STATUS: OPEN — Interview Insights, built from student-filed reports
</div>
""")