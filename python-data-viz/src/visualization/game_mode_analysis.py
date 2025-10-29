"""
Módulo para análise específica de cada modo de jogo.
Fornece visualizações e estatísticas detalhadas para:
- Modo de Aparição Única (GAME_MODE_SINGLE = 0)
- Modo Alternado (GAME_MODE_ALTERNATING = 1)
- Modo Infinito (GAME_MODE_INFINITE = 2)
- Modo Seta Colorida (GAME_MODE_ARROW = 3)
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Constantes dos modos de jogo
GAME_MODE_SINGLE = 0
GAME_MODE_ALTERNATING = 1
GAME_MODE_INFINITE = 2
GAME_MODE_ARROW = 3

MODE_NAMES = {
    GAME_MODE_SINGLE: "Modo de Aparição Única",
    GAME_MODE_ALTERNATING: "Modo Alternado",
    GAME_MODE_INFINITE: "Modo Infinito",
    GAME_MODE_ARROW: "Modo Seta Colorida"
}

def get_mode_name(mode):
    """Retorna o nome amigável do modo de jogo"""
    if isinstance(mode, str):
        mode = int(mode)
    return MODE_NAMES.get(mode, f"Modo Desconhecido ({mode})")

def extract_trials_by_mode(data):
    """
    Extrai todas as tentativas organizadas por modo de jogo
    
    Args:
        data: Dados JSON carregados contendo as sessões de jogo
        
    Returns:
        dict: Dicionário com listas de tentativas para cada modo
    """
    sessions = data.get('sessions', [])
    if not sessions and isinstance(data, dict):
        sessions = [data]
    
    trials_by_mode = {
        GAME_MODE_SINGLE: [],
        GAME_MODE_ALTERNATING: [],
        GAME_MODE_INFINITE: [],
        GAME_MODE_ARROW: []
    }
    
    for session in sessions:
        username = session.get('username', 'Anônimo')
        trials = session.get('trials', [])
        
        for trial in trials:
            game_mode = trial.get('game_mode')
            if game_mode is not None:
                if isinstance(game_mode, str):
                    game_mode = int(game_mode)
                if game_mode in trials_by_mode:
                    # Adiciona informação do usuário à tentativa
                    trial_copy = trial.copy()
                    trial_copy['username'] = username
                    trials_by_mode[game_mode].append(trial_copy)
    
    return trials_by_mode

def analyze_reaction_times(trials_by_mode):
    """
    Analisa tempos de reação para cada modo de jogo
    
    Args:
        trials_by_mode: Dicionário com tentativas organizadas por modo
        
    Returns:
        DataFrame com estatísticas de tempo de reação por modo
    """
    stats = []
    
    for mode, trials in trials_by_mode.items():
        if not trials:
            continue
            
        reaction_times = [t['reaction_time'] for t in trials if t.get('reaction_time') is not None]
        
        if reaction_times:
            stats.append({
                'Modo': get_mode_name(mode),
                'Tentativas': len(trials),
                'Tempo Médio (s)': np.mean(reaction_times),
                'Tempo Mediano (s)': np.median(reaction_times),
                'Desvio Padrão': np.std(reaction_times),
                'Tempo Mínimo (s)': np.min(reaction_times),
                'Tempo Máximo (s)': np.max(reaction_times)
            })
    
    return pd.DataFrame(stats)

def analyze_success_rates(trials_by_mode):
    """
    Analisa taxas de sucesso para cada modo de jogo
    
    Args:
        trials_by_mode: Dicionário com tentativas organizadas por modo
        
    Returns:
        DataFrame com estatísticas de sucesso por modo
    """
    stats = []
    
    for mode, trials in trials_by_mode.items():
        if not trials:
            continue
            
        total = len(trials)
        successes = sum(1 for t in trials if t.get('success', False))
        
        stats.append({
            'Modo': get_mode_name(mode),
            'Total de Tentativas': total,
            'Acertos': successes,
            'Erros': total - successes,
            'Taxa de Sucesso (%)': (successes / total * 100) if total > 0 else 0
        })
    
    return pd.DataFrame(stats)

def plot_reaction_times_comparison(trials_by_mode):
    """
    Cria gráficos comparativos de tempo de reação entre modos
    """
    # Conta quantos modos têm dados
    modes_with_data = []
    for mode, trials in trials_by_mode.items():
        reaction_times = [t['reaction_time'] for t in trials if t.get('reaction_time') is not None]
        if reaction_times:
            modes_with_data.append((mode, trials, reaction_times))
    
    # Se não houver dados, retorna figura vazia
    if not modes_with_data:
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        ax.text(0.5, 0.5, 'Nenhum dado de tempo de reação disponível', 
                ha='center', va='center', fontsize=14)
        ax.axis('off')
        return fig
    
    # Cria layout baseado na quantidade de modos com dados
    n_modes = len(modes_with_data)
    if n_modes == 1:
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    else:
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    fig.suptitle('Análise de Tempos de Reação por Modo de Jogo', fontsize=16, fontweight='bold')
    
    # Prepara dados para boxplot
    data_for_boxplot = [reaction_times for _, _, reaction_times in modes_with_data]
    labels_for_boxplot = [get_mode_name(mode) for mode, _, _ in modes_with_data]
    
    # Boxplot comparativo (sempre na primeira posição)
    if n_modes == 1:
        ax_box = axes[0]
    else:
        ax_box = axes[0, 0]
    
    ax_box.boxplot(data_for_boxplot, labels=labels_for_boxplot)
    ax_box.set_title('Comparação de Tempos de Reação (Boxplot)', fontweight='bold')
    ax_box.set_ylabel('Tempo de Reação (segundos)')
    ax_box.grid(True, alpha=0.3)
    ax_box.tick_params(axis='x', rotation=15)
    
    # Histogramas para cada modo
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
    
    for idx, (mode, trials, reaction_times) in enumerate(modes_with_data):
        # Calcula posição no grid
        if n_modes == 1:
            ax = axes[1]
        else:
            # Pula a primeira posição (boxplot)
            pos = idx + 1
            row = pos // 2
            col = pos % 2
            ax = axes[row, col]
        
        ax.hist(reaction_times, bins=min(20, len(reaction_times)), 
                color=colors[idx % len(colors)], alpha=0.7, edgecolor='black')
        ax.set_title(get_mode_name(mode), fontweight='bold')
        ax.set_xlabel('Tempo de Reação (s)')
        ax.set_ylabel('Frequência')
        ax.grid(True, alpha=0.3)
        
        # Adiciona linha da média
        mean_time = np.mean(reaction_times)
        median_time = np.median(reaction_times)
        ax.axvline(mean_time, color='red', linestyle='--', linewidth=2, 
                   label=f'Média: {mean_time:.2f}s')
        ax.axvline(median_time, color='green', linestyle=':', linewidth=2, 
                   label=f'Mediana: {median_time:.2f}s')
        ax.legend()
        
        # Adiciona texto com estatísticas
        stats_text = f'n={len(reaction_times)}\nσ={np.std(reaction_times):.2f}s'
        ax.text(0.98, 0.98, stats_text, transform=ax.transAxes,
                verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Remove subplots vazios se houver
    if n_modes == 1:
        pass  # Layout 1x2, sem subplots extras
    else:
        total_plots = n_modes + 1  # +1 para o boxplot
        if total_plots < 4:
            for i in range(total_plots, 4):
                row = i // 2
                col = i % 2
                fig.delaxes(axes[row, col])
    
    plt.tight_layout()
    return fig

def plot_success_rate_comparison(trials_by_mode):
    """
    Cria gráficos de comparação de taxa de sucesso
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('Análise de Taxa de Sucesso por Modo de Jogo', fontsize=16, fontweight='bold')
    
    modes = []
    success_rates = []
    total_trials = []
    
    for mode, trials in trials_by_mode.items():
        if not trials:
            continue
            
        total = len(trials)
        successes = sum(1 for t in trials if t.get('success', False))
        success_rate = (successes / total * 100) if total > 0 else 0
        
        modes.append(get_mode_name(mode))
        success_rates.append(success_rate)
        total_trials.append(total)
    
    # Gráfico de barras de taxa de sucesso
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
    bars = axes[0].bar(modes, success_rates, color=colors[:len(modes)])
    axes[0].set_title('Taxa de Sucesso por Modo')
    axes[0].set_ylabel('Taxa de Sucesso (%)')
    axes[0].set_ylim(0, 100)
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # Adiciona valores nas barras
    for bar in bars:
        height = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom', fontweight='bold')
    
    axes[0].tick_params(axis='x', rotation=15)
    
    # Gráfico de pizza de distribuição de tentativas
    axes[1].pie(total_trials, labels=modes, colors=colors[:len(modes)], autopct='%1.1f%%', startangle=90)
    axes[1].set_title('Distribuição de Tentativas por Modo')
    
    plt.tight_layout()
    return fig

