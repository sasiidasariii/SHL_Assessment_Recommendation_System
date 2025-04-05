import pandas as pd
import re
from sentence_transformers import SentenceTransformer, util
import numpy as np
from difflib import get_close_matches


model = SentenceTransformer("all-MiniLM-L6-v2")

class SHLRecommender:
    def __init__(self, data_path="data/shl_detailed_test_info_final.csv"):
        self.df = pd.read_csv(data_path)
        self.df["description"] = self.df["description"].fillna("")
        self.df["job_levels"] = self.df["job_levels"].fillna("")

        self.df["text"] = self.df.apply(
            lambda x: f"{x['assessment_name']} {x['test_type_full']} {x['description']} {x['job_levels']}",
            axis=1
        )
        self.embeddings = model.encode(self.df["text"].tolist(), convert_to_tensor=True)

        self.known_job_levels = [
            "Director", "Entry-Level", "Executive", "General Population", "Graduate",
            "Manager", "Mid-Professional", "Front Line Manager", "Supervisor"
        ]

        self.skill_keywords = [
            "python", "sql", "javascript", "java", "communication",
            "problem solving", "c++", "html", "css", "data analysis",
            "teamwork", "collaboration", "leadership", "critical thinking"
        ]

        self.synonym_dict = {
            "js": "javascript",
            "py": "python",
            "pythn": "python",
            "javascrpt": "javascript",
            "java script": "javascript",  # <-- Added
            "sqls": "sql",
            "prob solving": "problem solving",
            "collab": "collaboration",
            "lead": "leadership",
            "comm": "communication",
            "html5": "html",
            "css3": "css",
            "data analytics": "data analysis"
        }

    def recommend(self, query, top_k=10):
        duration_limit = self.extract_duration(query)
        keywords = self.extract_keywords(query)
        matched_levels = self.extract_job_levels(query)

        query_embedding = model.encode(query, convert_to_tensor=True)
        scores = util.cos_sim(query_embedding, self.embeddings)[0].cpu().numpy()
        self.df["score"] = scores

        if keywords:
            self.df["keyword_matches"] = self.df["description"].apply(
                lambda desc: sum(1 for kw in keywords if kw.lower() in str(desc).lower())
            )
            self.df["final_score"] = self.df["score"] + 0.2 * self.df["keyword_matches"]
        else:
            self.df["final_score"] = self.df["score"]

        if matched_levels:
            self.df["job_level_match"] = self.df["job_levels"].apply(
                lambda levels: any(level in levels for level in matched_levels)
            )
            self.df["final_score"] += self.df["job_level_match"].astype(float) * 0.3

        filtered = self.df.copy()
        if duration_limit:
            filtered["duration_num"] = (
                self.df["assessment_length"].str.extract(r"(\d+)").astype(float)
            )
            filtered = filtered[filtered["duration_num"] <= duration_limit]

        # 🧠 Apply skill conflict filter to avoid Java vs JavaScript confusion
        filtered = self.filter_conflicting_skills(keywords, filtered)

        filtered = filtered.sort_values("final_score", ascending=False)

        results = filtered.head(top_k)[[ 
            "assessment_name", "url", "assessment_length",
            "remote_testing_support", "adaptive_irt_support",
            "test_type_full", "final_score"
        ]].rename(columns={
            "assessment_name": "Name",
            "url": "URL",
            "assessment_length": "Duration",
            "remote_testing_support": "Remote",
            "adaptive_irt_support": "Adaptive",
            "test_type_full": "Type",
            "final_score": "score"
        })

        results["Remote"] = results["Remote"].apply(lambda x: "Yes" if str(x).strip().lower() == "true" else "No")
        results["Adaptive"] = results["Adaptive"].apply(lambda x: "Yes" if str(x).strip().lower() == "true" else "No")

        return results.to_dict(orient="records")

    def extract_duration(self, query):
        match = re.search(r"(\d+)\s*minutes", query.lower())
        if match:
            return int(match.group(1))
        return None

    def extract_keywords(self, query):
        query_lower = query.lower()

        # Normalize known spaced keywords like "java script"
        replacements = {
            "java script": "javascript",
            "data analytics": "data analysis",
            "problem-solving": "problem solving"
        }
        for k, v in replacements.items():
            query_lower = query_lower.replace(k, v)

        # Apply synonym substitutions
        for short_form, full_form in self.synonym_dict.items():
            query_lower = re.sub(rf"\b{re.escape(short_form)}\b", full_form, query_lower)

        words = re.findall(r'\w+', query_lower)
        matched_skills = set()
        for word in words:
            close = self.fuzzy_match_keywords(word, self.skill_keywords)
            if close:
                matched_skills.add(close)

        # 👇 Handle conflict: if "java" present and "javascript" is not explicitly mentioned, remove "javascript"
        if "java" in matched_skills and "javascript" in matched_skills and "javascript" not in query_lower:
            matched_skills.remove("javascript")

        return list(matched_skills)

    def fuzzy_match_keywords(self, word, keyword_list, threshold=0.8):
        matches = get_close_matches(word, keyword_list, n=1, cutoff=threshold)
        return matches[0] if matches else None

    def extract_job_levels(self, query):
        query_lower = query.lower()
        return [level for level in self.known_job_levels if level.lower() in query_lower]

    def filter_conflicting_skills(self, keywords, df):
        # 🧹 Exclude front-end skills if query is about Java only
        if "java" in keywords and "javascript" not in keywords:
            df = df[~df["description"].str.contains("javascript|html|css", case=False, na=False)]
            df = df[~df["assessment_name"].str.contains("javascript|html|css", case=False, na=False)]
        return df

# For Evaluation

recommender = SHLRecommender()

def retrieve_top_k(query: str, k: int = 5):
    return recommender.recommend(query, top_k=k)

