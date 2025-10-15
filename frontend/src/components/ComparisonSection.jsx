import React from 'react'

const ComparisonSection = () => {
  const comparisons = [
    {
      title: 'Mês Anterior',
      value: '163kWh',
      change: '+9.2%'
    },

    {
      title: 'Média Trimestral',
      value: '155 kWh',
      change: '+14.8%'
    },

    {
      title: 'Previsão para o Próximo Mês',
      value: '287kWh',
      change: '+25.4%'
    },

    {
      title: 'Média Anual',
      value: '168kWh',
      change: '+6%'
    }
  ]

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Comparação Histórica</h3>
      
      <div className="grid grid-cols-2 gap-4 mb-6">
        {comparisons.map((item, index) => (
          <div key={index} className="text-center p-4 bg-gray-50 rounded-lg">
            <div className="text-2xl font-bold text-gray-900">{item.value}</div>
            <div className="text-sm text-gray-600 mt-1">{item.title}</div>
            <div className="text-xs text-green-500 mt-1">{item.change}</div>
          </div>
        ))}
      </div>

      {/* placeholdergrafico */}
      <div className="bg-gray-100 h-48 rounded-lg flex items-center justify-center">
        <p className="text-gray-500">Gráfico: Consumo Real vs Predição</p>
      </div>
    </div>
  )
}

export default ComparisonSection