from search_embeddings import search


# =========================================================
# EVALUATION DATASET
# =========================================================

TEST_CASES = [

    # -----------------------------------------------------
    # PREPARATION
    # -----------------------------------------------------

    {
        "query": "How should I prepare for BNY?",
        "expected_intents": ["preparation"],
        "expected_company": ["BNY Mellon"],
        "expected_fields": [
            "test_preparation",
            "important_topics",
            "resources",
        ],
    },

    {
        "query": "Any tips for someone preparing for BNY?",
        "expected_intents": ["advice"],
        "expected_company": ["BNY Mellon"],
        "expected_fields": [
            "junior_advice",
            "last_minute_preparation",
        ],
    },

    {
        "query": "What should I be ready for at BNY?",
        "expected_intents": ["preparation"],
        "expected_company": ["BNY Mellon"],
        "expected_fields": [
            "test_preparation",
            "important_topics",
            "resources",
        ],
    },


    # -----------------------------------------------------
    # INTERVIEW
    # -----------------------------------------------------

    {
        "query": "What questions were asked in BNY interviews?",
        "expected_intents": ["interview"],
        "expected_company": ["BNY Mellon"],
        "expected_fields": [
            "interview_experience",
            "important_topics",
        ],
    },

    {
        "query": "What kind of things did they ask candidates about?",
        "expected_intents": ["interview"],
        "expected_company": [],
        "expected_fields": [
            "interview_experience",
            "important_topics",
        ],
    },

    {
        "query": "What interview questions were asked at Deutsche Bank?",
        "expected_intents": ["interview"],
        "expected_company": ["Deutsche Bank"],
        "expected_fields": [
            "interview_experience",
            "important_topics",
        ],
    },


    # -----------------------------------------------------
    # PROJECTS
    # -----------------------------------------------------

    {
        "query": "What projects did they ask about at BNY?",
        "expected_intents": ["projects", "interview"],
        "expected_company": ["BNY Mellon"],
        "expected_fields": [
            "projects",
            "interview_experience",
            "important_topics",
        ],
    },

    {
        "query": "What projects were discussed during the interview?",
        "expected_intents": ["projects", "interview"],
        "expected_company": [],
        "expected_fields": [
            "projects",
            "interview_experience",
            "important_topics",
        ],
    },


    # -----------------------------------------------------
    # TEST
    # -----------------------------------------------------

    {
        "query": "What was the coding test like at BNY?",
        "expected_intents": ["test"],
        "expected_company": ["BNY Mellon"],
        "expected_fields": [
            "test_description",
            "test_preparation",
        ],
    },

    {
        "query": "What was the online assessment like?",
        "expected_intents": ["test"],
        "expected_company": [],
        "expected_fields": [
            "test_description",
            "test_preparation",
        ],
    },


    # -----------------------------------------------------
    # SELECTION
    # -----------------------------------------------------

    {
        "query": "What is the selection process at BNY?",
        "expected_intents": ["selection"],
        "expected_company": ["BNY Mellon"],
        "expected_fields": [
            "selection_procedure",
        ],
    },

    {
        "query": "How many rounds were there?",
        "expected_intents": ["selection"],
        "expected_company": [],
        "expected_fields": [
            "selection_procedure",
        ],
    },


    # -----------------------------------------------------
    # TOPICS
    # -----------------------------------------------------

    {
        "query": "What DSA topics were asked?",
        "expected_intents": ["topics", "interview"],
        "expected_company": [],
        "expected_fields": [
            "important_topics",
            "interview_experience",
        ],
    },

    {
        "query": "Which DBMS topics were asked?",
        "expected_intents": ["topics"],
        "expected_company": [],
        "expected_fields": [
            "important_topics",
        ],
    },

    {
        "query": "What OS topics were asked?",
        "expected_intents": ["topics"],
        "expected_company": [],
        "expected_fields": [
            "important_topics",
        ],
    },

    {
        "query": "What OOPS topics were asked?",
        "expected_intents": ["topics", "interview"],
        "expected_company": [],
        "expected_fields": [
            "important_topics",
            "interview_experience",
        ],
    },

    {
        "query": "Which computer networks topics were asked?",
        "expected_intents": ["topics", "interview"],
        "expected_company": [],
        "expected_fields": [
            "important_topics",
            "interview_experience",
        ],
    },


    # -----------------------------------------------------
    # ELIGIBILITY
    # -----------------------------------------------------

    {
        "query": "What CGPA is required for BNY?",
        "expected_intents": ["eligibility"],
        "expected_company": ["BNY Mellon"],
        "expected_fields": [
            "eligibility",
        ],
    },

    {
        "query": "Which branches are eligible?",
        "expected_intents": ["eligibility"],
        "expected_company": [],
        "expected_fields": [
            "eligibility",
        ],
    },


    # -----------------------------------------------------
    # COMPENSATION
    # -----------------------------------------------------

    {
        "query": "What stipend did BNY offer?",
        "expected_intents": ["compensation"],
        "expected_company": ["BNY Mellon"],
        "expected_fields": [
            "compensation",
        ],
    },

    {
        "query": "What salary was offered?",
        "expected_intents": ["compensation"],
        "expected_company": [],
        "expected_fields": [
            "compensation",
        ],
    },


    # -----------------------------------------------------
    # ADVICE
    # -----------------------------------------------------

    {
        "query": "What advice would you give juniors preparing for placements?",
        "expected_intents": ["advice"],
        "expected_company": [],
        "expected_fields": [
            "junior_advice",
            "last_minute_preparation",
        ],
    },

    {
        "query": "What would you recommend to a fresher?",
        "expected_intents": ["advice"],
        "expected_company": [],
        "expected_fields": [
            "junior_advice",
            "last_minute_preparation",
        ],
    },


    # -----------------------------------------------------
    # MULTI-INTENT
    # -----------------------------------------------------

    {
        "query": "What is the selection process and what was the online test like at BNY?",
        "expected_intents": ["selection", "test"],
        "expected_company": ["BNY Mellon"],
        "expected_fields": [
            "selection_procedure",
            "test_description",
            "test_preparation",
        ],
    },

    {
        "query": "How should I prepare for BNY and what questions were asked?",
        "expected_intents": ["preparation", "interview"],
        "expected_company": ["BNY Mellon"],
        "expected_fields": [
            "test_preparation",
            "important_topics",
            "resources",
            "interview_experience",
        ],
    },


    # -----------------------------------------------------
    # COMPANY ALIAS / REGRESSION
    # -----------------------------------------------------

    {
        "query": "What interview questions were asked at Deutsche Bank?",
        "expected_intents": ["interview"],
        "expected_company": ["Deutsche Bank"],
        "expected_fields": [
            "interview_experience",
            "important_topics",
        ],
    },

    {
        "query": "What DBMS topics should I study?",
        "expected_intents": ["preparation", "topics"],
        "expected_company": [],
        "expected_fields": [
            "test_preparation",
            "important_topics",
            "resources",
        ],
    },

    {
        "query": "What DB topics should I study for interviews?",
        "expected_intents": ["preparation", "topics"],
        "expected_company": [],
        "expected_fields": [
            "test_preparation",
            "important_topics",
            "resources",
        ],
    },
]


