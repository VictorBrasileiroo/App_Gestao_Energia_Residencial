import React from 'react'
import DashboardLayout from '../components/DashboardLayout'
import StatsCards from '../components/StatsCards'
import ConsumptionChart from '../components/ConsumptionChart'
import ComparisonSection from '../components/ComparisonSection'
import DailyConsumption from '../components/DailyConsumption' 
import PredictionCard from '../components/PredictionCard'
import { Download } from 'lucide-react'

const Dashboard = () => {
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
                <span className="font-semibold text-gray-800">Usuário:</span> Família Silva
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              type="button"
              className="flex items-center gap-3 bg-gradient-to-r from-green-500 to-green-600 text-white px-5 py-3 rounded-2xl hover:from-green-600 hover:to-green-700 transition shadow-lg transform hover:scale-105 font-semibold"
              aria-label="Exportar relatório"
            >
              <Download size={18} />
              Exportar Relatório
            </button>

            <button
              type="button"
              className="px-4 py-3 rounded-2xl border border-gray-200 bg-white text-gray-700 hover:bg-gray-50 transition font-medium"
              aria-label="Ver filtros"
            >
              Ver filtros
            </button>
          </div>
        </div>

        {/* statscards */}
        <StatsCards />

        <div className='grid grid-cols-1 lg:grid-cols-3 gap-8'>
          {/*col esquerda - comparação histórica*/}
          <div className='lg:col-span-2 space-y-8'>
            <ComparisonSection />
            <ConsumptionChart />
          </div>

          {/*col direita - consumo diário e predição*/}
          <div className='space-y-8'>
            <DailyConsumption />
            <PredictionCard />
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}

export default Dashboard