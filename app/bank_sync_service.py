import json
import random
from datetime import datetime, timedelta
from typing import Dict, List
from sqlalchemy.orm import Session
from app.fiu_models import BankAccount, Transaction, SessionLocal
import uuid

class BankSyncService:
    """Service to sync bank account data and transactions"""
    
    def __init__(self):
        self.mock_transactions = [
            {"desc": "SALARY CREDIT", "amount": 50000, "type": "credit", "category": "salary"},
            {"desc": "ATM WITHDRAWAL", "amount": -5000, "type": "debit", "category": "cash"},
            {"desc": "GROCERY STORE", "amount": -3500, "type": "debit", "category": "groceries"},
            {"desc": "ELECTRICITY BILL", "amount": -2000, "type": "debit", "category": "bills"},
            {"desc": "FUEL STATION", "amount": -1200, "type": "debit", "category": "fuel"},
            {"desc": "RESTAURANT", "amount": -2500, "type": "debit", "category": "food"},
            {"desc": "ONLINE SHOPPING", "amount": -5000, "type": "debit", "category": "shopping"},
            {"desc": "MEDICAL STORE", "amount": -800, "type": "debit", "category": "healthcare"},
            {"desc": "MOBILE RECHARGE", "amount": -399, "type": "debit", "category": "bills"},
            {"desc": "UBER RIDE", "amount": -450, "type": "debit", "category": "transport"},
            {"desc": "NETFLIX SUBSCRIPTION", "amount": -199, "type": "debit", "category": "entertainment"},
            {"desc": "DIVIDEND CREDIT", "amount": 1500, "type": "credit", "category": "investment"},
            {"desc": "RENT PAYMENT", "amount": -15000, "type": "debit", "category": "rent"},
            {"desc": "INSURANCE PREMIUM", "amount": -2500, "type": "debit", "category": "insurance"},
            {"desc": "FREELANCE PAYMENT", "amount": 8000, "type": "credit", "category": "freelance"}
        ]
    
    def sync_account_balance(self, account_id: int) -> Dict:
        """Sync account balance from bank"""
        db = SessionLocal()
        try:
            account = db.query(BankAccount).filter(BankAccount.id == account_id).first()
            if not account:
                return {"error": "Account not found"}
            
            # Simulate fetching balance from bank API
            # In real implementation, this would call actual bank APIs
            mock_balance = random.uniform(10000, 100000)
            
            old_balance = account.balance
            account.balance = mock_balance
            account.last_sync = datetime.utcnow()
            account.is_synced = True
            
            db.commit()
            
            return {
                "success": True,
                "account_number": account.account_number,
                "old_balance": old_balance,
                "new_balance": mock_balance,
                "sync_time": account.last_sync.isoformat()
            }
            
        except Exception as e:
            db.rollback()
            return {"error": str(e)}
        finally:
            db.close()
    
    def sync_transactions(self, account_id: int, days: int = 30) -> Dict:
        """Sync transactions from bank for specified days"""
        db = SessionLocal()
        try:
            account = db.query(BankAccount).filter(BankAccount.id == account_id).first()
            if not account:
                return {"error": "Account not found"}
            
            # Generate mock transactions for the specified period
            synced_transactions = []
            start_date = datetime.now() - timedelta(days=days)
            
            # Generate 5-15 random transactions
            num_transactions = random.randint(5, 15)
            
            for i in range(num_transactions):
                # Random date within the period
                random_date = start_date + timedelta(
                    days=random.randint(0, days),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
                
                # Random transaction from mock data
                mock_tx = random.choice(self.mock_transactions)
                
                # Check if similar transaction already exists
                existing_tx = db.query(Transaction).filter(
                    Transaction.user_id == account.user_id,
                    Transaction.description.contains(mock_tx["desc"][:10]),
                    Transaction.created_at >= start_date
                ).first()
                
                if existing_tx:
                    continue  # Skip if similar transaction exists
                
                # Create transaction
                transaction = Transaction(
                    user_id=account.user_id,
                    from_account=account.account_number if mock_tx["type"] == "debit" else "EXTERNAL",
                    to_account="EXTERNAL" if mock_tx["type"] == "debit" else account.account_number,
                    amount=abs(mock_tx["amount"]),
                    transaction_type=mock_tx["type"],
                    category="income" if mock_tx["type"] == "credit" else "expense",
                    description=f"{mock_tx['desc']} - Synced from bank",
                    status="completed",
                    masumi_tx_hash=str(uuid.uuid4()),
                    created_at=random_date
                )
                
                db.add(transaction)
                synced_transactions.append({
                    "description": transaction.description,
                    "amount": transaction.amount,
                    "type": transaction.transaction_type,
                    "date": transaction.created_at.isoformat()
                })
            
            # Update account sync status
            account.last_sync = datetime.utcnow()
            account.is_synced = True
            
            db.commit()
            
            return {
                "success": True,
                "account_number": account.account_number,
                "synced_count": len(synced_transactions),
                "transactions": synced_transactions,
                "sync_time": account.last_sync.isoformat()
            }
            
        except Exception as e:
            db.rollback()
            return {"error": str(e)}
        finally:
            db.close()
    
    def get_sync_status(self, user_id: str) -> Dict:
        """Get sync status for all user accounts"""
        db = SessionLocal()
        try:
            from app.fiu_models import User
            user = db.query(User).filter(User.user_id == user_id).first()
            if not user:
                return {"error": "User not found"}
            
            accounts_status = []
            for account in user.bank_accounts:
                accounts_status.append({
                    "account_id": account.id,
                    "account_number": account.account_number,
                    "bank_name": account.bank_name,
                    "is_synced": account.is_synced,
                    "last_sync": account.last_sync.isoformat() if account.last_sync else None,
                    "balance": account.balance
                })
            
            return {
                "success": True,
                "accounts": accounts_status
            }
            
        except Exception as e:
            return {"error": str(e)}
        finally:
            db.close()
    
    def full_account_sync(self, account_id: int) -> Dict:
        """Perform full sync - balance and transactions"""
        # Sync balance first
        balance_result = self.sync_account_balance(account_id)
        if not balance_result.get("success"):
            return balance_result
        
        # Then sync transactions
        transactions_result = self.sync_transactions(account_id)
        if not transactions_result.get("success"):
            return transactions_result
        
        return {
            "success": True,
            "message": "Full account sync completed",
            "balance_sync": balance_result,
            "transactions_sync": transactions_result
        }