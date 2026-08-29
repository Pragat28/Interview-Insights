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
    # =====================================================

    search_result = search(
        query
    )

    query_types = search_result[
        "query_types"
    ]

    fields = search_result[
        "relevant_fields"
    ]

    company = search_result[
        "matched_companies"
    ]

    company_was_mentioned = search_result.get(
        "company_was_mentioned",
        False
    )


    # =====================================================
    # Unknown company
    # =====================================================

    if (
        company_was_mentioned
        and not company
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
                "",

            "companies_without_data":
                []
        }


    # =====================================================
    # MULTI-COMPANY RETRIEVAL
    #
    # Retrieve separately for every detected company.
    # Each company gets its own top results.
    #
    # companies_without_data tracks, by EXACT canonical
    # dataset name, any matched company for which we could
    # not find any usable rows (even after the per-company
    # fallback search). Previously this was silently dropped
    # — the loop just moved on — leaving the LLM to notice
    # (or not notice) the gap on its own, and to invent its
    # own label for that company using the user's original
    # wording instead of the dataset's actual name. Tracking
    # it explicitly here lets generate_answer.py report it
    # deterministically and with the correct name, instead of
    # leaving it to the model.
    # =====================================================

    if len(company) > 1:

        all_results = []
        candidate_count = 0
        companies_without_data = []

        for company_name in company:

            company_rows = df[
                df["company"] == company_name
            ]

            candidate_count += len(
                company_rows
            )

            if company_rows.empty:
                companies_without_data.append(
                    company_name
                )
                continue

            company_indices = company_rows.index.tolist()


            # =================================================
            # Retrieve this company's results
            # =================================================

            company_search_results = []

            for result in search_result[
                "results"
            ]:

                if result["index"] in company_indices:

                    company_search_results.append(
                        result
                    )


            # =================================================
            # If the global top-K did not contain this
            # company's results, perform a company-specific
            # retrieval.
            # =================================================

            if not company_search_results:

                company_result = search(
                    f"{query} at {company_name}"
                )

                company_search_results = [
                    result
                    for result in company_result.get(
                        "results",
                        []
                    )
                    if result["company"] == company_name
                ]


            # =================================================
            # If the fallback search STILL found nothing usable
            # for this company, record it as having no data
            # instead of silently dropping it.
            # =================================================

            if not company_search_results:
                companies_without_data.append(
                    company_name
                )
                continue


            # =================================================
            # Keep the best 2 results for this company
            # =================================================

            company_search_results = sorted(
                company_search_results,
                key=lambda x: x["similarity"],
                reverse=True
            )[:2]


            # =================================================
            # Add results without duplicates
            # =================================================

            for result in company_search_results:

                if not any(
                    existing["index"] == result["index"]
                    for existing in all_results
                ):

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

        companies_without_data = []


    # =====================================================
    # Build context
    # =====================================================

    context_parts = []


    for result in search_results:

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
            context,

        "companies_without_data":
            companies_without_data
    }