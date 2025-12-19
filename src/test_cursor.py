# test_cursor.py
import pygame, sys, os
from config import IMAGES_PATH, SCREEN_WIDTH, SCREEN_HEIGHT, FPS

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

cursor_path = os.path.join(IMAGES_PATH, "cursor.png")
print("Loading cursor from:", cursor_path)
cursor = pygame.image.load(cursor_path).convert_alpha()
# resize nếu quá lớn (tuỳ bạn)
cursor = pygame.transform.smoothscale(cursor, (48, 48))
offset = (cursor.get_width()//2, cursor.get_height()//2)

bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
bg.fill((30, 30, 40))  # nền dễ thấy

pygame.mouse.set_visible(False)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    screen.blit(bg, (0,0))

    # vẽ 1 số UI giả để kiểm tra bị che hay không
    pygame.draw.rect(screen, (80,80,120), (100,100,300,200))
    pygame.draw.circle(screen, (200,50,50), (600,300), 60)

    mx, my = pygame.mouse.get_pos()
    screen.blit(cursor, (mx - offset[0], my - offset[1]))

    pygame.display.flip()
    clock.tick(FPS)
