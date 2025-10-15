import React from 'react'

const MonthlySaving = () => {
    const savings = [
        { month: 'Julho', percentage: '-12%', values: 'R$ 45,20'},
        { month: 'Agosto', percentage: '-8%', values: 'R$ 30,50'},
        { month: 'Setembro', percentage: '-15%', values: 'R$ 60,00'},
        { month: 'Outubro', percentage: '-10%', values: 'R$ 40,75'},
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