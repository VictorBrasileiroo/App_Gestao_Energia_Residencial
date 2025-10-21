import React, { useState, useEffect } from 'react'
import DashboardLayout from '../components/DashboardLayout'
import StatsCards from '../components/StatsCards'
import ConsumptionChart from '../components/ConsumptionChart'
import ComparisonSection from '../components/ComparisonSection'
import DailyConsumption from '../components/DailyConsumption' 
import PredictionCard from '../components/PredictionCard'
import { Download } from 'lucide-react'
import { dashboardAPI, predictionsAPI } from '../services/api'
import { useAuth } from '../contexts/AuthContext'

const Dashboard = () => {
  const { user } = useAuth()
  const [dashboardData, setDashboardData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      const response = await dashboardAPI.getSummary()
      setDashboardData(response.data)
      setError(null)
    } catch (err) {
      console.error('Error fetching dashboard data:', err)
      setError('Erro ao carregar dados do dashboard')
    } finally {
      setLoading(false)
    }
  }

  const handleGeneratePrediction = async () => {
    try {
      await predictionsAPI.generate()
      await fetchDashboardData()
      alert('Predição gerada com sucesso!')
    } catch (err) {
      console.error('Error generating prediction:', err)
      alert('Erro ao gerar predição: ' + (err.response?.data?.detail || err.message))
    }
  }

  if (loading) {
    return (
      <DashboardLayout>
        <div className='flex items-center justify-center min-h-screen'>
          <div className='text-xl'>Carregando dados...</div>
        </div>
      </DashboardLayout>
    )
  }

  if (error) {
    return (
      <DashboardLayout>
        <div className='flex items-center justify-center min-h-screen'>
          <div className='text-xl text-red-600'>{error}</div>
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout>
      <div className='p-8 space-y-10 bg-gradient-to-br from-gray-50 to-gray-100 min-h-screen'>
        <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-6 shadow-lg flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div className="flex flex-col space-y-2">
            <div className="flex items-center gap-4">
              <h1 className="text-4xl font-extrabold text-gray-900">Dashboard</h1>
              <span className="text-sm bg-green-100 text-green-800 font-medium px-3 py-1 rounded-full">Atualizado • Hoje</span>
            </div>
            <p className="text-gray-600">Visão geral do seu consumo de energia com insights e relatórios rápidos.</p>

            <div className="flex items-center gap-3 mt-3">
              <div className="text-sm text-gray-500">
                <span className="font-semibold text-gray-800">Mês:</span> Março 2025
              </div>
              <div className="h-6 w-px bg-gray-200" />
              <div className="text-sm text-gray-500">
                <span className="font-semibold text-gray-800">Usuário:</span> {user?.name || user?.email || 'Usuário'}
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={handleGeneratePrediction}
              className="flex items-center gap-3 bg-gradient-to-r from-purple-500 to-purple-600 text-white px-5 py-3 rounded-2xl hover:from-purple-600 hover:to-purple-700 transition shadow-lg transform hover:scale-105 font-semibold"
              aria-label="Gerar Predição"
            >
              Gerar Predição
            </button>

            <button
              type="button"
              onClick={fetchDashboardData}
              className="flex items-center gap-3 bg-gradient-to-r from-green-500 to-green-600 text-white px-5 py-3 rounded-2xl hover:from-green-600 hover:to-green-700 transition shadow-lg transform hover:scale-105 font-semibold"
              aria-label="Atualizar dados"
            >
              <Download size={18} />
              Atualizar
            </button>
          </div>
        </div>

        {/* statscards */}
        <StatsCards data={dashboardData} />

        <div className='grid grid-cols-1 lg:grid-cols-3 gap-8'>
          {/*col esquerda - comparação histórica*/}
          <div className='lg:col-span-2 space-y-8'>
            <ComparisonSection data={dashboardData} />
            <ConsumptionChart data={dashboardData} />
          </div>

          {/*col direita - consumo diário e predição*/}
          <div className='space-y-8'>
            <DailyConsumption data={dashboardData} />
            <PredictionCard data={dashboardData} />
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}

export default Dashboard