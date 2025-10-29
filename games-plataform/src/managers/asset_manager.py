"""
asset_manager.py - Gerenciador de assets (imagens, sons, músicas)
"""
import pygame
from pathlib import Path

class AssetManager:
    """Carrega e gerencia todos os assets do jogo"""
    
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.base_path = Path("assets")
        self.music_loaded = False
        self._load_all_assets()
    
    def _load_all_assets(self):
        """Carrega todos os assets necessários"""
        self._load_images()
        self._load_music()
    
    def _load_images(self):
        """Carrega todas as imagens"""
        image_files = {
            # Menu principal
            'main_menu_bg': 'images/menu-complete.png',
            'menu_button': 'images/menu_button-menu.png',
            'options_button': 'images/option_button-menu.png',
            'start_button': 'images/start-button-menu.png',
            
            # Menu de seleção de jogos
            'selection_menu_bg': 'images/poker-menu-background.png',
            'poker_icon': 'images/poker-icon.png',
            'arrow_left': 'images/arrow-left.png',
            'arrow_right': 'images/arrow-right.png',
            'back_arrow': 'images/back-arrow.png',
            # Loading screen
            'loading_screen_bg': 'images/loading-screen.png',
        }
        
        print("\n📦 Carregando assets...")
        
        for key, filename in image_files.items():
            path = self.base_path / filename
            
            if not path.exists():
                print(f"⚠ Arquivo não encontrado: {filename}")
                print(f"   Caminho procurado: {path.absolute()}")
                self.images[key] = self._create_placeholder(key, filename)
                continue
            
            try:
                self.images[key] = pygame.image.load(str(path)).convert_alpha()
                size = self.images[key].get_size()
                print(f"✓ Carregado: {filename} ({size[0]}x{size[1]})")
            except pygame.error as e:
                print(f"✗ Erro ao carregar {filename}: {e}")
                self.images[key] = self._create_placeholder(key, filename)
        
        print("")
    
    def _load_music(self):
        """Carrega a música do menu"""
        music_path = self.base_path / "sounds/music/fliperama-main-menu-sound.mp3"
        
        if not music_path.exists():
            print(f"⚠ Música não encontrada: {music_path}")
            self.music_loaded = False
            return
        
        try:
            pygame.mixer.music.load(str(music_path))
            self.music_loaded = True
            print("✓ Música carregada")
        except pygame.error as e:
            print(f"✗ Erro ao carregar música: {e}")
            self.music_loaded = False
    
    def _create_placeholder(self, key, filename):
        """
        Cria uma imagem placeholder para assets faltantes
        
        Args:
            key: Chave do asset
            filename: Nome do arquivo original
            
        Returns:
            pygame.Surface: Superfície placeholder
        """
        # Tamanhos padrão baseados no tipo de asset
        sizes = {
            'main_menu_bg': (1920, 1080),
            'selection_menu_bg': (1920, 1080),
            'poker_icon': (300, 300),
            'arrow_left': (100, 100),
            'arrow_right': (100, 100),
            'back_arrow': (100, 100),
            'menu_button': (235, 99),
            'options_button': (235, 99),
            'start_button': (235, 99),
            'rules_button': (235, 99),
        }
        
        size = sizes.get(key, (200, 100))
        surface = pygame.Surface(size, pygame.SRCALPHA)
        surface.fill((255, 0, 255, 180))  # Rosa translúcido
        
        # Borda branca
        pygame.draw.rect(surface, (255, 255, 255), surface.get_rect(), 3)
        
        # Texto com o nome do arquivo
        font = pygame.font.Font(None, 24)
        text_lines = [
            key.upper(),
            f"({filename})"
        ]
        
        y_offset = size[1] // 3
        for line in text_lines:
            text = font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(size[0]//2, y_offset))
            surface.blit(text, text_rect)
            y_offset += 30
        
        return surface
    
    def get_image(self, key):
        """
        Retorna uma imagem carregada
        
        Args:
            key: Chave da imagem
            
        Returns:
            pygame.Surface ou None: A imagem ou None se não existir
        """
        return self.images.get(key)
    
    def get_scaled_image(self, key, new_size):
        """
        Retorna uma versão escalonada de uma imagem
        
        Args:
            key: Chave da imagem
            new_size: Tupla (largura, altura)
            
        Returns:
            pygame.Surface ou None: Imagem escalonada ou None
        """
        original = self.get_image(key)
        if original:
            return pygame.transform.scale(original, new_size)
        return None
    
    def play_music(self, loops=-1, volume=0.5):
        """
        Toca a música de fundo
        
        Args:
            loops: Número de repetições (-1 = infinito)
            volume: Volume (0.0 a 1.0)
            
        Returns:
            bool: True se conseguiu tocar
        """
        if self.music_loaded:
            pygame.mixer.music.play(loops=loops)
            pygame.mixer.music.set_volume(volume)
            return True
        return False
    
    def stop_music(self):
        """Para a música"""
        pygame.mixer.music.stop()
    
    def pause_music(self):
        """Pausa a música"""
        pygame.mixer.music.pause()
    
    def unpause_music(self):
        """Retoma a música pausada"""
        pygame.mixer.music.unpause()
    
    def set_music_volume(self, volume):
        """
        Ajusta o volume da música
        
        Args:
            volume: Volume (0.0 a 1.0)
        """
        pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))
    
    def get_music_volume(self):
        """
        Retorna o volume atual da música
        
        Returns:
            float: Volume (0.0 a 1.0)
        """
        return pygame.mixer.music.get_volume()