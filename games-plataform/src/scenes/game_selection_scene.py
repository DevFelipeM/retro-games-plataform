"""
game_selection_scene.py - Cena de seleção de jogos
"""
import pygame
from src.scenes.base_scene import Scene
from src.components.button import Button
from src.utils.constants import SceneType

class GameSelectionScene(Scene):
    """Menu de seleção de jogos disponíveis"""
    
    def __init__(self, screen, assets):
        super().__init__(screen, assets)
        
        # Carrega assets
        self.background = assets.get_image('selection_menu_bg')
        self.game_icon = assets.get_image('poker_icon')
        self.arrow_left = assets.get_image('arrow_left')
        self.arrow_right = assets.get_image('arrow_right')
        self.back_arrow = assets.get_image('back_arrow')
        
        # Debug: Verifica se background foi carregado e testa cor
        if self.background:
            print(f"✓ Background GameSelection carregado: {self.background.get_size()}")
            
            # Testa se a imagem não está totalmente preta
            try:
                avg_color = pygame.transform.average_color(self.background)
                print(f"  Cor média do background: RGB{avg_color[:3]}")
                
                # Se a cor média for muito escura, avisa
                if sum(avg_color[:3]) < 30:
                    print("  ⚠️ AVISO: Imagem parece estar muito escura!")
                    print("  💡 Solução: Use uma imagem mais clara ou edite o brilho")
            except:
                pass
            
            # Converte para remover possíveis problemas de alpha
            self.background = self.background.convert()
        else:
            print("⚠️ Background GameSelection NÃO carregado!")
        
        self.buttons = {}
        self.game_icon_rect = None
        self._setup_elements()
    
    def _setup_elements(self):
        """Configura todos os elementos visuais da cena"""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        # Ícone do jogo no centro (15% da largura da tela)
        icon_size = int(screen_width * 0.15)
        self.game_icon_scaled = pygame.transform.scale(
            self.game_icon, 
            (icon_size, icon_size)
        )
        self.game_icon_rect = self.game_icon_scaled.get_rect(
            center=(center_x, center_y - 50)
        )
        
        # Tamanho das setas (8% da largura da tela)
        arrow_size = int(screen_width * 0.08)
        
        # Distância entre as setas e o ícone central
        arrow_distance = icon_size + 80
        
        # Botão seta esquerda
        arrow_left_scaled = pygame.transform.scale(
            self.arrow_left,
            (arrow_size, arrow_size)
        )
        self.buttons['arrow_left'] = Button(
            arrow_left_scaled,
            center_x - arrow_distance,
            center_y - 50,
            'arrow_left'
        )
        
        # Botão seta direita
        arrow_right_scaled = pygame.transform.scale(
            self.arrow_right,
            (arrow_size, arrow_size)
        )
        self.buttons['arrow_right'] = Button(
            arrow_right_scaled,
            center_x + arrow_distance,
            center_y - 50,
            'arrow_right'
        )
        
        # Botão de voltar (canto superior esquerdo)
        back_arrow_size = 80
        back_arrow_scaled = pygame.transform.scale(
            self.back_arrow,
            (back_arrow_size, back_arrow_size)
        )
        self.buttons['back'] = Button(
            back_arrow_scaled,
            80,
            80,
            'back'
        )
    
    def handle_events(self, events):
        """Processa eventos da seleção de jogos"""
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
        if self.buttons['arrow_left'].is_clicked(mouse_pos):
            print("⬅️ Navegar para jogo anterior")
            # Futuramente: self.previous_game()
        
        elif self.buttons['arrow_right'].is_clicked(mouse_pos):
            print("➡️ Navegar para próximo jogo")
            # Futuramente: self.next_game()
        
        elif self.buttons['back'].is_clicked(mouse_pos):
            print("🔙 Voltando ao menu principal")
            self.next_scene = SceneType.MAIN_MENU
        
        # Clique no ícone do jogo para iniciar
        elif self.game_icon_rect and self.game_icon_rect.collidepoint(mouse_pos):
            print("🎮 Iniciando jogo!")
            # Futuramente: self.next_scene = SceneType.GAME
    
    def draw(self):
        """Desenha a tela de seleção - VERSÃO FINAL CORRETA"""
        screen_size = self.screen.get_size()
        
        # ⚠️ CRÍTICO: Sempre limpe a tela no início!
        self.screen.fill((0, 0, 0))  # Limpa completamente
        
        # Background
        if self.background:
            try:
                scaled_bg = pygame.transform.scale(self.background, screen_size)
                self.screen.blit(scaled_bg, (0, 0))
            except Exception as e:
                print(f"❌ Erro no background: {e}")
                self.screen.fill((120, 80, 200))  # Fallback
        
        # Resto dos elementos...
        if self.game_icon_scaled and self.game_icon_rect:
            self.screen.blit(self.game_icon_scaled, self.game_icon_rect)
        
        for button in self.buttons.values():
            button.draw(self.screen)
        
        self._draw_ui_text()

    def _draw_ui_text(self):
        """Desenha texto da UI"""
        screen_width = self.screen.get_width()
        font_large = pygame.font.Font(None, 80)
        font_medium = pygame.font.Font(None, 40)
        font_small = pygame.font.Font(None, 30)
        
        # Título principal
        title = font_large.render("SELECT GAME", True, (255, 255, 255))
        title_shadow = font_large.render("SELECT GAME", True, (80, 40, 120))
        title_rect = title.get_rect(center=(screen_width // 2, 120))
        
        # Sombra
        self.screen.blit(title_shadow, (title_rect.x + 4, title_rect.y + 4))
        self.screen.blit(title, title_rect)
        
        # Instruções
        instructions = [
            "Click the center icon to start game",
            "Use arrows to browse games", 
            "Back button to return to menu"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font_small.render(instruction, True, (220, 220, 255))
            text_rect = text.get_rect(center=(screen_width // 2, 180 + i * 35))
            self.screen.blit(text, text_rect)

    def _draw_minimal_debug(self):
        """Desenha informações de debug mínimas"""
        font = pygame.font.Font(None, 24)
        debug_text = f"BG Color: RGB(83,34,127) | Buttons: {len(self.buttons)}"
        text = font.render(debug_text, True, (255, 255, 0))
        self.screen.blit(text, (10, 10))