from context_builder import build_context


# =========================================================
# Test query
# =========================================================

query = "What projects should I explain for BNY and what questions were asked?"

# =========================================================
# Build context
# =========================================================

result = build_context(query)


# =========================================================
# Display everything
# =========================================================

print("\nQUESTION")
print("=" * 70)

print(result["query"])


print("\nCOMPANY")
print("=" * 70)

print(result["company"])


print("\nCANDIDATE DOCUMENTS")
print("=" * 70)

print(result["candidate_count"])


print("\nQUERY TYPES")
print("=" * 70)

print(result["query_types"])


print("\nFIELDS SELECTED")
print("=" * 70)

for field in result["fields"]:

    print(field)


print("\nCONTEXT THAT WILL EVENTUALLY GO TO THE LLM")
print("=" * 70)

print(result["context"])
print("\nCONTEXT SIZE")
print("=" * 70)

word_count = len(result["context"].split())

print("Approximate word count:", word_count)