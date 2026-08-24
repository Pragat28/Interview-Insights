from generate_answer import generate_answer


# =========================================================
# Test queries
# =========================================================

TEST_QUERIES = [

    # -----------------------------------------------------
    # 1. Company + preparation
    # -----------------------------------------------------

    "How should I prepare for BNY?",


    # -----------------------------------------------------
    # 2. Company + technical interview
    # -----------------------------------------------------

    "What questions were asked in BNY technical interviews?",


    # -----------------------------------------------------
    # 3. Company + selection process
    # -----------------------------------------------------

    "What is the selection process for Wells Fargo?",


    # -----------------------------------------------------
    # 4. Company + eligibility
    # -----------------------------------------------------

    "What is the CGPA eligibility for Wells Fargo?",


    # -----------------------------------------------------
    # 5. Company + coding test
    # -----------------------------------------------------

    "What should I prepare for the Wells Fargo coding test?",


    # -----------------------------------------------------
    # 6. Company + compensation
    # -----------------------------------------------------

    "What stipend does BNY Mellon offer for internships?",


    # -----------------------------------------------------
    # 7. Company + projects
    # -----------------------------------------------------

    "What kind of projects should I be prepared to explain for BNY?",


    # -----------------------------------------------------
    # 8. Company + topics
    # -----------------------------------------------------

    "What subjects should I study for BNY?",


    # -----------------------------------------------------
    # 9. No company
    # -----------------------------------------------------

    "How should I prepare for a technical interview?",


    # -----------------------------------------------------
    # 10. No company + DSA
    # -----------------------------------------------------

    "What DSA topics should I focus on for placements?",


    # -----------------------------------------------------
    # 11. Advice
    # -----------------------------------------------------

    "What advice would you give to juniors preparing for placements?",


    # -----------------------------------------------------
    # 12. Unknown company
    # -----------------------------------------------------

    "How should I prepare for Google's technical interview?"

]


# =========================================================
# Run tests
# =========================================================

for number, query in enumerate(TEST_QUERIES, start=1):

    print("\n")
    print("#" * 80)
    print(f"TEST {number}")
    print("#" * 80)

    print("\nQUESTION")
    print("-" * 80)

    print(query)


    try:

        result = generate_answer(query)


        print("\nCOMPANY")
        print("-" * 80)

        print(result["company"])


        print("\nCANDIDATE DOCUMENTS")
        print("-" * 80)

        print(result["candidate_count"])


        print("\nQUERY TYPES")
        print("-" * 80)

        print(result["query_types"])


        print("\nFIELDS")
        print("-" * 80)

        print(result["fields"])


        print("\nANSWER")
        print("-" * 80)

        print(result["answer"])


    except Exception as e:

        print("\nERROR")
        print("-" * 80)

        print(e)