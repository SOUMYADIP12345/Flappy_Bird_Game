import pygame
import random

pygame.init()

# Screen setup
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Jet")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BORDER_COLOR = (0, 200, 255)
BACKGROUND_COLOR = (30, 30, 30)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)

# Bird (jet) properties
bird_x = 70
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0
gravity = 0.5
flap_strength = -7

# Pipe properties
PIPE_WIDTH = 70
PIPE_GAP = 180
pipe_velocity = -3
pipes = []

# Game variables
score = 0
high_score = 0
clock = pygame.time.Clock()
flap_cooldown = 0

def draw_stylish_border():
    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 8)

def draw_jet_bird(x, y):
    # Airplane structure (triangle body with wings)
    pygame.draw.polygon(screen, YELLOW, [(x, y), (x - 20, y + 10), (x - 20, y - 10)])  # body
    pygame.draw.rect(screen, RED, (x - 18, y - 5, 10, 10))  # tail fin
    pygame.draw.line(screen, WHITE, (x - 10, y - 10), (x - 30, y - 20), 3)  # top wing
    pygame.draw.line(screen, WHITE, (x - 10, y + 10), (x - 30, y + 20), 3)  # bottom wing

def draw_pipes():
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe['top'], border_radius=8)
        pygame.draw.rect(screen, GREEN, pipe['bottom'], border_radius=8)

def check_collision():
    bird_rect = pygame.Rect(bird_x - 20, bird_y - 10, 40, 20)  # Adjust for airplane size
    for pipe in pipes:
        if bird_rect.colliderect(pipe['top']) or bird_rect.colliderect(pipe['bottom']):
            return True
    if bird_y > SCREEN_HEIGHT or bird_y < 0:
        return True
    return False

def update_pipes():
    global score
    for pipe in pipes[:]:
        pipe['top'].x += pipe_velocity
        pipe['bottom'].x += pipe_velocity
        if pipe['top'].x + PIPE_WIDTH < 0:
            pipes.remove(pipe)
            score += 1
    if len(pipes) == 0 or pipes[-1]['top'].x < SCREEN_WIDTH - 200:
        pipe_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        pipes.append({
            'top': pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, pipe_height),
            'bottom': pygame.Rect(SCREEN_WIDTH, pipe_height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - pipe_height - PIPE_GAP)
        })

def game_over_screen():
    global high_score
    if score > high_score:
        high_score = score

    font_large = pygame.font.SysFont("comicsansms", 48)
    font_small = pygame.font.SysFont("comicsansms", 32)

    screen.fill(BACKGROUND_COLOR)
    draw_stylish_border()
    over_text = font_large.render("GAME OVER", True, RED)
    screen.blit(over_text, (SCREEN_WIDTH // 2 - over_text.get_width() // 2, 150))

    score_text = font_small.render(f"Score: {score}", True, WHITE)
    high_score_text = font_small.render(f"Highest: {high_score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 230))
    screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 270))

    # Buttons
    play_again_btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, 350, 200, 50)
    exit_btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, 420, 200, 50)
    pygame.draw.rect(screen, GREEN, play_again_btn, border_radius=12)
    pygame.draw.rect(screen, RED, exit_btn, border_radius=12)

    play_again_text = font_small.render("PLAY AGAIN", True, BLACK)
    exit_text = font_small.render("EXIT", True, BLACK)
    screen.blit(play_again_text, (play_again_btn.centerx - play_again_text.get_width() // 2, play_again_btn.centery - 15))
    screen.blit(exit_text, (exit_btn.centerx - exit_text.get_width() // 2, exit_btn.centery - 15))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_btn.collidepoint(event.pos):
                    return True
                if exit_btn.collidepoint(event.pos):
                    pygame.quit()
                    exit()

# Main game loop
def game_loop():
    global bird_y, bird_velocity, pipes, score, flap_cooldown
    bird_y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0
    flap_cooldown = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and flap_cooldown <= 0:
                    bird_velocity = flap_strength
                    flap_cooldown = 10
            if event.type == pygame.MOUSEBUTTONDOWN and flap_cooldown <= 0:
                bird_velocity = flap_strength
                flap_cooldown = 10

        bird_velocity += gravity
        bird_y += bird_velocity

        update_pipes()

        if check_collision():
            if not game_over_screen():
                running = False
                break
            else:
                game_loop()  # Restart if play again

        if flap_cooldown > 0:
            flap_cooldown -= 1

        screen.fill(BACKGROUND_COLOR)
        draw_stylish_border()
        draw_pipes()
        draw_jet_bird(bird_x, bird_y)

        font = pygame.font.SysFont("comicsansms", 32)
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

game_loop()
