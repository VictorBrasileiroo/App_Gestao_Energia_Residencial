import React from 'react'
import { Download } from 'lucide-react'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Bar } from 'react-chartjs-2'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

const DailyConsumption = ({ data }) => {
    const dailyView = data?.daily_view_last_7_days?.series || []
    
    // GAMBIARRA: Mascarar datas para parecer outubro 2025 (22-28 de outubro)
    const labels = dailyView.map((d, index) => {
        // Criar datas fixas de outubro 2025 para os últimos 7 dias
        const octoberDates = [
            new Date(2025, 9, 22), // 22 de outubro (Ter)
            new Date(2025, 9, 23), // 23 de outubro (Qua)
            new Date(2025, 9, 24), // 24 de outubro (Qui)
            new Date(2025, 9, 25), // 25 de outubro (Sex)
            new Date(2025, 9, 26), // 26 de outubro (Sáb)
            new Date(2025, 9, 27), // 27 de outubro (Dom)
            new Date(2025, 9, 28), // 28 de outubro (Seg)
        ]
        
        // Usar as datas mascaradas ao invés das datas reais do CSV
        const maskedDate = octoberDates[index] || new Date(d.date)
        return maskedDate.toLocaleDateString('pt-BR', { weekday: 'short' }).replace('.', '')
    })
    
    const values = dailyView.map(d => d.energy_kwh)
    
    const chartData = {
        labels: labels.length > 0 ? labels : ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
        datasets: [
            {
                label: 'Consumo (kWh)',
                data: values.length > 0 ? values : [0, 0, 0, 0, 0, 0, 0],
                backgroundColor: [
                    '#10b981',  // Verde
                    '#059669',  // Verde escuro
                    '#06b6d4',  // Cyan
                    '#3b82f6',  // Azul
                    '#6366f1',  // Índigo
                    '#8b5cf6',  // Violeta
                    '#ec4899'   // Rosa
                ],
                borderColor: [
                    '#059669',
                    '#047857',
                    '#0891b2',
                    '#2563eb',
                    '#4f46e5',
                    '#7c3aed',
                    '#db2777'
                ],
                borderWidth: 2,
                borderRadius: 8,
                borderSkipped: false
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
                borderWidth: 1,
                callbacks: {
                    label: function(context) {
                        return `${context.parsed.y} kWh`
                    }
                }
            }
        },
        scales: {
            x: {
                grid: {
                    display: false
                },
                ticks: {
                    font: {
                        size: 12,
                        weight: 'bold'
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
                    },
                    callback: function(value) {
                        return value + ' kWh'
                    }
                },
                beginAtZero: true,
                max: 20
            }
        }
    }

    return (
        <div className='bg-white p-6 rounded-2xl shadow-lg border border-gray-100'>
            <div className='flex justify-between items-center mb-6'>
                <h3 className='text-xl font-bold text-gray-900'>Consumo Diário (Última Semana)</h3>
                <button className='flex items-center gap-2 text-green-600 hover:text-green-700 text-sm font-medium bg-green-50 px-3 py-2 rounded-lg hover:bg-green-100 transition-colors'>
                    <Download size={16} />
                    Exportar
                </button>
            </div>

            {/* Gráfico Chart.js */}
            <div className='h-64'>
                <Bar data={chartData} options={chartOptions} />
            </div>
        </div>
    )
}

export default DailyConsumption