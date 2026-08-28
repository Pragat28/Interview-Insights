import os
import re
import json
from pathlib import Path

import pandas as pd
import numpy as np
import spacy

from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer, util


# =========================================================
# 1. PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"


# =========================================================
# 2. ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found. Please add it to your .env file."
    )

groq_client = Groq(api_key=api_key)


# =========================================================
# 3. LOAD DATASET
# =========================================================

df = pd.read_csv(DATA_DIR / "interview_insights_dataset (1).csv")
print("Loaded responses:", len(df))


# =========================================================
# 4. LOAD FIELD EMBEDDINGS
# =========================================================

field_embeddings = np.load(DATA_DIR / "field_embeddings.npy")

FIELDS_PATH = DATA_DIR / "field_embedding_names.txt"

with open(FIELDS_PATH, "r", encoding="utf-8") as file:
    EMBEDDING_FIELDS = [line.strip() for line in file if line.strip()]


# =========================================================
# 5. VALIDATE FIELD EMBEDDINGS
# =========================================================

if field_embeddings.ndim != 3:
    raise ValueError("field_embeddings.npy must have shape (documents, fields, dimensions).")

if field_embeddings.shape[0] != len(df):
    raise ValueError("Number of embedding documents does not match dataset rows.")

if field_embeddings.shape[1] != len(EMBEDDING_FIELDS):
    raise ValueError("Number of embedding fields does not match field_embedding_names.txt.")

print("Loaded field embeddings:", field_embeddings.shape)
print("Embedding fields:", EMBEDDING_FIELDS)


# =========================================================
# 6. LOAD SENTENCE TRANSFORMER
# =========================================================

model = SentenceTransformer("all-MiniLM-L6-v2")


# =========================================================
# 7. LOAD SPACY
# =========================================================

nlp = spacy.load("en_core_web_sm")


# =========================================================
# 8. LOAD INTENT EMBEDDINGS
# =========================================================

INTENT_EMBEDDINGS_PATH = DATA_DIR / "intent_embeddings.npy"
INTENT_NAMES_PATH = DATA_DIR / "intent_embedding_names.txt"

intent_embeddings = np.load(INTENT_EMBEDDINGS_PATH)

with open(INTENT_NAMES_PATH, "r", encoding="utf-8") as file:
    INTENT_NAMES = [line.strip() for line in file if line.strip()]


# =========================================================
# 9. VALIDATE INTENT EMBEDDINGS
# =========================================================

if intent_embeddings.ndim != 2:
    raise ValueError("intent_embeddings.npy must have shape (intents, dimensions).")

if intent_embeddings.shape[0] != len(INTENT_NAMES):
    raise ValueError("Number of intent embeddings does not match intent_embedding_names.txt.")

print("Loaded intent embeddings:", intent_embeddings.shape)
print("Intent names:", INTENT_NAMES)


# =========================================================
# 10. RETRIEVAL CONFIGURATION
# =========================================================

COMPANY_TOP_K = 2
GENERIC_TOP_K = 8
INTENT_TOP_K = 3


# =========================================================
# 11. QUERY TYPE -> DATASET FIELDS
# =========================================================

QUERY_FIELDS = {
    "preparation": ["test_preparation", "important_topics", "resources"],
    "selection": ["selection_procedure"],
    "test": ["test_description", "test_preparation"],
    "interview": ["interview_experience", "important_topics"],
    "eligibility": ["eligibility"],
    "topics": ["important_topics"],
    "projects": ["projects", "interview_experience"],
    "compensation": ["compensation"],
    "advice": ["junior_advice", "last_minute_preparation"],
}


# =========================================================
# 12. COMPANIES IN DATASET
# =========================================================

companies = (
    df["company"]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
    .tolist()
)

companies = sorted(companies, key=len, reverse=True)


# =========================================================
# 13. COMPANY ALIASES
# =========================================================
#
# NOTE: "db" (Deutsche Bank) and "ti" (Texas Instruments)
# were removed. Nobody actually queries using those short
# forms, and they collided with common technical terms
# ("db" = database, "ti" = various technical abbreviations),
# causing false-positive company detection. Full names and
# the other unambiguous aliases below still work fine.
# =========================================================

COMPANY_ALIASES = {
    "bny": "BNY Mellon",
    "bny mellon": "BNY Mellon",
    "wells": "Wells Fargo",
    "wells fargo": "Wells Fargo",
    "deutsche": "Deutsche Bank",
    "deutsche bank": "Deutsche Bank",
    "hpcl": "Hindustan Petroleum Corporation Limited (HPCL)",
    "bpcl": "Bharat Petroleum Corporation Limited",
    "jpmc": "JP Morgan Chase",
    "jp morgan": "JP Morgan Chase",
    "jpmorgan": "JP Morgan Chase",
    "qualcomm": "Qualcomm India Private Ltd.",
    "cisco": "Cisco",
    "nvidia": "Nvidia",
    "amazon": "Amazon",
    "accenture": "Accenture",
}


# =========================================================
# 14. NORMALIZE TEXT
# =========================================================

def normalize_text(text):
    text = str(text).lower()
    text = re.sub(r"'s\b", "", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# =========================================================
# 15. PHRASE MATCHING
# =========================================================

def phrase_in_text(phrase, text):
    normalized_phrase = normalize_text(phrase)
    normalized_text = normalize_text(text)
    pattern = r"\b" + re.escape(normalized_phrase) + r"\b"
    return bool(re.search(pattern, normalized_text))


# =========================================================
# 16. EXPLICIT INTENT DETECTION
# =========================================================

EXPLICIT_INTENT_PHRASES = {
    "preparation": [
        "how should i prepare", "how do i prepare", "how to prepare",
        "how can i prepare", "prepare for", "preparation for",
        "how should i study", "what should i study", "how can i study",
        "what should i practice", "how should i practice",
        "what should i focus on", "how to get ready", "get ready for",
        "prepare",
    ],
    "interview": [
        "interview questions", "questions asked", "what questions were asked",
        "what questions was asked", "what questions were asked in",
        "what questions was asked in", "what was asked", "what were asked",
        "which questions were asked", "which questions was asked",
        "technical interview", "technical round", "technical questions",
        "interview experience", "interview round", "interview rounds",
        "hr interview", "hr round", "hr questions", "interview",
    ],
    "selection": [
        "selection process", "selection procedure", "selection stages",
        "selection rounds", "hiring process", "recruitment process",
        "what are the rounds", "what were the rounds", "how many rounds",
        "rounds in the selection",
    ],
    "test": [
        "online assessment", "online test", "coding test", "coding assessment",
        "assessment test", "online coding", "oa", "test pattern",
        "test experience", "what was the test", "what was the online assessment",
        "assessment",
    ],
    "eligibility": [
        "eligibility", "eligible", "eligibility criteria",
        "eligibility requirement", "eligibility requirements",
        "cgpa requirement", "cgpa criteria", "academic criteria",
        "academic eligibility",
    ],
    "topics": [
        "what topics", "which topics", "important topics", "topics asked",
        "subjects asked", "what subjects", "which subjects", "dsa topics",
        "dbms topics", "oops topics", "os topics", "cn topics",
        "data structures", "operating systems", "computer networks",
    ],
    "projects": [
        "what projects", "which projects", "projects asked",
        "project questions", "project discussion", "what project",
        "which project", "projects",
    ],
    "compensation": ["salary", "stipend", "compensation", "package", "ctc", "pay"],
    "advice": [
        "give me advice", "need advice", "any advice", "what advice",
        "what advice would you give", "advice for juniors",
        "advice for freshers", "advice for students", "tips", "give me tips",
        "any tips", "what tips", "tips for juniors", "tips for freshers",
        "suggestions", "give me suggestions", "any suggestions",
        "what would you recommend", "what do you recommend",
        "recommendations", "last minute advice", "last minute tips",
        "last minute preparation",
    ],
}


def detect_explicit_intents(query):
    detected = []
    normalized_query = normalize_text(query)

    for intent, phrases in EXPLICIT_INTENT_PHRASES.items():
        for phrase in phrases:
            if phrase_in_text(phrase, normalized_query):
                detected.append(intent)
                break

    return list(dict.fromkeys(detected))


# =========================================================
# 16B. AUTO-GENERATED "CORE NAME" MATCHING
#
# Many company names in the dataset carry a parenthetical
# short form (e.g. "Texas Instruments (TI)") or a trailing
# legal-entity suffix (e.g. "Qualcomm India Private Ltd.").
# detect_company() previously required the FULL company
# string to appear literally inside the user's query — so a
# user typing just "Texas Instruments" never matched
# "Texas Instruments (TI)", because the extra "(TI)" token
# broke the exact substring check.
#
# Rather than patch this one company with a manual alias
# (which only fixes Texas Instruments and leaves every other
# similarly-formatted company broken), we derive a "core
# name" for every company by stripping parenthetical text
# and trailing legal-entity words, and match against that
# too. This fixes the whole class of bug automatically, for
# current and future companies in the dataset.
# =========================================================

LEGAL_SUFFIX_WORDS = {
    "india", "private", "pvt", "ltd", "limited", "corporation",
    "corp", "inc", "llc", "co", "plc",
}


def strip_parenthetical(text):
    return re.sub(r"\(.*?\)", "", str(text))


def build_core_name(company):
    text = strip_parenthetical(company)
    text = normalize_text(text)
    words = text.split()

    while words and words[-1] in LEGAL_SUFFIX_WORDS:
        words.pop()

    return " ".join(words)


CORE_NAME_TO_COMPANY = {}

for _company in companies:
    _core_name = build_core_name(_company)
    if _core_name and _core_name not in CORE_NAME_TO_COMPANY:
        CORE_NAME_TO_COMPANY[_core_name] = _company


# =========================================================
# 16C. DISTINCTIVE FIRST-WORD MATCHING
#
# Users often drop words entirely, not just suffixes — e.g.
# typing "texas" instead of "Texas Instruments", or "jindal"
# instead of "Jindal Stainless Ltd". The core-name fix above
# only handles trimmed *endings*; it still requires the full
# remaining phrase to appear in the query.
#
# Here we index the first word of every core name, and treat
# it as a safe standalone match ONLY when that word is long
# enough (>=4 chars, to avoid short generic words) AND unique
# across the dataset (exactly one company starts with it, to
# avoid ambiguity). A few words are excluded even when unique
# because they collide with common domain terminology — e.g.
# "Turing" the company vs. "Turing machine" / "Turing test",
# which come up constantly in CS interview questions.
# =========================================================

FIRST_WORD_BLACKLIST = {
    "turing",  # collides with "Turing machine" / "Turing test" (CS topics)
}

FIRST_WORD_TO_COMPANIES = {}

for _core_name, _company in CORE_NAME_TO_COMPANY.items():
    _words = _core_name.split()
    if not _words:
        continue
    _first_word = _words[0]
    if len(_first_word) < 5:
        continue
    if _first_word in FIRST_WORD_BLACKLIST:
        continue
    FIRST_WORD_TO_COMPANIES.setdefault(_first_word, []).append(_company)


def match_distinctive_first_word(normalized_query):
    query_words = set(normalized_query.split())
    matched = []

    for first_word, matching_companies in FIRST_WORD_TO_COMPANIES.items():
        if len(matching_companies) == 1 and first_word in query_words:
            matched.append(matching_companies[0])

    return matched


# =========================================================
# 17. DETECT COMPANY
# =========================================================

def detect_company(query):
    normalized_query = normalize_text(query)
    matches = []

    # Dataset companies
    for company in companies:
        if phrase_in_text(company, normalized_query):
            matches.append(company)

    # Core names (handles names like "Texas Instruments (TI)")
    for core_name, company in CORE_NAME_TO_COMPANY.items():
        if phrase_in_text(core_name, normalized_query):
            matches.append(company)

    # Distinctive first-word matches (e.g. "texas" -> "Texas Instruments")
    matches.extend(match_distinctive_first_word(normalized_query))

    # spaCy proper nouns
    doc = nlp(query)
    proper_nouns = []

    for token in doc:
        if token.pos_ == "PROPN":
            noun = normalize_text(token.text)
            if noun:
                proper_nouns.append(noun)

    proper_nouns = list(dict.fromkeys(proper_nouns))

    # Single-word aliases
    for noun in proper_nouns:
        if noun in COMPANY_ALIASES:
            company = COMPANY_ALIASES[noun]
            if company in companies:
                matches.append(company)

    # Multi-word aliases
    for alias, company in COMPANY_ALIASES.items():
        if phrase_in_text(alias, normalized_query):
            if company in companies:
                matches.append(company)

    return list(dict.fromkeys(matches))


# =========================================================
# 18. DETECT WHETHER COMPANY WAS MENTIONED
# =========================================================

# Common technical/domain terms that spaCy sometimes mis-tags
# as PROPN. These must never be treated as a company signal, or
# generic technical queries silently return zero candidates.
NON_COMPANY_PROPN_BLACKLIST = {
    "dsa", "db", "dbms", "ti", "oops", "oop", "os", "cn", "sql",
    "java", "python", "cpp", "c", "html", "css", "js", "javascript",
    "hr", "oa", "cgpa", "ctc", "api", "aws", "sde", "ml", "ai", "dl",
    "nlp",
}


def detect_mentioned_company(query):
    normalized_query = normalize_text(query)

    # Dataset companies
    for company in companies:
        if phrase_in_text(company, normalized_query):
            return True

    # Core names (handles names like "Texas Instruments (TI)")
    for core_name in CORE_NAME_TO_COMPANY:
        if phrase_in_text(core_name, normalized_query):
            return True

    # Distinctive first-word matches (e.g. "texas" -> "Texas Instruments")
    if match_distinctive_first_word(normalized_query):
        return True

    # Aliases
    for alias in COMPANY_ALIASES:
        if phrase_in_text(alias, normalized_query):
            return True

    # Proper nouns (fallback for unrecognized company names)
    doc = nlp(query)
    proper_nouns = []

    for token in doc:
        if token.pos_ == "PROPN":
            noun = normalize_text(token.text)
            if noun:
                proper_nouns.append(noun)

    proper_nouns = list(dict.fromkeys(proper_nouns))

    company_question_words = [
        "prepare", "preparation", "interview", "technical", "selection",
        "test", "assessment", "oa", "stipend", "salary", "package",
        "eligibility", "questions", "round", "rounds", "hiring",
        "placement", "internship",
    ]

    query_words = normalized_query.split()

    has_company_context = any(word in query_words for word in company_question_words)

    if has_company_context:
        for noun in proper_nouns:
            if noun in {"i", "what", "how", "why", "when", "where", "which"}:
                continue
            if noun in NON_COMPANY_PROPN_BLACKLIST:
                continue
            return True

    return False


# =========================================================
# 19. GET TOP INTENT CANDIDATES
# =========================================================

def get_top_intent_candidates(query):
    query_embedding = model.encode(query, convert_to_tensor=True)
    similarities = util.cos_sim(query_embedding, intent_embeddings)[0]

    scored_intents = []
    for index, score in enumerate(similarities):
        scored_intents.append({
            "intent": INTENT_NAMES[index],
            "similarity": float(score.item()),
        })

    scored_intents.sort(key=lambda x: x["similarity"], reverse=True)
    return scored_intents[:INTENT_TOP_K]


# =========================================================
# 20. LLM INTENT RESOLVER
# =========================================================

def resolve_query_intents(query, intent_candidates):

    explicit_intents = detect_explicit_intents(query)
    print("\nEXPLICIT INTENTS:")
    print(explicit_intents)

    if intent_candidates:
        candidate_text = "\n".join(
            f"{index + 1}. {item['intent']} (similarity={item['similarity']:.4f})"
            for index, item in enumerate(intent_candidates)
        )
    else:
        candidate_text = "None"

    all_intents_text = ", ".join(INTENT_NAMES)

    prompt = f"""
You are the intent classifier for an internship and placement
experience search system.

USER QUERY:
{query}

SEMANTIC HINTS FROM THE EMBEDDING MODEL:
{candidate_text}

AVAILABLE INTENTS:
{all_intents_text}

TASK:
Determine EVERY intent that is directly represented in the user's query.
A query may contain multiple independent intents.
Classify using the meaning and context of the complete query, not merely
individual words.
The semantic hints are ONLY hints. You are allowed to select ANY intent
from the available intents, even if that intent does not appear in the
semantic hints.

============================================================
INTENT DEFINITIONS
============================================================

PREPARATION:
The user wants to know how to prepare, what to study, what to practice,
what to focus on, or how to get ready.
Examples:
"How should I prepare for BNY?" -> preparation
"What should I study for BNY?" -> preparation
"How can I get ready for the interview?" -> preparation
"What should I practice before the OA?" -> preparation

ADVICE:
The user explicitly asks for advice, tips, suggestions, recommendations,
guidance, or last-minute guidance.
Examples:
"What advice would you give juniors?" -> advice
"Any tips for someone preparing for BNY?" -> advice
"What would you recommend to a fresher?" -> advice
"Do you have any advice for someone applying?" -> advice

============================================================
CRITICAL PREPARATION VS ADVICE DISTINCTION
============================================================

Words such as "how", "should", "prepare", "what" DO NOT automatically
imply advice.

"How should I prepare for BNY?" -> preparation, NOT advice

"How should I prepare for BNY and what questions were asked?"
-> preparation, interview, NOT preparation, advice, interview

However, when the user explicitly requests advice/tips/recommendations,
classify it as advice.

"Any tips for someone preparing for BNY?" -> advice
"What advice would you give someone preparing for BNY?" -> advice

============================================================
INTERVIEW
============================================================
Questions about interviews, interview experiences, interview questions,
technical interview questions, HR questions, technical rounds, or what
was asked during an interview.
"What questions were asked in BNY?" -> interview
"What was asked during the interview?" -> interview
"What technical questions were asked?" -> interview
"What was the interview experience?" -> interview

A query can contain both interview and another intent:
"What projects were discussed during the interview?" -> projects, interview

============================================================
SELECTION
============================================================
Questions about the hiring process, selection process, recruitment
process, selection stages, hiring rounds, or recruitment sequence.
"What is the selection process?" -> selection
"How many rounds were there?" -> selection
"What were the hiring stages?" -> selection

============================================================
TEST
============================================================
Questions about online assessments, coding tests, aptitude tests, OAs,
online tests, test patterns, test formats, or test experiences.
"What was the online test like?" -> test
"What was the OA pattern?" -> test
"What coding assessment did they have?" -> test

============================================================
TOPICS
============================================================
Questions specifically asking about technical subjects, technical
topics, DSA topics, DBMS, OS, OOPs, Computer Networks, algorithms, or
other subjects to study.
"What DSA topics should I study?" -> topics
"Which DBMS topics are important?" -> topics
"What CS subjects were asked?" -> topics

============================================================
PROJECTS
============================================================
Questions about projects, project discussions, project questions,
resume projects, or projects discussed during interviews.
"What projects were discussed?" -> projects
"What project questions were asked?" -> projects
"What projects did they discuss during the interview?" -> projects, interview

============================================================
ELIGIBILITY
============================================================
Questions about eligibility, CGPA, branches, backlogs, academic
requirements, or who can apply.
"What CGPA is required?" -> eligibility
"Which branches are eligible?" -> eligibility
"Who can apply?" -> eligibility

============================================================
COMPENSATION
============================================================
Questions about salary, stipend, CTC, package, pay, or compensation.
"What stipend did they offer?" -> compensation
"What was the CTC?" -> compensation
"What salary was offered?" -> compensation

============================================================
IMPORTANT RULES
============================================================
1. Return EVERY directly relevant intent.
2. Do NOT return vaguely related intents.
3. Do NOT create new intents.
4. Do NOT classify "advice" merely because the query contains "how",
   "should", "prepare", or "what".
5. Explicit requests for tips, advice, recommendations, or suggestions
   should be classified as advice.
6. The semantic hints are NOT a restriction.
7. You may select an intent that is absent from the semantic hints if
   the query clearly expresses it.
8. Every returned intent must be one of the available intents.
9. If no intent is clearly applicable, return an empty list.
10. Return the result using the required JSON structure.
"""

    llm_intents = []

    try:
        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a strict intent classifier. "
                        "Classify the user's query using only the provided intents. "
                        "Return only the required JSON object."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            reasoning_effort="low",
            include_reasoning=False,
            max_completion_tokens=150,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "intent_classification",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "intents": {
                                "type": "array",
                                "items": {"type": "string", "enum": INTENT_NAMES},
                            }
                        },
                        "required": ["intents"],
                        "additionalProperties": False,
                    },
                },
            },
        )

        raw_answer = (response.choices[0].message.content or "{}").strip()

        print("\nINTENT RESOLVER RAW OUTPUT:")
        print(repr(raw_answer))
        print("INTENT RESOLVER FINISH REASON:")
        print(response.choices[0].finish_reason)

        parsed_response = json.loads(raw_answer)
        returned_intents = parsed_response.get("intents", [])

        if not isinstance(returned_intents, list):
            returned_intents = []

        for intent in returned_intents:
            if (
                isinstance(intent, str)
                and intent in INTENT_NAMES
                and intent not in llm_intents
            ):
                llm_intents.append(intent)

    except Exception as error:
        print("Intent resolver warning:", error)
        llm_intents = []

    final_intents = []

    for intent in llm_intents:
        if intent not in final_intents:
            final_intents.append(intent)

    for intent in explicit_intents:
        if intent not in final_intents:
            final_intents.append(intent)

    if not final_intents:
        if explicit_intents:
            final_intents = list(explicit_intents)
        elif intent_candidates:
            final_intents = [intent_candidates[0]["intent"]]
        else:
            final_intents = []

    print("LLM INTENTS:", llm_intents)
    print("FINAL INTENTS:", final_intents)

    return final_intents


