import pygame
import math
import random

from pygame import mixer

#initialize pygame
pygame.init()
pygame.font.init()

#Create the screen
screen = pygame.display.set_mode((800,600))

# Background image
background = pygame.image.load('background1.png')

#Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#Title and Logo
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numOfEnemys = 6

for i in range(numOfEnemys):
    enemyImg.append(pygame.image.load('ufo2.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(30,100))
    enemyX_change.append(4)
    enemyY_change.append(40)

#bullet
#ready - can't see bullet
#fire - bullet is moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bulletState = "ready"

#score
scoreValue = 0
font = pygame.font.SysFont('freesansbold.ttf', 32)
textX = 10
textY = 10

#Game over text
overFont = pygame.font.SysFont('freesansbold.ttf', 64)

def showScore(x,y):
    score = font.render('Score: ' + str(scoreValue), True, (255,255,255))
    screen.blit(score, (x, y))

def gameOverText():
    gameOver = overFont.render('Game Over', True, (255,255,255))
    screen.blit(gameOver, (200,250))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

#Game loop
running = True
while running:
    #RGB screen color
    screen.fill((0,150,0))
    #Background image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #If
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5

            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bulletState is "ready":
                    #Bullet sound
                    bulletSound = mixer.Sound('laser.wav')
                    bulletSound.play()
                    #fire bullet
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0.0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736

    for i in range(numOfEnemys):

        #Game over
        if enemyY[i] > 440:
            for j in range(numOfEnemys):
                enemyY[j] = 2000
            gameOverText()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)

        if collision:
            #collision sound
            # Bullet sound
            collisionSound = mixer.Sound('explosion.wav')
            collisionSound.play()
            bulletY = 480
            bulletState = "ready"
            scoreValue += 1
            print(scoreValue)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(30, 100)

        enemy(enemyX[i], enemyY[i], i)

    #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bulletState = "ready"
    if bulletState is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    player(playerX,playerY)
    showScore(textX,textY)
    pygame.display.update()

