"""
game.py - Classe principal do jogo
"""
import pygame
import sys
from src.managers.asset_manager import AssetManager
from src.managers.scene_manager import SceneManager

class Game:
    """Classe principal que controla o loop do jogo"""
    
    def __init__(self):
        """Inicializa o jogo"""
        pygame.init()
        
        # Configurações da tela
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Let's Play The Game")
        
        # Clock para controlar FPS
        self.clock = pygame.time.Clock()
        
        # Gerenciadores
        self.assets = AssetManager()
        self.scene_manager = SceneManager(self.screen, self.assets)
        
        # Estado do jogo
        self.running = True
        
        # Inicia música de fundo
        self._start_music()
    
    def _start_music(self):
        """Inicia a música de fundo"""
        if self.assets.play_music(loops=-1, volume=0.5):
            print("🎵 Música iniciada (volume: 50%)")
        else:
            print("🔇 Música não disponível")
    
    def handle_events(self):
        """Processa eventos do pygame"""
        events = pygame.event.get()
        
        for event in events:
            # Evento de fechar janela
            if event.type == pygame.QUIT:
                self.running = False
            
            # Teclas pressionadas
            elif event.type == pygame.KEYDOWN:
                self._handle_keypress(event.key)
        
        # IMPORTANTE: Passa eventos para o gerenciador de cenas DEPOIS de processar teclas
        self.scene_manager.handle_events(events)
    
    def _handle_keypress(self, key):
        """Processa teclas pressionadas"""
        # ESC para sair
        if key == pygame.K_ESCAPE:
            print("👋 Encerrando jogo...")
            self.running = False
        
        # Controles de música
        elif key == pygame.K_m:
            self._toggle_music()
        
        elif key == pygame.K_PLUS or key == pygame.K_EQUALS:
            self._change_volume(0.1)
        
        elif key == pygame.K_MINUS:
            self._change_volume(-0.1)
    
    def _toggle_music(self):
        """Liga/desliga a música"""
        if pygame.mixer.music.get_busy():
            self.assets.pause_music()
            print("🔇 Música pausada")
        else:
            self.assets.unpause_music()
            print("🔊 Música retomada")
    
    def _change_volume(self, delta):
        """
        Altera o volume da música
        
        Args:
            delta: Valor a adicionar/subtrair do volume (-1.0 a 1.0)
        """
        current_volume = self.assets.get_music_volume()
        new_volume = max(0.0, min(1.0, current_volume + delta))
        self.assets.set_music_volume(new_volume)
        print(f"🔊 Volume: {int(new_volume * 100)}%")
    
    def update(self):
        """Atualiza a lógica do jogo"""
        # Delta time em segundos
        dt = self.clock.tick(60) / 1000.0
        
        # Atualiza o gerenciador de cenas
        self.scene_manager.update(dt)
    
    def draw(self):
        """Desenha tudo na tela"""
        # O gerenciador de cenas cuida de tudo
        self.scene_manager.draw()
        
        # Atualiza a tela
        pygame.display.flip()
    
    def run(self):
        """Loop principal do jogo"""
        self._print_welcome_message()
        
        # Loop principal
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
        
        # Limpeza ao sair
        self._cleanup()
    
    def _print_welcome_message(self):
        """Exibe mensagem de boas-vindas no console"""
        print("\n" + "="*50)
        print("🎮 LET'S PLAY THE GAME")
        print("="*50)
        print("\n📋 Controles:")
        print("   ESC    - Sair do jogo")
        print("   M      - Mute/Unmute música")
        print("   +      - Aumentar volume")
        print("   -      - Diminuir volume")
        print("\n▶️  Jogo iniciado!\n")
    
    def _cleanup(self):
        """Limpeza ao encerrar o jogo"""
        print("\n🛑 Encerrando...")
        self.assets.stop_music()
        pygame.quit()
        sys.exit()