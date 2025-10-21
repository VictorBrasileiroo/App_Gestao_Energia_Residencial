import React from 'react'
import { Brain, TrendingDown, Lightbulb, AlertTriangle } from 'lucide-react'

const PredictionCard = ({ data }) => {
  const prediction = data?.next_month_prediction || {}
  const hasData = prediction.energy_kwh_pred !== null && prediction.energy_kwh_pred !== undefined
  
  if (!hasData) {
    return (
      <div className="bg-white p-6 rounded-2xl shadow-lg border border-gray-100">
        <div className="flex items-center mb-6">
          <div className="p-2 bg-purple-500 rounded-lg mr-3">
            <Brain className="h-6 w-6 text-white" />
          </div>
          <h3 className="text-xl font-bold text-gray-900">Predição para o Próximo Mês</h3>
        </div>
        <div className="text-center py-8 text-gray-500">
          Dados insuficientes para gerar predição. Importe dados de consumo para visualizar predições.
        </div>
      </div>
    )
  }
  
  const energyPred = prediction.energy_kwh_pred.toFixed(0)
  const costPred = prediction.cost_brl_pred?.toFixed(2) || '0.00'
  
  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg border border-gray-100">
      <div className="flex items-center mb-6">
        <div className="p-2 bg-purple-500 rounded-lg mr-3">
          <Brain className="h-6 w-6 text-white" />
        </div>
        <h3 className="text-xl font-bold text-gray-900">Predição para o Próximo Mês</h3>
      </div>

      <div className="space-y-4">
        {/* Consumo Previsto */}
        <div className="bg-gradient-to-r from-blue-50 to-blue-100 p-5 rounded-xl border-l-4 border-blue-500">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm font-medium text-blue-700">Consumo Previsto ({prediction.target_month})</div>
              <div className="text-3xl font-bold text-blue-900">~{energyPred} <span className="text-lg">kWh</span></div>
            </div>
            <Brain className="h-8 w-8 text-blue-500" />
          </div>
        </div>

        {/* Custo Previsto */}
        <div className="bg-gradient-to-r from-green-50 to-green-100 p-5 rounded-xl border-l-4 border-green-500">
          <div className="text-sm font-medium text-green-700">Custo Previsto</div>
          <div className="text-3xl font-bold text-green-900">~R$ {costPred}</div>
          <div className="text-sm text-green-600 font-medium">Estimativa baseada em consumo histórico</div>
        </div>

        {/* Insight */}
        <div className="bg-gradient-to-r from-yellow-50 to-orange-100 p-5 rounded-xl border-l-4 border-orange-500">
          <div className="flex items-start">
            <Lightbulb className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
            <div>
              <div className="text-sm font-bold text-orange-800 mb-1">Insight</div>
              <div className="text-sm text-orange-700">
                As predições são baseadas nos seus padrões de consumo dos últimos 90 dias. Mantenha bons hábitos de consumo!
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PredictionCard