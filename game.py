import pygame
import random
import sys
import time
import os
import json
from datetime import datetime

# Inicializa o pygame
pygame.init()

# variáveis de configuração do jogo
WIDTH, HEIGHT = 1000, 700  # Tamanho otimizado para telas menores
BACKGROUND_COLOR = (200, 200, 200)
ESCALATOR_COLORS = [(100, 100, 100), (120, 120, 120), (140, 140, 140)]

# Cores do tema do jogo
GAME_BLUE = (30, 60, 120)
GAME_LIGHT_BLUE = (60, 120, 200)
GAME_GOLD = (255, 215, 0)
GAME_SILVER = (192, 192, 192)
GAME_WHITE = (255, 255, 255)
GAME_BLACK = (0, 0, 0)
GAME_GREEN = (0, 180, 0)
GAME_RED = (220, 30, 30)

# Cores dos quadrantes para o modo seta
QUADRANT_COLORS = [
    (255, 100, 100),  # Vermelho claro - Superior esquerdo
    (100, 255, 100),  # Verde claro - Superior direito  
    (100, 100, 255),  # Azul claro - Inferior esquerdo
    (255, 255, 100)   # Amarelo claro - Inferior direito
]
ESCALATOR_SPEEDS = [2, 3, 4]  # velocidades diferentes para cada escada
ESCALATOR_WIDTH = 150  # Largura maior das escadas
ESCALATOR_SPACING = 100  # Espaçamento entre escadas
# Cálculo para centralizar as 3 escadas na tela
# Total de largura ocupada: 3 * ESCALATOR_WIDTH + 2 * ESCALATOR_SPACING
TOTAL_ESCALATORS_WIDTH = 3 * ESCALATOR_WIDTH + 2 * ESCALATOR_SPACING
ESCALATOR_START_X = (WIDTH - TOTAL_ESCALATORS_WIDTH) // 2  # Centraliza o conjunto

# propriedades do personagem
CHARACTER_SIZE = 120  # Tamanho total do personagem aumentado para melhor visibilidade

# Estados do jogo
GAME_STATE_MENU = 0
GAME_STATE_DISPLAY_TARGET = 1
GAME_STATE_PLAYING = 2
GAME_STATE_SUCCESS = 3
GAME_STATE_FAILURE = 4
GAME_STATE_USER_INPUT = 5  # Novo estado para identificação do usuário
GAME_STATE_NAME_INPUT = 6  # Estado para inserir nome após o jogo
GAME_STATE_HIGHSCORE = 7  # Estado para mostrar highscore
GAME_STATE_INSTRUCTIONS = 8  # Estado para mostrar instruções
GAME_STATE_CONFIRM_PLAYER = 9  # Estado para confirmar se é o mesmo jogador

# Modos de jogo
GAME_MODE_SINGLE = 0  # Alvo aparece uma vez
GAME_MODE_ALTERNATING = 1  # Alvo alterna a cada acerto
GAME_MODE_INFINITE = 2  # Infinito, o jogador ganha tempo ao clicar em personagens
GAME_MODE_ARROW = 3  # Modo da seta girando apontando para quadrantes coloridos

# Taxa de aparição de personagens
CHARACTER_SPAWN_RATE = 60  # Frames entre aparições de personagens

# Fontes - aumentadas para tela maior
FONT = pygame.font.SysFont('Arial', 42)
SMALL_FONT = pygame.font.SysFont('Arial', 24)
TINY_FONT = pygame.font.SysFont('Arial', 18)
TITLE_FONT = pygame.font.SysFont('Arial', 56, bold=True)

# Fontes para estilo de jogo
try:
    # Tenta carregar fontes mais game-like - aumentadas para tela maior
    GAME_TITLE_FONT = pygame.font.SysFont('Trebuchet MS', 72, bold=True)
    GAME_SUBTITLE_FONT = pygame.font.SysFont('Trebuchet MS', 38, bold=True)
    MENU_FONT = pygame.font.SysFont('Trebuchet MS', 24)
    BUTTON_FONT = pygame.font.SysFont('Trebuchet MS', 28, bold=True)
    # Fontes maiores e mais grossas para instruções e highscore
    INSTRUCTIONS_TITLE_FONT = pygame.font.SysFont('Trebuchet MS', 64, bold=True)
    INSTRUCTIONS_TEXT_FONT = pygame.font.SysFont('Trebuchet MS', 28, bold=True)
    HIGHSCORE_TITLE_FONT = pygame.font.SysFont('Trebuchet MS', 64, bold=True)
    HIGHSCORE_TEXT_FONT = pygame.font.SysFont('Trebuchet MS', 36, bold=True)
except:
    # Fallback para fontes padrão se as acima não estiverem disponíveis
    GAME_TITLE_FONT = pygame.font.SysFont('Arial', 72, bold=True)
    GAME_SUBTITLE_FONT = pygame.font.SysFont('Arial', 38, bold=True)
    MENU_FONT = pygame.font.SysFont('Arial', 24)
    BUTTON_FONT = pygame.font.SysFont('Arial', 28, bold=True)
    # Fontes maiores e mais grossas para instruções e highscore
    INSTRUCTIONS_TITLE_FONT = pygame.font.SysFont('Arial', 64, bold=True)
    INSTRUCTIONS_TEXT_FONT = pygame.font.SysFont('Arial', 28, bold=True)
    HIGHSCORE_TITLE_FONT = pygame.font.SysFont('Arial', 64, bold=True)
    HIGHSCORE_TEXT_FONT = pygame.font.SysFont('Arial', 36, bold=True)

# Inicializa a tela
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Memory Escalator - Jogo da Memória na Escada Rolante")
clock = pygame.time.Clock()

# Carrega recursos
def load_assets():
    assets = {
        'bodies': [],
        'faces': [],
        'hats': [],
        'heads': []
    }
    
    # Calcula o tamanho de cada segmento baseado no CHARACTER_SIZE atual
    segment_size = CHARACTER_SIZE // 3  # Cada parte do personagem
    
    # Carrega corpos (3 arquivos possíveis)
    try:
        for i in range(1, 4):
            path = f"assets/bodies/bodie{i}.png"
            if os.path.exists(path):
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (CHARACTER_SIZE, segment_size))  # Escala proporcional
                assets["bodies"].append({"image": img, "name": f"Corpo {i}"})
    except Exception as e:
        print(f"Erro ao carregar corpos: {e}")
        # Cria corpo padrão se não houver arquivos
        for i, color in enumerate([(255, 0, 0), (0, 255, 0), (0, 0, 255)]):
            img = pygame.Surface((CHARACTER_SIZE, segment_size), pygame.SRCALPHA)
            pygame.draw.rect(img, color, (0, 0, CHARACTER_SIZE, segment_size))
            assets["bodies"].append({"image": img, "name": f"Corpo {i+1}"})

    # Carrega rostos (15 arquivos possíveis)
    try:
        for i in range(1, 16):
            path = f"assets/faces/face{i}.png"
            if os.path.exists(path):
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (CHARACTER_SIZE, segment_size))  # Escala proporcional
                assets["faces"].append({"image": img, "name": f"Rosto {i}"})
    except Exception as e:
        print(f"Erro ao carregar rostos: {e}")
        # Cria rosto padrão se não houver arquivos
        for i in range(15):
            img = pygame.Surface((CHARACTER_SIZE, segment_size), pygame.SRCALPHA)
            # Ajusta proporcionalmente os olhos
            eye_radius = segment_size // 8
            eye1_x, eye1_y = CHARACTER_SIZE // 4, segment_size // 2
            eye2_x, eye2_y = 3 * CHARACTER_SIZE // 4, segment_size // 2
            pygame.draw.circle(img, (0, 0, 0), (eye1_x, eye1_y), eye_radius)
            pygame.draw.circle(img, (0, 0, 0), (eye2_x, eye2_y), eye_radius)
            assets["faces"].append({"image": img, "name": f"Rosto {i+1}"})

    # Carrega chapéus (10 arquivos)
    try:
        for i in range(1, 11):
            path = f"assets/hats/hat{i}.png"
            if os.path.exists(path):
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (CHARACTER_SIZE, segment_size))  # Escala proporcional
                assets["hats"].append({"image": img, "name": f"Chapéu {i}"})
    except Exception as e:
        print(f"Erro ao carregar chapéus: {e}")
        # Cria chapéu padrão se não houver arquivos
        for i in range(10):
            img = pygame.Surface((CHARACTER_SIZE, segment_size), pygame.SRCALPHA)
            color = (random.randint(50, 250), random.randint(50, 250), random.randint(50, 250))
            # Ajusta proporcionalmente o desenho do chapéu
            hat_width = CHARACTER_SIZE * 3 // 4
            hat_height = segment_size * 3 // 4
            hat_x = (CHARACTER_SIZE - hat_width) // 2
            hat_y = (segment_size - hat_height) // 2
            pygame.draw.rect(img, color, (hat_x, hat_y, hat_width, hat_height))
            assets["hats"].append({"image": img, "name": f"Chapéu {i+1}"})

    # Carrega cabeças (3 arquivos)
    try:
        for i in range(1, 4):
            path = f"assets/heads/head{i}.png"
            if os.path.exists(path):
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (CHARACTER_SIZE, segment_size))  # Escala proporcional
                assets["heads"].append({"image": img, "name": f"Cabeça {i}"})
    except Exception as e:
        print(f"Erro ao carregar cabeças: {e}")
        # Cria cabeça padrão se não houver arquivos
        for i, color in enumerate([(255, 200, 200), (200, 255, 200), (200, 200, 255)]):
            img = pygame.Surface((CHARACTER_SIZE, segment_size), pygame.SRCALPHA)
            pygame.draw.rect(img, color, (0, 0, CHARACTER_SIZE, segment_size))
            assets["heads"].append({"image": img, "name": f"Cabeça {i+1}"})

    return assets

# Carrega recursos
CHARACTER_ASSETS = load_assets()

