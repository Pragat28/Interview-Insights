import re
import pandas as pd

from search_embeddings import search


# =========================================================
# 1. Load dataset
# =========================================================

df = pd.read_csv(
    "../data/interview_insights_dataset (1).csv"
)


# =========================================================
# 2. Query type -> relevant dataset fields
# =========================================================

QUERY_FIELDS = {

    "preparation": [
        "test_preparation",
        "important_topics",
        "resources"
    ],

    "selection": [
        "selection_procedure",
        "test_description",
        "interview_experience"
    ],

    "test": [
        "test_description",
        "test_preparation",
        "important_topics"
    ],

    "interview": [
        "interview_experience",
        "important_topics"
    ],

    "eligibility": [
        "eligibility"
    ],

    "topics": [
        "important_topics"
    ],

    "projects": [
        "projects",
        "interview_experience"
    ],

    "compensation": [
        "compensation"
    ],

    "advice": [
        "junior_advice",
        "last_minute_preparation"
    ]
}


# =========================================================
# 3. Keywords -> query type
# =========================================================

QUERY_KEYWORDS = {

    "preparation": [
        "how should i prepare",
        "how do i prepare",
        "how to prepare",
        "prepare for",
        "preparation",
        "prepare",
        "practice",
        "learn",
        "ready"
    ],

    "selection": [
        "selection process",
        "selection procedure",
        "selection",
        "rounds",
        "stages"
    ],

    "test": [
        "online assessment",
        "coding test",
        "assessment",
        "test",
        "oa"
    ],

    "interview": [
        "technical interview",
        "technical round",
        "hr interview",
        "hr round",
        "interview questions",
        "questions asked",
        "what questions",
        "what was asked",
        "what were asked",
        "interview experience",
        "interview"
    ],

    "eligibility": [
        "eligibility",
        "eligible",
        "cgpa",
        "criteria"
    ],

    "topics": [
        "computer networks",
        "operating system",
        "topics",
        "subjects",
        "dsa",
        "dbms",
        "oops",
        "os",
        "cn"
    ],

    "projects": [
        "what projects",
        "which projects",
        "projects",
        "project",
        "resume"
    ],

    "compensation": [
        "compensation",
        "stipend",
        "salary",
        "package",
        "ctc"
    ],

    "advice": [
        "last minute",
        "suggestions",
        "advice",
        "tips",
        "juniors"
    ]
}


# =========================================================
# 4. Helper: phrase matching
# =========================================================

def contains_phrase(query, phrase):

    query = query.lower()
    phrase = phrase.lower()

    pattern = r"\b" + re.escape(phrase) + r"\b"

    return bool(
        re.search(
            pattern,
            query
        )
    )


# =========================================================
# 5. Detect query types
# =========================================================

def detect_query_types(query):

    detected_types = []

    query = query.lower()

    for query_type, keywords in QUERY_KEYWORDS.items():

        # Check longer phrases first
        keywords = sorted(
            keywords,
            key=len,
            reverse=True
        )

        for keyword in keywords:

            if contains_phrase(
                query,
                keyword
            ):

                detected_types.append(
                    query_type
                )

                break

    return detected_types


# =========================================================
# 6. Determine whether "interview" is a real intent
# =========================================================

def has_explicit_interview_question(query):

    explicit_phrases = [

        "questions asked",
        "what questions",
        "what was asked",
        "what were asked",
        "which questions",
        "interview questions",
        "interview experience",
        "technical round",
        "hr round",
        "hr interview"
    ]

    for phrase in explicit_phrases:

        if contains_phrase(
            query,
            phrase
        ):

            return True

    return False


# =========================================================
# 7. Find fields required for query
# =========================================================

def get_relevant_fields(query):

    detected_types = detect_query_types(
        query
    )

    query_types = detected_types.copy()


    # =====================================================
    # Handle interview intent
    # =====================================================

    # Example:
    #
    # "How should I prepare for BNY's technical interview?"
    #
    # Detected:
    # preparation + interview
    #
    # But "interview" here only describes the thing
    # we are preparing for. It is NOT asking what happened
    # in previous interviews.
    #
    # Therefore remove interview.
    #
    # -----------------------------------------------------
    #
    # Example:
    #
    # "What projects should I explain and what questions
    # were asked?"
    #
    # Detected:
    # projects + interview
    #
    # Here interview IS a genuine intent, so keep it.
    # =====================================================

    if (
        "preparation" in query_types
        and "interview" in query_types
        and not has_explicit_interview_question(query)
    ):

        query_types.remove(
            "interview"
        )


    # =====================================================
    # Build final field list
    # =====================================================

    fields = []

    for query_type in query_types:

        for field in QUERY_FIELDS[
            query_type
        ]:

            if field not in fields:

                fields.append(
                    field
                )


    # =====================================================
    # Fallback
    # =====================================================

    if not fields:

        fields = [
            "selection_procedure",
            "test_description",
            "test_preparation",
            "interview_experience",
            "important_topics"
        ]


    return (
        query_types,
        fields
    )


# =========================================================
# 8. Build context
# =========================================================

def build_context(query):

    # -----------------------------------------------------
    # Retrieve relevant experiences
    # -----------------------------------------------------

    search_result = search(
        query
    )


    # -----------------------------------------------------
    # Determine query types and fields
    # -----------------------------------------------------

    query_types, fields = (
        get_relevant_fields(
            query
        )
    )


    context_parts = []


    # -----------------------------------------------------
    # Build context from retrieved documents
    # -----------------------------------------------------

    for result in search_result["results"]:

        index = result["index"]

        row = df.iloc[
            index
        ]


        # -------------------------------------------------
        # Basic metadata
        # -------------------------------------------------

        text = (
            f"Company: {row['company']}\n"
            f"Experience Type: {row['experience_type']}\n"
            f"Branch: {row['branch']}\n"
            f"Role: {row['role']}\n"
        )


        # -------------------------------------------------
        # Add only relevant fields
        # -------------------------------------------------

        for field in fields:

            value = row[field]

            if (
                pd.notna(value)
                and str(value).strip()
            ):

                text += (
                    f"\n"
                    f"{field.replace('_', ' ').title()}:\n"
                    f"{value}\n"
                )


        context_parts.append(
            text
        )


    # -----------------------------------------------------
    # Separate candidate experiences
    # -----------------------------------------------------

    context = (
        "\n"
        + "\n" + "-" * 70 + "\n"
    ).join(
        context_parts
    )


    # -----------------------------------------------------
    # Return context
    # -----------------------------------------------------

    return {

        "query":
            query,

        "company":
            search_result[
                "matched_companies"
            ],

        "candidate_count":
            search_result[
                "candidate_count"
            ],

        "query_types":
            query_types,

        "fields":
            fields,

        "context":
            context
    }