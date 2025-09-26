import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List
from app.fiu_models import create_tables
from app.fiu_services_extended import ExtendedFIUService
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(
    title="FIU Platform - AI-Powered Financial Management",
    description="Complete Financial Information User platform with Masumi integration and AI budget analysis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database and services
create_tables()
fiu_service = ExtendedFIUService()

# Pydantic models for API requests
class UserCreate(BaseModel):
    name: str
    email: str
    phone: str

class BankAccountCreate(BaseModel):
    user_id: str
    account_number: str
    bank_name: str
    account_type: str
    ifsc_code: str
    account_holder_name: str
    initial_balance: float = 0.0

class TransferRequest(BaseModel):
    user_id: str
    from_account: str
    to_account: str
    amount: float
    description: str = ""

class IncomeRequest(BaseModel):
    user_id: str
    account_number: str
    amount: float
    source: str
    description: str = ""

class ExpenseRequest(BaseModel):
    user_id: str
    account_number: str
    amount: float
    category: str
    description: str = ""

class BudgetAnalysisRequest(BaseModel):
    user_id: str

# API Endpoints

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    """Serve the FIU platform dashboard"""
    with open("fiu_dashboard.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/users/create")
async def create_user(user_data: UserCreate):
    """Create a new user account"""
    result = fiu_service.create_user(user_data.name, user_data.email, user_data.phone)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/api/accounts/add")
async def add_bank_account(account_data: BankAccountCreate):
    """Add bank account for user"""
    result = fiu_service.add_bank_account(
        account_data.user_id,
        account_data.account_number,
        account_data.bank_name,
        account_data.account_type,
        account_data.ifsc_code,
        account_data.account_holder_name,
        account_data.initial_balance
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/api/accounts/{user_id}")
async def get_user_accounts(user_id: str):
    """Get all bank accounts for a user"""
    accounts = fiu_service.get_user_accounts(user_id)
    return {"accounts": accounts}

@app.post("/api/transfer")
async def transfer_money(transfer_data: TransferRequest):
    """Transfer money between accounts"""
    result = fiu_service.transfer_money(
        transfer_data.user_id,
        transfer_data.from_account,
        transfer_data.to_account,
        transfer_data.amount,
        transfer_data.description
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/api/income/add")
async def add_income(income_data: IncomeRequest):
    """Add income to account"""
    result = fiu_service.add_income(
        income_data.user_id,
        income_data.account_number,
        income_data.amount,
        income_data.source,
        income_data.description
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/api/expense/add")
async def add_expense(expense_data: ExpenseRequest):
    """Add expense from account"""
    result = fiu_service.add_expense(
        expense_data.user_id,
        expense_data.account_number,
        expense_data.amount,
        expense_data.category,
        expense_data.description
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/api/balance/{user_id}")
async def get_balance(user_id: str, account_number: Optional[str] = None):
    """Get account balance(s)"""
    result = fiu_service.get_balance(user_id, account_number)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.get("/api/transactions/{user_id}")
async def get_transaction_history(user_id: str, limit: int = 50):
    """Get transaction history for user"""
    transactions = fiu_service.get_transaction_history(user_id, limit)
    return {"transactions": transactions}

@app.post("/api/budget/analyze")
async def generate_budget_analysis(request: BudgetAnalysisRequest):
    """Generate AI-powered budget analysis"""
    result = fiu_service.generate_budget_analysis(request.user_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/api/banks/supported")
async def get_supported_banks():
    """Get list of supported banks"""
    banks = fiu_service.get_supported_banks()
    return {"banks": banks}

@app.post("/api/banks/validate")
async def validate_bank_details(request: dict):
    """Validate bank details without saving"""
    result = fiu_service.validate_bank_details_only(
        request.get('account_number', ''),
        request.get('ifsc_code', ''),
        request.get('account_holder_name', ''),
        request.get('account_type', 'savings')
    )
    return result

@app.get("/api/categories/expense")
async def get_expense_categories():
    """Get valid expense categories"""
    categories = fiu_service.get_expense_categories()
    return {"categories": categories}

@app.get("/api/categories/income")
async def get_income_categories():
    """Get valid income categories"""
    categories = fiu_service.get_income_categories()
    return {"categories": categories}

@app.post("/api/accounts/{account_id}/sync/balance")
async def sync_account_balance(account_id: int):
    """Sync account balance from bank"""
    result = fiu_service.sync_account_balance(account_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/api/accounts/{account_id}/sync/transactions")
async def sync_account_transactions(account_id: int, days: int = 30):
    """Sync transactions from bank"""
    result = fiu_service.sync_account_transactions(account_id, days)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/api/accounts/{account_id}/sync/full")
async def full_account_sync(account_id: int):
    """Perform full account sync"""
    result = fiu_service.full_account_sync(account_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/api/sync/status/{user_id}")
async def get_sync_status(user_id: str):
    """Get sync status for user accounts"""
    result = fiu_service.get_sync_status(user_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "FIU Platform"}

def find_free_port():
    """Find a free port to run the server"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

if __name__ == "__main__":
    port = int(os.getenv('FIU_PORT', find_free_port()))
    print(f"Starting FIU Platform on port {port}...")
    print(f"Dashboard: http://localhost:{port}")
    print(f"API Documentation: http://localhost:{port}/docs")
    uvicorn.run(app, host="0.0.0.0", port=port)