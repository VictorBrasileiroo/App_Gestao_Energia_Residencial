import React from 'react'

const WeeklyAnalysis = () => {
  const days = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
  const values = [8, 12, 10, 14, 16, 18, 12] // Valores aproximados do design

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Análise Semanal</h3>
      
      {/*grfico*/}
      <div className="h-48 relative">
        {/*linhas de grade*/}
        <div className="absolute inset-0 flex flex-col justify-between">
          {[0, 1, 2, 3].map((i) => (
            <div key={i} className="border-t border-gray-200"></div>
          ))}
        </div>

        {/*barras*/}
        <div className="absolute inset-0 flex items-end justify-between px-4 pb-6">
          {values.map((value, index) => (
            <div key={index} className="flex flex-col items-center">
              {/*barra*/}
              <div 
                className="w-6 bg-gradient-to-t from-green-500 to-green-600 rounded-t-lg"
                style={{ height: `${(value / 16) * 100}%` }}
              ></div>
              
              {/*dia*/}
              <div className="text-xs text-gray-500 mt-2">{days[index]}</div>
            </div>
          ))}
        </div>

        {/*Y*/}
        <div className="absolute left-0 top-0 bottom-0 flex flex-col justify-between text-xs text-gray-500 py-6">
          <span>16</span>
          <span>12</span>
          <span>8</span>
          <span>4</span>
          <span>0</span>
        </div>
      </div>
    </div>
  )
}

export default WeeklyAnalysis