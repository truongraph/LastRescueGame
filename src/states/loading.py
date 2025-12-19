import pygame
from src.config import IMAGES_PATH, SCREEN_WIDTH, SCREEN_HEIGHT, FONTS_PATH, SOUNDS_PATH
from src.utils.transition import fade_transition
class LoadingScreen:
    def __init__(self):
        # Background full màn hình
        self.background = pygame.image.load(IMAGES_PATH + "loading_bg.png")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Logo ở trên giữa
        try:
            logo_original = pygame.image.load(IMAGES_PATH + "logo.png").convert_alpha()
            self.logo = pygame.transform.smoothscale(logo_original, (450, 250))
        except pygame.error:
            font_logo = pygame.font.Font(FONTS_PATH, 80)
            self.logo = font_logo.render("The Last Rescue", True, (255, 255, 255))

        # Loading bar frame và bar
        target_frame_width = 500
        target_frame_height = 60

        self.loading_frame = pygame.transform.smoothscale(
            pygame.image.load(IMAGES_PATH + "loading_frame.png").convert_alpha(),
            (target_frame_width, target_frame_height)
        )

        bar_width = target_frame_width - 40
        bar_height = target_frame_height - 38
        self.loading_bar_full = pygame.transform.smoothscale(
            pygame.image.load(IMAGES_PATH + "loading_bar.png").convert_alpha(),
            (bar_width, bar_height)
        )

        self.padding_x = 21
        self.padding_y = 18
        self.bar_max_width = bar_width

        # Font chữ
        self.info_font = pygame.font.Font(FONTS_PATH, 30)

        # Developer logo góc dưới phải
        try:
            dev_original = pygame.image.load(IMAGES_PATH + "develop.png").convert_alpha()
            dev_target_width = 140
            ratio = dev_target_width / dev_original.get_width()
            dev_target_height = int(dev_original.get_height() * ratio)
            self.dev_image = pygame.transform.smoothscale(dev_original, (dev_target_width, dev_target_height))
        except pygame.error:
            self.dev_image = None

        self.dev_margin_x = 20
        self.dev_margin_y = 20

        # Trạng thái loading
        self.progress = 0
        self.total_steps = 100
        self.loading_complete = False

        # Fade effect
        #self.fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        #self.fade_surface.fill((0, 0, 0))
        #self.fading_out = False
        #self.fade_alpha = 0

        # Âm thanh click khi nhấn phím để tiếp tục
        try:
            self.continue_sound = pygame.mixer.Sound(SOUNDS_PATH + "button_click.wav")
            self.continue_sound.set_volume(0.7)
        except pygame.error:
            self.continue_sound = None

        # Load nhạc nền menu (sẵn sàng phát khi chuyển cảnh)
        try:
            pygame.mixer.music.load(SOUNDS_PATH + "sound_menu.mp3")
            pygame.mixer.music.set_volume(0.6)
        except pygame.error:
            print("Không load được sound_menu.mp3")

    def render_styled_text(self, text):
        main_color = (255, 215, 0)
        outline_color = (0, 0, 0)
        glow_color = (255, 255, 100)

        text_surf = self.info_font.render(text, True, main_color)
        text_rect = text_surf.get_rect()
        size = (text_rect.width + 12, text_rect.height + 12)
        styled_surf = pygame.Surface(size, pygame.SRCALPHA)

        for offset in [(2,2), (2,-2), (-2,2), (-2,-2), (4,0), (-4,0), (0,4), (0,-4)]:
            glow = self.info_font.render(text, True, glow_color)
            styled_surf.blit(glow, (offset[0] + 6, offset[1] + 6))

        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if dx*dx + dy*dy <= 9:
                    outline = self.info_font.render(text, True, outline_color)
                    styled_surf.blit(outline, (dx + 6, dy + 6))

        styled_surf.blit(text_surf, (6, 6))

        return styled_surf

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        logo_x = (SCREEN_WIDTH - self.logo.get_width()) // 2
        logo_y = SCREEN_HEIGHT // 5
        screen.blit(self.logo, (logo_x, logo_y))

        frame_x = (SCREEN_WIDTH - self.loading_frame.get_width()) // 2
        frame_y = SCREEN_HEIGHT - 130
        screen.blit(self.loading_frame, (frame_x, frame_y))

        if self.progress > 0:
            current_bar_width = int((self.progress / self.total_steps) * self.bar_max_width)
            if current_bar_width > 0:
                bar_crop = pygame.Rect(0, 0, current_bar_width, self.loading_bar_full.get_height())
                bar_surface = self.loading_bar_full.subsurface(bar_crop)
                screen.blit(bar_surface, (frame_x + self.padding_x, frame_y + self.padding_y))

        text_y = frame_y - 45
        if not self.loading_complete:
            percent = int((self.progress / self.total_steps) * 100)
            loading_text = self.render_styled_text(f"LOADING... {percent}%")
            text_x = frame_x + (self.loading_frame.get_width() - loading_text.get_width()) // 2
            screen.blit(loading_text, (text_x, text_y))
        else:
            if int(pygame.time.get_ticks() / 500) % 2 == 0:
                press_text = self.render_styled_text("Press any key to continue")
                text_x = frame_x + (self.loading_frame.get_width() - press_text.get_width()) // 2
                screen.blit(press_text, (text_x, text_y))

        if self.dev_image:
            dev_x = SCREEN_WIDTH - self.dev_image.get_width() - self.dev_margin_x
            dev_y = SCREEN_HEIGHT - self.dev_image.get_height() - self.dev_margin_y
            screen.blit(self.dev_image, (dev_x, dev_y))

    def run(self, screen, clock):
        progress_timer = 0
        progress_interval = 30
        pressed_to_continue = False

        while True:
            dt = clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if self.loading_complete and not pressed_to_continue:
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        pressed_to_continue = True
                        if self.continue_sound:
                            self.continue_sound.play()
                        pygame.mixer.music.play(-1)
                        fade_transition(screen, clock, 350)
                        return "menu"  # Trả về menu sau fade

            if not self.loading_complete:
                progress_timer += dt
                if progress_timer >= progress_interval:
                    progress_timer = 0
                    self.progress += 1
                    if self.progress >= self.total_steps:
                        self.progress = self.total_steps
                        self.loading_complete = True

            self.draw(screen)
            pygame.display.update()