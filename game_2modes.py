import pygame
import random
import sys
import time
import itertools

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
CHARACTER_SIZE = 50

# Character trait lists for random combinations
BODY_COLORS = [
    {"color": (255, 0, 0), "name": "Red"},
    {"color": (0, 255, 0), "name": "Green"},
    {"color": (0, 0, 255), "name": "Blue"},
    {"color": (255, 255, 0), "name": "Yellow"},
    {"color": (255, 0, 255), "name": "Purple"},
    {"color": (0, 255, 255), "name": "Cyan"}
]

FACE_TYPES = [
    {"type": "happy", "name": "Happy"},
    {"type": "sad", "name": "Sad"},
    {"type": "angry", "name": "Angry"},
    {"type": "surprised", "name": "Surprised"}
]

HAT_TYPES = [
    {"type": "none", "name": "No Hat"},
    {"type": "top", "name": "Top Hat", "color": (50, 50, 50)},
    {"type": "cap", "name": "Cap", "color": (150, 75, 0)},
    {"type": "crown", "name": "Crown", "color": (255, 215, 0)}
]

ACCESSORY_TYPES = [
    {"type": "none", "name": "No Accessory"},
    {"type": "glasses", "name": "Glasses", "color": (0, 0, 0)},
    {"type": "bowtie", "name": "Bowtie", "color": (255, 20, 147)},
    {"type": "necklace", "name": "Necklace", "color": (192, 192, 192)}
]

# Game state
GAME_STATE_DISPLAY_TARGET = 0
GAME_STATE_PLAYING = 1
GAME_STATE_SUCCESS = 2
GAME_STATE_FAILURE = 3

# Character spawn rate
CHARACTER_SPAWN_RATE = 60  # Frames between character spawns

# Font
FONT = pygame.font.SysFont('Arial', 36)
SMALL_FONT = pygame.font.SysFont('Arial', 24)
TINY_FONT = pygame.font.SysFont('Arial', 16)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escalator Memory Game")
clock = pygame.time.Clock()

