# 🏠⚡ Sistema de Gestão de Energia Residencial

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)
![License](https://img.shields.io/badge/License-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![React](https://img.shields.io/badge/React-19.2.0-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-teal)

Sistema completo de monitoramento, análise e previsão de consumo de energia elétrica residencial com interface web moderna, algoritmos de Machine Learning e arquitetura distribuída.

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura](#-arquitetura)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Uso](#-uso)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [API Endpoints](#-api-endpoints)
- [Machine Learning](#-machine-learning)
- [Screenshots](#-screenshots)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)
- [Autores](#-autores)

---

## 🎯 Sobre o Projeto

O **Sistema de Gestão de Energia Residencial** é uma aplicação web completa desenvolvida para ajudar famílias e residências a monitorar, analisar e otimizar seu consumo de energia elétrica. 

### Objetivos

- 📊 **Monitoramento em Tempo Real**: Acompanhe seu consumo de energia hora a hora
- 📈 **Análises Detalhadas**: Gráficos e estatísticas sobre padrões de consumo
- 🔮 **Previsões Inteligentes**: Machine Learning para prever consumo futuro
- 💡 **Dicas Personalizadas**: Recomendações para economia de energia
- 🚨 **Alertas Inteligentes**: Notificações de consumo anormal
- 📑 **Relatórios Completos**: Exportação de dados e análises

---

## ✨ Funcionalidades

### Dashboard Principal
- Visualização de consumo diário, semanal e mensal
- Comparação com períodos anteriores
- Indicadores de tendência e economia
- Gráficos interativos com Chart.js

### Análise de Consumo
- Consumo por hora do dia
- Análise de padrões semanais
- Identificação de picos de consumo
- Comparação mês a mês

### Previsões com ML
- Predição de consumo para próximo mês
- Algoritmos de Random Forest
- Análise de sazonalidade
- Estimativas de custos futuros

### Alertas Automáticos
- Detecção de consumo anormal
- Notificações personalizáveis
- Histórico de alertas
- Sugestões de ações corretivas

### Relatórios
- Relatórios mensais e anuais
- Exportação em PDF/CSV
- Análises comparativas
- Estatísticas detalhadas

### Importação de Dados
- Upload de arquivos CSV
- Validação automática de dados
- Processamento em lote
- Histórico de importações

---

## 🏗️ Arquitetura

O projeto utiliza uma arquitetura de três camadas:

```
┌─────────────────┐
│    Frontend     │  React + Vite + TailwindCSS
│  (Port 5173)    │  Interface do Usuário
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Middle Layer   │  FastAPI Middleware
│  (Port 8001)    │  Autenticação + Roteamento
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Backend      │  FastAPI + SQLAlchemy
│  (Port 8000)    │  Lógica de Negócio + ML
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Database     │  SQLite
│                 │  Armazenamento de Dados
└─────────────────┘
```

### Camadas

1. **Frontend**: Interface do usuário construída com React, oferecendo uma experiência moderna e responsiva
2. **Middle Layer**: Camada intermediária de segurança e roteamento, gerenciando autenticação e requisições
3. **Backend**: API principal com lógica de negócio, processamento de dados e modelos de ML
4. **Database**: Banco de dados SQLite para armazenamento persistente

---

## 🛠️ Tecnologias Utilizadas

### Frontend
- **React 19.2.0** - Biblioteca UI
- **Vite** - Build tool e dev server
- **TailwindCSS** - Framework CSS utility-first
- **Chart.js** - Biblioteca de gráficos
- **React Router** - Navegação SPA
- **Axios** - Cliente HTTP
- **Lucide React** - Ícones modernos

### Backend
- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para Python
- **Pydantic** - Validação de dados
- **Pandas** - Análise e manipulação de dados
- **NumPy** - Computação numérica
- **Scikit-learn** - Machine Learning
- **Passlib** - Hashing de senhas
- **Python-JOSE** - JWT tokens

### Middle Layer
- **FastAPI** - Framework middleware
- **HTTPX** - Cliente HTTP assíncrono
- **Python-dotenv** - Gerenciamento de variáveis de ambiente

### DevOps
- **Docker** - Containerização
- **Docker Compose** - Orquestração de containers
- **Make** - Automação de tarefas

---

## 📦 Pré-requisitos

- **Python 3.8+** instalado
- **Node.js 16+** e npm instalado
- **Git** para clonar o repositório
- **Docker** (opcional, para deployment)

---

## 🚀 Instalação

### 1️⃣ Clone o Repositório

```bash
git clone https://github.com/VictorBrasileiroo/App_Gestao_Energia_Residencial.git
cd App_Gestao_Energia_Residencial
```

### 2️⃣ Configure o Backend

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 3️⃣ Configure o Middle Layer

```bash
cd ../middle
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 4️⃣ Configure o Frontend

```bash
cd ../frontend
npm install
```

### 5️⃣ Gere Dados de Exemplo (Opcional)

```bash
cd ..
python generate_realistic_data.py
```

Este script gerará dados realistas de consumo de energia para o período de 01/01/2025 até 27/10/2025.

---

## 💻 Uso

### Iniciar o Backend

```bash
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

Backend estará rodando em: `http://localhost:8000`
Documentação da API: `http://localhost:8000/docs`

### Iniciar o Middle Layer

```bash
cd middle
.\venv\Scripts\activate
uvicorn src.main:app --reload --port 8001
```

Middleware estará rodando em: `http://localhost:8001`

### Iniciar o Frontend

```bash
cd frontend
npm run dev
```

Frontend estará rodando em: `http://localhost:5173`

### 🐳 Usando Docker (Alternativa)

```bash
cd middle
docker-compose up -d
```

---

## 📁 Estrutura do Projeto

```
App_Gestao_Energia_Residencial/
│
├── 📂 backend/                    # API Principal
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py               # Entry point do FastAPI
│   │   ├── database.py           # Configuração do banco
│   │   ├── models.py             # Modelos SQLAlchemy
│   │   ├── schemas.py            # Schemas Pydantic
│   │   ├── auth/                 # Autenticação e segurança
│   │   ├── consumption/          # Gestão de consumo
│   │   ├── predictions/          # Modelos de ML
│   │   ├── alerts/               # Sistema de alertas
│   │   ├── dashboard/            # Dados do dashboard
│   │   ├── reports/              # Geração de relatórios
│   │   └── utils/                # Utilidades
│   └── requirements.txt
│
├── 📂 frontend/                   # Interface Web
│   ├── src/
│   │   ├── components/           # Componentes React
│   │   ├── pages/                # Páginas da aplicação
│   │   ├── services/             # Serviços API
│   │   ├── contexts/             # Context API
│   │   ├── styles/               # Estilos globais
│   │   └── utils/                # Utilitários
│   ├── public/                   # Arquivos estáticos
│   ├── package.json
│   └── vite.config.js
│
├── 📂 middle/                     # Camada Intermediária
│   ├── src/
│   │   ├── main.py
│   │   ├── config.py
│   │   └── routes/               # Rotas do middleware
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── requirements.txt
│
├── 📂 data/                       # Dados de consumo
│   ├── dados_consumo_por_hora.csv
│   └── dados_consumo_por_dia.csv
│
├── generate_realistic_data.py    # Gerador de dados
└── README.md                      # Este arquivo
```

---

## 🔌 API Endpoints

### Autenticação

```http
POST   /auth/register          # Registrar novo usuário
POST   /auth/login             # Login
GET    /auth/me                # Obter usuário atual
```

### Dashboard

```http
GET    /dashboard/summary      # Resumo geral do dashboard
GET    /dashboard/monthly      # Comparação mensal
```

### Consumo

```http
GET    /consumption/           # Listar consumos
POST   /consumption/upload     # Upload CSV
GET    /consumption/analytics  # Análises detalhadas
```

### Previsões

```http
GET    /predictions/           # Obter previsões
POST   /predictions/train      # Treinar modelo
```

### Alertas

```http
GET    /alerts/                # Listar alertas
POST   /alerts/                # Criar alerta
DELETE /alerts/{id}            # Deletar alerta
```

### Relatórios

```http
GET    /reports/monthly        # Relatório mensal
GET    /reports/annual         # Relatório anual
GET    /reports/export         # Exportar dados
```

📖 **Documentação Completa**: Acesse `/docs` na API para documentação interativa Swagger.

---

## 🤖 Machine Learning

### Modelo de Previsão

O sistema utiliza **Random Forest Regressor** para prever o consumo futuro de energia.

#### Features Utilizadas

- Mês do ano (1-12)
- Estação do ano (1-4)
- Temperatura média do mês
- Médias móveis de consumo
- Tendências históricas

#### Pipeline de Treinamento

1. **Coleta de Dados**: Dados históricos de consumo
2. **Feature Engineering**: Criação de features temporais
3. **Normalização**: StandardScaler para normalização
4. **Treinamento**: Random Forest com GridSearch
5. **Validação**: Cross-validation e métricas de erro
6. **Predição**: Forecasting para próximo mês

#### Métricas

- **MAE** (Mean Absolute Error)
- **RMSE** (Root Mean Squared Error)
- **R² Score**

---

## 📸 Screenshots

### Dashboard Principal
![Dashboard](./docs/screenshots/dashboard.png)

### Análise de Consumo
![Análise](./docs/screenshots/analytics.png)

### Previsões
![Previsões](./docs/screenshots/predictions.png)

### Alertas
![Alertas](./docs/screenshots/alerts.png)

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Diretrizes

- Siga os padrões de código do projeto
- Escreva testes para novas funcionalidades
- Atualize a documentação quando necessário
- Mantenha commits claros e descritivos

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👥 Autores

| Nome completo                       | Cargo                                       |
| ----------------------------------- | ------------------------------------------- |
| Victor André Lopes Brasileiro       | Gestor de projetos e desenvolvedor backend  |
| Clauderlan Batista Alves            | Desenvolvedor frontend                      |
| Artur Ferreira Marques da Silva     | Suporte técnico em desenvolvimento frontend |
| João Victor Duarte do Nascimento    | Desenvolvedor frontend                      |
| José Milton de Moraes Silva Neto    | Suporte técnico em desenvolvimento frontend |
| Davi Cavalcanti Muritiba            | Suporte técnico em desenvolvimento frontend |
| Laura Beatriz Lins Ramos Mainero    | Desenvolvedora backend                      |
| Yuri Raphael Mota de Araujo Barbosa | Desenvolvedor backend                       |
| Eduardo Gomes                       | Desenvolvedor full stack                    |
| Denilson Bulhões                    | Desenvolvedor full stack                    |
| Leonardo Vinícius                   | Desenvolvedor full stack                    |
| Matheus Giordini                    | Desenvolvedor full stack                    |
| Ayron                               | Desenvolvedor full stack                    |

---

## 📞 Contato

Para dúvidas, sugestões ou feedback:

- 📧 Email: [seu-email@exemplo.com](mailto:valb1@ic.ufal.br)
- 🐙 GitHub: [@VictorBrasileiroo](https://github.com/VictorBrasileiroo)
- 💼 LinkedIn: [Seu LinkedIn](https://www.linkedin.com/in/victorbrasileirooo/)

---

## 🙏 Agradecimentos

- Comunidade React e FastAPI
- Bibliotecas de código aberto utilizadas
- Contribuidores do projeto
---

## 🔮 Roadmap

### Versão 2.0 (Planejado)

- [ ] Integração com dispositivos IoT
- [ ] App mobile (React Native)
- [ ] Suporte para múltiplas residências
- [ ] Dashboard de administração
- [ ] Notificações em tempo real (WebSocket)
- [ ] Integração com APIs de concessionárias
- [ ] Análise de custo por aparelho
- [ ] Modo offline com sincronização
- [ ] Temas escuro/claro
- [ ] Internacionalização (i18n)

---

## ⚙️ Configuração Avançada

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz de cada serviço:

**Backend (.env)**
```env
DATABASE_URL=sqlite:///./energy.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Middle (.env)**
```env
BACKEND_URL=http://localhost:8000
PORT=8001
```

**Frontend (.env)**
```env
VITE_API_URL=http://localhost:8001
```

---

## 🐛 Troubleshooting

### Problemas Comuns

**Erro de CORS**
- Verifique se o frontend está na lista `allow_origins` do backend

**Banco de dados não encontrado**
- Execute o backend primeiro para criar o banco automaticamente

**Porta já em uso**
- Mude a porta nos comandos de inicialização

**Módulos não encontrados**
- Certifique-se de ter instalado todas as dependências

---

## 📊 Estatísticas do Projeto

- **Linhas de Código**: ~10.000+
- **Arquivos**: 50+
- **Componentes React**: 15+
- **API Endpoints**: 20+
- **Tempo de Desenvolvimento**: Em andamento

---
