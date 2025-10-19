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

const DailyConsumption = () => {
    const chartData = {
        labels: ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
        datasets: [
            {
                label: 'Consumo (kWh)',
                data: [12, 15, 11, 16, 14, 17, 18],
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