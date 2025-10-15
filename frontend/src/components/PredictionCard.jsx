import React from 'react'

const PredictionCard = () => {
  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
      <div className="flex items-center mb-4">
        <span className="text-2xl mr-2">🤖</span>
        <h3 className="text-lg font-semibold text-gray-900">Predição para o Próximo Mês</h3>
      </div>

      <div className="space-y-4">
        <div className="bg-blue-50 p-4 rounded-lg">
          <div className="text-sm text-gray-600">Consumo Previsto</div>
          <div className="text-xl font-bold text-gray-900">~287 kWh</div>
          <div className="text-sm text-green-500">8% abaixo da média</div>
        </div>

        <div className="bg-green-50 p-4 rounded-lg">
          <div className="text-sm text-gray-600">Custo Previsto</div>
          <div className="text-xl font-bold text-gray-900">~R$ 210</div>
          <div className="text-sm text-green-500">Economia estimada de R$ 23,50 vs mês anterior</div>
        </div>

        <div className="bg-purple-50 p-4 rounded-lg">
          <div className="text-sm text-gray-600">Intervalo de Confiança 95%</div>
          <div className="flex justify-between text-sm">
            <span>Mínimo: 190 kWh</span>
            <span>Máximo: 330 kWh</span>
          </div>
        </div>

        <div className="bg-yellow-50 p-4 rounded-lg">
          <div className="text-sm font-medium text-gray-900">💡 Insight</div>
          <div className="text-sm text-gray-600 mt-1">
            Baseado nos seus padrões, você está no caminho certo para atingir sua meta de economia de 15%. Continue mantendo os bons hábitos!
          </div>
        </div>
      </div>
    </div>
  )
}

export default PredictionCard