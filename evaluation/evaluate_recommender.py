import pandas as pd
from difflib import SequenceMatcher

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.recommender import retrieve_top_k

# --- Define ground truth examples ---
test_queries = [
    {
        "query": "Find an entry-level test that evaluates reasoning skills for candidates with a time limit of 60 minutes.",
        "ground_truth_names": [
            "Verify - Deductive Reasoning",
            "Verify - Numerical Ability",
            "Verify - Following Instructions",
            "Verify - Inductive Reasoning (2014)",
           
        ],
    },
    {
        "query": "Give me assessments to test JavaScript skills for graduates that are remote-compatible.",
        "ground_truth_names": [
            "Automata Front End",
            "Smart Interview Live Coding",
            "Virtual Assessment and Development Centers"
        ],
    },
]



# --- Load the assessment dataset ---
df = pd.read_csv("data/shl_detailed_test_info_final.csv")
print(f"✅ Loaded {len(df)} rows from data/shl_detailed_test_info_final.csv")

# --- Utility: Fuzzy matching ---
def is_similar(a, b, threshold=0.8):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() >= threshold

# --- Evaluation Metrics ---
def recall_at_k(predicted, relevant, k):
    top_k = predicted[:k]
    hits = sum(1 for item in top_k if any(is_similar(item, r) for r in relevant))
    return hits / len(relevant) if relevant else 0.0

def map_at_k(predicted, relevant, k):
    top_k = predicted[:k]
    score = 0.0
    hits = 0
    for i, p in enumerate(top_k, start=1):
        if any(is_similar(p, r) for r in relevant):
            hits += 1
            score += hits / i
    return score / min(len(relevant), k) if relevant else 0.0

# --- Run Evaluation ---
def evaluate_model(model, dataset, queries, k=5):
    for q in queries:
        query = q["query"]
        relevant_names = q["ground_truth_names"]
        
        print(f"\n🔍 Evaluating Query: {query}")
        results = retrieve_top_k(query, k=k)
        print(results)

        
        predicted_names = [item["Name"] for item in results]
        predicted_names = list(dict.fromkeys(predicted_names))  # Removes duplicates, preserves order

        scores = [item["score"] for item in results]

        print("📌 Top 5 Predictions:")
        for idx, (name, score) in enumerate(zip(predicted_names, scores), 1):
            print(f"{idx}. {name} (Score: {round(score, 2)})")

        print("🔎 Ground Truths:", relevant_names)
        print("🎯 Predicted Names:", predicted_names)

        r_at_k = recall_at_k(predicted_names, relevant_names, k)
        m_at_k = map_at_k(predicted_names, relevant_names, k)

        print(f"\n✅ Evaluation Complete")
        print(f"🧠 Query: {query}")
        print(f"📊 Recall@{k}: {round(r_at_k, 4)}")
        print(f"📈 MAP@{k}: {round(m_at_k, 4)}")
        print("-" * 60)

# --- Run it ---
if __name__ == "__main__":
    evaluate_model(None, df, test_queries, k=5)