# =========================================================
# 21. DETECT QUERY TYPES
# =========================================================

def detect_query_types(query):
    candidates = get_top_intent_candidates(query)
    return resolve_query_intents(query, candidates)


# =========================================================
# 22. RELEVANT FIELDS FROM INTENTS
# =========================================================

def get_relevant_fields_from_intents(query_types):
    fields = []

    for query_type in query_types:
        if query_type not in QUERY_FIELDS:
            continue
        for field in QUERY_FIELDS[query_type]:
            if field not in fields:
                fields.append(field)

    if not fields:
        fields = [
            "selection_procedure",
            "test_description",
            "test_preparation",
            "interview_experience",
            "important_topics",
        ]

    return fields


# =========================================================
# 23. GET CANDIDATE DOCUMENTS
# =========================================================

def get_candidates(query):
    matched_companies = detect_company(query)
    company_was_mentioned = detect_mentioned_company(query)

    if not company_was_mentioned:
        return df, matched_companies, False

    if not matched_companies:
        return df.iloc[0:0], [], True

    candidates = df[df["company"].isin(matched_companies)]
    return candidates, matched_companies, True


# =========================================================
# 24. BUILD RESULT
# =========================================================

def build_result(row, original_index, similarity, field_scores):
    return {
        "index": original_index,
        "experience_id": row["experience_id"],
        "experience_type": row["experience_type"],
        "branch": row["branch"],
        "company": row["company"],
        "role": row["role"],
        "similarity": float(similarity),
        "field_scores": field_scores,
        "document_text": row["document_text"],
    }


