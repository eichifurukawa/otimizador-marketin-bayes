<h1 align="center">📈 Otimizador de Campanhas de Marketing com Teorema de Bayes 📈</h1>

## 📝 Descrição do projeto 📝
<p align="left">
Este projeto é uma aplicação web que utiliza o Teorema de Bayes para analisar e otimizar campanhas de marketing digital. A ferramenta processa dados de desempenho de diferentes canais de marketing (como Google Ads, Instagram, Email, etc.) e fornece recomendações baseadas em probabilidades de conversão e ROI (Retorno sobre Investimento).
</p>

## ✨ Funcionalidades Principais ✨
- Análise Bayesiana: Calcula a probabilidade de conversão para cada canal usando o Teorema de Bayes
- Recomendações Inteligentes: Sugere o melhor canal para alocação de recursos com base em scores combinados
- Visualização de Dados: Exibe os dados brutos e resultados de forma clara e organizada
- Dados de Exemplo: Permite testar a aplicação sem precisar carregar dados

## 🛠️ Tecnologias Utilizadas 🛠️
- Backend: FastAPI (Python)
- Frontend: HTML, CSS, JavaScript
- Bibliotecas: Pandas, NumPy
- Estilo: CSS moderno e responsivo

## 🚀 Como Executar o Projeto

1. Clone o repositório:
```bash
git clone https://github.com/eichifurukawa/otimizador-marketin-bayes.git
cd otimizador-marketin-bayes
```
2. Certifique-se de ter o [🐍Python](https://www.python.org/downloads/) instalado 
3. Instale as dependências:
```bash
pip install -r requirements.txt
```
3. Entre na pasta '\backend' pelo terminal:
```bash
cd backend
```
4. Execute o servidor FastAPI:
```bash
python -m uvicorn app:app --reload
```
```bash
INFO:     Will watch for changes in these directories: ['C:\\otimizador-marketin-bayes\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12192] using StatReload
INFO:     Started server process [7536]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```
5. Abra o arquivo 'index.html'

## 📂 Estrutura de Arquivos
```bash
otimizador-marketin-bayes/
│   README.md
│
├───backend
│   │   app.py                      # Lógica principal da API
│   │   requirements.txt            # Dependências Python
│   │
│   ├───data
│   │       sample_data.csv         # Dados de exemplo
│   │
│   └───__pycache__
│           app.cpython-311.pyc
│
└───frontend
        index.html                  # Página principal
        script.js                   # Interações do usuário
        style.css                   # Estilos CSS
```

##  🎲 Formato dos Dados

| Coluna       | Tipo     | Descrição                         |
|--------------|----------|-----------------------------------|
| channel      | string   | Nome do canal de marketing        |
| impressions  | inteiro  | Número de impressões/exibições    |
| clicks       | inteiro  | Número de cliques                 |
| conversions  | inteiro  | Número de conversões              |
| cost         | float    | Custo total (em dólares)          |





