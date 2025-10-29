"""
Classe base para todas as cenas
"""
from src.utils.constants import TransitionType

class Scene:
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets
        self.next_scene = None
        self.transition_type = TransitionType.FADE
    
    def handle_events(self, events):
        raise NotImplementedError
    
    def update(self, dt):
        pass
    
    def draw(self):
        raise NotImplementedError
    
    def on_enter(self):
        pass
    
    def on_exit(self):
        pass