class Character:
    def __init__(self, x, y, traits):
        self.x = x
        self.y = y
        self.traits = traits  # Dicionário de características
        self.size = CHARACTER_SIZE
        self.escalator_index = None  # Em qual escada rolante o personagem está
        self.step_position = 0  # Posição no degrau atual (0-1)
        self.current_step = 0  # Em qual degrau o personagem está atualmente
    
    def update(self, speed, escalator):
        # O personagem deve se mover com os degraus da escada rolante
        # Calcula a altura do degrau e quantos degraus cabem na tela
        step_height = 20
        total_steps = HEIGHT // step_height
        
        # Atualiza a posição do degrau com base na velocidade da escada
        # Isso cria um efeito de movimento sincronizado
        self.step_position += speed / step_height
        
        # Se passamos de um degrau, vamos para o próximo
        if self.step_position >= 1:
            self.current_step += 1
            self.step_position -= 1
        
        # Calcula a posição y com base no degrau atual e na posição dentro do degrau
        self.y = (self.current_step * step_height) + (self.step_position * step_height)
        # Garante que o personagem fique centralizado na escada rolante
        self.x = escalator.x + (escalator.width - self.size) // 2
    
    def draw(self, screen):
        # Calcula as posições baseado no tamanho atual do personagem
        segment_height = self.size // 3  # Divide em 3 partes iguais
        
        # Desenha o corpo na parte inferior
        screen.blit(self.traits["body"]["image"], 
                    (self.x, self.y + segment_height * 2))  # Parte inferior
        
        # Desenha a cabeça no meio
        screen.blit(self.traits["head"]["image"], 
                    (self.x, self.y + segment_height))  # Parte do meio
        
        # Desenha o rosto sobre a cabeça (mesma posição da cabeça pois é uma sobreposição)
        screen.blit(self.traits["face"]["image"], 
                    (self.x, self.y + segment_height))  # Sobrepõe na cabeça
        
        # Desenha o chapéu no topo
        screen.blit(self.traits["hat"]["image"], 
                    (self.x, self.y))  # Parte do topo
    
    def is_clicked(self, mouse_pos):
        # Verifica se este personagem foi clicado
        mx, my = mouse_pos
        return (self.x <= mx <= self.x + self.size and 
                self.y <= my <= self.y + self.size)
    
    def is_same_as(self, other):
        # Verifica se este personagem tem as mesmas características que outro
        return (self.traits["body"]["name"] == other.traits["body"]["name"] and
                self.traits["face"]["name"] == other.traits["face"]["name"] and
                self.traits["head"]["name"] == other.traits["head"]["name"] and
                self.traits["hat"]["name"] == other.traits["hat"]["name"])
    
    def __str__(self):
        # Retorna uma representação em string do personagem
        return f"{self.traits['head']['name']} com {self.traits['face']['name']}, " \
               f"{self.traits['body']['name']} e {self.traits['hat']['name']}"

class CharacterFactory:
    def __init__(self, assets):
        self.assets = assets
        self.created_characters = []
        self.all_possible_combinations = self._generate_all_possible_combinations()
        self.available_combinations = self.all_possible_combinations.copy()
    
    def _generate_all_possible_combinations(self):
        # Gera todas as combinações possíveis de características
        all_combinations = []
        for head in self.assets["heads"]:
            for face in self.assets["faces"]:
                for body in self.assets["bodies"]:
                    for hat in self.assets["hats"]:
                        traits = {
                            "head": head,
                            "face": face,
                            "body": body,
                            "hat": hat
                        }
                        all_combinations.append(traits)
        return all_combinations
    
    def reset(self):
        # Reinicia as combinações disponíveis
        self.available_combinations = self.all_possible_combinations.copy()
        self.created_characters = []
    
    def create_random_character(self, x, y):
        # Cria um personagem aleatório com características únicas
        if not self.available_combinations:
            print("Aviso: Não há mais combinações únicas disponíveis!")
            # Se usamos todas as combinações, regeneramos a lista
            self.available_combinations = self.all_possible_combinations.copy()
        
        # Obtém uma combinação aleatória de características
        traits = random.choice(self.available_combinations)
        self.available_combinations.remove(traits)
        
        # Cria e retorna um novo personagem
        character = Character(x, y, traits)
        self.created_characters.append(character)
        return character
    
    def get_random_existing_traits(self):
        # Obtém características de um personagem que já criamos
        if not self.created_characters:
            return None
        
        character = random.choice(self.created_characters)
        return character.traits.copy()

class Button:
    def __init__(self, x, y, width, height, text, color=None, hover_color=None):
        if color is None:
            color = (50, 100, 180)  # Azul amigável
        if hover_color is None:
            hover_color = (70, 130, 200)  # Azul mais claro para hover
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = BUTTON_FONT
    
    def draw(self, screen):
        # Cores simples e amigáveis
        if self.is_hovered:
            button_color = (70, 130, 200)  # Azul mais claro no hover
            border_color = (255, 255, 255)
            text_color = (255, 255, 255)
        else:
            button_color = (50, 100, 180)  # Azul padrão
            border_color = (200, 200, 200)
            text_color = (255, 255, 255)
        
        # Fundo do botão simples
        pygame.draw.rect(screen, button_color, self.rect)
        pygame.draw.rect(screen, button_color, self.rect, border_radius=8)
        
        # Borda simples
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=8)
        
        # Efeito sutil de luz no topo para dar volume
        if self.rect.height > 10:
            light_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.rect.width - 4, 2)
            pygame.draw.rect(screen, (255, 255, 255, 60), light_rect, border_radius=6)
        
        # Texto com sombra sutil
        # Sombra
        text_shadow = self.font.render(self.text, True, (0, 0, 0, 120))
        shadow_rect = text_shadow.get_rect(center=(self.rect.centerx + 1, self.rect.centery + 1))
        screen.blit(text_shadow, shadow_rect)
        
        # Texto principal
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class Escalator:
    def __init__(self, x, width, speed, color):
        self.x = x
        self.width = width
        self.speed = speed
        self.color = color
        self.characters = []
        self.step_offset = 0  # Para animar os degraus da escada rolante
    
    def add_character(self, character):
        # Adiciona um personagem a esta escada rolante
        character.escalator_index = ESCALATOR_SPEEDS.index(self.speed)
        character.current_step = -3  # Começa acima da tela
        character.step_position = 0
        self.characters.append(character)
    
    def update(self):
        # Atualiza a animação dos degraus
        self.step_offset = (self.step_offset + self.speed) % 20  # 20 é a altura do degrau
        
        # Atualiza todos os personagens nesta escada rolante
        for character in self.characters[:]:
            character.update(self.speed, self)
            # Remove personagens que saíram da tela
            if character.y > HEIGHT:
                self.characters.remove(character)
    
    def draw(self, screen):
        # Desenha a escada rolante
        pygame.draw.rect(screen, self.color, (self.x, 0, self.width, HEIGHT))
        
        # Desenha segmentos de linha para representar os degraus da escada rolante
        step_height = 20
        for y in range(0, HEIGHT + step_height, step_height):
            # Ajusta a posição y baseada no step_offset para animação
            adjusted_y = (y + self.step_offset) % (HEIGHT + step_height)
            pygame.draw.line(screen, (50, 50, 50), 
                           (self.x, adjusted_y), 
                           (self.x + self.width, adjusted_y), 2)
        
        # Desenha todos os personagens nesta escada rolante
        for character in self.characters:
            character.draw(screen)
    
    def check_character_click(self, mouse_pos):
        # Verifica se algum personagem nesta escada rolante foi clicado
        for character in self.characters:
            if character.is_clicked(mouse_pos):
                return character
        return None

class TextInput:
    def __init__(self, x, y, width, height, font=None, placeholder="Digite seu nome"):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.active = True
        self.placeholder = placeholder
        self.font = font or SMALL_FONT
        self.color_inactive = pygame.Color('gray')
        self.color_active = pygame.Color('black')
        self.color = self.color_active if self.active else self.color_inactive
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_blink_rate = 0.5  # segundos
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text  # Envia texto ao pressionar Enter
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    # Adiciona apenas caracteres imprimíveis
                    if event.unicode.isprintable():
                        self.text += event.unicode
        return None
    
    def update(self):
        # Pisca o cursor
        self.cursor_timer += 1/60  # Assumindo 60 FPS
        if self.cursor_timer >= self.cursor_blink_rate:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    
    def draw(self, screen):
        # Fundo do campo de texto com bordas arredondadas
        pygame.draw.rect(screen, (255, 255, 255), self.rect, border_radius=8)
        
        # Borda colorida
        border_color = (70, 130, 200) if self.active else (150, 150, 150)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=8)
        
        # Renderiza o texto ou o placeholder
        if self.text:
            text_surf = self.font.render(self.text, True, (50, 50, 50))
        else:
            text_surf = self.font.render(self.placeholder, True, (150, 150, 150))
        
        # Desenha a superfície do texto
        text_rect = text_surf.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        screen.blit(text_surf, text_rect)
        
        # Desenha o cursor
        if self.active and self.cursor_visible and len(self.text) < 30:  # Limita o tamanho do texto
            cursor_x = text_rect.right + 2 if self.text else self.rect.x + 5
            pygame.draw.line(screen, self.color, 
                           (cursor_x, self.rect.y + 5), 
                           (cursor_x, self.rect.bottom - 5), 2)

