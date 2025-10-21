import React, { useState, useEffect } from 'react'
import DashboardLayout from '../components/DashboardLayout'
import StatsCardsRelatorios from '../components/StatsCardsRelatorios'
import ConsumptionChart from '../components/ConsumptionChart'
import MonthlySaving from '../components/MonthlySaving'
import WeeklyAnalysis from '../components/WeeklyAnalysis'
import { FileText, Download } from 'lucide-react'
import { reportsAPI, dashboardAPI } from '../services/api'

const Relatorios = () => {
    const [reportData, setReportData] = useState(null)
    const [dashboardData, setDashboardData] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetchReportData()
    }, [])

    const fetchReportData = async () => {
        try {
            setLoading(true)
            const [reportResponse, dashboardResponse] = await Promise.all([
                reportsAPI.getSummary(),
                dashboardAPI.getSummary()
            ])
            setReportData(reportResponse.data)
            setDashboardData(dashboardResponse.data)
        } catch (err) {
            console.error('Error fetching report data:', err)
        } finally {
            setLoading(false)
        }
    }

    if (loading) {
        return (
            <DashboardLayout>
                <div className='flex items-center justify-center min-h-screen'>
                    <div className='text-xl'>Carregando relatórios...</div>
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
                            <h1 className="text-4xl font-extrabold text-gray-900">Relatórios</h1>
                            <span className="text-sm bg-blue-100 text-blue-800 font-medium px-3 py-1 rounded-full">Análise Completa</span>
                        </div>
                        <p className="text-gray-600">Análise detalhada do consumo de energia com insights avançados.</p>

                        <div className="flex items-center gap-3 mt-3">
                            <div className="text-sm text-gray-500">
                                <span className="font-semibold text-gray-800">Período:</span> Últimos 30 dias
                            </div>
                            <div className="h-6 w-px bg-gray-200" />
                            <div className="text-sm text-gray-500">
                                <span className="font-semibold text-gray-800">Atualizado:</span> Agora
                            </div>
                        </div>
                    </div>

                    <div className="flex items-center gap-3">
                        <button
                            type="button"
                            className="flex items-center gap-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white px-5 py-3 rounded-2xl hover:from-blue-600 hover:to-blue-700 transition shadow-lg transform hover:scale-105 font-semibold"
                            aria-label="Este mês"
                        >
                            <FileText size={18} />
                            Este Mês
                        </button>

                        <button
                            type="button"
                            className="flex items-center gap-3 bg-gradient-to-r from-green-500 to-green-600 text-white px-5 py-3 rounded-2xl hover:from-green-600 hover:to-green-700 transition shadow-lg transform hover:scale-105 font-semibold"
                            aria-label="Exportar PDF"
                        >
                            <Download size={18} />
                            Exportar PDF
                        </button>
                    </div>
                </div>

                {/*statscards*/}
                <StatsCardsRelatorios data={reportData} />

                {/*tabs e gráficos*/}
                <div className='bg-white rounded-2xl p-6 shadow-lg'>
                    <div className='flex gap-6 border-b border-gray-200 mb-6'>
                        {['Comparativo', 'Detalhado', 'Tendências'].map((tab) => (
                            <button
                            key={tab}
                            className={`pb-4 px-4 font-semibold transition-all duration-200 ${
                                tab === 'Comparativo'
                                ? 'text-green-600 border-b-3 border-green-600 bg-green-50 rounded-t-lg'
                                : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50 rounded-t-lg' 
                            }`}>
                            {tab}
                            </button>
                        ))}
                    </div>

                    {/*charts grid*/}
                    <div className='grid grid-cols-1 lg:grid-cols-2 gap-8'>
                        {/*col esquerda*/}
                        <div className='space-y-8'>
                            <WeeklyAnalysis data={dashboardData} />
                            <ConsumptionChart data={dashboardData} />
                        </div>

                        {/*col direita*/}
                        <div className='space-y-8'>
                            <MonthlySaving data={reportData} />
                        </div>
                    </div>
                </div>
            </div>
        </DashboardLayout>
    )
}

export default Relatorios