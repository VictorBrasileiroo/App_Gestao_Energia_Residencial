import React from 'react'

const MonthlySaving = ({ data }) => {
    const reportData = data || {}
    
    // Calculate savings based on real data
    const cost7Days = reportData.cost_last_7_days || 0
    const cost30Days = reportData.cost_last_30_days || 0
    const costCurrentMonth = reportData.cost_current_month || 0
    
    const savings = [
        { 
            month: 'Últimos 7 Dias', 
            percentage: '', 
            values: `R$ ${cost7Days.toFixed(2)}`
        },
        { 
            month: 'Últimos 30 Dias', 
            percentage: '', 
            values: `R$ ${cost30Days.toFixed(2)}`
        },
        { 
            month: 'Mês Atual', 
            percentage: '', 
            values: `R$ ${costCurrentMonth.toFixed(2)}`
        },
        { 
            month: 'Predição Próximo Mês', 
            percentage: '', 
            values: reportData.prediction?.cost_pred ? `R$ ${reportData.prediction.cost_pred.toFixed(2)}` : 'N/A'
        },
    ]

    return (
        <div className='bg-white p-6 rounded-xl shadow-sm border border-gray-100'>
            <h3 className='text-lg font-semibold text-gray-900 mb-4'>Economia Mensal</h3>

            <div className='space-y-3'>
                {savings.map((item, index) => (
                    <div key={index} className='flex justify-between items-center p-3 bg-gray-50 rounded-lg'>
                        <div>
                            <div className='font-medium text-gray-900'>{item.month}</div>
                            <div className='text-sm text-green-500'>{item.percentage}</div>
                        </div>
                        <div className='text-lg font-bold text-gray-900'>{item.values}</div>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default MonthlySaving