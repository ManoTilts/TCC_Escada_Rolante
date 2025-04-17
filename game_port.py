import pygame
import random
import sys
import time
import os

# Inicializa o pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 1000, 800
BACKGROUND_COLOR = (200, 200, 200)
ESCALATOR_COLORS = [(100, 100, 100), (120, 120, 120), (140, 140, 140)]
ESCALATOR_SPEEDS = [2, 3, 4]  # Diferentes velocidades para cada escada rolante
ESCALATOR_WIDTH = 120
ESCALATOR_SPACING = 100
ESCALATOR_START_X = 170  # Posição X inicial para a primeira escada rolante

# Propriedades do personagem
CHARACTER_SIZE = 50

# Estado do jogo
GAME_STATE_MENU = 0
GAME_STATE_DISPLAY_TARGET = 1
GAME_STATE_PLAYING = 2
GAME_STATE_SUCCESS = 3
GAME_STATE_FAILURE = 4

# Modos de jogo
GAME_MODE_SINGLE = 0  # O alvo aparece apenas uma vez
GAME_MODE_MULTIPLE = 1  # O alvo aparece várias vezes
GAME_MODE_INFINITE = 2  # Modo infinito com bônus de tempo

# Taxa de spawn de personagens
CHARACTER_SPAWN_RATE = 60  # Quadros entre os spawns de personagens

# Fonte
FONT = pygame.font.SysFont('Arial', 36)
SMALL_FONT = pygame.font.SysFont('Arial', 24)
TINY_FONT = pygame.font.SysFont('Arial', 16)
TITLE_FONT = pygame.font.SysFont('Arial', 48, bold=True)

# Inicializa a tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Memória da Escada Rolante")
clock = pygame.time.Clock()