class Character:
    def __init__(self, x, y, traits):
        self.x = x
        self.y = y
        self.traits = traits  # Dictionary of traits
        self.size = CHARACTER_SIZE
        self.escalator_index = None  # Which escalator the character is on
    
    def update(self, speed):
        # Move the character down the escalator
        self.y += speed
    
    def draw(self, screen):
        # Draw body (square with body color)
        body_color = self.traits["body"]["color"]
        pygame.draw.rect(screen, body_color, (self.x, self.y, self.size, self.size))
        
        # Draw face
        face_type = self.traits["face"]["type"]
        if face_type == "happy":
            # Draw smile
            pygame.draw.arc(screen, (0, 0, 0), 
                          (self.x + 10, self.y + 20, self.size - 20, self.size - 20),
                          0.2, 2.9, 2)
            # Draw eyes
            pygame.draw.circle(screen, (0, 0, 0), (self.x + 15, self.y + 20), 3)
            pygame.draw.circle(screen, (0, 0, 0), (self.x + self.size - 15, self.y + 20), 3)
        elif face_type == "sad":
            # Draw frown
            pygame.draw.arc(screen, (0, 0, 0), 
                          (self.x + 10, self.y + 30, self.size - 20, self.size - 20),
                          3.3, 6.1, 2)
            # Draw eyes
            pygame.draw.circle(screen, (0, 0, 0), (self.x + 15, self.y + 20), 3)
            pygame.draw.circle(screen, (0, 0, 0), (self.x + self.size - 15, self.y + 20), 3)
        elif face_type == "angry":
            # Draw angry mouth
            pygame.draw.line(screen, (0, 0, 0), 
                           (self.x + 15, self.y + 35), 
                           (self.x + self.size - 15, self.y + 35), 2)
            # Draw angry eyes
            pygame.draw.line(screen, (0, 0, 0), 
                           (self.x + 10, self.y + 15), 
                           (self.x + 20, self.y + 20), 2)
            pygame.draw.line(screen, (0, 0, 0), 
                           (self.x + self.size - 10, self.y + 15), 
                           (self.x + self.size - 20, self.y + 20), 2)
        elif face_type == "surprised":
            # Draw surprised mouth
            pygame.draw.circle(screen, (0, 0, 0), (self.x + self.size//2, self.y + 35), 5)
            # Draw eyes
            pygame.draw.circle(screen, (0, 0, 0), (self.x + 15, self.y + 20), 4)
            pygame.draw.circle(screen, (0, 0, 0), (self.x + self.size - 15, self.y + 20), 4)
        
        # Draw hat
        hat_type = self.traits["hat"]["type"]
        if hat_type == "top":
            hat_color = self.traits["hat"]["color"]
            pygame.draw.rect(screen, hat_color, 
                           (self.x + 10, self.y - 10, self.size - 20, 10))
            pygame.draw.rect(screen, hat_color, 
                           (self.x + 5, self.y, self.size - 10, 5))
        elif hat_type == "cap":
            hat_color = self.traits["hat"]["color"]
            pygame.draw.rect(screen, hat_color, 
                           (self.x + 5, self.y, self.size - 10, 10))
            pygame.draw.rect(screen, hat_color, 
                           (self.x + 35, self.y - 5, 10, 5))
        elif hat_type == "crown":
            hat_color = self.traits["hat"]["color"]
            points = [
                (self.x + 10, self.y),
                (self.x + 15, self.y - 10),
                (self.x + 25, self.y - 5),
                (self.x + 35, self.y - 10),
                (self.x + self.size - 10, self.y)
            ]
            pygame.draw.polygon(screen, hat_color, points)
        
        # Draw accessory
        accessory_type = self.traits["accessory"]["type"]
        if accessory_type == "glasses":
            acc_color = self.traits["accessory"]["color"]
            pygame.draw.circle(screen, acc_color, (self.x + 15, self.y + 20), 5, 1)
            pygame.draw.circle(screen, acc_color, (self.x + self.size - 15, self.y + 20), 5, 1)
            pygame.draw.line(screen, acc_color, 
                           (self.x + 20, self.y + 20), 
                           (self.x + self.size - 20, self.y + 20), 1)
        elif accessory_type == "bowtie":
            acc_color = self.traits["accessory"]["color"]
            points1 = [
                (self.x + self.size//2, self.y + self.size - 10),
                (self.x + self.size//2 - 10, self.y + self.size - 15),
                (self.x + self.size//2 - 10, self.y + self.size - 5)
            ]
            points2 = [
                (self.x + self.size//2, self.y + self.size - 10),
                (self.x + self.size//2 + 10, self.y + self.size - 15),
                (self.x + self.size//2 + 10, self.y + self.size - 5)
            ]
            pygame.draw.polygon(screen, acc_color, points1)
            pygame.draw.polygon(screen, acc_color, points2)
            pygame.draw.circle(screen, acc_color, (self.x + self.size//2, self.y + self.size - 10), 2)
        elif accessory_type == "necklace":
            acc_color = self.traits["accessory"]["color"]
            pygame.draw.arc(screen, acc_color, 
                          (self.x + 15, self.y + self.size - 25, self.size - 30, 20),
                          0, 3.14, 2)
    
    def is_clicked(self, mouse_pos):
        # Check if this character was clicked
        mx, my = mouse_pos
        return (self.x <= mx <= self.x + self.size and 
                self.y <= my <= self.y + self.size)
    
    def is_same_as(self, other):
        # Check if this character has the same traits as another
        return (self.traits["body"]["name"] == other.traits["body"]["name"] and
                self.traits["face"]["name"] == other.traits["face"]["name"] and
                self.traits["hat"]["name"] == other.traits["hat"]["name"] and
                self.traits["accessory"]["name"] == other.traits["accessory"]["name"])
    
    def __str__(self):
        # Return a string representation of the character
        return f"{self.traits['body']['name']} body with {self.traits['face']['name']} face, " \
               f"{self.traits['hat']['name']}, and {self.traits['accessory']['name']}"

class CharacterFactory:
    def __init__(self):
        self.created_characters = []
        self.all_possible_combinations = self._generate_all_possible_combinations()
        self.available_combinations = self.all_possible_combinations.copy()
    
    def _generate_all_possible_combinations(self):
        # Generate all possible trait combinations
        all_combinations = []
        for body in BODY_COLORS:
            for face in FACE_TYPES:
                for hat in HAT_TYPES:
                    for accessory in ACCESSORY_TYPES:
                        traits = {
                            "body": body,
                            "face": face,
                            "hat": hat,
                            "accessory": accessory
                        }
                        all_combinations.append(traits)
        return all_combinations
    
    def reset(self):
        # Reset available combinations
        self.available_combinations = self.all_possible_combinations.copy()
        self.created_characters = []
    
    def create_random_character(self, x, y):
        # Create a random character with unique traits
        if not self.available_combinations:
            print("Warning: No more unique combinations available!")
            # If we've used all combinations, regenerate the list
            self.available_combinations = self.all_possible_combinations.copy()
        
        # Get a random traits combination
        traits = random.choice(self.available_combinations)
        self.available_combinations.remove(traits)
        
        # Create and return a new character
        character = Character(x, y, traits)
        self.created_characters.append(character)
        return character
    
    def get_random_existing_traits(self):
        # Get traits from a character we've already created
        if not self.created_characters:
            return None
        
        character = random.choice(self.created_characters)
        return character.traits.copy()

class Escalator:
    def __init__(self, x, width, speed, color):
        self.x = x
        self.width = width
        self.speed = speed
        self.color = color
        self.characters = []
    
    def add_character(self, character):
        # Add a character to this escalator
        character.escalator_index = ESCALATOR_SPEEDS.index(self.speed)
        self.characters.append(character)
    
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
        self.target_character = None
        self.target_traits = None
        self.display_target_time = 4  # seconds to display target
        self.target_display_start = 0
        self.score = 0
        self.time_limit = 30  # 30 seconds to find the character
        self.start_time = 0
        self.has_target_spawned = False
        self.target_spawned_time = 0
        self.character_factory = CharacterFactory()
        
        # Create the three escalators
        for i in range(3):
            x = ESCALATOR_START_X + i * (ESCALATOR_WIDTH + ESCALATOR_SPACING)
            escalator = Escalator(x, ESCALATOR_WIDTH, ESCALATOR_SPEEDS[i], ESCALATOR_COLORS[i])
            self.escalators.append(escalator)
        
        # Select a random target character
        self.select_new_target()
    
    def select_new_target(self):
        # Create a target character (not placed on any escalator yet)
        self.target_character = self.character_factory.create_random_character(
            WIDTH//2 - CHARACTER_SIZE//2, 
            HEIGHT//2 - CHARACTER_SIZE//2
        )
        self.target_traits = self.target_character.traits
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
                            # Check if it matches the target character
                            if clicked_character.traits == self.target_traits:
                                self.game_state = GAME_STATE_SUCCESS
                            else:
                                self.game_state = GAME_STATE_FAILURE
                            break
    
    def reset_game(self):
        # Reset the game state
        for escalator in self.escalators:
            escalator.characters = []
        self.character_factory.reset()
        self.select_new_target()
        self.game_state = GAME_STATE_DISPLAY_TARGET
        self.spawn_counter = 0
        self.start_time = 0
        self.has_target_spawned = False
    
    def spawn_character(self, target=False):
        # Choose a random escalator
        escalator = random.choice(self.escalators)
        char_x = escalator.x + (escalator.width - CHARACTER_SIZE) // 2
        char_y = 0 - CHARACTER_SIZE  # Start above the screen
        
        if target:
            # Create the target character with the same traits
            character = Character(char_x, char_y, self.target_traits)
            self.has_target_spawned = True
            self.target_spawned_time = time.time()
        else:
            # Create a random character (ensure it's not the same as target)
            while True:
                character = self.character_factory.create_random_character(char_x, char_y)
                if character.traits != self.target_traits:
                    break
        
        escalator.add_character(character)
    
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
                
                # Spawn the target character if it hasn't been spawned yet and enough time has passed
                if not self.has_target_spawned and current_time - self.start_time >= 5:
                    self.spawn_character(target=True)
                else:
                    # Spawn a random non-target character
                    self.spawn_character(target=False)
    
    def draw_character_traits(self, y_pos):
        # Draw text describing the character traits
        body_text = TINY_FONT.render(f"Body: {self.target_traits['body']['name']}", True, (0, 0, 0))
        face_text = TINY_FONT.render(f"Face: {self.target_traits['face']['name']}", True, (0, 0, 0))
        hat_text = TINY_FONT.render(f"Hat: {self.target_traits['hat']['name']}", True, (0, 0, 0))
        accessory_text = TINY_FONT.render(f"Accessory: {self.target_traits['accessory']['name']}", True, (0, 0, 0))
        
        screen.blit(body_text, (WIDTH//2 - 100, y_pos))
        screen.blit(face_text, (WIDTH//2 - 100, y_pos + 20))
        screen.blit(hat_text, (WIDTH//2 - 100, y_pos + 40))
        screen.blit(accessory_text, (WIDTH//2 - 100, y_pos + 60))
    
    def draw(self):
        # Clear the screen
        screen.fill(BACKGROUND_COLOR)
        
        if self.game_state == GAME_STATE_DISPLAY_TARGET:
            # Display the target character
            text = FONT.render("Remember this character:", True, (0, 0, 0))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//4))
            
            # Draw the target character
            self.target_character.draw(screen)
            
            # Draw character traits description
            self.draw_character_traits(HEIGHT//2 + 50)
            
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