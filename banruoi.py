from cProfile import run
from errno import ENOTEMPTY
import random
from tkinter import CENTER
import pygame


WIDTH = 800
HEIGHT= 600
pygame.display.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
backgroungimg = pygame.image.load("img/background.png")
screen.blit(backgroungimg,(0,0))
clock = pygame.time.Clock()
#sprite player
playerimg = pygame.image.load("img/player.png")
playerimg = pygame.transform.scale(playerimg,(64,64))
player = pygame.sprite.Sprite()
player.image = playerimg
player.rect = player.image.get_rect(center=(400,500))
playerChangeX = 0

#enemy sprite
class Enemy(pygame.sprite.Sprite):
    enemySpeed = 5
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        enemyimg = pygame.image.load("img/e1.png")
        self.image = enemyimg
        self.rect = self.image.get_rect(center=(x,y))
        self.move = 20
        self.timeBomb = pygame.time.get_ticks()
    def update(self): 
        now = pygame.time.get_ticks()
        if (now - self.timeBomb > random.randint(2000,15000)):
            self.timeBomb = now
            b = Bomb(self.rect.center)
            Bombs.add(b)
            all_sprites.add(b)
        self.move = self.move - 1
        if (self.move < -20):
            self.move = 20
        if (self.move < 0) & (self.rect.x - self.enemySpeed >0):
            self.rect.x -= self.enemySpeed
        elif (self.move > 0) & (self.rect.x + self.enemySpeed < WIDTH):
            self.rect.x += self.enemySpeed

class Bomb(pygame.sprite.Sprite):
    def __init__(self,poscenter):
        pygame.sprite.Sprite.__init__(self)
        bombimg = pygame.image.load("img/enemyBomb.png")
        bombimg = pygame.transform.scale(bombimg,(23,23))
        self.image = bombimg
        self.rect = self.image.get_rect(center=poscenter)
    
    def update(self):
        self.rect.y = self.rect.y + 5
        if (self.rect.y > (HEIGHT + 100)):
            self.kill()
#bullet sprite
class Bullet(pygame.sprite.Sprite):
    bulletSpeed = -5
    def __init__(self,x,y) :
        pygame.sprite.Sprite.__init__(self)
        bulletimg = pygame.image.load("img/bullet.png")
        bulletimg = pygame.transform.scale(bulletimg,(9,27))
        self.image = bulletimg
        self.rect = self.image.get_rect(center=(x,y))
        bulletStatus = "ready"
    def update(self):
        self.rect.y = self.rect.y + self.bulletSpeed 
        if (self.rect.y < -100):
            self.kill()
class Explosion(pygame.sprite.Sprite):
    def __init__(self, poscenter):
        pygame.sprite.Sprite.__init__(self)
        Explosionimg = pygame.image.load("img/explosion/Exp1.png")
        self.image = Explosionimg
        self.rect = self.image.get_rect(center=poscenter)
        self.lastupdate = pygame.time.get_ticks()
        self.indeximg = 1
    def update(self):
        now = pygame.time.get_ticks()
        if (now - self.lastupdate > 60):
            self.indeximg += 1
            if (self.indeximg <= 8):
                imgname = "img/explosion/Exp" + str(self.indeximg) + ".png" 
                Explosionimg = pygame.image.load(imgname) 
                self.image = Explosionimg               
                self.lastupdate = pygame.time.get_ticks()
            else:
                self.kill()    
Bombs = pygame.sprite.Group()            
Enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group([player])
bullets = pygame.sprite.Group()
max_enemy = 6
for i in range(max_enemy):
    enemy = Enemy(100+ WIDTH/(max_enemy+1) * i,100 )
    Enemies.add(enemy)
    all_sprites.add(enemy)
running = True
while running == True:
    clock.tick(60)
    screen.fill((0,0,0))
    screen.blit(backgroungimg,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerChangeX = 5
            if event.key == pygame.K_LEFT:
                playerChangeX = -5   
            if event.key == pygame.K_SPACE:
                b = Bullet(player.rect.x + 25, player.rect.y - 20)
                bullets.add(b)
                all_sprites.add(b)
    for hit in pygame.sprite.groupcollide(Enemies,bullets,1,1).keys():
        e = Explosion(hit.rect.center)     
        all_sprites.add(e)
    if pygame.sprite.spritecollide(player,Bombs,1):
        backgroungimg = pygame.image.load("img/gameover.png")
        backgroungimg = pygame.transform.scale(backgroungimg,(WIDTH,HEIGHT))
        all_sprites.empty()
    all_sprites.update()
    if (player.rect.x + playerChangeX > 0) & (player.rect.x + playerChangeX + player.rect.width < WIDTH):
        player.rect.x = player.rect.x + playerChangeX
    all_sprites.draw(screen)
    pygame.display.update()