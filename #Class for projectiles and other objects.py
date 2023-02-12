'''#Class for projectiles and other objects 
class Object:
    def __init__(self,x,y,width,height,image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.velocity = [0,0]
        self.collider = [width,height]

        objects.append(self)
    def draw(self):
        DISPLAY.blit(pygame.transform.scale(self.image,(self.width,self.height)),(self.x,self.y))

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.draw()

    def get_center(self):
        return self.x + self.width/2, self.y + self.height/2

#Abstract class for player and enemy 
class Living(Object):
    def __init__(self,x,y,width,height,tileset,speed):
        super().__init__(x,y,width,height,None)

        self.speed = speed
        self.tileset = load_tileset(tileset,16,16)
        self.direction = 0
        self.flipx = False
        self.frame = 0
        self.frames = [0,1,0,2]
        self.frame_timer = 0

    def change_direction(self):
        if self.velocity[0] < 0:
            self.direction = HORIZONTAL
            self.flipx = True
        elif self.velocity[0] > 0:
            self.direction = HORIZONTAL
            self.flipx = False
        elif self.velocity[1] >0:
            self.direction = DOWN
        elif self.velocity[1]<0:
            self.direction = UP

    def draw(self):
        image = pygame.transform.scale(self.tileset[self.frames[self.frame]][self.direction], (self.width,self.height))
        self.change_direction()
        image = pygame.transform.flip(image,self.flipx,False)
        DISPLAY.blit(image,(self.x,self.y))
        if self.velocity[0] == 0 and self.velocity[1] == 0:
            self.frame = 0
            return
        self.frame_timer += 1
        if self.frame_timer <10:
            return
        self.frame += 1
        if self.frame >= len(self.frames):
            self.frame = 0
        self.frame_timer = 0

    def update(self):
        self.x += self.velocity[0] * self.speed
        self.y += self.velocity[1] * self.speed
        self.draw()

#enemy class
class Enemy(Living):
    def __init__(self,x,y,width,height,tileset,speed):
        super().__init__(x,y,width,height,tileset,speed)
        self.health = 3
        #self.collider = [width/2.5,height/1.5] 
        enemies.append(self)

    def update(self):
        playerx = player.rect.x
        playery = player.rect.y
        enemy_center = self.get_center()

        self.velocity = [playerx-enemy_center[0],playery-enemy_center[1]]
        
        magnitude = (self.velocity[0]**2 + self.velocity[1]**2) ** 0.5
        self.velocity =  [self.velocity[0]/magnitude*self.speed, self.velocity[1]/magnitude*self.speed]

        super().update()

    def change_direction(self):
        super().change_direction()

        if self.velocity[1] > self.velocity[0] > 0:
            self.direction = DOWN
        elif self.velocity[1] < self.velocity[0] <0:
            self.direction = UP
    
    def take_damage(self,damage):
        self.health -= damage
        if self.health <= 0:
            global score
            score += 10
            self.destroy()

    def destroy(self):
        objects.remove(self)
        enemies.remove(self)



is_game_over = False

def load_tileset(file,width,height):
    image = pygame.image.load(file).convert_alpha()
    image_width, image_height = image.get_size()
    tileset = []
    for tile_x in range(0,image_width//width):
        line = []
        tileset.append(line)
        for tile_y in range(0,image_height//height):
            rect = (tile_x * width, tile_y * height, width, height)
            line.append(image.subsurface(rect))
    return tileset

    
    mousePos = pygame.mouse.get_pos() #tuple for position of cursor 
    target.x = mousePos[0] - target.width/2
    target.y = mousePos[1] - target.height/2

    #player movement
    player.velocity[0] = player_input["right"] - player_input["left"]
    player.velocity[1] = player_input["down"] - player_input["up"]

    for e in enemies:
        if check_collisions(player,e):
            player.health -= 1
            e.destroy()
            continue
        for b in bullets:
            if check_collisions(b,e):
                e.take_damage(1)
                bullets.remove(b)
                objects.remove(b)

    if is_game_over:
        update_screen()
        continue

    if player.health <= 0:
        if not is_game_over:
            is_game_over = True

    for obj in objects:
        obj.update()'''

    