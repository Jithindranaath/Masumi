import React, { useState } from 'react'
import axios from 'axios'
import BudgetChart from './BudgetChart'

const Dashboard = () => {
  const [loading, setLoading] = useState(false)
  const [budgetPlan, setBudgetPlan] = useState(null)
  const [error, setError] = useState(null)
  const [userId, setUserId] = useState('demo_user')

  const generateBudgetPlan = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await axios.post('http://localhost:8000/generate_budget_plan', {
        user_id: userId
      })
      
      setBudgetPlan(response.data.budget_plan)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate budget plan')
    } finally {
      setLoading(false)
    }
  }

  const mockChartData = [
    { category: 'Income', amount: 50000, color: '#10B981' },
    { category: 'Groceries', amount: 8000, color: '#F59E0B' },
    { category: 'Utilities', amount: 3000, color: '#EF4444' },
    { category: 'Rent', amount: 15000, color: '#8B5CF6' },
    { category: 'Transport', amount: 4000, color: '#06B6D4' },
    { category: 'Dining Out', amount: 6000, color: '#F97316' },
    { category: 'Shopping', amount: 5000, color: '#EC4899' },
    { category: 'Entertainment', amount: 2000, color: '#84CC16' }
  ]

  return (
    <div className="space-y-8">
      {/* User Input Section */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Get Your Personalized Budget Plan
        </h2>
        <div className="flex items-center space-x-4">
          <input
            type="text"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            placeholder="Enter your user ID"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <button
            onClick={generateBudgetPlan}
            disabled={loading}
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span>Analyzing...</span>
              </>
            ) : (
              <span>Generate My Budget Plan</span>
            )}
          </button>
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <div className="flex items-center space-x-3">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
            <div>
              <h3 className="text-lg font-medium text-blue-900">
                Our AI crew is analyzing your finances...
              </h3>
              <p className="text-blue-700">
                🗂️ Categorizing transactions → 📊 Analyzing patterns → 💡 Creating strategy → ✍️ Generating report
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <h3 className="text-lg font-medium text-red-900 mb-2">Error</h3>
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {/* Budget Plan Results */}
      {budgetPlan && (
        <div className="space-y-6">
          {/* Budget Report */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">
              📋 Your Personalized Budget Report
            </h3>
            <div className="prose max-w-none">
              <pre className="whitespace-pre-wrap text-sm text-gray-700 bg-gray-50 p-4 rounded-md">
                {budgetPlan}
              </pre>
            </div>
          </div>

          {/* Spending Breakdown Chart */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">
              📊 Spending Breakdown
            </h3>
            <BudgetChart data={mockChartData} />
          </div>

          {/* Quick Actions */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">
              🎯 Quick Actions
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <h4 className="font-medium text-green-900">Set Savings Goal</h4>
                <p className="text-sm text-green-700 mt-1">
                  Automate your savings based on the 50/30/20 rule
                </p>
              </div>
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <h4 className="font-medium text-yellow-900">Review Subscriptions</h4>
                <p className="text-sm text-yellow-700 mt-1">
                  Cancel unused subscriptions to save money
                </p>
              </div>
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h4 className="font-medium text-blue-900">Track Progress</h4>
                <p className="text-sm text-blue-700 mt-1">
                  Monitor your spending against budget limits
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Initial State */}
      {!budgetPlan && !loading && !error && (
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <div className="text-6xl mb-4">🤖</div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            Ready to Transform Your Finances?
          </h3>
          <p className="text-gray-600 mb-6">
            Our AI crew will analyze your transactions and create a personalized budget plan with actionable insights.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm">
            <div className="flex flex-col items-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl mb-2">🗂️</div>
              <div className="font-medium">Categorize</div>
              <div className="text-gray-600">Smart transaction sorting</div>
            </div>
            <div className="flex flex-col items-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl mb-2">📊</div>
              <div className="font-medium">Analyze</div>
              <div className="text-gray-600">Find spending patterns</div>
            </div>
            <div className="flex flex-col items-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl mb-2">💡</div>
              <div className="font-medium">Strategize</div>
              <div className="text-gray-600">Create budget plan</div>
            </div>
            <div className="flex flex-col items-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl mb-2">✍️</div>
              <div className="font-medium">Report</div>
              <div className="text-gray-600">Actionable insights</div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Dashboard