"""
Componentes de UI do jogo (botões, inputs de texto, etc)
"""
import pygame
from config import BUTTON_FONT, SMALL_FONT


class Button:
    """Botão clicável com efeito de hover"""
    def __init__(self, x, y, width, height, text, color=None, hover_color=None):
        if color is None:
            color = (50, 100, 180)
        if hover_color is None:
            hover_color = (70, 130, 200)
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = BUTTON_FONT
    
    def draw(self, screen):
        """Desenha o botão na tela"""
        if self.is_hovered:
            button_color = (70, 130, 200)
            border_color = (255, 255, 255)
            text_color = (255, 255, 255)
        else:
            button_color = (50, 100, 180)
            border_color = (200, 200, 200)
            text_color = (255, 255, 255)
        
        pygame.draw.rect(screen, button_color, self.rect, border_radius=8)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=8)
        
        if self.rect.height > 10:
            light_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2, 
                                    self.rect.width - 4, 2)
            pygame.draw.rect(screen, (255, 255, 255, 60), light_rect, border_radius=6)
        
        text_shadow = self.font.render(self.text, True, (0, 0, 0, 120))
        shadow_rect = text_shadow.get_rect(center=(self.rect.centerx + 1, 
                                                   self.rect.centery + 1))
        screen.blit(text_shadow, shadow_rect)
        
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def check_hover(self, mouse_pos):
        """Verifica se o mouse está sobre o botão"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self, mouse_pos):
        """Verifica se o botão foi clicado"""
        return self.rect.collidepoint(mouse_pos)


class TextInput:
    """Campo de entrada de texto"""
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
        self.cursor_blink_rate = 0.5
    
    def handle_event(self, event):
        """Processa eventos de teclado"""
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.unicode.isprintable():
                        self.text += event.unicode
        return None
    
    def update(self):
        """Atualiza o cursor piscando"""
        self.cursor_timer += 1/60
        if self.cursor_timer >= self.cursor_blink_rate:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    
    def draw(self, screen):
        """Desenha o campo de texto na tela"""
        pygame.draw.rect(screen, (255, 255, 255), self.rect, border_radius=8)
        
        border_color = (70, 130, 200) if self.active else (150, 150, 150)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=8)
        
        if self.text:
            text_surf = self.font.render(self.text, True, (50, 50, 50))
        else:
            text_surf = self.font.render(self.placeholder, True, (150, 150, 150))
        
        text_rect = text_surf.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        screen.blit(text_surf, text_rect)
        
        if self.active and self.cursor_visible and len(self.text) < 30:
            cursor_x = text_rect.right + 2 if self.text else self.rect.x + 5
            pygame.draw.line(screen, self.color, 
                           (cursor_x, self.rect.y + 5), 
                           (cursor_x, self.rect.bottom - 5), 2)


class Escalator:
    """Escada rolante que contém personagens"""
    def __init__(self, x, width, speed, color):
        self.x = x
        self.width = width
        self.speed = speed
        self.color = color
        self.characters = []
        self.step_offset = 0
    
    def add_character(self, character):
        """Adiciona um personagem à escada"""
        from config import ESCALATOR_SPEEDS
        character.escalator_index = ESCALATOR_SPEEDS.index(self.speed)
        character.current_step = -3
        character.step_position = 0
        self.characters.append(character)
    
    def update(self):
        """Atualiza a escada e seus personagens"""
        from config import HEIGHT
        self.step_offset = (self.step_offset + self.speed) % 20
        
        for character in self.characters[:]:
            character.update(self.speed, self)
            if character.y > HEIGHT:
                self.characters.remove(character)
    
    def draw(self, screen):
        """Desenha a escada e seus personagens"""
        from config import HEIGHT
        pygame.draw.rect(screen, self.color, (self.x, 0, self.width, HEIGHT))
        
        step_height = 20
        for y in range(0, HEIGHT + step_height, step_height):
            adjusted_y = (y + self.step_offset) % (HEIGHT + step_height)
            pygame.draw.line(screen, (50, 50, 50), 
                           (self.x, adjusted_y), 
                           (self.x + self.width, adjusted_y), 2)
        
        for character in self.characters:
            character.draw(screen)
    
    def check_character_click(self, mouse_pos):
        """Verifica se algum personagem foi clicado"""
        for character in self.characters:
            if character.is_clicked(mouse_pos):
                return character
        return None
