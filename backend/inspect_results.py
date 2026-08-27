import pandas as pd

from search_embeddings import search


df = pd.read_csv(
    "../data/interview_insights_dataset (1).csv"
)


# =========================================================
# DSA
# =========================================================

print("\n")
print("=" * 80)
print("DSA QUERY")
print("=" * 80)

result = search(
    "What DSA topics should I study?"
)

for item in result["results"]:

    row = df.iloc[
        item["index"]
    ]

    print("\nCOMPANY:")
    print(
        row["company"]
    )

    print(
        "SCORE:",
        round(
            item["similarity"],
            3
        )
    )

    print(
        "\nIMPORTANT TOPICS:"
    )

    print(
        row["important_topics"]
    )

    print(
        "\n"
        + "-" * 60
    )


# =========================================================
# BNY PREPARATION
# =========================================================

print("\n")
print("=" * 80)
print("BNY PREPARATION")
print("=" * 80)

result = search(
    "How should I prepare for BNY?"
)

for item in result["results"]:

    row = df.iloc[
        item["index"]
    ]

    print("\nCOMPANY:")
    print(
        row["company"]
    )

    print(
        "SCORE:",
        round(
            item["similarity"],
            3
        )
    )

    print(
        "\nTEST PREPARATION:"
    )

    print(
        row["test_preparation"]
    )

    print(
        "\nIMPORTANT TOPICS:"
    )

    print(
        row["important_topics"]
    )

    print(
        "\nRESOURCES:"
    )

    print(
        row["resources"]
    )

    print(
        "\n"
        + "-" * 60
    )


# =========================================================
# BNY INTERVIEW
# =========================================================

print("\n")
print("=" * 80)
print("BNY INTERVIEW")
print("=" * 80)

result = search(
    "What questions were asked in BNY?"
)

for item in result["results"]:

    row = df.iloc[
        item["index"]
    ]

    print("\nCOMPANY:")
    print(
        row["company"]
    )

    print(
        "SCORE:",
        round(
            item["similarity"],
            3
        )
    )

    print(
        "\nINTERVIEW EXPERIENCE:"
    )

    print(
        row["interview_experience"]
    )

    print(
        "\nIMPORTANT TOPICS:"
    )

    print(
        row["important_topics"]
    )

    print(
        "\n"
        + "-" * 60
    )