import pygame
import sys
import os
import random
from typing import List, Tuple



class KnightTourVisualizer:
    def __init__(self, board_config: List[List[int]], cell_size: int = None):
        """
        Initialize the Knight Tour Visualizer with dynamic board sizing
        
        :param board_config: 2D list representing the board configuration
        :param cell_size: Optional custom cell size, otherwise auto-calculated
        """
        pygame.init()
        
        # Determine board size from configuration
        self.board_config = board_config
        self.BOARD_SIZE = len(board_config)
        
        # Dynamically calculate cell size to fit screen
        if cell_size is None:
            # Get screen resolution
            infoObject = pygame.display.Info()
            screen_width = infoObject.current_w
            screen_height = infoObject.current_h
            
            # Calculate max possible cell size while keeping entire board visible
            max_cell_width = (screen_width - 200) // self.BOARD_SIZE  # Increased margin for labels
            max_cell_height = (screen_height - 200) // self.BOARD_SIZE  # Increased margin for labels
            
            # Choose the smaller dimension to ensure full visibility
            self.CELL_SIZE = min(max_cell_width, max_cell_height, 150)
        else:
            self.CELL_SIZE = cell_size
        
        # Calculate screen size with additional space for labels
        self.SCREEN_SIZE_X = self.BOARD_SIZE * self.CELL_SIZE + 100  # Add label space on sides
        self.SCREEN_SIZE_Y = self.BOARD_SIZE * self.CELL_SIZE + 100  # Add label space on top/bottom
        
        # Pygame setup with dynamic sizing
        self.screen = pygame.display.set_mode((self.SCREEN_SIZE_X, self.SCREEN_SIZE_Y))
        pygame.display.set_caption("🏇 Magical Knight's Mystical Tour 🏇")
        
        # Enhanced color palette with gradients and creativity
        self.BACKGROUND_COLOR = (30, 30, 50)  # Deep midnight blue
        self.LIGHT_SQUARE = self.gradient_color((240, 217, 181), (220, 197, 161))
        self.DARK_SQUARE = self.gradient_color((181, 136, 99), (161, 116, 79))
        
        # Particle and effect colors
        self.PARTICLE_COLORS = [
            (255, 0, 0),    # Vibrant red
            (0, 255, 0),    # Bright green
            (0, 0, 255),    # Deep blue
            (255, 165, 0),  # Orange
            (255, 0, 255),  # Magenta
            (255, 255, 0),  # Yellow
            (128, 0, 128)   # Purple
        ]
        
        # Fonts
        pygame.font.init()
        self.font = pygame.font.Font(None, int(max(24, self.CELL_SIZE // 5)))
        self.large_font = pygame.font.Font(None, int(max(48, self.CELL_SIZE // 2.5)))
        
        # Tour path and particles
        self.tour_path = self.load_tour_path()
        self.particles = []
        
        # Particle and effect management
        self.max_particles = 100
        self.particle_timer = 0
        
        # Load enhanced knight image
        self.knight_img = self.create_knight_surface()
        
        # Pygame clock for smooth animation
        self.clock = pygame.time.Clock()

        # Board drawing offsets
        self.BOARD_OFFSET_X = 50  # Space for column labels
        self.BOARD_OFFSET_Y = 50  # Space for row labels
    
    def gradient_color(self, color1, color2):
        """Create a gradient between two colors"""
        return tuple(
            int((color1[i] + color2[i]) / 2) 
            for i in range(3)
        )
    
    def create_particle(self, x, y):
        """Create a magical particle with random properties"""
        return {
            'x': x,
            'y': y,
            'color': random.choice(self.PARTICLE_COLORS),
            'size': random.randint(2, max(3, self.CELL_SIZE // 20)),
            'speed_x': random.uniform(-2, 2),
            'speed_y': random.uniform(-2, 2),
            'life': random.randint(30, 60)
        }
    
    def update_particles(self):
        """Update and render magical particles"""
        for particle in self.particles[:]:
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']
            particle['life'] -= 1
            
            # Render particle
            pygame.draw.circle(
                self.screen, 
                particle['color'], 
                (int(particle['x']), int(particle['y'])), 
                particle['size']
            )
            
            # Remove dead particles
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def create_knight_surface(self) -> pygame.Surface:
        """Create a magical knight surface with glowing effect"""
        knight_surf = pygame.Surface((self.CELL_SIZE, self.CELL_SIZE), pygame.SRCALPHA)
        
        # Mystical knight shape
        points = [
            (self.CELL_SIZE * 0.3, self.CELL_SIZE * 0.7),
            (self.CELL_SIZE * 0.7, self.CELL_SIZE * 0.7),
            (self.CELL_SIZE * 0.5, self.CELL_SIZE * 0.3)
        ]
        
        # Draw knight with gradient and glow
        pygame.draw.polygon(knight_surf, (50, 50, 200), points)
        
        # Add a glowing effect
        glow_surf = pygame.Surface((self.CELL_SIZE, self.CELL_SIZE), pygame.SRCALPHA)
        for i in range(10, 0, -1):
            glow_color = (50, 50, 200, 30 - i)
            pygame.draw.polygon(glow_surf, glow_color, 
                [tuple(p * (1 + i * 0.05) for p in point) for point in points])
        
        knight_surf.blit(glow_surf, (0, 0))
        return knight_surf
    
    def load_tour_path(self) -> List[Tuple[int, int]]:
        """
        Load the knight's tour path from path.txt
        
        :return: List of (x, y) coordinates for the knight's tour
        """
        path = []
        with open('path.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('Step'):
                    coords_str = line.split('(')[1].split(')')[0]
                    x, y = map(int, coords_str.split(','))
                    path.append((x, y))
        return path
        
    def draw_board(self):
        """Draw the chessboard with labeled rows and columns."""
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                # Rectangle position with offset for labels
                rect = pygame.Rect(
                    col * self.CELL_SIZE + self.BOARD_OFFSET_X,
                    (self.BOARD_SIZE - 1 - row) * self.CELL_SIZE + self.BOARD_OFFSET_Y,
                    self.CELL_SIZE,
                    self.CELL_SIZE
                )

                # Determine square color
                color = self.LIGHT_SQUARE if (row + col) % 2 == 0 else self.DARK_SQUARE
                pygame.draw.rect(self.screen, color, rect)

        # Draw row labels (1, 2, ..., BOARD_SIZE) on the left side
        for row in range(self.BOARD_SIZE):
            label = str(row + 1)
            text_surf = self.font.render(label, True, (255, 255, 255))
            text_rect = text_surf.get_rect(
                center=(self.BOARD_OFFSET_X // 2,
                        (self.BOARD_SIZE - 1 - row) * self.CELL_SIZE + self.BOARD_OFFSET_Y + self.CELL_SIZE // 2)
            )
            self.screen.blit(text_surf, text_rect)

        # Draw column labels (a, b, ..., BOARD_SIZE as letters) at the bottom
        for col in range(self.BOARD_SIZE):
            label = chr(ord('a') + col)
            text_surf = self.font.render(label, True, (255, 255, 255))
            text_rect = text_surf.get_rect(
                center=(col * self.CELL_SIZE + self.BOARD_OFFSET_X + self.CELL_SIZE // 2,
                        self.SCREEN_SIZE_Y - self.BOARD_OFFSET_Y // 2)
            )
            self.screen.blit(text_surf, text_rect)

    # def visualize_tour(self):
    #     """
    #     Visualize the entire knight's tour with magical step-by-step animation
    #     """
    #     for step, (x, y) in enumerate(self.tour_path):
    #         # Clear the screen with a magical background
    #         self.screen.fill(self.BACKGROUND_COLOR)
            
    #         # Draw the board
    #         self.draw_board()
            
    #         # Draw historical path
    #         for prev_step in range(step + 1):
    #             prev_x, prev_y = self.tour_path[prev_step]
                
    #             # Fade effect for historical moves
    #             opacity = int(255 * (prev_step / step)) if step > 0 else 255
    #             historical_knight = self.knight_img.copy()
    #             historical_knight.set_alpha(opacity)
                
    #             knight_rect = historical_knight.get_rect(
    #                 center=(
    #                     prev_x * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_OFFSET_X, 
    #                     (self.BOARD_SIZE - 1 - prev_y) * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_OFFSET_Y
    #                 )
    #             )
    #             self.screen.blit(historical_knight, knight_rect)
                
    #             # Draw path lines with fading
    #             if prev_step > 0:
    #                 prev_prev_x, prev_prev_y = self.tour_path[prev_step - 1]
    #                 line_surface = pygame.Surface((self.SCREEN_SIZE_X, self.SCREEN_SIZE_Y), pygame.SRCALPHA)
    #                 pygame.draw.line(
    #                     line_surface, 
    #                     (*self.PARTICLE_COLORS[prev_step % len(self.PARTICLE_COLORS)], opacity),
    #                     (prev_prev_x * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_OFFSET_X, 
    #                      (self.BOARD_SIZE - 1 - prev_prev_y) * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_OFFSET_Y),
    #                     (prev_x * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_OFFSET_X, 
    #                      (self.BOARD_SIZE - 1 - prev_y) * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_OFFSET_Y),
    #                     5
    #                 )
    #                 self.screen.blit(line_surface, (0, 0))
            
    #         # Generate magical particles
    #         center_x = x * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_OFFSET_X
    #         center_y = (self.BOARD_SIZE - 1 - y) * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_OFFSET_Y
            
    #         # Add new particles
    #         if len(self.particles) < self.max_particles:
    #             for _ in range(random.randint(10, 20)):
    #                 particle = self.create_particle(center_x, center_y)
    #                 self.particles.append(particle)
            
    #         # Update and draw particles
    #         self.update_particles()
            
    #         # Draw step number with magical styling
    #         step_text = self.large_font.render(f"Step {step + 1}", True, (255, 255, 255))
    #         self.screen.blit(step_text, (10, 10))
            
    #         # Update display
    #         pygame.display.flip()
            
            
    #         # Smooth animation
    #         self.clock.tick(120)  # 120 FPS for detailed observation
            
    #         # Event handling
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 sys.exit()
        
    #     # Keep window open after tour is complete
    #     waiting = True
    #     while waiting:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 waiting = False
        
    #     pygame.quit()
    
    def visualize_tour(self):
        """
        Visualize the entire knight's tour with cleaner path lines and black step numbers
        """
        for step, (x, y) in enumerate(self.tour_path):
            # Clear the screen with a magical background
            self.screen.fill(self.BACKGROUND_COLOR)
            
            # Draw the board
            self.draw_board()
            
            # Draw historical path with step numbers
            for prev_step in range(step + 1):
                prev_x, prev_y = self.tour_path[prev_step]
                
                # Fade effect for historical moves (including numbers)
                opacity = int(255 * (0.3 + 0.7 * (prev_step / step))) if step > 0 else 255
                
                # Draw faded knight image
                historical_knight = self.knight_img.copy()
                historical_knight.set_alpha(opacity)
                knight_rect = historical_knight.get_rect(
                    center=(
                        prev_x * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_OFFSET_X, 
                        (self.BOARD_SIZE - 1 - prev_y) * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_OFFSET_Y
                    )
                )
                self.screen.blit(historical_knight, knight_rect)
                
                # Draw step number with fading (black text)
                step_num = str(prev_step + 1)
                step_surface = pygame.Surface((self.CELL_SIZE, self.CELL_SIZE), pygame.SRCALPHA)
                
                # Render black text with opacity
                text_surf = self.font.render(step_num, True, (0, 0, 0, opacity))  # Black text
                text_rect = text_surf.get_rect(
                    center=(self.CELL_SIZE // 2, self.CELL_SIZE // 2)
                )
                
                # Draw semi-transparent white background for better visibility
                bg_rect = pygame.Rect(
                    text_rect.x - 5, 
                    text_rect.y - 2, 
                    text_rect.width + 10, 
                    text_rect.height + 4
                )
                pygame.draw.rect(
                    step_surface, 
                    (255, 255, 255, opacity // 2),  # Semi-transparent white bg
                    bg_rect, 
                    border_radius=3
                )
                
                step_surface.blit(text_surf, text_rect)
                
                # Position the step number surface on the board
                self.screen.blit(
                    step_surface,
                    (
                        prev_x * self.CELL_SIZE + self.BOARD_OFFSET_X,
                        (self.BOARD_SIZE - 1 - prev_y) * self.CELL_SIZE + self.BOARD_OFFSET_Y
                    )
                )
                
                # Draw path lines with fading - only draw up to current step
                if prev_step > 0 and prev_step < step:  # Changed condition
                    prev_prev_x, prev_prev_y = self.tour_path[prev_step - 1]
                    line_surface = pygame.Surface((self.SCREEN_SIZE_X, self.SCREEN_SIZE_Y), pygame.SRCALPHA)
                    pygame.draw.line(
                        line_surface, 
                        (*self.PARTICLE_COLORS[prev_step % len(self.PARTICLE_COLORS)], opacity),
                        (prev_prev_x * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_OFFSET_X, 
                        (self.BOARD_SIZE - 1 - prev_prev_y) * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_OFFSET_Y),
                        (prev_x * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_OFFSET_X, 
                        (self.BOARD_SIZE - 1 - prev_y) * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_OFFSET_Y),
                        3  # Thinner line
                    )
                    self.screen.blit(line_surface, (0, 0))
            
            # Generate magical particles only for current step
            if step < len(self.tour_path) - 1:  # Don't show particles on final step
                center_x = x * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_OFFSET_X
                center_y = (self.BOARD_SIZE - 1 - y) * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_OFFSET_Y
                
                # Add new particles
                if len(self.particles) < self.max_particles:
                    for _ in range(random.randint(5, 10)):  # Fewer particles
                        particle = self.create_particle(center_x, center_y)
                        self.particles.append(particle)
            
            # Update and draw particles
            self.update_particles()
            
            # Draw current step counter
            step_text = self.large_font.render(f"Step {step + 1}/{len(self.tour_path)}", True, (255, 255, 255))
            self.screen.blit(step_text, (10, 10))
            
            # Special display for final step
            if step == len(self.tour_path) - 1:
                # Draw all path lines in a single color with full opacity
                line_surface = pygame.Surface((self.SCREEN_SIZE_X, self.SCREEN_SIZE_Y), pygame.SRCALPHA)
                for i in range(1, len(self.tour_path)):
                    prev_x, prev_y = self.tour_path[i-1]
                    curr_x, curr_y = self.tour_path[i]
                    pygame.draw.line(
                        line_surface,
                        (50, 200, 50, 200),  # Consistent green color
                        (prev_x * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_OFFSET_X,
                        (self.BOARD_SIZE - 1 - prev_y) * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_OFFSET_Y),
                        (curr_x * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_OFFSET_X,
                        (self.BOARD_SIZE - 1 - curr_y) * self.CELL_SIZE + self.CELL_SIZE // 2 + self.BOARD_OFFSET_Y),
                        3
                    )
                self.screen.blit(line_surface, (0, 0))
                
                # Display completion message
                complete_text = self.large_font.render("TOUR COMPLETE!", True, (255, 255, 0))
                text_rect = complete_text.get_rect(center=(self.SCREEN_SIZE_X//2, 30))
                self.screen.blit(complete_text, text_rect)
            
            # Update display
            pygame.display.flip()
            
            # Smooth animation - slower on final step
            self.clock.tick(60 if step == len(self.tour_path) - 1 else 120)
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
        # Keep window open after tour is complete
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
        
        pygame.quit()

def main():
    # Read the board configuration
    with open('board.txt', 'r') as f:
        board_config = [list(map(int, line.split())) for line in f.readlines()]
    
    # Initialize and run visualization
    visualizer = KnightTourVisualizer(board_config)
    visualizer.visualize_tour()

if __name__ == "__main__":
    main()