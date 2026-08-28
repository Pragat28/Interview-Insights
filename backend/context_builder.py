from pathlib import Path

import pandas as pd

from search_embeddings import search


# =========================================================
# 1. Project paths
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"


# =========================================================
# 2. Load dataset
# =========================================================

df = pd.read_csv(
    DATA_DIR / "interview_insights_dataset (1).csv"
)


# =========================================================
# 3. Build context
# =========================================================

def build_context(query):

    # =====================================================
    # Initial retrieval
    #
    # This determines:
    # - intents
    # - relevant fields
    # - mentioned companies
    # =====================================================

    search_result = search(query)

    query_types = search_result["query_types"]
    fields = search_result["relevant_fields"]

    company = search_result["matched_companies"]
    company_was_mentioned = search_result.get(
        "company_was_mentioned",
        False
    )


    # =====================================================
    # Unknown company
    # =====================================================

    if company_was_mentioned and not company:

        return {

            "query":
                query,

            "company":
                [],

            "candidate_count":
                0,

            "company_was_mentioned":
                True,

            "query_types":
                query_types,

            "fields":
                fields,

            "context":
                ""
        }


    # =====================================================
    # MULTI-COMPANY RETRIEVAL
    #
    # If multiple companies were detected, search for each
    # company separately.
    #
    # This prevents one company's experiences from pushing
    # another company's experiences out of the top-K results.
    # =====================================================

    if len(company) > 1:

        all_results = []
        candidate_count = 0

        for company_name in company:

            company_query = f"{query} at {company_name}"

            company_result = search(
                company_query
            )

            candidate_count += company_result.get(
                "candidate_count",
                0
            )

            for result in company_result.get(
                "results",
                []
            ):

                # Avoid duplicate experiences
                if result["index"] not in [
                    item["index"]
                    for item in all_results
                ]:

                    all_results.append(
                        result
                    )

        search_results = all_results

    else:

        candidate_count = search_result[
            "candidate_count"
        ]

        search_results = search_result[
            "results"
        ]


    # =====================================================
    # Build context
    # =====================================================

    context_parts = []


    for result in search_results:

        index = result["index"]

        row = df.iloc[index]


        # =================================================
        # Basic metadata
        # =================================================

        text = (

            f"Company: "
            f"{row['company']}\n"

            f"Experience Type: "
            f"{row['experience_type']}\n"

            f"Branch: "
            f"{row['branch']}\n"

            f"Role: "
            f"{row['role']}\n"

        )


        # =================================================
        # Relevant fields only
        # =================================================

        for field in fields:

            value = row[field]

            if (
                pd.notna(value)
                and str(value).strip()
            ):

                text += (

                    "\n"
                    f"{field.replace('_', ' ').title()}:\n"
                    f"{value}\n"

                )


        context_parts.append(
            text
        )


    # =====================================================
    # Separate experiences
    # =====================================================

    context = (

        "\n"
        + "-" * 70
        + "\n"

    ).join(
        context_parts
    )


    # =====================================================
    # Return
    # =====================================================

    return {

        "query":
            query,

        "company":
            company,

        "candidate_count":
            candidate_count,

        "company_was_mentioned":
            company_was_mentioned,

        "query_types":
            query_types,

        "fields":
            fields,

        "context":
            context
    }