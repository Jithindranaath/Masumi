#!/usr/bin/env python3
"""
Test script for AI Budget Planner
Run this to verify the setup is working correctly
"""

import asyncio
import json
from app.services.aa_client import AAClient
from app.crew import BudgetPlannerCrew
from logging_config import setup_logging

logger = setup_logging()

async def test_aa_client():
    """Test Account Aggregator client"""
    print("🔍 Testing Account Aggregator Client...")
    
    aa_client = AAClient()
    
    # Test fetching mock data
    data = await aa_client.fetch_data("test_user")
    
    if "transactions" in data:
        print(f"✅ AA Client working - fetched {len(data['transactions'])} transactions")
        return data
    else:
        print("❌ AA Client failed")
        return None

def test_budget_crew(transactions_data):
    """Test Budget Planning Crew"""
    print("\n🤖 Testing Budget Planning Crew...")
    
    try:
        crew = BudgetPlannerCrew(verbose=False)
        
        # Test with mock data
        result = crew.crew.kickoff(inputs={"transactions_data": json.dumps(transactions_data)})
        
        print("✅ Budget Planning Crew working")
        print(f"📋 Generated report preview: {str(result)[:200]}...")
        return result
        
    except Exception as e:
        print(f"❌ Budget Planning Crew failed: {str(e)}")
        return None

async def main():
    """Run all tests"""
    print("🚀 AI Budget Planner - System Test\n")
    
    # Test AA Client
    transactions_data = await test_aa_client()
    
    if transactions_data:
        # Test Budget Crew
        result = test_budget_crew(transactions_data)
        
        if result:
            print("\n🎉 All tests passed! Your AI Budget Planner is ready.")
            print("\nNext steps:")
            print("1. Start the backend: python main.py api")
            print("2. Start the frontend: cd frontend && npm run dev")
            print("3. Open http://localhost:3000 in your browser")
        else:
            print("\n❌ Budget crew test failed")
    else:
        print("\n❌ AA client test failed")

if __name__ == "__main__":
    asyncio.run(main())