from app.fiu_services import FIUService
from app.bank_validator import BankValidator
from app.bank_sync_service import BankSyncService
from typing import List, Dict

class ExtendedFIUService(FIUService):
    """Extended FIU service with additional validation and sync methods"""
    
    def __init__(self):
        super().__init__()
        self.sync_service = BankSyncService()
    
    def get_supported_banks(self) -> List[Dict]:
        """Get list of supported banks for validation"""
        return BankValidator.get_bank_list()
    
    def validate_bank_details_only(self, account_number: str, ifsc_code: str, 
                                  account_holder_name: str, account_type: str) -> Dict:
        """Validate bank details without saving to database"""
        return BankValidator.validate_bank_details(
            account_number, ifsc_code, account_holder_name, account_type
        )
    
    def get_expense_categories(self) -> List[str]:
        """Get valid expense categories"""
        return [
            'food', 'transport', 'shopping', 'bills', 'entertainment', 
            'healthcare', 'education', 'rent', 'groceries', 'fuel',
            'clothing', 'electronics', 'travel', 'insurance', 'loan_emi',
            'investment', 'charity', 'gifts', 'maintenance', 'other'
        ]
    
    def get_income_categories(self) -> List[str]:
        """Get valid income categories"""
        return [
            'salary', 'business', 'freelance', 'investment', 'rental', 
            'pension', 'bonus', 'commission', 'dividend', 'interest', 'other'
        ]
    
    def sync_account_balance(self, account_id: int) -> Dict:
        """Sync account balance from bank"""
        return self.sync_service.sync_account_balance(account_id)
    
    def sync_account_transactions(self, account_id: int, days: int = 30) -> Dict:
        """Sync transactions from bank"""
        return self.sync_service.sync_transactions(account_id, days)
    
    def get_sync_status(self, user_id: str) -> Dict:
        """Get sync status for user accounts"""
        return self.sync_service.get_sync_status(user_id)
    
    def full_account_sync(self, account_id: int) -> Dict:
        """Perform full account sync"""
        return self.sync_service.full_account_sync(account_id)
    
    def get_detailed_expenses(self, user_id: str, limit: int = 50) -> Dict:
        """Get detailed expenses with purposes and spending reasons"""
        try:
            # Get all transactions for the user
            transactions_result = self.get_transaction_history(user_id, limit * 2)  # Get more to filter expenses
            
            if "error" in transactions_result:
                return transactions_result
            
            transactions = transactions_result["transactions"]
            
            # Filter for expense transactions only
            expenses = [tx for tx in transactions if tx["type"] == "debit" and tx["category"] == "expense"]
            
            # Limit results
            expenses = expenses[:limit]
            
            # Calculate summary statistics
            total_expenses = sum(abs(tx["amount"]) for tx in expenses)
            expense_count = len(expenses)
            avg_expense = total_expenses / expense_count if expense_count > 0 else 0
            
            # Category breakdown
            category_breakdown = {}
            priority_breakdown = {}
            reason_analysis = {}
            merchant_analysis = {}
            payment_method_breakdown = {}
            
            for expense in expenses:
                # Extract category from description or use 'other'
                description = expense.get("description", "")
                category = "other"
                if ":" in description:
                    category = description.split(":")[0].split(" at ")[0].lower()
                
                priority = expense.get("priority", "unknown")
                reason = expense.get("reason", "No reason provided")
                merchant = expense.get("merchant", "Unknown")
                payment_method = expense.get("payment_method", "unknown")
                amount = abs(expense["amount"])
                
                category_breakdown[category] = category_breakdown.get(category, 0) + amount
                priority_breakdown[priority] = priority_breakdown.get(priority, 0) + amount
                payment_method_breakdown[payment_method] = payment_method_breakdown.get(payment_method, 0) + amount
                
                if reason and reason != "No reason provided":
                    reason_analysis[reason] = reason_analysis.get(reason, 0) + amount
                
                if merchant and merchant != "Unknown":
                    merchant_analysis[merchant] = merchant_analysis.get(merchant, 0) + amount
            
            # Find top spending patterns
            top_category = max(category_breakdown.items(), key=lambda x: x[1]) if category_breakdown else ("none", 0)
            top_reason = max(reason_analysis.items(), key=lambda x: x[1]) if reason_analysis else ("none", 0)
            top_merchant = max(merchant_analysis.items(), key=lambda x: x[1]) if merchant_analysis else ("none", 0)
            
            # Separate detailed and simple expenses
            detailed_expenses = [tx for tx in expenses if tx.get("is_detailed", False)]
            simple_expenses = [tx for tx in expenses if not tx.get("is_detailed", False)]
            
            return {
                "expenses": expenses,
                "detailed_expenses": detailed_expenses,
                "simple_expenses": simple_expenses,
                "summary": {
                    "total_expenses": total_expenses,
                    "expense_count": expense_count,
                    "detailed_count": len(detailed_expenses),
                    "simple_count": len(simple_expenses),
                    "average_expense": avg_expense,
                    "top_category": top_category[0],
                    "top_category_amount": top_category[1],
                    "top_reason": top_reason[0],
                    "top_reason_amount": top_reason[1],
                    "top_merchant": top_merchant[0],
                    "top_merchant_amount": top_merchant[1]
                },
                "breakdowns": {
                    "by_category": category_breakdown,
                    "by_priority": priority_breakdown,
                    "by_reason": reason_analysis,
                    "by_merchant": merchant_analysis,
                    "by_payment_method": payment_method_breakdown
                }
            }
            
