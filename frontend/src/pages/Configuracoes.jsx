import React, { useState } from 'react'
import DashboardLayout from '../components/DashboardLayout'
import { Settings, Download } from 'lucide-react'

const Configuracoes = () => {
  const [configuracoes, setConfiguracoes] = useState({
    notificacoesEmail: true,
    notificacoesAlertas: true,
    modoEscuro: false,
    idioma: 'pt-br',
    unidadeEnergia: 'kwh'
  })

  const handleToggle = (config) => {
    setConfiguracoes(prev => ({
      ...prev,
      [config]: !prev[config]
    }))
  }

  const handleSelectChange = (config, value) => {
    setConfiguracoes(prev => ({
      ...prev,
      [config]: value
    }))
  }

  const salvarConfiguracoes = () => {
    //integração com back
    alert('Configurações salvas com sucesso!')
  }

  return (
    <DashboardLayout>
      <div className="p-6 max-w-4xl mx-auto bg-green-00">
        {/* Header */}
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-sm border border-gray-100 p-6 mb-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="bg-gradient-to-r from-green-500 to-green-600 p-3 rounded-xl shadow-lg">
                <Settings className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  Configurações
                </h1>
                <p className="text-gray-600 mt-1">
                  Gerencie suas preferências e configurações da conta
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <span className="bg-green-100 text-green-800 text-sm font-medium px-3 py-1 rounded-full">
                Sistema Ativo
              </span>
              <button className="bg-gradient-to-r from-green-500 to-green-600 text-white px-4 py-2 rounded-lg hover:from-green-600 hover:to-green-700 transition-all duration-200 flex items-center space-x-2 shadow-md">
                <Download className="w-4 h-4" />
                <span>Exportar Config</span>
              </button>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-sm p-8 mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Preferências de Notificação</h2>
          
          <div className="space-y-6">
            {/*notoficação por email*/}
            <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
              <div>
                <h3 className="font-medium text-gray-900">Notificações por Email</h3>
                <p className="text-sm text-gray-500">Receba alertas e relatórios por email</p>
              </div>
              <button
                onClick={() => handleToggle('notificacoesEmail')}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  configuracoes.notificacoesEmail ? 'bg-green-500' : 'bg-gray-300'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    configuracoes.notificacoesEmail ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>

            {/*alertas em tempo real*/}
            <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
              <div>
                <h3 className="font-medium text-gray-900">Alertas em Tempo Real</h3>
                <p className="text-sm text-gray-500">Notificações instantâneas sobre consumo</p>
              </div>
              <button
                onClick={() => handleToggle('notificacoesAlertas')}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  configuracoes.notificacoesAlertas ? 'bg-green-500' : 'bg-gray-300'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    configuracoes.notificacoesAlertas ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-sm p-8 mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Configurações Gerais</h2>
          
          <div className="space-y-6">
            {/*idioma*/}
            <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
              <div>
                <h3 className="font-medium text-gray-900">Idioma</h3>
                <p className="text-sm text-gray-500">Selecione o idioma da interface</p>
              </div>
              <select
                value={configuracoes.idioma}
                onChange={(e) => handleSelectChange('idioma', e.target.value)}
                className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                <option value="pt-br">Português (BR)</option>
                <option value="en">English</option>
                <option value="es">Español</option>
              </select>
            </div>

            {/*Unidade de energia*/}
            <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
              <div>
                <h3 className="font-medium text-gray-900">Unidade de Energia</h3>
                <p className="text-sm text-gray-500">Unidade de medida para consumo</p>
              </div>
              <select
                value={configuracoes.unidadeEnergia}
                onChange={(e) => handleSelectChange('unidadeEnergia', e.target.value)}
                className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                <option value="kwh">kWh</option>
                <option value="mwh">MWh</option>
                <option value="j">Joules</option>
              </select>
            </div>
          </div>
        </div>

        {/*bt de salvar*/}
        <div className="text-center">
          <button
            onClick={salvarConfiguracoes}
            className="bg-green-500 text-white px-8 py-3 rounded-lg hover:bg-green-600 transition-colors font-medium"
          >
            Salvar Configurações
          </button>
        </div>
      </div>
    </DashboardLayout>
  )
}

export default Configuracoes