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
    # Retrieval
    #
    # search() now performs:
    #
    # query
    #   -> intent embeddings
    #   -> top-K intents
    #   -> intent resolver LLM
    #   -> document retrieval
    #
    # Therefore we MUST use the query_types and fields
    # returned by search().
    # =====================================================

    search_result = search(
        query
    )


    # =====================================================
    # Get resolved intents and fields
    # =====================================================

    query_types = search_result[
        "query_types"
    ]

    fields = search_result[
        "relevant_fields"
    ]


    # =====================================================
    # Unknown company
    # =====================================================

    if (
        search_result.get(
            "company_was_mentioned",
            False
        )
        and not search_result[
            "matched_companies"
        ]
    ):

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
    # Build context
    # =====================================================

    context_parts = []


    for result in search_result[
        "results"
    ]:

        index = result[
            "index"
        ]

        row = df.iloc[
            index
        ]


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
            search_result[
                "matched_companies"
            ],

        "candidate_count":
            search_result[
                "candidate_count"
            ],

        "company_was_mentioned":
            search_result.get(
                "company_was_mentioned",
                False
            ),

        "query_types":
            query_types,

        "fields":
            fields,

        "context":
            context
    }