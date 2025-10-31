"""
Configurações e constantes do jogo
"""
import pygame

# Inicializa o pygame
pygame.init()

# Variáveis de configuração da tela
WIDTH, HEIGHT = 1400, 1000
BACKGROUND_COLOR = (200, 200, 200)

# Cores do tema do jogo
GAME_BLUE = (30, 60, 120)
GAME_LIGHT_BLUE = (60, 120, 200)
GAME_GOLD = (255, 215, 0)
GAME_SILVER = (192, 192, 192)
GAME_WHITE = (255, 255, 255)
GAME_BLACK = (0, 0, 0)
GAME_GREEN = (0, 180, 0)
GAME_RED = (220, 30, 30)

# Cores das escadas rolantes
ESCALATOR_COLORS = [(100, 100, 100), (120, 120, 120), (140, 140, 140)]
ESCALATOR_SPEEDS = [2, 3, 4]
ESCALATOR_WIDTH = 150
ESCALATOR_SPACING = 100

# Cálculo para centralizar as 3 escadas
TOTAL_ESCALATORS_WIDTH = 3 * ESCALATOR_WIDTH + 2 * ESCALATOR_SPACING
ESCALATOR_START_X = (WIDTH - TOTAL_ESCALATORS_WIDTH) // 2

# Cores dos quadrantes para o modo seta
QUADRANT_COLORS = [
    (255, 100, 100),  # Vermelho claro - Superior esquerdo
    (100, 255, 100),  # Verde claro - Superior direito  
    (100, 100, 255),  # Azul claro - Inferior esquerdo
    (255, 255, 100)   # Amarelo claro - Inferior direito
]

# Propriedades do personagem
CHARACTER_SIZE = 120
CHARACTER_SPAWN_RATE = 60  # Frames entre aparições

# Estados do jogo
GAME_STATE_MENU = 0
GAME_STATE_DISPLAY_TARGET = 1
GAME_STATE_PLAYING = 2
GAME_STATE_SUCCESS = 3
GAME_STATE_FAILURE = 4
GAME_STATE_USER_INPUT = 5
GAME_STATE_NAME_INPUT = 6
GAME_STATE_HIGHSCORE = 7
GAME_STATE_INSTRUCTIONS = 8
GAME_STATE_CONFIRM_PLAYER = 9

# Modos de jogo
GAME_MODE_SINGLE = 0  # Alvo aparece uma vez
GAME_MODE_ALTERNATING = 1  # Alvo alterna a cada acerto
GAME_MODE_INFINITE = 2  # Infinito, ganha tempo ao clicar
GAME_MODE_ARROW = 3  # Modo da seta girando

# Fontes
FONT = pygame.font.SysFont('Arial', 42)
SMALL_FONT = pygame.font.SysFont('Arial', 24)
TINY_FONT = pygame.font.SysFont('Arial', 18)
TITLE_FONT = pygame.font.SysFont('Arial', 56, bold=True)

# Fontes para estilo de jogo
try:
    GAME_TITLE_FONT = pygame.font.SysFont('Trebuchet MS', 72, bold=True)
    GAME_SUBTITLE_FONT = pygame.font.SysFont('Trebuchet MS', 38, bold=True)
    MENU_FONT = pygame.font.SysFont('Trebuchet MS', 24)
    BUTTON_FONT = pygame.font.SysFont('Trebuchet MS', 28, bold=True)
    INSTRUCTIONS_TITLE_FONT = pygame.font.SysFont('Trebuchet MS', 64, bold=True)
    INSTRUCTIONS_TEXT_FONT = pygame.font.SysFont('Trebuchet MS', 28, bold=True)
    HIGHSCORE_TITLE_FONT = pygame.font.SysFont('Trebuchet MS', 64, bold=True)
    HIGHSCORE_TEXT_FONT = pygame.font.SysFont('Trebuchet MS', 36, bold=True)
except:
    GAME_TITLE_FONT = pygame.font.SysFont('Arial', 72, bold=True)
    GAME_SUBTITLE_FONT = pygame.font.SysFont('Arial', 38, bold=True)
    MENU_FONT = pygame.font.SysFont('Arial', 24)
    BUTTON_FONT = pygame.font.SysFont('Arial', 28, bold=True)
    INSTRUCTIONS_TITLE_FONT = pygame.font.SysFont('Arial', 64, bold=True)
    INSTRUCTIONS_TEXT_FONT = pygame.font.SysFont('Arial', 28, bold=True)
    HIGHSCORE_TITLE_FONT = pygame.font.SysFont('Arial', 64, bold=True)
    HIGHSCORE_TEXT_FONT = pygame.font.SysFont('Arial', 36, bold=True)

# Inicializa a tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Escalator - Jogo da Memória na Escada Rolante")
clock = pygame.time.Clock()
