from crewai import Agent, Crew, Task, Process
from crewai_tools import BaseTool
import pandas as pd
import json
import re
from typing import Dict, List
from logging_config import get_logger

logger = get_logger(__name__)

class TransactionCategorizerTool(BaseTool):
    name: str = "transaction_categorizer"
    description: str = "Categorizes financial transactions into predefined categories"
    
    def _run(self, transactions_json: str) -> str:
        """Categorize transactions into budget categories"""
        try:
            transactions = json.loads(transactions_json)
            categorized = []
            
            category_rules = {
                'Income': ['salary', 'bonus', 'interest', 'dividend'],
                'Groceries': ['grocery', 'supermarket', 'vegetables', 'fruits'],
                'Utilities': ['electricity', 'water', 'gas', 'internet', 'phone'],
                'Rent/Mortgage': ['rent', 'mortgage', 'housing'],
                'EMI': ['emi', 'loan', 'credit card'],
                'Transport': ['uber', 'ola', 'petrol', 'fuel', 'bus', 'metro'],
                'Dining Out': ['zomato', 'swiggy', 'restaurant', 'food'],
                'Shopping': ['shopping', 'mall', 'amazon', 'flipkart'],
                'Entertainment': ['movie', 'cinema', 'netflix', 'spotify', 'games'],
                'Subscriptions': ['subscription', 'netflix', 'spotify', 'prime'],
                'Miscellaneous': []
            }
            
            for txn in transactions.get('transactions', []):
                description = txn['description'].lower()
                category = 'Miscellaneous'
                
                for cat, keywords in category_rules.items():
                    if any(keyword in description for keyword in keywords):
                        category = cat
                        break
                
                # Special handling for income
                if txn['type'] == 'credit' and txn['amount'] > 10000:
                    category = 'Income'
                
                categorized.append({
                    'date': txn['date'],
                    'amount': abs(txn['amount']),
                    'description': txn['description'],
                    'category': category,
                    'type': txn['type']
                })
            
            df = pd.DataFrame(categorized)
            return df.to_csv(index=False)
            
        except Exception as e:
            logger.error(f"Error categorizing transactions: {str(e)}")
            return f"Error: {str(e)}"

class FinancialAnalysisTool(BaseTool):
    name: str = "financial_analyzer"
    description: str = "Analyzes categorized financial data for insights"
    
    def _run(self, categorized_csv: str) -> str:
        """Analyze financial data and generate insights"""
        try:
            from io import StringIO
            df = pd.read_csv(StringIO(categorized_csv))
            
            # Calculate key metrics
            income = df[df['type'] == 'credit']['amount'].sum()
            expenses = df[df['type'] == 'debit']['amount'].sum()
            savings_rate = ((income - expenses) / income * 100) if income > 0 else 0
            
            # Category breakdown
            expense_breakdown = df[df['type'] == 'debit'].groupby('category')['amount'].sum()
            expense_percentages = (expense_breakdown / expenses * 100).round(2)
            
            # Recurring payments (simplified detection)
            recurring = df[df['category'].isin(['Subscriptions', 'Utilities', 'Rent/Mortgage'])]
            
            # Top expenses
            top_expenses = df[df['type'] == 'debit'].nlargest(5, 'amount')[['description', 'amount', 'category']]
            
            analysis = {
                'total_income': float(income),
                'total_expenses': float(expenses),
                'savings_rate': float(savings_rate),
                'expense_breakdown': expense_breakdown.to_dict(),
                'expense_percentages': expense_percentages.to_dict(),
                'recurring_payments': recurring[['description', 'amount', 'category']].to_dict('records'),
                'top_expenses': top_expenses.to_dict('records')
            }
            
            return json.dumps(analysis, indent=2)
            
        except Exception as e:
            logger.error(f"Error analyzing financial data: {str(e)}")
            return f"Error: {str(e)}"

class BudgetPlannerCrew:
    def __init__(self, verbose=True, logger=None):
        self.verbose = verbose
        self.logger = logger or get_logger(__name__)
        self.crew = self.create_crew()
        self.logger.info("BudgetPlannerCrew initialized")

    def create_crew(self):
        self.logger.info("Creating budget planner crew with agents")
        
        # Agent 1: Transaction Categorizer
        categorizer = Agent(
            role='Transaction Categorizer',
            goal='Transform raw transaction data into clean, categorized financial records',
            backstory='Expert at parsing and categorizing financial transactions using intelligent rules and patterns',
            tools=[TransactionCategorizerTool()],
            verbose=self.verbose
        )

        # Agent 2: Financial Analyst
        analyst = Agent(
            role='Financial Analyst',
            goal='Analyze categorized financial data to uncover spending patterns and key metrics',
            backstory='Skilled financial analyst who identifies trends, calculates ratios, and spots financial opportunities',
            tools=[FinancialAnalysisTool()],
            verbose=self.verbose
        )

        # Agent 3: Budget Strategist
        strategist = Agent(
            role='Budget Strategist',
            goal='Create actionable budget recommendations based on financial analysis',
            backstory='Expert budget planner who applies proven budgeting frameworks like 50/30/20 rule to create personalized financial strategies',
            verbose=self.verbose
        )

        # Agent 4: Report Generator
        reporter = Agent(
            role='Report Generator',
            goal='Create user-friendly, encouraging financial reports with actionable insights',
            backstory='Skilled communicator who transforms complex financial data into clear, motivating reports that empower users',
            verbose=self.verbose
        )

        self.logger.info("Created all budget planner agents")

        # Define tasks
        categorize_task = Task(
            description='Categorize the raw transaction data: {transactions_data}',
            expected_output='Clean CSV data with transactions categorized into: Income, Groceries, Utilities, Rent/Mortgage, EMI, Transport, Dining Out, Shopping, Entertainment, Subscriptions, Miscellaneous',
            agent=categorizer
        )

        analyze_task = Task(
            description='Analyze the categorized transaction data to calculate key financial metrics including income, expenses, savings rate, category breakdown, recurring payments, and top expenses',
            expected_output='Structured JSON analysis with total income, total expenses, savings rate, expense breakdown by category, recurring payments list, and top 5 expenses',
            agent=analyst
        )

        strategy_task = Task(
            description='Create budget recommendations using the 50/30/20 rule (50% needs, 30% wants, 20% savings) and provide specific actionable insights based on the financial analysis',
            expected_output='Budget plan with recommended spending limits for each category and at least 3 specific, data-driven insights for improvement',
            agent=strategist
        )

        report_task = Task(
            description='Generate a comprehensive, user-friendly budget report that combines the financial analysis and budget strategy into an encouraging, actionable format',
            expected_output='Final markdown report with financial summary, budget recommendations, and motivating insights written in simple, supportive language',
            agent=reporter
        )

        crew = Crew(
            agents=[categorizer, analyst, strategist, reporter],
            tasks=[categorize_task, analyze_task, strategy_task, report_task],
            process=Process.sequential,
            verbose=self.verbose
        )
        
        self.logger.info("Budget planner crew setup completed")
        return crew