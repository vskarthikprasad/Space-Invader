import pygame
import os
import time
import random
import math

pygame.init()
pygame.display.set_caption('Space Invader')
display_width=800
display_height=600
display=pygame.display.set_mode((display_width,display_height))
collision_sound = pygame.mixer.Sound(r"C:\Stud\Python\Pygame\Space_invader\assets\sounds\shipexplosion.wav") 
bullet_sound = pygame.mixer.Sound(r"C:\Stud\Python\Pygame\Space_invader\assets\sounds\shoot.wav") 
vel=12
score=0
dodged=0
black = (0,0,0)
white = (255,255,255)
pause = False
red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)

current_path = os.path.dirname(__file__) # Where your .py file is located
resource_path = os.path.join(current_path, 'assets') # The resource folder path
image_path = os.path.join(resource_path, 'images')
background_img = pygame.image.load(os.path.join(image_path, 'background.jpg'))
ship_img=pygame.image.load(os.path.join(image_path, 'ship.png')) # 50 * 48
bullet_img=pygame.image.load(os.path.join(image_path, 'bullet.png'))
enemybullet_img=pygame.image.load(os.path.join(image_path, 'enemybullet.png'))
font=pygame.font.SysFont("comicsans",30)



enemyvel=[]
enemyImg=[]
enemy_limit=5
enemyy=[]
enemyx=[] 
ship_width=50
ship_height=48
x=400
y=500
bulletx=x
bullety=y
bulletvel=10
bullet_state="ready"
run=True
FPS=60
enemy_collided=0
clock=pygame.time.Clock()
instructions='left/right - to move. space- bullets'



for i in range(enemy_limit):
    enemyImg.append(pygame.image.load(os.path.join(image_path,  random.choice(['enemy1.png','enemy2.png','enemy3.png']))))
    enemyx.append(random.randrange(ship_width, display_width-ship_width))
    enemyy.append(random.randrange(-500,-200))
    enemyvel.append(random.randrange(0,4))




def ship(i,j):
    display.blit(ship_img, (i,j))

def back():
    display.blit(background_img, (0,0))

def firebullet(i,j,img):

    global bullet_state
    bullet_state="fired"
    display.blit(img,(i+25,j+24))



def enemy(i,j,x):
    display.blit(enemyImg[x],(i,j))


def collision(enemyx,enemyy,bulletx,bullety):
    distance=math.sqrt((math.pow((enemyx-bulletx),2))+(math.pow((enemyy-bullety),2)))
    return (distance < 50)

def disp_dodge(x):
    display.blit(x,(display_width-120,10))

def disp_score(x):
    display.blit(x,(10,10))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(display, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(display, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    display.blit(textSurf, textRect)
    

def draw():
    back()
    ship(x,y)
    pygame.display.update()


def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False

def quitgame():
    pygame.quit()
    quit()

while run:
    clock.tick(FPS)
    draw()
    dodged_label=font.render(f"Dodged: {dodged}",1,(255,255,255))
    score_label=font.render(f"Score: {score}",1,(255,255,255))
    life_label=font.render(f"Health: -{enemy_collided}",1,(255,255,255))
  
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run = False
    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x>0:
        x-=vel
    if keys[pygame.K_RIGHT] and x < display_width-ship_width-2:
        x+=vel

    if keys[pygame.K_p]:
    	pause=True
    	while pause:
    		for event in pygame.event.get():
    			if event.type == pygame.QUIT:
    				pygame.quit()
    				quit()
    		button(instructions,30,150,500,100,white,white,None)
    		button('continue',150,450,100,50,green,bright_green,unpause)
    		button('quit',550,450,100,50,red,bright_red,quitgame)
	    	pygame.display.update()
    if keys[pygame.K_SPACE]:
        pygame.mixer.Sound.play(bullet_sound)
        pygame.mixer.music.stop()
        if bullet_state is "ready":
            bulletx=x
            firebullet(bulletx,bullety,bullet_img)

    if bullety <=0 :
        bullety=y
        bullet_state='ready'

    if bullet_state is "fired":

        firebullet(bulletx,bullety,bullet_img)
        bullety-=bulletvel


    for i in range(enemy_limit):
        enemy(enemyx[i],enemyy[i],i)
        enemyy[i]+=enemyvel[i]



        disp_dodge(dodged_label)
        if enemyy[i] > display_height:
            dodged+=1
            enemyy[i]=-ship_height*2
            enemyx[i]=random.randrange(ship_width,display_width-ship_width)



        col=collision(enemyx[i],enemyy[i],bulletx,bullety)
        if col:
            pygame.mixer.Sound.play(collision_sound)
            pygame.mixer.music.stop()
            bullety=y
            bullet_state="ready"
            score+=1
            disp_score(score_label)
            enemyx[i] = random.randrange(0+ship_width, display_width-ship_width)
            enemyy[i] = random.randrange(-500,50)

    display.blit(score_label,(10,10))
   
    pygame.display.update()

pygame.quit()

