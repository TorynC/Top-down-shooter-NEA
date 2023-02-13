import pygame,sys
#pygame setup
pygame.init()
pygame.font.get_init()

TEXT_FONT = pygame.font.Font("assets/font.otf", 32)

WINDOWSIZE = (1280,720)

DISPLAY = pygame.display.set_mode(WINDOWSIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("Top Down Shooter")
MAPBOUND_X = 1800
MAPBOUND_Y = 1200

score = 0 
class CameraGroup(pygame.sprite.Group):
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
            self.display_surface.blit(sprite.image,offset_pos)

#player class
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)
        self.health = self.max_health = 3 #double assignment
        self.image = pygame.transform.scale(pygame.image.load("assets/test.png").convert_alpha(),(40,40))
        self.rect = self.image.get_rect(center = pos)
        self.speed = 5
        self.direction = pygame.math.Vector2()

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

        self.rect.x += self.direction.x * speed
        self.rect.y += self.direction.y * speed
        self.rect.center = self.rect.center
        if self.rect.right >= MAPBOUND_X:  
            self.rect.right = MAPBOUND_X
        if self.rect.left <=0:
            self.rect.x = 0
        if self.rect.bottom >= MAPBOUND_Y:  
            self.rect.bottom = MAPBOUND_Y
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
        self.rect = self.image.get_rect(center =self.rect.center )

    def update(self):
        self.input()
        self.get_status()
        self.animate()
        
        self.move(self.speed)

#objects
camera_group = CameraGroup()
player = Player((600,400),camera_group)

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
    clock.tick(60)
    pygame.display.update()


#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    DISPLAY.fill((0,0,0))
    
    camera_group.update()
    camera_group.custom_draw(player)

    display_ui()
    update_screen()
