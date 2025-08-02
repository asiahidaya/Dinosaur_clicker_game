import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dinosaur Clicker Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Load the Dinosaur Image
try:
    dino_image = pygame.image.load('dino.png')  # Make sure you have a 'dino.png' file in the same directory as this script
    dino_rect = dino_image.get_rect()
except pygame.error:
    print("Error: dino.png not found! Please make sure 'dino.png' is in the same directory as the script.")
    exit()

# Initial Position
dino_rect.topleft = (random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100))

# Font for Score
font = pygame.font.SysFont(None, 36)

# Variables
score = 0
clock = pygame.time.Clock()

# Game timer (in seconds)
start_time = time.time()
game_duration = 30  # 30 seconds

# Initialize sound
pygame.mixer.init()
click_sound = pygame.mixer.Sound('click_sound.wav')  # Replace with the correct sound file
game_over_sound = pygame.mixer.Sound('game_over.wav')  # Game Over sound file

# Load high score from a file (if it exists)
try:
    with open('high_score.txt', 'r') as f:
        high_score = int(f.read())
except FileNotFoundError:
    high_score = 0  # If the file doesn't exist, start with 0

# Countdown before the game starts
countdown_time = 3
countdown_start_time = time.time()

while countdown_time > 0:
    screen.fill(WHITE)
    countdown_text = font.render(f"Starting in {countdown_time}...", True, BLACK)
    screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 3))
    
    pygame.display.flip()
    
    if time.time() - countdown_start_time >= 1:
        countdown_time -= 1
        countdown_start_time = time.time()
    
    clock.tick(1)

# Game Loop
running = True
while running:
    screen.fill(WHITE)
    
    # Check if time is up
    elapsed_time = time.time() - start_time
    if elapsed_time >= game_duration:
        game_over_sound.play()  # Play game over sound
        running = False
        # Game Over message
        game_over_text = font.render("Game Over!", True, BLACK)
        final_score_text = font.render(f"Final Score: {score}", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2))
        
        # Wait for 3 seconds before closing the game
        pygame.display.flip()
        time.sleep(3)  # 3 seconds before exiting
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Detect mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if dino_rect.collidepoint(event.pos):  # Check if the dinosaur was clicked
                score += 1
                dino_rect.topleft = (random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100))  # Move the dino
                click_sound.play()  # Play the click sound

    # Draw the dinosaur
    screen.blit(dino_image, dino_rect)

    # Draw the score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update high score
    if score > high_score:
        high_score = score
        with open('high_score.txt', 'w') as f:
            f.write(str(high_score))

    # Display high score
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 10))

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(30)

# Quit the game
pygame.quit()
