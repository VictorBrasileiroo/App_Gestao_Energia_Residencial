import React from 'react'
import { Zap, DollarSign, BarChart3, Target } from 'lucide-react'

const StatsCardsRelatorios = () => {
  const stats = [
    {
      title: 'Consumo Total',
      value: '2,847',
      unit: 'kWh',
      change: '+5.2%',
      trend: 'up',
      icon: Zap,
      iconBg: 'bg-green-500',
      iconColor: 'text-white'
    },
    {
      title: 'Custo Total',
      value: 'R$ 1.987,90',
      unit: '',
      change: '+4.8%',
      trend: 'up',
      icon: DollarSign,
      iconBg: 'bg-orange-500',
      iconColor: 'text-white'
    },
    {
      title: 'Média Diária',
      value: '94.9',
      unit: 'kWh',
      change: '+2.1%',
      trend: 'up',
      icon: BarChart3,
      iconBg: 'bg-blue-500',
      iconColor: 'text-white'
    },
    {
      title: 'Eficiência',
      value: '92',
      unit: '%',
      change: '+8.5%',
      trend: 'up',
      icon: Target,
      iconBg: 'bg-purple-500',
      iconColor: 'text-white'
    }
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {stats.map((stat, index) => {
        const IconComponent = stat.icon
        return (
          <div key={index} className="relative bg-white p-6 rounded-2xl shadow-lg border border-gray-100 hover:shadow-xl transform hover:scale-105 transition-all duration-300 overflow-hidden">
            {/* Background gradient sutil */}
            <div className={`absolute top-0 right-0 w-24 h-24 ${stat.iconBg} opacity-10 rounded-full -mr-12 -mt-12`}></div>
            
            <div className="relative z-10">
              {/* Header com ícone, título e badge */}
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-3">
                  <div className={`p-3 rounded-xl ${stat.iconBg} shadow-lg`}>
                    <IconComponent className={`h-6 w-6 ${stat.iconColor}`} />
                  </div>
                  <h3 className="text-sm font-semibold text-gray-600">{stat.title}</h3>
                </div>
                {stat.change && (
                  <span className={`text-xs font-bold px-2 py-1 rounded-full ${stat.trend === 'up' ? 'text-green-700 bg-green-100' : 'text-red-700 bg-red-100'}`}>
                    {stat.change}
                  </span>
                )}
              </div>
              
              {/* Valor principal */}
              <div className="mt-4">
                <div className="flex items-baseline">
                  <span className="text-4xl font-black text-gray-900">{stat.value}</span>
                  {stat.unit && (
                    <span className="text-lg text-gray-500 ml-2 font-medium">{stat.unit}</span>
                  )}
                </div>
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}

export default StatsCardsRelatorios