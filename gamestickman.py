import pygame
import sys
import random

# Initialisatie
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ultimate Stickman Adventure - Collect All Coins")
clock = pygame.time.Clock()

# Kleuren
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)
PURPLE = (128, 0, 128)

# Game variabelen
score = 0
lives = 3
game_time = 60
level_time = 0
current_level = 0
game_state = "playing"  # "playing", "level_complete", "game_over", "game_win"
font = pygame.font.SysFont('Arial', 24)
big_font = pygame.font.SysFont('Arial', 48)

# Stickman variabelen
stickman_x = 100
stickman_y = 300
stickman_width = 20
stickman_height = 40
stickman_vel_y = 0
stickman_jump = False
stickman_speed = 5
is_invincible = False
invincible_timer = 0

# Zwaartekracht
gravity = 0.5

# Levels
levels = [
    # Level 1 (beginner)
    {
        "platforms": [
            {"x": 0, "y": 550, "width": 300, "height": 20},
            {"x": 350, "y": 550, "width": 450, "height": 20},
            {"x": 300, "y": 450, "width": 200, "height": 20},
            {"x": 500, "y": 350, "width": 200, "height": 20}
        ],
        "target": {"x": 700, "y": 300, "width": 30, "height": 30},
        "coins": [{"x": 150, "y": 500}, {"x": 400, "y": 400}, {"x": 600, "y": 300}],
        "enemies": [{"x": 200, "y": 530, "width": 30, "height": 20, "speed": 2}],
        "start": (100, 300),
        "time_limit": 60,
        "required_coins": 3  # Alle 3 coins moeten worden verzameld
    },
    
    # Level 2 (medium)
    {
        "platforms": [
            {"x": 0, "y": 550, "width": 200, "height": 20},
            {"x": 300, "y": 500, "width": 200, "height": 20},
            {"x": 200, "y": 400, "width": 150, "height": 20},
            {"x": 400, "y": 350, "width": 150, "height": 20},
            {"x": 600, "y": 300, "width": 200, "height": 20}
        ],
        "target": {"x": 700, "y": 250, "width": 30, "height": 30},
        "coins": [{"x": 250, "y": 450}, {"x": 350, "y": 400}, {"x": 450, "y": 300}, {"x": 650, "y": 250}],
        "enemies": [
            {"x": 250, "y": 480, "width": 30, "height": 20, "speed": 3},
            {"x": 450, "y": 330, "width": 30, "height": 20, "speed": 2}
        ],
        "start": (100, 300),
        "time_limit": 45,
        "required_coins": 4  # Alle 4 coins moeten worden verzameld
    },
    
    # Level 3 (expert)
    {
        "platforms": [
            {"x": 0, "y": 550, "width": 100, "height": 20},
            {"x": 150, "y": 500, "width": 100, "height": 20},
            {"x": 300, "y": 450, "width": 100, "height": 20},
            {"x": 450, "y": 400, "width": 100, "height": 20},
            {"x": 600, "y": 350, "width": 100, "height": 20},
            {"x": 200, "y": 300, "width": 100, "height": 20},
            {"x": 350, "y": 250, "width": 100, "height": 20},
            {"x": 500, "y": 200, "width": 100, "height": 20}
        ],
        "target": {"x": 650, "y": 150, "width": 30, "height": 30},
        "coins": [{"x": 100, "y": 500}, {"x": 200, "y": 450}, {"x": 350, "y": 400}, 
                 {"x": 500, "y": 350}, {"x": 650, "y": 300}, {"x": 250, "y": 250}],
        "enemies": [
            {"x": 100, "y": 530, "width": 30, "height": 20, "speed": 4},
            {"x": 350, "y": 430, "width": 30, "height": 20, "speed": 3},
            {"x": 600, "y": 330, "width": 30, "height": 20, "speed": 2}
        ],
        "start": (100, 300),
        "time_limit": 30,
        "required_coins": 6  # Alle 6 coins moeten worden verzameld
    }
]

def reset_level():
    global stickman_x, stickman_y, stickman_vel_y, stickman_jump, level_time
    stickman_x, stickman_y = levels[current_level]["start"]
    stickman_vel_y = 0
    stickman_jump = False
    level_time = 0

    # Herstel de coins uit de backup, of maak een backup als die er nog niet is
    if "coins_before_level" in levels[current_level]:
        levels[current_level]["coins"] = levels[current_level]["coins_before_level"][:]
    else:
        levels[current_level]["coins_before_level"] = levels[current_level]["coins"][:]



