# 🎮 Can I Run It? - API & Dashboard

Uma aplicação Full-Stack modular que compara o hardware do utilizador (CPU e GPU) com os requisitos mínimos oficiais dos jogos na Steam, informando se o jogo roda liso, sofre ou não roda.

## 🚀 Tecnologias Utilizadas
* **Backend:** Python, FastAPI, Pydantic
* **Processamento de Dados:** Pandas, TheFuzz (Fuzzy String Matching)
* **Integração:** Steam Store API, BeautifulSoup4
* **Frontend:** HTML5, CSS3 (Neon UI), JavaScript Vanilla
* **Arquitetura:** Microservices / Layered Architecture (Models, Services, API)

## ✨ Funcionalidades
- Pesquisa inteligente de Jogos direto da base de dados da Steam (Autocomplete).
- Datalist automático com milhares de CPUs e GPUs reais (dados extraídos do PassMark).
- Algoritmo de tolerância que classifica a performance em 4 níveis (Ultra, Liso, Sofrendo e Não Roda).

## ⚙️ Como executar na sua máquina
1. Clone este repositório:
   `git clone https://github.com/Heliojrdevs/can-i-run-it.git`
2. Instale as dependências:
   `pip install fastapi uvicorn pandas thefuzz requests beautifulsoup4 fastapi-cors`
3. Inicie o servidor:
   `python -m uvicorn app.main:app --reload`
4. Abra o arquivo `frontend/index.html` no seu navegador!
