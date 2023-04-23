import pygame,sys
from random import randint, choice


class Spritesheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha() # loading spritesheet

    def get_image(self, x, y, width, height):
        '''returns surface(frame) from spritesheet using position and size'''
        image = pygame.Surface((width, height), pygame.SRCALPHA) 
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        return image

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x,y,  screen_width, screen_height):
        '''
        x,y --> target direction
        screeen_width and height used to spawn obstacles at random postion out of the screen
        '''
        super().__init__()
        self.speed = randint(3,9) # random speed for frame duration and velocity
        self.spritesheet = Spritesheet('graphics/rock_2.png')
        self.frame_duration = 5*self.speed
        self.num_frames = 32

        # loading obstacle frames
        self.frames = []
        for row in range(8):
            for column in range(8):
                self.frames.append(self.spritesheet.get_image(column * 128, row*128, 128, 128))
        self.current_frame = 0
        self.image = self.frames[0]
        self.last_update_time = pygame.time.get_ticks()

        # directing obstacle towards target direction with 100 px offset
        direct_x = randint(x-100, x +100)
        direct_y = randint(y-100, y +100)

        #spawning obstacle out of the screen at random position
        spawn_x = choice([randint(-100,0), randint(screen_width,screen_width+100), randint(0, screen_width)])
        if spawn_x < 0 or spawn_x > screen_width: 
            # if x is out of screen then y can be any value
            spawn_y = randint(-100,screen_height+100) 
        else: 
            # if x is inside of screen then y will be out of screen
            spawn_y = choice([randint(-100,0), randint(screen_height,screen_height+100)])

        pos = (spawn_x,spawn_y)
        self.rect = self.image.get_rect(topleft = pos)

        # direction
        direction_vector = pygame.math.Vector2(direct_x - self.rect.x, direct_y - self.rect.y)
        direction_vector.normalize_ip() # unit vector
        self.direction = direction_vector * self.speed

    def update(self):
        # moving obstacle
        self.rect.move_ip(self.direction)

        # updating obstacle sprite
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.frame_duration:
            self.current_frame = (self.current_frame + 1) % self.num_frames
            self.image = self.frames[self.current_frame]
            self.last_update_time = current_time

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class Blast(pygame.sprite.Sprite):
    def __init__(self, pos,frames):
        super().__init__()
        self.frame_duration = 40
        self.num_frames = 48

        self.current_frame = 0
        self.frames = frames
        self.image = self.frames[0]
        self.last_update_time = pygame.time.get_ticks()
        self.rect = self.image.get_rect(topleft = pos)
    
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.frame_duration:
            self.current_frame = (self.current_frame + 1) % self.num_frames
            self.image = self.frames[self.current_frame]
            self.last_update_time = current_time
        if self.current_frame == self.num_frames -1:
            self.kill()

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('Obstacle')
    clock = pygame.time.Clock()
    obstacles = pygame.sprite.Group()
    blast_sprites = pygame.sprite.RenderPlain()
    BG = (50,50,50)
    spritesheet = Spritesheet('graphics/blast_2.png')
    spritesheet.sheet= pygame.transform.scale(spritesheet.sheet, (1024,768))
    frames = []
    for row in range(8):
        for column in range(6):
            frames.append(spritesheet.get_image(column * 128, row*128, 128, 128))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for i in range(10):
                        x,y = pygame.mouse.get_pos()
                        obstacles.add(Obstacle(x,y, 800,800))
                if event.key == pygame.K_BACKSPACE:
                    for obstacle in obstacles:
                        blast_sprites.add(Blast(obstacle.rect.topleft,frames))
                        obstacle.kill()
        screen.fill(BG)

        blast_sprites.draw(screen)
        blast_sprites.update()

        obstacles.draw(screen)
        obstacles.update()
        pygame.display.flip()
        clock.tick(60)
