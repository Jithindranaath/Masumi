# AI Automated Budget Planner

This **AI Automated Budget Planner** is built using the CrewAI Masumi Starter Kit and provides personalized budget planning through AI-powered financial analysis. The application integrates with India's Account Aggregator (AA) framework to fetch financial data and uses a multi-agent CrewAI system to generate actionable budget insights.

## 🚀 Key Features

- **Multi-Agent AI System**: Four specialized CrewAI agents work together to analyze your finances
- **Account Aggregator Integration**: Secure financial data fetching via India's AA framework
- **Personalized Budget Plans**: AI-generated recommendations based on the 50/30/20 rule
- **Interactive Dashboard**: React frontend with charts and visualizations
- **Masumi Payment Integration**: Monetized AI services with decentralized payments

## 🏗️ Architecture

### Backend (FastAPI)
- **Transaction Categorizer Agent** 🗂️: Intelligently categorizes transactions
- **Financial Analyst Agent** 📊: Analyzes spending patterns and calculates key metrics
- **Budget Strategist Agent** 💡: Creates personalized budget recommendations
- **Report Generator Agent** ✍️: Generates user-friendly financial reports

### Frontend (React + Vite + Tailwind)
- Interactive dashboard with budget visualization
- Real-time AI crew processing status
- Spending breakdown charts using Recharts
- Responsive design with Tailwind CSS

### Data Integration
- Account Aggregator (AA) client for secure financial data access
- SQLite database for user data and budget reports
- Mock transaction data for demo purposes

## 📋 Prerequisites

- Python >= 3.10 and < 3.13
- Node.js >= 16
- uv (Python package manager)
- npm or yarn

## 🛠️ Setup Instructions

### 1. Clone and Setup Backend

```bash
git clone https://github.com/masumi-network/crewai-masumi-quickstart-template.git
cd crewai-masumi-quickstart-template
```

Create Python virtual environment:
```bash
uv venv --python 3.13
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Update `.env` with your credentials:
```ini
# Payment Service (for Masumi integration)
PAYMENT_SERVICE_URL=http://localhost:3001/api/v1
PAYMENT_API_KEY=your_payment_key
AGENT_IDENTIFIER=your_agent_identifier
SELLER_VKEY=your_selling_wallet_vkey

# OpenAI API
OPENAI_API_KEY=your_openai_api_key

# Account Aggregator (for production)
AA_BASE_URL=https://sandbox.setu.co/api
AA_API_KEY=your_aa_api_key
AA_CLIENT_ID=your_aa_client_id

# Network
NETWORK=Preprod
```

### 3. Setup Frontend

Navigate to frontend directory and install dependencies:
```bash
cd frontend
npm install
```

### 4. Run the Application

#### Start Backend Server:
```bash
# From project root
python main.py api
```
Backend will be available at: http://localhost:8001

#### Start Frontend Development Server:
```bash
# From frontend directory
npm run dev
```
Frontend will be available at: http://localhost:3000

## 🎯 Usage

### Demo Mode (No Payment Required)

1. Open http://localhost:3000 in your browser
2. Enter a user ID (e.g., "demo_user")
3. Click "Generate My Budget Plan"
4. Watch the AI crew analyze mock financial data
5. View your personalized budget report and spending charts

### Production Mode (With Masumi Payments)

1. Set up the Masumi Payment Service following the [Installation Guide](https://docs.masumi.network/documentation/get-started/installation)
2. Register your agent on Masumi Network
3. Use the `/start_job` endpoint for paid budget planning services

## 🤖 AI Crew Workflow

The budget planning process involves four AI agents working sequentially:

1. **Transaction Categorizer** 🗂️
   - Parses raw transaction JSON from AA framework
   - Categorizes transactions into: Income, Groceries, Utilities, Rent/Mortgage, EMI, Transport, Dining Out, Shopping, Entertainment, Subscriptions, Miscellaneous
   - Uses intelligent rules and LLM reasoning for ambiguous transactions

2. **Financial Analyst** 📊
   - Calculates total income, expenses, and savings rate
   - Generates spending breakdown by category
   - Identifies recurring payments and top expenses
   - Outputs structured financial analysis

3. **Budget Strategist** 💡
   - Applies 50/30/20 budgeting rule (Needs/Wants/Savings)
   - Creates category-specific spending recommendations
   - Generates actionable insights based on spending patterns

4. **Report Generator** ✍️
   - Combines analysis and strategy into user-friendly report
   - Uses encouraging, supportive tone
   - Provides clear, actionable recommendations

## 📊 API Endpoints

### Budget Planning
- `POST /generate_budget_plan` - Generate budget plan (demo mode)
- `POST /start_job` - Start paid budget planning job
- `GET /status?job_id={id}` - Check job status

### Masumi Integration
- `GET /availability` - Check server availability
- `GET /input_schema` - Get input requirements
- `GET /health` - Health check

## 🔧 Development

### Adding New Features

1. **New AI Agents**: Add to `app/crew.py`
2. **Database Models**: Update `app/models.py`
3. **API Endpoints**: Add to `main.py`
4. **Frontend Components**: Add to `frontend/src/components/`

### Testing

Test the budget planning workflow:
```bash
curl -X POST "http://localhost:8001/generate_budget_plan" \
-H "Content-Type: application/json" \
-d '{"user_id": "test_user"}'
```

## 🚀 Deployment

### Backend Deployment
- Deploy FastAPI app to your preferred platform (Railway, Heroku, AWS)
- Ensure environment variables are configured
- Set up production database (PostgreSQL recommended)

### Frontend Deployment
```bash
cd frontend
npm run build
# Deploy dist/ folder to your hosting platform
```

## 🔗 Integration with Account Aggregator

The application integrates with India's Account Aggregator framework for secure financial data access:

1. **Consent Management**: Request user consent for data access
2. **Data Fetching**: Retrieve transaction data from multiple bank accounts
3. **Privacy**: No storage of sensitive financial data

For production, integrate with AA providers like:
- [Setu](https://setu.co/)
- [Finvu](https://finvu.in/)
- [CAMS Finserv](https://www.camsonline.com/)

## 📚 Resources

- [CrewAI Documentation](https://docs.crewai.com)
- [Masumi Documentation](https://docs.masumi.network)
- [Account Aggregator Framework](https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=50465)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [React Documentation](https://react.dev)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ using CrewAI, Masumi, and the Account Aggregator framework**