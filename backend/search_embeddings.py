import re

import pandas as pd
import numpy as np
import spacy

from sentence_transformers import SentenceTransformer, util


# =========================================================
# 1. Load dataset
# =========================================================

df = pd.read_csv(
    "../data/interview_insights_dataset (1).csv"
)

print("Loaded responses:", len(df))


# =========================================================
# 2. Load embeddings
# =========================================================

document_embeddings = np.load(
    "../data/embeddings.npy"
)


# =========================================================
# 3. Load the SAME embedding model
# =========================================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# =========================================================
# 4. Load spaCy POS tagger
# =========================================================

nlp = spacy.load(
    "en_core_web_sm"
)


# =========================================================
# 5. Get UNIQUE company names from dataset
# =========================================================

companies = (
    df["company"]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
    .tolist()
)


# Sort longer company names first
companies = sorted(
    companies,
    key=len,
    reverse=True
)


# =========================================================
# 6. Company aliases
# =========================================================

COMPANY_ALIASES = {

    "bny": "BNY Mellon",
    "bny mellon": "BNY Mellon",

    "wells": "Wells Fargo",
    "wells fargo": "Wells Fargo",

    "db": "Deutsche Bank",
    "deutsche": "Deutsche Bank",
    "deutsche bank": "Deutsche Bank",

    "hpcl":
        "Hindustan Petroleum Corporation Limited (HPCL)",

    "bpcl":
        "Bharat Petroleum Corporation Limited",

    "ti":
        "Texas Instruments",

    "jpmc":
        "JP Morgan Chase",

    "jp morgan":
        "JP Morgan Chase",

    "jpmorgan":
        "JP Morgan Chase",

    "qualcomm":
        "Qualcomm India Private Ltd.",

    "cisco":
        "Cisco",

    "nvidia":
        "Nvidia",

    "amazon":
        "Amazon",

    "accenture":
        "Accenture"
}


# =========================================================
# 7. Normalize text
# =========================================================

def normalize_text(text):

    text = str(text).lower()

    # Remove possessive
    # BNY's -> BNY
    # Amazon's -> Amazon

    text = re.sub(
        r"'s\b",
        "",
        text
    )

    # Replace punctuation with spaces

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    # Remove extra spaces

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


# =========================================================
# 8. Check whether a phrase occurs as a complete phrase
# =========================================================

def phrase_in_text(
    phrase,
    text
):

    normalized_phrase = normalize_text(
        phrase
    )

    normalized_text = normalize_text(
        text
    )

    pattern = (
        r"\b"
        + re.escape(normalized_phrase)
        + r"\b"
    )

    return bool(
        re.search(
            pattern,
            normalized_text
        )
    )


# =========================================================
# 9. Detect company
#
#    1. Direct company-name matching
#    2. POS tagging
#    3. Alias matching
# =========================================================

def detect_company(query):

    normalized_query = normalize_text(
        query
    )

    matches = []


    # =====================================================
    # STEP 1
    # Direct match against actual dataset companies
    # =====================================================

    for company in companies:

        if phrase_in_text(
            company,
            normalized_query
        ):

            matches.append(
                company
            )


    # =====================================================
    # STEP 2
    # POS tagging
    # =====================================================

    doc = nlp(
        query
    )

    proper_nouns = []

    for token in doc:

        if token.pos_ == "PROPN":

            proper_nouns.append(
                normalize_text(
                    token.text
                )
            )


    # Remove duplicate proper nouns

    proper_nouns = list(
        dict.fromkeys(
            proper_nouns
        )
    )


    # =====================================================
    # STEP 3
    # Match proper nouns against aliases
    # =====================================================

    for noun in proper_nouns:

        if noun in COMPANY_ALIASES:

            company = COMPANY_ALIASES[
                noun
            ]

            if company in companies:

                matches.append(
                    company
                )


    # =====================================================
    # STEP 4
    # Directly check multi-word aliases
    #
    # Example:
    # "Wells Fargo"
    # "JP Morgan"
    # =====================================================

    for alias, company in COMPANY_ALIASES.items():

        if phrase_in_text(
            alias,
            normalized_query
        ):

            if company in companies:

                matches.append(
                    company
                )


    # =====================================================
    # STEP 5
    # Remove duplicates while preserving order
    # =====================================================

    return list(
        dict.fromkeys(
            matches
        )
    )


# =========================================================
# 10. Get candidate documents
# =========================================================

def get_candidates(query):

    matched_companies = detect_company(
        query
    )


    # -----------------------------------------------------
    # No company mentioned
    # -----------------------------------------------------

    if not matched_companies:

        candidates = df

        return (
            candidates,
            matched_companies
        )


    # -----------------------------------------------------
    # One or more companies mentioned
    # -----------------------------------------------------

    candidates = df[
        df["company"].isin(
            matched_companies
        )
    ]


    return (
        candidates,
        matched_companies
    )


# =========================================================
# 11. Semantic search
# =========================================================

