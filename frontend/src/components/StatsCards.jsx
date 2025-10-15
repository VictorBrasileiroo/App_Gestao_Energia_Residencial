import React from 'react'

const StatsCards = () => {
    const stats = [
        {
            title: 'Consume Total',
            value: '289 kwh',
            change: '-5',
            trend: 'down',
        },

        {
            title: 'Custo Total',
            value: 'R$ 202,30',
            change: null
        },

        {
            title: 'Média Diária',
            value: '9,6 kwh',
            change: null
        },

        {
            title: 'Pico',
            value: '15,8 kwh',
            change: null
        }
    ]

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {stats.map((stat, index) => (
                <div key={index} className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <h3 className="text-sm font-medium text-gray-600">{stat.title}</h3>
                <div className="flex items-baseline mt-2">
                    <span className="text-2xl font-bold text-gray-900">{stat.value}</span>
                    {stat.change && (
                    <span className={`ml-2 text-sm ${stat.trend === 'down' ? 'text-green-500' : 'text-red-500'}`}>
                        {stat.change}%
                    </span>
                    )}
                </div>
            </div>
        ))}
    </div>
  )
}

export default StatsCards