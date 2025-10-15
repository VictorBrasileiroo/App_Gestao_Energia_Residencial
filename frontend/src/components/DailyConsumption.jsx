import React from 'react'

const DailyConsumption = () => {
    return (
        <div className='bg-white p-6 rounded-xl shadow-sm border border-gray-100'>
            <div className='flex justify-between items-center mb-4'>
                <h3 className='text-lg font-semibold text-gray-900'>Consumo Diário (Última Semana)</h3>
                <button className='text-green-600 hover:text-green-700 text-sm font-medium'>
                    Exportar
                </button>
            </div>

            {/* grafico placeholde */}
            <div className='bg-gray-100 h-48 rounded-lg flex items-center justify-center'>
                <p className='text-gray-500'>Gráfico: Consumo Diário</p>
            </div>
        </div>
    )
}

export default DailyConsumption