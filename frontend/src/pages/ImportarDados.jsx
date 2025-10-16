import React, { useState, useRef } from 'react'
import DashboardLayout from '../components/DashboardLayout'

const ImportarDados = () => {
  const [arquivo, setArquivo] = useState(null)
  const [estaArrastando, setEstaArrastando] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [estaEnviando, setEstaEnviando] = useState(false)
  const fileInputRef = useRef(null)

  //f. pra lidar com arrastare soltar
  const handleDragOver = (e) => {
    e.preventDefault()
    setEstaArrastando(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setEstaArrastando(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setEstaArrastando(false)
    
    const files = e.dataTransfer.files
    if (files.length > 0) {
      processarArquivo(files[0])
    }
  }

  //f. pra lidae com a seleção de arq
  const handleFileSelect = (e) => {
    const files = e.target.files
    if (files.length > 0) {
      processarArquivo(files[0])
    }
  }

  //processa o arq 
  const processarArquivo = (file) => {
    // Validar tipo de arquivo
    if (!file.name.toLowerCase().endsWith('.csv')) {
      alert('Por favor, selecione um arquivo CSV.')
      return
    }

    //tamanho max: 10MB validação
    if (file.size > 10 * 1024 * 1024) {
      alert('O arquivo é muito grande. Tamanho máximo: 10MB.')
      return
    }

    setArquivo(file)
  }

  //simula upload (backend)
  const handleUpload = async () => {
    if (!arquivo) return

    setEstaEnviando(true)
    setUploadProgress(0)

    //simulaçao de progresso de upload
    const interval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval)
          setTimeout(() => {
            setEstaEnviando(false)
            alert('Arquivo importado com sucesso!')
            setArquivo(null)
          }, 500)
          return 100
        }
        return prev + 10
      })
    }, 200)
  }

  //abrir seletor de arq
  const abrirSeletorArquivos = () => {
    fileInputRef.current?.click()
  }

  return (
    <DashboardLayout>
      <div className="p-6 max-w-4xl mx-auto bg-green-00">
        {/*header*/}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Importe seu Histórico de Consumo
          </h1>
          <p className="text-gray-600 text-lg">
            Envie seu arquivo CSV com os dados de consumo por hora (datetime, energy_kwh).
          </p>
        </div>

        {/*area de upload*/}
        <div className="bg-white rounded-2xl shadow-sm border-2 border-dashed border-gray-300 p-8 mb-6">
          <div
            className={`text-center p-12 rounded-xl transition-all cursor-pointer ${
              estaArrastando 
                ? 'bg-green-50 border-2 border-green-400 border-dashed' 
                : 'bg-gray-50 hover:bg-gray-100'
            }`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={abrirSeletorArquivos}
          >
            {estaEnviando ? (
              <div className="space-y-4">
                <div className="w-16 h-16 mx-auto border-4 border-green-200 border-t-green-500 rounded-full animate-spin"></div>
                <div>
                  <p className="text-lg font-medium text-gray-900">Enviando arquivo...</p>
                  <div className="w-48 mx-auto mt-2 bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-green-500 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${uploadProgress}%` }}
                    ></div>
                  </div>
                  <p className="text-sm text-gray-500 mt-1">{uploadProgress}%</p>
                </div>
              </div>
            ) : arquivo ? (
              <div className="space-y-4">
                <div className="w-16 h-16 mx-auto bg-green-100 rounded-full flex items-center justify-center">
                  <img 
                    src="/images/envio.png" 
                    alt="Arquivo selecionado" 
                    className="w-8 h-8"
                  />
                </div>
                <div>
                  <p className="text-lg font-medium text-gray-900">{arquivo.name}</p>
                  <p className="text-sm text-gray-500">
                    {(arquivo.size / (1024 * 1024)).toFixed(2)} MB
                  </p>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    handleUpload()
                  }}
                  className="bg-green-500 text-white px-6 py-2 rounded-lg hover:bg-green-600 transition-colors"
                >
                  Importar Dados
                </button>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="w-16 h-16 mx-auto bg-gray-200 rounded-full flex items-center justify-center">
                  <img 
                    src="/images/envio.png" 
                    alt="Enviar arquivo" 
                    className="w-8 h-8 opacity-60"
                  />
                </div>
                <div>
                  <p className="text-lg font-medium text-gray-900">
                    Arraste e solte seu arquivo aqui
                  </p>
                  <p className="text-gray-500">ou</p>
                </div>
                <button
                  onClick={(e) => e.stopPropagation()}
                  className="bg-green-500 text-white px-6 py-2 rounded-lg hover:bg-green-600 transition-colors"
                >
                  Selecionar Arquivo
                </button>
              </div>
            )}
          </div>

          {/*input do arq hidden*/}
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileSelect}
            accept=".csv"
            className="hidden"
          />
        </div>

        {/*infos do arquivo*/}
        <div className="text-center text-sm text-gray-500 mb-8">
          <p>Formatos aceitos: CSV • Tamanho máximo: 10MB</p>
          <p className="mt-1">
            Estrutura esperada: datetime (YYYY-MM-DD HH:MM:SS), energy_kwh (número)
          </p>
        </div>

        {/*botao pra pular etapa*/}
        <div className="text-center">
          <button className="text-green-600 hover:text-green-700 font-medium transition-colors">
            Pular esta etapa →
          </button>
        </div>

        {/*exemplo da estrutura csv*/}
        <div className="mt-12 bg-gray-50 rounded-xl p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Exemplo de estrutura do CSV:</h3>
          <div className="bg-white rounded-lg p-4 border border-gray-200 overflow-x-auto">
            <pre className="text-sm text-gray-700">
{`datetime,energy_kwh
2024-01-01 00:00:00,0.85
2024-01-01 01:00:00,0.92
2024-01-01 02:00:00,0.78
2024-01-01 03:00:00,0.65
2024-01-01 04:00:00,0.71
...`}
            </pre>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}

export default ImportarDados