"""
button.py - Componente de botão reutilizável
"""
import pygame
from src.utils.constants import BUTTON_HOVER_SCALE

class Button:
    """Botão interativo com efeito de hover"""
    
    def __init__(self, image, x, y, name=""):
        """
        Args:
            image: Superfície pygame da imagem do botão
            x: Posição X do centro do botão
            y: Posição Y do centro do botão
            name: Nome identificador do botão
        """
        self.original_image = image
        self.image = image
        self.original_size = image.get_size()
        self.x = x
        self.y = y
        self.name = name
        self.rect = self.image.get_rect(center=(x, y))
        self.hovered = False
        self.hover_scale = BUTTON_HOVER_SCALE
    
    def update_hover(self, mouse_pos):
        """
        Atualiza o estado de hover do botão
        
        Args:
            mouse_pos: Tupla (x, y) com a posição do mouse
            
        Returns:
            bool: True se o hover começou neste frame
        """
        was_hovered = self.hovered
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        # Se mudou o estado de hover, atualiza a aparência
        if was_hovered != self.hovered:
            if self.hovered:
                # Aumenta o botão
                new_size = (
                    int(self.original_size[0] * self.hover_scale),
                    int(self.original_size[1] * self.hover_scale)
                )
                self.image = pygame.transform.scale(self.original_image, new_size)
                self.rect = self.image.get_rect(center=(self.x, self.y))
            else:
                # Volta ao tamanho original
                self.image = self.original_image
                self.rect = self.image.get_rect(center=(self.x, self.y))
        
        return self.hovered and not was_hovered
    
    def is_clicked(self, mouse_pos):
        """
        Verifica se o botão foi clicado
        
        Args:
            mouse_pos: Tupla (x, y) com a posição do mouse
            
        Returns:
            bool: True se o mouse está sobre o botão
        """
        return self.rect.collidepoint(mouse_pos)
    
    def draw(self, surface):
        """
        Desenha o botão na superfície
        
        Args:
            surface: Superfície pygame onde desenhar
        """
        surface.blit(self.image, self.rect)