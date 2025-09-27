# Detailed Expenses API Documentation

## Overview

The FIU Platform now supports **detailed expense tracking** with comprehensive purpose analysis. This feature allows users to record not just the amount and category of expenses, but also the **reason for spending**, priority level, merchant information, and payment method.

## 🎯 Key Features

- **Purpose Tracking**: Record why money was spent with detailed reasons
- **Priority Classification**: Essential, Important, Optional, or Impulse purchases
- **Merchant Information**: Track where money was spent
- **Payment Method**: Monitor how payments were made
- **AI Analysis**: Get insights into spending patterns and reasons
- **Comprehensive Reporting**: Detailed breakdowns by category, priority, and purpose

## 📊 API Endpoints

### 1. Get Detailed Expenses

**Endpoint**: `GET /api/expenses/detailed/{user_id}`

**Description**: Retrieve all detailed expenses with comprehensive analysis

**Parameters**:
- `user_id` (path): User identifier
- `limit` (query, optional): Maximum number of expenses to return (default: 50)

**Response**:
```json
{
  "expenses": [...],
  "detailed_expenses": [...],
  "simple_expenses": [...],
  "summary": {
    "total_expenses": 15750.0,
    "expense_count": 12,
    "detailed_count": 8,
    "simple_count": 4,
    "average_expense": 1312.5,
    "top_category": "food",
    "top_category_amount": 4500.0,
    "top_reason": "Monthly groceries for family",
    "top_reason_amount": 2800.0,
    "top_merchant": "Big Bazaar",
    "top_merchant_amount": 2800.0
  },
  "breakdowns": {
    "by_category": {
      "food": 4500.0,
      "transport": 2200.0,
      "shopping": 3050.0
    },
    "by_priority": {
      "essential": 6800.0,
      "important": 4200.0,
      "optional": 2750.0,
      "impulse": 2000.0
    },
    "by_reason": {
      "Monthly groceries for family": 2800.0,
      "Emergency car repair": 2200.0,
      "Birthday gift for spouse": 1500.0
    },
    "by_merchant": {
      "Big Bazaar": 2800.0,
      "Auto Repair Shop": 2200.0,
      "Amazon": 1500.0
    },
    "by_payment_method": {
      "card": 8750.0,
      "upi": 4200.0,
      "cash": 2800.0
    }
  }
}
```

### 2. Add Detailed Expense

**Endpoint**: `POST /api/expense/detailed/add`

**Description**: Add a new expense with detailed purpose and priority information

**Request Body**:
```json
{
  "user_id": "demo_user",
  "account_number": "1234567890",
  "amount": 850.0,
  "category": "food",
  "description": "Dinner with family",
  "merchant": "The Olive Garden Restaurant",
  "reason": "Monthly family dinner - celebrating mom's birthday",
  "priority": "important",
  "payment_method": "card"
}
```

**Response**:
```json
{
  "success": true,
  "transaction_id": "tx_abc123",
  "new_balance": 9150.0,
  "masumi_tx_hash": "masumi_xyz789",
  "expense_category": "Food",
  "merchant": "The Olive Garden Restaurant",
  "reason": "Monthly family dinner - celebrating mom's birthday",
  "priority": "important",
  "payment_method": "card"
}
```

## 🏷️ Field Definitions

### Priority Levels
- **Essential** 🔴: Must-have expenses (rent, utilities, groceries)
- **Important** 🟡: Should-have expenses (healthcare, education)
- **Optional** 🟢: Nice-to-have expenses (entertainment, dining out)
- **Impulse** 🔵: Unplanned purchases (spontaneous shopping)

### Categories
- `food` - Food & Dining
- `transport` - Transportation
- `shopping` - Shopping
- `bills` - Bills & Utilities
- `rent` - Rent/Mortgage
- `entertainment` - Entertainment
- `healthcare` - Healthcare
- `education` - Education
- `groceries` - Groceries
- `fuel` - Fuel
- `clothing` - Clothing
- `other` - Other expenses

### Payment Methods
- `cash` - Cash payments
- `card` - Debit/Credit card
- `upi` - UPI payments
- `netbanking` - Net banking
- `other` - Other payment methods

## 💡 Usage Examples

