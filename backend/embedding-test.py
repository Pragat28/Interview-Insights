from sentence_transformers import SentenceTransformer

# Load a pretrained model
model = SentenceTransformer("all-MiniLM-L6-v2")

text = "I prepared DSA, DBMS and OOP for my technical interview."

# Convert text into an embedding
embedding = model.encode(text)

print("Embedding type:", type(embedding))
print("Number of dimensions:", len(embedding))
print("First 10 values:", embedding[:10])