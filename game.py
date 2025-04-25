import pygame
import random
import sys
import time
import os
import json
from datetime import datetime

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 800
BACKGROUND_COLOR = (200, 200, 200)
ESCALATOR_COLORS = [(100, 100, 100), (120, 120, 120), (140, 140, 140)]
ESCALATOR_SPEEDS = [2, 3, 4]  # Different speeds for each escalator
ESCALATOR_WIDTH = 120
ESCALATOR_SPACING = 100
ESCALATOR_START_X = 170  # Starting X position for the first escalator

# Character properties
CHARACTER_SIZE = 50

# Game state
GAME_STATE_MENU = 0
GAME_STATE_DISPLAY_TARGET = 1
GAME_STATE_PLAYING = 2
GAME_STATE_SUCCESS = 3
GAME_STATE_FAILURE = 4

# Game modes
GAME_MODE_SINGLE = 0  # Target appears only once
GAME_MODE_MULTIPLE = 1  # Target appears multiple times
GAME_MODE_INFINITE = 2  # Infinite mode with time bonuses

# Character spawn rate
CHARACTER_SPAWN_RATE = 60  # Frames between character spawns

# Font
FONT = pygame.font.SysFont('Arial', 36)
SMALL_FONT = pygame.font.SysFont('Arial', 24)
TINY_FONT = pygame.font.SysFont('Arial', 16)
TITLE_FONT = pygame.font.SysFont('Arial', 48, bold=True)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escalator Memory Game")
clock = pygame.time.Clock()

