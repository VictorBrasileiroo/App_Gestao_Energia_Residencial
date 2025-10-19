import React, { useState } from 'react'
import DashboardLayout from '../components/DashboardLayout'
import { useNavigate } from 'react-router-dom'
import { User, Download } from 'lucide-react'

const Perfil = () => {
  const navigate = useNavigate()
  const [usuario, setUsuario] = useState({
    nome: 'João Silva',
    email: 'joao.silva@email.com',
    telefone: '(11) 99999-9999',
    empresa: 'Tech Solutions Ltda',
    cargo: 'Gerente de Operações'
  })

  const [editando, setEditando] = useState(false)

  const handleInputChange = (field, value) => {
    setUsuario(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const salvarPerfil = () => {
    //integra com back
    setEditando(false)
    alert('Perfil atualizado com sucesso!')
  }

  const handleLogout = () => {
    if (window.confirm('Tem certeza que deseja sair?')) {
      //logout
      navigate('/login')
    }
  }

  return (
    <DashboardLayout>
      <div className="p-6 max-w-4xl mx-auto bg-green-00">
        {/* Header */}
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-sm border border-gray-100 p-6 mb-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="bg-gradient-to-r from-purple-500 to-purple-600 p-3 rounded-xl shadow-lg">
                <User className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  Meu Perfil
                </h1>
                <p className="text-gray-600 mt-1">
                  Gerencie suas informações pessoais e preferências
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <span className="bg-purple-100 text-purple-800 text-sm font-medium px-3 py-1 rounded-full">
                Perfil Ativo
              </span>
              <button className="bg-gradient-to-r from-purple-500 to-purple-600 text-white px-4 py-2 rounded-lg hover:from-purple-600 hover:to-purple-700 transition-all duration-200 flex items-center space-x-2 shadow-md">
                <Download className="w-4 h-4" />
                <span>Exportar Dados</span>
              </button>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-sm p-8 mb-6">
          {/*avatar e infos*/}
          <div className="flex items-center space-x-6 mb-8">
            <div className="relative">
              <img
                src="/images/user.png"
                alt="Usuário"
                className="h-24 w-24 rounded-full object-cover border-4 border-green-100"
              />
              <button className="absolute bottom-0 right-0 bg-green-500 text-white p-2 rounded-full hover:bg-green-600 transition-colors">
                <img src="/images/edit.png" alt="Editar" className="h-4 w-4" />
              </button>
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-900">{usuario.nome}</h2>
              <p className="text-gray-600">{usuario.cargo}</p>
              <p className="text-gray-500 text-sm">{usuario.empresa}</p>
            </div>
          </div>

          {/*form de adição*/}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Nome Completo
              </label>
              <input
                type="text"
                value={usuario.nome}
                onChange={(e) => handleInputChange('nome', e.target.value)}
                disabled={!editando}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:bg-gray-100"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email
              </label>
              <input
                type="email"
                value={usuario.email}
                onChange={(e) => handleInputChange('email', e.target.value)}
                disabled={!editando}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:bg-gray-100"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Telefone
              </label>
              <input
                type="tel"
                value={usuario.telefone}
                onChange={(e) => handleInputChange('telefone', e.target.value)}
                disabled={!editando}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:bg-gray-100"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Empresa
              </label>
              <input
                type="text"
                value={usuario.empresa}
                onChange={(e) => handleInputChange('empresa', e.target.value)}
                disabled={!editando}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:bg-gray-100"
              />
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Cargo
              </label>
              <input
                type="text"
                value={usuario.cargo}
                onChange={(e) => handleInputChange('cargo', e.target.value)}
                disabled={!editando}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:bg-gray-100"
              />
            </div>
          </div>

          {/*bnt de ação*/}
          <div className="flex justify-end space-x-4 mt-8 pt-6 border-t border-gray-200">
            {editando ? (
              <>
                <button
                  onClick={() => setEditando(false)}
                  className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancelar
                </button>
                <button
                  onClick={salvarPerfil}
                  className="bg-green-500 text-white px-6 py-2 rounded-lg hover:bg-green-600 transition-colors"
                >
                  Salvar Alterações
                </button>
              </>
            ) : (
              <button
                onClick={() => setEditando(true)}
                className="bg-green-500 text-white px-6 py-2 rounded-lg hover:bg-green-600 transition-colors"
              >
                Editar Perfil
              </button>
            )}
          </div>
        </div>

        {/*ações imortantes*/}
        <div className="bg-white rounded-2xl shadow-sm p-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Ações da Conta</h2>
          
          <div className="space-y-4">
            <button 
              onClick={() => navigate('/configuracoes')}
              className="w-full flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-green-50 transition-colors text-left"
            >
              <div>
                <h3 className="font-medium text-gray-900">Configurações</h3>
                <p className="text-sm text-gray-500">Gerencie preferências e notificações</p>
              </div>
              <img src="/images/config.png" alt=">" className="h-4 w-4" />
            </button>

            <button 
              onClick={handleLogout}
              className="w-full flex items-center justify-between p-4 border border-red-200 rounded-lg hover:bg-red-50 transition-colors text-left"
            >
              <div>
                <h3 className="font-medium text-red-700">Sair da Conta</h3>
                <p className="text-sm text-red-500">Encerrar sessão atual</p>
              </div>
              <img src="/images/arrow-right.png" alt="Sair" className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}

export default Perfil