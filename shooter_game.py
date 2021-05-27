from pygame import *
from random import *
from time  import time as timer



#фоновая музыка
'''mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')'''

font.init()
font1 = font.Font(None, 80)
win = font1.render('You Win! 0_0', True, (255, 255, 255))
lose = font1.render('You Lose!', True, (180, 0, 0))


font2 = font.Font(None, 36)

#нам нужны такие картинки:
img_back = "galaxy.jpg" #фон игры
img_hero = "rocket.png" #герой
img_enemy = "ufo.png"  
img_bullet = 'bullet.png'


score = 0
goal = 10
lost = 0
max_lost = 3



#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Вызываем конструктор класса (Sprite):
       sprite.Sprite.__init__(self)
 
       #каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       
       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #метод, отрисовывающий героя на окне
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
 
#класс главного игрока
class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
    def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

 #метод "выстрел" (используем место игрока, чтобы создать там пулю)
 
#Создаем окошко
win_width = 750
win_height = 550
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
#создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 15)


monsters = sprite.Group()
for i in range(6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint (1, 5))
    monsters.add(monster)

'''asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)'''

bullets = sprite.Group

bullets = sprite.Group()
#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False

rel_time = False

num_fire = 0
#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                    
                    if num_fire < 10 and rel_time == False:
                        num_fire = num_fire + 1
                        #fire_sound.play()
                        ship.fire()
                        
                    if num_fire >= 10 and rel_time == False:
                        last_time = timer()
                        rel_time = True
#fire_sound.play()
                
    #событие нажатия на кнопку Закрыть

        

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 10
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint (1, 5))
            monsters.add(monster)
            
    if lost >= max_lost:
        finish = True
        window.blit(lose, (200, 200))           

        
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200,200))                            
    
    if not finish:
        #обновляем фон
        window.blit(background,(0,0))
 
        text = font2.render('Очков:' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Подождите, перезарядка...', 1, (150, 0 , 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False
        
   
        #производим движения спрайтов
    

        ship.update()
        bullets.update()
        monsters.update() 
        '''asteroids.update()'''
        #обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        bullets.draw(window) 
        '''asteroid.draw(window)'''
    display.update()
    #цикл срабатывает каждые 0.05 секунд
    time.delay(50)
