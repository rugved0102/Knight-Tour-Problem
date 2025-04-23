import pygame
import sys

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (30, 144, 255)
LIGHT_BLUE = (100, 149, 237)
RED = (255, 69, 58)

# Screen Dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Input Variables
board_size = ""
time_limit = ""
error_message = ""

def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def draw_button(text, x, y, width, height, color, hover_color, action=None):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height), border_radius=10)
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height), border_radius=10)
    
    draw_text(text, font, WHITE, x + 20, y + 10)

def validate_input():
    global error_message
    try:
        size = int(board_size)
        time = float(time_limit)
        if size < 5 or size > 12 or time <= 0:
            error_message = "Invalid Input! Board size (5-12) & Time > 0"
        else:
            error_message = "Starting Knight's Tour..."
            print(f"Board Size: {size}, Time Limit: {time}s")
            # Here you can call your visualization function
    except ValueError:
        error_message = "Invalid Input! Enter numbers only."

def main():
    global board_size, time_limit, error_message
    
    clock = pygame.time.Clock()
    input_active = "board_size"
    
    # Initialize screen
    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Knight's Tour Setup")
    
    while True:
        screen.fill(BLACK)
        draw_text("Knight's Tour Setup", large_font, LIGHT_BLUE, 120, 30)
        draw_text("Board Size (5-12):", font, WHITE, 80, 150)
        draw_text("Time Limit (seconds):", font, WHITE, 80, 220)
        
        # Draw input boxes
        pygame.draw.rect(screen, LIGHT_BLUE if input_active == "board_size" else WHITE, (340, 145, 150, 40), border_radius=5)
        pygame.draw.rect(screen, LIGHT_BLUE if input_active == "time_limit" else WHITE, (340, 215, 150, 40), border_radius=5)
        
        draw_text(board_size, font, BLACK, 350, 150)
        draw_text(time_limit, font, BLACK, 350, 220)
        
        # Display error message
        if error_message:
            draw_text(error_message, font, RED, 80, 280)
        
        # Draw Start Button
        draw_button("Start Tour", 220, 330, 160, 50, BLUE, LIGHT_BLUE, validate_input)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 340 <= event.pos[0] <= 490 and 145 <= event.pos[1] <= 185:
                    input_active = "board_size"
                elif 340 <= event.pos[0] <= 490 and 215 <= event.pos[1] <= 255:
                    input_active = "time_limit"
            elif event.type == pygame.KEYDOWN:
                if input_active == "board_size":
                    if event.key == pygame.K_BACKSPACE:
                        board_size = board_size[:-1]
                    elif event.unicode.isdigit():
                        board_size += event.unicode
                elif input_active == "time_limit":
                    if event.key == pygame.K_BACKSPACE:
                        time_limit = time_limit[:-1]
                    elif event.unicode.isdigit() or event.unicode == '.':
                        time_limit += event.unicode
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
