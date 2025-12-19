# src/sound_manager.py
import pygame

class SoundManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.sound_volume = 0.7  # Mặc định 70%
            cls._instance.hover_sound = None
            cls._instance.click_sound = None
        return cls._instance

    def load_sounds(self, sounds_path):
        try:
            self.hover_sound = pygame.mixer.Sound(sounds_path + "button_hover.wav")
        except pygame.error:
            self.hover_sound = None

        try:
            self.click_sound = pygame.mixer.Sound(sounds_path + "button_click.wav")
        except pygame.error:
            self.click_sound = None

        self.update_volume()

    def update_volume(self):
        vol = self.sound_volume if self.sound_volume > 0 else 0.0
        if self.hover_sound:
            self.hover_sound.set_volume(vol)
        if self.click_sound:
            self.click_sound.set_volume(vol)

    def play_hover(self):
        if self.sound_volume > 0 and self.hover_sound:
            self.hover_sound.play()

    def play_click(self):
        if self.sound_volume > 0 and self.click_sound:
            self.click_sound.play()