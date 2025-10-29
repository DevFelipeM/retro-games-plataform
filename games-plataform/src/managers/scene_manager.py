"""
scene_manager.py - Gerenciador de cenas e transições
"""
import pygame
from src.utils.constants import SceneType, TRANSITION_SPEED
from src.scenes.main_menu_scene import MainMenuScene
from src.scenes.game_selection_scene import GameSelectionScene

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
        
        self.background = assets.get_image('loading_screen_bg')
        
        # Controle de transição
        self.transitioning = False
        self.transition_alpha = 0
        self.transition_speed = TRANSITION_SPEED
        self.next_scene_type = None
        
        # Superfície para efeito de fade
        screen_size = screen.get_size()
        self.fade_surface = pygame.Surface(screen_size)
        self.fade_surface.fill((0, 0, 0))
        
        self._setup_scenes()
    
    def _setup_scenes(self):
        """Cria todas as cenas disponíveis"""
        self.scenes = {
            SceneType.MAIN_MENU: MainMenuScene(self.screen, self.assets),
            SceneType.GAME_SELECTION: GameSelectionScene(self.screen, self.assets),
            # Adicione mais cenas aqui conforme necessário
        }
        
        # Define cena inicial
        self.current_scene = self.scenes[SceneType.MAIN_MENU]
        self.current_scene.on_enter()
    
    def change_scene(self, scene_type):
        """
        Muda para uma nova cena SEM TRANSIÇÃO (para teste)
        """
        if scene_type in self.scenes and not self.transitioning:
            print(f"🔄 Mudança DIRETA para: {scene_type.value} (sem transição)")
            
            # Sai da cena atual
            self.current_scene.on_exit()
            
            # Muda diretamente para a nova cena
            self.current_scene = self.scenes[scene_type]
            self.current_scene.on_enter()
    
    def update(self, dt):
        """
        Atualiza cena atual SEM verificar transições
        """
        # Verifica se a cena atual quer mudar
        if self.current_scene.next_scene:
            self.change_scene(self.current_scene.next_scene)
            self.current_scene.next_scene = None
        
        # Atualiza a cena atual
        self.current_scene.update(dt)
    
    def _update_transition(self):
        """Atualiza o estado da transição (fade in/out)"""
        # Fase 1: Fade out (escurece a tela)
        if self.transition_alpha < 255:
            self.transition_alpha += self.transition_speed
            
            if self.transition_alpha >= 255:
                self.transition_alpha = 255
                # Momento de trocar a cena (no meio da transição)
                if self.next_scene_type:
                    self._switch_scene()
        
        # Fase 2: Fade in (clareia a tela)
        else:
            self.transition_alpha -= self.transition_speed
            
            if self.transition_alpha <= 0:
                self.transition_alpha = 0
                self.transitioning = False
                print("✓ Transição concluída")
    
    def _switch_scene(self):
        """Executa a troca de cena"""
        # Sai da cena atual
        self.current_scene.on_exit()
        
        # Muda para a nova cena
        self.current_scene = self.scenes[self.next_scene_type]
        
        print(f"✓ Mudando para cena: {self.next_scene_type.value}")
        
        self.current_scene.on_enter()
        
        self.next_scene_type = None
    
    def handle_events(self, events):
        """
        Passa eventos para a cena atual
        
        Args:
            events: Lista de eventos do pygame
        """
        # Não processa eventos durante transição
        if not self.transitioning:
            self.current_scene.handle_events(events)
    
    def draw(self):
        """Desenha apenas a cena atual - SEM EFEITOS DE TRANSIÇÃO"""
        self.current_scene.draw()
        
        # DEBUG: Mostra que não há transição
        font = pygame.font.Font(None, 36)
        text = font.render("SEM TRANSIÇÃO - TESTE", True, (0, 255, 0))
        self.screen.blit(text, (10, 10))