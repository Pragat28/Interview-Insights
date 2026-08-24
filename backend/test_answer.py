from generate_answer import generate_answer


# =========================================================
# Test questions
# =========================================================

TEST_QUERIES = [

    # -----------------------------------------------------
    # 1. Single company + preparation
    # -----------------------------------------------------

    "How should I prepare for BNY?",


    # -----------------------------------------------------
    # 2. Single company + interview
    # -----------------------------------------------------

    "What questions were asked in BNY technical interviews?",


    # -----------------------------------------------------
    # 3. Single company + selection
    # -----------------------------------------------------

    "What is the selection process for Wells Fargo?",


    # -----------------------------------------------------
    # 4. Single company + eligibility
    # -----------------------------------------------------

    "What is the CGPA eligibility for Wells Fargo?",


    # -----------------------------------------------------
    # 5. Single company + test preparation
    # -----------------------------------------------------

    "What should I prepare for the Wells Fargo coding test?",


    # -----------------------------------------------------
    # 6. Single company + compensation
    # -----------------------------------------------------

    "What stipend does BNY Mellon offer for internships?",


    # -----------------------------------------------------
    # 7. Single company + projects
    # -----------------------------------------------------

    "What kind of projects should I be prepared to explain for BNY?",


    # -----------------------------------------------------
    # 8. Single company + topics
    # -----------------------------------------------------

    "What subjects should I study for BNY?",


    # -----------------------------------------------------
    # 9. Multiple companies + preparation
    # -----------------------------------------------------

    "How should I prepare for BNY and Wells Fargo?",


    # -----------------------------------------------------
    # 10. Multiple companies + projects + interview
    # -----------------------------------------------------

    "What projects should I prepare for BNY and Wells Fargo and what questions were asked?",


    # -----------------------------------------------------
    # 11. Multiple intents + single company
    # -----------------------------------------------------

    "What are the selection process and interview questions for BNY?",


    # -----------------------------------------------------
    # 12. Preparation + topics
    # -----------------------------------------------------

    "How should I prepare for BNY and what DSA topics should I study?",


    # -----------------------------------------------------
    # 13. Preparation + interview
    # -----------------------------------------------------

    "How should I prepare for BNY technical interviews and what questions were asked?",


    # -----------------------------------------------------
    # 14. No company mentioned
    # -----------------------------------------------------

    "How should I prepare for a technical interview?",


    # -----------------------------------------------------
    # 15. No company + DSA
    # -----------------------------------------------------

    "What DSA topics should I focus on for placements?",


    # -----------------------------------------------------
    # 16. No company + general advice
    # -----------------------------------------------------

    "What advice would you give to juniors preparing for placements?",


    # -----------------------------------------------------
    # 17. Unknown company
    # -----------------------------------------------------

    "How should I prepare for Google?",


    # -----------------------------------------------------
    # 18. Unknown company + specific topic
    # -----------------------------------------------------

    "What is the selection process for Microsoft?",


    # -----------------------------------------------------
    # 19. Grounding test
    #
    # The dataset does not explicitly provide exact DSA
    # topics for BNY.
    #
    # The answer should NOT invent topics from Striver.
    # -----------------------------------------------------

    "What exact DSA topics are asked in BNY?",


    # -----------------------------------------------------
    # 20. Unknown information
    # -----------------------------------------------------

    "What is the exact BNY interview pass percentage?",


    # -----------------------------------------------------
    # 21. Company alias test
    # -----------------------------------------------------

    "How should I prepare for BNY's technical interview?",


    # -----------------------------------------------------
    # 22. Another company alias test
    # -----------------------------------------------------

    "How should I prepare for Wells technical interviews?",


    # -----------------------------------------------------
    # 23. Multiple company + compensation
    # -----------------------------------------------------

    "What is the internship stipend at BNY and Wells Fargo?",


    # -----------------------------------------------------
    # 24. Multiple company + selection
    # -----------------------------------------------------

    "What are the selection processes for BNY and Wells Fargo?",


    # -----------------------------------------------------
    # 25. Multiple company + topics
    # -----------------------------------------------------

    "What subjects should I study for BNY and Wells Fargo?"
]


# =========================================================
# Run tests
# =========================================================

for i, query in enumerate(
    TEST_QUERIES,
    start=1
):

    print("\n")
    print("#" * 80)
    print(f"TEST {i}")
    print("#" * 80)


    print("\nQUERY")
    print("-" * 80)
    print(query)


    try:

        result = generate_answer(
            query
        )


        # -------------------------------------------------
        # Company detection
        # -------------------------------------------------

        print("\nDETECTED COMPANY")
        print("-" * 80)
        print(
            result["company"]
        )


        # -------------------------------------------------
        # Candidate count
        # -------------------------------------------------

        print("\nCANDIDATE DOCUMENTS")
        print("-" * 80)
        print(
            result["candidate_count"]
        )


        # -------------------------------------------------
        # Query types
        # -------------------------------------------------

        print("\nQUERY TYPES")
        print("-" * 80)
        print(
            result["query_types"]
        )


        # -------------------------------------------------
        # Selected fields
        # -------------------------------------------------

        print("\nFIELDS")
        print("-" * 80)
        print(
            result["fields"]
        )


        # -------------------------------------------------
        # Final answer
        # -------------------------------------------------

        print("\nANSWER")
        print("-" * 80)
        print(
            result["answer"]
        )


    except Exception as e:

        print("\nERROR")
        print("-" * 80)

        print(
            type(e).__name__,
            ":",
            e
        )


print("\n")
print("=" * 80)
print("ALL TESTS COMPLETED")
print("=" * 80)