# Load assets
def load_assets():
    assets = {
        'bodies': [],
        'faces': [],
        'hats': [],
        'heads': []
    }
    
    # Load bodies (3 files)
    try:
        for i in range(1, 4):
            path = f"assets/bodies/bodie{i}.png"
            if os.path.exists(path):
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (CHARACTER_SIZE, CHARACTER_SIZE))
                assets["bodies"].append({"image": img, "name": f"Body {i}"})
    except Exception as e:
        print(f"Error loading bodies: {e}")
        # Create default body
        for i, color in enumerate([(255, 0, 0), (0, 255, 0), (0, 0, 255)]):
            img = pygame.Surface((CHARACTER_SIZE, CHARACTER_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(img, color, (0, CHARACTER_SIZE//2, CHARACTER_SIZE, CHARACTER_SIZE//2))
            assets["bodies"].append({"image": img, "name": f"Body {i+1}"})

    # Load faces (15 files)
    try:
        for i in range(1, 16):
            path = f"assets/faces/face{i}.png"
            if os.path.exists(path):
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (CHARACTER_SIZE, CHARACTER_SIZE))
                assets["faces"].append({"image": img, "name": f"Face {i}"})
    except Exception as e:
        print(f"Error loading faces: {e}")
        # Create default faces
        for i in range(15):
            img = pygame.Surface((CHARACTER_SIZE, CHARACTER_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(img, (0, 0, 0), (CHARACTER_SIZE//4, CHARACTER_SIZE//3), 3)
            pygame.draw.circle(img, (0, 0, 0), (CHARACTER_SIZE*3//4, CHARACTER_SIZE//3), 3)
            pygame.draw.arc(img, (0, 0, 0), (CHARACTER_SIZE//4, CHARACTER_SIZE//2, CHARACTER_SIZE//2, CHARACTER_SIZE//3), 0, 3.14, 2)
            assets["faces"].append({"image": img, "name": f"Face {i+1}"})

    # Load hats (10 files)
    try:
        for i in range(1, 11):
            path = f"assets/hats/hat{i}.png"
            if os.path.exists(path):
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (CHARACTER_SIZE, CHARACTER_SIZE//2))
                assets["hats"].append({"image": img, "name": f"Hat {i}"})
    except Exception as e:
        print(f"Error loading hats: {e}")
        # Create default hats
        for i in range(10):
            img = pygame.Surface((CHARACTER_SIZE, CHARACTER_SIZE//2), pygame.SRCALPHA)
            color = (random.randint(50, 250), random.randint(50, 250), random.randint(50, 250))
            if i % 3 == 0:  # Top hat
                pygame.draw.rect(img, color, (CHARACTER_SIZE//4, CHARACTER_SIZE//4, CHARACTER_SIZE//2, 10))
                pygame.draw.rect(img, color, (CHARACTER_SIZE//3, 0, CHARACTER_SIZE//3, CHARACTER_SIZE//4))
            elif i % 3 == 1:  # Cap
                pygame.draw.rect(img, color, (CHARACTER_SIZE//4, CHARACTER_SIZE//4, CHARACTER_SIZE//2, 10))
                pygame.draw.polygon(img, color, [(CHARACTER_SIZE//4, CHARACTER_SIZE//4), 
                                            (CHARACTER_SIZE*3//4, CHARACTER_SIZE//4), 
                                            (CHARACTER_SIZE//2, 0)])
            else:  # Crown
                pygame.draw.rect(img, color, (CHARACTER_SIZE//4, CHARACTER_SIZE//4, CHARACTER_SIZE//2, 10))
                pygame.draw.polygon(img, color, [(CHARACTER_SIZE//4, CHARACTER_SIZE//4), 
                                            (CHARACTER_SIZE//3, 0), 
                                            (CHARACTER_SIZE//2, CHARACTER_SIZE//4), 
                                            (CHARACTER_SIZE*2//3, 0), 
                                            (CHARACTER_SIZE*3//4, CHARACTER_SIZE//4)])
            assets["hats"].append({"image": img, "name": f"Hat {i+1}"})

    # Load heads (3 files)
    try:
        for i in range(1, 4):
            path = f"assets/heads/head{i}.png"
            if os.path.exists(path):
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (CHARACTER_SIZE, CHARACTER_SIZE))
                assets["heads"].append({"image": img, "name": f"Head {i}"})
    except Exception as e:
        print(f"Error loading heads: {e}")
        # Create default heads
        for i, color in enumerate([(255, 200, 200), (200, 255, 200), (200, 200, 255)]):
            img = pygame.Surface((CHARACTER_SIZE, CHARACTER_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(img, color, (0, 0, CHARACTER_SIZE, CHARACTER_SIZE))
            assets["heads"].append({"image": img, "name": f"Head {i+1}"})

    return assets

def create_sample_assets():
    """Create sample asset images for demo purposes"""
    # This is just a placeholder - in a real implementation, you'd create actual PNG files
    print("Sample assets would be created here in a full implementation")
    # For now, we'll rely on the fallback colored rectangles

# Load assets
CHARACTER_ASSETS = load_assets()

class Character:
    def __init__(self, x, y, traits):
        self.x = x
        self.y = y
        self.traits = traits  # Dictionary of traits
        self.size = CHARACTER_SIZE
        self.escalator_index = None  # Which escalator the character is on
        self.step_position = 0  # Position on the current step (0-1)
        self.current_step = 0  # Which step the character is currently on
    
    def update(self, speed, escalator):
        # The character should move with the escalator steps
        # Calculate the step height and how many steps fit in the screen
        step_height = 20
        total_steps = HEIGHT // step_height
        
        # Update the step position based on the escalator speed
        # This creates a synchronized movement effect
        self.step_position += speed / step_height
        
        # If we've moved past a step, move to the next one
        if self.step_position >= 1:
            self.current_step += 1
            self.step_position -= 1
        
        # Calculate the y position based on the current step and position within the step
        self.y = (self.current_step * step_height) + (self.step_position * step_height)
        
        # Make sure the character stays centered on the escalator
        self.x = escalator.x + (escalator.width - self.size) // 2
    
    def draw(self, screen):
        # Draw body
        screen.blit(self.traits["body"]["image"], (self.x, self.y))
        
        # Draw head
        screen.blit(self.traits["head"]["image"], (self.x, self.y))
        
        # Draw face
        screen.blit(self.traits["face"]["image"], (self.x, self.y))
        
        # Draw hat (slightly above the head)
        screen.blit(self.traits["hat"]["image"], (self.x, self.y - self.size//4))
    
    def is_clicked(self, mouse_pos):
        # Check if this character was clicked
        mx, my = mouse_pos
        return (self.x <= mx <= self.x + self.size and 
                self.y <= my <= self.y + self.size)
    
    def is_same_as(self, other):
        # Check if this character has the same traits as another
        return (self.traits["body"]["name"] == other.traits["body"]["name"] and
                self.traits["face"]["name"] == other.traits["face"]["name"] and
                self.traits["head"]["name"] == other.traits["head"]["name"] and
                self.traits["hat"]["name"] == other.traits["hat"]["name"])
    
    def __str__(self):
        # Return a string representation of the character
        return f"{self.traits['head']['name']} with {self.traits['face']['name']}, " \
               f"{self.traits['body']['name']}, and {self.traits['hat']['name']}"

class CharacterFactory:
    def __init__(self, assets):
        self.assets = assets
        self.created_characters = []
        self.all_possible_combinations = self._generate_all_possible_combinations()
        self.available_combinations = self.all_possible_combinations.copy()
    
    def _generate_all_possible_combinations(self):
        # Generate all possible trait combinations
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

class Button:
    def __init__(self, x, y, width, height, text, color=(100, 100, 200), hover_color=(150, 150, 250)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.SysFont('Arial', 24)
    
    def draw(self, screen):
        # Draw the button
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Border
        
        # Draw text
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
        self.step_offset = 0  # For animating the escalator steps
    
    def add_character(self, character):
        # Add a character to this escalator
        character.escalator_index = ESCALATOR_SPEEDS.index(self.speed)
        character.current_step = -3  # Start above the screen
        character.step_position = 0
        self.characters.append(character)
    
    def update(self):
        # Update the step animation
        self.step_offset = (self.step_offset + self.speed) % 20  # 20 is the step height
        
        # Update all characters on this escalator
        for character in self.characters[:]:
            character.update(self.speed, self)
            # Remove characters that have gone off screen
            if character.y > HEIGHT:
                self.characters.remove(character)
    
    def draw(self, screen):
        # Draw the escalator
        pygame.draw.rect(screen, self.color, (self.x, 0, self.width, HEIGHT))
        
        # Draw line segments to represent the escalator steps
        step_height = 20
        for y in range(0, HEIGHT + step_height, step_height):
            # Adjust the y position based on step_offset for animation
            adjusted_y = (y + self.step_offset) % (HEIGHT + step_height)
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

class GameDataCollector:
    def __init__(self):
        self.current_session = {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "game_mode": None,
            "trials": [],
            "mouse_tracking": []
        }
        self.current_trial = None
        self.target_spawn_time = None
    
    def start_new_trial(self, game_mode):
        self.current_session["game_mode"] = game_mode
        self.current_trial = {
            "trial_start_time": time.time(),
            "target_character": None,
            "target_spawn_time": None,
            "selection_time": None,
            "success": False,
            "reaction_time": None
        }
    
    def record_target_spawn(self, character_traits):
        if self.current_trial:
            self.current_trial["target_character"] = character_traits
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
    
    def save_session_data(self):
        filename = f"game_data_{self.current_session['session_id']}.json"
        with open(filename, 'w') as f:
            json.dump(self.current_session, f, indent=2)

class Game:
    def __init__(self):
        self.escalators = []
        self.spawn_counter = 0
        self.running = True
        self.game_state = GAME_STATE_MENU
        self.game_mode = GAME_MODE_SINGLE
        self.target_character = None
        self.target_traits = None
        self.display_target_time = 4  # seconds to display target
        self.target_display_start = 0
        self.score = 0
        self.highest_score = 0
        self.time_limit = 30  # 30 seconds to find the character
        self.start_time = 0
        self.target_spawn_count = 0  # How many times the target has spawned
        self.target_max_spawns = 3  # Maximum times target can spawn in multiple mode
        self.has_target_spawned = False
        self.target_spawned_time = 0
        self.character_factory = CharacterFactory(CHARACTER_ASSETS)
        self.time_bonus = 5  # Time added for correct clicks in infinite mode
        self.data_collector = GameDataCollector()
        
        # Create buttons for menu
        button_width, button_height = 200, 50
        button_x = WIDTH // 2 - button_width // 2
        
        self.single_mode_button = Button(
            button_x, HEIGHT // 2 - 70, 
            button_width, button_height, 
            "Single Appearance Mode"
        )
        
        self.multiple_mode_button = Button(
            button_x, HEIGHT // 2, 
            button_width, button_height, 
            "Multiple Appearances Mode"
        )

        self.infinite_mode_button = Button(
            button_x, HEIGHT // 2 + 70, 
            button_width, button_height, 
            "Infinite Mode"
        )
        
        # Create the three escalators
        for i in range(3):
            x = ESCALATOR_START_X + i * (ESCALATOR_WIDTH + ESCALATOR_SPACING)
            escalator = Escalator(x, ESCALATOR_WIDTH, ESCALATOR_SPEEDS[i], ESCALATOR_COLORS[i])
            self.escalators.append(escalator)
        
        # Load menu background image
        self.menu_image = self.load_menu_image()
    
    def load_menu_image(self):
        if os.path.exists("assets/misc/menu.png"):
            try:
                return pygame.image.load("assets/misc/menu.png")
            except pygame.error:
                print("Menu image found but couldn't be loaded, using default menu.")
                return False
        else:
            print("Menu image not found, using default menu.")
            return False
    
    def select_new_target(self):
        # Create a target character (not placed on any escalator yet)
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
                    # Restart the game
                    self.reset_game()
                    self.game_state = GAME_STATE_DISPLAY_TARGET  # Ensure it goes back to displaying the target
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == GAME_STATE_MENU:
                    # Check if either game mode button was clicked
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
                    # Check all escalators for clicked characters
                    for escalator in self.escalators:
                        clicked_character = escalator.check_character_click(mouse_pos)
                        if clicked_character:
                            if clicked_character.traits == self.target_traits:
                                # Correct character clicked
                                self.score += 1
                                self.data_collector.record_selection(True)
                                if self.game_mode == GAME_MODE_SINGLE:
                                    # In single mode, finding the character once ends the game with success
                                    self.game_state = GAME_STATE_SUCCESS
                                else:
                                    # In multiple mode, we continue until all instances are found or wrong click
                                    # Remove the character from escalator
                                    escalator.characters.remove(clicked_character)
                                    if self.game_mode == GAME_MODE_MULTIPLE and self.score >= self.target_max_spawns:
                                        self.game_state = GAME_STATE_SUCCESS
                                    elif self.game_mode == GAME_MODE_INFINITE:
                                        # Add time bonus for infinite mode
                                        self.time_limit += self.time_bonus
                                        # Spawn a new target immediately to keep the game going
                                        self.has_target_spawned = False
                            else:
                                # Wrong character clicked
                                self.data_collector.record_selection(False)
                                self.game_state = GAME_STATE_FAILURE
                            break
        
        # Update button hover states
        if self.game_state == GAME_STATE_MENU:
            self.single_mode_button.check_hover(mouse_pos)
            self.multiple_mode_button.check_hover(mouse_pos)
            self.infinite_mode_button.check_hover(mouse_pos)
    
    def reset_game(self):
        # Reset the game state
        for escalator in self.escalators:
            escalator.characters = []
        self.character_factory.reset()
        self.select_new_target()
        self.spawn_counter = 0
        self.start_time = 0
        self.has_target_spawned = False
        self.target_spawn_count = 0
        self.score = 0
        self.data_collector.start_new_trial(self.game_mode)
    
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
            self.target_spawn_count += 1
            self.data_collector.record_target_spawn(self.target_traits)
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
                # Update highest score if needed
                if self.score > self.highest_score:
                    self.highest_score = self.score
            
            # Spawn new characters
            self.spawn_counter += 1
            if self.spawn_counter >= CHARACTER_SPAWN_RATE:
                self.spawn_counter = 0
                
                # Handle target character spawning depending on game mode
                if self.game_mode == GAME_MODE_SINGLE:
                    # In single mode, spawn the target only once
                    if not self.has_target_spawned and current_time - self.start_time >= 5:
                        self.spawn_character(target=True)
                    else:
                        # Always spawn a random non-target character
                        self.spawn_character(target=False)
                elif self.game_mode == GAME_MODE_MULTIPLE:
                    # In multiple mode, spawn the target multiple times
                    if self.target_spawn_count < self.target_max_spawns and random.random() < 0.15:
                        # 15% chance to spawn target each time
                        self.spawn_character(target=True)
                    else:
                        # Spawn a random non-target character
                        self.spawn_character(target=False)
                elif self.game_mode == GAME_MODE_INFINITE:
                    # In infinite mode, always make sure there's one target
                    if not self.has_target_spawned and random.random() < 0.2:
                    # 20% chance to spawn target when there isn't one
                        self.spawn_character(target=True)
                    else:
                    # Spawn a random non-target character
                        self.spawn_character(target=False)
    
    def draw_character_traits(self, y_pos):
        # Draw text describing the character traits
        head_text = TINY_FONT.render(f"Head: {self.target_traits['head']['name']}", True, (0, 0, 0))
        face_text = TINY_FONT.render(f"Face: {self.target_traits['face']['name']}", True, (0, 0, 0))
        body_text = TINY_FONT.render(f"Body: {self.target_traits['body']['name']}", True, (0, 0, 0))
        hat_text = TINY_FONT.render(f"Hat: {self.target_traits['hat']['name']}", True, (0, 0, 0))
        
        screen.blit(head_text, (WIDTH//2 - 100, y_pos))
        screen.blit(face_text, (WIDTH//2 - 100, y_pos + 20))
        screen.blit(body_text, (WIDTH//2 - 100, y_pos + 40))
        screen.blit(hat_text, (WIDTH//2 - 100, y_pos + 60))
    
    def draw_menu(self):
        # Draw menu screen
        if self.menu_image:
            # If the menu image exists, blit it to the screen
            screen.blit(self.menu_image, (0, 0))  # Draw the image at the top-left corner
        else:
            # If the image doesn't exist, draw the default menu
            title = TITLE_FONT.render("Escalator Memory Game", True, (50, 50, 150))
            screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))

            instructions = SMALL_FONT.render("Select Game Mode:", True, (0, 0, 0))
            screen.blit(instructions, (WIDTH//2 - instructions.get_width()//2, HEIGHT//2 - 120))
        
            # Draw game mode selection buttons
            self.single_mode_button.draw(screen)
            self.multiple_mode_button.draw(screen)
            self.infinite_mode_button.draw(screen)
        
            # Draw game mode descriptions
            single_desc = TINY_FONT.render("Find the character shown at start (appears once)", True, (0, 0, 0))
            multiple_desc = TINY_FONT.render(f"Find all {self.target_max_spawns} appearances of the character", True, (0, 0, 0))
            infinite_desc = TINY_FONT.render("Find characters to earn more time - play until you lose!", True, (0, 0, 0))
        
            screen.blit(single_desc, (WIDTH//2 - single_desc.get_width()//2, HEIGHT//2 - 35))
            screen.blit(multiple_desc, (WIDTH//2 - multiple_desc.get_width()//2, HEIGHT//2 + 35))
            screen.blit(infinite_desc, (WIDTH//2 - infinite_desc.get_width()//2, HEIGHT//2 + 105))
   
    def draw(self):
        # Clear the screen
        screen.fill(BACKGROUND_COLOR)
        
        if self.game_state == GAME_STATE_MENU:
            self.draw_menu()
            
        elif self.game_state == GAME_STATE_DISPLAY_TARGET:
            # Display the target character
            if self.game_mode == GAME_MODE_SINGLE:
                mode_text = "Single Appearance Mode"
            elif self.game_mode == GAME_MODE_MULTIPLE:
                mode_text = "Multiple Appearances Mode"
            else:
                mode_text = "Infinite Mode"

            mode_render = SMALL_FONT.render(mode_text, True, (50, 50, 150))
            screen.blit(mode_render, (WIDTH//2 - mode_render.get_width()//2, 20))
            
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
            
            # Display score
            if self.game_mode == GAME_MODE_SINGLE:
                mode_text = "Find once"
            elif self.game_mode == GAME_MODE_MULTIPLE:
                mode_text = f"Find {self.target_spawn_count}/{self.target_max_spawns}"
            else:  # Infinite mode
                mode_text = f"+{self.time_bonus}s per find"
            score_text = SMALL_FONT.render(f"Score: {self.score} - {mode_text}", True, (0, 0, 0))
            screen.blit(score_text, (10, 40))
            
            # In case of multiple mode, show a small reminder of what the character looks like
            if self.game_mode != GAME_MODE_SINGLE:
                reminder_text = TINY_FONT.render("Target Character:", True, (0, 0, 0))
                screen.blit(reminder_text, (10, 70))
                
                # Draw a small version of the target
                mini_character = Character(20, 90, self.target_traits)
                mini_character.size = CHARACTER_SIZE // 2  # Make it smaller
                mini_character.draw(screen)
            
        elif self.game_state == GAME_STATE_SUCCESS:
            text = FONT.render("Success! You found the character!", True, (0, 128, 0))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))
            
            score_text = FONT.render(f"Score: {self.score}", True, (0, 0, 0))
            screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
            
            restart = SMALL_FONT.render("Press 'R' to play again or ESC for menu", True, (0, 0, 0))
            screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 50))
            
        elif self.game_state == GAME_STATE_FAILURE:
            text = FONT.render("Game Over! You didn't find the character.", True, (255, 0, 0))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))
            
            score_text = FONT.render(f"Score: {self.score}", True, (0, 0, 0))
            screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
            
            # Render high score as a text surface
            high_score_text = SMALL_FONT.render(f"Highest Score: {self.highest_score}", True, (0, 0, 0))
            screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//2 + 30))
            
            restart = SMALL_FONT.render("Press 'R' to play again or ESC for menu", True, (0, 0, 0))
            screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 70))
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)  # 60 FPS
        self.data_collector.save_session_data()

# Main function
def main():
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()