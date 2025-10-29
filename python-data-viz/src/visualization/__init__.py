"""
Módulo de visualização para análise de dados do jogo Memory Escalator.
Fornece funções para gerar mapas de calor e análises detalhadas por modo de jogo.
"""

from .heatmap import generate_heatmap
from .game_mode_analysis import (
    generate_comprehensive_report,
    display_report_window,
    extract_trials_by_mode,
    analyze_reaction_times,
    analyze_success_rates
)

__all__ = [
    'generate_heatmap',
    'generate_comprehensive_report',
    'display_report_window',
    'extract_trials_by_mode',
    'analyze_reaction_times',
    'analyze_success_rates'
]
