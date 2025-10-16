import React from 'react'
import DashboardLayout from '../components/DashboardLayout'
import StatsCardsRelatorios from '../components/StatsCardsRelatorios'
import ConsumptionChart from '../components/ConsumptionChart'
import MonthlySaving from '../components/MonthlySaving'
import WeeklyAnalysis from '../components/WeeklyAnalysis'

const Relatorios = () => {
    return (
        <DashboardLayout>
            <div className='p-6 space-y-6  bg-green-00'>
                {/*corpo*/}
                <div className='flex justify-between items-center'>
                    <div>
                        <h1 className='text-2xl font-bold text-gray-900'>Relatórios</h1>
                        <p className='text-gray-600'>Análise detalhada do consumo de energia</p>
                    </div>
                    <div className='flex gap-2'>
                        <button className='bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition-colors'>
                            Este Mês
                        </button>
                        <button className='bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition-colors'>
                            Exportar PDF
                        </button>
                    </div>
                </div>

                {/*statscards*/}
                <StatsCardsRelatorios />

                {/*tabs e gráficos*/}
                <div className='flex gap-4 border-b border-gray-200'>
                    {['Comparativo', 'Detalhado', 'Tendências'].map((tab) => (
                        <button
                        key={tab}
                        className={`pb-3 px-1 font-medium ${
                            tab === 'Comparativo'
                            ? 'text-green-600 border-b-2 border-green-600'
                            : 'text-gray-500 hover:text-gray-700' 
                        }`}>
                        {tab}
                        </button>
                    ))}
                </div>

                {/*chards grid*/}
                <div className='grid grid-cols-1 lg:grid-cols-2 gap-6'>
                    {/*col esquerda*/}
                    <div className='space-y-6'>
                        <ConsumptionChart />
                        <WeeklyAnalysis />
                    </div>

                    {/*col direita*/}
                    <div className='space-y-6'>
                        <MonthlySaving />
                    </div>
                </div>
            </div>
        </DashboardLayout>
    )
}

export default Relatorios