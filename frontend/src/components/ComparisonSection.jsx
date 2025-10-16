import React from 'react'
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

const ComparisonSection = () => {
  const comparisons = [
    {
      title: 'Mês Anterior',
      value: '163',
      unit: 'kWh',
      change: '+9.2%',
      valueColor: 'text-green-600',
      bgColor: 'bg-gradient-to-br from-green-50 to-green-100',
      changeColor: 'text-red-500'
    },
    {
      title: 'Média Trimestral',
      value: '155',
      unit: 'kWh',
      change: '+14.8%',
      valueColor: 'text-blue-600',
      bgColor: 'bg-gradient-to-br from-blue-50 to-blue-100',
      changeColor: 'text-red-500'
    },
    {
      title: 'Previsão para o Próximo Mês',
      value: '287',
      unit: 'kWh',
      change: '+25.4%',
      valueColor: 'text-orange-600',
      bgColor: 'bg-gradient-to-br from-orange-50 to-orange-100',
      changeColor: 'text-red-500'
    },
    {
      title: 'Média Anual',
      value: '168',
      unit: 'kWh',
      change: '+6%',
      valueColor: 'text-purple-600',
      bgColor: 'bg-gradient-to-br from-purple-50 to-purple-100',
      changeColor: 'text-red-500'
    }
  ]

  const chartData = {
    labels: ['Set', 'Out', 'Nov', 'Dez', 'Jan (Prev)', 'Fev (Prev)'],
    datasets: [
      {
        label: 'Consumo Real',
        data: [135, 160, 170, null, null, null],
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
        data: [null, null, 170, 175, 172, 180],
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
        min: 120,
        max: 200
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
        <Line data={chartData} options={chartOptions} />
      </div>
    </div>
  )
}

export default ComparisonSection