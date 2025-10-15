import React from 'react'

const ConsumptionChart = () => {
  const months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul']
  const values = [180, 220, 190, 240, 280, 260, 285] //valore do design

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Consumo Mensal vs Meta</h3>
      
      {/*o grafico */}
      <div className="h-64 relative">

        {/*linhas de grade */}
        <div className="absolute inset-0 flex flex-col justify-between">
          {[0, 1, 2, 3].map((i) => (
            <div key={i} className="border-t border-gray-200"></div>
          ))}
        </div>

        {/*barras*/}
        <div className="absolute inset-0 flex items-end justify-between px-4 pb-8">
          {values.map((value, index) => (
            <div key={index} className="flex flex-col items-center">
              {/*baara*/}
              <div 
                className="w-8 bg-gradient-to-t from-primary-500 to-green-600 rounded-t-lg relative"
                style={{ height: `${(value / 360) * 100}%` }}
              >
                {/*valor no topo da barra*/}
                <div className="absolute -top-6 left-1/2 transform -translate-x-1/2 text-xs font-medium text-gray-700">
                  {value}
                </div>
              </div>
              
              {/*Mes*/}
              <div className="text-xs text-gray-500 mt-2">{months[index]}</div>
            </div>
          ))}
        </div>

        {/*Y*/}
        <div className="absolute left-0 top-0 bottom-0 flex flex-col justify-between text-xs text-gray-500 py-8">
          <span>360</span>
          <span>270</span>
          <span>180</span>
          <span>90</span>
          <span>0</span>
        </div>
      </div>
    </div>
  )
}

export default ConsumptionChart