"""
Empire 3D - Main Game Loop
This module contains the primary game loop for the Empire 3D game.
Handles initialization, event processing, rendering, and game state management.
"""

import pygame
import sys
from enum import Enum
from typing import Optional


class GameState(Enum):
    """Enumeration for different game states."""
    INITIALIZING = 1
    MENU = 2
    PLAYING = 3
    PAUSED = 4
    GAME_OVER = 5
    QUIT = 6


class Empire3DGame:
    """Main game class managing the Empire 3D game loop."""
    
    # Game window constants
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    TARGET_FPS = 60
    
    def __init__(self):
        """Initialize the game engine and window."""
        pygame.init()
        
        # Window setup
        self.display = pygame.display.set_mode(
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        )
        pygame.display.set_caption("Empire 3D")
        
        # Clock for FPS management
        self.clock = pygame.time.Clock()
        self.fps = 0
        self.frame_count = 0
        self.fps_update_timer = 0
        
        # Game state management
        self.current_state = GameState.INITIALIZING
        self.running = True
        self.is_paused = False
        
        # Game timing
        self.delta_time = 0.0
        self.total_time = 0.0
        
        # Font for FPS display
        self.font_small = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 48)
        
        # Initialize game modules (placeholder for future game systems)
        self._initialize_game_systems()
        
        # Set initial state
        self.current_state = GameState.MENU
    
    def _initialize_game_systems(self) -> None:
        """Initialize all game systems and modules."""
        # TODO: Import and initialize game modules
        # - MapManager
        # - EntityManager
        # - RenderingEngine
        # - AISystem
        # - InputManager
        pass
    
    def handle_events(self) -> None:
        """Handle all input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.current_state = GameState.QUIT
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                self._handle_key_down(event)
            
            elif event.type == pygame.KEYUP:
                self._handle_key_up(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_down(event)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouse_up(event)
            
            elif event.type == pygame.MOUSEMOTION:
                self._handle_mouse_motion(event)
    
    def _handle_key_down(self, event: pygame.event.Event) -> None:
        """Handle key press events."""
        if event.key == pygame.K_ESCAPE:
            if self.current_state == GameState.PLAYING:
                self.current_state = GameState.PAUSED
                self.is_paused = True
            elif self.current_state == GameState.PAUSED:
                self.current_state = GameState.PLAYING
                self.is_paused = False
            else:
                self.running = False
        
        elif event.key == pygame.K_F1:
            # Debug key - placeholder
            pass
        
        # Game-specific key handling
        if self.current_state == GameState.PLAYING:
            # TODO: Add game-specific input handling
            # - Camera movement (WASD)
            # - Unit selection/commands
            # - Building placement
            # - Menu interactions
            pass
    
    def _handle_key_up(self, event: pygame.event.Event) -> None:
        """Handle key release events."""
        # TODO: Handle key release events for smooth movement
        pass
    
    def _handle_mouse_down(self, event: pygame.event.Event) -> None:
        """Handle mouse button press events."""
        if event.button == 1:  # Left click
            # TODO: Handle unit/building selection
            pass
        elif event.button == 3:  # Right click
            # TODO: Handle unit movement/commands
            pass
    
    def _handle_mouse_up(self, event: pygame.event.Event) -> None:
        """Handle mouse button release events."""
        pass
    
    def _handle_mouse_motion(self, event: pygame.event.Event) -> None:
        """Handle mouse movement events."""
        # TODO: Handle camera panning/scrolling at screen edges
        pass
    
    def update(self, delta_time: float) -> None:
        """Update game logic based on current state."""
        self.delta_time = delta_time
        self.total_time += delta_time
        
        if self.current_state == GameState.PLAYING and not self.is_paused:
            # TODO: Update game systems
            # - Update entity positions
            # - Update AI logic
            # - Update animations
            # - Check for collisions
            # - Check win/lose conditions
            pass
        
        elif self.current_state == GameState.MENU:
            # TODO: Update menu logic
            pass
        
        elif self.current_state == GameState.PAUSED:
            # Game is paused - minimal updates
            pass
        
        elif self.current_state == GameState.GAME_OVER:
            # TODO: Handle game over state
            pass
    
    def render(self) -> None:
        """Render the game frame."""
        # Clear screen
        self.display.fill((20, 20, 30))  # Dark blue background
        
        # Render based on game state
        if self.current_state == GameState.MENU:
            self._render_menu()
        
        elif self.current_state == GameState.PLAYING:
            self._render_game()
        
        elif self.current_state == GameState.PAUSED:
            self._render_game()  # Render game underneath
            self._render_pause_overlay()
        
        elif self.current_state == GameState.GAME_OVER:
            self._render_game_over()
        
        # Always render HUD elements
        self._render_hud()
        
        # Update display
        pygame.display.flip()
    
    def _render_menu(self) -> None:
        """Render main menu screen."""
        title_text = self.font_large.render(
            "Empire 3D", True, (255, 200, 100)
        )
        title_rect = title_text.get_rect(
            center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 3)
        )
        self.display.blit(title_text, title_rect)
        
        start_text = self.font_small.render(
            "Press any key to start or ESCAPE to quit", True, (200, 200, 200)
        )
        start_rect = start_text.get_rect(
            center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2)
        )
        self.display.blit(start_text, start_rect)
    
    def _render_game(self) -> None:
        """Render the main game world."""
        # TODO: Render game world
        # - Render 3D map/terrain
        # - Render entities (units, buildings)
        # - Render UI elements
        # - Render selection boxes
        # - Render build previews
        
        # Placeholder: render grid pattern
        grid_color = (50, 50, 70)
        grid_spacing = 50
        
        for x in range(0, self.WINDOW_WIDTH, grid_spacing):
            pygame.draw.line(
                self.display, grid_color,
                (x, 0), (x, self.WINDOW_HEIGHT)
            )
        
        for y in range(0, self.WINDOW_HEIGHT, grid_spacing):
            pygame.draw.line(
                self.display, grid_color,
                (0, y), (self.WINDOW_WIDTH, y)
            )
    
    def _render_pause_overlay(self) -> None:
        """Render pause menu overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.display.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.font_large.render("PAUSED", True, (255, 100, 100))
        pause_rect = pause_text.get_rect(
            center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2)
        )
        self.display.blit(pause_text, pause_rect)
        
        # Resume instructions
        resume_text = self.font_small.render(
            "Press ESC to resume", True, (200, 200, 200)
        )
        resume_rect = resume_text.get_rect(
            center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 50)
        )
        self.display.blit(resume_text, resume_rect)
    
    def _render_game_over(self) -> None:
        """Render game over screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.display.blit(overlay, (0, 0))
        
        # Game Over text
        gameover_text = self.font_large.render(
            "GAME OVER", True, (255, 50, 50)
        )
        gameover_rect = gameover_text.get_rect(
            center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 50)
        )
        self.display.blit(gameover_text, gameover_rect)
        
        # Restart instructions
        restart_text = self.font_small.render(
            "Press any key to return to menu or ESCAPE to quit",
            True, (200, 200, 200)
        )
        restart_rect = restart_text.get_rect(
            center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 50)
        )
        self.display.blit(restart_text, restart_rect)
    
    def _render_hud(self) -> None:
        """Render heads-up display (HUD) elements."""
        self._render_fps_counter()
        self._render_game_info()
    
    def _render_fps_counter(self) -> None:
        """Render FPS counter in top-left corner."""
        fps_text = self.font_small.render(
            f"FPS: {self.fps}", True, (100, 255, 100)
        )
        self.display.blit(fps_text, (10, 10))
    
    def _render_game_info(self) -> None:
        """Render game information on HUD."""
        info_texts = [
            f"State: {self.current_state.name}",
            f"Time: {self.total_time:.1f}s",
        ]
        
        y_offset = 40
        for text_str in info_texts:
            text_surface = self.font_small.render(
                text_str, True, (200, 200, 200)
            )
            self.display.blit(text_surface, (10, y_offset))
            y_offset += 25
    
    def _update_fps(self) -> None:
        """Update FPS counter."""
        self.frame_count += 1
        self.fps_update_timer += self.delta_time
        
        if self.fps_update_timer >= 1.0:
            self.fps = self.frame_count
            self.frame_count = 0
            self.fps_update_timer = 0.0
    
    def run(self) -> None:
        """Main game loop."""
        print("=" * 50)
        print("Empire 3D Game Started")
        print(f"Window Size: {self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        print(f"Target FPS: {self.TARGET_FPS}")
        print("=" * 50)
        
        while self.running:
            # Handle all events
            self.handle_events()
            
            # Calculate delta time
            delta_time = self.clock.tick(self.TARGET_FPS) / 1000.0
            self._update_fps()
            
            # Update game logic
            self.update(delta_time)
            
            # Render frame
            self.render()
        
        self.shutdown()
    
    def shutdown(self) -> None:
        """Clean up and shut down the game."""
        print("Shutting down game...")
        # TODO: Save game state if needed
        # TODO: Clean up resources
        pygame.quit()
        sys.exit()


def main():
    """Entry point for the game."""
    try:
        game = Empire3DGame()
        game.run()
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()
