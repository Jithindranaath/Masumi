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