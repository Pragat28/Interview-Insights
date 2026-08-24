import pandas as pd


# Load dataset
df = pd.read_csv(
    "../data/interview_insights_dataset (1).csv"
)


print(
    "Total responses:",
    len(df)
)


def search(keyword):

    results = df[
        df["document_text"]
        .str.contains(
            keyword,
            case=False,
            na=False
        )
    ]


    print(
        f"\nResults for: '{keyword}'"
    )

    print("=" * 60)


    for _, row in results.head(5).iterrows():

        print(
            f"\nExperience: "
            f"{row['experience_id']}"
        )

        print(
            f"Type: "
            f"{row['experience_type']}"
        )

        print(
            f"Company: "
            f"{row['company']}"
        )

        print(
            f"Branch: "
            f"{row['branch']}"
        )

        print(
            f"Role: "
            f"{row['role']}"
        )


        print("\nImportant Topics:")

        print(
            row["important_topics"]
            if pd.notna(row["important_topics"])
            else "Not provided"
        )


        print("\nInterview Experience:")

        print(
            row["interview_experience"]
            if pd.notna(
                row["interview_experience"]
            )
            else "Not provided"
        )


        print("-" * 60)


# Test
search("DSA")