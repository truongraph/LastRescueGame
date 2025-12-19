import pygame
from src.config import IMAGES_PATH, SCREEN_WIDTH, SCREEN_HEIGHT, FONTS_PATH, SOUNDS_PATH
from src.sound_manager import SoundManager  # Thêm import
from src.utils.transition import fade_transition
class MenuScreen:
    def __init__(self, screen=None):
        # Background
        self.screen = screen
        self.background = pygame.image.load(IMAGES_PATH + "menu_bg.png")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Logo căn trái
        try:
            logo_original = pygame.image.load(IMAGES_PATH + "logo.png").convert_alpha()
            logo_target_width = 300
            ratio = logo_target_width / logo_original.get_width()
            logo_target_height = int(logo_original.get_height() * ratio)
            self.logo = pygame.transform.smoothscale(logo_original, (logo_target_width, logo_target_height))
        except pygame.error:
            fallback_font = pygame.font.Font(FONTS_PATH, 80)
            self.logo = fallback_font.render("The Last Rescue", True, (255, 255, 255))

        # Nút thường
        self.normal_button_width = 300
        self.normal_button_height = 70
        self.normal_frame_original = pygame.image.load(IMAGES_PATH + "menu_button.png").convert_alpha()
        self.normal_frame_base = pygame.transform.smoothscale(
            self.normal_frame_original,
            (self.normal_button_width, self.normal_button_height)
        )

        # Nút Start lớn hơn
        try:
            play_original = pygame.image.load(IMAGES_PATH + "play_button.png").convert_alpha()
            self.start_button_width = 380
            self.start_button_height = 90
            self.start_frame_base = pygame.transform.smoothscale(
                play_original,
                (self.start_button_width, self.start_button_height)
            )
            self.start_frame_original = play_original
        except pygame.error:
            print("Không tải được play_button.png")
            self.start_frame_base = self.normal_frame_base
            self.start_button_width = self.normal_button_width
            self.start_button_height = self.normal_button_height
            self.start_frame_original = self.normal_frame_original

        # Font
        self.button_font = pygame.font.Font(FONTS_PATH, 25)
        self.start_font = pygame.font.Font(FONTS_PATH, 32)
        self.version_font = pygame.font.Font(FONTS_PATH, 14)

        # Phiên bản (giữ lại nếu muốn)
        self.version_text = "App version 1.0 | Python game"
        self.version_color = (200, 200, 200)
        self.version_margin = 15

        # Dùng SoundManager chung
        self.sound_manager = SoundManager()
        self.sound_manager.load_sounds(SOUNDS_PATH)

        self.last_hovered_index = None

        # Danh sách nút
        self.buttons = [
            {"text": "Start",           "action": self.start_game,       "is_start": True},
            {"text": "Select chapter", "action": self.select_chapter, "is_start": False},
            {"text": "Setting",         "action": self.settings,         "is_start": False},
            {"text": "Quit game",       "action": self.exit_game,        "is_start": False}
        ]

        # Developer logo
        try:
            dev_original = pygame.image.load(IMAGES_PATH + "develop.png").convert_alpha()
            dev_target_width = 150
            ratio = dev_target_width / dev_original.get_width()
            dev_target_height = int(dev_original.get_height() * ratio)
            self.dev_image = pygame.transform.smoothscale(dev_original, (dev_target_width, dev_target_height))
        except pygame.error:
            self.dev_image = None

        self.dev_margin_x = 20
        self.dev_margin_y = 20

        self.hover_scale = 1.1
        self.hovered_index = None

    def render_styled_text(self, text, font=None):
        if font is None:
            font = self.button_font
        main_color = (255, 215, 0)
        outline_color = (0, 0, 0)
        glow_color = (255, 255, 100)

        text_surf = font.render(text, True, main_color)
        size = (text_surf.get_width() + 16, text_surf.get_height() + 16)
        styled_surf = pygame.Surface(size, pygame.SRCALPHA)

        for offset in [(2,2), (2,-2), (-2,2), (-2,-2)]:
            glow = font.render(text, True, glow_color)
            styled_surf.blit(glow, (offset[0] + 8, offset[1] + 8))

        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if dx*dx + dy*dy <= 9:
                    outline = font.render(text, True, outline_color)
                    styled_surf.blit(outline, (dx + 8, dy + 8))

        styled_surf.blit(text_surf, (8, 8))
        return styled_surf

    def start_game(self):
        self.sound_manager.play_click()
        print("Bắt đầu game!")

    def select_chapter(self):
        self.sound_manager.play_click()
        return "chapter"

    def settings(self):
        self.sound_manager.play_click()
        return "settings"

    def exit_game(self):
        self.sound_manager.play_click()
        pygame.quit()
        exit()

    def run(self, screen, clock):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            self.hovered_index = None
            current_hovered = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, button in enumerate(self.buttons):
                        is_start = button["is_start"]
                        w = self.start_button_width if is_start else self.normal_button_width
                        h = self.start_button_height if is_start else self.normal_button_height
                        y = 220 + i * 100
                        x = (SCREEN_WIDTH - w) // 2
                        rect = pygame.Rect(x, y, w, h)

                        if self.hovered_index == i:
                            scaled_w = int(w * self.hover_scale)
                            scaled_h = int(h * self.hover_scale)
                            scaled_x = (SCREEN_WIDTH - scaled_w) // 2
                            scaled_y = y - (scaled_h - h) // 2
                            rect = pygame.Rect(scaled_x, scaled_y, scaled_w, scaled_h)

                        if rect.collidepoint(mouse_pos):
                            result = button["action"]()
                            if result in ["chapter", "settings"]:
                                fade_transition(screen, clock, 250)
                                return result
                            elif result:
                                return result

            screen.blit(self.background, (0, 0))
            screen.blit(self.logo, (10, 40))

            for i, button in enumerate(self.buttons):
                is_start = button["is_start"]
                base_y = 220 + i * 100

                if is_start:
                    base_w = self.start_button_width
                    base_h = self.start_button_height
                    base_frame = self.start_frame_base
                    frame_original = self.start_frame_original
                    text_font = self.start_font
                else:
                    base_w = self.normal_button_width
                    base_h = self.normal_button_height
                    base_frame = self.normal_frame_base
                    frame_original = self.normal_frame_original
                    text_font = self.button_font

                base_x = (SCREEN_WIDTH - base_w) // 2
                temp_rect = pygame.Rect(base_x, base_y, base_w, base_h)
                is_hovered = temp_rect.collidepoint(mouse_pos)

                if is_hovered:
                    self.hovered_index = i
                    current_hovered = i
                    if self.last_hovered_index != i:
                        self.sound_manager.play_hover()

                    scaled_w = int(base_w * self.hover_scale)
                    scaled_h = int(base_h * self.hover_scale)
                    scaled_frame = pygame.transform.smoothscale(frame_original, (scaled_w, scaled_h))
                    scaled_x = (SCREEN_WIDTH - scaled_w) // 2
                    scaled_y = base_y - (scaled_h - base_h) // 2
                    screen.blit(scaled_frame, (scaled_x, scaled_y))

                    styled_text = self.render_styled_text(button["text"], text_font)
                    text_scaled = pygame.transform.smoothscale(styled_text, (int(styled_text.get_width() * self.hover_scale), int(styled_text.get_height() * self.hover_scale)))
                    text_x = scaled_x + (scaled_w - text_scaled.get_width()) // 2
                    text_y = scaled_y + (scaled_h - text_scaled.get_height()) // 2
                    screen.blit(text_scaled, (text_x, text_y))
                else:
                    screen.blit(base_frame, (base_x, base_y))
                    styled_text = self.render_styled_text(button["text"], text_font)
                    text_x = base_x + (base_w - styled_text.get_width()) // 2
                    text_y = base_y + (base_h - styled_text.get_height()) // 2
                    screen.blit(styled_text, (text_x, text_y))

            self.last_hovered_index = current_hovered

            if self.dev_image:
                dev_x = SCREEN_WIDTH - self.dev_image.get_width() - self.dev_margin_x
                dev_y = SCREEN_HEIGHT - self.dev_image.get_height() - self.dev_margin_y
                screen.blit(self.dev_image, (dev_x, dev_y))

            pygame.display.update()
            clock.tick(60)