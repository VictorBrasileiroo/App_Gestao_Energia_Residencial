import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'

const DashboardLayout = ({ children }) => {
  const location = useLocation()
  const [showUserMenu, setShowUserMenu] = useState(false)

  const menuItems = [
    { name: 'Dashboard', path: '/dashboard', icon: '/images/dashboard.png' },
    { name: 'Relatórios', path: '/relatorios', icon: '/images/relatorio.png' },
    { name: 'Alertas', path: '/alertas', badge: 3, icon: '/images/alerta.png' },
    { name: 'Importar Dados', path: '/importar', icon: '/images/importar.png' },
    { name: 'Configurações', path: '/configuracoes', icon: '/images/config.png' },
  ]

  return (
    <div className="flex h-screen bg-green-00">
      {/*sidebar*/}
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
                <img src={item.icon} alt={item.name} className="h-5 w-5 mr-3"></img>
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
        <div className="flex justify-end items-center p-4 bg-transparent relative">
          <div 
            className="h-10 w-10 bg-gray-300 rounded-full flex items-center justify-center cursor-pointer hover:ring-2 hover:ring-green-500 transition"
            onClick={() => setShowUserMenu(!showUserMenu)}
          >
            <img
              src="/images/user.png"
              alt="Usuário"
              className="h-10 w-10 rounded-full object-cover"
            />
          </div>

          {/*menu dropdown para usuário*/}
          {showUserMenu && (
            <div className="absolute top-16 right-4 bg-white rounded-lg shadow-lg border border-gray-200 py-2 w-48 z-50">
              <Link 
                to="/perfil" 
                className="flex items-center px-4 py-2 text-gray-700 hover:bg-green-50 cursor-pointer"
                onClick={() => setShowUserMenu(false)}
              >
                <img src="/images/conta.png" alt="Perfil" className="h-4 w-4 mr-3" />
                Meu Perfil
              </Link>
              <Link 
                to="/configuracoes" 
                className="flex items-center px-4 py-2 text-gray-700 hover:bg-green-50 cursor-pointer"
                onClick={() => setShowUserMenu(false)}
              >
                <img src="/images/config.png" alt="Configurações" className="h-4 w-4 mr-3" />
                Configurações
              </Link>
              <div className="border-t border-gray-200 my-1"></div>
              <button 
                className="flex items-center px-4 py-2 text-red-600 hover:bg-red-50 cursor-pointer w-full text-left"
                onClick={() => {
                  setShowUserMenu(false)
                  //logout
                  alert('Saindo do sistema...')
                }}
              >
                <img src="/images/arrow-right.png" alt="Sair" className="h-4 w-4 mr-3" />
                Sair
              </button>
            </div>
          )}
        </div>

        {children}
      </div>
    </div>
  )
}

export default DashboardLayout