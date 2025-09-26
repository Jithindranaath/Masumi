import json
import pandas as pd
from typing import Dict
from logging_config import get_logger

logger = get_logger(__name__)

class DemoBudgetPlanner:
    """Demo budget planner that works without OpenAI API"""
    
    def __init__(self, verbose=True, logger=None):
        self.verbose = verbose
        self.logger = logger or get_logger(__name__)
        self.logger.info("DemoBudgetPlanner initialized")

    def process_transactions(self, transactions_data: str) -> str:
        """Process transactions and generate budget report"""
        try:
            # Parse transaction data
            data = json.loads(transactions_data)
            transactions = data.get('transactions', [])
            
            # Step 1: Categorize transactions
            categorized = self._categorize_transactions(transactions)
            
            # Step 2: Analyze financial data
            analysis = self._analyze_finances(categorized)
            
            # Step 3: Create budget strategy
            strategy = self._create_budget_strategy(analysis)
            
            # Step 4: Generate final report
            report = self._generate_report(analysis, strategy)
            
            return report
            
        except Exception as e:
            logger.error(f"Error processing transactions: {str(e)}")
            return f"Error processing transactions: {str(e)}"
    
    def _categorize_transactions(self, transactions):
        """Categorize transactions into budget categories"""
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
        
        for txn in transactions:
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
        
        return categorized
    
    def _analyze_finances(self, categorized):
        """Analyze categorized financial data"""
        df = pd.DataFrame(categorized)
        
        # Calculate key metrics
        income = df[df['type'] == 'credit']['amount'].sum()
        expenses = df[df['type'] == 'debit']['amount'].sum()
        savings_rate = ((income - expenses) / income * 100) if income > 0 else 0
        
        # Category breakdown
        expense_breakdown = df[df['type'] == 'debit'].groupby('category')['amount'].sum()
        
        # Recurring payments
        recurring = df[df['category'].isin(['Subscriptions', 'Utilities', 'Rent/Mortgage'])]
        
        # Top expenses
        top_expenses = df[df['type'] == 'debit'].nlargest(5, 'amount')
        
        return {
            'total_income': float(income),
            'total_expenses': float(expenses),
            'savings_rate': float(savings_rate),
            'expense_breakdown': expense_breakdown.to_dict(),
            'recurring_payments': recurring[['description', 'amount', 'category']].to_dict('records'),
            'top_expenses': top_expenses[['description', 'amount', 'category']].to_dict('records')
        }
    
    def _create_budget_strategy(self, analysis):
        """Create budget recommendations using 50/30/20 rule"""
        income = analysis['total_income']
        
        # 50/30/20 rule
        needs_budget = income * 0.5  # 50% for needs
        wants_budget = income * 0.3  # 30% for wants
        savings_budget = income * 0.2  # 20% for savings
        
        # Category recommendations
        recommendations = {
            'needs_budget': needs_budget,
            'wants_budget': wants_budget,
            'savings_budget': savings_budget,
            'insights': []
        }
        
        # Generate insights
        if analysis['savings_rate'] < 20:
            recommendations['insights'].append(
                f"Your current savings rate is {analysis['savings_rate']:.1f}%. "
                f"Try to increase it to 20% by saving Rs.{savings_budget - (analysis['total_income'] - analysis['total_expenses']):.0f} more per month."
            )
        
        # Check subscription spending
        subscription_spending = sum([
            amount for cat, amount in analysis['expense_breakdown'].items() 
            if 'subscription' in cat.lower()
        ])
        if subscription_spending > 0:
            recommendations['insights'].append(
                f"You're spending Rs.{subscription_spending:.0f} on subscriptions. "
                "Review and cancel unused subscriptions to save money."
            )
        
        # Check dining out spending
        dining_spending = analysis['expense_breakdown'].get('Dining Out', 0)
        if dining_spending > wants_budget * 0.3:
            recommendations['insights'].append(
                f"Your dining out expenses (Rs.{dining_spending:.0f}) are high. "
                f"Consider reducing to Rs.{wants_budget * 0.3:.0f} per month."
            )
        
        return recommendations
    
    def _generate_report(self, analysis, strategy):
        """Generate final user-friendly report"""
        report = f"""
# Your AI-Generated Budget Report

## Financial Summary
- **Total Income**: Rs.{analysis['total_income']:,.0f}
- **Total Expenses**: Rs.{analysis['total_expenses']:,.0f}
- **Net Savings**: Rs.{analysis['total_income'] - analysis['total_expenses']:,.0f}
- **Savings Rate**: {analysis['savings_rate']:.1f}%

## Budget Recommendations (50/30/20 Rule)
- **Needs (50%)**: Rs.{strategy['needs_budget']:,.0f}
- **Wants (30%)**: Rs.{strategy['wants_budget']:,.0f}
- **Savings (20%)**: Rs.{strategy['savings_budget']:,.0f}

## Personalized Insights
"""
        
        for i, insight in enumerate(strategy['insights'], 1):
            report += f"{i}. {insight}\n"
        
        report += f"""
## Spending Breakdown
"""
        
        for category, amount in analysis['expense_breakdown'].items():
            percentage = (amount / analysis['total_expenses']) * 100 if analysis['total_expenses'] > 0 else 0
            report += f"- **{category}**: Rs.{amount:,.0f} ({percentage:.1f}%)\n"
        
        report += f"""
## Recurring Payments
"""
        
        for payment in analysis['recurring_payments']:
            report += f"- {payment['description']}: Rs.{payment['amount']:,.0f}\n"
        
        report += f"""
## Top 5 Expenses
"""
        
        for expense in analysis['top_expenses']:
            report += f"- {expense['description']}: Rs.{expense['amount']:,.0f}\n"
        
        report += f"""
---
*Generated by AI Budget Planner - Your path to financial wellness starts here!*
"""
        
        return report.strip()