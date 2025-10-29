"""
main_menu_scene.py - Cena do menu principal
"""
import pygame
from src.scenes.base_scene import Scene
from src.components.button import Button
from src.utils.constants import SceneType, BUTTON_SIZE

class MainMenuScene(Scene):
    """Menu principal do jogo"""
    
    def __init__(self, screen, assets):
        super().__init__(screen, assets)
        self.background = assets.get_image('main_menu_bg')
        self.buttons = {}
        self._setup_buttons()
    
    def _setup_buttons(self):
        """Configura os botões do menu principal"""
        screen_width = self.screen.get_width()
        screen_center_x = screen_width // 2
        
        # Posições Y dos botões (sem RULES)
        button_y_positions = {
            'start': 695,
            'menu': 800,
            'options': 905,
        }
        
        # Cria os botões
        self.buttons = {
            'start': Button(
                self.assets.get_scaled_image('start_button', BUTTON_SIZE),
                screen_center_x,
                button_y_positions['start'],
                'start'
            ),
            'menu': Button(
                self.assets.get_scaled_image('menu_button', BUTTON_SIZE),
                screen_center_x,
                button_y_positions['menu'],
                'menu'
            ),
            'options': Button(
                self.assets.get_scaled_image('options_button', BUTTON_SIZE),
                screen_center_x,
                button_y_positions['options'],
                'options'
            ),
        }
    
    def handle_events(self, events):
        """Processa eventos do menu principal"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Atualiza hover de todos os botões
        for button in self.buttons.values():
            button.update_hover(mouse_pos)
        
        # Processa cliques
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_button_clicks(mouse_pos)
    
    def _handle_button_clicks(self, mouse_pos):
        """Processa cliques nos botões"""
        if self.buttons['start'].is_clicked(mouse_pos):
            print("🎮 START clicado - Indo para seleção de jogos")
            self.next_scene = SceneType.GAME_SELECTION
        
        elif self.buttons['menu'].is_clicked(mouse_pos):
            print("🎮 MENU clicado - Indo para seleção de jogos")
            self.next_scene = SceneType.GAME_SELECTION
        
        elif self.buttons['rules'].is_clicked(mouse_pos):
            print("📖 RULES clicado - Funcionalidade não implementada")
            # Futuramente: self.next_scene = SceneType.RULES
        
        elif self.buttons['options'].is_clicked(mouse_pos):
            print("⚙️ OPTIONS clicado - Funcionalidade não implementada")
            # Futuramente: abrir menu de opções
    
    def draw(self):
        """Desenha o menu principal"""
        # Background em fullscreen
        screen_size = self.screen.get_size()
        
        if self.background:
            scaled_bg = pygame.transform.scale(self.background, screen_size)
            self.screen.blit(scaled_bg, (0, 0))
        else:
            # Fallback se não houver background
            self.screen.fill((75, 45, 135))
        
        # Desenha todos os botões
        for button in self.buttons.values():
            button.draw(self.screen)
    
    def on_enter(self):
        """Chamado ao entrar na cena"""
        print("📍 Cena ativa: Menu Principal")
    
    def on_exit(self):
        """Chamado ao sair da cena"""
        print("📍 Saindo do Menu Principal")