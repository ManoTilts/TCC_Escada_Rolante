"""
Memory Escalator - Jogo da Memória na Escada Rolante
Arquivo principal refatorado
"""
import pygame
import sys
import time
import random
import os

# Adiciona o diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importa módulos do jogo
from refactored.config import *
from refactored.characters import load_assets, Character, CharacterFactory
from refactored.ui_components import Button, TextInput, Escalator
from refactored.data_collector import GameDataCollector
from refactored.highscore_manager import HighscoreManager
from refactored.game_modes import ArrowMode, CharacterMode
from refactored import rendering


class Game:
    """Classe principal do jogo"""
    def __init__(self):
        self.running = True
        self.game_state = GAME_STATE_MENU
        self.game_mode = GAME_MODE_SINGLE
        
        # Sistemas do jogo
        self.data_collector = GameDataCollector()
        self.highscore_manager = HighscoreManager()
        
        # Carrega assets e cria fábrica de personagens
        self.character_assets = load_assets()
        self.character_factory = CharacterFactory(self.character_assets)
        
        # Modos de jogo
        self.arrow_mode = ArrowMode()
        self.character_mode = CharacterMode(self.character_factory)
        
        # Variáveis de jogo
        self.score = 0
        self.highest_score = 0
        self.last_score = 0
        self.is_new_highscore = False
        self.player_name = ""
        
        # Variáveis de tempo
        self.time_limit = 30
        self.start_time = 0
        self.display_target_time = 4
        self.target_display_start = 0
        self.is_first_target = True
        self.time_bonus = 5
        
        # Variáveis de spawn
        self.spawn_counter = 0
        
        # Rastreamento de seleção
        self.selections_total = 0
        self.selections_correct = 0
        
        # Cria escadas rolantes
        self.escalators = []
        for i in range(3):
            x = ESCALATOR_START_X + i * (ESCALATOR_WIDTH + ESCALATOR_SPACING)
            escalator = Escalator(x, ESCALATOR_WIDTH, ESCALATOR_SPEEDS[i], ESCALATOR_COLORS[i])
            self.escalators.append(escalator)
        
        # Cria botões e inputs
        self._create_ui_elements()
    
    def _create_ui_elements(self):
        """Cria todos os elementos de UI"""
        button_width, button_height = 280, 60
        button_x = WIDTH // 2 - button_width // 2
        
        # Botões do menu
        self.single_mode_button = Button(
            button_x, HEIGHT // 2 - 70, button_width, button_height, "Modo Aparição Única")
        self.alternating_mode_button = Button(
            button_x, HEIGHT // 2, button_width, button_height, "Modo Alternado")
        self.infinite_mode_button = Button(
            button_x, HEIGHT // 2 + 70, button_width, button_height, "Modo Infinito")
        self.arrow_mode_button = Button(
            button_x, HEIGHT // 2 + 140, button_width, button_height, "Modo Seta Colorida")
        self.instructions_button = Button(
            button_x, HEIGHT // 2 + 210, button_width, button_height, "Como Jogar")
        self.highscore_button = Button(
            button_x, HEIGHT // 2 + 280, button_width, button_height, "Melhores Pontuações")
        
        # Botão voltar
        self.back_button = Button(50, HEIGHT - 100, 160, 50, "Voltar")
        
        # Inputs de texto
        self.highscore_input = TextInput(
            WIDTH//2 - 200, HEIGHT//2 + 50, 400, 50, 
            placeholder="Digite seu nome para o ranking")
        self.highscore_confirm_button = Button(
            WIDTH//2 - 100, HEIGHT//2 + 120, 200, 50, "Salvar")
    
    def reset_game(self):
        """Reinicia o estado do jogo"""
        for escalator in self.escalators:
            escalator.characters = []
        
        self.character_factory.reset()
        self.spawn_counter = 0
        self.start_time = 0
        self.score = 0
        self.selections_total = 0
        self.selections_correct = 0
        self.is_first_target = True
        
        if self.game_mode == GAME_MODE_ARROW:
            self.arrow_mode.select_new_target()
            self.arrow_mode.arrow_angle = 0
            self.arrow_mode.arrow_in_target_zone = False
            self.arrow_mode.last_quadrant_pointed = -1
            self.time_limit = 90
            self.start_time = time.time()
        else:
            # Cria o personagem alvo posicionado no centro para exibição
            self.character_mode.select_new_target(
                WIDTH//2 - CHARACTER_SIZE//2, HEIGHT//2 - CHARACTER_SIZE//2)
            self.time_limit = 30
            # Inicia o contador de exibição do alvo
            self.target_display_start = time.time()
        
        self.data_collector.create_new_session(self.game_mode)
        self.data_collector.start_new_trial(self.game_mode)
    
    def handle_events(self):
        """Processa eventos do jogo"""
        mouse_pos = pygame.mouse.get_pos()
        self.data_collector.record_mouse_position(mouse_pos, self.game_state)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mousedown(mouse_pos)
        
        # Atualiza estados de hover
        self._update_button_hovers(mouse_pos)
    
    def _handle_keydown(self, event):
        """Processa teclas pressionadas"""
        if event.key == pygame.K_ESCAPE:
            if self.game_state == GAME_STATE_MENU:
                self.running = False
            else:
                self.game_state = GAME_STATE_MENU
        
        elif event.key == pygame.K_r and (self.game_state == GAME_STATE_SUCCESS or 
                                         self.game_state == GAME_STATE_FAILURE):
            self.reset_game()
            self.game_state = GAME_STATE_DISPLAY_TARGET
        
        # Manipula entrada de texto
        if self.game_state == GAME_STATE_NAME_INPUT:
            result = self.highscore_input.handle_event(event)
            if result is not None:
                self.highscore_manager.add_highscore(result, self.last_score, self.game_mode)
                self.data_collector.set_username(result if result else "Anônimo")
                self.game_state = GAME_STATE_MENU
    
    def _handle_mousedown(self, mouse_pos):
        """Processa cliques do mouse"""
        if self.game_state == GAME_STATE_MENU:
            self._handle_menu_clicks(mouse_pos)
        
        elif self.game_state == GAME_STATE_PLAYING:
            self._handle_playing_clicks(mouse_pos)
        
        elif self.game_state == GAME_STATE_INSTRUCTIONS or self.game_state == GAME_STATE_HIGHSCORE:
            if self.back_button.is_clicked(mouse_pos):
                self.game_state = GAME_STATE_MENU
        
        elif self.game_state == GAME_STATE_NAME_INPUT:
            if self.highscore_confirm_button.is_clicked(mouse_pos):
                name = self.highscore_input.text.strip() if self.highscore_input.text else ""
                self.highscore_manager.add_highscore(name, self.last_score, self.game_mode)
                self.data_collector.set_username(name if name else "Anônimo")
                self.game_state = GAME_STATE_MENU
    
    def _handle_menu_clicks(self, mouse_pos):
        """Processa cliques no menu"""
        if self.single_mode_button.is_clicked(mouse_pos):
            self.game_mode = GAME_MODE_SINGLE
            self.reset_game()
            self.game_state = GAME_STATE_DISPLAY_TARGET
        
        elif self.alternating_mode_button.is_clicked(mouse_pos):
            self.game_mode = GAME_MODE_ALTERNATING
            self.reset_game()
            self.game_state = GAME_STATE_DISPLAY_TARGET
        
        elif self.infinite_mode_button.is_clicked(mouse_pos):
            self.game_mode = GAME_MODE_INFINITE
            self.reset_game()
            self.game_state = GAME_STATE_DISPLAY_TARGET
        
        elif self.arrow_mode_button.is_clicked(mouse_pos):
            self.game_mode = GAME_MODE_ARROW
            self.reset_game()
            self.game_state = GAME_STATE_PLAYING
        
        elif self.instructions_button.is_clicked(mouse_pos):
            self.game_state = GAME_STATE_INSTRUCTIONS
        
        elif self.highscore_button.is_clicked(mouse_pos):
            self.game_state = GAME_STATE_HIGHSCORE
    
    def _handle_playing_clicks(self, mouse_pos):
        """Processa cliques durante o jogo"""
        if self.game_mode == GAME_MODE_ARROW:
            self._handle_arrow_mode_click(mouse_pos)
        else:
            self._handle_character_mode_click(mouse_pos)
    
    def _handle_arrow_mode_click(self, mouse_pos):
        """Processa cliques no modo seta"""
        clicked_quadrant = self.arrow_mode.get_clicked_quadrant(mouse_pos)
        if clicked_quadrant is not None:
            self.selections_total += 1
            
            if (clicked_quadrant == self.arrow_mode.target_quadrant and 
                self.arrow_mode.arrow_in_target_zone):
                # Acerto!
                self.score += 1
                self.selections_correct += 1
                self.data_collector.record_click(mouse_pos, True)
                self.data_collector.update_trial_score(self.score)
                self.data_collector.record_arrow_selection(
                    True, clicked_quadrant, self.arrow_mode.target_quadrant, 
                    self.arrow_mode.arrow_angle, self.arrow_mode.arrow_rotation_speed, 
                    self.arrow_mode.arrow_in_target_zone)
                
                self.arrow_mode.select_new_target()
                self.data_collector.start_new_trial(self.game_mode)
            else:
                # Erro
                self.data_collector.record_click(mouse_pos, False)
                self.data_collector.update_trial_score(self.score)
                self.data_collector.record_arrow_selection(
                    False, clicked_quadrant, self.arrow_mode.target_quadrant, 
                    self.arrow_mode.arrow_angle, self.arrow_mode.arrow_rotation_speed, 
                    self.arrow_mode.arrow_in_target_zone)
    
    def _handle_character_mode_click(self, mouse_pos):
        """Processa cliques nos modos com personagens"""
        for escalator in self.escalators:
            clicked_character = escalator.check_character_click(mouse_pos)
            if clicked_character:
                if clicked_character.traits == self.character_mode.target_traits:
                    # Personagem correto!
                    self.score += 1
                    self.selections_total += 1
                    self.selections_correct += 1
                    self.data_collector.record_click(mouse_pos, True)
                    self.data_collector.update_trial_score(self.score)
                    self.data_collector.record_selection(True)
                    
                    if self.game_mode == GAME_MODE_SINGLE:
                        self.last_score = self.score
                        self.game_state = GAME_STATE_NAME_INPUT
                    else:
                        escalator.characters.remove(clicked_character)
                        
                        if self.game_mode == GAME_MODE_ALTERNATING:
                            self.character_mode.select_new_target(
                                WIDTH//2 - CHARACTER_SIZE//2, HEIGHT//2 - CHARACTER_SIZE//2)
                            self.character_mode.has_target_spawned = False
                            self.is_first_target = False
                            self.game_state = GAME_STATE_DISPLAY_TARGET
                            self.target_display_start = time.time()
                            self.data_collector.start_new_trial(self.game_mode)
                        
                        elif self.game_mode == GAME_MODE_INFINITE:
                            self.time_limit += self.time_bonus
                            self.character_mode.has_target_spawned = False
                            self.data_collector.start_new_trial(self.game_mode)
                else:
                    # Personagem errado
                    self.selections_total += 1
                    self.data_collector.record_click(mouse_pos, False)
                    self.data_collector.update_trial_score(self.score)
                    self.data_collector.record_selection(False)
                    
                    if self.game_mode == GAME_MODE_INFINITE:
                        self.time_limit -= 3
                    else:
                        self.last_score = self.score
                        self.game_state = GAME_STATE_NAME_INPUT
                break
    
    def _update_button_hovers(self, mouse_pos):
        """Atualiza o estado de hover dos botões"""
        if self.game_state == GAME_STATE_MENU:
            self.single_mode_button.check_hover(mouse_pos)
            self.alternating_mode_button.check_hover(mouse_pos)
            self.infinite_mode_button.check_hover(mouse_pos)
            self.arrow_mode_button.check_hover(mouse_pos)
            self.instructions_button.check_hover(mouse_pos)
            self.highscore_button.check_hover(mouse_pos)
        
        elif self.game_state in [GAME_STATE_INSTRUCTIONS, GAME_STATE_HIGHSCORE]:
            self.back_button.check_hover(mouse_pos)
        
        elif self.game_state == GAME_STATE_NAME_INPUT:
            self.highscore_confirm_button.check_hover(mouse_pos)
    
    def update(self):
        """Atualiza o estado do jogo"""
        if self.game_state == GAME_STATE_NAME_INPUT:
            self.highscore_input.update()
        
        current_time = time.time()
        
        # Transição de DISPLAY_TARGET para PLAYING
        if self.game_state == GAME_STATE_DISPLAY_TARGET:
            display_time = 2.5 if (self.game_mode == GAME_MODE_ALTERNATING and 
                                  not self.is_first_target) else self.display_target_time
            
            if current_time - self.target_display_start >= display_time:
                self.game_state = GAME_STATE_PLAYING
                if self.start_time == 0:
                    self.start_time = current_time
        
        # Atualiza escadas rolantes
        for escalator in self.escalators:
            escalator.update()
        
        if self.game_state == GAME_STATE_PLAYING:
            self._update_playing_state(current_time)
    
    def _update_playing_state(self, current_time):
        """Atualiza o estado durante o jogo"""
        # Modo seta
        if self.game_mode == GAME_MODE_ARROW:
            if self.start_time == 0:
                self.start_time = current_time
            self.arrow_mode.update()
        
        # Verifica timeout
        if current_time - self.start_time >= self.time_limit:
            self.last_score = self.score
            self.game_state = GAME_STATE_NAME_INPUT
            if self.score > self.highest_score:
                self.highest_score = self.score
        
        # Spawn de personagens (apenas modos com personagens)
        if self.game_mode != GAME_MODE_ARROW:
            self._spawn_characters(current_time)
    
    def _spawn_characters(self, current_time):
        """Controla o spawn de personagens"""
        self.spawn_counter += 1
        if self.spawn_counter >= CHARACTER_SPAWN_RATE:
            self.spawn_counter = 0
            
            escalator = random.choice(self.escalators)
            
            if self.game_mode == GAME_MODE_SINGLE:
                if not self.character_mode.has_target_spawned and current_time - self.start_time >= 5:
                    character = self.character_mode.spawn_character(escalator, target=True)
                    self.data_collector.record_target_spawn(self.character_mode.target_traits)
                else:
                    self.character_mode.spawn_character(escalator, target=False)
            
            elif self.game_mode in [GAME_MODE_ALTERNATING, GAME_MODE_INFINITE]:
                if not self.character_mode.has_target_spawned and random.random() < 0.2:
                    character = self.character_mode.spawn_character(escalator, target=True)
                    self.data_collector.record_target_spawn(self.character_mode.target_traits)
                else:
                    self.character_mode.spawn_character(escalator, target=False)
    
    def draw(self):
        """Desenha o jogo na tela"""
        screen.fill(BACKGROUND_COLOR)
        
        if self.game_state == GAME_STATE_MENU:
            buttons = [self.single_mode_button, self.alternating_mode_button,
                      self.infinite_mode_button, self.arrow_mode_button,
                      self.instructions_button, self.highscore_button]
            rendering.draw_menu(screen, buttons)
        
        elif self.game_state == GAME_STATE_DISPLAY_TARGET:
            rendering.draw_display_target(
                screen, self.character_mode.target_character, self.game_mode,
                2.5 if (self.game_mode == GAME_MODE_ALTERNATING and not self.is_first_target) 
                    else self.display_target_time,
                self.target_display_start, self.is_first_target, self.score)
        
        elif self.game_state == GAME_STATE_PLAYING:
            if self.game_mode == GAME_MODE_ARROW:
                self.arrow_mode.draw(screen)
                # Info do jogo
                current_time = time.time()
                time_left = max(0, self.time_limit - (current_time - self.start_time))
                
                score_text = FONT.render(f"Pontuação: {self.score}", True, GAME_WHITE)
                screen.blit(score_text, (10, 10))
                
                time_text = FONT.render(f"Tempo: {time_left:.1f}s", True, GAME_WHITE)
                screen.blit(time_text, (10, 50))
                
                speed_text = SMALL_FONT.render(
                    f"Velocidade: {self.arrow_mode.arrow_rotation_speed:.1f}", 
                    True, GAME_WHITE)
                screen.blit(speed_text, (10, 90))
                
                if self.arrow_mode.arrow_in_target_zone:
                    instruction_text = SMALL_FONT.render(
                        "🎯 AGORA! Clique no quadrante brilhante!", True, GAME_GOLD)
                    instruction_bg_color = (50, 100, 50)
                else:
                    instruction_text = SMALL_FONT.render(
                        "Aguarde a seta apontar para o quadrante da mesma cor!", 
                        True, GAME_WHITE)
                    instruction_bg_color = (0, 0, 0)
                
                instruction_rect = instruction_text.get_rect(centerx=WIDTH//2, y=HEIGHT - 50)
                pygame.draw.rect(screen, instruction_bg_color, 
                               instruction_rect.inflate(20, 10))
                screen.blit(instruction_text, instruction_rect)
            else:
                rendering.draw_playing_state(
                    screen, self.escalators, self.game_mode, self.score,
                    self.time_limit, self.start_time, self.character_mode.target_traits,
                    self.is_first_target)
        
        elif self.game_state == GAME_STATE_NAME_INPUT:
            rendering.draw_name_input(
                screen, self.is_new_highscore, self.last_score,
                self.highscore_input, self.highscore_confirm_button)
        
        elif self.game_state == GAME_STATE_INSTRUCTIONS:
            rendering.draw_instructions(screen, self.back_button)
        
        elif self.game_state == GAME_STATE_HIGHSCORE:
            rendering.draw_highscores(screen, self.highscore_manager.highscores, 
                                     self.back_button)
        
        pygame.display.flip()
    
    def run(self):
        """Loop principal do jogo"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)
        
        self.data_collector.save_session_data()


def main():
    """Função principal"""
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
