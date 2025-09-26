import json
import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.fiu_models import User, BankAccount, Transaction, BudgetAnalysis, SessionLocal
from app.demo_crew import DemoBudgetPlanner
from app.bank_validator import BankValidator
from typing import List, Dict, Optional

class FIUService:
    """Financial Information User service for managing accounts and transactions"""
    
    def __init__(self):
        self.budget_planner = DemoBudgetPlanner()
    
    def create_user(self, name: str, email: str, phone: str) -> Dict:
        """Create a new user account"""
        db = SessionLocal()
        try:
            # Check if user exists
            existing_user = db.query(User).filter(
                (User.email == email) | (User.phone == phone)
            ).first()
            
            if existing_user:
                return {"error": "User already exists with this email or phone"}
            
            # Create new user
            user = User(name=name, email=email, phone=phone)
            db.add(user)
            db.commit()
            db.refresh(user)
            
            return {
                "success": True,
                "user_id": user.user_id,
                "message": "User created successfully"
            }
        except Exception as e:
            db.rollback()
            return {"error": str(e)}
        finally:
            db.close()
    
    def add_bank_account(self, user_id: str, account_number: str, bank_name: str, 
                        account_type: str, ifsc_code: str, account_holder_name: str,
                        initial_balance: float = 0.0) -> Dict:
        """Add validated bank account for user"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.user_id == user_id).first()
            if not user:
                return {"error": "User not found"}
            
            # Validate bank details
            validation_result = BankValidator.validate_bank_details(
                account_number, ifsc_code, account_holder_name, account_type
            )
            
            if not validation_result['valid']:
                return {
                    "error": "Invalid bank details",
                    "validation_errors": validation_result['errors']
                }
            
            # Use clean account number from validation
            clean_account_number = validation_result['clean_account']
            
            # Check if account already exists
            existing_account = db.query(BankAccount).filter(
                BankAccount.account_number == clean_account_number
            ).first()
            
            if existing_account:
                return {"error": "Account already exists"}
            
            # Get validated bank info
            bank_info = validation_result['bank_info']
            validated_bank_name = bank_info['bank_name']
            
            # Create bank account
            is_primary = len(user.bank_accounts) == 0  # First account is primary
            
            bank_account = BankAccount(
                user_id=user.id,
                account_number=clean_account_number,
                account_holder_name=account_holder_name.strip().title(),
                bank_name=validated_bank_name,
                account_type=account_type.lower(),
                ifsc_code=ifsc_code.upper(),
                balance=initial_balance,
                is_primary=is_primary,
                is_synced=False
            )
            
            db.add(bank_account)
            db.commit()
            
            result = {
                "success": True,
                "message": "Bank account added and verified successfully",
                "account_id": bank_account.id,
                "validated_bank_name": validated_bank_name,
                "clean_account_number": clean_account_number
            }
            
            if validation_result.get('warnings'):
                result['warnings'] = validation_result['warnings']
            
            return result
            
        except Exception as e:
            db.rollback()
            return {"error": str(e)}
        finally:
            db.close()
    
    def get_user_accounts(self, user_id: str) -> List[Dict]:
        """Get all bank accounts for a user"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.user_id == user_id).first()
            if not user:
                return []
            
            accounts = []
            for account in user.bank_accounts:
                accounts.append({
                    "id": account.id,
                    "account_number": account.account_number,
                    "bank_name": account.bank_name,
                    "account_type": account.account_type,
                    "balance": account.balance,
                    "ifsc_code": account.ifsc_code,
                    "is_primary": account.is_primary
                })
            
            return accounts
        finally:
            db.close()
    
    def transfer_money(self, user_id: str, from_account: str, to_account: str, 
                      amount: float, description: str = "") -> Dict:
        """Transfer money between accounts"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.user_id == user_id).first()
            if not user:
                return {"error": "User not found"}
            
            # Get sender account
            sender_account = db.query(BankAccount).filter(
                BankAccount.account_number == from_account,
                BankAccount.user_id == user.id
            ).first()
            
            if not sender_account:
                return {"error": "Sender account not found"}
            
            if sender_account.balance < amount:
                return {"error": "Insufficient balance"}
            
            # Create debit transaction for sender
            debit_tx = Transaction(
                user_id=user.id,
                from_account=from_account,
                to_account=to_account,
                amount=amount,
                transaction_type="debit",
                category="transfer",
                description=f"Transfer to {to_account}: {description}",
                masumi_tx_hash=str(uuid.uuid4())  # Simulate Masumi transaction
            )
            
            # Update sender balance
            sender_account.balance -= amount
            
            # Check if receiver account exists in our system
            receiver_account = db.query(BankAccount).filter(
                BankAccount.account_number == to_account
            ).first()
            
            if receiver_account:
                # Internal transfer - create credit transaction for receiver
                credit_tx = Transaction(
                    user_id=receiver_account.user_id,
                    from_account=from_account,
                    to_account=to_account,
                    amount=amount,
                    transaction_type="credit",
                    category="transfer",
                    description=f"Transfer from {from_account}: {description}",
                    masumi_tx_hash=debit_tx.masumi_tx_hash
                )
                receiver_account.balance += amount
                db.add(credit_tx)
            
            db.add(debit_tx)
            db.commit()
            
            return {
                "success": True,
                "transaction_id": debit_tx.transaction_id,
                "masumi_tx_hash": debit_tx.masumi_tx_hash,
                "message": "Transfer completed successfully"
            }
        except Exception as e:
            db.rollback()
            return {"error": str(e)}
        finally:
            db.close()
    
    def add_income(self, user_id: str, account_number: str, amount: float, 
                  source: str, description: str = "", category: str = "salary") -> Dict:
        """Add validated income to account"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.user_id == user_id).first()
            if not user:
                return {"error": "User not found"}
            
            account = db.query(BankAccount).filter(
                BankAccount.account_number == account_number,
                BankAccount.user_id == user.id
            ).first()
            
            if not account:
                return {"error": "Account not found"}
            
            # Validate transaction limits
            limit_check = BankValidator.validate_transaction_limits(
                amount, 'deposit', account.account_type
            )
            
            if not limit_check['valid']:
                return {"error": limit_check['error']}
            
            # Validate income categories
            valid_income_categories = [
                'salary', 'business', 'freelance', 'investment', 'rental', 
                'pension', 'bonus', 'commission', 'dividend', 'interest', 'other'
            ]
            
            if category.lower() not in valid_income_categories:
                category = 'other'
            
            # Create credit transaction
            transaction = Transaction(
                user_id=user.id,
                from_account=source,
                to_account=account_number,
                amount=amount,
                transaction_type="credit",
                category="income",
                description=f"{category.title()} from {source}: {description}",
                masumi_tx_hash=str(uuid.uuid4())
            )
            
            # Update balance
            account.balance += amount
            
            db.add(transaction)
            db.commit()
            
            result = {
                "success": True,
                "transaction_id": transaction.transaction_id,
                "new_balance": account.balance,
                "masumi_tx_hash": transaction.masumi_tx_hash
            }
            
            if limit_check.get('warnings'):
                result['warnings'] = limit_check['warnings']
            
            return result
            
        except Exception as e:
            db.rollback()
            return {"error": str(e)}
        finally:
            db.close()
    
    def add_expense(self, user_id: str, account_number: str, amount: float, 
                   category: str, description: str = "", merchant: str = "") -> Dict:
        """Add validated expense from account"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.user_id == user_id).first()
            if not user:
                return {"error": "User not found"}
            
            account = db.query(BankAccount).filter(
                BankAccount.account_number == account_number,
                BankAccount.user_id == user.id
            ).first()
            
            if not account:
                return {"error": "Account not found"}
            
            if account.balance < amount:
                return {
                    "error": f"Insufficient balance. Available: Rs.{account.balance:,.2f}, Required: Rs.{amount:,.2f}"
                }
            
            # Validate transaction limits
            limit_check = BankValidator.validate_transaction_limits(
                amount, 'withdrawal', account.account_type
            )
            
            if not limit_check['valid']:
                return {"error": limit_check['error']}
            
            # Validate expense categories
            valid_expense_categories = [
                'food', 'transport', 'shopping', 'bills', 'entertainment', 
                'healthcare', 'education', 'rent', 'groceries', 'fuel',
                'clothing', 'electronics', 'travel', 'insurance', 'loan_emi',
                'investment', 'charity', 'gifts', 'maintenance', 'other'
            ]
            
            if category.lower() not in valid_expense_categories:
                category = 'other'
            
            # Create debit transaction
            merchant_info = f" at {merchant}" if merchant else ""
            transaction = Transaction(
                user_id=user.id,
                from_account=account_number,
                to_account=f"{category}{merchant_info}",
                amount=amount,
                transaction_type="debit",
                category="expense",
                description=f"{category.title()}{merchant_info}: {description}",
                masumi_tx_hash=str(uuid.uuid4())
            )
            
            # Update balance
            account.balance -= amount
            
            db.add(transaction)
            db.commit()
            
            result = {
                "success": True,
                "transaction_id": transaction.transaction_id,
                "new_balance": account.balance,
                "masumi_tx_hash": transaction.masumi_tx_hash,
                "expense_category": category.title()
            }
            
            if limit_check.get('warnings'):
                result['warnings'] = limit_check['warnings']
            
            return result
            
        except Exception as e:
            db.rollback()
            return {"error": str(e)}
        finally:
            db.close()
    
    def get_transaction_history(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get transaction history for user"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.user_id == user_id).first()
            if not user:
                return []
            
            transactions = db.query(Transaction).filter(
                Transaction.user_id == user.id
            ).order_by(Transaction.created_at.desc()).limit(limit).all()
            
            history = []
            for tx in transactions:
                history.append({
                    "transaction_id": tx.transaction_id,
                    "from_account": tx.from_account,
                    "to_account": tx.to_account,
                    "amount": tx.amount,
                    "type": tx.transaction_type,
                    "category": tx.category,
                    "description": tx.description,
                    "status": tx.status,
                    "masumi_tx_hash": tx.masumi_tx_hash,
                    "date": tx.created_at.isoformat()
                })
            
            return history
        finally:
            db.close()
    
    def get_balance(self, user_id: str, account_number: str = None) -> Dict:
        """Get account balance(s)"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.user_id == user_id).first()
            if not user:
                return {"error": "User not found"}
            
            if account_number:
                # Get specific account balance
                account = db.query(BankAccount).filter(
                    BankAccount.account_number == account_number,
                    BankAccount.user_id == user.id
                ).first()
                
                if not account:
                    return {"error": "Account not found"}
                
                return {
                    "account_number": account.account_number,
                    "balance": account.balance,
                    "bank_name": account.bank_name
                }
            else:
                # Get all account balances
                balances = []
                total_balance = 0
                
                for account in user.bank_accounts:
                    balances.append({
                        "account_number": account.account_number,
                        "balance": account.balance,
                        "bank_name": account.bank_name,
                        "is_primary": account.is_primary
                    })
                    total_balance += account.balance
                
                return {
                    "accounts": balances,
                    "total_balance": total_balance
                }
        finally:
            db.close()
    
    def generate_budget_analysis(self, user_id: str) -> Dict:
        """Generate AI-powered budget analysis"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.user_id == user_id).first()
            if not user:
                return {"error": "User not found"}
            
            # Get transactions from last 30 days
            thirty_days_ago = datetime.now() - timedelta(days=30)
            transactions = db.query(Transaction).filter(
                Transaction.user_id == user.id,
                Transaction.created_at >= thirty_days_ago
            ).all()
            
            if not transactions:
                return {"error": "No transactions found for analysis"}
            
            # Convert transactions to format expected by budget planner
            transaction_data = {
                "transactions": []
            }
            
            for tx in transactions:
                transaction_data["transactions"].append({
                    "date": tx.created_at.strftime("%Y-%m-%d"),
                    "amount": tx.amount if tx.transaction_type == "credit" else -tx.amount,
                    "description": tx.description,
                    "type": tx.transaction_type
                })
            
            # Generate budget analysis using AI
            budget_report = self.budget_planner.process_transactions(json.dumps(transaction_data))
            
            # Calculate key metrics
            income_txs = [tx for tx in transactions if tx.transaction_type == "credit" and tx.category == "income"]
            expense_txs = [tx for tx in transactions if tx.transaction_type == "debit" and tx.category == "expense"]
            
            total_income = sum(tx.amount for tx in income_txs)
            total_expenses = sum(tx.amount for tx in expense_txs)
            savings_rate = ((total_income - total_expenses) / total_income * 100) if total_income > 0 else 0
            
            # Save analysis to database
            analysis = BudgetAnalysis(
                user_id=user.id,
                analysis_data=budget_report,
                total_income=total_income,
                total_expenses=total_expenses,
                savings_rate=savings_rate,
                recommendations=budget_report
            )
            
            db.add(analysis)
            db.commit()
            
            return {
                "success": True,
                "budget_report": budget_report,
                "total_income": total_income,
                "total_expenses": total_expenses,
                "savings_rate": savings_rate,
                "analysis_id": analysis.id
            }
        except Exception as e:
            db.rollback()
            return {"error": str(e)}
        finally:
            db.close()