# Interview Insights

> Learn from the students who went through it before you.

Interview Insights is a RAG-based system that helps students explore real
internship and placement experiences shared by other students.

Instead of searching through dozens of interview reports manually, ask a
question in natural language and get an answer based on the most relevant
experiences in the dataset.

---

## What can you ask?

- **Preparation** — How should I prepare for BNY?
- **Interview Questions** — What questions were asked in technical interviews?
- **Selection Process** — What were the selection rounds?
- **Online Tests** — What was the coding test like?
- **Technical Topics** — What DSA / DBMS / OS / OOPS topics were asked?
- **Projects** — What projects were discussed?
- **Eligibility** — What CGPA or academic criteria were required?
- **Compensation** — What stipend or package was offered?
- **Advice** — What advice did students have for juniors?

Multiple intents can also be handled in a single query.

---

## How it works

The system follows a retrieval-augmented generation pipeline:

```text
User Question
      |
      v
Intent Detection
      |
      v
Company Detection
      |
      v
Relevant Field Selection
      |
      v
Semantic Retrieval
      |
      v
Context Building
      |
      v
Answer Generation
