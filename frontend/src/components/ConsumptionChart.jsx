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

const ConsumptionChart = () => {
  // Dados para Evolução Mensal
  const monthlyData = {
    labels: ['Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul'],
    datasets: [
      {
        label: 'Consumo (kWh)',
        data: [270, 280, 285, 290, 295, 300],
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        borderWidth: 3,
        pointBackgroundColor: '#10b981',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2,
        pointRadius: 6,
        pointHoverRadius: 8,
        tension: 0.4,
        fill: true
      }
    ]
  }

  // Dados para Padrão de Consumo por Horário
  const hourlyData = {
    labels: ['00h', '04h', '08h', '12h', '16h', '20h'],
    datasets: [
      {
        label: 'Consumo por Hora (kW)',
        data: [1.2, 0.8, 2.5, 4.8, 6.2, 5.1],
        borderColor: '#f59e0b',
        backgroundColor: 'rgba(245, 158, 11, 0.2)',
        borderWidth: 3,
        pointBackgroundColor: '#f59e0b',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2,
        pointRadius: 6,
        pointHoverRadius: 8,
        tension: 0.4,
        fill: true
      }
    ]
  }

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
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
            size: 12
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
        }
      }
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false
    }
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Evolução Mensal */}
      <div className="bg-white p-6 rounded-2xl shadow-lg border border-gray-100">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-bold text-gray-900">Evolução Mensal</h3>
          <div className="text-sm text-green-600 font-medium bg-green-50 px-3 py-1 rounded-full">+2.8%</div>
        </div>
        
        <div className="h-64">
          <Line data={monthlyData} options={chartOptions} />
        </div>
      </div>

      {/* Padrão de Consumo por Horário */}
      <div className="bg-white p-6 rounded-2xl shadow-lg border border-gray-100">
        <h3 className="text-xl font-bold text-gray-900 mb-6">Padrão de Consumo por Horário</h3>
        
        <div className="h-64">
          <Line data={hourlyData} options={chartOptions} />
        </div>

        {/* Distribuição por período */}
        <div className="mt-6 grid grid-cols-2 gap-4">
          <div className="flex items-center justify-between bg-blue-50 p-3 rounded-lg">
            <div className="flex items-center">
              <div className="w-3 h-3 rounded-full bg-blue-500 mr-2"></div>
              <span className="text-xs text-gray-700 font-medium">Manhã (6h-12h)</span>
            </div>
            <span className="text-sm font-bold text-blue-700">82 kWh</span>
          </div>
          
          <div className="flex items-center justify-between bg-green-50 p-3 rounded-lg">
            <div className="flex items-center">
              <div className="w-3 h-3 rounded-full bg-green-500 mr-2"></div>
              <span className="text-xs text-gray-700 font-medium">Tarde (12h-18h)</span>
            </div>
            <span className="text-sm font-bold text-green-700">123 kWh</span>
          </div>
          
          <div className="flex items-center justify-between bg-orange-50 p-3 rounded-lg">
            <div className="flex items-center">
              <div className="w-3 h-3 rounded-full bg-orange-500 mr-2"></div>
              <span className="text-xs text-gray-700 font-medium">Noite (18h-00h)</span>
            </div>
            <span className="text-sm font-bold text-orange-700">156 kWh</span>
          </div>
          
          <div className="flex items-center justify-between bg-purple-50 p-3 rounded-lg">
            <div className="flex items-center">
              <div className="w-3 h-3 rounded-full bg-purple-500 mr-2"></div>
              <span className="text-xs text-gray-700 font-medium">Madrugada (00h-6h)</span>
            </div>
            <span className="text-sm font-bold text-purple-700">49 kWh</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ConsumptionChart