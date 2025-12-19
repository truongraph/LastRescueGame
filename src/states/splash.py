import pygame
from src.config import IMAGES_PATH, SCREEN_WIDTH, SCREEN_HEIGHT

class SplashScreen():
    def __init__(self):
        # Load hình nền và logo
        self.background = pygame.image.load(IMAGES_PATH + "splash_bg.png").convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.logo_original = pygame.image.load(IMAGES_PATH + "logo.png")
        self.logo = pygame.transform.scale(self.logo_original, (650, 350))

        try:
            dev_original = pygame.image.load(IMAGES_PATH + "develop.png").convert_alpha()
            dev_target_width = 150
            ratio = dev_target_width / dev_original.get_width()
            dev_target_height = int(dev_original.get_height() * ratio)
            self.dev_image = pygame.transform.smoothscale(dev_original, (dev_target_width, dev_target_height))
        except pygame.error:
            # Fallback nếu không load được ảnh
            print("Warning: develop.png not found. Skipping developer logo in Splash.")
            self.dev_image = None

        # Khoảng cách từ góc dưới phải
        self.dev_margin_x = 20
        self.dev_margin_y = 20

        # Trạng thái alpha và fade (chỉ áp dụng cho logo)
        self.alpha = 0
        self.showing = True
        self.fade_speed = 2
        self.transitioning = False

    def fade_to_black(self, screen):
        """Hiệu ứng fade toàn màn hình chuyển sang màu đen."""
        transition_alpha = 0
        fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fade_surface.fill((0, 0, 0))

        while transition_alpha < 255:
            fade_surface.set_alpha(transition_alpha)
            screen.blit(self.background, (0, 0))
            if self.dev_image:
                dev_x = SCREEN_WIDTH - self.dev_image.get_width() - self.dev_margin_x
                dev_y = SCREEN_HEIGHT - self.dev_image.get_height() - self.dev_margin_y
                screen.blit(self.dev_image, (dev_x, dev_y))
            screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            transition_alpha += 5
            pygame.time.delay(10)

    def run(self, screen, clock):
        running = True
        self.alpha = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Fade in/out logo
            if self.showing:
                self.alpha += self.fade_speed
                if self.alpha >= 255:
                    self.alpha = 255
                    pygame.time.delay(1000)
                    self.showing = False
            elif not self.transitioning:
                self.alpha -= self.fade_speed
                if self.alpha <= 0:
                    self.alpha = 0
                    self.transitioning = True

            if self.transitioning:
                self.fade_to_black(screen)
                return "loading"


            screen.blit(self.background, (0, 0))

            logo_copy = self.logo.copy()
            logo_copy.set_alpha(self.alpha)
            screen.blit(logo_copy,
                        ((SCREEN_WIDTH - logo_copy.get_width()) // 2,
                         (SCREEN_HEIGHT - logo_copy.get_height()) // 2))

            if self.dev_image:
                dev_x = SCREEN_WIDTH - self.dev_image.get_width() - self.dev_margin_x
                dev_y = SCREEN_HEIGHT - self.dev_image.get_height() - self.dev_margin_y
                screen.blit(self.dev_image, (dev_x, dev_y))

            pygame.display.update()
            clock.tick(60)