class GameDataCollector:
    def __init__(self):
        self.all_sessions = self.load_existing_data()
        self.current_session = {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "username": "Anônimo",
            "game_mode": None,
            "trials": [],
            "mouse_tracking": [],
            "session_metrics": {
                "total_clicks": 0,
                "correct_clicks": 0,
                "incorrect_clicks": 0,
                "missed_targets": 0,
                "false_positives": 0,  # Cliques em personagens errados
                "session_duration": 0,
                "focus_breaks": 0  # Períodos longos sem interação
            }
        }
        self.current_trial = None
        self.target_spawn_time = None
        self.last_interaction_time = time.time()
        self.clicks_positions = []  # Armazena posições de todos os cliques
    
    def load_existing_data(self):
        # Verifica se já existe um arquivo de dados
        date_str = datetime.now().strftime("%Y-%m-%d")
        date_str_no_dash = datetime.now().strftime("%Y%m%d")
        time_str = datetime.now().strftime("%H%M%S")
        base_dir = "playerdata"
        date_dir = os.path.join(base_dir, date_str)
        
        # Cria os diretórios se não existirem
        os.makedirs(date_dir, exist_ok=True)
        
        # Cria nome de arquivo consistente para os dados de hoje com timestamp
        filename = os.path.join(date_dir, f"game_data_{date_str_no_dash}_{time_str}.json")
        
        # Também verifica arquivos em formato antigo que possam existir
        old_filename1 = os.path.join(date_dir, f"game_data_{date_str_no_dash}.json")
        old_filename2 = os.path.join(date_dir, f"game_data_{date_str}.json")
        
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                print(f"Erro ao carregar arquivo de dados existente, criando novo")
                return {"sessions": []}
        elif os.path.exists(old_filename1):
            try:
                with open(old_filename1, 'r') as f:
                    data = json.load(f)
                    # Salva no novo formato para consistência
                    with open(filename, 'w') as new_f:
                        json.dump(data, new_f, indent=2)
                    return data
            except (json.JSONDecodeError, FileNotFoundError):
                print(f"Erro ao carregar arquivo de dados existente, criando novo")
                return {"sessions": []}
        elif os.path.exists(old_filename2):
            try:
                with open(old_filename2, 'r') as f:
                    data = json.load(f)
                    # Salva no novo formato para consistência
                    with open(filename, 'w') as new_f:
                        json.dump(data, new_f, indent=2)
                    return data
            except (json.JSONDecodeError, FileNotFoundError):
                print(f"Erro ao carregar arquivo de dados existente, criando novo")
                return {"sessions": []}
        else:
            return {"sessions": []}
    
    def set_username(self, username):
        self.current_session["username"] = username if username else "Anônimo"
    
    def start_new_trial(self, game_mode):
        # Em vez de sobrescrever o modo de jogo da sessão, armazena em cada tentativa
        self.current_trial = {
            "trial_start_time": time.time(),
            "game_mode": game_mode,
            "target_character": None,
            "target_spawn_time": None,
            "selection_time": None,
            "success": False,
            "reaction_time": None,
            "score": 0,
            "trial_metrics": {
                "mouse_movements": 0,  # Quantidade de movimentos do mouse
                "hesitation_time": 0,  # Tempo de hesitação antes do clique
                "clicks_before_success": 0,  # Número de cliques antes de acertar
                "average_mouse_speed": 0,  # Velocidade média do mouse
                "mouse_path_length": 0  # Comprimento do caminho do mouse
            }
        }
        
        # Para o modo seta, já define o target_spawn_time como agora
        # pois o alvo (quadrante colorido) está sempre visível
        if game_mode == 3:  # GAME_MODE_ARROW
            self.current_trial["target_spawn_time"] = time.time()
        
        # Reset variáveis de rastreamento da trial
        self.clicks_positions = []
        self.mouse_movement_count = 0
        self.last_mouse_pos = None
        self.total_mouse_distance = 0
    
    def update_trial_score(self, score):
        if self.current_trial:
            self.current_trial["score"] = score
    
    def record_target_spawn(self, character_traits):
        if self.current_trial:
            # Cria uma versão serializável dos traços sem pygame Surfaces
            serializable_traits = {
                'head': {'name': character_traits['head']['name']},
                'face': {'name': character_traits['face']['name']},
                'body': {'name': character_traits['body']['name']},
                'hat': {'name': character_traits['hat']['name']}
            }
            self.current_trial["target_character"] = serializable_traits
            self.current_trial["target_spawn_time"] = time.time()
            self.target_spawn_time = time.time()

    def record_mouse_position(self, mouse_pos, game_state):
        current_time = time.time()
        
        # Registra posição do mouse
        self.current_session["mouse_tracking"].append({
            "timestamp": current_time,
            "x": mouse_pos[0],
            "y": mouse_pos[1],
            "game_state": game_state
        })
        
        # Calcula métricas de movimento do mouse durante a tentativa
        if self.current_trial and self.last_mouse_pos:
            # Calcula distância percorrida
            dx = mouse_pos[0] - self.last_mouse_pos[0]
            dy = mouse_pos[1] - self.last_mouse_pos[1]
            distance = (dx**2 + dy**2)**0.5
            
            # Considera movimento apenas se for significativo (> 5 pixels)
            if distance > 5:
                self.mouse_movement_count += 1
                self.total_mouse_distance += distance
        
        # Detecta quebra de foco (mais de 3 segundos sem interação)
        # Garante que session_metrics existe (compatibilidade com dados antigos)
        if "session_metrics" not in self.current_session:
            self.current_session["session_metrics"] = {
                "total_clicks": 0,
                "correct_clicks": 0,
                "incorrect_clicks": 0,
                "missed_targets": 0,
                "false_positives": 0,
                "session_duration": 0,
                "focus_breaks": 0
            }
        
        if current_time - self.last_interaction_time > 3.0:
            self.current_session["session_metrics"]["focus_breaks"] += 1
        
        self.last_interaction_time = current_time
        self.last_mouse_pos = mouse_pos
    
    def record_click(self, position, success):
        """Registra um clique para análise de precisão"""
        self.clicks_positions.append({
            "x": position[0],
            "y": position[1],
            "timestamp": time.time(),
            "success": success
        })
        
        # Garante que session_metrics existe (compatibilidade com dados antigos)
        if "session_metrics" not in self.current_session:
            self.current_session["session_metrics"] = {
                "total_clicks": 0,
                "correct_clicks": 0,
                "incorrect_clicks": 0,
                "missed_targets": 0,
                "false_positives": 0,
                "session_duration": 0,
                "focus_breaks": 0
            }
        
        # Atualiza métricas da sessão
        self.current_session["session_metrics"]["total_clicks"] += 1
        if success:
            self.current_session["session_metrics"]["correct_clicks"] += 1
        else:
            self.current_session["session_metrics"]["incorrect_clicks"] += 1
            self.current_session["session_metrics"]["false_positives"] += 1
        
        # Atualiza métricas da tentativa
        if self.current_trial:
            self.current_trial["trial_metrics"]["clicks_before_success"] += 1
    
    def record_selection(self, success):
        if self.current_trial and self.target_spawn_time:
            selection_time = time.time()
            self.current_trial["selection_time"] = selection_time
            self.current_trial["success"] = success
            self.current_trial["reaction_time"] = selection_time - self.target_spawn_time
            
            # Calcula métricas adicionais
            trial_duration = selection_time - self.current_trial["trial_start_time"]
            self.current_trial["trial_metrics"]["mouse_movements"] = self.mouse_movement_count
            
            if self.total_mouse_distance > 0 and trial_duration > 0:
                self.current_trial["trial_metrics"]["average_mouse_speed"] = self.total_mouse_distance / trial_duration
                self.current_trial["trial_metrics"]["mouse_path_length"] = self.total_mouse_distance
            
            # Calcula tempo de hesitação (diferença entre ver o alvo e clicar)
            if self.current_trial["target_spawn_time"]:
                hesitation = selection_time - self.current_trial["target_spawn_time"]
                self.current_trial["trial_metrics"]["hesitation_time"] = hesitation
            
            # Adiciona posições dos cliques
            self.current_trial["clicks"] = self.clicks_positions.copy()
            
            self.current_session["trials"].append(self.current_trial)
            self.current_trial = None
            
            # Reset variáveis
            self.clicks_positions = []
            self.mouse_movement_count = 0
            self.total_mouse_distance = 0
    
    def record_arrow_selection(self, success, clicked_quadrant, target_quadrant, arrow_angle, arrow_speed, arrow_in_zone):
        """Registra uma seleção específica do modo seta com métricas detalhadas"""
        if self.current_trial:
            selection_time = time.time()
            self.current_trial["selection_time"] = selection_time
            self.current_trial["success"] = success
            self.current_trial["reaction_time"] = selection_time - self.current_trial["trial_start_time"]
            
            # Métricas específicas do modo seta
            self.current_trial["arrow_metrics"] = {
                "clicked_quadrant": clicked_quadrant,
                "target_quadrant": target_quadrant,
                "arrow_angle_at_click": arrow_angle,
                "arrow_rotation_speed": arrow_speed,
                "arrow_in_target_zone": arrow_in_zone,
                "timing_accuracy": "perfect" if arrow_in_zone else "missed_timing",
                "quadrant_accuracy": "correct" if clicked_quadrant == target_quadrant else "wrong_quadrant"
            }
            
            # Calcula métricas adicionais
            trial_duration = selection_time - self.current_trial["trial_start_time"]
            self.current_trial["trial_metrics"]["mouse_movements"] = self.mouse_movement_count
            
            if self.total_mouse_distance > 0 and trial_duration > 0:
                self.current_trial["trial_metrics"]["average_mouse_speed"] = self.total_mouse_distance / trial_duration
                self.current_trial["trial_metrics"]["mouse_path_length"] = self.total_mouse_distance
            
            # Adiciona posições dos cliques
            self.current_trial["clicks"] = self.clicks_positions.copy()
            
            self.current_session["trials"].append(self.current_trial)
            self.current_trial = None
            
            # Reset variáveis
            self.clicks_positions = []
            self.mouse_movement_count = 0
            self.total_mouse_distance = 0
    
    def create_new_session(self, game_mode=None):
        # Adiciona a sessão atual a all_sessions antes de criar uma nova
        if len(self.current_session["trials"]) > 0:
            # Cria uma cópia serializável da sessão
            serializable_session = self.prepare_session_for_saving(self.current_session)
            # Adiciona à nossa coleção de todas as sessões
            self.all_sessions["sessions"].append(serializable_session)
        
        # Cria uma nova sessão com um timestamp único (inclui milissegundos para unicidade)
        self.current_session = {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S_%f"),
            "username": self.current_session["username"],  # Mantém o mesmo nome de usuário
            "game_mode": game_mode,  # Armazena o modo de jogo na sessão
            "trials": [],
            "mouse_tracking": [],
            "session_metrics": {
                "total_clicks": 0,
                "correct_clicks": 0,
                "incorrect_clicks": 0,
                "missed_targets": 0,
                "false_positives": 0,
                "session_duration": 0,
                "focus_breaks": 0
            }
        }
    
    def prepare_session_for_saving(self, session):
        # Garante que session_metrics existe (compatibilidade com dados antigos)
        if "session_metrics" not in session:
            session["session_metrics"] = {
                "total_clicks": 0,
                "correct_clicks": 0,
                "incorrect_clicks": 0,
                "missed_targets": 0,
                "false_positives": 0,
                "session_duration": 0,
                "focus_breaks": 0
            }
        
        # Calcula duração total da sessão
        if session["trials"]:
            first_trial_time = session["trials"][0]["trial_start_time"]
            last_trial_time = session["trials"][-1].get("selection_time", session["trials"][-1]["trial_start_time"])
            session["session_metrics"]["session_duration"] = last_trial_time - first_trial_time
        
        # Cria uma cópia serializável dos dados da sessão
        serializable_session = {
            "session_id": session["session_id"],
            "username": session["username"],
            "game_mode": session["game_mode"],
            "trials": [],
            "mouse_tracking": session["mouse_tracking"],
            "session_metrics": session["session_metrics"]
        }
        
        # Converte os dados das tentativas para formato serializável
        for trial in session["trials"]:
            serializable_trial = {
                "trial_start_time": trial["trial_start_time"],
                "game_mode": trial["game_mode"],
                "target_spawn_time": trial["target_spawn_time"],
                "selection_time": trial["selection_time"],
                "success": trial["success"],
                "reaction_time": trial["reaction_time"],
                "score": trial.get("score", 0),
                "trial_metrics": trial.get("trial_metrics", {}),
                "clicks": trial.get("clicks", [])
            }
            
            # Inclui target_character apenas se existir
            if trial.get("target_character"):
                serializable_trial["target_character"] = {
                    'head': {'name': trial["target_character"]["head"]["name"]},
                    'face': {'name': trial["target_character"]["face"]["name"]},
                    'body': {'name': trial["target_character"]["body"]["name"]},
                    'hat': {'name': trial["target_character"]["hat"]["name"]}
                }
            
            # Inclui métricas da seta se existir
            if trial.get("arrow_metrics"):
                serializable_trial["arrow_metrics"] = trial["arrow_metrics"]
                
            serializable_session["trials"].append(serializable_trial)
            
        return serializable_session
    
    def save_session_data(self):
        # Adiciona a sessão atual a all_sessions se tiver tentativas
        if self.current_session and len(self.current_session["trials"]) > 0:
            serializable_session = self.prepare_session_for_saving(self.current_session)
            self.all_sessions["sessions"].append(serializable_session)
        
        # Cria estrutura de diretórios
        date_str = datetime.now().strftime("%Y-%m-%d")
        date_str_no_dash = datetime.now().strftime("%Y%m%d")
        time_str = datetime.now().strftime("%H%M%S")
        base_dir = "playerdata"
        date_dir = os.path.join(base_dir, date_str)
        
        # Cria diretórios se não existirem
        os.makedirs(date_dir, exist_ok=True)
        
        # Cria nome de arquivo com a data de hoje e hora atual
        filename = os.path.join(date_dir, f"game_data_{date_str_no_dash}_{time_str}.json")
        
        # Salva os dados serializáveis no arquivo
        with open(filename, 'w') as f:
            json.dump(self.all_sessions, f, indent=2)

