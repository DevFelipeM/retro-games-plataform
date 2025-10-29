"""
constants.py - Constantes e enumerações do jogo
"""
from enum import Enum

class SceneType(Enum):
    """Tipos de cenas disponíveis"""
    MAIN_MENU = "main_menu"
    GAME_SELECTION = "game_selection"
    RULES = "rules"
    GAME = "game"

class TransitionType(Enum):
    """Tipos de transição entre cenas"""
    NONE = 0
    FADE = 1
    SLIDE_LEFT = 2
    SLIDE_RIGHT = 3

# Configurações visuais
TRANSITION_SPEED = 5  # Velocidade do fade (quanto maior, mais rápido)
BUTTON_HOVER_SCALE = 1.1  # Escala do botão ao passar o mouse (10% maior)

# Tamanhos padrão dos botões
BUTTON_SIZE = (235, 99)