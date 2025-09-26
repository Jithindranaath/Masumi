import React from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

const BudgetChart = ({ data }) => {
  const COLORS = ['#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4', '#F97316', '#EC4899', '#84CC16']

  return (
    <div className="space-y-6">
      {/* Bar Chart */}
      <div>
        <h4 className="text-lg font-medium text-gray-900 mb-4">Monthly Spending by Category</h4>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="category" 
              angle={-45}
              textAnchor="end"
              height={80}
              fontSize={12}
            />
            <YAxis 
              tickFormatter={(value) => `₹${value.toLocaleString()}`}
              fontSize={12}
            />
            <Tooltip 
              formatter={(value) => [`₹${value.toLocaleString()}`, 'Amount']}
              labelStyle={{ color: '#374151' }}
            />
            <Bar 
              dataKey="amount" 
              fill="#3B82F6"
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Pie Chart */}
      <div>
        <h4 className="text-lg font-medium text-gray-900 mb-4">Expense Distribution</h4>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={data.filter(item => item.category !== 'Income')}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ category, percent }) => `${category} ${(percent * 100).toFixed(0)}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="amount"
            >
              {data.filter(item => item.category !== 'Income').map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip formatter={(value) => `₹${value.toLocaleString()}`} />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <h5 className="font-medium text-green-900">Total Income</h5>
          <p className="text-2xl font-bold text-green-700">
            ₹{data.find(item => item.category === 'Income')?.amount.toLocaleString() || '0'}
          </p>
        </div>
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <h5 className="font-medium text-red-900">Total Expenses</h5>
          <p className="text-2xl font-bold text-red-700">
            ₹{data.filter(item => item.category !== 'Income')
                .reduce((sum, item) => sum + item.amount, 0)
                .toLocaleString()}
          </p>
        </div>
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h5 className="font-medium text-blue-900">Net Savings</h5>
          <p className="text-2xl font-bold text-blue-700">
            ₹{(
              (data.find(item => item.category === 'Income')?.amount || 0) -
              data.filter(item => item.category !== 'Income')
                .reduce((sum, item) => sum + item.amount, 0)
            ).toLocaleString()}
          </p>
        </div>
      </div>
    </div>
  )
}

export default BudgetChart