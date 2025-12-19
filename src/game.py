# game.py
import pygame
from src.states.splash import SplashScreen
from src.states.loading import LoadingScreen
from src.states.menu import MenuScreen
from src.states.setting import SettingScreen
from src.states.chapter import ChapterScreen
from src.utils.transition import fade_transition  # Thêm dòng này
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("The Last Rescue")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

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
            result = current_screen.run(self.screen, self.clock)

            if result == "quit":
                self.running = False
            elif result:
                # Nếu có hiệu ứng chuyển cảnh cần fade
                if result in ["loading", "menu", "chapter", "settings"]:
                    next_state = result
                    fade_transition(self.screen, self.clock)
                    self.current_state = next_state
                else:
                    self.current_state = result

            pygame.display.flip()

        pygame.quit()