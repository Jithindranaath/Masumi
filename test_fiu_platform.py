#!/usr/bin/env python3
"""
Test script for FIU Platform
"""

import asyncio
import json
from app.fiu_services_extended import ExtendedFIUService
from app.fiu_models import create_tables

async def test_fiu_platform():
    """Test the FIU platform functionality"""
    print("=" * 60)
    print("TESTING FIU PLATFORM")
    print("=" * 60)
    
    # Initialize database and service
    create_tables()
    fiu_service = ExtendedFIUService()
    
    # Test 1: Create User
    print("\n1. Testing User Creation...")
    import time
    timestamp = str(int(time.time()))
    user_result = fiu_service.create_user(
        name=f"Test User {timestamp}",
        email=f"test{timestamp}@example.com", 
        phone=f"98765{timestamp[-5:]}"
    )
    
    if user_result.get("success"):
        user_id = user_result["user_id"]
        print(f"SUCCESS: User created successfully: {user_id}")
    else:
        print(f"ERROR: User creation failed: {user_result.get('error')}")
        return
    
    # Test 2: Add Bank Account
    print("\n2. Testing Bank Account Addition...")
    account_result = fiu_service.add_bank_account(
        user_id=user_id,
        account_number="12345678901234",  # 14 digits for HDFC
        bank_name="HDFC Bank",
        account_type="savings",
        ifsc_code="HDFC0001234",
        account_holder_name="Test User",
        initial_balance=25000.0
    )
    
    if account_result.get("success"):
        print(f"SUCCESS: Bank account added: {account_result['clean_account_number']}")
        print(f"  Bank: {account_result['validated_bank_name']}")
    else:
        print(f"ERROR: Bank account addition failed: {account_result.get('error')}")
        if 'validation_errors' in account_result:
            print(f"  Validation errors: {account_result['validation_errors']}")
        return
    
    # Test 3: Get User Accounts
    print("\n3. Testing Account Retrieval...")
    accounts = fiu_service.get_user_accounts(user_id)
    if accounts:
        account = accounts[0]
        account_id = account['id']
        account_number = account['account_number']
        print(f"SUCCESS: Retrieved {len(accounts)} account(s)")
        print(f"  Account: {account_number}, Balance: Rs.{account['balance']:,.2f}")
    else:
        print("ERROR: No accounts found")
        return
    
    # Test 4: Add Income
    print("\n4. Testing Income Addition...")
    income_result = fiu_service.add_income(
        user_id=user_id,
        account_number=account_number,
        amount=50000.0,
        source="ABC Company",
        description="Monthly salary",
        category="salary"
    )
    
    if income_result.get("success"):
        print(f"SUCCESS: Income added: Rs.50,000")
        print(f"  New balance: Rs.{income_result['new_balance']:,.2f}")
        print(f"  Masumi TX: {income_result['masumi_tx_hash'][:8]}...")
    else:
        print(f"ERROR: Income addition failed: {income_result.get('error')}")
    
    # Test 5: Add Expense
    print("\n5. Testing Expense Addition...")
    expense_result = fiu_service.add_expense(
        user_id=user_id,
        account_number=account_number,
        amount=15000.0,
        category="rent",
        description="Monthly rent payment",
        merchant="XYZ Apartments"
    )
    
    if expense_result.get("success"):
        print(f"SUCCESS: Expense added: Rs.15,000")
        print(f"  Category: {expense_result['expense_category']}")
        print(f"  New balance: Rs.{expense_result['new_balance']:,.2f}")
    else:
        print(f"ERROR: Expense addition failed: {expense_result.get('error')}")
    
    # Test 6: Sync Account
    print("\n6. Testing Bank Account Sync...")
    sync_result = fiu_service.full_account_sync(account_id)
    
    if sync_result.get("success"):
        balance_sync = sync_result['balance_sync']
        tx_sync = sync_result['transactions_sync']
        print(f"SUCCESS: Account sync completed")
        print(f"  Balance updated: Rs.{balance_sync['new_balance']:,.2f}")
        print(f"  Synced {tx_sync['synced_count']} transactions")
    else:
        print(f"ERROR: Account sync failed: {sync_result.get('error')}")
    
    # Test 7: Get Transaction History
    print("\n7. Testing Transaction History...")
    transactions = fiu_service.get_transaction_history(user_id, limit=10)
    if transactions:
        print(f"SUCCESS: Retrieved {len(transactions)} transactions")
        for i, tx in enumerate(transactions[:3], 1):
            print(f"  {i}. {tx['description']}: Rs.{tx['amount']:,.2f} ({tx['type']})")
    else:
        print("ERROR: No transactions found")
    
    # Test 8: Generate Budget Analysis
    print("\n8. Testing AI Budget Analysis...")
    budget_result = fiu_service.generate_budget_analysis(user_id)
    
    if budget_result.get("success"):
        print(f"SUCCESS: Budget analysis generated")
        print(f"  Total Income: Rs.{budget_result['total_income']:,.2f}")
        print(f"  Total Expenses: Rs.{budget_result['total_expenses']:,.2f}")
        print(f"  Savings Rate: {budget_result['savings_rate']:.1f}%")
        print(f"  Analysis ID: {budget_result['analysis_id']}")
    else:
        print(f"ERROR: Budget analysis failed: {budget_result.get('error')}")
    
    # Test 9: Bank Validation
    print("\n9. Testing Bank Validation...")
    validation_result = fiu_service.validate_bank_details_only(
        account_number="987654321098",
        ifsc_code="SBIN0001234",
        account_holder_name="Jane Smith",
        account_type="current"
    )
    
    if validation_result.get("valid"):
        print("SUCCESS: Bank validation successful")
        print(f"  Bank: {validation_result['bank_info']['bank_name']}")
        print(f"  Clean Account: {validation_result['clean_account']}")
    else:
        print(f"ERROR: Bank validation failed: {validation_result.get('errors')}")
    
    print("\n" + "=" * 60)
    print("FIU PLATFORM TEST COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_fiu_platform())