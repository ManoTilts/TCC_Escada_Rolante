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
WIDTH, HEIGHT = 1000, 800
BACKGROUND_COLOR = (200, 200, 200)
ESCALATOR_COLORS = [(100, 100, 100), (120, 120, 120), (140, 140, 140)]
ESCALATOR_SPEEDS = [2, 3, 4]  # velocidades diferentes para cada escada
ESCALATOR_WIDTH = 120
ESCALATOR_SPACING = 100
ESCALATOR_START_X = 170  # posição inicial da primeira escada

# propriedades do personagem
CHARACTER_SIZE = 75  # Tamanho total do personagem (3 * 25px)

# Estados do jogo
GAME_STATE_MENU = 0
GAME_STATE_DISPLAY_TARGET = 1
GAME_STATE_PLAYING = 2
GAME_STATE_SUCCESS = 3
GAME_STATE_FAILURE = 4
GAME_STATE_USER_INPUT = 5  # Novo estado para identificação do usuário

# Modos de jogo
GAME_MODE_SINGLE = 0  # Alvo aparece uma vez
GAME_MODE_MULTIPLE = 1  # Alvo aparece várias vezes
GAME_MODE_INFINITE = 2  # Infinito, o jogador ganha tempo ao clicar em personagens

# Taxa de aparição de personagens
CHARACTER_SPAWN_RATE = 60  # Frames entre aparições de personagens

# Fontes
FONT = pygame.font.SysFont('Arial', 36)
SMALL_FONT = pygame.font.SysFont('Arial', 24)
TINY_FONT = pygame.font.SysFont('Arial', 16)
TITLE_FONT = pygame.font.SysFont('Arial', 48, bold=True)

# Inicializa a tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Memória na Escada Rolante")
clock = pygame.time.Clock()

