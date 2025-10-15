import React, { useState } from 'react'
import DashboardLayout from '../components/DashboardLayout'

const Alertas = () => {
  const [filtroAtivo, setFiltroAtivo] = useState('todos')
  const [alertas, setAlertas] = useState([
    {
      id: 1,
      tipo: 'Crítico',
      titulo: 'Consumo Anormal',
      horario: 'Hoje às 14:32',
      descricao: 'Consumo 15% acima da média para este horário',
      acao: 'Verificar aparelhos',
      lido: false,
      icone: '/images/atencao.png',
      cor: 'red'
    },

    {
      id: 2,
      tipo: 'Sucesso',
      titulo: 'Meta',
      horario: 'Hoje às 12:15',
      descricao: 'Meta mensal de economia foi alcançada!',
      acao: '',
      lido: false,
      icone: '/images/success.png',
      cor: 'green'
    },

    {
      id: 3,
      tipo: 'Atenção',
      titulo: 'Pico de Consumo',
      horario: 'Ontem às 19:30',
      descricao: 'Pico de consumo detectado no período da noite',
      acao: 'Revisar hábitos',
      lido: true,
      icone: '/images/grafico.png',
      cor: 'yellow'
    },
    
    {
      id: 4,
      tipo: 'Info',
      titulo: 'Manutenção Preventiva',
      horario: '2 dias atrás',
      descricao: 'Recomendada manutenção preventiva para o próximo mês',
      acao: 'Agendar',
      lido: true,
      icone: '/images/manutencao.png',
      cor: 'blue'
    },
    {
      id: 5,
      tipo: 'Crítico',
      titulo: 'Dispositivo Inativo',
      horario: '3 dias atrás',
      descricao: 'Sensor de consumo parou de enviar dados',
      acao: 'Verificar conexão',
      lido: true,
      icone: '/images/atencao.png',
      cor: 'red'
    }
  ])

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
      <div className="p-6 space-y-6">
        {/*head de estaticias*/}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Alertas e Notificações</h1>
              <p className="text-gray-600 mt-1">Acompanhe eventos importantes do seu consumo</p>
            </div>
            <button 
              onClick={marcarTodosComoLidos}
              className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition-colors"
            >
              Marcar todos como lidos
            </button>
          </div>

          {/*estatistica*/}
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
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}

export default Alertas