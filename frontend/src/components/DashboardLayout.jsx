import React from 'react'
import { Link, useLocation } from 'react-router-dom'

const DashboardLayout = ({ children }) => {
  const location = useLocation()

  const menuItems = [
    { name: 'Dashboard', path: '/dashboard' },
    { name: 'Relatórios', path: '/relatorios' },
    { name: 'Alertas', path: '/alertas', badge: 3 },
    { name: 'Importar Dados', path: '/importar' },
    { name: 'Configurações', path: '/configuracoes' },
    { name: 'Sair', path: '/login' }
  ]

  return (
    <div className="flex h-screen bg-gray-50">
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
          {menuItems.map((item) => {
            const isActive = location.pathname === item.path
            
            return (
              <Link 
                key={item.name}
                to={item.path}
                className={`flex items-center px-6 py-3 text-gray-700 hover:bg-green-50 hover:text-green-600 cursor-pointer ${
                  isActive ? 'bg-green-50 text-green-600 border-r-2 border-green-600' : ''
                }`}
              >
                {/*Adiciona ícone*/}
                <span className="mr-3 text-lg">{item.icon}</span>
                <span className="flex-1">{item.name}</span>
                {item.badge && (
                  <span className="bg-red-500 text-white text-xs px-2 py-1 rounded-full">
                    {item.badge}
                  </span>
                )}
              </Link>
            )
          })}
        </nav>
      </div>

      {/*main*/}
      <div className="flex-1 overflow-auto">
        {/*cabeca global com perfil*/}
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