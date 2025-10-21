import React, { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

const DashboardLayout = ({ children }) => {
  const location = useLocation()
  const navigate = useNavigate()
  const { logout, user } = useAuth()
  const [showUserMenu, setShowUserMenu] = useState(false)
  const [sidebarVisible, setSidebarVisible] = useState(true)

  const menuItems = [
    { name: 'Dashboard', path: '/dashboard', icon: '/images/dashboard.png' },
    { name: 'Relatórios', path: '/relatorios', icon: '/images/relatorio.png' },
    { name: 'Alertas', path: '/alertas', badge: 3, icon: '/images/alerta.png' },
    { name: 'Importar Dados', path: '/importar', icon: '/images/importar.png' },
    { name: 'Configurações', path: '/configuracoes', icon: '/images/config.png' },
  ]

  return (
    <div className="flex h-screen bg-gray-50">
      {/*sidebar*/}
      <div className={`${sidebarVisible ? 'w-64' : 'w-16'} bg-gradient-to-b from-slate-600 to-slate-700 shadow-xl transition-all duration-300 relative`}>
        <div className="p-4">
          {/*Header com logo e toggle*/}
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center">
              <img
                src="/images/logo_3.png"
                alt="Voltix"
                className="h-10 w-10"
              />
              {sidebarVisible && (
                <h1 className="ml-3 text-xl font-bold text-white">Voltix</h1>
              )}
            </div>
            <button 
              onClick={() => setSidebarVisible(!sidebarVisible)}
              className="p-2 rounded-lg hover:bg-slate-700 transition-colors duration-200"
            >
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={sidebarVisible ? "M11 19l-7-7 7-7M18 19l-7-7 7-7" : "M4 6h16M4 12h16M4 18h16"} />
              </svg>
            </button>
          </div>
        </div>

        <nav className="px-2 space-y-2">
          {menuItems.map((item) => {
            const isActive = location.pathname === item.path
            
            return (
              <Link 
                key={item.name}
                to={item.path}
                className={`flex items-center p-3 rounded-xl transition-all duration-200 group relative ${
                  isActive 
                    ? 'bg-gradient-to-r from-green-500 to-emerald-500 text-white shadow-lg' 
                    : 'text-gray-300 hover:bg-slate-700 hover:text-white'
                }`}
                title={!sidebarVisible ? item.name : ''}
              >
                <img 
                  src={item.icon} 
                  alt={item.name} 
                  className="h-5 w-5 flex-shrink-0"
                />
                
                {sidebarVisible && (
                  <>
                    <span className="ml-3 font-medium flex-1">{item.name}</span>
                    {item.badge && (
                      <span className="bg-red-500 text-white text-xs px-2 py-1 rounded-full font-bold">
                        {item.badge}
                      </span>
                    )}
                  </>
                )}
                
                {/*Tooltip para sidebar colapsada*/}
                {!sidebarVisible && (
                  <div className="absolute left-full ml-2 px-3 py-2 bg-slate-800 text-white text-sm rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 whitespace-nowrap z-50">
                    {item.name}
                    {item.badge && (
                      <span className="ml-2 bg-red-500 text-white text-xs px-2 py-1 rounded-full">
                        {item.badge}
                      </span>
                    )}
                  </div>
                )}
              </Link>
            )
          })}
        </nav>
      </div>

      {/* main content */}
      <div className="flex-1 overflow-auto">
        {/* header global com perfil - sua versão */}
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

          {/* menu dropdown para usuário - sua versão */}
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
                  logout()
                  navigate('/login')
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