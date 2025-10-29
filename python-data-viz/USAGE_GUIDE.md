# Guia de Uso - Análise de Dados do Memory Escalator

## Visão Geral

Este programa analisa os dados coletados do jogo Memory Escalator, oferecendo visualizações e estatísticas detalhadas para cada um dos 4 modos de jogo disponíveis.

## Modos de Jogo

### 1. Modo de Aparição Única (GAME_MODE_SINGLE = 0)
- O jogador vê um personagem alvo no início
- O alvo aparece uma única vez na escada rolante
- Objetivo: Clicar no personagem correto quando ele passar

### 2. Modo Alternado (GAME_MODE_ALTERNATING = 1)
- Similar ao modo único, mas o alvo alterna após cada acerto
- Testa memória de longo prazo e adaptação
- A cada acerto, um novo alvo é definido

### 3. Modo Infinito (GAME_MODE_INFINITE = 2)
- Jogo contínuo com limite de tempo
- Cada acerto correto adiciona tempo extra
- Objetivo: Conseguir a maior pontuação possível
- Ideal para medir desempenho sustentado

### 4. Modo Seta Colorida (GAME_MODE_ARROW = 3)
- Uma seta gira no centro da tela
- A tela é dividida em 4 quadrantes coloridos
- A seta tem a cor do quadrante alvo
- Objetivo: Clicar no quadrante correto quando a seta apontar para ele
- Testa reflexos e atenção visual

## Como Usar o Programa

### Passo 1: Iniciar o Programa

```bash
cd python-data-viz
python src/main.py
```

### Passo 2: Selecionar Arquivo de Dados

1. Uma janela de seleção de arquivo será aberta
2. Navegue até a pasta `playerdata/`
3. Selecione um arquivo JSON (ex: `game_data_20251008_134450.json`)

### Passo 3: Explorar os Dados

#### Tabela de Dados
- Visualize todas as sessões de jogo
- Informações incluem:
  - ID da Sessão
  - Nome do Usuário
  - Número do Jogo
  - Modo de Jogo
  - Pontuação
  - Taxa de Sucesso
  - Tempo Médio de Reação

#### Gerar Mapa de Calor
1. Selecione uma linha na tabela
2. Clique em "Gerar Mapa de Calor para Sessão Selecionada"
3. Visualize onde o mouse se moveu durante o jogo

#### Análise por Modo de Jogo
1. Clique em "Análise por Modo de Jogo"
2. Uma nova janela com 4 abas será aberta:

Aba 1: Tempo de Reação
- Estatísticas detalhadas (média, mediana, min, max, desvio padrão)
- Boxplot comparativo entre modos
- Histogramas de distribuição para cada modo

Aba 2: Taxa de Sucesso
- Porcentagem de acertos por modo
- Gráfico de barras comparativo
- Gráfico de pizza mostrando distribuição de tentativas

Aba 3: Progressão de Pontuação
- Gráficos de progressão ao longo do tempo
- Linhas de tendência
- Específico para modos Infinito e Seta Colorida

Aba 4: Evolução Temporal
- Como o tempo de reação evolui ao longo das tentativas
- Média móvel para identificar padrões
- Análise separada para cada modo

#### Exportar Dados
1. Clique em "Exportar Dados"
2. Escolha o formato (CSV ou Excel)
3. Selecione o local para salvar

## Interpretando os Resultados

### Tempo de Reação
- Tempo Médio Baixo: Indica reflexos rápidos e boa familiaridade com o jogo
- Desvio Padrão Baixo: Indica consistência no desempenho
- Tendência Decrescente: Sugere melhora com a prática

### Taxa de Sucesso
- Maior que 80%: Excelente desempenho
- 60-80%: Bom desempenho
- Menor que 60%: Pode indicar dificuldade ou falta de concentração

### Comparação Entre Modos
- Modo Seta: Geralmente tem tempos de reação mais rápidos (reflexos puros)
- Modo Infinito: Testa resistência e consistência
- Modos Único/Alternado: Testam memória visual de curto prazo

## Dicas de Análise

1. Compare múltiplas sessões do mesmo usuário para ver evolução
2. Analise padrões no mapa de calor para entender estratégias visuais
3. Observe a média móvel para identificar fadiga ou melhora
4. Compare diferentes usuários para entender variações individuais

## Solução de Problemas

### Erro ao abrir arquivo
- Verifique se o arquivo JSON está bem formatado
- Certifique-se de que está na pasta `playerdata/`

### Gráficos não aparecem
- Verifique se matplotlib está instalado: `pip install matplotlib`
- Tente reinstalar: `pip install --upgrade matplotlib`

### Dados faltando
- Alguns modos podem não ter sido jogados
- Gráficos mostrarão "Sem dados" para esses casos

### Erro de memória
- Arquivos muito grandes podem causar problemas
- Tente analisar arquivos de dias individuais

## Estrutura dos Dados JSON

```json
{
  "sessions": [
    {
      "session_id": "20251008_134241",
      "username": "Jogador1",
      "game_mode": 3,
      "trials": [
        {
          "trial_start_time": 1759941761.388815,
          "game_mode": 3,
          "target_spawn_time": 1759941761.388816,
          "selection_time": 1759941764.056037,
          "success": true,
          "reaction_time": 2.667222,
          "score": 1
        }
      ],
      "mouse_tracking": [
        {
          "timestamp": 1759941761.0,
          "x": 700,
          "y": 500,
          "game_state": 2
        }
      ]
    }
  ]
}
```

## Contribuindo

Para adicionar novos tipos de análise:

1. Edite `src/visualization/game_mode_analysis.py`
2. Adicione novas funções de plotagem
3. Atualize `generate_comprehensive_report()` para incluir suas análises
4. Adicione nova aba em `display_report_window()`

## Contato

Para dúvidas ou sugestões, abra uma issue no repositório do projeto.
