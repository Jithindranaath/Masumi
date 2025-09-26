from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_verified = Column(Boolean, default=False)
    
    # Relationships
    bank_accounts = relationship("BankAccount", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")

class BankAccount(Base):
    __tablename__ = "bank_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    account_number = Column(String, unique=True, index=True)
    account_holder_name = Column(String, nullable=False)
    bank_name = Column(String, nullable=False)
    account_type = Column(String, nullable=False)  # savings, current
    balance = Column(Float, default=0.0)
    ifsc_code = Column(String, nullable=False)
    is_primary = Column(Boolean, default=False)
    is_synced = Column(Boolean, default=False)
    last_sync = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="bank_accounts")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.id"))
    from_account = Column(String)
    to_account = Column(String)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)  # credit, debit, transfer
    category = Column(String)  # income, expense, transfer
    description = Column(String)
    status = Column(String, default="completed")  # pending, completed, failed
    masumi_tx_hash = Column(String)  # Masumi blockchain transaction hash
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="transactions")

class BudgetAnalysis(Base):
    __tablename__ = "budget_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    analysis_data = Column(Text)
    total_income = Column(Float)
    total_expenses = Column(Float)
    savings_rate = Column(Float)
    recommendations = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Database setup
DATABASE_URL = "sqlite:///./fiu_platform.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)