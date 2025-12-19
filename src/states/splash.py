# src/states/splash.py
import pygame
from src.config import IMAGES_PATH, SCREEN_WIDTH, SCREEN_HEIGHT, SOUNDS_PATH

class SplashScreen:
    def __init__(self):
        # Load hình nền
        self.background = pygame.image.load(IMAGES_PATH + "splash_bg.png").convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Load logo original (không scale trước)
        self.logo_original = pygame.image.load(IMAGES_PATH + "logo.png").convert_alpha()

        # Kích thước logo cuối cùng
        self.final_width = 650
        self.final_height = 350
        self.final_logo = pygame.transform.smoothscale(self.logo_original, (self.final_width, self.final_height))

        # Developer logo
        try:
            dev_original = pygame.image.load(IMAGES_PATH + "develop.png").convert_alpha()
            dev_target_width = 150
            ratio = dev_target_width / dev_original.get_width()
            dev_target_height = int(dev_original.get_height() * ratio)
            self.dev_image = pygame.transform.smoothscale(dev_original, (dev_target_width, dev_target_height))
        except pygame.error:
            print("Warning: develop.png not found. Skipping developer logo in Splash.")
            self.dev_image = None

        self.dev_margin_x = 20
        self.dev_margin_y = 20

        # Trạng thái hiệu ứng
        self.alpha = 0
        self.scale = 0.1              # Bắt đầu từ rất nhỏ
        self.zooming_in = True
        self.showing_full = False
        self.fading_out = False
        self.transitioning = False

        self.zoom_speed = 0.04        # <<< CHẬM HƠN (trước là 0.08) → zoom đẹp, từ từ
        self.fade_speed = 6           # Fade in/out alpha vẫn nhanh để không bị nhàm

        self.full_delay_timer = 0     # Thời gian giữ logo full

        # Âm thanh intro logo - phát ngay khi bắt đầu zoom
        try:
            self.intro_sound = pygame.mixer.Sound(SOUNDS_PATH + "logo_intro.mp3")
            self.intro_sound.set_volume(0.7)
            self.sound_played = False
        except pygame.error as e:
            print(f"Không load được logo_intro.mp3: {e}")
            self.intro_sound = None
            self.sound_played = True

    def fade_to_black(self, screen, clock):
        fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fade_surface.fill((0, 0, 0))
        alpha = 0

        while alpha < 255:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            alpha += 8
            if alpha > 255:
                alpha = 255
            fade_surface.set_alpha(alpha)

            screen.blit(self.background, (0, 0))
            if self.dev_image:
                dev_x = SCREEN_WIDTH - self.dev_image.get_width() - self.dev_margin_x
                dev_y = SCREEN_HEIGHT - self.dev_image.get_height() - self.dev_margin_y
                screen.blit(self.dev_image, (dev_x, dev_y))
            screen.blit(fade_surface, (0, 0))

            pygame.display.update()
            clock.tick(60)

    def run(self, screen, clock):
        while True:
            dt = clock.get_time()  # Dùng dt để timing chính xác hơn

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Phát nhạc logo_intro ngay khi bắt đầu zoom (chỉ 1 lần)
            if self.zooming_in and not self.sound_played and self.intro_sound:
                self.intro_sound.play()
                self.sound_played = True

            # === Logic hiệu ứng ===
            if self.zooming_in:
                self.scale += self.zoom_speed
                self.alpha += self.fade_speed

                if self.scale >= 1.0:
                    self.scale = 1.0
                    self.alpha = 255
                    self.zooming_in = False
                    self.showing_full = True
                    self.full_delay_timer = 1500  # <<< GIỮ LOGO FULL 1.5 GIÂY (trước là 1000)

            elif self.showing_full:
                self.full_delay_timer -= dt
                if self.full_delay_timer <= 0:
                    self.showing_full = False
                    self.fading_out = True

            elif self.fading_out:
                self.alpha -= self.fade_speed
                if self.alpha <= 0:
                    self.alpha = 0
                    self.fading_out = False
                    self.transitioning = True

            elif self.transitioning:
                self.fade_to_black(screen, clock)
                return "loading"

            # === Vẽ ===
            screen.blit(self.background, (0, 0))

            # Scale logo hiện tại
            current_width = int(self.final_width * self.scale)
            current_height = int(self.final_height * self.scale)
            if current_width > 0 and current_height > 0:
                current_logo = pygame.transform.smoothscale(self.logo_original, (current_width, current_height))
            else:
                current_logo = self.final_logo

            current_logo.set_alpha(self.alpha)

            logo_x = (SCREEN_WIDTH - current_logo.get_width()) // 2
            logo_y = (SCREEN_HEIGHT - current_logo.get_height()) // 2
            screen.blit(current_logo, (logo_x, logo_y))

            # Developer logo
            if self.dev_image:
                dev_x = SCREEN_WIDTH - self.dev_image.get_width() - self.dev_margin_x
                dev_y = SCREEN_HEIGHT - self.dev_image.get_height() - self.dev_margin_y
                screen.blit(self.dev_image, (dev_x, dev_y))

            pygame.display.update()
            clock.tick(60)