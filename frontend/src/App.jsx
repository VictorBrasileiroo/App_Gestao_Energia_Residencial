import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Relatorios from './pages/Relatorios'
import Alertas from './pages/Alertas'
import ImportarDados from './pages/ImportarDados'
import Configuracoes from './pages/Configuracoes'
import Perfil from './pages/Perfil'

function App() {
// return o que será renderizado na tela
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/relatorios" element={<Relatorios />} />
        <Route path="/alertas" element={<Alertas />} />
        <Route path="/importar" element={<ImportarDados />} />
        <Route path="/configuracoes" element={<Configuracoes />} />
        <Route path="/perfil" element={<Perfil />} />
      </Routes>
    </Router>
  )
}

//exporta componente App para que ele possa ser usado noutros arq
export default App