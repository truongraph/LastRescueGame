import pygame
from src.states.splash import SplashScreen
from src.states.loading import LoadingScreen
from src.states.menu import MenuScreen
from src.states.setting import SettingScreen
from src.states.chapter import ChapterScreen
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("The Last Rescue")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Khởi tạo states một lần
        self.states = {
            "splash": SplashScreen(),
            "loading": LoadingScreen(),
            "menu": MenuScreen(),
            "settings": SettingScreen(),
            "chapter": ChapterScreen()
        }
        self.current_state = "splash"

    def run(self):
        while self.running:
            current_screen = self.states[self.current_state]
            next_state = current_screen.run(self.screen, self.clock)
            if next_state:
                # Reset trạng thái fade khi enter state mới
                if hasattr(self.states[next_state], 'on_enter'):
                    self.states[next_state].on_enter()
                self.current_state = next_state
            pygame.display.flip()