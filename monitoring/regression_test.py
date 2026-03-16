import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from tracing import trace_search

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

# Quality thresholds — if scores drop below these, the test fails
THRESHOLDS = {
    "min_results":         3,     # must return at least 3 results
    "min_top_score":       0.0,   # top reranker score must be above 0
    "min_results_ratio":   1.0,   # must return all requested results
}

TEST_QUERIES = [
    "What are the latest treatments for diabetes?",
    "How does immunotherapy work for cancer?",
    "What are the side effects of metformin?",
]

def run_regression():
    print("=" * 60)
    print("RAG Regression Test")
    print("=" * 60)

    passed = 0
    failed = 0
    failures = []

    for query in TEST_QUERIES:
        print(f"\nTesting: {query[:50]}...")
        answer, results = trace_search(query, top_k=3)

        errors = []

        # Check 1 - minimum results
        if len(results) < THRESHOLDS["min_results"]:
            errors.append(f"Too few results: {len(results)} < {THRESHOLDS['min_results']}")

        # Check 2 - top score
        top_score = results[0]["rerank_score"] if results else -999
        if top_score <= THRESHOLDS["min_top_score"]:
            errors.append(f"Low top score: {top_score:.4f}")

        # Check 3 - coverage
        ratio = len(results) / 3
        if ratio < THRESHOLDS["min_results_ratio"]:
            errors.append(f"Low coverage: {ratio:.2f} < {THRESHOLDS['min_results_ratio']}")

        if errors:
            failed += 1
            failures.append({"query": query, "errors": errors})
            print(f"  FAIL — {', '.join(errors)}")
        else:
            passed += 1
            print(f"  PASS — {len(results)} results, top score: {top_score:.4f}")

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed > 0:
        print("\nFAILED QUERIES:")
        for f in failures:
            print(f"  - {f['query']}")
            for e in f["errors"]:
                print(f"    {e}")
        sys.exit(1)
    else:
        print("\nAll tests passed. RAG quality is stable.")
        sys.exit(0)


if __name__ == "__main__":
    run_regression()