# Sistema de Análise de Evasão Escolar
Sistema desenvolvido para análise e previsão de evasão escolar em cursos superiores, utilizando técnicas de Machine Learning e visualização de dados.
## 📋 Descrição do Projeto
Este projeto consiste em uma aplicação desktop desenvolvida em Python que permite:
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
- **Python 3.x**
- **PyQt5** - Interface gráfica
- **Pandas** - Manipulação de dados
- **Scikit-learn** - Modelos de Machine Learning
- **Matplotlib** - Visualização de dados
- **Google Sheets API** - Integração com planilhas online
## 📁 Estrutura do Projeto
PI-IV/
├── app/
│   ├── data/
│   │   ├── data_loader.py    # Carregamento de dados
│   │   └── data_processor.py # Processamento de dados
│   ├── prediction/
│   │   └── prediction.py     # Modelos preditivos
│   ├── ui/
│   │   ├── charts.py        # Componentes de visualização
│   │   └── main_window.py   # Interface principal
│   └── main.py              # Ponto de entrada da aplicação
└── README.md



## ⚙️ Como Executar
1. Clone o repositório:

```bash
git clone https://github.com/Adriel007/PI-IV/
```


2. Instale as dependências:
```bash
pip install -r requirements.txt
```


3. Execute a aplicação:
```bash
python app/main.py
```


## 🤝 Como Contribuir
1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Faça o Commit das suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Faça o Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## ✨ Autores
* **Adriel Andrade** - *Desenvolvimento Inicial* - [GitHub](https://github.com/adriel007)
* **Henrique Freitas** - *Desenvolvimento Inicial* - [GitHub](https://github.com/)
* **Kaíke Silva** - *Desenvolvimento Inicial* - [GitHub](https://github.com/)

## 📊 Status do Projeto
O projeto está em desenvolvimento ativo, com atualizações regulares e novas funcionalidades sendo adicionadas.