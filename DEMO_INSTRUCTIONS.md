# 🚀 AI Budget Planner - Quick Demo Instructions

## 🎯 **Easiest Way to Run Demo**

### Option 1: Universal Demo Runner (Recommended)
```bash
python run_demo.py
```
This script will:
- ✅ Check and install missing dependencies
- ✅ Find available ports automatically
- ✅ Start backend server
- ✅ Open demo in your browser
- ✅ Work on any system (Windows/Mac/Linux)

### Option 2: Standalone HTML Demo
1. Start backend: `python main.py api`
2. Open `demo.html` in your browser
3. The demo will automatically find the backend server

### Option 3: Manual Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Start backend: `python main.py api`
3. Open http://localhost:[PORT] (port will be shown in terminal)

## 🔑 **Required Setup**

### OpenAI API Key (Required)
1. Get your key from: https://platform.openai.com/api-keys
2. Add it to `.env` file:
   ```
   OPENAI_API_KEY=your_key_here
   ```

## 🎮 **Demo Features**

### What You'll See:
- 🤖 **AI-Powered Analysis**: Real AI agents process your financial data
- 📊 **Interactive Charts**: Visual spending breakdown
- 💡 **Smart Recommendations**: Personalized budget insights using 50/30/20 rule
- 📋 **Detailed Reports**: Comprehensive financial analysis

### Demo Data:
- Uses mock transaction data (no real bank connection needed)
- Simulates Account Aggregator framework
- Shows realistic financial scenarios

## 🔧 **Troubleshooting**

### Port Issues:
- The app automatically finds free ports
- If you see port errors, just restart the demo

### Missing Dependencies:
- Run: `pip install fastapi uvicorn pandas sqlalchemy python-dotenv crewai masumi`

### OpenAI API Issues:
- Make sure your API key is valid
- Check your OpenAI account has credits
- The demo uses very minimal API calls (costs ~$0.01-0.10)

## 🌐 **Cross-Platform Compatibility**

### Works On:
- ✅ Windows (any version)
- ✅ macOS (any version)  
- ✅ Linux (any distribution)
- ✅ Any Python 3.8+ installation

### No Additional Setup Needed:
- ❌ No Node.js required
- ❌ No Docker required
- ❌ No complex configuration
- ❌ No external databases

## 📱 **Demo Workflow**

1. **Enter User ID**: Use "demo_user" or any ID
2. **Click Generate**: AI crew starts processing
3. **Watch Progress**: Real-time status updates
4. **View Results**: 
   - Detailed budget report
   - Spending breakdown charts
   - Actionable recommendations
   - Financial insights

## 🎯 **Perfect for:**
- ✅ Hackathon demonstrations
- ✅ Portfolio showcases
- ✅ Technical interviews
- ✅ Proof of concept presentations
- ✅ Educational purposes

---

**🚀 Ready to see AI-powered financial planning in action? Run `python run_demo.py` now!**