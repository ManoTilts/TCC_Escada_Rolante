# TCC_Escada_Rolante

## Sobre o Projeto

Este projeto foi desenvolvido como parte de um Trabalho de Conclusão de Curso (TCC) para estudar a atenção, tempo de reação e padrões comportamentais em jogadores, com foco especial em indivíduos com TDAH (Transtorno do Déficit de Atenção com Hiperatividade).

O jogo utiliza uma metáfora visual de escadas rolantes com personagens em movimento para testar diferentes aspectos cognitivos através de 4 modos de jogo distintos.

## Sobre o Jogo (game.py)

### Conceito
O Memory Escalator é um jogo interativo que apresenta personagens em movimento em escadas rolantes. O jogador deve identificar e selecionar alvos específicos baseado em diferentes critérios, dependendo do modo de jogo escolhido.

### Modos de Jogo

#### 1. Modo de Aparição Única (GAME_MODE_SINGLE = 0)
- Objetivo: Encontrar e clicar em um personagem específico mostrado previamente
- Mecânica: O personagem alvo é exibido por alguns segundos, depois aparece uma vez entre outros personagens
- Avalia: Memória visual de curto prazo, atenção seletiva

#### 2. Modo Alternado (GAME_MODE_ALTERNATING = 1)
- Objetivo: Encontrar personagens que mudam a cada acerto
- Mecânica: Após cada acerto, um novo personagem alvo é definido
- Avalia: Flexibilidade cognitiva, adaptação, memória de trabalho

#### 3. Modo Infinito (GAME_MODE_INFINITE = 2)
- Objetivo: Conseguir a maior pontuação possível dentro do tempo limite
- Mecânica: Cada acerto adiciona tempo extra ao cronômetro
- Avalia: Atenção sustentada, resistência à fadiga, desempenho sob pressão
- Diferencial: Ideal para medir concentração prolongada

#### 4. Modo Seta Colorida (GAME_MODE_ARROW = 3)
- Objetivo: Clicar no quadrante correto quando a seta apontar para ele
- Mecânica: Uma seta gira no centro, a tela é dividida em 4 quadrantes coloridos
- Avalia: Reflexos, coordenação visuomotora, tempo de reação puro
- Diferencial: Menos dependente de memória, mais de reflexos

### Dados Coletados

O jogo coleta dados abrangentes para análise científica:

#### Métricas por Tentativa
- Tempo de reação: Do spawn do alvo até o clique
- Sucesso/Falha: Se o jogador acertou ou errou
- Pontuação: Score acumulado
- Características do alvo: Corpo, rosto, cabeça e chapéu do personagem
- Movimentos do mouse: Quantidade e distância percorrida
- Velocidade média do mouse: Pixels por segundo
- Tempo de hesitação: Delay entre ver o alvo e clicar
- Cliques antes do sucesso: Tentativas erradas antes de acertar
- Posições de todos os cliques: Coordenadas X, Y e timestamp

#### Métricas por Sessão
- Duração total da sessão
- Total de cliques (corretos e incorretos)
- Taxa de acerto geral
- Falsos positivos: Cliques em personagens errados
- Quebras de foco: Períodos longos (>3s) sem interação
- Rastreamento de mouse: Posição contínua durante o jogo

#### Métricas Específicas do Modo Seta
- Quadrante clicado vs quadrante alvo
- Ângulo da seta no momento do clique
- Velocidade de rotação da seta
- Precisão de timing: Se clicou no momento certo
- Precisão espacial: Se clicou no quadrante correto

### Formato de Saída

Os dados são salvos em formato JSON estruturado em:
```
playerdata/
  └── YYYY-MM-DD/
      └── game_data_YYYYMMDD_HHMMSS.json
```

Exemplo de estrutura:
```json
{
  "sessions": [
    {
      "session_id": "20251029_143022",
      "username": "Jogador1",
      "game_mode": 2,
      "session_metrics": {
        "total_clicks": 45,
        "correct_clicks": 38,
        "incorrect_clicks": 7,
        "focus_breaks": 2,
        "session_duration": 125.5
      },
      "trials": [
        {
          "game_mode": 2,
          "reaction_time": 1.234,
          "success": true,
          "trial_metrics": {
            "mouse_movements": 15,
            "hesitation_time": 0.5,
            "average_mouse_speed": 234.5,
            "mouse_path_length": 456.7
          }
        }
      ]
    }
  ]
}
```

### Propósito Científico

Os dados coletados permitem análise de:

