from fastapi import FastAPI
from pydantic import BaseModel
from models.recommender import SHLRecommender
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = FastAPI()
recommender = SHLRecommender()

class QueryRequest(BaseModel):
    query: str

@app.post("/recommend")
def recommend_tests(request: QueryRequest):
    results = recommender.recommend(request.query)
    return {"results": results}
if __name__ == "__main__":
    app.run(debug=True)