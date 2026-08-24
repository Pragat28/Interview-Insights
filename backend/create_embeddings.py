import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer


# 1. Load our cleaned dataset
df = pd.read_csv(
    "../data/interview_insights_dataset (1).csv"
)

print("Loaded responses:", len(df))


# 2. Load the pretrained embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# 3. Take the text we want to make searchable
documents = (
    df["document_text"]
    .fillna("")
    .tolist()
)

print("Creating embeddings...")


# 4. Convert every document into a 384-dimensional vector
embeddings = model.encode(
    documents,
    show_progress_bar=True
)


# 5. Save the vectors
np.save(
    "../data/embeddings.npy",
    embeddings
)


print("\nDone!")
print("Embedding shape:", embeddings.shape)