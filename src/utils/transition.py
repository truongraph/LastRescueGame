# src/utils/transition.py
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT  # Đổi từ src.config sang config (phù hợp với game.py)


def fade_transition(screen, clock, duration_ms=300):
    """
    Hiệu ứng fade to black nhanh và mượt.

    Args:
        screen: pygame surface hiện tại
        clock: pygame clock
        duration_ms: thời gian fade hoàn tất (ms). Mặc định 300ms → rất nhanh, đẹp.
                     Có thể thử 200 (siêu nhanh) hoặc 400 (chậm hơn một chút).
    """
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))

    steps = 30  # Số bước fade (càng nhiều càng mượt, nhưng không cần quá nhiều)
    alpha_step = 255 / steps
    delay_per_step = duration_ms // steps

    alpha = 0
    fade_surface.set_alpha(alpha)

    for _ in range(steps):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        alpha += alpha_step
        if alpha > 255:
            alpha = 255
        fade_surface.set_alpha(int(alpha))

        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        clock.tick(1000 // delay_per_step)  # Giữ tốc độ chính xác theo duration

    # Không cần giữ đen thêm, trả về ngay để state mới render
    # (frame đầu tiên của state mới sẽ xuất hiện gần như tức thì)