import React from 'react'
import { Zap, DollarSign, BarChart3, TrendingUp } from 'lucide-react'

const StatsCards = ({ data }) => {
    // Extract data from API response
    const todayData = data?.summary_today || {}
    const dailyView = data?.daily_view_last_7_days?.series || []
    
    // Calculate average and peak from last 7 days
    const avgDaily = dailyView.length > 0 
        ? (dailyView.reduce((sum, d) => sum + d.energy_kwh, 0) / dailyView.length)
        : 0
    
    const peak = dailyView.length > 0
        ? Math.max(...dailyView.map(d => d.energy_kwh))
        : 0
    
    const totalConsumption = dailyView.length > 0
        ? dailyView.reduce((sum, d) => sum + d.energy_kwh, 0)
        : 0
    
    const stats = [
        {
            title: 'Consumo Total (7d)',
            value: totalConsumption.toFixed(0),
            unit: 'kWh',
            change: todayData.comparison_vs_yesterday_pct ? `${todayData.comparison_vs_yesterday_pct > 0 ? '+' : ''}${todayData.comparison_vs_yesterday_pct.toFixed(1)}%` : null,
            trend: todayData.comparison_vs_yesterday_pct < 0 ? 'down' : 'up',
            icon: Zap,
            iconBg: 'bg-green-500',
            iconColor: 'text-white'
        },
        {
            title: 'Custo Total (7d)',
            value: `R$ ${(totalConsumption * 0.70).toFixed(2)}`,
            unit: '',
            change: null,
            icon: DollarSign,
            iconBg: 'bg-orange-500',
            iconColor: 'text-white'
        },
        {
            title: 'Média Diária',
            value: avgDaily.toFixed(1),
            unit: 'kWh',
            change: null,
            icon: BarChart3,
            iconBg: 'bg-blue-500',
            iconColor: 'text-white'
        },
        {
            title: 'Pico',
            value: peak.toFixed(1),
            unit: 'kWh',
            change: null,
            icon: TrendingUp,
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
                                    <span className={`text-xs font-bold px-2 py-1 rounded-full ${stat.trend === 'down' ? 'text-green-700 bg-green-100' : 'text-red-700 bg-red-100'}`}>
                                        {stat.change}%
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

export default StatsCards