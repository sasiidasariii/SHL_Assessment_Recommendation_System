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



