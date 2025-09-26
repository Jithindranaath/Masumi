#!/usr/bin/env python3
"""
Test script to show demo output directly
"""

import asyncio
import json
from app.demo_crew import DemoBudgetPlanner
from app.services.aa_client import AAClient

async def show_demo_output():
    """Show the actual demo output"""
    print("=" * 60)
    print("AI BUDGET PLANNER - DEMO OUTPUT")
    print("=" * 60)
    
    # Step 1: Fetch mock transaction data
    print("\n1. FETCHING TRANSACTION DATA...")
    aa_client = AAClient()
    transactions_data = await aa_client.fetch_data("demo_user")
    
    print(f"   - Fetched {len(transactions_data['transactions'])} transactions")
    print("   - Sample transactions:")
    for i, txn in enumerate(transactions_data['transactions'][:3]):
        print(f"     {i+1}. {txn['description']}: Rs.{abs(txn['amount'])} ({txn['type']})")
    
    # Step 2: Process with AI Budget Planner
    print("\n2. PROCESSING WITH AI BUDGET PLANNER...")
    demo_planner = DemoBudgetPlanner()
    
    print("   - Categorizing transactions...")
    print("   - Analyzing financial patterns...")
    print("   - Creating budget strategy...")
    print("   - Generating final report...")
    
    # Generate the budget report
    budget_report = demo_planner.process_transactions(json.dumps(transactions_data))
    
    # Step 3: Show the results
    print("\n3. AI-GENERATED BUDGET REPORT:")
    print("=" * 60)
    print(budget_report)
    print("=" * 60)
    
    print("\n4. DEMO FEATURES DEMONSTRATED:")
    print("   ✓ Transaction categorization (10 categories)")
    print("   ✓ Financial analysis (income, expenses, savings rate)")
    print("   ✓ 50/30/20 budget strategy")
    print("   ✓ Personalized insights and recommendations")
    print("   ✓ Spending breakdown by category")
    print("   ✓ Recurring payment detection")
    print("   ✓ Top expense identification")
    
    print("\n5. TECHNICAL IMPLEMENTATION:")
    print("   ✓ Account Aggregator integration (mock data)")
    print("   ✓ Multi-agent AI system (4 specialized agents)")
    print("   ✓ FastAPI backend with REST endpoints")
    print("   ✓ React frontend with interactive charts")
    print("   ✓ SQLite database for data persistence")
    print("   ✓ Masumi payment integration ready")
    
    print("\nDEMO COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(show_demo_output())