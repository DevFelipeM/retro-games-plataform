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
        
        # Carrega background
        self.background = assets.get_image('selection_menu_bg')
        if self.background:
            self.background = self.background.convert()
            print(f"✓ Background GameSelection carregado: {self.background.get_size()}")
        
        # MAPEAMENTO: cada jogo com seu ícone e cena
        self.games_data = [
            {
                'icon': assets.get_image('poker_icon'),
                'scene': SceneType.POKER_GAME,
                'name': 'Poker'
            },
            {
                'icon': assets.get_image('paciencia_icon'),
                'scene': SceneType.PACIENCIA_GAME,
                'name': 'Paciência'
            },
            {
                'icon': assets.get_image('jogo_da_velha_icon'),
                'scene': SceneType.JOGO_DA_VELHA_GAME,
                'name': 'Jogo da Velha'
            },
            {
                'icon': assets.get_image('blackjack_icon'),
                'scene': SceneType.BLACKJACK_GAME,
                'name': 'Blackjack'
            }
        ]
        
        # Carrega setas de navegação
        self.arrow_left = assets.get_image('arrow_left')
        self.arrow_right = assets.get_image('arrow_right')
        self.back_arrow = assets.get_image('back_arrow')
        
        # Índice do jogo atual no carrossel
        self.current_game_index = 0
        
        # Botões da interface
        self.buttons = {}
        
        # Escala todos os ícones
        self.game_icon_scaled = []
        
        self._setup_elements()
    
    def _setup_elements(self):
        """Configura todos os elementos visuais da cena"""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        # Escala todos os ícones de jogos (tamanho pequeno para navegação)
        icon_size = int(screen_width * 0.15)
        for game_data in self.games_data:
            if game_data['icon']:
                scaled_icon = pygame.transform.scale(game_data['icon'], (icon_size, icon_size))
                self.game_icon_scaled.append(scaled_icon)
            else:
                print(f"⚠️ Ícone não carregado para {game_data['name']}")
                # Cria um placeholder
                placeholder = pygame.Surface((icon_size, icon_size))
                placeholder.fill((100, 100, 100))
                self.game_icon_scaled.append(placeholder)
        
        # Configurar botões de navegação
        self._setup_navigation_buttons(screen_width, screen_height, center_x, center_y, icon_size)
        
        # Cria o botão do jogo central
        self._create_current_game_button()
    
    def _setup_navigation_buttons(self, screen_width, screen_height, center_x, center_y, icon_size):
        """Configura os botões de navegação (setas e voltar)"""
        # Tamanho das setas (8% da largura da tela)
        arrow_size = int(screen_width * 0.08)
        arrow_distance = icon_size + 80
        
        # Botão seta esquerda
        if self.arrow_left:
            arrow_left_scaled = pygame.transform.scale(self.arrow_left, (arrow_size, arrow_size))
            self.buttons['arrow_left'] = Button(
                arrow_left_scaled,
                center_x - arrow_distance,
                center_y - 50,
                'arrow_left'
            )
        
        # Botão seta direita
        if self.arrow_right:
            arrow_right_scaled = pygame.transform.scale(self.arrow_right, (arrow_size, arrow_size))
            self.buttons['arrow_right'] = Button(
                arrow_right_scaled,
                center_x + arrow_distance,
                center_y - 50,
                'arrow_right'
            )
        
        # Botão de voltar (canto superior esquerdo)
        if self.back_arrow:
            back_arrow_size = 150
            back_arrow_scaled = pygame.transform.scale(self.back_arrow, (back_arrow_size, back_arrow_size))
            self.buttons['back'] = Button(
                back_arrow_scaled,
                80,
                80,
                'back'
            )
    
    def _create_current_game_button(self):
        """Cria/atualiza o botão do jogo atualmente selecionado no centro"""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        # Pega o ícone do jogo atual
        current_icon = self.game_icon_scaled[self.current_game_index]
        
        # Escala para tamanho grande (botão central)
        current_game_size = 400
        current_game_scaled = pygame.transform.scale(
            current_icon,
            (current_game_size, current_game_size)
        )
        
        # Cria/atualiza o botão
        self.buttons['selected_game'] = Button(
            current_game_scaled,
            center_x,
            center_y - 50,
            'selected_game'
        )
    
    def next_game(self):
        """Avança para o próximo jogo no carrossel"""
        self.current_game_index = (self.current_game_index + 1) % len(self.games_data)
        self._create_current_game_button()
        
        current_game_name = self.games_data[self.current_game_index]['name']
        print(f"➡️ Jogo selecionado: {current_game_name}")
    
    def previous_game(self):
        """Volta para o jogo anterior no carrossel"""
        self.current_game_index = (self.current_game_index - 1) % len(self.games_data)
        self._create_current_game_button()
        
        current_game_name = self.games_data[self.current_game_index]['name']
        print(f"⬅️ Jogo selecionado: {current_game_name}")
    
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
        if 'arrow_left' in self.buttons and self.buttons['arrow_left'].is_clicked(mouse_pos):
            self.previous_game()
        
        elif 'arrow_right' in self.buttons and self.buttons['arrow_right'].is_clicked(mouse_pos):
            self.next_game()
        
        elif 'back' in self.buttons and self.buttons['back'].is_clicked(mouse_pos):
            print("🔙 Voltando ao menu principal")
            self.next_scene = SceneType.MAIN_MENU
        
        elif 'selected_game' in self.buttons and self.buttons['selected_game'].is_clicked(mouse_pos):
            self._start_selected_game()
    
    def _start_selected_game(self):
        """Inicia o jogo selecionado"""
        current_game = self.games_data[self.current_game_index]
        game_scene = current_game['scene']
        game_name = current_game['name']
        
        print(f"🎮 Iniciando {game_name}!")
        self.next_scene = game_scene
    
    def draw(self):
        """Desenha a tela de seleção"""
        screen_size = self.screen.get_size()
        
        # Limpa a tela
        self.screen.fill((0, 0, 0))
        
        # Desenha background
        if self.background:
            try:
                scaled_bg = pygame.transform.scale(self.background, screen_size)
                self.screen.blit(scaled_bg, (0, 0))
            except Exception as e:
                print(f"❌ Erro no background: {e}")
                self.screen.fill((120, 80, 200))  # Fallback roxo
        
        # Desenha todos os botões
        for button in self.buttons.values():
            button.draw(self.screen)
        
        # Desenha textos da UI
        self._draw_ui_text()
    
    def _draw_ui_text(self):
        """Desenha texto da UI"""
        screen_width = self.screen.get_width()
        font_large = pygame.font.Font(None, 80)
        font_small = pygame.font.Font(None, 30)
        
        # Título principal
        title = font_large.render("SELECT GAME", True, (255, 255, 255))
        title_shadow = font_large.render("SELECT GAME", True, (80, 40, 120))
        title_rect = title.get_rect(center=(screen_width // 2, 120))
        
        # Sombra
        self.screen.blit(title_shadow, (title_rect.x + 4, title_rect.y + 4))
        self.screen.blit(title, title_rect)
        
        # Nome do jogo atual
        current_game_name = self.games_data[self.current_game_index]['name']
        game_name_text = font_large.render(current_game_name, True, (255, 255, 100))
        game_name_rect = game_name_text.get_rect(center=(screen_width // 2, self.screen.get_height() - 150))
        self.screen.blit(game_name_text, game_name_rect)
        
        # Instruções
        instructions = [
            "Click the center icon to start game",
            "Use arrows to browse games", 
            "Back button to return to menu"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font_small.render(instruction, True, (220, 220, 255))
            text_rect = text.get_rect(center=(screen_width // 2, 200 + i * 35))
            self.screen.blit(text, text_rect)