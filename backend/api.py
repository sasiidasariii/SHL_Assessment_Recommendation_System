from fastapi import FastAPI
from pydantic import BaseModel
from models.recommender import SHLRecommender

app = FastAPI()
recommender = SHLRecommender()

class QueryRequest(BaseModel):
    query: str

@app.post("/recommend")
def recommend_tests(request: QueryRequest):
    results = recommender.recommend(request.query)
    return {"results": results}
