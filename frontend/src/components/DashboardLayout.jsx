import React from 'react'
import { Link } from 'react-router-dom'

const DashboardLayout = ({ children }) => {
  return (
    <div className="flex h-screen bg-green-00">
      {/* sidebar */}
      <div className="w-64 bg-white shadow-lg">
        <div className="p-6">
          <div className='flex items-center space-x-3'>
            <img
              src="/images/logo_3.png"
              alt="Voltix"
              className="h-14 w-14"
            />
            <h1 className="text-2xl font-extrabold text-green-600">Voltix</h1>
          </div>

          <p className="text-sm text-gray-600 mt-2">Gestão Inteligente de Energia</p>
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
              className={`flex items-center px-6 py-3 text-gray-700 hover:bg-green-50 hover:text-green-600 cursor-pointer ${
                item.active ? 'bg-green-50 text-green-600 border-r-2 border-green-600' : ''
              }`}
            >
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
        {/* header global com perfil */}
        <div className="flex justify-end items-center p-4 border-b bg-white">
          <div className="h-10 w-10 bg-gray-300 rounded-full flex items-center justify-center cursor-pointer hover:ring-2 hover:ring-green-500 transition">
            <img
              src="/images/user.png"
              alt="Usuário"
              className="h-10 w-10 rounded-full object-cover"
            />
          </div>
        </div>

        {children}
      </div>
    </div>
  )
}

export default DashboardLayout
