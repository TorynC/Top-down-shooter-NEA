import pygame,sys,math
#pygame setup
pygame.init()
pygame.font.get_init()

TEXT_FONT = pygame.font.Font("assets/font.otf", 32)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
WINDOWSIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)

DISPLAY = pygame.display.set_mode(WINDOWSIZE)
CLOCK = pygame.time.Clock()
pygame.display.set_caption("Grave Fighter")

bullets = []
enemies = []

score = 0 
'''class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface= pygame.display.get_surface()
        self.ground_surf = pygame.transform.scale(pygame.image.load('assets/map1.png').convert(),(MAPBOUND_X,MAPBOUND_Y))
        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0]//2
        self.half_h = self.display_surface.get_size()[1]//2

    def custom_draw(self,player):
        self.offset.x = player.rect.centerx - self.half_w
        self.offset.y = player.rect.centery - self.half_h
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf,ground_offset)

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)'''
        

#player class
class Player(pygame.sprite.Sprite):
    def __init__(self,group):
        super().__init__(group)
        self.health = self.max_health = 4 #double assignment
        self.image = pygame.transform.scale(pygame.image.load("assets/test.png").convert_alpha(),(40,40))
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
        self.speed = 5
        self.direction = pygame.math.Vector2()

        #graphics setup 
        self.frame_count = 0 
        self.import_player_assets()
        self.status = 'idle'
        self.animation_speed = 0.15

    def import_player_assets(self):
        #dictionary of animations 
        self.animations = {"up":[pygame.transform.scale(pygame.image.load("assets/player sprite/tile006.png").convert_alpha(),(40,40)),pygame.transform.scale(pygame.image.load("assets/player sprite/tile007.png").convert_alpha(),(40,40)),
pygame.transform.scale(pygame.image.load("assets/player sprite/tile008.png").convert_alpha(),(40,40))],
        "down":[pygame.transform.scale(pygame.image.load("assets/player sprite/tile001.png").convert_alpha(),(40,40)),
pygame.transform.scale(pygame.image.load("assets/player sprite/tile002.png").convert_alpha(),(40,40))],
        "right":[pygame.transform.scale(pygame.image.load("assets/player sprite/tile003.png").convert_alpha(),(40,40)),pygame.transform.scale(pygame.image.load("assets/player sprite/tile004.png").convert_alpha(),(40,40)),
pygame.transform.scale(pygame.image.load("assets/player sprite/tile005.png").convert_alpha(),(40,40))],
        "left":[pygame.transform.scale(pygame.transform.flip(pygame.image.load("assets/player sprite/tile003.png").convert_alpha(),True,False),(40,40)),pygame.transform.scale(pygame.transform.flip(pygame.image.load("assets/player sprite/tile004.png").convert_alpha(),True,False),(40,40)),
pygame.transform.scale(pygame.transform.flip(pygame.image.load("assets/player sprite/tile005.png").convert_alpha(),True,False),(40,40))],
        "idle":[pygame.transform.scale(pygame.image.load("assets/player sprite/tile000.png").convert_alpha(),(40,40))]}

    def input(self):
        keys = pygame.key.get_pressed()

        #movement input 
        if keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.status = "down"
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

    def move(self,speed):
        if self.direction.magnitude()!=0:
            self.direction = self.direction.normalize()
        
        self.rect.centerx += self.direction.x * speed
        self.rect.centery += self.direction.y * speed
        if self.rect.right >= SCREEN_WIDTH:  
            self.rect.right = SCREEN_WIDTH
        if self.rect.left <=0:
            self.rect.left = 0
        if self.rect.bottom >= SCREEN_HEIGHT:  
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.top <=0:
            self.rect.top = 0

    def get_status(self):
        #idle_status
        if self.direction.x == 0 and self.direction.y == 0:
            self.status = 'idle'

    def animate(self):
        animation = self.animations[self.status]
        #loop over frame counter
        self.frame_count += self.animation_speed
        if self.frame_count >= len(animation):
            self.frame_count = 0
        #set the image
        self.image = animation[int(self.frame_count)]
        self.rect = self.image.get_rect(center = self.rect.center)
        
    def update(self):
        self.input()
        self.get_status()
        self.animate()
        self.move(self.speed)

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.x = x
        self.y = y
        self.health = 4
        self.image = pygame.transform.scale(pygame.image.load("assets/enemy sprite 2/E2-tile000.png").convert_alpha(),(40,40))
        self.rect = self.image.get_rect(center = (self.x,self.y))
        self.animations = [pygame.transform.scale(pygame.image.load("assets/enemy sprite 3/slime_animation_0.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/enemy sprite 3/slime_animation_1.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/enemy sprite 3/slime_animation_2.png").convert_alpha(),(40,40))]
        self.animationcount = 0
        enemies.append(self)

        
    def update(self):
        #animation
        if self.animationcount +1 == 12:
            self.animationcount = 0
        self.animationcount += 1
        
        #for following player 
        player_center = [SCREEN_WIDTH/2,SCREEN_HEIGHT/2]
        if player_center[0] > self.rect.centerx - camera_group.offset.x:
            self.rect.centerx += 3
        elif player_center[0] < self.rect.centerx - camera_group.offset.x:
            self.rect.centerx -= 3

        if player_center[1] > self.rect.centery - camera_group.offset.y:
            self.rect.centery += 3
        elif player_center[1] < self.rect.centery - camera_group.offset.y:
            self.rect.centery -= 3
        
        #+2 or -1x
        DISPLAY.blit(self.animations[self.animationcount//4],(self.rect.centerx-camera_group.offset.x,self.rect.centery-camera_group.offset.y))
        
#bullet class
class Bullet():
    def __init__(self,angle,x,y):

        self.image = pygame.transform.scale(pygame.image.load("assets/bullet.png").convert_alpha(),(16,16))
        self.rect = self.image.get_rect(center = (x,y) )
        self.angle = angle
        self.speed = 15

    def change(self):
        self.rect.centery -= int(math.sin(self.angle) * self.speed)
        self.rect.centerx -= int(math.cos(self.angle) * self.speed)
        DISPLAY.blit(self.image,(self.rect.x,self.rect.y))

#target class
class Target():
    #x,y,width,height,image
    def __init__(self,x,y,width,height):
        self.image = pygame.transform.scale(pygame.image.load("assets/cursor.png"),(width,height))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center = (self.x,self.y))
        self.width = width
        self.height = height
    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.rect.x = self.rect.center[0] - self.width/2
        self.rect.y = self.rect.center[1] - self.height/2
        DISPLAY.blit(self.image,(self.rect.x,self.rect.y))
        
#objects
camera_group = CameraGroup()
player = Player(camera_group)
target = Target(0,0,30,30)
enemy1 = Enemy(900,720)
enemy2 = Enemy(10,500)
enemy3 = Enemy(100,250)
enemy4 = Enemy(10,900)

def display_ui():
    for i in range(player.max_health):
        img = pygame.image.load("assets/heart_empty.png" if i >= player.health else "assets/heart.png")
        img = pygame.transform.scale(img,(50,50))
        DISPLAY.blit(img,(i*50+WINDOWSIZE[0]/2-player.max_health*25,25))

    score_text = TEXT_FONT.render(f'Score: {score}', True, (255,255,255))
    DISPLAY.blit(score_text,(score_text.get_width()/2,25))
    start_time = pygame.time.get_ticks()
    time_since_start = pygame.time.get_ticks() - start_time
    time_text = TEXT_FONT.render(f'Time: {time_since_start}',True,(255,255,255))
    DISPLAY.blit(time_text,(1100,25))

def update_screen():
    CLOCK.tick(60)
    pygame.display.update()

def shoot():
        mouse_pos = pygame.mouse.get_pos()
        angle = math.atan2((SCREEN_HEIGHT//2-mouse_pos[1]) , (SCREEN_WIDTH//2-mouse_pos[0]))
        bullet = Bullet(angle,SCREEN_WIDTH//2,SCREEN_HEIGHT//2)
        bullets.append(bullet)

#game loop
is_gameover = False
collision_tolerance = 10
pygame.mouse.set_visible(False)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot()
            
    
    DISPLAY.fill((0,0,0))
    
    camera_group.update()
    camera_group.custom_draw(player)
    target.update()
    
    for e in enemies:
        e.update()
        if e.rect.colliderect(player.rect):
            if player.rect.top-e.rect.bottom < collision_tolerance:
                enemies.remove(e)
                player.health -=1
            elif player.rect.bottom - e.rect.top < collision_tolerance:
                enemies.remove(e)
                player.health -=1
            elif player.rect.right - e.rect.left < collision_tolerance:
                enemies.remove(e)
                player.health -=1
            elif player.rect.left - e.rect.right < collision_tolerance:
                enemies.remove(e)
                player.health -=1
    
    for b in bullets:
        b.change()

    for e in enemies:
        for b in bullets:
            if b.rect.colliderect(e.rect):
                enemies.remove(e)
                score += 10

    display_ui()
    update_screen()