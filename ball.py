import pygame
class Ball(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("ball.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        #BAll parameters
        self.directionx = 1
        self.directiony = 1
        self.speed = 12
    
        
    def update(self):

        self.rect.centerx +=self.speed*self.directionx
        self.rect.centery +=self.speed*self.directiony

        if self.rect.left<=10 or self.rect.right>1270:
            self.directionx *= -1
        if self.rect.top<=10 or self.rect.bottom>=720:
            self.directiony *= -1