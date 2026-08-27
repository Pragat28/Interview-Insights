from pathlib import Path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer


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

print(
    "Loaded responses:",
    len(df)
)


# =========================================================
# 3. Fields that we want individual embeddings for
# =========================================================

FIELDS = [

    "test_preparation",

    "important_topics",

    "resources",

    "selection_procedure",

    "test_description",

    "interview_experience",

    "eligibility",

    "projects",

    "compensation",

    "junior_advice",

    "last_minute_preparation"
]


# =========================================================
# 4. Verify fields exist
# =========================================================

missing_fields = [

    field

    for field in FIELDS

    if field not in df.columns
]


if missing_fields:

    raise ValueError(
        "The following fields are missing from the dataset: "
        + str(missing_fields)
    )


# =========================================================
# 5. Load embedding model
# =========================================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# =========================================================
# 6. Create field embeddings
#
# Shape:
#
#     number_of_rows
#     ×
#     number_of_fields
#     ×
#     embedding_dimension
#
# With your current dataset:
#
#     57 × 11 × 384
#
# =========================================================

all_field_embeddings = []


for field in FIELDS:

    print(
        f"Embedding field: {field}"
    )


    texts = (

        df[field]

        .fillna("")

        .astype(str)

        .tolist()
    )


    embeddings = model.encode(

        texts,

        convert_to_numpy=True,

        show_progress_bar=True
    )


    all_field_embeddings.append(
        embeddings
    )


# =========================================================
# 7. Stack embeddings
# =========================================================

field_embeddings = np.stack(
    all_field_embeddings,
    axis=1
)


# =========================================================
# 8. Save embeddings
# =========================================================

output_path = (
    DATA_DIR
    / "field_embeddings.npy"
)


np.save(
    output_path,
    field_embeddings
)


# =========================================================
# 9. Save field ordering
#
# This is important.
#
# field_embeddings[:, 0, :]
#     -> test_preparation
#
# field_embeddings[:, 1, :]
#     -> important_topics
#
# etc.
#
# =========================================================

fields_path = (
    DATA_DIR
    / "field_embedding_names.txt"
)


with open(
    fields_path,
    "w",
    encoding="utf-8"
) as file:

    for field in FIELDS:

        file.write(
            field + "\n"
        )


# =========================================================
# 10. Print verification
# =========================================================

print()
print("=" * 70)

print(
    "Field embeddings generated successfully."
)

print(
    "Shape:",
    field_embeddings.shape
)

print(
    "Saved to:",
    output_path
)

print(
    "Field names saved to:",
    fields_path
)

print("=" * 70)