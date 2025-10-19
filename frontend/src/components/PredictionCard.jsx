import React from 'react'
import { Brain, TrendingDown, Lightbulb, AlertTriangle } from 'lucide-react'

const PredictionCard = () => {
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
              <div className="text-sm font-medium text-blue-700">Consumo Previsto</div>
              <div className="text-3xl font-bold text-blue-900">~287 <span className="text-lg">kWh</span></div>
              <div className="text-sm text-green-600 font-medium">8% abaixo da média</div>
            </div>
            <TrendingDown className="h-8 w-8 text-green-500" />
          </div>
        </div>

        {/* Custo Previsto */}
        <div className="bg-gradient-to-r from-green-50 to-green-100 p-5 rounded-xl border-l-4 border-green-500">
          <div className="text-sm font-medium text-green-700">Custo Previsto</div>
          <div className="text-3xl font-bold text-green-900">~R$ 210</div>
          <div className="text-sm text-green-600 font-medium">Economia estimada de R$ 23,50 vs mês anterior</div>
        </div>

        {/* Intervalo de Confiança */}
        <div className="bg-gradient-to-r from-purple-50 to-purple-100 p-5 rounded-xl border-l-4 border-purple-500">
          <div className="text-sm font-medium text-purple-700 mb-3">Intervalo de Confiança</div>
          <div className="flex justify-between text-sm">
            <div className="text-purple-800">
              <div className="font-medium">Mínimo</div>
              <div className="text-lg font-bold">190 kWh</div>
            </div>
            <div className="w-px bg-purple-300"></div>
            <div className="text-purple-800 text-right">
              <div className="font-medium">Máximo</div>
              <div className="text-lg font-bold">330 kWh</div>
            </div>
          </div>
        </div>

        {/* Insight */}
        <div className="bg-gradient-to-r from-yellow-50 to-orange-100 p-5 rounded-xl border-l-4 border-orange-500">
          <div className="flex items-start">
            <Lightbulb className="h-5 w-5 text-orange-500 mr-2 mt-0.5 flex-shrink-0" />
            <div>
              <div className="text-sm font-bold text-orange-800 mb-1">Insight</div>
              <div className="text-sm text-orange-700">
                Baseado nos seus padrões, você está no caminho certo para atingir sua meta de economia de 15%. Continue mantendo os bons hábitos!
              </div>
            </div>
          </div>
        </div>

        {/* Notificações */}
        <div className="bg-gradient-to-r from-red-50 to-red-100 p-4 rounded-xl border-l-4 border-red-500">
          <div className="flex items-center">
            <AlertTriangle className="h-5 w-5 text-red-500 mr-2" />
            <div>
              <div className="text-sm font-bold text-red-800">Crítico</div>
              <div className="text-xs text-red-700">Consumo 15% acima da média para este horário</div>
            </div>
            <div className="ml-auto bg-red-500 text-white text-xs px-2 py-1 rounded-full">1</div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PredictionCard