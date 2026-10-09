# 📉 Termômetro do Desemprego Real e Subutilização no Brasil

Este projeto realiza a extração, o tratamento, a modelagem preditiva e a visualização interativa da **Taxa Combinada de Subutilização da Força de Trabalho** no Brasil. 

O objetivo analítico é ir além da métrica estática de desocupação tradicional do IBGE, capturando o "desemprego real" — ou seja, incluindo também os trabalhadores desalentados, a ociosidade oculta e a força de trabalho potencial em cada Estado (UF).

##  Arquitetura e Tecnologias

O pipeline do projeto foi desenhado para ser resiliente e modular, cobrindo o ciclo completo dos dados:

* **ETL (Extração e Tratamento):** Script automatizado para consumir a API do SIDRA/IBGE (Tabela 6441). Possui um sistema de *fallback* (contingência estruturada) para garantir a continuidade dos testes mesmo em caso de instabilidades de rede (DNS/Timeouts) no servidor do governo.
* **Machine Learning:** Engenharia de features temporais (*lags*) e treinamento de um modelo preditivo utilizando **XGBoost Regressor** para acompanhar tendências estaduais com alta precisão e baixo Erro Quadrático Médio (RMSE).
* **Data Viz (Dashboard):** Painel executivo interativo construído com **Streamlit** e **Plotly**, permitindo filtros granulares por Unidade da Federação, comparativos de ranking e visualização da evolução histórica.

**Stack Tecnológica:** `Python`, `Pandas`, `XGBoost`, `Scikit-Learn`, `Streamlit`, `Plotly`, `Requests`.

## 📂 Estrutura do Repositório

```text
desemprego-real-brasil/
├── data/
│   └── processed/       # Diretório onde o CSV tratado é salvo localmente
├── dashboard/
│   └── app.py           # Código fonte do painel interativo (Streamlit)
├── src/
│   ├── extract.py       # Script de ingestão da API do IBGE / Geração de Contingência
│   └── train.py         # Treinamento do modelo de Machine Learning (XGBoost)
├── .gitignore           # Arquivos ignorados pelo Git
├── requirements.txt     # Dependências do projeto
└── README.md            # Documentação


  Como Clonar e Executar Localmente
Siga o passo a passo abaixo para rodar o projeto em qualquer ambiente local.

1. Clone o repositório e acesse a pasta:

Bash
git clone [https://github.com/SEU-USUARIO/desemprego-real-brasil.git](https://github.com/SEU-USUARIO/desemprego-real-brasil.git)
cd desemprego-real-brasil
2. Instale as dependências necessárias:

Bash
pip install -r requirements.txt
3. Execute o pipeline de Extração de Dados (ETL):

Bash
python src/extract.py
(Este comando gerará o arquivo subutilizacao_uf.csv na pasta data/processed/ baseando-se na API oficial ou no fallback estruturado).

4. Treine o Modelo de Machine Learning:

Bash
python src/train.py
(O script aplicará engenharia de recursos com base em defasagens temporais e treinará o algoritmo XGBoost, imprimindo as métricas de validação RMSE).

5. Inicie o Dashboard Web:

Bash
streamlit run dashboard/app.py
(O Streamlit iniciará um servidor local e abrirá o painel automaticamente no seu navegador padrão).