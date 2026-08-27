import numpy as np

from pathlib import Path
from sentence_transformers import SentenceTransformer


# =========================================================
# 1. PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"


# =========================================================
# 2. INTENT DESCRIPTIONS
# =========================================================
#
# IMPORTANT:
#
# These descriptions define the semantic meaning of each
# intent for the embedding model.
#
# PREPARATION and ADVICE are deliberately separated.
#
# PREPARATION:
#   "How do I get ready?"
#
# ADVICE:
#   "What recommendation/guidance would you give me?"
#
# =========================================================

INTENT_DESCRIPTIONS = {

    "preparation":
        """
        Questions asking how to prepare or get ready for
        a company interview, placement, internship,
        online assessment, coding round, test, or hiring
        process.

        Includes questions about what to study, what to
        practice, what to focus on, and how to prepare.

        Examples:
        How should I prepare for BNY?
        What should I study for the interview?
        How can I get ready for the coding test?
        What should I practice before the OA?
        """,


    "selection":
        """
        Questions asking about the selection process,
        recruitment process, hiring stages, interview
        stages, rounds, or sequence of assessments.

        Examples:
        What is the selection process?
        How many rounds are there?
        What are the hiring stages?
        """,


    "test":
        """
        Questions asking about online assessments, coding
        tests, aptitude tests, online tests, OAs, test
        patterns, test experiences, or what happens during
        a company assessment.

        Examples:
        What was the online test like?
        What was the OA pattern?
        What type of coding test was given?
        """,


    "interview":
        """
        Questions asking about interview experiences,
        questions asked during interviews, technical
        interview questions, HR questions, technical
        rounds, or what candidates were asked.

        Examples:
        What questions were asked?
        What did they ask in the technical interview?
        What was the interview experience?
        """,


    "eligibility":
        """
        Questions asking who is eligible, eligibility
        criteria, CGPA requirements, academic criteria,
        branches, backlogs, or requirements for applying.

        Examples:
        What is the eligibility criteria?
        What CGPA is required?
        Which branches are eligible?
        """,


    "topics":
        """
        Questions asking specifically which technical
        subjects or topics should be studied.

        Includes DSA, DBMS, Operating Systems, Computer
        Networks, OOPs, programming topics, and other
        technical subjects.

        Examples:
        What DSA topics should I study?
        Which DBMS topics are important?
        What CS fundamentals should I prepare?
        """,


    "projects":
        """
        Questions asking about projects, project preparation,
        projects discussed in interviews, resume projects,
        or project-related questions.

        Examples:
        What projects were discussed?
        What project questions were asked?
        Which projects should I prepare?
        """,


    "compensation":
        """
        Questions asking about salary, stipend, compensation,
        package, CTC, pay, or financial benefits.

        Examples:
        What is the stipend?
        What package was offered?
        What was the CTC?
        """,


    "advice":
        """
        Questions explicitly asking for recommendations,
        tips, suggestions, guidance, or personal advice.

        This intent is about REQUESTING GUIDANCE.

        It is NOT simply a question containing the words
        "how", "should", or "prepare".

        A preparation question asks:
        How do I get ready?

        An advice question asks:
        What would you recommend?
        What advice would you give?
        Any tips for me?
        What suggestions do you have?

        Examples:
        What advice would you give juniors?
        Any tips for someone preparing for placements?
        What would you recommend to a fresher?
        Do you have any suggestions?
        """
}


# =========================================================
# 3. LOAD EMBEDDING MODEL
# =========================================================

print(
    "Loading embedding model..."
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# =========================================================
# 4. PREPARE DESCRIPTIONS
# =========================================================

intent_names = list(
    INTENT_DESCRIPTIONS.keys()
)


intent_texts = [

    INTENT_DESCRIPTIONS[intent]

    for intent in intent_names

]


# =========================================================
# 5. GENERATE EMBEDDINGS
# =========================================================

print(
    "Generating intent embeddings..."
)


embeddings = model.encode(

    intent_texts,

    convert_to_numpy=True,

    normalize_embeddings=True

)


# =========================================================
# 6. SAVE EMBEDDINGS
# =========================================================

embedding_path = (

    DATA_DIR
    / "intent_embeddings.npy"

)


np.save(

    embedding_path,

    embeddings

)


# =========================================================
# 7. SAVE INTENT NAMES
# =========================================================

names_path = (

    DATA_DIR
    / "intent_embedding_names.txt"

)


with open(

    names_path,

    "w",

    encoding="utf-8"

) as file:

    for intent in intent_names:

        file.write(

            intent + "\n"

        )


# =========================================================
# 8. DONE
# =========================================================

print()

print("=" * 60)

print(
    "Intent embeddings generated successfully."
)

print(
    "Shape:",
    embeddings.shape
)

print(
    "Saved to:",
    embedding_path
)

print(
    "Intent names saved to:",
    names_path
)

print("=" * 60)