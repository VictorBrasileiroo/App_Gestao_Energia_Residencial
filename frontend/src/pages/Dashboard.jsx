import React from 'react'
import DashboardLayout from '../components/DashboardLayout'
import StatsCards from '../components/StatsCards'
import ConsumptionChart from '../components/ConsumptionChart'
import ComparisonSection from '../components/ComparisonSection'
import DailyConsumption from '../components/DailyConsumption' 
import PredictionCard from '../components/PredictionCard'
import TipsCard from '../components/TipsCard'

const Dashboard = () => {
  return (
    <DashboardLayout>
      <div className='p-6 space-y-6'>
        {/*header*/}
        <div className='flex justify-between items-center'>
          <h1 className='text-2xl font-bold text-gray-900'>Dashboard</h1>
          <button className='bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition-colors'>
            Exportar Relatório
          </button>
        </div>

        <p className='text-gray-600'>Visão geral do seu consumo de energia</p>

        {/*statscards*/}
        <StatsCards />

        <div className='grid grid-cols-1 lg:grid-cols-2 gap-6'>
          {/*col esquerda*/}
          <div className='space-y-6'>
            <ComparisonSection />
            <DailyConsumption />
          </div>

          {/*col direito*/}
          <div className='space-y-6'>
            <PredictionCard />
            <TipsCard />
          </div>
        </div>

        <ConsumptionChart />
      </div>
    </DashboardLayout>
  )
}

export default Dashboard