# =========================================================
# 25. EXTRACT QUERY TERMS
# =========================================================

def get_query_terms(query):
    normalized_query = normalize_text(query)

    stop_words = {
        "what", "which", "where", "when", "why", "how", "should", "could",
        "would", "can", "do", "does", "did", "i", "me", "my", "we", "our",
        "you", "your", "is", "are", "was", "were", "be", "to", "for", "in",
        "on", "of", "and", "or", "the", "a", "an", "this", "that", "these",
        "those", "study", "focus", "prepare", "preparation",
    }

    terms = []
    for word in normalized_query.split():
        if len(word) >= 3 and word not in stop_words:
            terms.append(word)

    return list(dict.fromkeys(terms))


# =========================================================
# 26. LEXICAL EVIDENCE
# =========================================================

def calculate_lexical_evidence(query, document_index, relevant_fields):
    query_terms = get_query_terms(query)

    if not query_terms:
        return 0.0

    best_score = 0.0

    for field in relevant_fields:
        if field not in EMBEDDING_FIELDS:
            continue

        value = df.iloc[document_index][field]
        if pd.isna(value):
            continue

        field_text = normalize_text(value)
        if not field_text:
            continue

        field_words = set(field_text.split())
        matched_terms = [term for term in query_terms if term in field_words]

        if not matched_terms:
            continue

        score = len(matched_terms) / len(query_terms)
        best_score = max(best_score, score)

    return best_score


