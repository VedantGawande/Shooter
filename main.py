import pygame,sys,os
import math
from laser import Laser
import  obstacles

class Gun(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.image.load('shotgun.png').convert_alpha()
        self.image = pygame.transform.flip(pygame.transform.scale(self.image,(100,20)), False,True)
        self.rect = self.image.get_rect(center = pos)
        
        self.original_image = self.image
        self.angle = 0

        self.lasers = pygame.sprite.Group()

    def shoot_laser(self,player_sprite):
        self.bangle = self.get_angle()
        laser_sprite = Laser(self.rect.center, 0,screen_height,screen_width, self.bangle)
        self.lasers.add(laser_sprite)
        self.direction = pygame.math.Vector2(1, 0).rotate(-self.bangle)
        player_sprite.recoil(self.direction)

    def get_angle(self):
        mouse_pos = pygame.mouse.get_pos()
        x, y = self.rect.center
        dx, dy = mouse_pos[0] - x, mouse_pos[1] - y

        # Calculate the angle using angle_to method
        angle = pygame.math.Vector2(dx, dy).angle_to(pygame.math.Vector2(1, 0))
        return angle
    
    def roate(self):
        self.get_angle()
        self.angle = self.get_angle()

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center = self.original_image.get_rect().center)

    def update(self):
        self.lasers.update()
        self.lasers.draw(screen)

        self.roate()

        x = player_sprite.rect.centerx
        y= player_sprite.rect.centery
        self.rect.centerx = x
        self.rect.centery = y


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class Player(pygame.sprite.Sprite):
    def __init__(self,gravity):
        super().__init__()
        #player init
        self.image = pygame.image.load('player_2.png')
        self.rect = self.image.get_rect(center= (screen_width/2, screen_height/2))
        
        #gun init
        self.gun_sprite = Gun((self.rect.centerx, self.rect.centery))
        self.gun = pygame.sprite.GroupSingle(self.gun_sprite)

        #player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 5
        self.gravity = 0.5
        self.jump_speed = -16
    
    def move_player(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def recoil(self, direction):
        self.direction = direction *-1
    
    def off_screen(self):
        if self.rect.y >= screen_height:
            self.rect.y = -60
            self.direction.y = 0.5
        elif self.rect.y <= -60:
            self.rect.y = screen_height
    
        if self.rect.x >= screen_width:
            self.rect.x = -60
        elif self.rect.x <= -60:
            self.rect.x = screen_width

    def friction(self, direction):
        if self.rect.x != 0:
            self.rect.x += direction.x * -1
        
        self.rect.y += direction.y * -1

    def update(self):
        # self.friction(self.direction)
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        self.move_player()
        self.off_screen()
        self.gun.draw(screen)
        self.gun.update()

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def collision(sprite_1, sprite_2):
    col = pygame.sprite.collide_rect(sprite_1,sprite_2)
    return col

def game_over():
    global lives, high_score,score

    game_over_surf = font.render('GAME OVER! Press Space', False, (255,100,155))
    game_over_rect = game_over_surf.get_rect(center=(screen_width/2,screen_height/2))
    screen.blit(game_over_surf, game_over_rect)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        lives= 5

        player_sprite.image = pygame.image.load('player_1.png')
        player_sprite.rect.center = (screen_width/2, screen_height/2)

        if int(high_score) < score:
            with open('high_score.txt','w') as h:
                h.write(str(score))
                h.close()
        with open('high_score.txt') as h:
            high_score = h.read()
            h.close()
        score = 0

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    # Game init
    pygame.init()
    screen_height = 800
    screen_width = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    pygame.display.set_caption("My Game")
    FPS = 60
    pygame.font.init()
    font = pygame.font.SysFont('arialblack', int(0.04*screen_height))

    # Player
    player_sprite = Player(10)
    player = pygame.sprite.GroupSingle(player_sprite)
    player_dead = pygame.image.load('player_dead.png')

    # Obstacle
    obstacles_group = pygame.sprite.Group()
    spawn_obstacle = pygame.USEREVENT + 1
    obstacle_timer = 1600
    obs_num = 2
    pygame.time.set_timer(spawn_obstacle,obstacle_timer)

    blast_sprites = pygame.sprite.Group()

    #Sound
    pygame.mixer.init()
    blast = pygame.mixer.Sound('blast.wav')

    # Read score
    with open('high_score.txt') as h:
        high_score = h.read()
        h.close()
    score = 0

    # Text render
    score_surf = font.render(str(score),True, (200,180,210))
    high_score_surf = font.render(str(high_score),True, (100,180,210))

    lives = 1
    lives_surf = font.render(str(lives),True, 'red')

    # Ammo
    max_bullets = 2
    bullet_left = max_bullets - len(player_sprite.gun_sprite.lasers)
    ammo_img = pygame.transform.rotate(pygame.image.load('bullet.png').convert_alpha(), 90)

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == spawn_obstacle and lives>0:
                for i in range(int(obs_num)):
                    obstacles_group.add(obstacles.Obstacle(player_sprite.rect.x, player_sprite.rect.y, screen_width,screen_height))

            if event.type == pygame.MOUSEBUTTONDOWN and lives>0 and len(player_sprite.gun_sprite.lasers) < max_bullets:
                player_sprite.gun_sprite.shoot_laser(player_sprite)
        
        # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        screen.fill((30,30,30))

        if lives >0:
            # collision
            for obstacle in obstacles_group:
                for laser in player_sprite.gun_sprite.lasers:
                    if collision(obstacle, laser):
                        # obs_num += 0.1
                        score += 10
                        blast_sprites.add(obstacles.Blast(obstacle.rect.topleft))
                        obstacle.destroy()
                        laser.kill()
                        blast.play(0,0,0)

                if collision(obstacle, player_sprite):
                    lives -= 1
                    obstacle.destroy()

        else:
            # Game Over
            player_sprite.image = player_dead
            player_sprite.direction = pygame.math.Vector2(0,0)
            obstacles_group.empty()
            game_over()
        
        # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        #ammo display
        bullet_left = max_bullets - len(player_sprite.gun_sprite.lasers)
        for i in range(bullet_left):
            screen.blit(ammo_img, (10+i*ammo_img.get_width(),screen_height-40))


        # Text Rendering
        score_surf = font.render(f'Score: {score}',True, (200,180,210))
        screen.blit(score_surf, (10,10))

        high_score_surf = font.render(f'High Score: {high_score}',True, (100,180,210))
        screen.blit(high_score_surf, (screen_width/2-high_score_surf.get_width()/2,10))

        lives_surf = font.render(f'Lives: {lives}',True, 'red')
        screen.blit(lives_surf, (screen_width-lives_surf.get_width()-10,10))


        #Sprites draw and update
        blast_sprites.draw(screen)
        blast_sprites.update()

        obstacles_group.draw(screen)
        obstacles_group.update()

        player.draw(screen)
        player.update()

        # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        pygame.display.update()
