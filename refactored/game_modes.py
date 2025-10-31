"""
Lógica específica para cada modo de jogo
"""
import random
import math
import pygame
from config import *


class ArrowMode:
    """Lógica específica do modo seta"""
    def __init__(self):
        self.arrow_angle = 0
        self.arrow_rotation_speed = 4.0
        self.target_quadrant = 0
        self.arrow_color = (255, 255, 255)
        self.arrow_in_target_zone = False
        self.last_quadrant_pointed = -1
        self.select_new_target()
    
    def select_new_target(self):
        """Seleciona um novo quadrante alvo"""
        self.target_quadrant = random.randint(0, 3)
        self.arrow_color = QUADRANT_COLORS[self.target_quadrant]
        self.arrow_rotation_speed = random.uniform(2.0, 8.0)
    
    def update(self):
        """Atualiza a rotação da seta"""
        self.arrow_angle += self.arrow_rotation_speed
        if self.arrow_angle >= 360:
            self.arrow_angle = 0
        
        pointed_quadrant = self.get_arrow_pointed_quadrant()
        self.arrow_in_target_zone = (pointed_quadrant == self.target_quadrant 
                                     and pointed_quadrant != -1)
        self.last_quadrant_pointed = pointed_quadrant
    
    def get_arrow_pointed_quadrant(self):
        """Determina para qual quadrante a seta está apontando"""
        angle = self.arrow_angle % 360
        
        if 270 <= angle or angle < 90:
            if 270 <= angle or angle < 0:
                return 1  # Superior direito
            else:
                return 3  # Inferior direito
        elif 90 <= angle < 270:
            if 180 <= angle < 270:
                return 0  # Superior esquerdo
            else:
                return 2  # Inferior esquerdo
        else:
            return -1
    
    def get_clicked_quadrant(self, mouse_pos):
        """Determina qual quadrante foi clicado"""
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
    
    def draw(self, screen):
        """Desenha a interface do modo seta"""
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        
        # Desenha os quadrantes coloridos
        for i in range(4):
            quadrant_color = QUADRANT_COLORS[i]
            
            if i == self.target_quadrant and self.arrow_in_target_zone:
                bright_color = tuple(min(255, c + 50) for c in quadrant_color)
                quadrant_color = bright_color
            elif i == self.target_quadrant:
                dark_color = tuple(max(50, c - 30) for c in quadrant_color)
                quadrant_color = dark_color
            
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
        self.draw_arrow(screen, center_x, center_y)
    
    def draw_arrow(self, screen, center_x, center_y):
        """Desenha a seta girando"""
        arrow_length = 80
        angle_rad = math.radians(self.arrow_angle)
        
        tip_x = center_x + arrow_length * math.cos(angle_rad)
        tip_y = center_y + arrow_length * math.sin(angle_rad)
        
        base_angle1 = angle_rad + math.radians(150)
        base_angle2 = angle_rad + math.radians(210)
        
        base1_x = center_x + (arrow_length - 30) * math.cos(base_angle1)
        base1_y = center_y + (arrow_length - 30) * math.sin(base_angle1)
        
        base2_x = center_x + (arrow_length - 30) * math.cos(base_angle2)
        base2_y = center_y + (arrow_length - 30) * math.sin(base_angle2)
        
        arrow_points = [(tip_x, tip_y), (base1_x, base1_y), (base2_x, base2_y)]
        
        shadow_points = [(p[0] + 2, p[1] + 2) for p in arrow_points]
        pygame.draw.polygon(screen, GAME_BLACK, shadow_points)
        
        pygame.draw.polygon(screen, self.arrow_color, arrow_points)
        pygame.draw.polygon(screen, GAME_BLACK, arrow_points, 3)
        
        pygame.draw.circle(screen, GAME_BLACK, (center_x, center_y), 15)
        pygame.draw.circle(screen, GAME_WHITE, (center_x, center_y), 12)


class CharacterMode:
    """Lógica base para modos que usam personagens"""
    def __init__(self, character_factory):
        self.character_factory = character_factory
        self.target_character = None
        self.target_traits = None
        self.has_target_spawned = False
        self.target_spawn_count = 0
        self.target_spawned_time = 0
    
    def select_new_target(self, x, y):
        """Cria um novo personagem alvo"""
        self.target_character = self.character_factory.create_random_character(x, y)
        self.target_traits = self.target_character.traits
        self.has_target_spawned = False
        self.target_spawn_count = 0
    
    def spawn_character(self, escalator, target=False):
        """Gera um personagem na escada"""
        from characters import Character
        char_x = escalator.x + (escalator.width - CHARACTER_SIZE) // 2
        char_y = 0 - CHARACTER_SIZE
        
        if target:
            character = Character(char_x, char_y, self.target_traits)
            self.has_target_spawned = True
            self.target_spawned_time = 0  # será definido externamente
            self.target_spawn_count += 1
        else:
            while True:
                character = self.character_factory.create_random_character(char_x, char_y)
                if character.traits != self.target_traits:
                    break
        
        escalator.add_character(character)
        return character