def plot_score_progression(trials_by_mode):
    """
    Plota a progressão de pontuação ao longo do tempo para modos Infinito e Seta
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('Progressão de Pontuação - Modos Infinito e Seta Colorida', fontsize=16, fontweight='bold')
    
    # Modo Infinito
    infinite_trials = trials_by_mode.get(GAME_MODE_INFINITE, [])
    if infinite_trials:
        scores = [t.get('score', 0) for t in infinite_trials]
        axes[0].plot(range(1, len(scores) + 1), scores, marker='o', linestyle='-', color='#45B7D1')
        axes[0].set_title('Modo Infinito - Progressão de Pontuação')
        axes[0].set_xlabel('Tentativa')
        axes[0].set_ylabel('Pontuação')
        axes[0].grid(True, alpha=0.3)
        
        # Adiciona linha de tendência
        if len(scores) > 1:
            z = np.polyfit(range(len(scores)), scores, 1)
            p = np.poly1d(z)
            axes[0].plot(range(1, len(scores) + 1), p(range(len(scores))), "r--", alpha=0.8, label='Tendência')
            axes[0].legend()
    else:
        axes[0].text(0.5, 0.5, 'Sem dados para Modo Infinito', ha='center', va='center', transform=axes[0].transAxes)
    
    # Modo Seta
    arrow_trials = trials_by_mode.get(GAME_MODE_ARROW, [])
    if arrow_trials:
        scores = [t.get('score', 0) for t in arrow_trials]
        axes[1].plot(range(1, len(scores) + 1), scores, marker='s', linestyle='-', color='#FFA07A')
        axes[1].set_title('Modo Seta Colorida - Progressão de Pontuação')
        axes[1].set_xlabel('Tentativa')
        axes[1].set_ylabel('Pontuação')
        axes[1].grid(True, alpha=0.3)
        
        # Adiciona linha de tendência
        if len(scores) > 1:
            z = np.polyfit(range(len(scores)), scores, 1)
            p = np.poly1d(z)
            axes[1].plot(range(1, len(scores) + 1), p(range(len(scores))), "r--", alpha=0.8, label='Tendência')
            axes[1].legend()
    else:
        axes[1].text(0.5, 0.5, 'Sem dados para Modo Seta Colorida', ha='center', va='center', transform=axes[1].transAxes)
    
    plt.tight_layout()
    return fig

def plot_reaction_time_over_trials(trials_by_mode):
    """
    Plota como o tempo de reação evolui ao longo das tentativas para cada modo
    """
    # Conta quantos modos têm dados
    modes_with_data = []
    for mode, trials in trials_by_mode.items():
        reaction_times = [t.get('reaction_time') for t in trials if t.get('reaction_time') is not None]
        if reaction_times and len(reaction_times) > 0:
            modes_with_data.append((mode, trials, reaction_times))
    
    # Se não houver dados, retorna figura vazia
    if not modes_with_data:
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        ax.text(0.5, 0.5, 'Nenhum dado de evolução temporal disponível', 
                ha='center', va='center', fontsize=14)
        ax.axis('off')
        return fig
    
    # Cria layout baseado na quantidade de modos
    n_modes = len(modes_with_data)
    if n_modes == 1:
        fig, axes = plt.subplots(1, 1, figsize=(12, 6))
        axes = [axes]  # Coloca em lista para consistência
    elif n_modes == 2:
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        axes = axes.flatten()
    elif n_modes == 3:
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        axes = axes.flatten()
    else:
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        axes = axes.flatten()
    
    fig.suptitle('Evolução do Tempo de Reação ao Longo das Tentativas', fontsize=16, fontweight='bold')
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
    
    for idx, (mode, trials, reaction_times) in enumerate(modes_with_data):
        ax = axes[idx]
        
        trial_numbers = list(range(1, len(reaction_times) + 1))
        ax.plot(trial_numbers, reaction_times, 
               marker='o', linestyle='-', color=colors[idx % len(colors)], 
               alpha=0.7, markersize=4)
        ax.set_title(f'{get_mode_name(mode)} ({len(reaction_times)} tentativas)', fontweight='bold')
        ax.set_xlabel('Tentativa')
        ax.set_ylabel('Tempo de Reação (s)')
        ax.grid(True, alpha=0.3)
        
        # Adiciona linha de média
        mean_time = np.mean(reaction_times)
        ax.axhline(mean_time, color='red', linestyle='--', linewidth=1.5, 
                   alpha=0.7, label=f'Média: {mean_time:.2f}s')
        
        # Adiciona média móvel se houver dados suficientes
        if len(reaction_times) >= 5:
            window = min(5, len(reaction_times) // 2)
            moving_avg = pd.Series(reaction_times).rolling(window=window, center=True).mean()
            ax.plot(trial_numbers, moving_avg, 
                   'g--', linewidth=2.5, alpha=0.8, label=f'Média Móvel ({window})')
        
        # Adiciona linha de tendência se houver dados suficientes
        if len(reaction_times) >= 3:
            z = np.polyfit(range(len(reaction_times)), reaction_times, 1)
            p = np.poly1d(z)
            ax.plot(trial_numbers, p(range(len(reaction_times))), 
                   "orange", linestyle=':', linewidth=2, alpha=0.8, label='Tendência')
            
            # Indica se está melhorando ou piorando
            if z[0] < 0:
                trend_text = "↓ Melhorando"
                trend_color = 'green'
            elif z[0] > 0:
                trend_text = "↑ Piorando"
                trend_color = 'red'
            else:
                trend_text = "→ Estável"
                trend_color = 'gray'
            
            ax.text(0.02, 0.98, trend_text, transform=ax.transAxes,
                   verticalalignment='top', horizontalalignment='left',
                   fontsize=10, fontweight='bold', color=trend_color,
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        ax.legend(loc='upper right', fontsize=8)
        
        # Define limites do eixo y para melhor visualização
        y_min = max(0, min(reaction_times) - 0.5)
        y_max = max(reaction_times) + 0.5
        ax.set_ylim(y_min, y_max)
    
    # Remove subplots vazios
    for idx in range(n_modes, len(axes)):
        fig.delaxes(axes[idx])
    
    plt.tight_layout()
    return fig

def generate_comprehensive_report(data):
    """
    Gera um relatório completo com todas as análises
    
    Args:
        data: Dados JSON carregados
        
    Returns:
        dict: Dicionário contendo DataFrames e figuras
    """
    trials_by_mode = extract_trials_by_mode(data)
    
    report = {
        'trials_by_mode': trials_by_mode,
        'reaction_time_stats': analyze_reaction_times(trials_by_mode),
        'success_rate_stats': analyze_success_rates(trials_by_mode),
        'figures': {
            'reaction_times_comparison': plot_reaction_times_comparison(trials_by_mode),
            'success_rate_comparison': plot_success_rate_comparison(trials_by_mode),
            'score_progression': plot_score_progression(trials_by_mode),
            'reaction_time_evolution': plot_reaction_time_over_trials(trials_by_mode)
        }
    }
    
    return report

def display_report_window(report):
    """
    Exibe o relatório em uma janela Tkinter com abas
    """
    import tkinter as tk
    from tkinter import ttk
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    
    window = tk.Toplevel()
    window.title("Relatório de Análise por Modo de Jogo")
    window.geometry("1200x800")
    
    # Cria notebook (abas)
    notebook = ttk.Notebook(window)
    notebook.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Aba 1: Estatísticas de Tempo de Reação
    stats_frame1 = ttk.Frame(notebook)
    notebook.add(stats_frame1, text="Tempo de Reação")
    
    # Adiciona tabela de estatísticas
    text1 = tk.Text(stats_frame1, wrap='none', height=10)
    text1.pack(fill='x', padx=10, pady=10)
    text1.insert('1.0', report['reaction_time_stats'].to_string(index=False))
    text1.config(state='disabled')
    
    # Adiciona gráfico
    canvas1 = FigureCanvasTkAgg(report['figures']['reaction_times_comparison'], stats_frame1)
    canvas1.draw()
    canvas1.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
    
    # Aba 2: Taxa de Sucesso
    stats_frame2 = ttk.Frame(notebook)
    notebook.add(stats_frame2, text="Taxa de Sucesso")
    
    text2 = tk.Text(stats_frame2, wrap='none', height=10)
    text2.pack(fill='x', padx=10, pady=10)
    text2.insert('1.0', report['success_rate_stats'].to_string(index=False))
    text2.config(state='disabled')
    
    canvas2 = FigureCanvasTkAgg(report['figures']['success_rate_comparison'], stats_frame2)
    canvas2.draw()
    canvas2.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
    
    # Aba 3: Progressão de Pontuação
    stats_frame3 = ttk.Frame(notebook)
    notebook.add(stats_frame3, text="Progressão de Pontuação")
    
    canvas3 = FigureCanvasTkAgg(report['figures']['score_progression'], stats_frame3)
    canvas3.draw()
    canvas3.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
    
    # Aba 4: Evolução do Tempo de Reação
    stats_frame4 = ttk.Frame(notebook)
    notebook.add(stats_frame4, text="Evolução Temporal")
    
    canvas4 = FigureCanvasTkAgg(report['figures']['reaction_time_evolution'], stats_frame4)
    canvas4.draw()
    canvas4.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
    
    return window