1. Atenção Seletiva: Capacidade de focar em estímulos específicos
2. Atenção Sustentada: Manutenção do foco ao longo do tempo
3. Velocidade de Processamento: Rapidez na tomada de decisão
4. Impulsividade: Padrão de cliques errados e precipitados
5. Fadiga Cognitiva: Degradação do desempenho ao longo da sessão
6. Padrões Visuais: Estratégias de busca através do rastreamento de mouse
7. Coordenação Motora: Precisão e suavidade dos movimentos

## Visualização de Dados (python-data-viz)

### Funcionalidades

A pasta `python-data-viz` contém ferramentas avançadas para análise e visualização dos dados coletados:

#### 1. Tabela de Dados Interativa
- Visualização de todas as sessões
- Filtros por jogador, modo, data
- Estatísticas resumidas por jogo
- Exportação para CSV/Excel

#### 2. Mapas de Calor
- Visualização de áreas de maior interação
- Identifica padrões de busca visual
- Destaca zonas de concentração de cliques

#### 3. Análise por Modo de Jogo
Relatório completo com 4 abas:

Aba 1: Tempo de Reação
- Boxplot comparativo entre modos
- Histogramas de distribuição
- Estatísticas descritivas (média, mediana, desvio padrão)
- Identificação de outliers

Aba 2: Taxa de Sucesso
- Porcentagem de acertos por modo
- Gráfico de barras comparativo
- Distribuição de tentativas (pizza)
- Análise de erros

Aba 3: Progressão de Pontuação
- Evolução da pontuação ao longo do tempo
- Linhas de tendência
- Identificação de padrões de aprendizado
- Específico para modos Infinito e Seta

Aba 4: Evolução Temporal
- Mudança no tempo de reação ao longo das tentativas
- Média móvel para suavizar flutuações
- Detecção de fadiga
- Indicadores de melhora/piora

#### 4. Métricas Avançadas
- Análise de movimentos do mouse
- Padrões de hesitação
- Precisão de cliques
- Quebras de concentração

### Como Usar

```bash
cd python-data-viz
python src/main.py
```

1. Selecione um arquivo JSON da pasta `playerdata/`
2. Visualize a tabela com resumo dos dados
3. Clique em "Análise por Modo de Jogo" para relatório completo
4. Selecione uma sessão e clique em "Gerar Mapa de Calor"
5. Exporte dados para análise externa (CSV/Excel)

### Dependências

```bash
pip install -r requirements.txt
```

Pacotes necessários:
- `pygame` - Motor do jogo
- `pandas` - Processamento de dados
- `seaborn` - Visualização de mapas de calor
- `matplotlib` - Plotagem de gráficos
- `numpy` - Operações numéricas

## Aplicações Científicas

### Para Pesquisadores
- Dados estruturados prontos para análise estatística
- Múltiplas métricas cognitivas e comportamentais
- Comparação entre grupos (TDAH vs controle)
- Análise longitudinal de progresso

### Para Clínicos
- Ferramenta de avaliação complementar
- Monitoramento de tratamento
- Identificação de padrões específicos de TDAH
- Relatórios visuais para pacientes e familiares

### Para Educadores
- Avaliação de atenção em ambiente lúdico
- Identificação precoce de dificuldades
- Acompanhamento de intervenções
- Feedback visual e motivador

## Próximos Passos

### Melhorias Planejadas

- Machine Learning: Modelo preditivo para identificar padrões de TDAH
- Análise de Clusters: Agrupamento automático de perfis de jogadores
- Dashboard Web: Interface online para visualização em tempo real
- Modo Multiplayer: Comparação direta entre jogadores
- Níveis de Dificuldade: Adaptação automática baseada no desempenho
- Relatórios PDF: Geração automática de laudos
- Integração com EEG: Correlação com dados neurológicos
- Gamificação: Sistema de conquistas e recompensas

### Validação Científica

- Validação com grupos controle
- Estudo piloto com população TDAH diagnosticada
- Análise de confiabilidade teste-reteste
- Correlação com testes neuropsicológicos padrão
- Publicação dos resultados em periódicos científicos

## Como Executar

### Requisitos
- Python 3.7 ou superior
- Pygame instalado
- Dependências do visualization (ver requirements.txt)

### Executando o Jogo
```bash
python game.py
```

### Executando Análise de Dados
```bash
cd python-data-viz
python src/main.py
```

## Contribuindo

Contribuições são bem-vindas. Áreas de interesse:
- Novos modos de jogo
- Métricas adicionais
- Visualizações aprimoradas
- Testes com usuários reais
- Documentação

## Licença

Este projeto está sob a licença especificada no arquivo LICENSE.

## Contato

Para dúvidas, sugestões ou colaborações científicas, abra uma issue no repositório.

---

Nota Importante: Este jogo é uma ferramenta de pesquisa e não substitui diagnóstico clínico profissional. Deve ser usado apenas como complemento a avaliações neuropsicológicas formais.