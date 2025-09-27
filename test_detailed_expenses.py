#!/usr/bin/env python3
"""
Test script for detailed expenses API
Demonstrates how to get detailed expenses with purposes and spending reasons
"""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8001"

def test_detailed_expenses_api():
    """Test the detailed expenses API endpoints"""
    
    print("🧪 Testing Detailed Expenses API")
    print("=" * 50)
    
    # Test user ID (you can change this to any existing user)
    user_id = "demo_user"
    
    try:
        # 1. Get detailed expenses
        print("\n📊 Getting detailed expenses...")
        response = requests.get(f"{BASE_URL}/api/expenses/detailed/{user_id}")
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Successfully retrieved detailed expenses")
            print(f"📈 Summary:")
            print(f"   - Total Expenses: Rs.{data['summary']['total_expenses']:,.2f}")
            print(f"   - Total Count: {data['summary']['expense_count']}")
            print(f"   - Detailed Expenses: {data['summary']['detailed_count']}")
            print(f"   - Simple Expenses: {data['summary']['simple_count']}")
            print(f"   - Average Expense: Rs.{data['summary']['average_expense']:,.2f}")
            
            if data['summary']['top_reason'] != 'none':
                print(f"   - Top Spending Reason: '{data['summary']['top_reason']}' (Rs.{data['summary']['top_reason_amount']:,.2f})")
            
            if data['summary']['top_merchant'] != 'none':
                print(f"   - Top Merchant: '{data['summary']['top_merchant']}' (Rs.{data['summary']['top_merchant_amount']:,.2f})")
            
            # Show category breakdown
            print(f"\n📋 Category Breakdown:")
            for category, amount in data['breakdowns']['by_category'].items():
                print(f"   - {category.title()}: Rs.{amount:,.2f}")
            
            # Show priority breakdown
            if data['breakdowns']['by_priority']:
                print(f"\n🎯 Priority Breakdown:")
                for priority, amount in data['breakdowns']['by_priority'].items():
                    emoji = {'essential': '🔴', 'important': '🟡', 'optional': '🟢', 'impulse': '🔵'}.get(priority, '⚪')
                    print(f"   - {emoji} {priority.title()}: Rs.{amount:,.2f}")
            
            # Show recent detailed expenses with reasons
            if data['detailed_expenses']:
                print(f"\n💸 Recent Detailed Expenses (with reasons):")
                for expense in data['detailed_expenses'][:5]:  # Show top 5
                    date = datetime.fromisoformat(expense['date'].replace('Z', '+00:00')).strftime('%Y-%m-%d')
                    priority_emoji = {'essential': '🔴', 'important': '🟡', 'optional': '🟢', 'impulse': '🔵'}.get(expense.get('priority', ''), '⚪')
                    
                    print(f"   {date} | Rs.{abs(expense['amount']):,.2f} | {priority_emoji} {expense.get('priority', 'unknown').title()}")
                    print(f"      📍 {expense.get('merchant', 'Unknown merchant')}")
                    print(f"      💭 Reason: \"{expense.get('reason', 'No reason provided')}\"")
                    print(f"      💳 Payment: {expense.get('payment_method', 'unknown').title()}")
                    print()
            
            # Show spending reasons analysis
            if data['breakdowns']['by_reason']:
                print(f"\n💡 Top Spending Reasons:")
                sorted_reasons = sorted(data['breakdowns']['by_reason'].items(), key=lambda x: x[1], reverse=True)
                for reason, amount in sorted_reasons[:5]:  # Show top 5 reasons
                    print(f"   - \"{reason}\": Rs.{amount:,.2f}")
            
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the FIU server is running on http://localhost:8001")
        print("   Run: python fiu_main.py")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def demo_add_detailed_expense():
    """Demo adding a detailed expense"""
    
    print("\n🆕 Demo: Adding Detailed Expense")
    print("=" * 40)
    
    # Sample detailed expense data
    expense_data = {
        "user_id": "demo_user",
        "account_number": "1234567890",  # Use appropriate account number
        "amount": 850.0,
        "category": "food",
        "description": "Dinner with family",
        "merchant": "The Olive Garden Restaurant",
        "reason": "Monthly family dinner - celebrating mom's birthday",
        "priority": "important",
        "payment_method": "card"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/expense/detailed/add", json=expense_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Detailed expense added successfully!")
            print(f"   Transaction ID: {result['transaction_id']}")
            print(f"   Amount: Rs.{result['amount']:,.2f}")
            print(f"   Merchant: {result['merchant']}")
            print(f"   Reason: {result['reason']}")
            print(f"   Priority: {result['priority']}")
            print(f"   New Balance: Rs.{result['new_balance']:,.2f}")
        else:
            print(f"❌ Error adding expense: {response.status_code} - {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the FIU server is running")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🏦 FIU Platform - Detailed Expenses API Test")
    print("=" * 60)
    
    # Test getting detailed expenses
    test_detailed_expenses_api()
    
    # Demo adding detailed expense (uncomment to test)
    # demo_add_detailed_expense()
    
    print("\n" + "=" * 60)
    print("📚 API Usage Examples:")
    print(f"GET  {BASE_URL}/api/expenses/detailed/{{user_id}} - Get detailed expenses")
    print(f"POST {BASE_URL}/api/expense/detailed/add - Add detailed expense with purpose")
    print("\n💡 The detailed expenses include:")
    print("   - Spending reasons and purposes")
    print("   - Priority levels (essential, important, optional, impulse)")
    print("   - Merchant/store information")
    print("   - Payment method tracking")
    print("   - Category and amount breakdowns")