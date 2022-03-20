#Создай собственный Шутер!

from pygame import *
from random import randint


#создай окно игры
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Shooter')
score = 0
lost = 0
mlost = 3
goal = 15
#задай фон сцены
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
bullets = sprite.Group()
font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 20)
win = font1.render('YOU WIN!!!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!!!', True, (180, 0, 0))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()   



class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, hp):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.hp = hp
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx, self.rect.top, 5, 100, 90)
        bullets.add(bullet) 
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x> 5:
            self.rect.x-= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x< win_width-80:
            self.rect.x += self.speed
        
        

class Enemy(GameSprite):
    
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y= 0
            lost = lost + 1
        
class Asteroid(GameSprite):
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y= 0


hero = Player('rocket.png', 310, 400, 80, 100, 10, 3)
bonus = GameSprite('asteroid.png', randint(80, win_width- 80), randint(80, win_height - 80), 50, 50, 0)
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy("ufo.png", randint(80, win_width-80), -40, 80, 50, randint(3,5))
    monsters.add(monster)
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_s = mixer.Sound('fire.ogg')

asteroids = sprite.Group()
for i in range(2):
    asteroid = Asteroid('asteroid.png', randint(80, win_width - 80), - 40, 100, 60, 3)
    asteroids.add(asteroid)

game = True
clock = time.Clock()
FPS = 60
finish = False


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_s.play()
                hero.fire()
    if finish != True:
        window.blit(background,(0,0))
        
        
        
        hero.update()
        monsters.update()
        asteroids.update()
        bonus.update()

        bonus.reset()
        hero.reset()
        asteroids.draw(window)
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy("ufo.png", randint(80, win_width-80), -40, 80, 50, randint(3,5))
            monsters.add(monster)
        collides = sprite.groupcollide(monsters, bullets, False, True)
        if sprite.spritecollide(hero, monsters, True):
            hero.hp -= 1
            monster = Enemy("ufo.png", randint(80, win_width-80), -40, 80, 50, randint(3,5))
            monsters.add(monster)
        if hero.hp <= 0 or lost >= mlost:
            finish = True
            window.blit(lose,(200, 200))
        if score >= goal:
            finish = True
            window.blit(win,(200, 200))
        if sprite.spritecollide(bonus, bullets, True):
            hero.hp += 1
            bonus.rect.x = randint(80, win_width - 80)
            bonus.rect.y = randint(80, win_height - 80)
        text = font2.render("Счет:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        text_hp = font2.render("Осталось жизней:" + str(hero.hp), 1, (255,255,255))
        window.blit(text_hp,(10, 80))
               
        
        
        display.update()
        clock.tick(FPS)
    else:
        finish = False
        score = 0
        lost = 0
        hp = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy("ufo.png", randint(80, win_width-80), -40, 80, 50, randint(3,5))
            monsters.add(monster)
    time.delay(50)