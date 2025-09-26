#!/usr/bin/env python3
"""
Simple server to run the AI Budget Planner demo
"""

import asyncio
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from app.demo_crew import DemoBudgetPlanner
from app.services.aa_client import AAClient

app = FastAPI(title="AI Budget Planner Demo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BudgetRequest(BaseModel):
    user_id: str

@app.get("/", response_class=HTMLResponse)
async def get_demo():
    """Serve the demo HTML page"""
    with open("demo.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/generate_budget_plan")
async def generate_budget_plan(request: BudgetRequest):
    """Generate budget plan using demo crew"""
    try:
        # Fetch transaction data
        aa_client = AAClient()
        transactions_data = await aa_client.fetch_data(request.user_id)
        
        # Process with demo planner
        demo_planner = DemoBudgetPlanner()
        budget_report = demo_planner.process_transactions(json.dumps(transactions_data))
        
        return {
            "status": "success",
            "user_id": request.user_id,
            "budget_plan": budget_report
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    print("Starting AI Budget Planner Demo Server...")
    print("Open your browser to: http://localhost:9000")
    uvicorn.run(app, host="0.0.0.0", port=9000)