# Carrega recursos
def load_assets():
    assets = {
        'bodies': [],
        'faces': [],
        'hats': [],
        'heads': []
    }
    
    # Carrega corpos (3 arquivos possíveis)
    try:
        for i in range(1, 4):
            path = f"assets/bodies/bodie{i}.png"
            if os.path.exists(path):
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (50, 25))  # 50x25 pixels
                assets["bodies"].append({"image": img, "name": f"Corpo {i}"})
    except Exception as e:
        print(f"Erro ao carregar corpos: {e}")
        # Cria corpo padrão se não houver arquivos
        for i, color in enumerate([(255, 0, 0), (0, 255, 0), (0, 0, 255)]):
            img = pygame.Surface((50, 25), pygame.SRCALPHA)
            pygame.draw.rect(img, color, (0, 0, 50, 25))
            assets["bodies"].append({"image": img, "name": f"Corpo {i+1}"})

    # Carrega rostos (15 arquivos possíveis)
    try:
        for i in range(1, 16):
            path = f"assets/faces/face{i}.png"
            if os.path.exists(path):
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (50, 25))  # 50x25 pixels
                assets["faces"].append({"image": img, "name": f"Rosto {i}"})
    except Exception as e:
        print(f"Erro ao carregar rostos: {e}")
        # Cria rosto padrão se não houver arquivos
        for i in range(15):
            img = pygame.Surface((50, 25), pygame.SRCALPHA)
            pygame.draw.circle(img, (0, 0, 0), (12, 12), 3)
            pygame.draw.circle(img, (0, 0, 0), (38, 12), 3)
            assets["faces"].append({"image": img, "name": f"Rosto {i+1}"})

    # Carrega chapéus (10 arquivos)
    try:
        for i in range(1, 11):
            path = f"assets/hats/hat{i}.png"
            if os.path.exists(path):
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (50, 25))  # 50x25 pixels
                assets["hats"].append({"image": img, "name": f"Chapéu {i}"})
    except Exception as e:
        print(f"Erro ao carregar chapéus: {e}")
        # Cria chapéu padrão se não houver arquivos
        for i in range(10):
            img = pygame.Surface((50, 25), pygame.SRCALPHA)
            color = (random.randint(50, 250), random.randint(50, 250), random.randint(50, 250))
            pygame.draw.rect(img, color, (10, 10, 30, 15))
            assets["hats"].append({"image": img, "name": f"Chapéu {i+1}"})

    # Carrega cabeças (3 arquivos)
    try:
        for i in range(1, 4):
            path = f"assets/heads/head{i}.png"
            if os.path.exists(path):
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (50, 25))  # 50x25 pixels
                assets["heads"].append({"image": img, "name": f"Cabeça {i}"})
    except Exception as e:
        print(f"Erro ao carregar cabeças: {e}")
        # Cria cabeça padrão se não houver arquivos
        for i, color in enumerate([(255, 200, 200), (200, 255, 200), (200, 200, 255)]):
            img = pygame.Surface((50, 25), pygame.SRCALPHA)
            pygame.draw.rect(img, color, (0, 0, 50, 25))
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
        total_height = 75  # Altura total do personagem (3 * 25px)
        
        # Desenha o corpo na parte inferior
        screen.blit(self.traits["body"]["image"], 
                    (self.x, self.y + 50))  # 25px inferiores
        
        # Desenha a cabeça no meio
        screen.blit(self.traits["head"]["image"], 
                    (self.x, self.y + 25))  # 25px do meio
        
        # Desenha o rosto sobre a cabeça (mesma posição da cabeça pois é uma sobreposição)
        screen.blit(self.traits["face"]["image"], 
                    (self.x, self.y + 25))  # Sobrepõe na cabeça
        
        # Desenha o chapéu no topo
        screen.blit(self.traits["hat"]["image"], 
                    (self.x, self.y))  # 25px do topo
    
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
    def __init__(self, x, y, width, height, text, color=(100, 100, 200), hover_color=(150, 150, 250)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.SysFont('Arial', 24)
    
    def draw(self, screen):
        # Desenha o botão
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Borda
        
        # Desenha o texto
        text_surf = self.font.render(self.text, True, (255, 255, 255))
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
        # Desenha o fundo do campo de texto
        pygame.draw.rect(screen, (255, 255, 255), self.rect)  # Fundo branco
        pygame.draw.rect(screen, self.color, self.rect, 2)  # Borda
        
        # Renderiza o texto ou o placeholder
        if self.text:
            text_surf = self.font.render(self.text, True, self.color)
        else:
            text_surf = self.font.render(self.placeholder, True, self.color_inactive)
        
        # Desenha a superfície do texto
        text_rect = text_surf.get_rect(midleft=(self.rect.x + 5, self.rect.centery))
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
            "username": "Anônimo",  # Nome de usuário padrão
            "game_mode": None,
            "trials": [],
            "mouse_tracking": []
        }
        self.current_trial = None
        self.target_spawn_time = None
    
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
            "game_mode": game_mode,  # Registra o modo de jogo por tentativa
            "target_character": None,
            "target_spawn_time": None,
            "selection_time": None,
            "success": False,
            "reaction_time": None,
            "score": 0  # Inicializa a pontuação para esta tentativa
        }
    
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
        self.current_session["mouse_tracking"].append({
            "timestamp": time.time(),
            "x": mouse_pos[0],
            "y": mouse_pos[1],
            "game_state": game_state
        })
    
    def record_selection(self, success):
        if self.current_trial and self.target_spawn_time:
            selection_time = time.time()
            self.current_trial["selection_time"] = selection_time
            self.current_trial["success"] = success
            self.current_trial["reaction_time"] = selection_time - self.target_spawn_time
            self.current_session["trials"].append(self.current_trial)
            self.current_trial = None
    
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
            "mouse_tracking": []
        }
    
    def prepare_session_for_saving(self, session):
        # Cria uma cópia serializável dos dados da sessão
        serializable_session = {
            "session_id": session["session_id"],
            "username": session["username"],
            "game_mode": session["game_mode"],
            "trials": [],
            "mouse_tracking": session["mouse_tracking"]
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
                "score": trial.get("score", 0)
            }
            # Inclui target_character apenas se existir
            if trial.get("target_character"):
                serializable_trial["target_character"] = {
                    'head': {'name': trial["target_character"]["head"]["name"]},
                    'face': {'name': trial["target_character"]["face"]["name"]},
                    'body': {'name': trial["target_character"]["body"]["name"]},
                    'hat': {'name': trial["target_character"]["hat"]["name"]}
                }
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
        self.game_state = GAME_STATE_USER_INPUT  # Começa com estado de entrada do usuário
        self.game_mode = GAME_MODE_SINGLE
        self.target_character = None
        self.target_traits = None
        self.display_target_time = 4  # segundos para exibir o alvo
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
        
        # Cria entrada de texto para nome do usuário
        self.text_input = TextInput(
            WIDTH//2 - 150, HEIGHT//2,
            300, 40, 
            placeholder="Digite seu nome"
        )
        
        # Cria botão de confirmação para nome do usuário
        self.confirm_button = Button(
            WIDTH//2 - 75, HEIGHT//2 + 50,
            150, 40,
            "Confirmar"
        )
        
        # Cria botões para o menu
        button_width, button_height = 200, 50
        button_x = WIDTH // 2 - button_width // 2
        
        self.single_mode_button = Button(
            button_x, HEIGHT // 2 - 70, 
            button_width, button_height, 
            "Modo Aparição Única"
        )
        
        self.multiple_mode_button = Button(
            button_x, HEIGHT // 2, 
            button_width, button_height, 
            "Modo Múltiplas Aparições"
        )
        
        self.infinite_mode_button = Button(
            button_x, HEIGHT // 2 + 70, 
            button_width, button_height, 
            "Modo Infinito"
        )
        
        # Cria as três escadas rolantes
        for i in range(3):
            x = ESCALATOR_START_X + i * (ESCALATOR_WIDTH + ESCALATOR_SPACING)
            escalator = Escalator(x, ESCALATOR_WIDTH, ESCALATOR_SPEEDS[i], ESCALATOR_COLORS[i])
            self.escalators.append(escalator)
        
        # Carrega imagem de fundo do menu
        self.menu_image = self.load_menu_image()
    
    def load_menu_image(self):
        if os.path.exists("assets/misc/menu.png"):
            try:
                return pygame.image.load("assets/misc/menu.png")
            except pygame.error:
                print("Imagem do menu encontrada mas não pôde ser carregada, usando menu padrão.")
                return False
        else:
            print("Imagem do menu não encontrada, usando menu padrão.")
            return False

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
                
                # Manipula entrada de texto para identificação do usuário
                if self.game_state == GAME_STATE_USER_INPUT:
                    result = self.text_input.handle_event(event)
                    if result is not None:  # Enter foi pressionado
                        self.data_collector.set_username(result)
                        self.game_state = GAME_STATE_MENU
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == GAME_STATE_USER_INPUT:
                    if self.confirm_button.is_clicked(mouse_pos):
                        self.data_collector.set_username(self.text_input.text)
                        self.game_state = GAME_STATE_MENU
                        
                elif self.game_state == GAME_STATE_MENU:
                    # Verifica se algum botão de modo de jogo foi clicado
                    if self.single_mode_button.is_clicked(mouse_pos):
                        self.game_mode = GAME_MODE_SINGLE
                        self.reset_game()
                        self.game_state = GAME_STATE_DISPLAY_TARGET
                    elif self.multiple_mode_button.is_clicked(mouse_pos):
                        self.game_mode = GAME_MODE_MULTIPLE
                        self.reset_game()
                        self.game_state = GAME_STATE_DISPLAY_TARGET
                    elif self.infinite_mode_button.is_clicked(mouse_pos):
                        self.game_mode = GAME_MODE_INFINITE
                        self.reset_game()
                        self.game_state = GAME_STATE_DISPLAY_TARGET
                
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
                                self.data_collector.update_trial_score(self.score)
                                self.data_collector.record_selection(True)
                                if self.game_mode == GAME_MODE_SINGLE:
                                    # No modo único, encontrar o personagem uma vez termina o jogo com sucesso
                                    self.game_state = GAME_STATE_SUCCESS
                                else:
                                    # No modo múltiplo, continuamos até que todas as instâncias sejam encontradas ou clique errado
                                    # Remove o personagem da escada rolante
                                    escalator.characters.remove(clicked_character)
                                    if self.game_mode == GAME_MODE_MULTIPLE and self.score >= self.target_max_spawns:
                                        self.game_state = GAME_STATE_SUCCESS
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
                                self.data_collector.update_trial_score(self.score)  # Registra pontuação final antes de terminar tentativa
                                self.data_collector.record_selection(False)
                                if self.game_mode == GAME_MODE_INFINITE:
                                    # No modo infinito, aplica penalidade de tempo mas continua
                                    self.time_limit -= 3  # Penalidade de 3 segundos
                                else:
                                    # Outros modos ainda terminam com clique errado
                                    self.game_state = GAME_STATE_FAILURE
                            break
        
        # Atualiza estados de hover dos botões
        if self.game_state == GAME_STATE_MENU:
            self.single_mode_button.check_hover(mouse_pos)
            self.multiple_mode_button.check_hover(mouse_pos)
            self.infinite_mode_button.check_hover(mouse_pos)
        elif self.game_state == GAME_STATE_USER_INPUT:
            self.confirm_button.check_hover(mouse_pos)
    
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
        
        # Cria uma nova sessão para cada reinício do jogo para garantir coleta precisa de dados
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
        
        current_time = time.time()
        
        # Manipula transições de estado do jogo
        if self.game_state == GAME_STATE_DISPLAY_TARGET:
            # Muda para estado de jogo após o tempo de exibição
            if current_time - self.target_display_start >= self.display_target_time:
                self.game_state = GAME_STATE_PLAYING
                self.start_time = current_time
        
        # Atualiza todas as escadas rolantes
        for escalator in self.escalators:
            escalator.update()
        
        if self.game_state == GAME_STATE_PLAYING:
            # Verifica se o tempo acabou
            if current_time - self.start_time >= self.time_limit:
                self.game_state = GAME_STATE_FAILURE
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
                elif self.game_mode == GAME_MODE_MULTIPLE:
                    # No modo múltiplo, faz o alvo aparecer várias vezes
                    if self.target_spawn_count < self.target_max_spawns and random.random() < 0.15:
                        # 15% de chance de fazer o alvo aparecer cada vez
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

    def draw_character_traits(self, y_pos):
        # Desenha o texto descrevendo as características do personagem
        head_text = TINY_FONT.render(f"Cabeça: {self.target_traits['head']['name']}", True, (0, 0, 0))
        face_text = TINY_FONT.render(f"Rosto: {self.target_traits['face']['name']}", True, (0, 0, 0))
        body_text = TINY_FONT.render(f"Corpo: {self.target_traits['body']['name']}", True, (0, 0, 0))
        hat_text = TINY_FONT.render(f"Chapéu: {self.target_traits['hat']['name']}", True, (0, 0, 0))
        
        screen.blit(head_text, (WIDTH//2 - 100, y_pos))
        screen.blit(face_text, (WIDTH//2 - 100, y_pos + 20))
        screen.blit(body_text, (WIDTH//2 - 100, y_pos + 40))
        screen.blit(hat_text, (WIDTH//2 - 100, y_pos + 60))

    def draw_menu(self):
        # Desenha a tela do menu
        if self.menu_image:
            # Se a imagem do menu existe, desenha na tela
            screen.blit(self.menu_image, (0, 0))  # Desenha a imagem no canto superior esquerdo
        else:
            # Se a imagem não existe, desenha o menu padrão
            title = TITLE_FONT.render("Jogo da Memória na Escada Rolante", True, (50, 50, 150))
            screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))

            instructions = SMALL_FONT.render("Selecione o Modo de Jogo:", True, (0, 0, 0))
            screen.blit(instructions, (WIDTH//2 - instructions.get_width()//2, HEIGHT//2 - 120))
        
            # Desenha os botões de seleção de modo
            self.single_mode_button.draw(screen)
            self.multiple_mode_button.draw(screen)
            self.infinite_mode_button.draw(screen)
        
            # Desenha as descrições dos modos de jogo
            single_desc = TINY_FONT.render("Encontre o personagem mostrado no início (aparece uma vez)", True, (0, 0, 0))
            multiple_desc = TINY_FONT.render(f"Encontre todas as {self.target_max_spawns} aparições do personagem", True, (0, 0, 0))
            infinite_desc = TINY_FONT.render("Encontre personagens para ganhar mais tempo - jogue até perder!", True, (0, 0, 0))
        
            screen.blit(single_desc, (WIDTH//2 - single_desc.get_width()//2, HEIGHT//2 - 35))
            screen.blit(multiple_desc, (WIDTH//2 - multiple_desc.get_width()//2, HEIGHT//2 + 35))
            screen.blit(infinite_desc, (WIDTH//2 - infinite_desc.get_width()//2, HEIGHT//2 + 105))

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
            
        elif self.game_state == GAME_STATE_DISPLAY_TARGET:
            # Exibe o personagem alvo
            if self.game_mode == GAME_MODE_SINGLE:
                mode_text = "Modo Aparição Única"
            elif self.game_mode == GAME_MODE_MULTIPLE:
                mode_text = "Modo Múltiplas Aparições"
            else:
                mode_text = "Modo Infinito"

            mode_render = SMALL_FONT.render(mode_text, True, (50, 50, 150))
            screen.blit(mode_render, (WIDTH//2 - mode_render.get_width()//2, 20))
            
            text = FONT.render("Lembre-se deste personagem:", True, (0, 0, 0))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//4))
            
            # Desenha o personagem alvo
            self.target_character.draw(screen)
            
            # Desenha a descrição das características do personagem
            self.draw_character_traits(HEIGHT//2 + 50)
            
            # Exibe a contagem regressiva
            time_left = max(0, self.display_target_time - (time.time() - self.target_display_start))
            countdown = FONT.render(f"Iniciando em: {time_left:.1f}", True, (0, 0, 0))
            screen.blit(countdown, (WIDTH//2 - countdown.get_width()//2, HEIGHT*3//4))
            
        elif self.game_state == GAME_STATE_PLAYING:
            # Desenha todas as escadas rolantes
            for escalator in self.escalators:
                escalator.draw(screen)
            
            # Exibe o tempo restante
            time_left = max(0, self.time_limit - (time.time() - self.start_time))
            time_text = SMALL_FONT.render(f"Tempo Restante: {time_left:.1f}s", True, (0, 0, 0))
            screen.blit(time_text, (10, 10))
            
            # Exibe a pontuação
            if self.game_mode == GAME_MODE_SINGLE:
                mode_text = "Encontre uma vez"
            elif self.game_mode == GAME_MODE_MULTIPLE:
                mode_text = f"Encontre {self.target_spawn_count}/{self.target_max_spawns}"
            else:  # Modo infinito
                mode_text = f"+{self.time_bonus}s por acerto"
            
            score_text = SMALL_FONT.render(f"Pontuação: {self.score} - {mode_text}", True, (0, 0, 0))
            screen.blit(score_text, (10, 40))
            
            # Exibe a precisão no modo infinito
            if self.game_mode == GAME_MODE_INFINITE and self.selections_total > 0:
                accuracy = (self.selections_correct / self.selections_total) * 100
                accuracy_text = SMALL_FONT.render(f"Precisão: {accuracy:.1f}%", True, (0, 0, 0))
                screen.blit(accuracy_text, (10, 70))
            
            # No caso do modo múltiplo, mostra um pequeno lembrete de como o personagem se parece
            if self.game_mode != GAME_MODE_SINGLE:
                reminder_text = TINY_FONT.render("Personagem Alvo:", True, (0, 0, 0))
                screen.blit(reminder_text, (10, 100))
                
                # Desenha uma versão pequena do alvo
                mini_character = Character(20, 120, self.target_traits)
                mini_character.size = CHARACTER_SIZE // 2  # Torna menor
                mini_character.draw(screen)
            
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