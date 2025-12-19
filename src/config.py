# src/config.py
import os

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS_PATH = os.path.join(BASE_DIR, "assets", "fonts", "guavacandy.ttf")
IMAGES_PATH = os.path.join(BASE_DIR, "assets", "images") + os.sep
SOUNDS_PATH = os.path.join(BASE_DIR, "assets", "sounds") + os.sep  # Thêm dòng này

# Đường dẫn tới file cursor (giữ lại dù không dùng nữa)
CURSOR_PATH = os.path.join(IMAGES_PATH, "cursor.png")