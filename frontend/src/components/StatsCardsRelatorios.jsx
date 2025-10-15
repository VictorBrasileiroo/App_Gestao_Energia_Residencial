import React from 'react'

const StatsCardsRelatorios = () => {
  const stats = [
    {
      title: 'Consumo Total',
      value: '2,847',
      unit: 'kWh',
      change: '+5.2%',
      trend: 'up'
    },

    {
      title: 'Custo Total',
      value: 'R$ 1.987,90',
      change: '+4.8%',
      trend: 'up'
    },

    {
      title: 'Média Diária',
      value: '94.9',
      unit: 'kWh',
      change: '+2.1%',
      trend: 'up'
    },
    
    {
      title: 'Eficiência',
      value: '92',
      unit: '%',
      change: '+8.5%',
      trend: 'up'
    }
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {stats.map((stat, index) => (
        <div key={index} className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h3 className="text-sm font-medium text-gray-600 mb-2">{stat.title}</h3>
          <div className="flex items-baseline">
            <span className="text-2xl font-bold text-gray-900">{stat.value}</span>
            {stat.unit && <span className="text-sm text-gray-500 ml-1">{stat.unit}</span>}
          </div>
          <div className={`flex items-center mt-2 text-sm ${
            stat.trend === 'up' ? 'text-green-500' : 'text-red-500'
          }`}>
            <span>{stat.change}</span>
          </div>
        </div>
      ))}
    </div>
  )
}

export default StatsCardsRelatorios