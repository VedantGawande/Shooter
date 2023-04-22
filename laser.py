import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self,pos, speed, screen_height, screen_width,angle):
        super().__init__()
        self.image = pygame.image.load('bullet.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.h = screen_height
        self.w = screen_width
        self.angle = angle
        self.direction = pygame.math.Vector2(1, 0).rotate(-self.angle)
        self.speed = 10
        self.rotate_(pos)
    
    def rotate_(self,pos):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center = self.original_image.get_rect().center)
        self.rect = self.image.get_rect(midbottom = pos)


    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.h+50 or self.rect.x <= -50 or self.rect.x >= self.w+50:
            self.kill()

    def update(self):
        self.rect.move_ip(self.direction * self.speed)
        self.destroy()