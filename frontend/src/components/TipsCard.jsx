import React from 'react'

const TipsCard = () => {
  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Dica de Economia</h3>
        <span className="text-sm text-gray-500">2 de 8</span>
      </div>
      
      <div className="bg-yellow-50 p-4 rounded-lg">
        <p className="text-sm text-gray-700">
          Tire os aparelhos da tomada quando não estiverem em uso. O modo 'stand-by' também consome energia!
        </p>
      </div>
      
      <button className="w-full mt-4 text-green-600 hover:text-green-700 text-sm font-medium">
        Ver mais dicas
      </button>
    </div>
  )
}

export default TipsCard