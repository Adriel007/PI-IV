# Sistema de Análise de Evasão Escolar
Sistema desenvolvido para análise e previsão de evasão escolar em cursos superiores, utilizando técnicas de Machine Learning e visualização de dados.
## 📋 Descrição do Projeto
Este projeto consiste em uma aplicação desktop desenvolvida em ElectronJS que permite:
- Carregar dados de evasão escolar de diferentes fontes (CSV, Excel, Google Sheets)
- Visualizar tendências e padrões através de gráficos interativos
- Realizar previsões de evasão utilizando diferentes modelos de Machine Learning
- Gerar análises comparativas entre cursos e períodos
## 🚀 Funcionalidades
- **Gestão de Dados**
  - Importação de planilhas locais (CSV, TXT, Excel)
  - Integração com Google Sheets (Em Breve)
  - Uso de template padronizado para validação automática
- **Visualização de Dados**
  - Gráficos de distribuição por curso
  - Análise temporal de desistências
  - Comparativo entre turnos e períodos
  - Dashboard interativo
- **Análise Preditiva**
  - Previsão de taxas de evasão
  - Comparação entre diferentes modelos (Linear, Ridge, Lasso, Random Forest)
  - Avaliação de performance dos modelos
  - Visualização das previsões
## 🛠️ Tecnologias Utilizadas
- **Electron** - Framework desktop
- **Python 3.x** - Backend e análise de dados
- **Pandas** - Manipulação de dados
- **Scikit-learn** - Modelos de Machine Learning
- **Chart.js** - Visualização de dados
- **TailwindCSS** - Estilização
## 📁 Estrutura do Projeto
```
PI-IV/
├── src/
│   ├── main.js           # Processo principal Electron
│   ├── preload.js        # Bridge IPC
│   ├── ml/
│   │   └── analysis.py   # Análise preditiva
│   └── renderer/         # Interface do usuário
├── transformacao/        # Scripts de ETL
└── README.md             # Documentação
```

## ⚙️ Como Executar
1. Clone o repositório:

```bash
git clone --branch electron --single-branch https://github.com/Adriel007/PI-IV/
cd ./pi-iv
```


2. Instale as dependências:
```bash
npm install
pip install -r requirements.txt
```


3. Execute a aplicação:
```bash
npm start
```


## 🤝 Como Contribuir
1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Faça o Commit das suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Faça o Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## ✨ Autores
* **Adriel Andrade** - *Desenvolvimento Inicial* - [GitHub](https://github.com/adriel007)
* **Henrique Freitas** - *Desenvolvimento Inicial* - [GitHub](https://github.com/HenriqueRDF)
* **Kaíke Silva** - *Desenvolvimento Inicial* - [GitHub](https://github.com/)

## 📊 Status do Projeto
O projeto está em desenvolvimento ativo, com atualizações regulares e novas funcionalidades sendo adicionadas.