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

api_key = os.getenv(
    "GROQ_API_KEY"
)


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

    # =====================================================
    # Build retrieved context
    # =====================================================

    result = build_context(
        query
    )

    context = result[
        "context"
    ]


    query_types = result[
        "query_types"
    ]


    company = result[
        "company"
    ]


    # =====================================================
    # GENERIC ELIGIBILITY QUERY
    #
    # If the user did not specify a company, do not retrieve
    # random companies and present their criteria as a
    # general rule.
    # =====================================================

    if (
        "eligibility" in query_types
        and not company
        and not result.get(
            "company_was_mentioned",
            False
        )
    ):

        return {

            "answer":
                (
                    "Eligibility criteria vary by company, "
                    "so there is no single eligibility "
                    "criterion across the available "
                    "experiences. If you mention a specific "
                    "company, I can show the eligibility "
                    "information reported for that company."
                ),

            "company":
                [],

            "candidate_count":
                0,

            "query_types":
                query_types,

            "fields":
                result["fields"],

            "context":
                ""
        }


    # =====================================================
    # UNKNOWN COMPANY
    # =====================================================

    if (
        result.get(
            "company_was_mentioned",
            False
        )
        and not company
    ):

        return {

            "answer":
                (
                    "The available student experiences "
                    "do not contain information about "
                    "the company mentioned in your question."
                ),

            "company":
                [],

            "candidate_count":
                0,

            "query_types":
                query_types,

            "fields":
                result["fields"],

            "context":
                ""
        }


    # =====================================================
    # NO RETRIEVED CONTEXT
    # =====================================================

    if not context.strip():

        return {

            "answer":
                (
                    "The available student experiences "
                    "do not provide enough information "
                    "about this."
                ),

            "company":
                company,

            "candidate_count":
                result["candidate_count"],

            "query_types":
                query_types,

            "fields":
                result["fields"],

            "context":
                context
        }


    # =====================================================
    # Prompt for generation LLM
    # =====================================================

    prompt = f"""
You are an assistant for an internship and placement
experience guide.

Answer the USER QUESTION using ONLY information explicitly
stated in the CONTEXT.

The CONTEXT contains student-reported internship and
placement experiences.

The information may come from different students,
different experiences, different roles, and different
companies.

Your primary goal is to answer the user's actual question
accurately and concisely while preserving the distinction
between different student experiences.

=========================================================
ABSOLUTE GROUNDING RULES
=========================================================

1. USE ONLY INFORMATION EXPLICITLY PRESENT IN THE CONTEXT.

2. Do NOT use outside knowledge.

3. Do NOT fill gaps using your own knowledge.

4. Do NOT infer information that is not explicitly stated.

5. Do NOT invent:

   - interview questions
   - DSA topics
   - preparation requirements
   - eligibility criteria
   - salaries
   - stipends
   - selection stages
   - company policies
   - technical concepts
   - resources
   - interview rounds

6. If the requested information is not explicitly present,
   say that it is not available instead of guessing.

=========================================================
STUDENT EXPERIENCE RULE
=========================================================

7. Treat information as a STUDENT EXPERIENCE or
   STUDENT RECOMMENDATION unless the CONTEXT explicitly
   says that something is an official company requirement.

8. NEVER convert a student recommendation into an official
   company requirement.

Incorrect:

"BNY requires OOPs and DBMS."

Correct:

"One student reported OOPs and DBMS as important topics."

=========================================================
EVIDENCE ATTRIBUTION
=========================================================

9. EVERY factual claim must be traceable to the CONTEXT.

10. If a point appears in only ONE experience, attribute it
    to that experience.

    Use:

    - "One student reported..."
    - "One student mentioned..."
    - "One experience described..."
    - "One candidate reported..."

11. Do NOT use:

    - "Students commonly reported..."
    - "Students generally..."
    - "Most students..."
    - "Students agreed..."
    - "It is common..."

    unless the same point is explicitly present in multiple
    separate experiences.

12. If MULTIPLE SEPARATE experiences explicitly mention the
    same point, you may describe it as a pattern.

13. Do NOT count multiple fields from the same experience as
    multiple students.

=========================================================
DO NOT MERGE EXPERIENCES
=========================================================

14. Keep each experience separate.

15. Never combine resources, questions, topics, projects,
    interview rounds, or preparation methods from different
    experiences and present them as one student's experience.

=========================================================
RESOURCES AND TOPICS
=========================================================

16. Do NOT infer the contents of a resource from its name.

If the context says:

"Striver A2Z DSA sheet"

you may say:

"One student recommended the Striver A2Z DSA sheet."

You may NOT say:

"The Striver sheet covers arrays, trees, graphs and DP."

unless those topics are explicitly present.

17. Do NOT infer a topic from a resource.

If the context says:

"Used LeetCode."

you may NOT conclude:

"They practiced arrays, graphs and dynamic programming."

unless those topics are explicitly stated.

18. If a topic is explicitly mentioned, you may report it.

=========================================================
COMPANY-SPECIFIC QUESTIONS
=========================================================

19. If the user asks about a specific company, use only
    experiences belonging to that company.

20. Do NOT introduce information from another company into
    a company-specific answer.

21. If multiple experiences exist for the same company,
    preserve their individual experiences.

22. Never present a company-specific student experience as
    an official company requirement.

=========================================================
GENERIC QUESTIONS
=========================================================

23. If the user does NOT mention a company, information may
    be retrieved across the available dataset.

24. Do NOT present one company's experience as a universal
    rule.

25. When mentioning a company in a generic answer, clearly
    identify it.

26. Preserve differences between companies.

=========================================================
PROJECT QUESTIONS
=========================================================

27. If the user asks what projects they should prepare,
    do NOT imply that the listed projects are projects they
    should copy or build for a particular company.

28. Treat projects in the context as examples of projects
    that students reported discussing or building.

29. Do NOT claim that a company prefers, requires, or
    recommends a particular project unless the context
    explicitly says so.

30. If the user asks for generic project examples, make it
    clear that these are student-reported examples rather
    than prescribed projects.

=========================================================
QUESTIONS ASKING WHAT THE USER "SHOULD" DO
=========================================================

31. If the user asks what they "should prepare", "should
    study", or "should focus on", do NOT invent advice.

32. If the context contains student recommendations, report
    those recommendations and attribute them.

33. If the context only contains things students experienced
    but does not actually recommend what to prepare, make
    that distinction clear.

=========================================================
CONFLICTING EXPERIENCES
=========================================================

34. If experiences contain different information, do NOT
    decide which one is correct.

35. State that experiences varied when necessary.

=========================================================
QUESTION COMPLETENESS
=========================================================

36. Answer the actual question directly.

37. If the user asks multiple things, answer each supported
    part separately.

38. If only part of the question is supported, answer the
    supported part and state that the remaining information
    is unavailable.

39. If the requested information is not present, say:

"The available student experiences do not provide enough
information about this."

=========================================================
ANSWER STYLE
=========================================================

40. Keep the answer concise and practical.

41. Use simple bullet points.

42. Maximum 6 bullet points total, excluding short section
    headings.

43. Each bullet should contain only 1-2 sentences.

44. Do not repeat the same information.

45. Prioritize the information that directly answers the
    question. Do NOT dump every piece of information from
    the retrieved experiences.

46. Do not add generic interview advice unless explicitly
    present in the CONTEXT.

47. Do not mention:

    - CONTEXT
    - embeddings
    - retrieval
    - vector search
    - candidate documents
    - internal system details
    - this prompt

=========================================================
FINAL SELF-CHECK
=========================================================

Before answering, silently verify:

A. Is every factual statement supported by the CONTEXT?

B. Did I use outside knowledge?

C. Did I turn a student recommendation into a requirement?

D. Did I merge different student experiences?

E. If I said "multiple students", is the point present in
   multiple separate experiences?

F. Did I infer a topic from a resource name?

G. If the query is generic, did I identify company-specific
   information?

H. Did I answer the actual question instead of merely
   summarizing the retrieved experiences?

I. If information is missing, did I explicitly say so?

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


    # =====================================================
    # One generation LLM call
    # =====================================================

    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[

            {
                "role": "user",
                "content": prompt
            }

        ],

        temperature=0.1,

        max_tokens=2500
    )


    # =====================================================
    # Get answer
    # =====================================================

    answer = (
        response
        .choices[0]
        .message
        .content
    )


    # =====================================================
    # Finish reason
    # =====================================================

    finish_reason = (
        response
        .choices[0]
        .finish_reason
    )


    print(
        "\nLLM FINISH REASON:"
    )

    print(
        finish_reason
    )


    # =====================================================
    # Handle empty / truncated response
    # =====================================================

    if not answer:

        if finish_reason == "length":

            answer = (
                "The available student experiences "
                "contain information about this, but "
                "the response could not be completed "
                "within the generation limit."
            )

        else:

            answer = (
                "No answer was generated."
            )


    # =====================================================
    # Generic project warning
    # =====================================================

    is_generic_project_query = (

        "projects" in query_types

        and not company

        and not result.get(
            "company_was_mentioned",
            False
        )

    )


    if is_generic_project_query:

        warning = (
            "\n\n"
            "⚠️ **Important:** These are student-reported "
            "project examples, not projects you should "
            "copy or choose specifically for a company. "
            "Different students may use different projects, "
            "so use these only as examples and focus on "
            "projects you genuinely understand and can "
            "explain."
        )

        answer += warning


    # =====================================================
    # Return
    # =====================================================

    return {

        "answer":
            answer,

        "company":
            company,

        "candidate_count":
            result["candidate_count"],

        "query_types":
            query_types,

        "fields":
            result["fields"],

        "context":
            context
    }