# =========================================================
# HELPERS
# =========================================================

def normalize_list(values):
    return set(values or [])


def calculate_accuracy(correct, total):
    if total == 0:
        return 0.0

    return (correct / total) * 100


# =========================================================
# RUN EVALUATION
# =========================================================

def run_evaluation():

    intent_correct = 0
    company_correct = 0
    field_correct = 0

    total = len(TEST_CASES)

    print("\n")
    print("=" * 80)
    print("RETRIEVAL SYSTEM EVALUATION")
    print("=" * 80)
    print("Total test cases:", total)

    for index, test in enumerate(TEST_CASES, start=1):

        query = test["query"]

        print("\n")
        print("-" * 80)
        print(f"TEST {index}/{total}")
        print("QUERY:", query)

        result = search(query)

        actual_intents = normalize_list(result["query_types"])
        expected_intents = normalize_list(test["expected_intents"])

        actual_company = normalize_list(result["matched_companies"])
        expected_company = normalize_list(test["expected_company"])

        actual_fields = normalize_list(result["relevant_fields"])
        expected_fields = normalize_list(test["expected_fields"])


        # -------------------------------------------------
        # INTENT
        # -------------------------------------------------

        intent_match = actual_intents == expected_intents

        if intent_match:
            intent_correct += 1

        print("\nINTENT")
        print("Expected:", sorted(expected_intents))
        print("Actual:  ", sorted(actual_intents))
        print("Status:  ", "PASS" if intent_match else "FAIL")


        # -------------------------------------------------
        # COMPANY
        # -------------------------------------------------

        company_match = actual_company == expected_company

        if company_match:
            company_correct += 1

        print("\nCOMPANY")
        print("Expected:", sorted(expected_company))
        print("Actual:  ", sorted(actual_company))
        print("Status:  ", "PASS" if company_match else "FAIL")


        # -------------------------------------------------
        # FIELDS
        # -------------------------------------------------

        field_match = actual_fields == expected_fields

        if field_match:
            field_correct += 1

        print("\nFIELDS")
        print("Expected:", sorted(expected_fields))
        print("Actual:  ", sorted(actual_fields))
        print("Status:  ", "PASS" if field_match else "FAIL")


    # =====================================================
    # FINAL RESULTS
    # =====================================================

    print("\n")
    print("=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)

    print(
        f"Intent accuracy:  "
        f"{calculate_accuracy(intent_correct, total):.2f}% "
        f"({intent_correct}/{total})"
    )

    print(
        f"Company accuracy: "
        f"{calculate_accuracy(company_correct, total):.2f}% "
        f"({company_correct}/{total})"
    )

    print(
        f"Field accuracy:   "
        f"{calculate_accuracy(field_correct, total):.2f}% "
        f"({field_correct}/{total})"
    )

    print("=" * 80)


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    run_evaluation()