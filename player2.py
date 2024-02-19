import pygame
class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("cat2.png")
        self.rect = self.image.get_rect()
        self.rect.x = 1216

        self.speed = 10

    def update(self):
        key=pygame.key.get_pressed()
        if key[pygame.K_UP] and self.rect.top>=10:
            self.rect.y -= self.speed
        elif key[pygame.K_DOWN] and self.rect.bottom<=724:
            self.rect.y += self.speed