class Game:
    def __init__(self):
        self.escalators = []
        self.spawn_counter = 0
        self.running = True
        self.game_state = GAME_STATE_MENU  # Começa no menu principal
        self.game_mode = GAME_MODE_SINGLE
        self.target_character = None
        self.target_traits = None
        self.display_target_time = 4  # segundos para exibir o alvo
        self.is_first_target = True  # Para controlar se é o primeiro alvo ou não
        self.target_display_start = 0
        self.score = 0
        self.highest_score = 0
        self.time_limit = 30  # 30 segundos para encontrar o personagem
        self.start_time = 0
        self.target_spawn_count = 0  # Quantas vezes o alvo apareceu
        self.target_max_spawns = 3  # Máximo de vezes que o alvo pode aparecer no modo múltiplo
        self.has_target_spawned = False
        self.target_spawned_time = 0
        self.character_factory = CharacterFactory(CHARACTER_ASSETS)
        self.time_bonus = 5  # Tempo adicionado para cliques corretos no modo infinito
        self.data_collector = GameDataCollector()
        # Para rastrear precisão no modo infinito
        self.selections_total = 0
        self.selections_correct = 0
        
        # Variáveis específicas do modo seta
        self.arrow_angle = 0  # Ângulo atual da seta
        self.arrow_rotation_speed = 4.0  # Velocidade de rotação da seta (varia de 2 a 8)
        self.target_quadrant = 0  # Quadrante alvo (0-3)
        self.arrow_color = (255, 255, 255)  # Cor da seta (será definida pelo quadrante alvo)
        self.arrow_in_target_zone = False  # Se a seta está no quadrante certo
        self.last_quadrant_pointed = -1  # Último quadrante que a seta apontou
        
        # Sistema de highscore
        self.highscores = self.load_highscores()
        self.last_score = 0
        self.is_new_highscore = False
        self.player_name = ""
        
        # Cria entrada de texto para nome do usuário - maior para tela maior
        self.text_input = TextInput(
            WIDTH//2 - 200, HEIGHT//2,
            400, 50, 
            placeholder="Digite seu nome"
        )
        
        # Cria botão de confirmação para nome do usuário
        self.confirm_button = Button(
            WIDTH//2 - 100, HEIGHT//2 + 60,
            200, 50,
            "Confirmar"
        )
        
        # Entrada de texto para highscore
        self.highscore_input = TextInput(
            WIDTH//2 - 200, HEIGHT//2 + 50,
            400, 50,
            placeholder="Digite seu nome para o ranking"
        )
        
        # Botão de confirmação para highscore
        self.highscore_confirm_button = Button(
            WIDTH//2 - 100, HEIGHT//2 + 120,
            200, 50,
            "Salvar"
        )
        
        # Botões para confirmação de jogador
        self.yes_button = Button(
            WIDTH//2 - 210, HEIGHT//2 + 60,
            160, 50,
            "Sim"
        )
        
        self.no_button = Button(
            WIDTH//2 + 50, HEIGHT//2 + 60,
            160, 50,
            "Não"
        )
        
        # Cria botões para o menu - tamanhos maiores para tela maior
        button_width, button_height = 280, 60
        button_x = WIDTH // 2 - button_width // 2
        
        self.single_mode_button = Button(
            button_x, HEIGHT // 2 - 70, 
            button_width, button_height, 
            "Modo Aparição Única"
        )
        
        self.alternating_mode_button = Button(
            button_x, HEIGHT // 2, 
            button_width, button_height, 
            "Modo Alternado"
        )
        
        self.infinite_mode_button = Button(
            button_x, HEIGHT // 2 + 70, 
            button_width, button_height, 
            "Modo Infinito"
        )
        
        self.arrow_mode_button = Button(
            button_x, HEIGHT // 2 + 140, 
            button_width, button_height, 
            "Modo Seta Colorida"
        )
        
        # Botões adicionais do menu
        self.instructions_button = Button(
            button_x, HEIGHT // 2 + 210,
            button_width, button_height,
            "Como Jogar"
        )
        
        self.highscore_button = Button(
            button_x, HEIGHT // 2 + 280,
            button_width, button_height,
            "Melhores Pontuações"
        )
        
        self.back_button = Button(
            50, HEIGHT - 100,
            160, 50,
            "Voltar"
        )
        
        # Cria as três escadas rolantes
        for i in range(3):
            x = ESCALATOR_START_X + i * (ESCALATOR_WIDTH + ESCALATOR_SPACING)
            escalator = Escalator(x, ESCALATOR_WIDTH, ESCALATOR_SPEEDS[i], ESCALATOR_COLORS[i])
            self.escalators.append(escalator)
        
        # Remove dependência de imagem - usaremos design programático
        # self.menu_image = self.load_menu_image()
    
    def load_highscores(self):
        """Carrega os highscores do arquivo"""
        try:
            highscore_path = os.path.join("playerdata", "highscore", "highscores.json")
            if os.path.exists(highscore_path):
                with open(highscore_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {"single": [], "alternating": [], "infinite": [], "arrow": []}
        except:
            return {"single": [], "alternating": [], "infinite": [], "arrow": []}
    
    def add_highscore(self, name, score, mode):
        """Adiciona uma nova pontuação ao ranking - APENAS para modos INFINITE e ARROW"""
        # Só salva no highscore se for modo INFINITE ou ARROW
        if mode != GAME_MODE_INFINITE and mode != GAME_MODE_ARROW:
            return
            
        mode_names = {
            GAME_MODE_SINGLE: "single",
            GAME_MODE_ALTERNATING: "alternating", 
            GAME_MODE_INFINITE: "infinite",
            GAME_MODE_ARROW: "arrow"
        }
        
        mode_key = mode_names.get(mode, "infinite")
        
        # Garante que a chave existe no dicionário de highscores
        if mode_key not in self.highscores:
            self.highscores[mode_key] = []
        
        # Adiciona nova pontuação - corrige bug de nomes com espaços
        clean_name = name.strip() if name and name.strip() else "Anônimo"
        new_score = {
            "name": clean_name,
            "score": score,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        
        self.highscores[mode_key].append(new_score)
        
        # Ordena por pontuação (maior primeiro) e mantém apenas top 10
        self.highscores[mode_key].sort(key=lambda x: x["score"], reverse=True)
        self.highscores[mode_key] = self.highscores[mode_key][:10]
        
        self.save_highscores()
    
    def is_highscore(self, score, mode):
        """Verifica se a pontuação é um highscore - APENAS para modos INFINITE e ARROW"""
        # Só considera highscore se for modo INFINITE ou ARROW
        if mode != GAME_MODE_INFINITE and mode != GAME_MODE_ARROW:
            return False
            
        mode_names = {
            GAME_MODE_SINGLE: "single",
            GAME_MODE_ALTERNATING: "alternating",
            GAME_MODE_INFINITE: "infinite",
            GAME_MODE_ARROW: "arrow"
        }
        
        mode_key = mode_names.get(mode, "infinite")
        scores = self.highscores[mode_key]
        
        # Se tem menos de 10 pontuações, sempre é highscore
        if len(scores) < 10:
            return True
        
        # Se a pontuação é maior que a menor do top 10
        return score > scores[-1]["score"]
    
    def save_highscores(self):
        """Salva os highscores no arquivo"""
        try:
            # Cria o diretório se não existir
            highscore_dir = os.path.join("playerdata", "highscore")
            os.makedirs(highscore_dir, exist_ok=True)
            
            # Salva na pasta correta
            highscore_path = os.path.join(highscore_dir, "highscores.json")
            with open(highscore_path, 'w', encoding='utf-8') as f:
                json.dump(self.highscores, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar highscores: {e}")
    


    def select_new_target(self):
        # Cria um personagem alvo (ainda não colocado em nenhuma escada rolante)
        self.target_character = self.character_factory.create_random_character(
            WIDTH//2 - CHARACTER_SIZE//2, 
            HEIGHT//2 - CHARACTER_SIZE//2
        )
        self.target_traits = self.target_character.traits
        self.target_display_start = time.time()
        self.has_target_spawned = False
        self.target_spawn_count = 0
    
    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        self.data_collector.record_mouse_position(mouse_pos, self.game_state)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                global screen, WIDTH, HEIGHT
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == GAME_STATE_MENU:
                        self.running = False
                    else:
                        self.game_state = GAME_STATE_MENU
                elif event.key == pygame.K_r and (self.game_state == GAME_STATE_SUCCESS or 
                                                self.game_state == GAME_STATE_FAILURE):
                    # Reinicia o jogo
                    self.reset_game()
                    self.game_state = GAME_STATE_DISPLAY_TARGET  # Garante que volte a exibir o alvo
                

                
                # Manipula entrada de texto para highscore
                if self.game_state == GAME_STATE_NAME_INPUT:
                    result = self.highscore_input.handle_event(event)
                    if result is not None:  # Enter foi pressionado
                        self.add_highscore(result, self.last_score, self.game_mode)
                        self.game_state = GAME_STATE_MENU
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == GAME_STATE_MENU:
                    # Verifica se algum botão de modo de jogo foi clicado
                    if self.single_mode_button.is_clicked(mouse_pos):
                        self.game_mode = GAME_MODE_SINGLE
                        self.reset_game()
                        if self.game_state != GAME_STATE_CONFIRM_PLAYER:
                            self.game_state = GAME_STATE_DISPLAY_TARGET
                    elif self.alternating_mode_button.is_clicked(mouse_pos):
                        self.game_mode = GAME_MODE_ALTERNATING
                        self.reset_game()
                        if self.game_state != GAME_STATE_CONFIRM_PLAYER:
                            self.game_state = GAME_STATE_DISPLAY_TARGET
                    elif self.infinite_mode_button.is_clicked(mouse_pos):
                        self.game_mode = GAME_MODE_INFINITE
                        self.reset_game()
                        if self.game_state != GAME_STATE_CONFIRM_PLAYER:
                            self.game_state = GAME_STATE_DISPLAY_TARGET
                    elif self.arrow_mode_button.is_clicked(mouse_pos):
                        self.game_mode = GAME_MODE_ARROW
                        self.reset_game()
                        if self.game_state != GAME_STATE_CONFIRM_PLAYER:
                            self.game_state = GAME_STATE_PLAYING  # Modo seta começa direto jogando
                    elif self.instructions_button.is_clicked(mouse_pos):
                        self.game_state = GAME_STATE_INSTRUCTIONS
                    elif self.highscore_button.is_clicked(mouse_pos):
                        self.game_state = GAME_STATE_HIGHSCORE
                
                elif self.game_state == GAME_STATE_PLAYING:
                    # Verifica todas as escadas rolantes por personagens clicados
                    for escalator in self.escalators:
                        clicked_character = escalator.check_character_click(mouse_pos)
                        if clicked_character:
                            if clicked_character.traits == self.target_traits:
                                # Personagem correto clicado
                                self.score += 1
                                self.selections_total += 1
                                self.selections_correct += 1
                                self.data_collector.record_click(mouse_pos, True)
                                self.data_collector.update_trial_score(self.score)
                                self.data_collector.record_selection(True)
                                if self.game_mode == GAME_MODE_SINGLE:
                                    # No modo único, encontrar o personagem uma vez termina o jogo com sucesso
                                    self.last_score = self.score
                                    self.game_state = GAME_STATE_NAME_INPUT
                                else:
                                    # Remove o personagem da escada rolante
                                    escalator.characters.remove(clicked_character)
                                    if self.game_mode == GAME_MODE_ALTERNATING:
                                        # No modo alternado, seleciona um novo alvo após cada acerto
                                        # Cria novo alvo com características diferentes
                                        self.select_new_target()
                                        self.has_target_spawned = False
                                        self.is_first_target = False  # Não é mais o primeiro alvo
                                        # Volta para o estado DISPLAY_TARGET para mostrar o novo personagem
                                        self.game_state = GAME_STATE_DISPLAY_TARGET
                                        # Inicia nova tentativa para o próximo alvo
                                        self.data_collector.start_new_trial(self.game_mode)
                                    elif self.game_mode == GAME_MODE_INFINITE:
                                        # Adiciona bônus de tempo para modo infinito
                                        self.time_limit += self.time_bonus
                                        # Faz aparecer um novo alvo imediatamente para manter o jogo fluindo
                                        self.has_target_spawned = False
                                        # Inicia uma nova tentativa para o próximo alvo
                                        self.data_collector.start_new_trial(self.game_mode)
                            else:
                                # Personagem errado clicado
                                self.selections_total += 1
                                self.data_collector.record_click(mouse_pos, False)
                                self.data_collector.update_trial_score(self.score)  # Registra pontuação final antes de terminar tentativa
                                self.data_collector.record_selection(False)
                                if self.game_mode == GAME_MODE_INFINITE:
                                    # No modo infinito, aplica penalidade de tempo mas continua
                                    self.time_limit -= 3  # Penalidade de 3 segundos
                                else:
                                    # Outros modos ainda terminam com clique errado
                                    self.last_score = self.score
                                    self.game_state = GAME_STATE_NAME_INPUT
                            break
                    
                    # Tratamento de cliques nos quadrantes para o modo seta
                    if self.game_mode == GAME_MODE_ARROW:
                        clicked_quadrant = self.get_clicked_quadrant(mouse_pos)
                        if clicked_quadrant is not None:
                            self.selections_total += 1
                            
                            # Verifica se clicou no quadrante correto E a seta está apontando para ele
                            if (clicked_quadrant == self.target_quadrant and self.arrow_in_target_zone):
                                # ACERTO PERFEITO! Quadrante correto no momento correto
                                self.score += 1
                                self.selections_correct += 1
                                self.data_collector.record_click(mouse_pos, True)
                                self.data_collector.update_trial_score(self.score)
                                # Registra métricas detalhadas do modo seta
                                self.data_collector.record_arrow_selection(
                                    True, clicked_quadrant, self.target_quadrant, 
                                    self.arrow_angle, self.arrow_rotation_speed, self.arrow_in_target_zone
                                )
                                # Modo seta não recebe bônus de tempo - tempo fixo de 90 segundos
                                # Seleciona novo quadrante alvo com nova velocidade
                                self.select_new_arrow_target()
                                # Inicia nova tentativa
                                self.data_collector.start_new_trial(self.game_mode)
                            else:
                                # ERRO: Quadrante errado OU timing errado
                                self.data_collector.record_click(mouse_pos, False)
                                self.data_collector.update_trial_score(self.score)
                                # Registra métricas detalhadas do erro
                                self.data_collector.record_arrow_selection(
                                    False, clicked_quadrant, self.target_quadrant, 
                                    self.arrow_angle, self.arrow_rotation_speed, self.arrow_in_target_zone
                                )
                                # Modo seta não tem penalidade de tempo - tempo fixo de 90 segundos
                
                elif self.game_state == GAME_STATE_INSTRUCTIONS or self.game_state == GAME_STATE_HIGHSCORE:
                    if self.back_button.is_clicked(mouse_pos):
                        self.game_state = GAME_STATE_MENU
                
                elif self.game_state == GAME_STATE_NAME_INPUT:
                    result = self.highscore_input.handle_event(event)
                    if result is not None or self.highscore_confirm_button.is_clicked(mouse_pos):
                        # Pega o nome do input, com tratamento correto para espaços
                        name = result if result is not None else self.highscore_input.text
                        # Limpa o nome antes de usar
                        clean_name = name.strip() if name else ""
                        self.add_highscore(clean_name, self.last_score, self.game_mode)
                        self.data_collector.set_username(clean_name if clean_name else "Anônimo")  # Salva nome para coleta de dados
                        self.game_state = GAME_STATE_MENU
                

        
        # Atualiza estados de hover dos botões
        if self.game_state == GAME_STATE_MENU:
            self.single_mode_button.check_hover(mouse_pos)
            self.alternating_mode_button.check_hover(mouse_pos)
            self.infinite_mode_button.check_hover(mouse_pos)
            self.arrow_mode_button.check_hover(mouse_pos)
            self.instructions_button.check_hover(mouse_pos)
            self.highscore_button.check_hover(mouse_pos)
        elif self.game_state == GAME_STATE_USER_INPUT:
            self.confirm_button.check_hover(mouse_pos)
        elif self.game_state == GAME_STATE_INSTRUCTIONS or self.game_state == GAME_STATE_HIGHSCORE:
            self.back_button.check_hover(mouse_pos)
        elif self.game_state == GAME_STATE_NAME_INPUT:
            self.highscore_confirm_button.check_hover(mouse_pos)
    
    def reset_game(self):
        # Reinicia o estado do jogo
        for escalator in self.escalators:
            escalator.characters = []
        self.character_factory.reset()
        self.select_new_target()
        self.spawn_counter = 0
        self.start_time = 0
        self.has_target_spawned = False
        self.target_spawn_count = 0
        self.score = 0
        self.selections_total = 0
        self.selections_correct = 0
        self.is_first_target = True  # Reseta para o primeiro alvo
        
        # Reset variáveis do modo seta
        if self.game_mode == GAME_MODE_ARROW:
            self.arrow_angle = 0
            self.arrow_in_target_zone = False
            self.last_quadrant_pointed = -1
            self.select_new_arrow_target()
            self.time_limit = 90  # 90 segundos fixos para o modo seta
            # Define o start_time para o modo seta já que ele não passa por DISPLAY_TARGET
            self.start_time = time.time()
        
        # Cria nova sessão para cada jogo e inicia nova trial
        self.data_collector.create_new_session(self.game_mode)
        self.data_collector.start_new_trial(self.game_mode)
    
    def spawn_character(self, target=False):
        # Escolhe uma escada rolante aleatória
        escalator = random.choice(self.escalators)
        char_x = escalator.x + (escalator.width - CHARACTER_SIZE) // 2
        char_y = 0 - CHARACTER_SIZE  # Começa acima da tela
        
        if target:
            # Cria o personagem alvo com os mesmos traços
            character = Character(char_x, char_y, self.target_traits)
            self.has_target_spawned = True
            self.target_spawned_time = time.time()
            self.target_spawn_count += 1
            self.data_collector.record_target_spawn(self.target_traits)
        else:
            # Cria um personagem aleatório (garante que não seja igual ao alvo)
            while True:
                character = self.character_factory.create_random_character(char_x, char_y)
                if character.traits != self.target_traits:
                    break
        
        escalator.add_character(character)
    
    def update(self):
        if self.game_state == GAME_STATE_USER_INPUT:
            self.text_input.update()
        elif self.game_state == GAME_STATE_NAME_INPUT:
            self.highscore_input.update()
        
        current_time = time.time()
        
        # Manipula transições de estado do jogo
        if self.game_state == GAME_STATE_DISPLAY_TARGET:
            # Determina o tempo de exibição baseado no modo e se é o primeiro alvo
            if self.game_mode == GAME_MODE_ALTERNATING and not self.is_first_target:
                display_time = 2.5  # Tempo menor para alvos subsequentes no modo alternado
            else:
                display_time = self.display_target_time  # Tempo normal
            
            # Muda para estado de jogo após o tempo de exibição
            if current_time - self.target_display_start >= display_time:
                self.game_state = GAME_STATE_PLAYING
                if self.start_time == 0:  # Só define start_time na primeira vez
                    self.start_time = current_time
        
        # Atualiza todas as escadas rolantes
        for escalator in self.escalators:
            escalator.update()
        
        if self.game_state == GAME_STATE_PLAYING:
            # Para o modo seta, garante que o start_time está definido
            if self.game_mode == GAME_MODE_ARROW and self.start_time == 0:
                self.start_time = current_time
            
            # Verifica se o tempo acabou
            if current_time - self.start_time >= self.time_limit:
                self.last_score = self.score
                self.game_state = GAME_STATE_NAME_INPUT
                # Atualiza maior pontuação se necessário
                if self.score > self.highest_score:
                    self.highest_score = self.score
            
            # Faz aparecer novos personagens
            self.spawn_counter += 1
            if self.spawn_counter >= CHARACTER_SPAWN_RATE:
                self.spawn_counter = 0
                
                # Manipula o aparecimento do personagem alvo dependendo do modo de jogo
                if self.game_mode == GAME_MODE_SINGLE:
                    # No modo único, faz o alvo aparecer apenas uma vez
                    if not self.has_target_spawned and current_time - self.start_time >= 5:
                        self.spawn_character(target=True)
                    else:
                        # Sempre faz aparecer um personagem aleatório não-alvo
                        self.spawn_character(target=False)
                elif self.game_mode == GAME_MODE_ALTERNATING:
                    # No modo alternado, sempre garante que haja um alvo
                    if not self.has_target_spawned and random.random() < 0.2:
                        # 20% de chance de fazer o alvo aparecer quando não há um
                        self.spawn_character(target=True)
                    else:
                        # Faz aparecer um personagem aleatório não-alvo
                        self.spawn_character(target=False)
                elif self.game_mode == GAME_MODE_INFINITE:
                    # No modo infinito, sempre garante que haja um alvo
                    if not self.has_target_spawned and random.random() < 0.2:
                        # 20% de chance de fazer o alvo aparecer quando não há um
                        self.spawn_character(target=True)
                    else:
                        # Faz aparecer um personagem aleatório não-alvo
                        self.spawn_character(target=False)
            
            # Atualiza a seta no modo seta
            if self.game_mode == GAME_MODE_ARROW:
                self.arrow_angle += self.arrow_rotation_speed
                if self.arrow_angle >= 360:
                    self.arrow_angle = 0
                
                # Verifica se a seta está apontando para o quadrante correto com alta precisão
                pointed_quadrant = self.get_arrow_pointed_quadrant()
                self.arrow_in_target_zone = (pointed_quadrant == self.target_quadrant and pointed_quadrant != -1)
                self.last_quadrant_pointed = pointed_quadrant

    def select_new_arrow_target(self):
        """Seleciona um novo quadrante alvo e define a cor da seta"""
        self.target_quadrant = random.randint(0, 3)
        self.arrow_color = QUADRANT_COLORS[self.target_quadrant]
        # Velocidade entre 2 (mais lento) e 8 (mais rápido)
        self.arrow_rotation_speed = random.uniform(2.0, 8.0)  # Entre 2 e 8
    
    def get_arrow_pointed_quadrant(self):
        """Determina para qual quadrante a seta está apontando - ativa quando ENTRA no quadrante"""
        # Normaliza o ângulo para 0-360
        angle = self.arrow_angle % 360
        
        # Mapeamento correto dos quadrantes visuais:
        # Quadrante 0 (Superior Esquerdo): 180° - 270°
        # Quadrante 1 (Superior Direito): 270° - 360° (0°)
        # Quadrante 2 (Inferior Esquerdo): 90° - 180°
        # Quadrante 3 (Inferior Direito): 0° - 90°
        
        # Expande a janela para começar mais cedo (quando entra no quadrante)
        if 270 <= angle or angle < 90:  # Direita (superior + inferior direito)
            if 270 <= angle or angle < 0:  # Superior direito
                return 1
            else:  # 0 <= angle < 90 - Inferior direito
                return 3
        elif 90 <= angle < 270:  # Esquerda (superior + inferior esquerdo)
            if 180 <= angle < 270:  # Superior esquerdo
                return 0
            else:  # 90 <= angle < 180 - Inferior esquerdo
                return 2
        else:
            return -1
    
    def get_clicked_quadrant(self, mouse_pos):
        """Determina qual quadrante foi clicado baseado na posição do mouse"""
        mx, my = mouse_pos
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        
        if mx < center_x and my < center_y:
            return 0  # Superior esquerdo
        elif mx >= center_x and my < center_y:
            return 1  # Superior direito
        elif mx < center_x and my >= center_y:
            return 2  # Inferior esquerdo
        else:
            return 3  # Inferior direito
    
    def draw_arrow_mode(self):
        """Desenha a interface do modo seta"""
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        
        # Desenha os quadrantes coloridos
        for i in range(4):
            quadrant_color = QUADRANT_COLORS[i]
            
            # Se é o quadrante alvo e a seta está apontando para ele, destaca com brilho
            if i == self.target_quadrant and self.arrow_in_target_zone:
                # Quadrante brilhante quando é a hora certa de clicar
                bright_color = tuple(min(255, c + 50) for c in quadrant_color)
                quadrant_color = bright_color
            elif i == self.target_quadrant:
                # Quadrante alvo mas seta não está apontando - fica um pouco mais escuro
                dark_color = tuple(max(50, c - 30) for c in quadrant_color)
                quadrant_color = dark_color
            
            # Desenha cada quadrante
            if i == 0:  # Superior esquerdo
                pygame.draw.rect(screen, quadrant_color, (0, 0, center_x, center_y))
            elif i == 1:  # Superior direito
                pygame.draw.rect(screen, quadrant_color, (center_x, 0, center_x, center_y))
            elif i == 2:  # Inferior esquerdo
                pygame.draw.rect(screen, quadrant_color, (0, center_y, center_x, center_y))
            else:  # Inferior direito
                pygame.draw.rect(screen, quadrant_color, (center_x, center_y, center_x, center_y))
        
        # Desenha linhas divisórias
        pygame.draw.line(screen, GAME_BLACK, (center_x, 0), (center_x, HEIGHT), 4)
        pygame.draw.line(screen, GAME_BLACK, (0, center_y), (WIDTH, center_y), 4)
        
        # Desenha a seta no centro
        self.draw_arrow(center_x, center_y)
        
        # Exibe informações do jogo
        score_text = FONT.render(f"Pontuação: {self.score}", True, GAME_WHITE)
        screen.blit(score_text, (10, 10))
        
        current_time = time.time()
        time_left = max(0, self.time_limit - (current_time - self.start_time))
        time_text = FONT.render(f"Tempo: {time_left:.1f}s", True, GAME_WHITE)
        screen.blit(time_text, (10, 50))
        
        # Mostra a velocidade atual da seta
        speed_text = SMALL_FONT.render(f"Velocidade: {self.arrow_rotation_speed:.1f}", True, GAME_WHITE)
        screen.blit(speed_text, (10, 90))
        
        # Precisão é coletada internamente mas não mostrada ao jogador
        
        # Instruções simples para o jogador
        if self.arrow_in_target_zone:
            instruction_text = SMALL_FONT.render("AGORA! Clique no quadrante brilhante!", True, GAME_GOLD)
            instruction_bg_color = (50, 100, 50)  # Verde escuro
        else:
            instruction_text = SMALL_FONT.render("Aguarde a seta apontar para o quadrante da mesma cor!", True, GAME_WHITE)
            instruction_bg_color = (0, 0, 0)  # Preto
        
        instruction_rect = instruction_text.get_rect(centerx=WIDTH//2, y=HEIGHT - 50)
        pygame.draw.rect(screen, instruction_bg_color, instruction_rect.inflate(20, 10))
        screen.blit(instruction_text, instruction_rect)
    
    def draw_arrow(self, center_x, center_y):
        """Desenha a seta girando no centro da tela"""
        import math
        
        # Tamanho da seta
        arrow_length = 80
        arrow_width = 20
        
        # Calcula as posições da seta baseado no ângulo
        angle_rad = math.radians(self.arrow_angle)
        
        # Ponta da seta
        tip_x = center_x + arrow_length * math.cos(angle_rad)
        tip_y = center_y + arrow_length * math.sin(angle_rad)
        
        # Base da seta
        base_angle1 = angle_rad + math.radians(150)
        base_angle2 = angle_rad + math.radians(210)
        
        base1_x = center_x + (arrow_length - 30) * math.cos(base_angle1)
        base1_y = center_y + (arrow_length - 30) * math.sin(base_angle1)
        
        base2_x = center_x + (arrow_length - 30) * math.cos(base_angle2)
        base2_y = center_y + (arrow_length - 30) * math.sin(base_angle2)
        
        # Desenha a seta como um triângulo
        arrow_points = [(tip_x, tip_y), (base1_x, base1_y), (base2_x, base2_y)]
        
        # Sombra da seta
        shadow_points = [(p[0] + 2, p[1] + 2) for p in arrow_points]
        pygame.draw.polygon(screen, GAME_BLACK, shadow_points)
        
        # Seta principal
        pygame.draw.polygon(screen, self.arrow_color, arrow_points)
        
        # Borda da seta
        pygame.draw.polygon(screen, GAME_BLACK, arrow_points, 3)
        
        # Círculo no centro
        pygame.draw.circle(screen, GAME_BLACK, (center_x, center_y), 15)
        pygame.draw.circle(screen, GAME_WHITE, (center_x, center_y), 12)

    def draw_menu(self):
        # Fundo simples e limpo com gradiente suave
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            # Gradiente suave do azul claro para azul médio
            r = int(135 + (45 - 135) * ratio)  # 135 -> 45
            g = int(206 + (85 - 206) * ratio)  # 206 -> 85  
            b = int(235 + (160 - 235) * ratio) # 235 -> 160
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))
        
        # Título principal simples com cor que contrasta
        title_text = "Memory Escalator"
        title_x = WIDTH//2 - GAME_TITLE_FONT.size(title_text)[0]//2
        
        # Sombra mais visível para contorno
        title_shadow = GAME_TITLE_FONT.render(title_text, True, (0, 0, 0))
        # Desenha sombra em múltiplas posições para criar contorno
        for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2), (-2, 0), (2, 0), (0, -2), (0, 2)]:
            screen.blit(title_shadow, (title_x + dx, 50 + dy))
        
        # Título principal em branco para máximo contraste
        title_main = GAME_TITLE_FONT.render(title_text, True, (255, 255, 255))
        screen.blit(title_main, (title_x, 50))
        
        # Subtítulo com cor mais escura
        subtitle_text = "Jogo da Memória na Escada Rolante"
        subtitle_x = WIDTH//2 - GAME_SUBTITLE_FONT.size(subtitle_text)[0]//2
        
        # Sombra do subtítulo para contorno
        subtitle_shadow = GAME_SUBTITLE_FONT.render(subtitle_text, True, (0, 0, 0))
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            screen.blit(subtitle_shadow, (subtitle_x + dx, 120 + dy))
        
        # Subtítulo em branco para melhor contraste
        subtitle = GAME_SUBTITLE_FONT.render(subtitle_text, True, (255, 255, 255))
        screen.blit(subtitle, (subtitle_x, 120))
        
        # Linha decorativa em cor escura
        line_y = 160
        pygame.draw.line(screen, (30, 50, 90), (WIDTH//2 - 200, line_y), (WIDTH//2 + 200, line_y), 2)
        
        # Instruções
        instructions = SMALL_FONT.render("Selecione o Modo de Jogo:", True, (255, 255, 255))
        screen.blit(instructions, (WIDTH//2 - instructions.get_width()//2, 190))
        
        # Desenha os botões
        self.single_mode_button.draw(screen)
        self.alternating_mode_button.draw(screen)
        self.infinite_mode_button.draw(screen)
        self.arrow_mode_button.draw(screen)
        self.instructions_button.draw(screen)
        self.highscore_button.draw(screen)
        
        # PS simples direcionando para Como Jogar
        ps_text = "PS: Para descobrir mais sobre como jogar e os modos de jogo, clique em 'Como Jogar'"
        ps_render = TINY_FONT.render(ps_text, True, (200, 200, 200))
        screen.blit(ps_render, (WIDTH//2 - ps_render.get_width()//2, HEIGHT - 80))
        
        # Footer simples - ajustado para tela maior
        footer_y = HEIGHT - 40
        footer_text = "Pressione ESC para sair"
        footer = TINY_FONT.render(footer_text, True, (200, 200, 200))
        screen.blit(footer, (WIDTH//2 - footer.get_width()//2, footer_y))
    
    def draw_instructions(self):
        # Mesmo fundo simples do menu
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(135 + (45 - 135) * ratio)
            g = int(206 + (85 - 206) * ratio)
            b = int(235 + (160 - 235) * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))
        
        # Título maior e mais grosso - ajustado para tela maior
        title_text = "TUTORIAL - Como Jogar"
        title_shadow = INSTRUCTIONS_TITLE_FONT.render(title_text, True, (0, 0, 0, 100))
        screen.blit(title_shadow, (WIDTH//2 - title_shadow.get_width()//2 + 3, 33))
        
        title = INSTRUCTIONS_TITLE_FONT.render(title_text, True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        # Tutorial passo a passo - layout melhorado
        sections = [
            {
                "title": "PASSO 1: MEMORIZE",
                "color": GAME_GOLD,
                "items": [
                    "Um personagem aparecerá na tela por 4 segundos",
                    "Observe TODAS as características: cabeça, rosto, corpo e chapéu", 
                    "Memorize bem! Você precisará encontrá-lo depois"
                ]
            },
            {
                "title": "PASSO 2: PROCURE", 
                "color": GAME_GOLD,
                "items": [
                    "Personagens começarão a descer pelas escadas rolantes",
                    "Cada escada tem velocidade diferente (rápida, média, lenta)",
                    "Encontre o personagem EXATO que você memorizou"
                ]
            },
            {
                "title": "PASSO 3: CLIQUE",
                "color": GAME_GOLD, 
                "items": [
                    "Clique NO personagem correto quando ele aparecer",
                    "Acertou = Pontos!",
                    "Errou = Fim de jogo (exceto no modo infinito: -3s)"
                ]
            },
            {
                "title": "MODOS DISPONÍVEIS:",
                "color": GAME_LIGHT_BLUE,
                "items": [
                    "APARIÇÃO ÚNICA: Encontre o personagem 1 vez (30 segundos)",
                    "MODO ALTERNADO: Personagem muda a cada acerto (30 segundos)", 
                    "MODO INFINITO: Continue encontrando, ganhe +5s por acerto!",
                    "MODO SETA: 90 segundos fixos - máxima pontuação possível!"
                ]
            },
            {
                "title": "MODO SETA - REGRAS ESPECIAIS:",
                "color": GAME_LIGHT_BLUE,
                "items": [
                    "Você tem EXATOS 90 segundos para pontuar o máximo possível",
                    "A seta gira e muda de cor constantemente",
                    "Clique no quadrante da mesma COR da seta",
                    "TIMING É TUDO: Só vale quando a seta APONTA para o quadrante correto!",
                    "Velocidade muda a cada acerto - mantenha o foco!"
                ]
            },
            {
                "title": "DICAS IMPORTANTES:",
                "color": GAME_GREEN,
                "items": [
                    "Preste atenção nos DETALHES de cada parte do personagem",
                    "Não clique muito rápido - observe bem antes de clicar",
                    "Use ESC para voltar ao menu a qualquer momento",
                    "No modo infinito: erro reduz tempo, acerto adiciona tempo"
                ]
            }
        ]
        
        y_pos = 100  # Posição inicial otimizada
        for section in sections:
            # Usa fontes diferenciadas por seção
            if section["title"].startswith("DICAS"):
                title_font = TINY_FONT
                item_font = TINY_FONT
                title_spacing = 24
                item_spacing = 18
                section_spacing = 10
            elif section["title"].startswith("MODO SETA"):
                title_font = SMALL_FONT
                item_font = TINY_FONT
                title_spacing = 30
                item_spacing = 20
                section_spacing = 12
            else:
                title_font = INSTRUCTIONS_TEXT_FONT
                item_font = SMALL_FONT
                title_spacing = 32
                item_spacing = 23
                section_spacing = 14
            
            # Desenha o título da seção
            title_text = title_font.render(section["title"], True, section["color"])
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, y_pos))
            y_pos += title_spacing
            
            # Desenha linha decorativa para passos
            if section["title"].startswith("PASSO"):
                pygame.draw.line(screen, section["color"], 
                               (WIDTH//2 - 250, y_pos), 
                               (WIDTH//2 + 250, y_pos), 3)
                y_pos += 12
            
            # Desenha os itens da seção
            for item in section["items"]:
                if section["title"].startswith("MODOS"):
                    item_text = item_font.render(item, True, GAME_SILVER)
                else:
                    item_text = item_font.render(item, True, GAME_WHITE)
                
                item_x = WIDTH//2 - item_text.get_width()//2
                screen.blit(item_text, (item_x, y_pos))
                y_pos += item_spacing
            
            # Espaço entre seções
            y_pos += section_spacing
        
        # Verifica se há espaço suficiente para o destaque final
        remaining_space = HEIGHT - 100 - y_pos  # Deixa espaço para o botão voltar
        
        if remaining_space > 50:  # Se há espaço suficiente
            # Destaque final - ajustado para tela maior
            final_tip = "Lembre-se: Paciência e atenção são a chave do sucesso!"
            final_text = SMALL_FONT.render(final_tip, True, GAME_GOLD)
            # Caixa de destaque
            pygame.draw.rect(screen, (0, 0, 0, 50), 
                            (WIDTH//2 - final_text.get_width()//2 - 15, y_pos - 8, 
                             final_text.get_width() + 30, 35), border_radius=12)
            screen.blit(final_text, (WIDTH//2 - final_text.get_width()//2, y_pos))
        
        # Botão voltar
        self.back_button.draw(screen)
    
    def draw_highscores(self):
        # Mesmo fundo simples do menu
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(135 + (45 - 135) * ratio)
            g = int(206 + (85 - 206) * ratio)
            b = int(235 + (160 - 235) * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))
        
        # Título maior e mais grosso
        title_text = "Melhores Pontuações"
        title_shadow = HIGHSCORE_TITLE_FONT.render(title_text, True, (0, 0, 0, 100))
        screen.blit(title_shadow, (WIDTH//2 - title_shadow.get_width()//2 + 3, 33))
        
        title = HIGHSCORE_TITLE_FONT.render(title_text, True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        # Duas colunas - modo infinito e modo seta
        left_x = WIDTH // 4
        right_x = WIDTH * 3 // 4
        
        # Modo Infinito - Coluna esquerda
        mode_title_infinite = HIGHSCORE_TEXT_FONT.render("Modo Infinito", True, GAME_GOLD)
        screen.blit(mode_title_infinite, (left_x - mode_title_infinite.get_width()//2, 100))
        
        # Linha decorativa
        pygame.draw.line(screen, GAME_GOLD, 
                        (left_x - 120, 140), 
                        (left_x + 120, 140), 3)
        
        # Pontuações do modo infinito
        scores_infinite = self.highscores.get("infinite", [])
        y_pos_left = 160
        
        if not scores_infinite:
            no_scores = SMALL_FONT.render("Nenhuma pontuação ainda", True, GAME_WHITE)
            screen.blit(no_scores, (left_x - no_scores.get_width()//2, y_pos_left))
        else:
            for j, score_data in enumerate(scores_infinite[:5]):  # Top 5
                rank = f"{j+1}º"
                name = score_data["name"][:12]  # Nome menor para caber na coluna
                score = score_data["score"]
                
                # Cor baseada na posição
                if j == 0:
                    color = GAME_GOLD
                    medal = "🥇"
                elif j == 1:
                    color = GAME_SILVER  
                    medal = "🥈"
                elif j == 2:
                    color = (205, 127, 50)  # Bronze
                    medal = "🥉"
                else:
                    color = GAME_WHITE
                    medal = ""
                
                # Formato melhorado com medal emoji
                if j < 3:
                    score_text = f"{medal} {rank} {name} - {score}"
                else:
                    score_text = f"{rank} {name} - {score}"
                
                text_surf = SMALL_FONT.render(score_text, True, color)
                screen.blit(text_surf, (left_x - text_surf.get_width()//2, y_pos_left))
                y_pos_left += 40

        # Modo Seta - Coluna direita
        mode_title_arrow = HIGHSCORE_TEXT_FONT.render("Modo Seta", True, GAME_LIGHT_BLUE)
        screen.blit(mode_title_arrow, (right_x - mode_title_arrow.get_width()//2, 100))
        
        # Linha decorativa
        pygame.draw.line(screen, GAME_LIGHT_BLUE, 
                        (right_x - 120, 140), 
                        (right_x + 120, 140), 3)
        
        # Pontuações do modo seta
        scores_arrow = self.highscores.get("arrow", [])
        y_pos_right = 160
        
        if not scores_arrow:
            no_scores = SMALL_FONT.render("Nenhuma pontuação ainda", True, GAME_WHITE)
            screen.blit(no_scores, (right_x - no_scores.get_width()//2, y_pos_right))
        else:
            for j, score_data in enumerate(scores_arrow[:5]):  # Top 5
                rank = f"{j+1}º"
                name = score_data["name"][:12]  # Nome menor para caber na coluna
                score = score_data["score"]
                
                # Cor baseada na posição
                if j == 0:
                    color = GAME_GOLD
                    medal = "🥇" # Display das medalhas ta zuado
                elif j == 1:
                    color = GAME_SILVER  
                    medal = "🥈"
                elif j == 2:
                    color = (205, 127, 50)  # Bronze
                    medal = "🥉"
                else:
                    color = GAME_WHITE
                    medal = ""
                
                if j < 3:
                    score_text = f"{medal} {rank} {name} - {score}"
                else:
                    score_text = f"{rank} {name} - {score}"
                
                text_surf = SMALL_FONT.render(score_text, True, color)
                screen.blit(text_surf, (right_x - text_surf.get_width()//2, y_pos_right))
                y_pos_right += 40
        
        # Botão voltar
        self.back_button.draw(screen)
    
    def draw_name_input(self):
        # Mesmo fundo simples do menu
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(135 + (45 - 135) * ratio)
            g = int(206 + (85 - 206) * ratio)
            b = int(235 + (160 - 235) * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))
        
        # Título
        if self.is_new_highscore:
            title = GAME_SUBTITLE_FONT.render("NOVO RECORDE!", True, GAME_GOLD)
            subtitle = SMALL_FONT.render(f"Você fez {self.last_score} pontos!", True, GAME_WHITE)
        else:
            title = GAME_SUBTITLE_FONT.render("Fim de Jogo", True, GAME_WHITE)
            subtitle = SMALL_FONT.render(f"Pontuação: {self.last_score}", True, GAME_WHITE)
        
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, HEIGHT//2 - 60))
        
        # Prompt
        prompt = SMALL_FONT.render("Digite seu nome:", True, GAME_WHITE)
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 - 20))
        
        # Campo de entrada
        self.highscore_input.draw(screen)
        self.highscore_confirm_button.draw(screen)
        
        # Instrução
        instruction = TINY_FONT.render("Pressione Enter ou clique em Salvar", True, GAME_WHITE)
        screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, HEIGHT//2 + 150))

    def draw(self):
        # Limpa a tela
        screen.fill(BACKGROUND_COLOR)
        
        if self.game_state == GAME_STATE_USER_INPUT:
            # Desenha a tela de identificação do usuário
            title = TITLE_FONT.render("Identificação do Jogador", True, (50, 50, 150))
            screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))
            
            prompt = SMALL_FONT.render("Por favor, digite seu nome:", True, (0, 0, 0))
            screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 - 40))
            
            self.text_input.draw(screen)
            self.confirm_button.draw(screen)
            
        elif self.game_state == GAME_STATE_MENU:
            self.draw_menu()
            
        elif self.game_state == GAME_STATE_HIGHSCORE:
            self.draw_highscores()
            
        elif self.game_state == GAME_STATE_INSTRUCTIONS:
            self.draw_instructions()
            
        elif self.game_state == GAME_STATE_NAME_INPUT:
            self.draw_name_input()
            
        elif self.game_state == GAME_STATE_DISPLAY_TARGET:
            # Exibe o personagem alvo
            if self.game_mode == GAME_MODE_SINGLE:
                mode_text = "Modo Aparição Única"
            elif self.game_mode == GAME_MODE_ALTERNATING:
                mode_text = "Modo Alternado"
            else:
                mode_text = "Modo Infinito"

            mode_render = SMALL_FONT.render(mode_text, True, (50, 50, 150))
            screen.blit(mode_render, (WIDTH//2 - mode_render.get_width()//2, 20))
            
            # Usa fonte maior para "MEMORIZE" - texto diferente para modo alternado
            if self.game_mode == GAME_MODE_ALTERNATING and not self.is_first_target:
                memorize_text = GAME_TITLE_FONT.render("NOVO ALVO!", True, (220, 30, 30))  # Vermelho para destacar
                subtitle_text = SMALL_FONT.render("Memorize o novo personagem", True, (0, 0, 0))
                screen.blit(subtitle_text, (WIDTH//2 - subtitle_text.get_width()//2, HEIGHT//4 + 60))
            else:
                memorize_text = GAME_TITLE_FONT.render("MEMORIZE", True, (0, 0, 0))
            screen.blit(memorize_text, (WIDTH//2 - memorize_text.get_width()//2, HEIGHT//4))
            
            # Desenha o personagem alvo
            self.target_character.draw(screen)
            
            # Exibe a contagem regressiva centralizada
            if self.game_mode == GAME_MODE_ALTERNATING and not self.is_first_target:
                display_time = 2.5
                countdown_text = "Continuando em:"
            else:
                display_time = self.display_target_time
                countdown_text = "Iniciando em:"
            
            time_left = max(0, display_time - (time.time() - self.target_display_start))
            countdown = FONT.render(f"{countdown_text} {time_left:.1f}", True, (0, 0, 0))
            screen.blit(countdown, (WIDTH//2 - countdown.get_width()//2, HEIGHT*3//4))
            
            # Mostra pontuação atual no modo alternado
            if self.game_mode == GAME_MODE_ALTERNATING and self.score > 0:
                score_text = SMALL_FONT.render(f"Pontuação atual: {self.score}", True, (0, 100, 0))
                screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT*3//4 + 40))
            
        elif self.game_state == GAME_STATE_PLAYING:
            if self.game_mode == GAME_MODE_ARROW:
                # Desenha a interface do modo seta
                self.draw_arrow_mode()
            else:
                # Desenha todas as escadas rolantes para outros modos
                for escalator in self.escalators:
                    escalator.draw(screen)
                
                # Desenha barra de progresso no topo em vez do timer
                time_left = max(0, self.time_limit - (time.time() - self.start_time))
                progress = time_left / self.time_limit if self.time_limit > 0 else 0
            
                # Barra de progresso - fundo
                progress_bar_width = WIDTH - 40
                progress_bar_height = 20
                progress_bar_x = 20
                progress_bar_y = 10
                
                # Fundo da barra (cinza escuro)
                pygame.draw.rect(screen, (100, 100, 100), (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height))
                
                # Barra de progresso (verde para vermelho baseado no tempo)
                if progress > 0.5:
                    bar_color = (0, 180, 0)  # Verde
                elif progress > 0.25:
                    bar_color = (255, 215, 0)  # Amarelo/Dourado
                else:
                    bar_color = (220, 30, 30)  # Vermelho
                
                progress_width = int(progress_bar_width * progress)
                if progress_width > 0:
                    pygame.draw.rect(screen, bar_color, (progress_bar_x, progress_bar_y, progress_width, progress_bar_height))
                
                # Borda da barra de progresso
                pygame.draw.rect(screen, (50, 50, 50), (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height), 2)
                
                # Exibe a pontuação
                if self.game_mode == GAME_MODE_SINGLE:
                    mode_text = "Encontre uma vez"
                elif self.game_mode == GAME_MODE_ALTERNATING:
                    mode_text = f"Personagem alterna: {self.score} acertos"
                else:  # Modo infinito
                    mode_text = f"+{self.time_bonus}s por acerto"
                
                score_text = SMALL_FONT.render(f"Pontuação: {self.score} - {mode_text}", True, (0, 0, 0))
                screen.blit(score_text, (10, 40))
                
                # Removida a exibição da precisão conforme solicitado
                
                # No caso do modo múltiplo, mostra um pequeno lembrete de como o personagem se parece
                if self.game_mode != GAME_MODE_SINGLE:
                    reminder_text = TINY_FONT.render("Personagem Alvo:", True, (0, 0, 0))
                    screen.blit(reminder_text, (10, 70))
                    
                    # Desenha uma versão pequena do alvo com tamanho correto
                    mini_size = int(CHARACTER_SIZE * 0.75)  # 75% do tamanho original para melhor visibilidade
                    mini_segment_height = mini_size // 3
                    
                    # Redimensiona e desenha cada parte do personagem
                    body_img = pygame.transform.scale(self.target_traits["body"]["image"], (mini_size, mini_segment_height))
                    head_img = pygame.transform.scale(self.target_traits["head"]["image"], (mini_size, mini_segment_height))
                    face_img = pygame.transform.scale(self.target_traits["face"]["image"], (mini_size, mini_segment_height))
                    hat_img = pygame.transform.scale(self.target_traits["hat"]["image"], (mini_size, mini_segment_height))
                    
                    # Posição do mini personagem
                    mini_x, mini_y = 20, 90
                    
                    # Desenha as partes na ordem correta
                    screen.blit(body_img, (mini_x, mini_y + mini_segment_height * 2))  # Corpo na parte inferior
                    screen.blit(head_img, (mini_x, mini_y + mini_segment_height))      # Cabeça no meio
                    screen.blit(face_img, (mini_x, mini_y + mini_segment_height))      # Rosto sobre a cabeça
                    screen.blit(hat_img, (mini_x, mini_y))                            # Chapéu no topo
            
        elif self.game_state == GAME_STATE_SUCCESS:
            text = FONT.render("Sucesso! Você encontrou o personagem!", True, (0, 128, 0))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))
            
            score_text = FONT.render(f"Pontuação: {self.score}", True, (0, 0, 0))
            screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
            
            restart = SMALL_FONT.render("Pressione 'R' para jogar novamente ou ESC para o menu", True, (0, 0, 0))
            screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 50))
            
        elif self.game_state == GAME_STATE_FAILURE:
            text = FONT.render("Fim de Jogo! Você não encontrou o personagem.", True, (255, 0, 0))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))
            
            score_text = FONT.render(f"Pontuação: {self.score}", True, (0, 0, 0))
            screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
            
            # Renderiza a pontuação máxima como uma superfície de texto
            high_score_text = SMALL_FONT.render(f"Maior Pontuação: {self.highest_score}", True, (0, 0, 0))
            screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//2 + 30))
            
            restart = SMALL_FONT.render("Pressione 'R' para jogar novamente ou ESC para o menu", True, (0, 0, 0))
            screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 70))
        
        # Atualiza a tela
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)  # 60 FPS
        # Salva os dados antes de sair
        self.data_collector.save_session_data()

# Função principal
def main():
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()