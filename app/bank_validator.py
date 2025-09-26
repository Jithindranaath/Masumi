import re
from typing import Dict, List, Optional

class BankValidator:
    """Validates bank account details for legitimacy"""
    
    # Indian bank IFSC code patterns and bank details
    BANK_DATA = {
        'SBIN': {'name': 'State Bank of India', 'pattern': r'^SBIN0\d{6}$'},
        'HDFC': {'name': 'HDFC Bank', 'pattern': r'^HDFC0\d{6}$'},
        'ICIC': {'name': 'ICICI Bank', 'pattern': r'^ICIC0\d{6}$'},
        'AXIS': {'name': 'Axis Bank', 'pattern': r'^UTIB0\d{6}$'},
        'PUNB': {'name': 'Punjab National Bank', 'pattern': r'^PUNB0\d{6}$'},
        'CNRB': {'name': 'Canara Bank', 'pattern': r'^CNRB0\d{6}$'},
        'UBIN': {'name': 'Union Bank of India', 'pattern': r'^UBIN0\d{6}$'},
        'BARB': {'name': 'Bank of Baroda', 'pattern': r'^BARB0\d{6}$'},
        'IOBA': {'name': 'Indian Overseas Bank', 'pattern': r'^IOBA0\d{6}$'},
        'CORP': {'name': 'Corporation Bank', 'pattern': r'^CORP0\d{6}$'},
        'YESB': {'name': 'Yes Bank', 'pattern': r'^YESB0\d{6}$'},
        'KKBK': {'name': 'Kotak Mahindra Bank', 'pattern': r'^KKBK0\d{6}$'},
        'INDB': {'name': 'IndusInd Bank', 'pattern': r'^INDB0\d{6}$'},
        'FDRL': {'name': 'Federal Bank', 'pattern': r'^FDRL0\d{6}$'},
        'KARB': {'name': 'Karnataka Bank', 'pattern': r'^KARB0\d{6}$'},
        'SCBL': {'name': 'Standard Chartered Bank', 'pattern': r'^SCBL0\d{6}$'},
        'CITI': {'name': 'Citibank', 'pattern': r'^CITI0\d{6}$'},
        'HSBC': {'name': 'HSBC Bank', 'pattern': r'^HSBC0\d{6}$'},
        'DBSS': {'name': 'DBS Bank', 'pattern': r'^DBSS0\d{6}$'},
        'ALLA': {'name': 'Allahabad Bank', 'pattern': r'^ALLA0\d{6}$'}
    }
    
    # Account number patterns by bank
    ACCOUNT_PATTERNS = {
        'SBIN': [r'^\d{11}$', r'^\d{17}$'],  # 11 or 17 digits
        'HDFC': [r'^\d{14}$'],  # 14 digits
        'ICIC': [r'^\d{12}$'],  # 12 digits
        'AXIS': [r'^\d{15,18}$'],  # 15-18 digits
        'PUNB': [r'^\d{13}$'],  # 13 digits
        'CNRB': [r'^\d{13}$'],  # 13 digits
        'UBIN': [r'^\d{15}$'],  # 15 digits
        'BARB': [r'^\d{14}$'],  # 14 digits
        'YESB': [r'^\d{15,18}$'],  # 15-18 digits
        'KKBK': [r'^\d{16}$'],  # 16 digits
        'default': [r'^\d{9,18}$']  # 9-18 digits for others
    }
    
    @classmethod
    def validate_ifsc(cls, ifsc_code: str) -> Dict:
        """Validate IFSC code format and return bank details"""
        if not ifsc_code or len(ifsc_code) != 11:
            return {'valid': False, 'error': 'IFSC code must be 11 characters'}
        
        ifsc_code = ifsc_code.upper()
        
        # Check basic format: 4 letters + 0 + 6 digits
        if not re.match(r'^[A-Z]{4}0[A-Z0-9]{6}$', ifsc_code):
            return {'valid': False, 'error': 'Invalid IFSC format. Should be: BANK0XXXXXX'}
        
        bank_code = ifsc_code[:4]
        
        # Check if bank exists in our database
        if bank_code in cls.BANK_DATA:
            bank_info = cls.BANK_DATA[bank_code]
            if re.match(bank_info['pattern'], ifsc_code):
                return {
                    'valid': True,
                    'bank_name': bank_info['name'],
                    'bank_code': bank_code,
                    'branch_code': ifsc_code[5:]
                }
        
        # If not in our database, check basic format
        return {
            'valid': True,
            'bank_name': f'Bank ({bank_code})',
            'bank_code': bank_code,
            'branch_code': ifsc_code[5:],
            'warning': 'Bank not in our database, but format is valid'
        }
    
    @classmethod
    def validate_account_number(cls, account_number: str, bank_code: str = None) -> Dict:
        """Validate account number format"""
        if not account_number:
            return {'valid': False, 'error': 'Account number is required'}
        
        # Remove spaces and special characters
        clean_account = re.sub(r'[^0-9]', '', account_number)
        
        if not clean_account:
            return {'valid': False, 'error': 'Account number must contain digits'}
        
        # Check length (minimum 9, maximum 18 digits)
        if len(clean_account) < 9 or len(clean_account) > 18:
            return {'valid': False, 'error': 'Account number must be 9-18 digits'}
        
        # Bank-specific validation
        if bank_code and bank_code in cls.ACCOUNT_PATTERNS:
            patterns = cls.ACCOUNT_PATTERNS[bank_code]
            valid_pattern = any(re.match(pattern, clean_account) for pattern in patterns)
            if not valid_pattern:
                return {
                    'valid': False, 
                    'error': f'Invalid account number format for {cls.BANK_DATA.get(bank_code, {}).get("name", bank_code)}'
                }
        
        return {'valid': True, 'clean_account': clean_account}
    
    @classmethod
    def validate_bank_details(cls, account_number: str, ifsc_code: str, 
                            account_holder_name: str, account_type: str = 'savings') -> Dict:
        """Comprehensive bank details validation"""
        result = {'valid': True, 'errors': [], 'warnings': []}
        
        # Validate IFSC
        ifsc_result = cls.validate_ifsc(ifsc_code)
        if not ifsc_result['valid']:
            result['valid'] = False
            result['errors'].append(ifsc_result['error'])
        else:
            result['bank_info'] = ifsc_result
            if 'warning' in ifsc_result:
                result['warnings'].append(ifsc_result['warning'])
        
        # Validate account number
        if result['valid']:  # Only if IFSC is valid
            bank_code = ifsc_result.get('bank_code')
            account_result = cls.validate_account_number(account_number, bank_code)
            if not account_result['valid']:
                result['valid'] = False
                result['errors'].append(account_result['error'])
            else:
                result['clean_account'] = account_result['clean_account']
        
        # Validate account holder name
        if not account_holder_name or len(account_holder_name.strip()) < 2:
            result['valid'] = False
            result['errors'].append('Account holder name must be at least 2 characters')
        elif not re.match(r'^[A-Za-z\s\.]+$', account_holder_name.strip()):
            result['valid'] = False
            result['errors'].append('Account holder name can only contain letters, spaces, and dots')
        
        # Validate account type
        valid_types = ['savings', 'current', 'salary', 'fixed_deposit', 'recurring_deposit']
        if account_type.lower() not in valid_types:
            result['valid'] = False
            result['errors'].append(f'Account type must be one of: {", ".join(valid_types)}')
        
        return result
    
    @classmethod
    def get_bank_list(cls) -> List[Dict]:
        """Get list of supported banks"""
        banks = []
        for code, info in cls.BANK_DATA.items():
            banks.append({
                'code': code,
                'name': info['name'],
                'ifsc_format': f'{code}0XXXXXX'
            })
        return sorted(banks, key=lambda x: x['name'])
    
    @classmethod
    def suggest_ifsc_format(cls, bank_name: str) -> Optional[str]:
        """Suggest IFSC format based on bank name"""
        bank_name_lower = bank_name.lower()
        
        for code, info in cls.BANK_DATA.items():
            if bank_name_lower in info['name'].lower():
                return f'{code}0XXXXXX'
        
        return None
    
    @classmethod
    def validate_transaction_limits(cls, amount: float, transaction_type: str, 
                                  account_type: str = 'savings') -> Dict:
        """Validate transaction limits based on account type and regulations"""
        result = {'valid': True, 'warnings': []}
        
        # Basic amount validation
        if amount <= 0:
            return {'valid': False, 'error': 'Amount must be greater than 0'}
        
        # Daily transaction limits (as per RBI guidelines)
        daily_limits = {
            'savings': {
                'withdrawal': 50000,
                'transfer': 200000,
                'deposit': 1000000
            },
            'current': {
                'withdrawal': 100000,
                'transfer': 500000,
                'deposit': 5000000
            },
            'salary': {
                'withdrawal': 75000,
                'transfer': 300000,
                'deposit': 2000000
            }
        }
        
        limits = daily_limits.get(account_type, daily_limits['savings'])
        limit = limits.get(transaction_type, 50000)
        
        if amount > limit:
            result['warnings'].append(
                f'Amount exceeds daily {transaction_type} limit of Rs.{limit:,} for {account_type} account'
            )
        
        # High-value transaction warnings
        if amount >= 200000:
            result['warnings'].append('High-value transaction may require additional verification')
        
        if amount >= 1000000:
            result['warnings'].append('Transaction above Rs.10 lakh may be reported to financial authorities')
        
        return result