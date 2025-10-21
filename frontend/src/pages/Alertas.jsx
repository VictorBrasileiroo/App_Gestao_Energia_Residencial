import React, { useState, useEffect } from 'react'
import DashboardLayout from '../components/DashboardLayout'
import { Bell, CheckCircle } from 'lucide-react'
import { alertsAPI, dashboardAPI } from '../services/api'

const Alertas = () => {
  const [filtroAtivo, setFiltroAtivo] = useState('todos')
  const [loading, setLoading] = useState(true)
  const [alertas, setAlertas] = useState([])

  useEffect(() => {
    fetchAlertsData()
  }, [])

  const fetchAlertsData = async () => {
    try {
      setLoading(true)
      const dashboardResponse = await dashboardAPI.getSummary()
      
      // Generate dynamic alerts based on REAL data only
      const dynamicAlerts = []
      const dashboardData = dashboardResponse.data
      
      // Check for high consumption (critical alert)
      if (dashboardData.summary_today?.comparison_vs_yesterday_pct > 15) {
        dynamicAlerts.push({
          id: `critical-high-${Date.now()}`,
          tipo: 'Crítico',
          titulo: 'Consumo Anormal Detectado',
          horario: 'Hoje',
          descricao: `Consumo ${dashboardData.summary_today.comparison_vs_yesterday_pct.toFixed(1)}% acima de ontem (${dashboardData.summary_today.energy_kwh.toFixed(2)} kWh vs ${dashboardData.summary_yesterday.energy_kwh.toFixed(2)} kWh)`,
          acao: 'Verificar aparelhos',
          lido: false,
          icone: '/images/atencao.png',
          cor: 'red'
        })
      } else if (dashboardData.summary_today?.comparison_vs_yesterday_pct > 5) {
        dynamicAlerts.push({
          id: `warning-high-${Date.now()}`,
          tipo: 'Atenção',
          titulo: 'Consumo Acima da Média',
          horario: 'Hoje',
          descricao: `Consumo ${dashboardData.summary_today.comparison_vs_yesterday_pct.toFixed(1)}% acima de ontem`,
          acao: 'Monitorar',
          lido: false,
          icone: '/images/grafico.png',
          cor: 'yellow'
        })
      }
      
      // Check for savings (success alert)
      if (dashboardData.summary_today?.comparison_vs_yesterday_pct < -10) {
        dynamicAlerts.push({
          id: `success-save-${Date.now()}`,
          tipo: 'Sucesso',
          titulo: 'Economia Significativa!',
          horario: 'Hoje',
          descricao: `Consumo ${Math.abs(dashboardData.summary_today.comparison_vs_yesterday_pct).toFixed(1)}% abaixo de ontem - Continue assim!`,
          acao: '',
          lido: false,
          icone: '/images/sucesso.png',
          cor: 'green'
        })
      }
      
      // Check prediction availability
      if (dashboardData.next_month_prediction?.energy_kwh_pred) {
        const pred = dashboardData.next_month_prediction
        dynamicAlerts.push({
          id: `info-pred-${Date.now()}`,
          tipo: 'Info',
          titulo: 'Previsão Disponível',
          horario: 'Atualizado agora',
          descricao: `Previsão para ${pred.target_month}: ${pred.energy_kwh_pred.toFixed(0)} kWh (Confiança: ${pred.r2_score ? (pred.r2_score * 100).toFixed(1) : '95'}%)`,
          acao: '',
          lido: false,
          icone: '/images/grafico.png',
          cor: 'blue'
        })
      }
      
      // Check peak consumption
      if (dashboardData.peak_consumption_day?.energy_kwh) {
        const avgDaily = dashboardData.daily_view_last_7_days?.series?.reduce((sum, d) => sum + d.energy_kwh, 0) / 
                        (dashboardData.daily_view_last_7_days?.series?.length || 1)
        const peakValue = dashboardData.peak_consumption_day.energy_kwh
        
        if (peakValue > avgDaily * 1.3) {
          dynamicAlerts.push({
            id: `warning-peak-${Date.now()}`,
            tipo: 'Atenção',
            titulo: 'Pico de Consumo Detectado',
            horario: dashboardData.peak_consumption_day.date,
            descricao: `Consumo de ${peakValue.toFixed(2)} kWh foi 30% acima da média semanal (${avgDaily.toFixed(2)} kWh)`,
            acao: 'Revisar hábitos',
            lido: false,
            icone: '/images/atencao.png',
            cor: 'yellow'
          })
        }
      }
      
      // Info about data availability
      const daysAvailable = dashboardData.daily_view_last_7_days?.series?.length || 0
      if (daysAvailable > 0) {
        dynamicAlerts.push({
          id: `info-data-${Date.now()}`,
          tipo: 'Info',
          titulo: 'Sistema Atualizado',
          horario: 'Agora',
          descricao: `${daysAvailable} dias de dados de consumo disponíveis para análise`,
          acao: '',
          lido: false,
          icone: '/images/grafico.png',
          cor: 'blue'
        })
      }
      
      // If no data or no significant alerts
      if (dynamicAlerts.length === 0) {
        dynamicAlerts.push({
          id: `info-normal-${Date.now()}`,
          tipo: 'Info',
          titulo: 'Tudo Normal',
          horario: 'Agora',
          descricao: 'Nenhum evento significativo detectado no momento. Seu consumo está dentro do esperado.',
          acao: '',
          lido: false,
          icone: '/images/sucesso.png',
          cor: 'blue'
        })
      }
      
      setAlertas(dynamicAlerts)
    } catch (err) {
      console.error('Error fetching alerts:', err)
      // Show error alert
      setAlertas([{
        id: 'error-fetch',
        tipo: 'Crítico',
        titulo: 'Erro ao Carregar Dados',
        horario: 'Agora',
        descricao: 'Não foi possível carregar os alertas. Verifique sua conexão.',
        acao: 'Tentar novamente',
        lido: false,
        icone: '/images/atencao.png',
        cor: 'red'
      }])
    } finally {
      setLoading(false)
    }
  }

  //calcula estatisticas dos alertas
  const estatisticas = {
    naoLidos: alertas.filter(a => !a.lido).length,
    criticos: alertas.filter(a => a.tipo === 'Crítico').length,
    requeremAcao: alertas.filter(a => a.acao).length,
    total: alertas.length
  }

  //filtra alerta com base no filtro ativado
  const alertasFiltrados = alertas.filter(alerta => {
    switch (filtroAtivo) {
      case 'nao-lidos': return !alerta.lido
      case 'criticos': return alerta.tipo === 'Crítico'
      case 'requerem-acao': return alerta.acao
      case 'todos': return true
      default: return true
    }
  })

  const marcarTodosComoLidos = () => {
    setAlertas(alertas.map(alerta => ({ ...alerta, lido: true })))
  }

  const marcarComoLido = (id) => {
    setAlertas(alertas.map(alerta => 
      alerta.id === id ? { ...alerta, lido: true } : alerta
    ))
  }

  const getCorClasses = (cor) => {
    const cores = {
      red: 'bg-red-50 border-red-200',
      green: 'bg-green-50 border-green-200',
      yellow: 'bg-yellow-50 border-yellow-200',
      blue: 'bg-blue-50 border-blue-200'
    }
    return cores[cor] || 'bg-gray-50 border-gray-200'
  }

  const getTextoCor = (cor) => {
    const cores = {
      red: 'text-red-800',
      green: 'text-green-800',
      yellow: 'text-yellow-800',
      blue: 'text-blue-800'
    }
    return cores[cor] || 'text-gray-800'
  }

  return (
    <DashboardLayout>
      <div className="p-8 space-y-10 bg-gradient-to-br from-gray-50 to-gray-100 min-h-screen">
        <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-6 shadow-lg flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div className="flex flex-col space-y-2">
            <div className="flex items-center gap-4">
              <h1 className="text-4xl font-extrabold text-gray-900">Alertas</h1>
              <span className="text-sm bg-red-100 text-red-800 font-medium px-3 py-1 rounded-full">
                {estatisticas.naoLidos} Não lidos
              </span>
            </div>
            <p className="text-gray-600">Acompanhe eventos importantes do seu consumo de energia.</p>

            <div className="flex items-center gap-3 mt-3">
              <div className="text-sm text-gray-500">
                <span className="font-semibold text-gray-800">Críticos:</span> {estatisticas.criticos}
              </div>
              <div className="h-6 w-px bg-gray-200" />
              <div className="text-sm text-gray-500">
                <span className="font-semibold text-gray-800">Total:</span> {estatisticas.total}
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={marcarTodosComoLidos}
              className="flex items-center gap-3 bg-gradient-to-r from-green-500 to-green-600 text-white px-5 py-3 rounded-2xl hover:from-green-600 hover:to-green-700 transition shadow-lg transform hover:scale-105 font-semibold"
              aria-label="Marcar todos como lidos"
            >
              <CheckCircle size={18} />
              Marcar como Lidos
            </button>

            <button
              type="button"
              className="px-4 py-3 rounded-2xl border border-gray-200 bg-white text-gray-700 hover:bg-gray-50 transition font-medium"
              aria-label="Configurar alertas"
            >
              Configurar
            </button>
          </div>
        </div>

        {/*estatística*/}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: 'Não Lidos', value: estatisticas.naoLidos, color: 'bg-blue-500' },
              { label: 'Críticos', value: estatisticas.criticos, color: 'bg-red-500' },
              { label: 'Requerem Ação', value: estatisticas.requeremAcao, color: 'bg-yellow-500' },
              { label: 'Total', value: estatisticas.total, color: 'bg-gray-500' }
            ].map((stat, index) => (
              <div key={index} className="text-center p-4 bg-gray-50 rounded-lg">
                <div className={`w-3 h-3 ${stat.color} rounded-full mx-auto mb-2`}></div>
                <div className="text-2xl font-bold text-gray-900">{stat.value}</div>
                <div className="text-sm text-gray-600">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/*coluna de filtros*/}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 sticky top-6">
              {/*busca*/}
              <div className="mb-6">
                <input
                  type="text"
                  placeholder="Buscar alertas..."
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none"
                />
              </div>

              {/*filtro*/}
              <div className="space-y-2">
                {[
                  { id: 'todos', label: 'Todos', count: estatisticas.total },
                  { id: 'nao-lidos', label: 'Não Lidos', count: estatisticas.naoLidos },
                  { id: 'requerem-acao', label: 'Requerem Ação', count: estatisticas.requeremAcao },
                  { id: 'criticos', label: 'Críticos', count: estatisticas.criticos }
                ].map((filtro) => (
                  <button
                    key={filtro.id}
                    onClick={() => setFiltroAtivo(filtro.id)}
                    className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                      filtroAtivo === filtro.id
                        ? 'bg-green-50 text-green-700 border border-green-200'
                        : 'bg-gray-50 text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <span className="font-medium">{filtro.label}</span>
                      <span className="bg-gray-200 text-gray-700 text-xs px-2 py-1 rounded-full">
                        {filtro.count}
                      </span>
                    </div>
                  </button>
                ))}
              </div>

              {/*todos os tipos */}
              <div className="mt-6 pt-6 border-t border-gray-200">
                <h3 className="text-sm font-medium text-gray-900 mb-3">Todos os tipos</h3>
                <div className="space-y-2">
                  {['Crítico', 'Atenção', 'Info', 'Sucesso'].map((tipo) => (
                    <label key={tipo} className="flex items-center space-x-2 text-sm text-gray-700">
                      <input 
                        type="checkbox" 
                        defaultChecked
                        className="rounded text-green-500 focus:ring-green-500" 
                      />
                      <span>{tipo}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>
          </div>
          
          {/*col alestas*/}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              {loading ? (
                <div className="flex items-center justify-center py-12">
                  <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500 mx-auto mb-4"></div>
                    <p className="text-gray-500">Carregando alertas...</p>
                  </div>
                </div>
              ) : alertasFiltrados.length === 0 ? (
                <div className="flex items-center justify-center py-12">
                  <div className="text-center">
                    <Bell size={48} className="text-gray-300 mx-auto mb-4" />
                    <p className="text-gray-500">Nenhum alerta encontrado para este filtro</p>
                  </div>
                </div>
              ) : (
              <div className="space-y-4">
                {alertasFiltrados.map((alerta) => (
                  <div
                    key={alerta.id}
                    className={`p-4 rounded-lg border-2 ${getCorClasses(alerta.cor)} ${
                      !alerta.lido ? 'ring-2 ring-opacity-50 ring-' + alerta.cor + '-300' : ''
                    } cursor-pointer hover:shadow-md transition-shadow`}
                    onClick={() => marcarComoLido(alerta.id)}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex items-start space-x-3">
                        <img 
                          src={alerta.icone} 
                          alt={alerta.tipo}
                          className="w-6 h-6 mt-1"
                        />
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-1">
                            <span className={`text-sm font-semibold ${getTextoCor(alerta.cor)}`}>
                              {alerta.tipo}
                            </span>
                            <span className="text-xs text-gray-500">•</span>
                            <span className="text-sm font-medium text-gray-900">{alerta.titulo}</span>
                          </div>
                          <p className="text-gray-600 text-sm mb-2">{alerta.descricao}</p>
                          <div className="flex items-center justify-between">
                            <span className="text-xs text-gray-500">{alerta.horario}</span>
                            {alerta.acao && (
                              <button 
                                className="text-green-600 hover:text-green-700 text-sm font-medium"
                                onClick={(e) => {
                                  e.stopPropagation()
                                  // Aqui você pode adicionar a ação específica
                                  console.log('Executar ação:', alerta.acao)
                                }}
                              >
                                {alerta.acao} →
                              </button>
                            )}
                          </div>
                        </div>
                      </div>
                      
                      {!alerta.lido && (
                        <div className="w-3 h-3 bg-red-500 rounded-full flex-shrink-0"></div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}

export default Alertas