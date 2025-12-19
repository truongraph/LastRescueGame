import pygame
from src.config import IMAGES_PATH, SCREEN_WIDTH, SCREEN_HEIGHT, FONTS_PATH, SOUNDS_PATH
from src.sound_manager import SoundManager

class ChapterScreen:
    def __init__(self):
        self.background = pygame.image.load(IMAGES_PATH + "menu_bg.png")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.title_font = pygame.font.Font(FONTS_PATH, 50)
        self.title_text = self.title_font.render("Chapters", True, (255, 215, 0))

        self.sound_manager = SoundManager()

        # Kích thước thẻ bài
        self.normal_width = 250
        self.normal_height = 350
        self.special_width = 250
        self.special_height = 350

        # Load hình chapter
        try:
            self.done_chapter = pygame.image.load(IMAGES_PATH + "done_chapter.png").convert_alpha()
            self.done_chapter = pygame.transform.smoothscale(self.done_chapter, (self.normal_width, self.normal_height))
        except: self.done_chapter = None

        try:
            self.block_chapter = pygame.image.load(IMAGES_PATH + "block_chapter.png").convert_alpha()
            self.block_chapter = pygame.transform.smoothscale(self.block_chapter, (self.normal_width, self.normal_height))
        except: self.block_chapter = None

        try:
            self.final_chapter = pygame.image.load(IMAGES_PATH + "final_chapter.png").convert_alpha()
            self.final_chapter = pygame.transform.smoothscale(self.final_chapter, (self.special_width, self.special_height))
        except: self.final_chapter = None

        # Sao
        self.star_size = 40
        try:
            self.star_light = pygame.image.load(IMAGES_PATH + "star_light.png").convert_alpha()
            self.star_light = pygame.transform.smoothscale(self.star_light, (self.star_size, self.star_size))
        except: self.star_light = None

        try:
            self.star_dark = pygame.image.load(IMAGES_PATH + "star_dark.png").convert_alpha()
            self.star_dark = pygame.transform.smoothscale(self.star_dark, (self.star_size, self.star_size))
        except: self.star_dark = None

        # Nút Previous / Next gốc + xám
        self.arrow_size = 80
        try:
            self.prev_btn_original = pygame.image.load(IMAGES_PATH + "previous.png").convert_alpha()
            self.prev_btn_original = pygame.transform.smoothscale(self.prev_btn_original, (self.arrow_size, self.arrow_size))
            self.prev_btn_gray = self.prev_btn_original.copy()
            self.prev_btn_gray.fill((100, 100, 100, 255), special_flags=pygame.BLEND_MULT)
        except:
            self.prev_btn_original = self.prev_btn_gray = None

        try:
            self.next_btn_original = pygame.image.load(IMAGES_PATH + "next.png").convert_alpha()
            self.next_btn_original = pygame.transform.smoothscale(self.next_btn_original, (self.arrow_size, self.arrow_size))
            self.next_btn_gray = self.next_btn_original.copy()
            self.next_btn_gray.fill((100, 100, 100, 255), special_flags=pygame.BLEND_MULT)
        except:
            self.next_btn_original = self.next_btn_gray = None

        # Back button
        self.back_button_width = 160
        self.back_button_height = 40
        try:
            self.back_frame_base = pygame.transform.smoothscale(
                pygame.image.load(IMAGES_PATH + "menu_button.png").convert_alpha(),
                (self.back_button_width, self.back_button_height)
            )
        except: self.back_frame_base = None
        self.back_font = pygame.font.Font(FONTS_PATH, 20)

        # Developer logo
        try:
            dev_original = pygame.image.load(IMAGES_PATH + "develop.png").convert_alpha()
            dev_target_width = 150
            ratio = dev_target_width / dev_original.get_width()
            self.dev_image = pygame.transform.smoothscale(dev_original, (dev_target_width, int(dev_original.get_height() * ratio)))
        except: self.dev_image = None
        self.dev_margin = 20

        # Slider
        self.total_slides = 6
        self.current_slide = 0
        self.target_offset_x = 0
        self.current_offset_x = 0

        # Hover chapter + hiệu ứng zoom mượt
        self.chapter_hovered = None  # idx đang hover
        self.last_chapter_hovered = None
        self.hover_target_scale = {}  # target scale cho từng chapter
        self.current_scales = {}       # scale hiện tại (mượt mà)
        self.zoom_speed = 0.15         # tốc độ easing (giống fade trong loading)

        # Khởi tạo scale mặc định = 1.0 cho tất cả chapter
        for i in range(11):
            self.hover_target_scale[i] = 1.0
            self.current_scales[i] = 1.0

        # Hover nút
        self.prev_hovered = self.next_hovered = self.back_hovered = False
        self.last_prev_hover = self.last_next_hover = self.last_back_hover = False

        # Danh sách chapter
        self.chapters = [
            {"type": "done", "name": "Chapter 1"}, {"type": "block", "name": "Chapter 2"},
            {"type": "block", "name": "Chapter 3"}, {"type": "block", "name": "Chapter 4"},
            {"type": "block", "name": "Chapter 5"}, {"type": "block", "name": "Chapter 6"},
            {"type": "block", "name": "Chapter 7"}, {"type": "block", "name": "Chapter 8"},
            {"type": "block", "name": "Chapter 9"}, {"type": "block", "name": "Chapter 10"},
            {"type": "final", "name": "Special Chapter"}
        ]

    def get_chapter_image(self, idx):
        if idx >= 10:
            return self.final_chapter
        return self.done_chapter if self.chapters[idx]["type"] == "done" else self.block_chapter

    def get_star(self, idx):
        return self.star_light if self.chapters[idx]["type"] == "done" else self.star_dark

    def draw_stars(self, screen, center_x, y, idx):
        star = self.get_star(idx)
        if not star: return
        spacing = 15
        total_w = 3 * self.star_size + 2 * spacing
        start_x = center_x - total_w // 2
        for i in range(3):
            screen.blit(star, (start_x + i * (self.star_size + spacing), y))

    def draw_chapter(self, screen, img, center_x, center_y, idx):
        if not img: return
        scale = self.current_scales.get(idx, 1.0)
        if scale != 1.0:
            w = int(img.get_width() * scale)
            h = int(img.get_height() * scale)
            scaled = pygame.transform.smoothscale(img, (w, h))
            screen.blit(scaled, (center_x - w // 2, center_y - h // 2))
        else:
            screen.blit(img, (center_x - img.get_width() // 2, center_y))

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        # Title
        title_x = (SCREEN_WIDTH - self.title_text.get_width()) // 2
        screen.blit(self.title_text, (title_x, 50))

        offset_x = self.current_offset_x
        center_y = 170
        chapter_spacing = 330

        # Vẽ chapter thường
        for slide_idx in range(5):
            base_x = slide_idx * SCREEN_WIDTH + offset_x
            screen_center_x = base_x + SCREEN_WIDTH // 2

            # Chapter trái
            idx1 = slide_idx * 2
            cx1 = screen_center_x - chapter_spacing // 2
            self.draw_chapter(screen, self.get_chapter_image(idx1), cx1, center_y, idx1)
            self.draw_stars(screen, cx1, center_y + self.normal_height + 15, idx1)

            # Chapter phải
            idx2 = slide_idx * 2 + 1
            cx2 = screen_center_x + chapter_spacing // 2
            self.draw_chapter(screen, self.get_chapter_image(idx2), cx2, center_y, idx2)
            self.draw_stars(screen, cx2, center_y + self.normal_height + 15, idx2)

        # Special chapter
        special_base_x = 5 * SCREEN_WIDTH + offset_x
        special_cx = special_base_x + SCREEN_WIDTH // 2
        self.draw_chapter(screen, self.get_chapter_image(10), special_cx, center_y, 10)
        self.draw_stars(screen, special_cx, center_y + self.special_height + 20, 10)

        # Nút Previous / Next
        arrow_margin = 120
        arrow_y = center_y + self.normal_height // 2 - self.arrow_size // 2 + 20
        prev_img = self.prev_btn_gray if self.current_slide == 0 else self.prev_btn_original
        next_img = self.next_btn_gray if self.current_slide == self.total_slides - 1 else self.next_btn_original

        if prev_img:
            screen.blit(prev_img, (arrow_margin, arrow_y))
        if next_img:
            screen.blit(next_img, (SCREEN_WIDTH - arrow_margin - self.arrow_size, arrow_y))

        # Dots
        dot_y = SCREEN_HEIGHT - 80
        dot_spacing = 35
        start_x = SCREEN_WIDTH // 2 - (self.total_slides * dot_spacing - dot_spacing) // 2
        for i in range(self.total_slides):
            color = (255, 215, 0) if i == self.current_slide else (120, 120, 120)
            radius = 10 if i == self.current_slide else 6
            pygame.draw.circle(screen, color, (start_x + i * dot_spacing, dot_y), radius)

        # Back button + Developer logo (giữ nguyên)
        back_x, back_y = 30, 30
        if self.back_frame_base:
            screen.blit(self.back_frame_base, (back_x, back_y))
        text = self.render_styled_text("Back", self.back_font)
        screen.blit(text, (back_x + (self.back_button_width - text.get_width()) // 2,
                          back_y + (self.back_button_height - text.get_height()) // 2))

        if self.dev_image:
            screen.blit(self.dev_image, (SCREEN_WIDTH - self.dev_image.get_width() - self.dev_margin,
                                        SCREEN_HEIGHT - self.dev_image.get_height() - self.dev_margin))

    def render_styled_text(self, text, font=None):
        if font is None: font = self.back_font
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

    def go_to_slide(self, slide_idx):
        self.current_slide = max(0, min(slide_idx, self.total_slides - 1))
        self.target_offset_x = -self.current_slide * SCREEN_WIDTH

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

            # Hover nút
            arrow_margin = 120
            arrow_y = 170 + self.normal_height // 2 - self.arrow_size // 2 + 20
            prev_rect = pygame.Rect(arrow_margin, arrow_y, self.arrow_size, self.arrow_size)
            next_rect = pygame.Rect(SCREEN_WIDTH - arrow_margin - self.arrow_size, arrow_y, self.arrow_size, self.arrow_size)
            back_rect = pygame.Rect(30, 30, self.back_button_width, self.back_button_height)

            self.prev_hovered = prev_rect.collidepoint(mouse_pos) and self.current_slide > 0
            self.next_hovered = next_rect.collidepoint(mouse_pos) and self.current_slide < self.total_slides - 1
            self.back_hovered = back_rect.collidepoint(mouse_pos)

            if self.prev_hovered and not self.last_prev_hover: self.sound_manager.play_hover()
            if self.next_hovered and not self.last_next_hover: self.sound_manager.play_hover()
            if self.back_hovered and not self.last_back_hover: self.sound_manager.play_hover()

            self.last_prev_hover, self.last_next_hover, self.last_back_hover = self.prev_hovered, self.next_hovered, self.back_hovered

            # Hover chapter + cập nhật target scale
            current_hover_chap = None
            visible_slide = round(-self.current_offset_x / SCREEN_WIDTH)
            center_y = 170
            chapter_spacing = 330

            if 0 <= visible_slide < 5:
                screen_center_x = visible_slide * SCREEN_WIDTH + SCREEN_WIDTH // 2 + self.current_offset_x
                rel_x = mouse_pos[0] - screen_center_x
                if center_y - 100 < mouse_pos[1] < center_y + self.normal_height + 100:
                    if abs(rel_x) < chapter_spacing // 2 + self.normal_width // 2:
                        current_hover_chap = visible_slide * 2 if rel_x < 0 else visible_slide * 2 + 1
            elif visible_slide == 5:
                if 100 < mouse_pos[1] < SCREEN_HEIGHT - 100:
                    current_hover_chap = 10

            # Cập nhật target scale
            for i in range(11):
                self.hover_target_scale[i] = 1.05 if i == current_hover_chap else 1.0

            if current_hover_chap != self.last_chapter_hovered and current_hover_chap is not None:
                self.sound_manager.play_hover()

            self.last_chapter_hovered = current_hover_chap

            # Easing scale mượt mà (giống fade trong loading)
            for i in range(11):
                diff = self.hover_target_scale[i] - self.current_scales[i]
                if abs(diff) > 0.001:
                    self.current_scales[i] += diff * self.zoom_speed

            # Click
            if clicked:
                if self.prev_hovered:
                    self.sound_manager.play_click()
                    self.go_to_slide(self.current_slide - 1)
                if self.next_hovered:
                    self.sound_manager.play_click()
                    self.go_to_slide(self.current_slide + 1)
                if self.back_hovered:
                    self.sound_manager.play_click()
                    return "menu"

                if current_hover_chap is not None:
                    self.sound_manager.play_click()
                    idx = current_hover_chap
                    if idx < 10:
                        if self.chapters[idx]["type"] == "done":
                            print(f"Bắt đầu {self.chapters[idx]['name']}")
                        else:
                            print(f"{self.chapters[idx]['name']} chưa mở khóa")
                    else:
                        print("Special Chapter - chưa mở khóa")

            # Animation trượt slider
            if abs(self.current_offset_x - self.target_offset_x) > 1:
                diff = self.target_offset_x - self.current_offset_x
                self.current_offset_x += diff * 0.2
            else:
                self.current_offset_x = self.target_offset_x
                self.current_slide = round(-self.current_offset_x / SCREEN_WIDTH)

            self.draw(screen)
            pygame.display.update()
            clock.tick(60)