### Example 1: Track Monthly Groceries
```python
import requests

expense_data = {
    "user_id": "user123",
    "account_number": "1234567890",
    "amount": 2800.0,
    "category": "groceries",
    "description": "Monthly grocery shopping",
    "merchant": "Big Bazaar",
    "reason": "Monthly groceries for family of 4 - includes vegetables, fruits, and household items",
    "priority": "essential",
    "payment_method": "card"
}

response = requests.post("http://localhost:8001/api/expense/detailed/add", json=expense_data)
```

### Example 2: Track Emergency Expense
```python
expense_data = {
    "user_id": "user123",
    "account_number": "1234567890",
    "amount": 2200.0,
    "category": "transport",
    "description": "Car repair",
    "merchant": "Auto Repair Shop",
    "reason": "Emergency car repair - brake pads replacement needed for safety",
    "priority": "essential",
    "payment_method": "upi"
}
```

### Example 3: Track Impulse Purchase
```python
expense_data = {
    "user_id": "user123",
    "account_number": "1234567890",
    "amount": 1200.0,
    "category": "shopping",
    "description": "Online shopping",
    "merchant": "Amazon",
    "reason": "Saw a good deal on electronics - bought wireless headphones",
    "priority": "impulse",
    "payment_method": "card"
}
```

## 📈 Analysis Features

### 1. Purpose Analysis
- Track **why** money is being spent
- Identify recurring spending reasons
- Understand spending motivations

### 2. Priority Breakdown
- See how much is spent on essentials vs wants
- Monitor impulse spending patterns
- Optimize budget allocation

### 3. Merchant Tracking
- Identify top spending locations
- Track loyalty and frequency
- Find opportunities for discounts

### 4. Payment Method Analysis
- Monitor payment preferences
- Track cashless vs cash spending
- Optimize payment methods for rewards

## 🚀 Getting Started

### 1. Database Migration
If you have an existing FIU database, run the migration:
```bash
python migrate_detailed_expenses.py
```

### 2. Start the Server
```bash
python fiu_main.py
```

### 3. Test the API
```bash
python test_detailed_expenses.py
```

## 🔍 Frontend Integration

The detailed expenses feature integrates seamlessly with the existing FIU frontend. The expense analysis section provides:

- **Real-time Analysis**: AI analyzes spending patterns after each transaction
- **Visual Breakdowns**: Charts showing category, priority, and reason distributions
- **Detailed Forms**: Easy-to-use forms for adding expenses with purposes
- **Smart Insights**: AI recommendations based on spending reasons and priorities

## 🤖 AI Integration

The detailed expense data enhances AI budget analysis by:

- **Understanding Intent**: AI knows why money was spent
- **Priority-based Recommendations**: Suggestions based on spending priorities
- **Pattern Recognition**: Identifying recurring spending reasons
- **Behavioral Insights**: Understanding spending motivations and triggers

## 📊 Sample Analysis Output

```
# AI Expense Analysis Report

## 📊 Expense Overview
- Total Expenses: Rs.15,750
- Expense Ratio: 78.5% of total income
- Number of Transactions: 12
- Average Expense: Rs.1,312

## 🎯 Priority Analysis
- 🔴 Essential: Rs.6,800 (43.2%)
- 🟡 Important: Rs.4,200 (26.7%)
- 🟢 Optional: Rs.2,750 (17.5%)
- 🔵 Impulse: Rs.2,000 (12.7%)

## 💡 Spending Reasons Analysis
1. "Monthly groceries for family" - Rs.2,800
2. "Emergency car repair" - Rs.2,200
3. "Birthday gift for spouse" - Rs.1,500
4. "Work lunch meetings" - Rs.1,200
5. "Weekend entertainment" - Rs.800

## 🤖 AI Recommendations
⚠️ Impulse Control: 12.7% of expenses are impulse purchases. Consider a 24-hour waiting period for non-essential purchases.
💡 Category Focus: Food represents 28.6% of your expenses. Look for optimization opportunities in this area.
```

## 🔒 Security & Privacy

- All expense data is encrypted and stored securely
- Masumi blockchain integration provides transaction verification
- Personal spending reasons are never shared or analyzed externally
- Users have full control over their detailed expense data

## 📞 Support

For questions or issues with the detailed expenses feature:
1. Check the API documentation above
2. Run the test script: `python test_detailed_expenses.py`
3. Review the migration script: `python migrate_detailed_expenses.py`
4. Examine the frontend expense analysis section

---

**Built with ❤️ for better financial understanding and control**