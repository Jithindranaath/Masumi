import json
from datetime import datetime
from typing import Dict, List

class DemoBudgetPlanner:
    """Demo budget planner that analyzes user transactions"""
    
    def __init__(self):
        self.expense_categories = {
            'food': 'Food & Dining',
            'transport': 'Transportation', 
            'shopping': 'Shopping',
            'bills': 'Bills & Utilities',
            'rent': 'Rent/Mortgage',
            'entertainment': 'Entertainment',
            'healthcare': 'Healthcare',
            'groceries': 'Groceries',
            'fuel': 'Fuel',
            'other': 'Other'
        }
        
        self.income_categories = {
            'salary': 'Salary',
            'business': 'Business Income',
            'freelance': 'Freelance',
            'investment': 'Investment Returns',
            'rental': 'Rental Income',
            'other': 'Other Income'
        }
    
    def process_transactions(self, transaction_data: str) -> str:
        """Process transactions and generate budget analysis"""
        try:
            data = json.loads(transaction_data)
            transactions = data.get('transactions', [])
            
            if not transactions:
                return self._generate_empty_report()
            
            # Analyze transactions
            analysis = self._analyze_transactions(transactions)
            
            # Generate comprehensive report
            return self._generate_budget_report(analysis)
            
        except Exception as e:
            return f"Error analyzing transactions: {str(e)}"
    
    def _analyze_transactions(self, transactions: List[Dict]) -> Dict:
        """Analyze transaction patterns and calculate metrics"""
        income_total = 0
        expense_total = 0
        expense_breakdown = {}
        income_breakdown = {}
        
        for tx in transactions:
            amount = abs(float(tx.get('amount', 0)))
            tx_type = tx.get('type', 'debit')
            description = tx.get('description', '').lower()
            
            if tx_type == 'credit' or amount > 0:
                # Income transaction
                income_total += amount
                category = self._categorize_income(description)
                income_breakdown[category] = income_breakdown.get(category, 0) + amount
            else:
                # Expense transaction
                expense_total += amount
                category = self._categorize_expense(description)
                expense_breakdown[category] = expense_breakdown.get(category, 0) + amount
        
        # Calculate key metrics
        net_savings = income_total - expense_total
        savings_rate = (net_savings / income_total * 100) if income_total > 0 else 0
        
        # 50/30/20 budget recommendations
        needs_budget = income_total * 0.5
        wants_budget = income_total * 0.3
        savings_budget = income_total * 0.2
        
        return {
            'total_income': income_total,
            'total_expenses': expense_total,
            'net_savings': net_savings,
            'savings_rate': savings_rate,
            'expense_breakdown': expense_breakdown,
            'income_breakdown': income_breakdown,
            'needs_budget': needs_budget,
            'wants_budget': wants_budget,
            'savings_budget': savings_budget,
            'transaction_count': len(transactions)
        }
    
    def _categorize_expense(self, description: str) -> str:
        """Categorize expense based on description"""
        description = description.lower()
        
        # Food & Dining
        if any(word in description for word in ['food', 'restaurant', 'dining', 'swiggy', 'zomato', 'cafe', 'pizza', 'burger']):
            return 'Food & Dining'
        
        # Transportation
        if any(word in description for word in ['uber', 'ola', 'taxi', 'bus', 'metro', 'fuel', 'petrol', 'diesel', 'transport']):
            return 'Transportation'
        
        # Shopping
        if any(word in description for word in ['shopping', 'mall', 'amazon', 'flipkart', 'store', 'purchase']):
            return 'Shopping'
        
        # Bills & Utilities
        if any(word in description for word in ['electricity', 'water', 'gas', 'internet', 'mobile', 'recharge', 'bill']):
            return 'Bills & Utilities'
        
        # Rent/Mortgage
        if any(word in description for word in ['rent', 'mortgage', 'emi', 'apartment', 'house']):
            return 'Rent/Mortgage'
        
        # Entertainment
        if any(word in description for word in ['movie', 'netflix', 'spotify', 'game', 'entertainment', 'subscription']):
            return 'Entertainment'
        
        # Healthcare
        if any(word in description for word in ['medical', 'doctor', 'hospital', 'pharmacy', 'medicine', 'health']):
            return 'Healthcare'
        
        # Groceries
        if any(word in description for word in ['grocery', 'supermarket', 'vegetables', 'fruits', 'milk']):
            return 'Groceries'
        
        return 'Other'
    
    def _categorize_income(self, description: str) -> str:
        """Categorize income based on description"""
        description = description.lower()
        
        if any(word in description for word in ['salary', 'payroll', 'wage', 'company']):
            return 'Salary'
        elif any(word in description for word in ['business', 'profit', 'revenue']):
            return 'Business Income'
        elif any(word in description for word in ['freelance', 'contract', 'project']):
            return 'Freelance'
        elif any(word in description for word in ['dividend', 'interest', 'investment', 'mutual fund']):
            return 'Investment Returns'
        elif any(word in description for word in ['rent', 'rental']):
            return 'Rental Income'
        else:
            return 'Other Income'
    
    def _generate_budget_report(self, analysis: Dict) -> str:
        """Generate comprehensive budget report"""
        
        # Generate insights
        insights = self._generate_insights(analysis)
        
        # Format expense breakdown
        expense_breakdown = ""
        for category, amount in sorted(analysis['expense_breakdown'].items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / analysis['total_income'] * 100) if analysis['total_income'] > 0 else 0
            expense_breakdown += f"- **{category}**: Rs.{amount:,.0f} ({percentage:.1f}% of income)\n"
        
        # Format income breakdown
        income_breakdown = ""
        for category, amount in sorted(analysis['income_breakdown'].items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / analysis['total_income'] * 100) if analysis['total_income'] > 0 else 0
            income_breakdown += f"- **{category}**: Rs.{amount:,.0f} ({percentage:.1f}% of total income)\n"
        
        # Generate action items
        action_items = self._generate_action_items(analysis)
        
        report = f"""# Your AI-Generated Budget Report

## 📊 Financial Summary
- **Total Income**: Rs.{analysis['total_income']:,.0f}
- **Total Expenses**: Rs.{analysis['total_expenses']:,.0f}
- **Net Savings**: Rs.{analysis['net_savings']:,.0f}
- **Savings Rate**: {analysis['savings_rate']:.1f}%
- **Transactions Analyzed**: {analysis['transaction_count']}

## 💡 Budget Recommendations (50/30/20 Rule)
- **Needs (50%)**: Rs.{analysis['needs_budget']:,.0f}
- **Wants (30%)**: Rs.{analysis['wants_budget']:,.0f}
- **Savings (20%)**: Rs.{analysis['savings_budget']:,.0f}

## 🎯 Personalized Insights
{insights}

## 💰 Income Breakdown
{income_breakdown}

## 💸 Expense Breakdown
{expense_breakdown}

## 📋 Action Items
{action_items}

## 💎 Financial Health Score
{self._calculate_health_score(analysis)}

---
*Generated by AI Budget Planner on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*Powered by CrewAI & Masumi Network*"""

        return report
    
    def _generate_insights(self, analysis: Dict) -> str:
        """Generate personalized insights based on analysis"""
        insights = []
        
        savings_rate = analysis['savings_rate']
        
        # Savings rate insights
        if savings_rate >= 30:
            insights.append(f"🎉 Excellent! Your savings rate of {savings_rate:.1f}% is outstanding. You're building wealth effectively.")
        elif savings_rate >= 20:
            insights.append(f"✅ Great job! Your savings rate of {savings_rate:.1f}% meets the recommended 20% target.")
        elif savings_rate >= 10:
            insights.append(f"⚠️ Your savings rate of {savings_rate:.1f}% is below the recommended 20%. Consider reducing expenses.")
        else:
            insights.append(f"🚨 Your savings rate of {savings_rate:.1f}% needs immediate attention. Focus on expense reduction.")
        
        # Expense analysis
        if analysis['expense_breakdown']:
            top_expense = max(analysis['expense_breakdown'].items(), key=lambda x: x[1])
            expense_percentage = (top_expense[1] / analysis['total_income'] * 100) if analysis['total_income'] > 0 else 0
            
            if expense_percentage > 30:
                insights.append(f"💡 Your highest expense category is {top_expense[0]} at Rs.{top_expense[1]:,.0f} ({expense_percentage:.1f}% of income). Consider optimizing this area.")
            else:
                insights.append(f"👍 Your expense distribution looks balanced with {top_expense[0]} being your highest category at {expense_percentage:.1f}% of income.")
        
        # Income diversification
        income_sources = len(analysis['income_breakdown'])
        if income_sources == 1:
            insights.append("💼 Consider diversifying your income sources to reduce financial risk.")
        elif income_sources >= 3:
            insights.append("🌟 Great job diversifying your income sources! This provides good financial stability.")
        
        return '\n'.join(f"{i+1}. {insight}" for i, insight in enumerate(insights))
    
    def _generate_action_items(self, analysis: Dict) -> str:
        """Generate actionable recommendations"""
        actions = []
        
        savings_rate = analysis['savings_rate']
        
        if savings_rate < 20:
            shortfall = analysis['savings_budget'] - analysis['net_savings']
            actions.append(f"🎯 **Priority**: Increase savings by Rs.{shortfall:,.0f} per month to reach 20% target")
        
        if analysis['expense_breakdown']:
            # Find optimization opportunities
            for category, amount in analysis['expense_breakdown'].items():
                percentage = (amount / analysis['total_income'] * 100) if analysis['total_income'] > 0 else 0
                
                if category == 'Food & Dining' and percentage > 15:
                    actions.append(f"🍽️ **Optimize**: Food expenses are {percentage:.1f}% of income. Try cooking more at home")
                elif category == 'Entertainment' and percentage > 10:
                    actions.append(f"🎬 **Review**: Entertainment expenses are high at {percentage:.1f}% of income")
                elif category == 'Shopping' and percentage > 10:
                    actions.append(f"🛍️ **Control**: Shopping expenses are {percentage:.1f}% of income. Create a shopping budget")
        
        if savings_rate >= 25:
            actions.append("💰 **Invest**: Your high savings rate allows for investment opportunities")
        
        if not actions:
            actions.append("✅ **Maintain**: Your financial habits are on track. Keep up the good work!")
        
        return '\n'.join(f"- {action}" for action in actions)
    
    def _calculate_health_score(self, analysis: Dict) -> str:
        """Calculate and format financial health score"""
        score = 0
        
        # Savings rate (40 points max)
        savings_rate = analysis['savings_rate']
        if savings_rate >= 30:
            score += 40
        elif savings_rate >= 20:
            score += 30
        elif savings_rate >= 10:
            score += 20
        else:
            score += 10
        
        # Income diversification (20 points max)
        income_sources = len(analysis['income_breakdown'])
        if income_sources >= 3:
            score += 20
        elif income_sources == 2:
            score += 15
        else:
            score += 10
        
        # Expense control (40 points max)
        if analysis['total_income'] > 0:
            expense_ratio = analysis['total_expenses'] / analysis['total_income']
            if expense_ratio <= 0.7:
                score += 40
            elif expense_ratio <= 0.8:
                score += 30
            elif expense_ratio <= 0.9:
                score += 20
            else:
                score += 10
        
        # Determine grade
        if score >= 85:
            grade = "A+ (Excellent)"
            emoji = "🏆"
        elif score >= 75:
            grade = "A (Very Good)"
            emoji = "🥇"
        elif score >= 65:
            grade = "B (Good)"
            emoji = "🥈"
        elif score >= 55:
            grade = "C (Fair)"
            emoji = "🥉"
        else:
            grade = "D (Needs Improvement)"
            emoji = "⚠️"
        
        return f"{emoji} **Score**: {score}/100 - Grade {grade}"
    
    def _generate_empty_report(self) -> str:
        """Generate report when no transactions are available"""
        return """# Your AI-Generated Budget Report

## 📊 Financial Summary
- **Total Income**: Rs.0
- **Total Expenses**: Rs.0
- **Net Savings**: Rs.0
- **Savings Rate**: 0%
- **Transactions Analyzed**: 0

## 💡 Getting Started
1. Add your income transactions to track earnings
2. Record your expenses to understand spending patterns
3. Sync your bank account for automatic transaction import
4. Return here for personalized AI insights

## 🎯 Next Steps
- Start by adding your monthly salary or income
- Record major expenses like rent, groceries, and utilities
- Use the bank sync feature to import existing transactions
- Check back weekly for updated insights

---
*Ready to analyze your finances! Add some transactions to get started.*"""