# =========================================================
# 27. FIELD-AWARE SIMILARITY (UNCHANGED — weighting untouched)
# =========================================================

def calculate_field_similarity(query_embedding, document_index, relevant_fields, query, query_types):
    field_scores = {}

    for position, field in enumerate(EMBEDDING_FIELDS):
        embedding = field_embeddings[document_index, position]
        score = util.cos_sim(query_embedding, embedding).item()
        field_scores[field] = score

    relevant_scores = []
    for field in relevant_fields:
        if field in field_scores:
            relevant_scores.append(field_scores[field])

    relevant_scores = sorted(relevant_scores, reverse=True)

    if not relevant_scores:
        semantic_score = max(field_scores.values())
    else:
        weights = [0.70, 0.20, 0.10]
        semantic_score = 0.0
        for i, score in enumerate(relevant_scores[:3]):
            semantic_score += weights[i] * score

    lexical_score = 0.0
    if (
        "topics" in query_types
        and not detect_mentioned_company(query)
        and "important_topics" in relevant_fields
    ):
        lexical_score = calculate_lexical_evidence(query, document_index, ["important_topics"])

    final_score = 0.90 * semantic_score + 0.10 * lexical_score

    return final_score, field_scores


# =========================================================
# 28. SEARCH
# =========================================================

