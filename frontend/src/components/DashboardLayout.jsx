import React from 'react'
import { Link } from 'react-router-dom'

const DashboardLayout = ({ children }) => {
  return (
    <div className="flex h-screen bg-gray-50">
      {/* sidabr */}
      <div className="w-64 bg-white shadow-lg">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-green-600">VOLTIX</h1>
          <p className="text-sm text-gray-600">Gestão Inteligente de Energia</p>
        </div>
        
        <nav className="mt-6">
          {[
            { name: 'Dashboard', active: true },
            { name: 'Relatórios' },
            { name: 'Alertas', badge: 3 },
            { name: 'Importar Dados' },
          ].map((item) => (
            <div
              key={item.name}
              className={`flex items-center px-6 py-3 text-gray-700 hover:bg-primary-50 hover:text-green-600 cursor-pointer ${
                item.active ? 'bg-primary-50 text-green-600 border-r-2 border-gren-600' : ''
              }`}
            >
              <span className="mr-3">{item.icon}</span>
              <span className="flex-1">{item.name}</span>
              {item.badge && (
                <span className="bg-red-500 text-white text-xs px-2 py-1 rounded-full">
                  {item.badge}
                </span>
              )}
            
            </div>
          
          ))}
        
        </nav>
      
      </div>

      {/* main */}
      <div className="flex-1 overflow-auto">
        {children}
      </div>
    </div>
  )
}

export default DashboardLayout