reset_level()

def draw_stickman(x, y, invincible=False):
    color = PURPLE if invincible else BLACK
    pygame.draw.circle(screen, color, (x + stickman_width // 2, y + 10), 10)
    pygame.draw.line(screen, color, (x + stickman_width // 2, y + 20), 
                    (x + stickman_width // 2, y + 40), 2)
    # Armen
    pygame.draw.line(screen, color, (x + stickman_width // 2, y + 25), 
                    (x, y + 35), 2)
    pygame.draw.line(screen, color, (x + stickman_width // 2, y + 25), 
                    (x + stickman_width, y + 35), 2)
    # Benen
    pygame.draw.line(screen, color, (x + stickman_width // 2, y + 40), 
                    (x, y + 55), 2)
    pygame.draw.line(screen, color, (x + stickman_width // 2, y + 40), 
                    (x + stickman_width, y + 55), 2)

# Game loop
running = True
while running:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not stickman_jump and game_state == "playing":
                stickman_vel_y = -12
                stickman_jump = True
            if event.key == pygame.K_r and game_state != "playing":
                if game_state == "level_complete":
                    current_level += 1
                    if current_level >= len(levels):
                        current_level = 0
                        game_state = "game_win"
                    else:
                        reset_level()
                        game_state = "playing"
                else:
                    reset_level()
                    game_state = "playing"
                    lives = 3
                    score = 0
                    current_level = 0
    
    if game_state == "playing":
        level_time += dt
        game_time = levels[current_level]["time_limit"] - level_time
        
        if game_time <= 0:
            game_state = "game_over"
        
        # Beweging
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            stickman_x -= stickman_speed
        if keys[pygame.K_RIGHT]:
            stickman_x += stickman_speed
        
        # Zwaartekracht toepassen
        stickman_vel_y += gravity
        stickman_y += stickman_vel_y
        
        # Collision detection met platforms
        stickman_jump = True
        current_platforms = levels[current_level]["platforms"]
        for platform in current_platforms:
            if (stickman_y + stickman_height >= platform["y"] and 
                stickman_y + stickman_height <= platform["y"] + platform["height"] and 
                stickman_x + stickman_width >= platform["x"] and 
                stickman_x <= platform["x"] + platform["width"] and 
                stickman_vel_y > 0):
                
                stickman_y = platform["y"] - stickman_height
                stickman_vel_y = 0
                stickman_jump = False
        
        # Check coins
        for coin in levels[current_level]["coins"][:]:
            if (stickman_x + stickman_width >= coin["x"] and 
                stickman_x <= coin["x"] + 20 and 
                stickman_y + stickman_height >= coin["y"] and 
                stickman_y <= coin["y"] + 20):
                
                levels[current_level]["coins"].remove(coin)
                score += 100
        
        # Update enemies
        for enemy in levels[current_level]["enemies"]:
            enemy["x"] += enemy["speed"]
            if enemy["x"] <= 0 or enemy["x"] >= screen_width - enemy["width"]:
                enemy["speed"] *= -1
        
        # Check enemy collision
        if not is_invincible:
            for enemy in levels[current_level]["enemies"]:
                if (stickman_x + stickman_width >= enemy["x"] and 
                    stickman_x <= enemy["x"] + enemy["width"] and 
                    stickman_y + stickman_height >= enemy["y"] and 
                    stickman_y <= enemy["y"] + enemy["height"]):
                    
                    lives -= 1
                    is_invincible = True
                    invincible_timer = 2.0  # 2 seconds invincibility
                    if lives <= 0:
                        game_state = "game_over"
                        current_level = 0
                    break
        
        # Update invincibility
        if is_invincible:
            invincible_timer -= dt
            if invincible_timer <= 0:
                is_invincible = False
        
        # Check of doel is bereikt (alleen als alle coins zijn verzameld)
        target = levels[current_level]["target"]
        coins_collected = len(levels[current_level]["coins_before_level"]) - len(levels[current_level]["coins"]) if "coins_before_level" in levels[current_level] else 0
        if (coins_collected >= levels[current_level]["required_coins"] and
            stickman_x + stickman_width >= target["x"] and 
            stickman_x <= target["x"] + target["width"] and 
            stickman_y + stickman_height >= target["y"] and 
            stickman_y <= target["y"] + target["height"]):
            
            # Bonus score voor overgebleven tijd
            score += int(game_time * 10)
            game_state = "level_complete"
        elif (stickman_x + stickman_width >= target["x"] and 
              stickman_x <= target["x"] + target["width"] and 
              stickman_y + stickman_height >= target["y"] and 
              stickman_y <= target["y"] + target["height"]):
            # Toon bericht dat niet alle coins zijn verzameld
            game_state = "missing_coins"
            missing_coins_time = 1.0  # Toon bericht voor 1 seconde
        
        # Schermgrenzen
        if stickman_x < 0:
            stickman_x = 0
        if stickman_x > screen_width - stickman_width:
            stickman_x = screen_width - stickman_width
        if stickman_y > screen_height:
            lives -= 1
            if lives <= 0:
                game_state = "game_over"
            else:
                reset_level()
    
    # Tekenen
    screen.fill(WHITE)
    
    # Teken huidig level
    level = levels[current_level]
    
    # Teken platforms
    for platform in level["platforms"]:
        pygame.draw.rect(screen, BLUE, (platform["x"], platform["y"], platform["width"], platform["height"]))
    
    # Teken doel
    pygame.draw.rect(screen, GREEN, (level["target"]["x"], level["target"]["y"], 
                     level["target"]["width"], level["target"]["height"]))
    
    # Teken coins
    for coin in level["coins"]:
        pygame.draw.circle(screen, GOLD, (coin["x"] + 10, coin["y"] + 10), 10)
    
    # Teken enemies
    for enemy in level["enemies"]:
        pygame.draw.rect(screen, RED, (enemy["x"], enemy["y"], enemy["width"], enemy["height"]))
    
    # Teken stickman
    draw_stickman(stickman_x, stickman_y, is_invincible)
    
    # Bereken verzamelde coins
    initial_coins = level["required_coins"]
    remaining_coins = len(level["coins"])
    coins_collected = initial_coins - remaining_coins
    
    # Teken HUD
    score_text = font.render(f"Score: {score}", True, BLACK)
    lives_text = font.render(f"Lives: {lives}", True, BLACK)
    level_text = font.render(f"Level: {current_level + 1}/{len(levels)}", True, BLACK)
    time_text = font.render(f"Time: {max(0, int(game_time))}", True, BLACK)
    coins_text = font.render(f"Coins: {coins_collected}/{level['required_coins']}", True, BLACK)
    
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))
    screen.blit(level_text, (10, 70))
    screen.blit(time_text, (10, 100))
    screen.blit(coins_text, (10, 130))
    
    # Teken game state berichten
    if game_state == "level_complete":
        if current_level + 1 >= len(levels):
            win_text = big_font.render("YOU WIN! Final Score: " + str(score), True, GREEN)
            screen.blit(win_text, (screen_width//2 - 200, screen_height//2 - 50))
            restart_text = font.render("Press R to play again", True, BLACK)
            screen.blit(restart_text, (screen_width//2 - 100, screen_height//2 + 20))
        else:
            complete_text = big_font.render(f"Level {current_level + 1} Complete!", True, GREEN)
            screen.blit(complete_text, (screen_width//2 - 150, screen_height//2 - 50))
            next_text = font.render("Press R for next level", True, BLACK)
            screen.blit(next_text, (screen_width//2 - 100, screen_height//2 + 20))
    elif game_state == "game_over":
        over_text = big_font.render("Game Over!", True, RED)
        screen.blit(over_text, (screen_width//2 - 100, screen_height//2 - 50))
        restart_text = font.render("Press R to restart", True, BLACK)
        screen.blit(restart_text, (screen_width//2 - 80, screen_height//2 + 20))
    elif game_state == "game_win":
        win_text = big_font.render("YOU WIN! Final Score: " + str(score), True, GREEN)
        screen.blit(win_text, (screen_width//2 - 200, screen_height//2 - 50))
        restart_text = font.render("Press R to play again", True, BLACK)
        screen.blit(restart_text, (screen_width//2 - 100, screen_height//2 + 20))
    elif game_state == "missing_coins":
        missing_text = big_font.render("Collect all coins first!", True, RED)
        screen.blit(missing_text, (screen_width//2 - 180, screen_height//2 - 50))
        missing_coins_time -= dt
        if missing_coins_time <= 0:
            game_state = "playing"
    
    pygame.display.flip()

pygame.quit()
sys.exit()
