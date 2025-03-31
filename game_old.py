import pygame
import random
import sys
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (200, 200, 200)
ESCALATOR_COLORS = [(100, 100, 100), (120, 120, 120), (140, 140, 140)]
ESCALATOR_SPEEDS = [2, 3, 4]  # Different speeds for each escalator
ESCALATOR_WIDTH = 120
ESCALATOR_SPACING = 100
ESCALATOR_START_X = 170  # Starting X position for the first escalator

# Character properties
CHARACTER_SIZE = 40
CHARACTER_TYPES = [
    {"color": (255, 0, 0), "name": "Red"},
    {"color": (0, 255, 0), "name": "Green"},
    {"color": (0, 0, 255), "name": "Blue"},
    {"color": (255, 255, 0), "name": "Yellow"},
    {"color": (255, 0, 255), "name": "Purple"},
    {"color": (0, 255, 255), "name": "Cyan"},
    {"color": (255, 165, 0), "name": "Orange"},
    {"color": (165, 42, 42), "name": "Brown"}
]
CHARACTER_SPAWN_RATE = 60  # Frames between character spawns

# Game state
GAME_STATE_DISPLAY_TARGET = 0
GAME_STATE_PLAYING = 1
GAME_STATE_SUCCESS = 2
GAME_STATE_FAILURE = 3

# Font
FONT = pygame.font.SysFont('Arial', 36)
SMALL_FONT = pygame.font.SysFont('Arial', 24)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escalator Memory Game")
clock = pygame.time.Clock()

class Character:
    def __init__(self, x, y, char_type):
        self.x = x
        self.y = y
        self.char_type = char_type
        self.color = char_type["color"]
        self.name = char_type["name"]
        self.size = CHARACTER_SIZE
        self.escalator_index = None  # Which escalator the character is on
    
    def update(self, speed):
        # Move the character down the escalator
        self.y += speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
    
    def is_clicked(self, mouse_pos):
        # Check if this character was clicked
        mx, my = mouse_pos
        return (self.x <= mx <= self.x + self.size and 
                self.y <= my <= self.y + self.size)

class Escalator:
    def __init__(self, x, width, speed, color):
        self.x = x
        self.width = width
        self.speed = speed
        self.color = color
        self.characters = []
    
    def add_character(self, target_type=None):
        # Add a new character at the top of the escalator
        char_x = self.x + (self.width - CHARACTER_SIZE) // 2
        char_y = 0 - CHARACTER_SIZE  # Start above the screen
        
        # If target_type is specified, use it; otherwise choose random
        if target_type:
            char_type = target_type
        else:
            char_type = random.choice(CHARACTER_TYPES)
            
        character = Character(char_x, char_y, char_type)
        character.escalator_index = ESCALATOR_SPEEDS.index(self.speed)
        self.characters.append(character)
        return character
    
    def update(self):
        # Update all characters on this escalator
        for character in self.characters[:]:
            character.update(self.speed)
            # Remove characters that have gone off screen
            if character.y > HEIGHT:
                self.characters.remove(character)
    
    def draw(self, screen):
        # Draw the escalator
        pygame.draw.rect(screen, self.color, (self.x, 0, self.width, HEIGHT))
        
        # Draw line segments to represent the escalator steps
        step_height = 20
        for y in range(0, HEIGHT, step_height):
            # Adjust the y position based on time for animation
            adjusted_y = (y + pygame.time.get_ticks() * self.speed / 100) % HEIGHT
            pygame.draw.line(screen, (50, 50, 50), 
                            (self.x, adjusted_y), 
                            (self.x + self.width, adjusted_y), 2)
        
        # Draw all characters on this escalator
        for character in self.characters:
            character.draw(screen)
    
    def check_character_click(self, mouse_pos):
        # Check if any character on this escalator was clicked
        for character in self.characters:
            if character.is_clicked(mouse_pos):
                return character
        return None

