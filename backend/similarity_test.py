from sentence_transformers import SentenceTransformer, util

# Load our pretrained embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "I prepared DSA and DBMS for my technical interview.",
    "I practiced data structures and database concepts before my technical round.",
    "The company provided accommodation and transportation."
]

# Convert all three sentences into embeddings
embeddings = model.encode(sentences, convert_to_tensor=True)

# Compare sentence A with B
similarity_ab = util.cos_sim(embeddings[0], embeddings[1])

# Compare sentence A with C
similarity_ac = util.cos_sim(embeddings[0], embeddings[2])

print("Similarity A ↔ B:", similarity_ab.item())
print("Similarity A ↔ C:", similarity_ac.item())