def search(query, top_k=None):
    intent_candidates = get_top_intent_candidates(query)
    query_types = resolve_query_intents(query, intent_candidates)
    relevant_fields = get_relevant_fields_from_intents(query_types)

    candidates, matched_companies, company_was_mentioned = get_candidates(query)

    if company_was_mentioned and not matched_companies:
        return {
            "query": query,
            "matched_companies": [],
            "candidate_count": 0,
            "company_was_mentioned": True,
            "query_types": query_types,
            "intent_candidates": intent_candidates,
            "relevant_fields": relevant_fields,
            "retrieved_count": 0,
            "results": [],
        }

    if top_k is not None:
        retrieval_k = top_k
    elif company_was_mentioned:
        retrieval_k = COMPANY_TOP_K
    else:
        retrieval_k = GENERIC_TOP_K

    query_embedding = model.encode(query, convert_to_tensor=True)
    candidate_indices = candidates.index.tolist()

    if not candidate_indices:
        return {
            "query": query,
            "matched_companies": matched_companies,
            "candidate_count": 0,
            "company_was_mentioned": company_was_mentioned,
            "query_types": query_types,
            "intent_candidates": intent_candidates,
            "relevant_fields": relevant_fields,
            "retrieved_count": 0,
            "results": [],
        }

    scored_results = []
    for original_index in candidate_indices:
        similarity, field_scores = calculate_field_similarity(
            query_embedding, original_index, relevant_fields, query, query_types
        )
        row = df.iloc[original_index]
        scored_results.append(build_result(row, original_index, similarity, field_scores))

    scored_results = sorted(scored_results, key=lambda x: x["similarity"], reverse=True)
    results = scored_results[:retrieval_k]

    return {
        "query": query,
        "matched_companies": matched_companies,
        "candidate_count": len(candidates),
        "company_was_mentioned": company_was_mentioned,
        "query_types": query_types,
        "intent_candidates": intent_candidates,
        "relevant_fields": relevant_fields,
        "retrieved_count": len(results),
        "results": results,
    }


