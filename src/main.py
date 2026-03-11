import pygame
import sys
from ball import Ball
from wall import Wall


import math
# Initialize pygame
pygame.init()

# Set up display dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyGame Circle Example")
dragging_mouse = False
# Circle properties
circle_radius = 7
circle_color = (255, 0, 0)  # Red in RGB format
circle_position = (WIDTH // 2, HEIGHT // 2)  # Center of the screen


class Level:
    def __init__(self,level_number):
        self.level_number = level_number
        self.walls = []
        self.start_pos = (WIDTH/2,HEIGHT/2)
        self.hole_pos = (0,0)
        self.ball_start_velocity = (0, 0)
    def load_level(self,level_num):
        self.level_number = level_num
        self.walls = []
        
        if self.level_number == 1:
            self.start_pos = (150, 300)
            self.hole_pos = (650, 300)
            self.walls = [
                Wall(400, 150, 700, 20, screen, 0, (100, 100, 100)),
                Wall(400, 450, 700, 20, screen, 0, (100, 100, 100)),
            ]
        elif self.level_number == 2:
            self.start_pos = (150, 500)
            self.hole_pos = (650, 100)
            self.walls = [
                Wall(400, 300, 600, 20, screen, 15, (100, 100, 100)),
                Wall(400, 300, 20, 400, screen, 0, (100, 100, 100)),
            ]
        elif self.level_number == 3:
            self.start_pos = (100, 100)
            self.hole_pos = (700, 500)
            self.walls = [
                Wall(400, 250, 400, 20, screen, 45, (150, 75, 0)),
                Wall(400, 350, 400, 20, screen, -45, (150, 75, 0)),
                Wall(400, 450, 300, 20, screen, 0, (150, 75, 0)),
            ]
        elif self.level_number == 4:
            self.start_pos = (200, 300)
            self.hole_pos = (600, 300)
            self.walls = [
                Wall(300, 200, 100, 100, screen, 0, (200, 0, 0)),
                Wall(500, 200, 100, 100, screen, 0, (0, 200, 0)),
                Wall(300, 400, 100, 100, screen, 0, (0, 0, 200)),
                Wall(500, 400, 100, 100, screen, 0, (200, 200, 0)),
            ]
        elif self.level_number == 5:
            self.start_pos = (400, 500)
            self.hole_pos = (400, 100)
            self.walls = [
                Wall(400, 250, 20, 300, screen, 0, (0, 0, 0)),
                Wall(150, 300, 20, 400, screen, 0, (0, 0, 0)),
                Wall(650, 300, 20, 400, screen, 0, (0, 0, 0)),
                Wall(400, 350, 150, 20, screen, 45, (255, 0, 0)),
            ]
        elif self.level_number == 6:
            self.start_pos = (400, 500)
            self.hole_pos = (400, 100)
            for i in range(5):
                y_pos = 200 + i * 70
                width = 600 - i*100
                self.walls.append(Wall(400, y_pos, width, 15, screen, 0, (0, 0, 255 - i * 40)))

        elif self.level_number == 7:
            self.start_pos = (400, 500)
            self.hole_pos = (400, 100)
            self.walls.append(Wall(400, 200, 150, 20, screen, 45, (200, 100, 0)))
            self.walls.append(Wall(400, 200, 150, 20, screen, -45, (200, 100, 0)))
            self.walls.append(Wall(400, 350, 200, 20, screen, 90, (200, 100, 0)))
            self.walls.append(Wall(400, 450, 250, 20, screen, 0, (200, 100, 0)))

        elif self.level_number == 8:
            self.start_pos = (100, 300)
            self.hole_pos = (700, 300)
            for i in range(7):
                x_pos = 150 + i * 90
                self.walls.append(Wall(x_pos, 200, 20, 150, screen, 0, (100, 100, 100)))
                self.walls.append(Wall(x_pos, 400, 20, 150, screen, 0, (100, 100, 100)))
                
        elif self.level_number == 9:
            self.start_pos = (200, 500)
            self.hole_pos = (600, 100)
            for i in range(8):
                angle = i * 45
                self.walls.append(Wall(400, 300, 500, 20, screen, angle, (150, 0, 150)))
        elif self.level_number == 10:
            self.start_pos = (400, 500)
            self.hole_pos = (400, 100)

            self.walls.append(Wall(400, 50, 780, 20, screen, 0, (0, 0, 0)))
            self.walls.append(Wall(400, 550, 780, 20, screen, 0, (0, 0, 0)))  
            self.walls.append(Wall(50, 300, 20, 500, screen, 0, (0, 0, 0)))  
            self.walls.append(Wall(750, 300, 20, 500, screen, 0, (0, 0, 0)))  
            
            self.walls.append(Wall(400, 150, 300, 20, screen, 30, (200, 0, 0)))  
            self.walls.append(Wall(400, 250, 300, 20, screen, -30, (0, 200, 0))) 
            self.walls.append(Wall(400, 350, 300, 20, screen, 30, (0, 0, 200)))  
            self.walls.append(Wall(400, 450, 300, 20, screen, -30, (200, 200, 0))) 
            
            self.walls.append(Wall(300, 300, 150, 20, screen, 45, (200, 0, 200)))
            self.walls.append(Wall(500, 300, 150, 20, screen, -45, (0, 200, 200)))
        return self.walls
        

            
level = Level(1)
current_level = 1
max_levels = 10


#balls
player = Ball(circle_position, circle_radius, circle_color,(0,0),0.75,0.999,screen)
score_hole = Ball((60,90),15,(0,0,0),surface=screen)


walls = level.load_level(current_level)
player.position = level.start_pos
score_hole.position = level.hole_pos

running = True
level_complete = False
show_level_text = True
game_won = False
level_text_timer = 0

FPS = 60

def check_win():
    dx = player.position[0] - score_hole.position[0]
    dy = player.position[1] - score_hole.position[1]
    distance = math.sqrt(dx**2 + dy**2)
    return distance <= score_hole.radius

def next_level():
    """Load the next level"""
    global current_level, walls, game_won, level_complete, show_level_text, level_text_timer
    
    if current_level < max_levels:
        current_level += 1
        walls = level.load_level(current_level)
        player.position = level.start_pos
        player.velocity = (0, 0)
        score_hole.position = level.hole_pos
        level_complete = False
        show_level_text = True
        level_text_timer = pygame.time.get_ticks()
    else:
        game_won = True

def reset_current_level():
    """Reset the current level"""
    player.position = level.start_pos
    player.velocity = (0, 0)

while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                reset_current_level()
            elif event.key == pygame.K_n and level_complete and not game_won:
                next_level()
            elif event.key == pygame.K_r:
                reset_current_level()
            elif event.key == pygame.K_1:
                current_level = 1
                walls = level.load_level(current_level)
                player.position = level.start_pos
                score_hole.position = level.hole_pos
                game_won = False
                level_complete = False
            elif event.key == pygame.K_2:
                current_level = 2
                walls = level.load_level(current_level)
                player.position = level.start_pos
                score_hole.position = level.hole_pos
                game_won = False
                level_complete = False
            elif event.key == pygame.K_9:
                current_level = 9
                walls = level.load_level(current_level)
                player.position = level.start_pos
                score_hole.position = level.hole_pos
                game_won = False
                level_complete = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            initial_mouse_position = pygame.mouse.get_pos()
            current_mouse_position = initial_mouse_position
            dragging_mouse = True
        elif event.type == pygame.MOUSEBUTTONUP:
            final_mouse_position = pygame.mouse.get_pos()
            distance_to_ball = ((initial_mouse_position[0] - final_mouse_position[0])/40,(initial_mouse_position[1] - final_mouse_position[1])/40)
            player.velocity = distance_to_ball
            dragging_mouse = False
        elif event.type == pygame.MOUSEMOTION and dragging_mouse:
            current_mouse_position = pygame.mouse.get_pos()


            
            
    
    # Fill the screen with a background color (white)
    screen.fill((30, 255, 30))

    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)

    level_text = font.render(f"Level {current_level}/{max_levels}", True, (0, 0, 150))
    screen.blit(level_text, (10, 10))

    instr_text = small_font.render("Click and drag to aim | SPACE to reset | R to restart level", True, (100, 100, 100))
    screen.blit(instr_text, (10, 50))

    if current_level < max_levels and level_complete:
        next_text = small_font.render("Press N for next level", True, (100, 100, 100))
        screen.blit(next_text, (10, 80))
    
    for wall in walls:
        wall.draw()
    score_hole.draw()

    if not game_won:
        # Check if level is complete
        if not level_complete and check_win():
            level_complete = True
            show_level_text = True
            level_text_timer = current_time
        # Move and draw player
        player.move()
        
        # Check collisions with walls
        for wall in walls:
            player.resolve_collision(wall)
    
    if level_complete and not game_won:
        if show_level_text and current_time - level_text_timer < 2000:  # Show for 2 seconds
            complete_text = font.render(f"Level {current_level} Complete!", True, (0, 150, 0))
            text_rect = complete_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            screen.blit(complete_text, text_rect)
            
            next_prompt = small_font.render("Press N for next level", True, (0, 100, 0))
            prompt_rect = next_prompt.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(next_prompt, prompt_rect)
        else:
            show_level_text = False
    
    if game_won:
        win_text = font.render("hackclub please give me funds for pizzas!", True, (0, 150, 0))
        text_rect = win_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        screen.blit(win_text, text_rect)
    
        restart_text = small_font.render("Press 1 to play again", True, (0, 100, 0))
        restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(restart_text, restart_rect)

    

    
    if dragging_mouse and initial_mouse_position and current_mouse_position:
            pygame.draw.line(screen, (0, 255, 0), 
                            initial_mouse_position, 
                            current_mouse_position, 
                            3)  # Line width of 3 pixels
            
            # Optional: Draw circles at the endpoints for better visibility
            pygame.draw.circle(screen, (255, 100, 100), initial_mouse_position, 6)
            pygame.draw.circle(screen, (100, 255, 100), current_mouse_position, 6)



    
    # Update the display
    pygame.display.flip()
    
    # Control frame rate
    pygame.time.Clock().tick(FPS)

# Quit pygame
pygame.quit()
sys.exit()