# Carregar ativos
def load_assets():
    assets = {
        "heads": [],
        "faces": [],
        "bodies": [],
        "hats": []
    }
    
    # Verifica se a pasta de ativos existe, se não, cria imagens de demonstração
    if not os.path.exists("assets"):
        os.makedirs("assets/heads", exist_ok=True)
        os.makedirs("assets/faces", exist_ok=True)
        os.makedirs("assets/bodies", exist_ok=True)
        os.makedirs("assets/hats", exist_ok=True)
        print("Pastas de ativos criadas. Por favor, adicione suas imagens a essas pastas.")
        
        # Cria ativos de amostra se não existirem
        create_sample_assets()
    
    # Carrega cabeças (3 variantes)
    for i in range(1, 4):
        path = f"assets/heads/head{i}.png"
        if os.path.exists(path):
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, (CHARACTER_SIZE, CHARACTER_SIZE))
            assets["heads"].append({"image": img, "name": f"Cabeça {i}"})
    
    # Carrega rostos (15 variantes)
    for i in range(1, 16):
        path = f"assets/faces/face{i}.png"
        if os.path.exists(path):
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, (CHARACTER_SIZE, CHARACTER_SIZE))
            assets["faces"].append({"image": img, "name": f"Rosto {i}"})
    
    # Carrega corpos (2 variantes)
    for i in range(1, 3):
        path = f"assets/bodies/body{i}.png"
        if os.path.exists(path):
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, (CHARACTER_SIZE, CHARACTER_SIZE))
            assets["bodies"].append({"image": img, "name": f"Corpo {i}"})
    
    # Carrega chapéus (10 variantes)
    for i in range(1, 11):
        path = f"assets/hats/hat{i}.png"
        if os.path.exists(path):
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, (CHARACTER_SIZE, CHARACTER_SIZE//2))
            assets["hats"].append({"image": img, "name": f"Chapéu {i}"})
    
    # Se nenhum ativo foi carregado, cria retângulos coloridos como fallback
    if len(assets["heads"]) == 0:
        for i, color in enumerate([(255, 200, 200), (200, 255, 200), (200, 200, 255)]):
            img = pygame.Surface((CHARACTER_SIZE, CHARACTER_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(img, color, (0, 0, CHARACTER_SIZE, CHARACTER_SIZE))
            assets["heads"].append({"image": img, "name": f"Cabeça {i+1}"})
    
    if len(assets["faces"]) == 0:
        for i in range(15):
            img = pygame.Surface((CHARACTER_SIZE, CHARACTER_SIZE), pygame.SRCALPHA)
            # Desenha um rosto simples
            pygame.draw.circle(img, (0, 0, 0), (CHARACTER_SIZE//4, CHARACTER_SIZE//3), 3)
            pygame.draw.circle(img, (0, 0, 0), (CHARACTER_SIZE*3//4, CHARACTER_SIZE//3), 3)
            pygame.draw.arc(img, (0, 0, 0), (CHARACTER_SIZE//4, CHARACTER_SIZE//2, CHARACTER_SIZE//2, CHARACTER_SIZE//3), 0, 3.14, 2)
            assets["faces"].append({"image": img, "name": f"Rosto {i+1}"})
    
    if len(assets["bodies"]) == 0:
        for i, color in enumerate([(255, 0, 0), (0, 0, 255)]):
            img = pygame.Surface((CHARACTER_SIZE, CHARACTER_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(img, color, (0, CHARACTER_SIZE//2, CHARACTER_SIZE, CHARACTER_SIZE//2))
            assets["bodies"].append({"image": img, "name": f"Corpo {i+1}"})
    
    if len(assets["hats"]) == 0:
        for i in range(10):
            img = pygame.Surface((CHARACTER_SIZE, CHARACTER_SIZE//2), pygame.SRCALPHA)
            color = (random.randint(50, 250), random.randint(50, 250), random.randint(50, 250))
            if i % 3 == 0:  # Chapéu alto
                pygame.draw.rect(img, color, (CHARACTER_SIZE//4, CHARACTER_SIZE//4, CHARACTER_SIZE//2, 10))
                pygame.draw.rect(img, color, (CHARACTER_SIZE//3, 0, CHARACTER_SIZE//3, CHARACTER_SIZE//4))
            elif i % 3 == 1:  # Boné
                pygame.draw.rect(img, color, (CHARACTER_SIZE//4, CHARACTER_SIZE//4, CHARACTER_SIZE//2, 10))
                pygame.draw.polygon(img, color, [(CHARACTER_SIZE//4, CHARACTER_SIZE//4), 
                                                (CHARACTER_SIZE*3//4, CHARACTER_SIZE//4), 
                                                (CHARACTER_SIZE//2, 0)])
            else:  # Coroa
                pygame.draw.rect(img, color, (CHARACTER_SIZE//4, CHARACTER_SIZE//4, CHARACTER_SIZE//2, 10))
                pygame.draw.polygon(img, color, [(CHARACTER_SIZE//4, CHARACTER_SIZE//4), 
                                                (CHARACTER_SIZE//3, 0), 
                                                (CHARACTER_SIZE//2, CHARACTER_SIZE//4), 
                                                (CHARACTER_SIZE*2//3, 0), 
                                                (CHARACTER_SIZE*3//4, CHARACTER_SIZE//4)])
            assets["hats"].append({"image": img, "name": f"Chapéu {i+1}"})
    
    return assets

def create_sample_assets():
    """Cria imagens de ativos de amostra para fins de demonstração"""
    # Isso é apenas um espaço reservado - em uma implementação real, você criaria arquivos PNG reais
    print("Ativos de amostra seriam criados aqui em uma implementação completa")
    # Por enquanto, vamos depender dos retângulos coloridos de fallback

# Carregar ativos
CHARACTER_ASSETS = load_assets()

class Character:
    def __init__(self, x, y, traits):
        self.x = x
        self.y = y
        self.traits = traits  # Dicionário de características
        self.size = CHARACTER_SIZE
        self.escalator_index = None  # Qual escada rolante o personagem está
        self.step_position = 0  # Posição no degrau atual (0-1)
        self.current_step = 0  # Qual degrau o personagem está atualmente
    
    def update(self, speed, escalator):
        # O personagem deve se mover com os degraus da escada rolante
        # Calcula a altura do degrau e quantos degraus cabem na tela
        step_height = 20
        total_steps = HEIGHT // step_height
        
        # Atualiza a posição do degrau com base na velocidade da escada rolante
        # Isso cria um efeito de movimento sincronizado
        self.step_position += speed / step_height
        
        # Se já passamos de um degrau, movemos para o próximo
        if self.step_position >= 1:
            self.current_step += 1
            self.step_position -= 1
        
        # Calcula a posição y com base no degrau atual e na posição dentro do degrau
        self.y = (self.current_step * step_height) + (self.step_position * step_height)
        
        # Garante que o personagem fique centralizado na escada rolante
        self.x = escalator.x + (escalator.width - self.size) // 2
    
    def draw(self, screen):
        # Desenha o corpo
        screen.blit(self.traits["body"]["image"], (self.x, self.y))
        
        # Desenha a cabeça
        screen.blit(self.traits["head"]["image"], (self.x, self.y))
        
        # Desenha o rosto
        screen.blit(self.traits["face"]["image"], (self.x, self.y))
        
        # Desenha o chapéu (um pouco acima da cabeça)
        screen.blit(self.traits["hat"]["image"], (self.x, self.y - self.size//4))
    
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
               f"{self.traits['body']['name']}, e {self.traits['hat']['name']}"

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
        # Redefine as combinações disponíveis
        self.available_combinations = self.all_possible_combinations.copy()
        self.created_characters = []
    
    def create_random_character(self, x, y):
        # Cria um personagem aleatório com características únicas
        if not self.available_combinations:
            print("Aviso: Nenhuma combinação única disponível!")
            # Se usamos todas as combinações, regeneramos a lista
            self.available_combinations = self.all_possible_combinations.copy()
        
        # Obtém uma combinação de características aleatória
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
        # Atualiza a animação do degrau
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
            # Ajusta a posição y com base no step_offset para animação
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

class Game:
    def __init__(self):
        self.escalators = []
        self.spawn_counter = 0
        self.running = True
        self.game_state = GAME_STATE_MENU
        self.game_mode = GAME_MODE_SINGLE
        self.target_character = None
        self.target_traits = None
        self.display_target_time = 4  # segundos para exibir o alvo
        self.target_display_start = 0
        self.score = 0
        self.highest_score = 0
        self.time_limit = 30  # 30 segundos para encontrar o personagem
        self.start_time = 0
        self.target_spawn_count = 0  # Quantas vezes o alvo foi gerado
        self.target_max_spawns = 3  # Máximo de vezes que o alvo pode aparecer no modo múltiplo
        self.has_target_spawned = False
        self.target_spawned_time = 0
        self.character_factory = CharacterFactory(CHARACTER_ASSETS)
        self.time_bonus = 5  # Tempo adicionado para cliques corretos no modo infinito
        
        # Cria botões para o menu
        button_width, button_height = 200, 50
        button_x = WIDTH // 2 - button_width // 2
        
        self.single_mode_button = Button(
            button_x, HEIGHT // 2 - 70, 
            button_width, button_height, 
            "Modo de Aparição Única"
        )
        
        self.multiple_mode_button = Button(
            button_x, HEIGHT // 2, 
            button_width, button_height, 
            "Modo de Múltiplas Aparições"
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
        
        # Carrega a imagem de fundo do menu
        self.menu_image = self.load_menu_image()
    
    def load_menu_image(self):
        if os.path.exists("assets/misc/menu.png"):
            try:
                return pygame.image.load("assets/misc/menu.png")
            except pygame.error:
                print("Imagem do menu encontrada, mas não pôde ser carregada, usando o menu padrão.")
                return False
        else:
            print("Imagem do menu não encontrada, usando o menu padrão.")
            return False
    
    def select_new_target(self):
        # Cria um personagem alvo (não colocado em nenhuma escada rolante ainda)
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == GAME_STATE_MENU:
                    # Verifica se algum botão do modo de jogo foi clicado
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
                                        # Adiciona bônus de tempo para o modo infinito
                                        self.time_limit += self.time_bonus
                                        # Gera um novo alvo imediatamente para manter o jogo em andamento
                                        self.has_target_spawned = False
                            else:
                                # Clique errado no personagem
                                self.game_state = GAME_STATE_FAILURE
                            break
        
        # Atualiza os estados de hover dos botões
        if self.game_state == GAME_STATE_MENU:
            self.single_mode_button.check_hover(mouse_pos)
            self.multiple_mode_button.check_hover(mouse_pos)
            self.infinite_mode_button.check_hover(mouse_pos)
    
    def reset_game(self):
        # Redefine o estado do jogo
        for escalator in self.escalators:
            escalator.characters = []
        self.character_factory.reset()
        self.select_new_target()
        self.spawn_counter = 0
        self.start_time = 0
        self.has_target_spawned = False
        self.target_spawn_count = 0
        self.score = 0
    
    def spawn_character(self, target=False):
        # Escolhe uma escada rolante aleatória
        escalator = random.choice(self.escalators)
        char_x = escalator.x + (escalator.width - CHARACTER_SIZE) // 2
        char_y = 0 - CHARACTER_SIZE  # Começa acima da tela
        
        if target:
            # Cria o personagem alvo com as mesmas características
            character = Character(char_x, char_y, self.target_traits)
            self.has_target_spawned = True
            self.target_spawned_time = time.time()
            self.target_spawn_count += 1
        else:
            # Cria um personagem aleatório (garante que não seja o mesmo que o alvo)
            while True:
                character = self.character_factory.create_random_character(char_x, char_y)
                if character.traits != self.target_traits:
                    break
        
        escalator.add_character(character)
    
    def update(self):
        current_time = time.time()
        
        # Lida com transições de estado do jogo
        if self.game_state == GAME_STATE_DISPLAY_TARGET:
            # Muda para o estado de jogo após o tempo de exibição
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
                # Atualiza a maior pontuação se necessário
                if self.score > self.highest_score:
                    self.highest_score = self.score
            
            # Gera novos personagens
            self.spawn_counter += 1
            if self.spawn_counter >= CHARACTER_SPAWN_RATE:
                self.spawn_counter = 0
                
                # Lida com o spawn do personagem alvo dependendo do modo de jogo
                if self.game_mode == GAME_MODE_SINGLE:
                    # No modo único, gera o alvo apenas uma vez
                    if not self.has_target_spawned and current_time - self.start_time >= 5:
                        self.spawn_character(target=True)
                    else:
                        # Sempre gera um personagem aleatório que não é o alvo
                        self.spawn_character(target=False)
                elif self.game_mode == GAME_MODE_MULTIPLE:
                    # No modo múltiplo, gera o alvo várias vezes
                    if self.target_spawn_count < self.target_max_spawns and random.random() < 0.15:
                        # 15% de chance de gerar o alvo a cada vez
                        self.spawn_character(target=True)
                    else:
                        # Gera um personagem aleatório que não é o alvo
                        self.spawn_character(target=False)
                elif self.game_mode == GAME_MODE_INFINITE:
                    # No modo infinito, sempre garante que haja um alvo
                    if not self.has_target_spawned and random.random() < 0.2:
                        # 20% de chance de gerar o alvo quando não há um
                        self.spawn_character(target=True)
                    else:
                        # Gera um personagem aleatório que não é o alvo
                        self.spawn_character(target=False)
    
    def draw_character_traits(self, y_pos):
        # Desenha texto descrevendo as características do personagem
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
            title = TITLE_FONT.render("Jogo da Memória da Escada Rolante", True, (50, 50, 150))
            screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))

            instructions = SMALL_FONT.render("Selecione o Modo de Jogo:", True, (0, 0, 0))
            screen.blit(instructions, (WIDTH//2 - instructions.get_width()//2, HEIGHT//2 - 120))
        
            # Desenha os botões de seleção do modo de jogo
            self.single_mode_button.draw(screen)
            self.multiple_mode_button.draw(screen)
            self.infinite_mode_button.draw(screen)
        
            # Desenha as descrições dos modos de jogo
            single_desc = TINY_FONT.render("Encontre o personagem que aparece apenas 1 vez", True, (0, 0, 0))
            multiple_desc = TINY_FONT.render(f"Encontre todas as {self.target_max_spawns} aparições do personagem", True, (0, 0, 0))
            infinite_desc = TINY_FONT.render("Encontre personagens para ganhar mais tempo - jogue até perder!", True, (0, 0, 0))
        
            screen.blit(single_desc, (WIDTH//2 - single_desc.get_width()//2, HEIGHT//2 - 35))
            screen.blit(multiple_desc, (WIDTH//2 - multiple_desc.get_width()//2, HEIGHT//2 + 35))
            screen.blit(infinite_desc, (WIDTH//2 - infinite_desc.get_width()//2, HEIGHT//2 + 105))
   
    def draw(self):
        # Limpa a tela
        screen.fill(BACKGROUND_COLOR)
        
        if self.game_state == GAME_STATE_MENU:
            self.draw_menu()
            
        elif self.game_state == GAME_STATE_DISPLAY_TARGET:
            # Exibe o personagem alvo
            if self.game_mode == GAME_MODE_SINGLE:
                mode_text = "Modo de Aparição Única"
            elif self.game_mode == GAME_MODE_MULTIPLE:
                mode_text = "Modo de Múltiplas Aparições"
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
                mode_text = "Encontrar uma vez"
            elif self.game_mode == GAME_MODE_MULTIPLE:
                mode_text = f"Encontrar {self.target_spawn_count}/{self.target_max_spawns}"
            else:  # Modo infinito
                mode_text = f"+{self.time_bonus}s por encontrar"
            score_text = SMALL_FONT.render(f"Pontuação: {self.score} - {mode_text}", True, (0, 0, 0))
            screen.blit(score_text, (10, 40))
            
            # No caso do modo múltiplo, mostra um pequeno lembrete de como é o personagem
            if self.game_mode != GAME_MODE_SINGLE:
                reminder_text = TINY_FONT.render("Personagem Alvo:", True, (0, 0, 0))
                screen.blit(reminder_text, (10, 70))
                
                # Desenha uma versão pequena do alvo
                mini_character = Character(20, 90, self.target_traits)
                mini_character.size = CHARACTER_SIZE // 2  # Faz menor
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
            
            # Renderiza a maior pontuação como uma superfície de texto
            high_score_text = SMALL_FONT.render(f"Maior Pontuação: {self.highest_score}", True, (0, 0, 0))
            screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//2 + 30))
            
            restart = SMALL_FONT.render("Pressione 'R' para jogar novamente ou ESC para o menu", True, (0, 0, 0))
            screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 70))
        
        # Atualiza a exibição
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)  # 60 FPS

# Função principal
def main():
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()