import httpx
import json
import os
from typing import Dict, List, Optional
from logging_config import get_logger

logger = get_logger(__name__)

class AAClient:
    """Account Aggregator client for fetching financial data"""
    
    def __init__(self):
        self.base_url = os.getenv("AA_BASE_URL", "https://sandbox.setu.co/api")
        self.api_key = os.getenv("AA_API_KEY")
        self.client_id = os.getenv("AA_CLIENT_ID")
        
    async def initiate_consent(self, user_id: str, accounts: List[str]) -> Dict:
        """Initiate consent request for account data"""
        try:
            async with httpx.AsyncClient() as client:
                payload = {
                    "userId": user_id,
                    "accounts": accounts,
                    "dataRange": {
                        "from": "2024-01-01",
                        "to": "2024-12-31"
                    }
                }
                
                response = await client.post(
                    f"{self.base_url}/consent",
                    json=payload,
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                
                if response.status_code == 200:
                    logger.info("Consent initiated successfully")
                    return response.json()
                else:
                    logger.error(f"Consent initiation failed: {response.text}")
                    return {"error": "Consent initiation failed"}
                    
        except Exception as e:
            logger.error(f"Error initiating consent: {str(e)}")
            return {"error": str(e)}
    
    async def check_status(self, consent_id: str) -> Dict:
        """Check consent status"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/consent/{consent_id}/status",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"Status check failed: {response.text}")
                    return {"error": "Status check failed"}
                    
        except Exception as e:
            logger.error(f"Error checking status: {str(e)}")
            return {"error": str(e)}
    
    async def fetch_data(self, consent_id: str) -> Dict:
        """Fetch transaction data using consent"""
        try:
            # For demo purposes, return mock transaction data
            # In production, this would make actual API calls to AA
            mock_transactions = {
                "transactions": [
                    {"date": "2024-01-15", "amount": -2500, "description": "ZOMATO ONLINE ORDER", "type": "debit"},
                    {"date": "2024-01-16", "amount": -1200, "description": "UBER RIDE", "type": "debit"},
                    {"date": "2024-01-17", "amount": -15000, "description": "RENT PAYMENT", "type": "debit"},
                    {"date": "2024-01-18", "amount": 50000, "description": "SALARY CREDIT", "type": "credit"},
                    {"date": "2024-01-20", "amount": -3500, "description": "GROCERY STORE", "type": "debit"},
                    {"date": "2024-01-22", "amount": -800, "description": "NETFLIX SUBSCRIPTION", "type": "debit"},
                    {"date": "2024-01-25", "amount": -4500, "description": "SWIGGY ORDER", "type": "debit"},
                    {"date": "2024-01-28", "amount": -2000, "description": "ELECTRICITY BILL", "type": "debit"},
                    {"date": "2024-02-01", "amount": -5000, "description": "SHOPPING MALL", "type": "debit"},
                    {"date": "2024-02-05", "amount": -1500, "description": "MOVIE TICKETS", "type": "debit"}
                ]
            }
            
            logger.info(f"Fetched {len(mock_transactions['transactions'])} transactions")
            return mock_transactions
            
        except Exception as e:
            logger.error(f"Error fetching data: {str(e)}")
            return {"error": str(e)}