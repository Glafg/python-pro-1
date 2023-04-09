from pygame import*

display.set_caption('Игра')
window = display.set_mode((700,500))
win_width=700
background = transform.scale(image.load('fon.png'), (700, 500))
final = transform.scale(image.load('win.jpg'), (700, 500))
lose = transform.scale(image.load('over.jpg'), (700, 500))

print(type(final))
class GameSprite(sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture),(w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, picture, w, h, x, y, x_speed, y_speed):
        super().__init__(picture, w, h, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self,barriers,False)
        if self.x_speed>0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right,p.rect.left)
        elif self.x_speed<0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left,p.rect.right)
        self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self,barriers,False)
        if self.y_speed>0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom,p.rect.top)
        elif self.y_speed<0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top,p.rect.bottom)

    def fire(self):
        bullet = Bullet('bullet.png',20,4,self.rect.right,self.rect.centery,15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, picture, w, h, x, y, speed):
        super().__init__(picture, w, h, x, y) 
        self.speed = speed

    def update(self):
        if self.rect.x<=470:
            self.direction='right'
        if self.rect.x>=win_width-85:
            self.direction='left'
        if self.direction=='left':
            self.rect.x-=self.speed
        else:
            self.rect.x+=self.speed

class Bullet(GameSprite):
    def __init__(self,minion_image,minion_x,minion_y,size_x,sixe_y,minion_speed):
        GameSprite.__init__(self,minion_image,minion_x,minion_y,size_x,sixe_y)
        self.speed = minion_speed
    def update(self):
        self.rect.x+=self.speed
        if self.rect.x>win_width+10:
            self.kill()
        

minion = Player('minion.jpg', 57, 37, 100, 400, 0, 0)
ggg = GameSprite('ggg.jpg', 219, 39, 170, 150)
ggg1 = GameSprite('ams.jpg', 39, 219, 380, 150)
final = GameSprite("final.png", 80, 80, 450, 150)
monster=Enemy('enemy.png',50,50,300,300,15)
barriers = sprite.Group()
barriers.add(ggg)
barriers.add(ggg1)
bullets = sprite.Group()
enemys=sprite.Group()
enemys.add(monster)

win = False
run = True

while run:
    time.delay(50)
    
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                minion.x_speed = -7
            elif e.key == K_RIGHT:
                minion.x_speed = 7
            elif e.key == K_UP:
                minion.y_speed = -7
            elif e.key == K_DOWN:
                minion.y_speed = 7
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                minion.x_speed = 0
            elif e.key == K_RIGHT:
                minion.x_speed = 0
            elif e.key == K_UP:
                minion.y_speed = 0
            elif e.key == K_DOWN:
                minion.y_speed = 0
            elif e.key == K_SPACE:
                minion.fire()
    if sprite.collide_rect(minion, final):
        win=True
        window.blit(final, (0, 0))
    
    if win != True:
        window.blit(background, (0, 0))
        enemys.update()
        enemys.draw(window)
        final.reset()
        minion.reset()
        minion.update()
        barriers.draw(window)
        bullets.update()
        bullets.draw(window)

        sprite.groupcollide(bullets,barriers,True,False)
        sprite.groupcollide(bullets,enemys,True,True)

        if sprite.spritecollide(minion, enemys,False):
            final=True
            img= image.load('over.jpg')
            window.blit(img, (0, 0))
        if sprite.collide_rect(minion, final):
            win=True
            window.blit(win, (0, 0))
        #beliy_2.reset()
        #beliy_3.reset()
        #kras.reset()
        
    display.update()