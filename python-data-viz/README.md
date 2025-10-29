# python-data-viz

Este projeto foi desenvolvido para ler os arquivos JSON de saída do `game.py` e exibir análises visuais detalhadas, incluindo mapas de calor, estatísticas de desempenho e análises específicas por modo de jogo.

## Funcionalidades

- Visualização de Dados em Tabela: Exibe todas as sessões de jogo com informações detalhadas
- Mapa de Calor: Gera visualização do movimento do mouse durante o jogo
- Análise por Modo de Jogo: Análises específicas para cada um dos 4 modos disponíveis:
  - Modo de Aparição Única (GAME_MODE_SINGLE = 0): O alvo aparece uma vez
  - Modo Alternado (GAME_MODE_ALTERNATING = 1): O alvo alterna a cada acerto
  - Modo Infinito (GAME_MODE_INFINITE = 2): Jogo contínuo com tempo adicional por acertos
  - Modo Seta Colorida (GAME_MODE_ARROW = 3): Seta girante apontando para quadrantes coloridos

## Estrutura do Projeto

```
python-data-viz
├── src
│   ├── main.py          # Ponto de entrada da aplicação
│   ├── visualization     # Módulo para funções de visualização
│   │   ├── __init__.py
│   │   ├── heatmap.py   # Funções para gerar mapas de calor
│   │   └── game_mode_analysis.py # Análises específicas por modo de jogo
│   ├── utils            # Módulo para funções utilitárias
│   │   ├── __init__.py
│   │   └── json_reader.py # Funções para ler dados JSON
│   └── config           # Módulo para configurações
│       ├── __init__.py
│       └── settings.py   # Configurações do projeto
├── tests                # Módulo para testes unitários
│   ├── __init__.py
│   └── test_json_reader.py # Testes para json_reader.py
├── requirements.txt     # Lista de dependências
└── README.md            # Documentação do projeto
```

## Instalação

1. Clone o repositório:
   ```
   git clone <repository-url>
   cd python-data-viz
   ```

2. Instale as dependências necessárias:
   ```
   pip install -r requirements.txt
   ```

## Uso

Para executar a aplicação, use o seguinte comando:
```
python src/main.py
```

A aplicação abrirá uma janela de seleção de arquivo. Selecione um arquivo JSON de dados do jogo e a interface exibirá:

1. Tabela de Dados: Resumo de todas as sessões com métricas principais
2. Botões de Análise:
   - Gerar Mapa de Calor para Sessão Selecionada: Visualiza o movimento do mouse
   - Análise por Modo de Jogo: Gera relatório completo com:
     - Estatísticas de tempo de reação por modo
     - Comparação de taxas de sucesso
     - Progressão de pontuação (para modos Infinito e Seta)
     - Evolução temporal do desempenho
   - Exportar Dados: Salva os dados em CSV ou Excel

## Análises Disponíveis

### Análise de Tempo de Reação
- Tempo médio, mediano, mínimo e máximo
- Desvio padrão
- Comparação visual entre modos
- Distribuição por histogramas
- Evolução ao longo das tentativas com média móvel

### Análise de Taxa de Sucesso
- Porcentagem de acertos por modo
- Distribuição de tentativas
- Comparação visual entre modos

### Análise de Progressão
- Gráficos de progressão de pontuação
- Linhas de tendência
- Análise específica para modos Infinito e Seta Colorida

## Testes

Para executar os testes, use o comando:
```
pytest tests/
```

Isso executará os testes unitários definidos em `test_json_reader.py`.

## Requisitos

- Python 3.7+
- pandas
- matplotlib
- seaborn
- numpy
- tkinter (geralmente incluído com Python)

## Licença

Este projeto está licenciado sob a Licença MIT.