"""
Classes relacionadas aos personagens do jogo
"""
import pygame
import random
import os
from config import CHARACTER_SIZE, HEIGHT

def load_assets():
    """Carrega todos os assets visuais dos personagens"""
    assets = {
        'bodies': [],
        'faces': [],
        'hats': [],
        'heads': []
    }
    
    segment_size = CHARACTER_SIZE // 3
    
    # Carrega corpos (3 arquivos possíveis)
    try:
        for i in range(1, 4):
            path = f"assets/bodies/bodie{i}.png"
            if os.path.exists(path):
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (CHARACTER_SIZE, segment_size))
                assets["bodies"].append({"image": img, "name": f"Corpo {i}"})
    except Exception as e:
        print(f"Erro ao carregar corpos: {e}")
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
                img = pygame.transform.scale(img, (CHARACTER_SIZE, segment_size))
                assets["faces"].append({"image": img, "name": f"Rosto {i}"})
    except Exception as e:
        print(f"Erro ao carregar rostos: {e}")
        for i in range(15):
            img = pygame.Surface((CHARACTER_SIZE, segment_size), pygame.SRCALPHA)
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
                img = pygame.transform.scale(img, (CHARACTER_SIZE, segment_size))
                assets["hats"].append({"image": img, "name": f"Chapéu {i}"})
    except Exception as e:
        print(f"Erro ao carregar chapéus: {e}")
        for i in range(10):
            img = pygame.Surface((CHARACTER_SIZE, segment_size), pygame.SRCALPHA)
            color = (random.randint(50, 250), random.randint(50, 250), random.randint(50, 250))
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
                img = pygame.transform.scale(img, (CHARACTER_SIZE, segment_size))
                assets["heads"].append({"image": img, "name": f"Cabeça {i}"})
    except Exception as e:
        print(f"Erro ao carregar cabeças: {e}")
        for i, color in enumerate([(255, 200, 200), (200, 255, 200), (200, 200, 255)]):
            img = pygame.Surface((CHARACTER_SIZE, segment_size), pygame.SRCALPHA)
            pygame.draw.rect(img, color, (0, 0, CHARACTER_SIZE, segment_size))
            assets["heads"].append({"image": img, "name": f"Cabeça {i+1}"})

    return assets


class Character:
    """Representa um personagem no jogo"""
    def __init__(self, x, y, traits):
        self.x = x
        self.y = y
        self.traits = traits
        self.size = CHARACTER_SIZE
        self.escalator_index = None
        self.step_position = 0
        self.current_step = 0
    
    def update(self, speed, escalator):
        """Atualiza a posição do personagem na escada"""
        step_height = 20
        self.step_position += speed / step_height
        
        if self.step_position >= 1:
            self.current_step += 1
            self.step_position -= 1
        
        self.y = (self.current_step * step_height) + (self.step_position * step_height)
        self.x = escalator.x + (escalator.width - self.size) // 2
    
    def draw(self, screen):
        """Desenha o personagem na tela"""
        segment_height = self.size // 3
        
        screen.blit(self.traits["body"]["image"], 
                    (self.x, self.y + segment_height * 2))
        screen.blit(self.traits["head"]["image"], 
                    (self.x, self.y + segment_height))
        screen.blit(self.traits["face"]["image"], 
                    (self.x, self.y + segment_height))
        screen.blit(self.traits["hat"]["image"], 
                    (self.x, self.y))
    
    def is_clicked(self, mouse_pos):
        """Verifica se o personagem foi clicado"""
        mx, my = mouse_pos
        return (self.x <= mx <= self.x + self.size and 
                self.y <= my <= self.y + self.size)


class CharacterFactory:
    """Fábrica para criar personagens aleatórios"""
    def __init__(self, assets):
        self.assets = assets
        self.used_combinations = set()
    
    def create_random_character(self, x, y):
        """Cria um personagem com características aleatórias"""
        traits = {
            "body": random.choice(self.assets["bodies"]),
            "face": random.choice(self.assets["faces"]),
            "head": random.choice(self.assets["heads"]),
            "hat": random.choice(self.assets["hats"])
        }
        
        combination = (traits["body"]["name"], traits["face"]["name"],
                      traits["head"]["name"], traits["hat"]["name"])
        self.used_combinations.add(combination)
        
        return Character(x, y, traits)
    
    def reset(self):
        """Reseta as combinações usadas"""
        self.used_combinations.clear()
