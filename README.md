# TCC_Escada_Rolante

## Sobre o Jogo (game.py)
O game.py é um jogo interativo desenvolvido para estudar a atenção e tempo de reação de jogadores com TDAH. O jogo apresenta personagens em movimento em uma escada rolante, onde o jogador deve identificar e selecionar alvos específicos baseado em diferentes modos de jogo:
- Modo de Seleção Unica: Encontrar e Selecionar um unico personagem em meio a multidão
- Modo de Multiplas Escolhas: Encontrar e Selecionar um personagem recorrente ao meio da multidão
- Modo infinito: O jogador devera encontrar o personagem pre-determinado, para aumentar o tempo do cronometro

O jogo gera um arquivo JSON com dados detalhados sobre:
- Posições dos cliques
- Tempo de reação do jogador
- Acertos e erros
- Pontuação
- Modo de jogo atual

#### Tarefas Pendentes:
- Alterar o modo de multiplas escolhas e possivelmente o modo infinito, para o personagem alvo mudar a cada acerto
- Alterar para que o jogo seja contínuo (se clicar no alvo errado o jogo não para, no modo infinito porem o jogador perde um pouco de tempo) com um placar de coleta
- Melhorar a UI

## Visualização de Dados (python-data-viz)

A pasta `python-data-viz` contém ferramentas para análise e visualização dos dados do jogo. Processa a saída JSON do jogo principal e fornece insights através de:

### Funcionalidades
- Mapas de calor mostrando áreas de interação do jogador
- Visualização de estatísticas do jogo incluindo:
  - Distribuição dos modos de jogo
  - Análise de pontuação
  - Medições de tempo de reação
  - Métricas de desempenho do jogador

### Uso
Navegue até a pasta python-data-viz e execute:
```bash
python src/main.py
```

A ferramenta de visualização espera encontrar o arquivo JSON de saída do jogo no diretório principal do projeto. Ela irá gerar representações visuais e estatísticas que ajudam a analisar o comportamento do jogador e o desempenho do jogo.

### Dependências
Os pacotes Python necessários estão listados em `requirements.txt` e incluem:
- pygame
- pandas (processamento de dados)
- seaborn (visualização de mapas de calor)
- matplotlib (plotagem)
- numpy (operações numéricas)