class Game:
    def __init__(self):
        self.escalators = []
        self.spawn_counter = 0
        self.running = True
        self.game_state = GAME_STATE_DISPLAY_TARGET
        self.target_character_type = None
        self.display_target_time = 3  # seconds to display target
        self.target_display_start = 0
        self.score = 0
        self.time_limit = 30  # 30 seconds to find the character
        self.start_time = 0
        self.has_target_spawned = False
        self.target_spawned_time = 0
        
        # Create the three escalators
        for i in range(3):
            x = ESCALATOR_START_X + i * (ESCALATOR_WIDTH + ESCALATOR_SPACING)
            escalator = Escalator(x, ESCALATOR_WIDTH, ESCALATOR_SPEEDS[i], ESCALATOR_COLORS[i])
            self.escalators.append(escalator)
        
        # Select a random target character
        self.select_new_target()
    
    def select_new_target(self):
        self.target_character_type = random.choice(CHARACTER_TYPES)
        self.target_display_start = time.time()
        self.has_target_spawned = False
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and (self.game_state == GAME_STATE_SUCCESS or 
                                                self.game_state == GAME_STATE_FAILURE):
                    # Restart the game
                    self.reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == GAME_STATE_PLAYING:
                    mouse_pos = pygame.mouse.get_pos()
                    # Check all escalators for clicked characters
                    for escalator in self.escalators:
                        clicked_character = escalator.check_character_click(mouse_pos)
                        if clicked_character:
                            # Check if it's the target character
                            if clicked_character.char_type == self.target_character_type:
                                self.game_state = GAME_STATE_SUCCESS
                            else:
                                self.game_state = GAME_STATE_FAILURE
                            break
    
    def reset_game(self):
        # Reset the game state
        for escalator in self.escalators:
            escalator.characters = []
        self.select_new_target()
        self.game_state = GAME_STATE_DISPLAY_TARGET
        self.spawn_counter = 0
        self.start_time = 0
        self.has_target_spawned = False
    
    def update(self):
        current_time = time.time()
        
        # Handle game state transitions
        if self.game_state == GAME_STATE_DISPLAY_TARGET:
            # Switch to playing state after display time
            if current_time - self.target_display_start >= self.display_target_time:
                self.game_state = GAME_STATE_PLAYING
                self.start_time = current_time
        
        # Update all escalators
        for escalator in self.escalators:
            escalator.update()
        
        if self.game_state == GAME_STATE_PLAYING:
            # Check if time has run out
            if current_time - self.start_time >= self.time_limit:
                self.game_state = GAME_STATE_FAILURE
            
            # Spawn new characters
            self.spawn_counter += 1
            if self.spawn_counter >= CHARACTER_SPAWN_RATE:
                self.spawn_counter = 0
                # Randomly choose an escalator to spawn a character on
                escalator = random.choice(self.escalators)
                
                # Spawn the target character if it hasn't been spawned yet and enough time has passed
                if not self.has_target_spawned and current_time - self.start_time >= 5:
                    escalator.add_character(self.target_character_type)
                    self.has_target_spawned = True
                    self.target_spawned_time = current_time
                else:
                    # Spawn a random character (not the target)
                    available_types = [t for t in CHARACTER_TYPES if t != self.target_character_type]
                    char_type = random.choice(available_types)
                    escalator.add_character(char_type)
    
    def draw(self):
        # Clear the screen
        screen.fill(BACKGROUND_COLOR)
        
        if self.game_state == GAME_STATE_DISPLAY_TARGET:
            # Display the target character
            text = FONT.render("Remember this character:", True, (0, 0, 0))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//4))
            
            # Draw the target character
            pygame.draw.rect(screen, self.target_character_type["color"], 
                           (WIDTH//2 - CHARACTER_SIZE//2, HEIGHT//2 - CHARACTER_SIZE//2, 
                            CHARACTER_SIZE, CHARACTER_SIZE))
            
            # Display countdown
            time_left = max(0, self.display_target_time - (time.time() - self.target_display_start))
            countdown = FONT.render(f"Starting in: {time_left:.1f}", True, (0, 0, 0))
            screen.blit(countdown, (WIDTH//2 - countdown.get_width()//2, HEIGHT*3//4))
            
        elif self.game_state == GAME_STATE_PLAYING:
            # Draw all escalators
            for escalator in self.escalators:
                escalator.draw(screen)
            
            # Display time left
            time_left = max(0, self.time_limit - (time.time() - self.start_time))
            time_text = SMALL_FONT.render(f"Time Left: {time_left:.1f}s", True, (0, 0, 0))
            screen.blit(time_text, (10, 10))
            
        elif self.game_state == GAME_STATE_SUCCESS:
            text = FONT.render("Success! You found the character!", True, (0, 128, 0))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            
            restart = SMALL_FONT.render("Press 'R' to play again", True, (0, 0, 0))
            screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 50))
            
        elif self.game_state == GAME_STATE_FAILURE:
            text = FONT.render("Game Over! You didn't find the character.", True, (255, 0, 0))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            
            restart = SMALL_FONT.render("Press 'R' to play again", True, (0, 0, 0))
            screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 50))
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)  # 60 FPS

# Main function
def main():
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()