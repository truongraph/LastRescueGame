import pygame
from src.config import IMAGES_PATH, SCREEN_WIDTH, SCREEN_HEIGHT, FONTS_PATH, SOUNDS_PATH
from src.sound_manager import SoundManager

class SettingScreen:
    def __init__(self):
        # Background
        self.background = pygame.image.load(IMAGES_PATH + "menu_bg.png")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Title
        self.title_font = pygame.font.Font(FONTS_PATH, 50)
        self.title_text = self.title_font.render("Settings", True, (255, 215, 0))

        # Font nhỏ hơn nữa
        self.label_font = pygame.font.Font(FONTS_PATH, 22)
        self.percent_font = pygame.font.Font(FONTS_PATH, 20)

        # SoundManager
        self.sound_manager = SoundManager()

        # Giá trị mặc định
        self.DEFAULT_MUSIC_VOLUME = 0.6
        self.DEFAULT_SOUND_VOLUME = 0.7

        # Volume hiện tại
        self.music_volume = self.DEFAULT_MUSIC_VOLUME
        self.sound_volume = self.sound_manager.sound_volume

        # Load frame và line - NHỎ HƠN NỮA
        try:
            self.frame_sound = pygame.image.load(IMAGES_PATH + "frame_sound.png").convert_alpha()
            self.frame_sound = pygame.transform.smoothscale(self.frame_sound, (400, 55))
        except:
            self.frame_sound = None

        try:
            self.line_sound_full = pygame.image.load(IMAGES_PATH + "line_sound.png").convert_alpha()
            self.line_sound_full = pygame.transform.smoothscale(self.line_sound_full, (330, 22))
        except:
            self.line_sound_full = None

        self.padding_x = 35
        self.padding_y = 16
        self.bar_max_width = 330

        # Icon rất nhỏ
        try:
            self.sound_off = pygame.image.load(IMAGES_PATH + "sound_off.png").convert_alpha()
            self.sound_off = pygame.transform.smoothscale(self.sound_off, (40, 40))
        except:
            self.sound_off = None

        try:
            self.sound_on = pygame.image.load(IMAGES_PATH + "sound_on.png").convert_alpha()
            self.sound_on = pygame.transform.smoothscale(self.sound_on, (40, 40))
        except:
            self.sound_on = None

        # Back button nhỏ và nằm góc trái trên
        self.back_button_width = 180
        self.back_button_height = 45
        try:
            self.back_frame_original = pygame.image.load(IMAGES_PATH + "menu_button.png").convert_alpha()
            self.back_frame_base = pygame.transform.smoothscale(
                self.back_frame_original,
                (self.back_button_width, self.back_button_height)
            )
        except:
            self.back_frame_base = None
            self.back_frame_original = None

        self.back_font = pygame.font.Font(FONTS_PATH, 22)

        # Reset button - TĂNG CHIỀU CAO LÊN (cao hơn)
        self.reset_button_width = 240
        self.reset_button_height = 65  # <<< Tăng từ 45 lên 65 để cao hơn
        try:
            self.reset_frame_original = pygame.image.load(IMAGES_PATH + "menu_button.png").convert_alpha()
            self.reset_frame_base = pygame.transform.smoothscale(
                self.reset_frame_original,
                (self.reset_button_width, self.reset_button_height)
            )
        except:
            self.reset_frame_base = None
            self.reset_frame_original = None

        self.reset_font = pygame.font.Font(FONTS_PATH, 26)  # Font to hơn để vừa nút cao

        self.back_hovered = False
        self.reset_hovered = False
        self.last_back_hover_state = False
        self.last_reset_hover_state = False
        self.hover_scale = 1.1

        # Developer logo
        try:
            dev_original = pygame.image.load(IMAGES_PATH + "develop.png").convert_alpha()
            dev_target_width = 150
            ratio = dev_target_width / dev_original.get_width()
            dev_target_height = int(dev_original.get_height() * ratio)
            self.dev_image = pygame.transform.smoothscale(dev_original, (dev_target_width, dev_target_height))
        except:
            self.dev_image = None

        self.dev_margin_x = 20
        self.dev_margin_y = 20

        pygame.mixer.music.set_volume(self.music_volume)

    def render_styled_text(self, text, font=None):
        if font is None:
            font = self.back_font
        main_color = (255, 215, 0)
        outline_color = (0, 0, 0)
        glow_color = (255, 255, 100)

        text_surf = font.render(text, True, main_color)
        size = (text_surf.get_width() + 14, text_surf.get_height() + 14)
        styled_surf = pygame.Surface(size, pygame.SRCALPHA)

        for offset in [(2,2), (2,-2), (-2,2), (-2,-2)]:
            glow = font.render(text, True, glow_color)
            styled_surf.blit(glow, (offset[0] + 7, offset[1] + 7))

        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx*dx + dy*dy <= 6:
                    outline = font.render(text, True, outline_color)
                    styled_surf.blit(outline, (dx + 7, dy + 7))

        styled_surf.blit(text_surf, (7, 7))
        return styled_surf

    def draw_volume_bar(self, screen, y_position, volume, label):
        frame_x = (SCREEN_WIDTH - 400) // 2

        if self.sound_off:
            off_x = frame_x - self.sound_off.get_width() - 20
            off_y = y_position + (55 - self.sound_off.get_height()) // 2
            screen.blit(self.sound_off, (off_x, off_y))

        if self.sound_on:
            on_x = frame_x + 400 + 20
            on_y = y_position + (55 - self.sound_on.get_height()) // 2
            screen.blit(self.sound_on, (on_x, on_y))

        if self.frame_sound:
            screen.blit(self.frame_sound, (frame_x, y_position))

        if self.line_sound_full:
            current_width = int(volume * self.bar_max_width)
            if current_width > 0:
                crop_rect = pygame.Rect(0, 0, current_width, self.line_sound_full.get_height())
                line_crop = self.line_sound_full.subsurface(crop_rect)
                screen.blit(line_crop, (frame_x + self.padding_x, y_position + self.padding_y))

        label_surf = self.label_font.render(label, True, (255, 255, 255))
        label_x = (SCREEN_WIDTH - label_surf.get_width()) // 2
        screen.blit(label_surf, (label_x, y_position - 30))

        percent_text = f"{int(volume * 100)}%"
        percent_surf = self.percent_font.render(percent_text, True, (255, 255, 255))
        percent_x = (SCREEN_WIDTH - percent_surf.get_width()) // 2
        percent_y = y_position + 60
        screen.blit(percent_surf, (percent_x, percent_y))

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        title_x = (SCREEN_WIDTH - self.title_text.get_width()) // 2
        screen.blit(self.title_text, (title_x, 60))

        self.draw_volume_bar(screen, 200, self.music_volume, "Music")
        self.draw_volume_bar(screen, 370, self.sound_volume, "Sound")

        # Reset button - cao hơn, chữ to hơn
        reset_x = (SCREEN_WIDTH - self.reset_button_width) // 2
        reset_y = 520

        if self.reset_hovered:
            sw = int(self.reset_button_width * self.hover_scale)
            sh = int(self.reset_button_height * self.hover_scale)
            scaled = pygame.transform.smoothscale(self.reset_frame_original, (sw, sh))
            sx = reset_x - (sw - self.reset_button_width) // 2
            sy = reset_y - (sh - self.reset_button_height) // 2
            screen.blit(scaled, (sx, sy))

            text = self.render_styled_text("Reset to Default", self.reset_font)
            text_scaled = pygame.transform.smoothscale(text, (int(text.get_width() * self.hover_scale), int(text.get_height() * self.hover_scale)))
            screen.blit(text_scaled, (sx + (sw - text_scaled.get_width()) // 2, sy + (sh - text_scaled.get_height()) // 2))
        else:
            if self.reset_frame_base:
                screen.blit(self.reset_frame_base, (reset_x, reset_y))
            text = self.render_styled_text("Reset to Default", self.reset_font)
            screen.blit(text, (reset_x + (self.reset_button_width - text.get_width()) // 2,
                              reset_y + (self.reset_button_height - text.get_height()) // 2))

        # Nút Back - góc trái trên
        back_x = 30
        back_y = 30

        if self.back_hovered:
            sw = int(self.back_button_width * self.hover_scale)
            sh = int(self.back_button_height * self.hover_scale)
            scaled = pygame.transform.smoothscale(self.back_frame_original, (sw, sh))
            sx = back_x - (sw - self.back_button_width) // 2
            sy = back_y - (sh - self.back_button_height) // 2
            screen.blit(scaled, (sx, sy))

            text = self.render_styled_text("Back", self.back_font)
            text_scaled = pygame.transform.smoothscale(text, (int(text.get_width() * self.hover_scale), int(text.get_height() * self.hover_scale)))
            screen.blit(text_scaled, (sx + (sw - text_scaled.get_width()) // 2, sy + (sh - text_scaled.get_height()) // 2))
        else:
            if self.back_frame_base:
                screen.blit(self.back_frame_base, (back_x, back_y))
            text = self.render_styled_text("Back", self.back_font)
            screen.blit(text, (back_x + (self.back_button_width - text.get_width()) // 2,
                              back_y + (self.back_button_height - text.get_height()) // 2))

        if self.dev_image:
            screen.blit(self.dev_image, (SCREEN_WIDTH - self.dev_image.get_width() - self.dev_margin_x,
                                        SCREEN_HEIGHT - self.dev_image.get_height() - self.dev_margin_y))

    def run(self, screen, clock):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            clicked = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clicked = True

            # Hover Back
            back_rect = pygame.Rect(30, 30, self.back_button_width, self.back_button_height)
            currently_hovered = back_rect.collidepoint(mouse_pos)

            if currently_hovered and not self.last_back_hover_state:
                self.sound_manager.play_hover()

            self.back_hovered = currently_hovered
            self.last_back_hover_state = currently_hovered

            # Hover Reset
            reset_rect = pygame.Rect((SCREEN_WIDTH - self.reset_button_width) // 2, 520, self.reset_button_width, self.reset_button_height)
            currently_reset_hovered = reset_rect.collidepoint(mouse_pos)

            if currently_reset_hovered and not self.last_reset_hover_state:
                self.sound_manager.play_hover()

            self.reset_hovered = currently_reset_hovered
            self.last_reset_hover_state = currently_reset_hovered

            # Kéo Music
            if pygame.mouse.get_pressed()[0]:
                music_y = 200
                if music_y - 20 <= mouse_pos[1] <= music_y + 55 + 20:
                    frame_x = (SCREEN_WIDTH - 400) // 2
                    rel_x = max(0, min(mouse_pos[0] - frame_x, 400))
                    new_vol = rel_x / 400
                    if abs(new_vol - self.music_volume) > 0.01:
                        self.sound_manager.play_click()
                        self.music_volume = new_vol
                        pygame.mixer.music.set_volume(self.music_volume)

            # Kéo Sound
            if pygame.mouse.get_pressed()[0]:
                sound_y = 370
                if sound_y - 20 <= mouse_pos[1] <= sound_y + 55 + 20:
                    frame_x = (SCREEN_WIDTH - 400) // 2
                    rel_x = max(0, min(mouse_pos[0] - frame_x, 400))
                    new_vol = rel_x / 400
                    if abs(new_vol - self.sound_volume) > 0.01:
                        self.sound_manager.play_click()
                        self.sound_volume = new_vol
                        self.sound_manager.sound_volume = new_vol
                        self.sound_manager.update_volume()

            # Click Reset
            if clicked and self.reset_hovered:
                self.sound_manager.play_click()
                self.music_volume = self.DEFAULT_MUSIC_VOLUME
                self.sound_volume = self.DEFAULT_SOUND_VOLUME
                pygame.mixer.music.set_volume(self.music_volume)
                self.sound_manager.sound_volume = self.DEFAULT_SOUND_VOLUME
                self.sound_manager.update_volume()

            # Click Back
            if clicked and self.back_hovered:
                self.sound_manager.play_click()
                return "menu"

            self.draw(screen)
            pygame.display.update()
            clock.tick(60)