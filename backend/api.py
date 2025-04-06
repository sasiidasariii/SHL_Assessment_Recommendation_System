from fastapi import FastAPI
from pydantic import BaseModel
from models.recommender import SHLRecommender
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Ensure the parent directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Create app
app = FastAPI()

# Enable CORS (important for Streamlit requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["http://localhost:8501"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load recommender once
recommender = SHLRecommender()

# Input model
class QueryRequest(BaseModel):
    query: str

# Endpoint
@app.post("/recommend")
def recommend_tests(request: QueryRequest):
    results = recommender.recommend(request.query)
    return {"results": results}
