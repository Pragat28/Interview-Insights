import os

from dotenv import load_dotenv
from groq import Groq

from context_builder import build_context


# =========================================================
# 1. Load environment variables
# =========================================================

load_dotenv()


# =========================================================
# 2. Get API key
# =========================================================

api_key = os.getenv("GROQ_API_KEY")

if not api_key:

    raise ValueError(
        "GROQ_API_KEY not found. "
        "Please add it to your .env file."
    )


# =========================================================
# 3. Create Groq client
# =========================================================

client = Groq(
    api_key=api_key
)


# =========================================================
# 4. Generate answer
# =========================================================

def generate_answer(query):

    # -----------------------------------------------------
    # Build retrieved context
    # -----------------------------------------------------

    result = build_context(query)

    context = result["context"]


    # -----------------------------------------------------
    # Prompt for the LLM
    # -----------------------------------------------------

    prompt = f"""
You are an assistant for an internship and placement
experience guide.

Your job is to answer the USER QUESTION using ONLY the
information explicitly stated in the CONTEXT.

The CONTEXT contains experiences and recommendations
reported by previous students.

=========================================================
STRICT GROUNDING RULES
=========================================================

1. Use ONLY information explicitly present in the CONTEXT.

2. Do NOT use outside knowledge.

3. Do NOT infer, expand, explain, or complete information
   using your own knowledge.

4. Do NOT infer DSA topics from the name of a resource.

   Example:
   If the context says:
   "Striver A2Z DSA sheet"

   You may say:
   "A student recommended the Striver A2Z DSA sheet."

   You may NOT say:
   "The Striver sheet covers arrays, trees, graphs,
   dynamic programming, etc."

   unless those topics are explicitly present in the
   CONTEXT.

5. Treat every statement as a STUDENT EXPERIENCE or
   STUDENT RECOMMENDATION unless the CONTEXT explicitly
   states that it is an official company requirement.

6. NEVER turn a student's recommendation into an official
   company requirement.

   Incorrect:
   "BNY requires OOPs and DBMS."

   Correct:
   "Students reported OOPs and DBMS as important topics."

7. VERY IMPORTANT:
   Do NOT merge information from different students into
   one student's experience.

   For example, if:

   Student A:
   "I was asked almost every concept of OOPs."

   Student B:
   "A medium-level DSA array question was asked."

   Do NOT write:
   "One student was asked OOPs and a medium-level DSA
   array question."

   Instead write:
   "One student reported being asked almost every concept
   of OOPs. Another student reported a medium-level DSA
   question on arrays."

8. If only ONE student mentions something, explicitly
   attribute it to one student.

   Use:
   - "One student mentioned..."
   - "One student reported..."
   - "One experience described..."

9. If MULTIPLE students mention the same point, you may
   summarize it as a common observation.

   Use:
   - "Multiple students mentioned..."
   - "Students commonly reported..."
   - "Several experiences highlighted..."

10. If students give different experiences, do NOT choose
    one as the correct version.

    Instead explain that experiences varied.

11. Do NOT invent:
    - interview questions
    - DSA topics
    - eligibility criteria
    - salaries
    - preparation requirements
    - company policies
    - selection stages
    - technical concepts

12. If the requested information is NOT present in the
    CONTEXT, explicitly say:

    "The available student experiences do not provide
    enough information about this."

13. If only part of the user's question can be answered,
    answer the part supported by the CONTEXT and clearly
    state that the remaining information is unavailable.

=========================================================
ANSWER STRUCTURE
=========================================================

14. Answer the actual question directly.

15. For compound questions containing multiple intents,
    answer each part separately when useful.

    Example:

    User:
    "What projects should I explain and what questions
    were asked?"

    Good structure:

    Projects:
    - ...

    Interview experience:
    - ...

16. For questions involving multiple companies, keep
    information separated by company.

    Example:

    BNY Mellon:
    - ...

    Wells Fargo:
    - ...

17. Do NOT mix experiences from different companies.

18. Use simple bullet points.

19. Maximum 6 bullet points in total, excluding short
    section headings.

20. Each bullet should contain only 1-2 sentences.

21. Keep the answer concise and practical.

22. Do not repeat the same information in multiple bullets.

23. Do not mention the CONTEXT, retrieval process,
    embeddings, or internal system details.

=========================================================
USER QUESTION
=========================================================

{query}

=========================================================
CONTEXT
=========================================================

{context}

=========================================================
FINAL ANSWER
=========================================================
"""


    # -----------------------------------------------------
    # One LLM call
    # -----------------------------------------------------

    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2,

        max_tokens=1500
    )


    # -----------------------------------------------------
    # Get generated answer
    # -----------------------------------------------------

    answer = response.choices[0].message.content


    # -----------------------------------------------------
    # Debug information
    # -----------------------------------------------------

    print("\nLLM FINISH REASON:")
    print(
        response.choices[0].finish_reason
    )


    # -----------------------------------------------------
    # Return answer + retrieval information
    # -----------------------------------------------------

    return {

        "answer":
            answer
            if answer
            else "No answer was generated.",

        "company":
            result["company"],

        "candidate_count":
            result["candidate_count"],

        "query_types":
            result["query_types"],

        "fields":
            result["fields"],

        "context":
            context
    }