def search(
    query,
    top_k=2
):

    # -----------------------------------------------------
    # Step 1: Detect companies and get candidates
    # -----------------------------------------------------

    candidates, matched_companies = (
        get_candidates(query)
    )


    # -----------------------------------------------------
    # Step 2: Convert query into embedding
    # -----------------------------------------------------

    query_embedding = model.encode(
        query,
        convert_to_tensor=True
    )


    results = []


    # =====================================================
    # CASE 1:
    # Multiple companies
    #
    # Retrieve up to top_k from EACH company.
    #
    # Example:
    #
    # BNY + Wells Fargo
    #
    # top_k = 2
    #
    # BNY        -> 2
    # Wells      -> 2
    #
    # Total      -> up to 4
    # =====================================================

    if len(matched_companies) > 1:

        for company in matched_companies:

            # ---------------------------------------------
            # Get documents belonging to this company
            # ---------------------------------------------

            company_candidates = df[
                df["company"] == company
            ]

            company_indices = (
                company_candidates.index.tolist()
            )


            # ---------------------------------------------
            # Get embeddings
            # ---------------------------------------------

            company_embeddings = (
                document_embeddings[
                    company_indices
                ]
            )


            # ---------------------------------------------
            # Calculate similarity
            # ---------------------------------------------

            similarities = util.cos_sim(
                query_embedding,
                company_embeddings
            )[0]


            # ---------------------------------------------
            # Retrieve top_k for THIS company
            # ---------------------------------------------

            k = min(
                top_k,
                len(company_candidates)
            )


            top_results = similarities.argsort(
                descending=True
            )[:k]


            # ---------------------------------------------
            # Build results
            # ---------------------------------------------

            for result_index in top_results:

                position = result_index.item()

                original_index = (
                    company_indices[position]
                )

                row = df.iloc[
                    original_index
                ]


                results.append({

                    "index":
                        original_index,

                    "experience_id":
                        row["experience_id"],

                    "experience_type":
                        row["experience_type"],

                    "branch":
                        row["branch"],

                    "company":
                        row["company"],

                    "role":
                        row["role"],

                    "similarity":
                        similarities[
                            position
                        ].item(),

                    "document_text":
                        row["document_text"]
                })


        # -------------------------------------------------
        # Sort all results by relevance
        #
        # This means the final context receives the most
        # relevant experiences first.
        # -------------------------------------------------

        results = sorted(
            results,
            key=lambda x: x["similarity"],
            reverse=True
        )


    # =====================================================
    # CASE 2:
    # Single company OR no company
    # =====================================================

    else:

        # -------------------------------------------------
        # Get candidate indices
        # -------------------------------------------------

        candidate_indices = (
            candidates.index.tolist()
        )


        # -------------------------------------------------
        # Get candidate embeddings
        # -------------------------------------------------

        candidate_embeddings = (
            document_embeddings[
                candidate_indices
            ]
        )


        # -------------------------------------------------
        # Calculate similarity
        # -------------------------------------------------

        similarities = util.cos_sim(
            query_embedding,
            candidate_embeddings
        )[0]


        # -------------------------------------------------
        # Don't retrieve more than available
        # -------------------------------------------------

        k = min(
            top_k,
            len(candidates)
        )


        # -------------------------------------------------
        # Get top results
        # -------------------------------------------------

        top_results = similarities.argsort(
            descending=True
        )[:k]


        # -------------------------------------------------
        # Build results
        # -------------------------------------------------

        for result_index in top_results:

            position = result_index.item()

            original_index = (
                candidate_indices[position]
            )

            row = df.iloc[
                original_index
            ]


            results.append({

                "index":
                    original_index,

                "experience_id":
                    row["experience_id"],

                "experience_type":
                    row["experience_type"],

                "branch":
                    row["branch"],

                "company":
                    row["company"],

                "role":
                    row["role"],

                "similarity":
                    similarities[
                        position
                    ].item(),

                "document_text":
                    row["document_text"]
            })


    # =====================================================
    # Return everything
    # =====================================================

    return {

        "query":
            query,

        "matched_companies":
            matched_companies,

        "candidate_count":
            len(candidates),

        "results":
            results
    }


# =========================================================
# 12. Test
# =========================================================

if __name__ == "__main__":

    query = (
        "How should I prepare for BNY and "
        "Wells Fargo?"
    )


    result = search(
        query
    )


    print("\nQuestion:")

    print(
        result["query"]
    )


    print("\nDetected company:")

    print(
        result["matched_companies"]
    )


    print("\nCandidate documents:")

    print(
        result["candidate_count"]
    )


    print("\nResults:")

    print(
        "=" * 70
    )


    for item in result["results"]:

        print(
            "\nExperience:",
            item["experience_id"]
        )


        print(
            "Type:",
            item["experience_type"]
        )


        print(
            "Company:",
            item["company"]
        )


        print(
            "Branch:",
            item["branch"]
        )


        print(
            "Role:",
            item["role"]
        )


        print(
            "Similarity:",
            round(
                item["similarity"],
                4
            )
        )


        print(
            "\nRelevant experience:"
        )


        print(
            item["document_text"][:1000]
        )


        print(
            "-" * 70
        )