from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class BudgetReport(Base):
    __tablename__ = "budget_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    report_data = Column(Text)
    total_income = Column(Float)
    total_expenses = Column(Float)
    savings_rate = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Database setup
DATABASE_URL = "sqlite:///./budget_planner.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)