import React, { useState, useEffect } from 'react'
import { dashboardAPI } from '../services/api'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { Line } from 'react-chartjs-2'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const ComparisonSection = ({ data }) => {
  const [monthlyData, setMonthlyData] = useState([])
  const [chartLoading, setChartLoading] = useState(true)
  
  const dailyView = data?.daily_view_last_7_days?.series || []
  const prediction = data?.next_month_prediction || {}
  const todayData = data?.summary_today || {}
  
  // Fetch monthly comparison data for chart
  useEffect(() => {
    const fetchMonthlyData = async () => {
      try {
        setChartLoading(true)
        const response = await dashboardAPI.getMonthlyComparison()
        const allData = response.data.monthly_data || []
        
        // GAMBIARRA: Filtrar apenas até outubro (mês atual) + predição
        const today = new Date()
        const currentMonth = today.getMonth() + 1 // 1-12
        const currentYear = today.getFullYear()
        
        const filteredData = allData.filter(item => {
          // Sempre incluir predições
          if (item.is_prediction) return true
          
          // Para dados reais, filtrar apenas até outubro/2025
          const [year, month] = item.month_key.split('-').map(Number)
          
          // Se for ano anterior, incluir
          if (year < currentYear) return true
          
          // Se for ano atual, incluir apenas até outubro
          if (year === currentYear && month <= currentMonth) return true
          
          // Resto (novembro, dezembro do ano atual) -> EXCLUIR
          return false
        })
        
        console.log('📊 Dados originais:', allData.length)
        console.log('✅ Dados filtrados (até OUT):', filteredData.length)
        console.log('🗓️ Dados finais:', filteredData)
        
        setMonthlyData(filteredData)
      } catch (error) {
        console.error('Erro ao carregar dados mensais:', error)
        setMonthlyData([])
      } finally {
        setChartLoading(false)
      }
    }
    
    if (data) {
      fetchMonthlyData()
    }
  }, [data])
  
  // Calculate statistics
  const last7DaysTotal = dailyView.reduce((sum, d) => sum + d.energy_kwh, 0)
  const avgDaily = dailyView.length > 0 ? (last7DaysTotal / dailyView.length) : 0
  const last30DaysAvg = avgDaily * 4.28 // Estimate month from week
  
  const comparisons = [
    {
      title: 'Consumo Hoje',
      value: todayData.energy_kwh?.toFixed(0) || '0',
      unit: 'kWh',
      change: todayData.comparison_vs_yesterday_pct ? `${todayData.comparison_vs_yesterday_pct > 0 ? '+' : ''}${todayData.comparison_vs_yesterday_pct.toFixed(1)}%` : 'N/A',
      valueColor: 'text-green-600',
      bgColor: 'bg-gradient-to-br from-green-50 to-green-100',
      changeColor: todayData.comparison_vs_yesterday_pct > 0 ? 'text-red-500' : 'text-green-500'
    },
    {
      title: 'Média Últimos 7 Dias',
      value: avgDaily.toFixed(0),
      unit: 'kWh/dia',
      change: 'Média diária',
      valueColor: 'text-blue-600',
      bgColor: 'bg-gradient-to-br from-blue-50 to-blue-100',
      changeColor: 'text-gray-600'
    },
    {
      title: 'Previsão Próximo Mês',
      value: prediction.energy_kwh_pred?.toFixed(0) || 'N/A',
      unit: prediction.energy_kwh_pred ? 'kWh' : '',
      change: prediction.target_month || 'Sem predição',
      valueColor: 'text-orange-600',
      bgColor: 'bg-gradient-to-br from-orange-50 to-orange-100',
      changeColor: 'text-orange-500'
    },
    {
      title: 'Total Últimos 7 Dias',
      value: last7DaysTotal.toFixed(0),
      unit: 'kWh',
      change: `${dailyView.length} dias`,
      valueColor: 'text-purple-600',
      bgColor: 'bg-gradient-to-br from-purple-50 to-purple-100',
      changeColor: 'text-purple-500'
    }
  ]

  // Prepare chart data from monthly API data
  const chartLabels = monthlyData.map(item => item.label)
  
  // Separar dados reais e predição
  const realMonths = monthlyData.filter(item => !item.is_prediction)
  const predictionMonths = monthlyData.filter(item => item.is_prediction)
  
  console.log('📊 Dados mensais:', monthlyData)
  console.log('✅ Meses reais:', realMonths.length)
  console.log('🔮 Predições:', predictionMonths.length)
  
  // Array de consumo real (verde) - termina em outubro
  const realConsumption = chartLabels.map((label, index) => {
    const monthData = monthlyData[index]
    return monthData.is_prediction ? null : monthData.energy_kwh
  })
  
  // Array de predição (laranja) - começa no último mês real e vai até o mês de predição
  const predictionData = chartLabels.map((label, index) => {
    const monthData = monthlyData[index]
    
    // Se for o mês de predição, mostrar o valor
    if (monthData.is_prediction) {
      return monthData.energy_kwh
    }
    
    // Se for o último mês real (outubro), também mostrar para conectar a linha
    if (index === realMonths.length - 1) {
      return monthData.energy_kwh
    }
    
    return null
  })
  
  console.log('🟢 Consumo Real:', realConsumption)
  console.log('🟠 Predição:', predictionData)

  const chartData = {
    labels: chartLabels,
    datasets: [
      {
        label: 'Consumo Real',
        data: realConsumption,
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        borderWidth: 3,
        pointBackgroundColor: '#10b981',
        pointBorderColor: '#10b981',
        pointRadius: 5,
        pointHoverRadius: 7,
        tension: 0.4,
        fill: false
      },
      {
        label: 'Predição',
        data: predictionData,
        borderColor: '#f97316',
        backgroundColor: 'rgba(249, 115, 22, 0.1)',
        borderWidth: 3,
        borderDash: [5, 5],
        pointBackgroundColor: '#f97316',
        pointBorderColor: '#f97316',
        pointRadius: 5,
        pointHoverRadius: 7,
        tension: 0.4,
        fill: false
      }
    ]
  }

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          usePointStyle: true,
          padding: 20,
          font: {
            size: 12
          }
        }
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: 'rgba(255, 255, 255, 0.1)',
        borderWidth: 1
      }
    },
    scales: {
      x: {
        grid: {
          display: true,
          color: 'rgba(0, 0, 0, 0.1)'
        },
        ticks: {
          font: {
            size: 11
          }
        }
      },
      y: {
        grid: {
          display: true,
          color: 'rgba(0, 0, 0, 0.1)'
        },
        ticks: {
          font: {
            size: 11
          }
        },
        beginAtZero: false
      }
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false
    }
  }

  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg border border-gray-100">
      <h3 className="text-xl font-bold text-gray-900 mb-6">Comparação Histórica</h3>
      
      <div className="grid grid-cols-2 gap-4 mb-8">
        {comparisons.map((item, index) => (
          <div key={index} className={`text-center p-5 ${item.bgColor} rounded-xl border border-opacity-20 hover:shadow-md transition-shadow duration-200`}>
            <div className={`text-3xl font-bold ${item.valueColor} mb-1`}>
              {item.value}
              <span className="text-lg text-gray-500 ml-1">{item.unit}</span>
            </div>
            <div className="text-sm text-gray-700 font-medium mb-1">{item.title}</div>
            <div className={`text-sm font-bold ${item.changeColor}`}>{item.change}</div>
          </div>
        ))}
      </div>

      {/* Gráfico Chart.js */}
      <div className="h-64">
        {chartLoading ? (
          <div className="flex items-center justify-center h-full">
            <p className="text-gray-500">Carregando dados mensais...</p>
          </div>
        ) : monthlyData.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <p className="text-gray-500">Sem dados históricos disponíveis</p>
          </div>
        ) : (
          <Line data={chartData} options={chartOptions} />
        )}
      </div>
    </div>
  )
}

export default ComparisonSection