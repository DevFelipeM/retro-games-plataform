"""
scene_manager.py - Gerenciador de cenas e transições
"""
import pygame
from src.utils.constants import SceneType, TRANSITION_SPEED
from src.scenes.main_menu_scene import MainMenuScene
from src.scenes.game_selection_scene import GameSelectionScene
from src.scenes.games.poker_game_scene import PokerGameScene
from src.scenes.games.paciencia_game_scene import PacienciaGameScene
from src.scenes.games.jogo_da_velha_game_scene import JogoDaVelhaGameScene
from src.scenes.games.blackjack_game_scene import BlackjackGameScene

class SceneManager:
    """Gerencia cenas e transições entre elas"""
    
    def __init__(self, screen, assets):
        """
        Args:
            screen: Superfície principal do pygame
            assets: Instância do AssetManager
        """
        self.screen = screen
        self.assets = assets
        self.scenes = {}
        self.current_scene = None
        
        # Carrega o background de loading
        self.loading_background = assets.get_image('loading_screen_bg')
        if self.loading_background: 
            self.loading_background = self.loading_background.convert()
        
        # Controle de transição com loading
        self.is_loading = False  
        self.loading_timer = 0
        self.loading_duration = 1.0 
        self.next_scene_type = None  # Qual cena carregar após o loading
        
        self._setup_scenes()
    
    def _setup_scenes(self):
        """Cria todas as cenas disponíveis"""
        self.scenes = {
            SceneType.MAIN_MENU: MainMenuScene(self.screen, self.assets),
            SceneType.GAME_SELECTION: GameSelectionScene(self.screen, self.assets),
            SceneType.POKER_GAME: PokerGameScene(self.screen, self.assets),
            SceneType.PACIENCIA_GAME: PacienciaGameScene(self.screen, self.assets),
            SceneType.JOGO_DA_VELHA_GAME: JogoDaVelhaGameScene(self.screen, self.assets),
            SceneType.BLACKJACK_GAME: BlackjackGameScene(self.screen, self.assets),
        }
        
        # Define cena inicial (SEM loading)
        self.current_scene = self.scenes[SceneType.MAIN_MENU]
        self.current_scene.on_enter()
        print(f"✓ Cena inicial: {SceneType.MAIN_MENU.value}")
    
    def change_scene(self, scene_type):
        """
        Inicia transição para uma nova cena (com tela de loading)
        
        Args:
            scene_type: Tipo da cena de destino
        """
        if scene_type in self.scenes and not self.is_loading:
            print(f"🔄 Iniciando transição para: {scene_type.value}")
            
            # Sai da cena atual
            self.current_scene.on_exit()
            
            # Ativa o modo loading
            self.is_loading = True
            self.loading_timer = 0
            self.next_scene_type = scene_type
    
    def update(self, dt):
        """
        Atualiza o estado do jogo
        
        Args:
            dt: Delta time em SEGUNDOS
        """
        if self.is_loading:
            # Está na tela de loading
            self.loading_timer += dt
            
            # Verifica se passaram 2 segundos
            if self.loading_timer >= self.loading_duration:
                self._finish_loading()
        else:
            if self.current_scene.next_scene:
                self.change_scene(self.current_scene.next_scene)
                self.current_scene.next_scene = None
            
            # Atualiza a cena atual
            self.current_scene.update(dt)
    
    def _finish_loading(self):
        """Finaliza o loading e muda para a nova cena"""
        print(f"✓ Loading concluído! Entrando em: {self.next_scene_type.value}")
        
        # Muda para a nova cena
        self.current_scene = self.scenes[self.next_scene_type]
        self.current_scene.on_enter()
        
        # Desativa o modo loading
        self.is_loading = False
        self.loading_timer = 0
        self.next_scene_type = None
    
    def handle_events(self, events):
        """
        Passa eventos para a cena atual
        
        Args:
            events: Lista de eventos do pygame
        """
        # Não processa eventos durante loading
        if not self.is_loading:
            self.current_scene.handle_events(events)
    
    def draw(self):
        """Desenha a tela atual (cena ou loading)"""
        if self.is_loading:
            # Desenha a tela de loading
            self._draw_loading_screen()
        else:
            # Desenha a cena atual
            self.current_scene.draw()
    
    def _draw_loading_screen(self):
        """Desenha a tela de loading com o background"""
        screen_size = self.screen.get_size()
        
        # Preenche com preto (fallback)
        self.screen.fill((0, 0, 0))
        
        # Desenha o background de loading se disponível
        if self.loading_background:
            try:
                scaled_bg = pygame.transform.scale(self.loading_background, screen_size)
                self.screen.blit(scaled_bg, (0, 0))
            except Exception as e:
                print(f"❌ Erro ao desenhar loading background: {e}")
                self.screen.fill((120, 80, 200))  # Fallback roxo
        