# =========================================================
# 29. TEST
# =========================================================

if __name__ == "__main__":

    test_queries = [
        "How should I prepare for BNY?",
        "What questions were asked in BNY?",
        "How should I prepare for BNY and what questions were asked?",
        "What is the selection process and what was the online test like at BNY?",
        "What kind of things did they ask candidates about?",
        "What should I be ready for at BNY?",
        "What advice would you give juniors preparing for placements?",
        "Any tips for someone preparing for BNY?",
        "What DSA topics should I study?",
        "What projects were discussed during the interview?",
        # regression checks — "db"/"ti" no longer trigger company detection
        "What DBMS topics should I study?",
        "What DB topics should I study for interviews?",
        "What interview questions were asked at Deutsche Bank?",
        # new: core-name matching for names with a parenthetical/suffix
        "What questions were asked at Texas Instruments?",
        "What is the eligibility for Texas Instruments?",
    ]

    for query in test_queries:
        result = search(query)

        print()
        print("=" * 70)
        print("Question:", result["query"])
        print("Intent candidates:")
        for item in result["intent_candidates"]:
            print(f"  {item['intent']}: {item['similarity']:.4f}")
        print("Resolved intents:", result["query_types"])
        print("Detected company:", result["matched_companies"])
        print("Company mentioned:", result["company_was_mentioned"])
        print("Relevant fields:", result["relevant_fields"])
        print("Candidate documents:", result["candidate_count"])
        print("Retrieved documents:", result["retrieved_count"])
        print("=" * 70)

        for item in result["results"]:
            print()
            print("Experience:", item["experience_id"])
            print("Company:", item["company"])
            print("Similarity:", round(item["similarity"], 4))
            print("Field scores:")
            for field, score in sorted(item["field_scores"].items(), key=lambda x: x[1], reverse=True):
                print(f"  {field}: {score:.4f}")
            print("\nRelevant experience:")
            print(item["document_text"][:1000])
            print("-" * 70)