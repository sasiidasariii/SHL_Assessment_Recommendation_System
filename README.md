## SHL Assessment Recommendation System

This project is a job-description-to-assessment matching engine that helps recommend the most relevant SHL Individual Test Solutions based on job descriptions or free-form queries. It uses a combination of Large Language Models (LLMs), Sentence-BERT, and a scoring mechanism to generate top-matching assessments.

🔗 **Live Resources**

🌐 **Web App**: https://assessmentapp.streamlit.app

🔌 **API URL**: http://3.110.124.223:8000/recommend

📂 **GitHub Repo**: https://github.com/sasiidasariii/SHL_Assessment_Recommendation_System


## 📁 Repository Structure

![image](https://github.com/user-attachments/assets/78ad5eb1-d62b-4f69-a3aa-c50bd565d0d6)



## 🧠 Approach & Architecture

📌 **Problem Statement**

Recommend the most relevant SHL assessments based on user-provided job titles, descriptions, or skill sets.

🔧 **Solution Architecture**

**Input Handling:** User enters a job title or description via Streamlit UI.

**Text Preprocessing:** Clean and normalize text input and SHL descriptions.

**Vectorization:** Encode texts using SentenceTransformer (MiniLM-based).

**Similarity Computation:** Use cosine similarity to find closest matching assessments.

**Ranking:** Top-N assessments returned based on semantic match score.

## 🔄 Backend API

The core logic is embedded in query.py, which exposes a function to process queries and return recommendations. This is integrated directly into the Streamlit UI.

**API URL**: http://3.110.124.223:8000/recommend


## Evaluation Metrics

The system evaluates the accuracy of the recommendations using two key metrics:

**1. Recall@5**

   Definition: Measures the percentage of relevant tests included in the top 5 recommendations.
   
   Formula: Recall@5 = (Number of Relevant Tests in Top 5) / Total Relevant Tests

**Example for Query 1:**

   Recall@5: 1.0 (100% of the relevant tests were found in the top 5 results)

**2. Mean Average Precision at 5 (MAP@5)**
   
   Definition: Measures the precision of the recommendations in the top 5, averaged across all queries.
   
   Formula: MAP@5 = (1/5) * sum(Precision at k for top k recommendations)

**Example for Query 1:**

   MAP@5: 0.8042 (Average precision for the top 5 recommendations)

**Example for Query 2:**

   MAP@5: 1.0 (Perfect precision for the top 4 recommendations)

**Results**

**Query 1: Find an entry-level test that evaluates reasoning skills for candidates with a time limit of 60 minutes**
Top 5 Recommendations:

   Verify - Deductive Reasoning (Score: 0.87)
   
   Time Management (U.S.) (Score: 0.85)
   
   Verify - Numerical Ability (Score: 0.83)
   
   Verify - Following Instructions (Score: 0.81)
   
   Verify - Inductive Reasoning (2014) (Score: 0.79)

**Evaluation:**

   > Recall@5: 1.0
   
   > MAP@5: 0.8042

**Query 2: Give me assessments to test JavaScript skills for graduates that are remote-compatible**
Top 4 Recommendations:
   
   Automata Front End (Score: 0.97)
   
   Virtual Assessment and Development Centers (Score: 0.97)
   
   Smart Interview Live Coding (Score: 0.78)
   
   RemoteWorkQ Participant Report (Score: 0.76)

**Evaluation:**

   > Recall@5: 1.0
   
   > MAP@5: 1.0
   
   evaluate/: Contains the evaluation script to assess the performance of the recommender.


## 🚀 How to Run Locally

**Clone the repository**

   > git clone https://github.com/sasiidasariii/SHL_Assessment_Recommendation_System.git
   
   > cd SHL_Assessment_Recommendation_System

**Install dependencies**

   > pip install -r requirements.txt

**Run the app**

   > streamlit run frontend/app.py




