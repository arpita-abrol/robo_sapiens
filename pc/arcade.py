import pygame, sys, os, time, random, csv, itertools
from pygame.locals import *

#GLOBAL VARS

FPS = 200
WIDTH = 400
HEIGHT = 300

##Game #1- PONG
THICK = 10
PADDLESIZE = 50
PADDLEOFF = 20

##Colors
BLACK = (0,0,0)
WHITE = (255,255,255)

GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
PINK = (255,0,255)
ORANGE = (255,178,102)
BROWN = (156,76,0)
PURPLE = (153,0,153)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~BEGIN HOME~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def displayList():
    #game #1- Pong
    game1 = pygame.Rect(50,50,300,60)
    pygame.draw.rect(DISPLAYSURF, WHITE, game1)

    gameName = FONT_A.render('PONG', True, BLACK)
    gameRes = gameName.get_rect()
    gameRes.topleft = (60,70)
    DISPLAYSURF.blit(gameName, gameRes)

    #game #2- Flappy Bird
    game2 = pygame.Rect(50,150,300,60)
    pygame.draw.rect(DISPLAYSURF, WHITE, game2)

    gameName2 = FONT_A.render('FLAPPY BIRD', True, BLACK)
    gameRes2 = gameName2.get_rect()
    gameRes2.topleft = (60,170)
    DISPLAYSURF.blit(gameName2, gameRes2)

def checkList(mousex, mousey):
    #game #1- Pong
    if mousex > 50 and mousex < 350 and mousey > 50 and mousey < 110:
        mainPong()
        
    if mousex > 50 and mousex < 350 and mousey > 150 and mousey < 210:
        mainBird()

def main():
    pygame.init()
    global DISPLAYSURF

    global FONT_A, FONT_A_SIZE
    FONT_A_SIZE = 20
    FONT_A = pygame.font.Font('freesansbold.ttf',FONT_A_SIZE)

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('ArcadeMe Home')

    while True: #game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = pygame.mouse.get_pos()
                checkList(mousex, mousey)
                #mainPong()

        DISPLAYSURF.fill(BLACK)
        displayList()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~BEGIN PONG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#sets up the game background
def setup():
    #BACKGROUND SETUP
    DISPLAYSURF.fill(BLACK)
    pygame.draw.rect(DISPLAYSURF,WHITE,((0,0),(WIDTH,HEIGHT)),THICK*2)
    pygame.draw.line(DISPLAYSURF,WHITE,((WIDTH/2),0),((WIDTH/2),HEIGHT),THICK/4)
 
#draws the paddles and ensure they stay within game limits
def drawPaddle(paddle):
    if paddle.bottom > HEIGHT - THICK:
        paddle.bottom = HEIGHT - THICK
    elif paddle.top < THICK:
        paddle.top = THICK
    pygame.draw.rect(DISPLAYSURF,WHITE,paddle)
 
#draws the ball
def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF,WHITE,ball)
 
#moves the ball
def moveBall(ball,Xdir,Ydir):
    ball.x += Xdir
    ball.y += Ydir
    return ball
 
#checks if the ball collides with top, bottom, paddles
def checkEdges(ball, Xdir, Ydir, score, topScore,FPS):
    if ball.top <= THICK or ball.bottom >= HEIGHT-THICK:
        Ydir *= -1
    if ball.left <= THICK or ball.right >= WIDTH-THICK:
        FPS = 100
        if ball.right >= WIDTH-THICK-2:
            score += 10
        else:
            score = 0
        if Xdir < 0:
            Xdir = 1
        else:
            Xdir = -1
        ball.y = HEIGHT/2
        ball.x = WIDTH/2 + 20*Xdir*-1
        if score > topScore:
            topScore = score
        score = 0
    return ball, Xdir, Ydir, score, topScore, FPS
 
#moves the opponent's paddle
def AI(ball, Xdir, paddle):
    if Xdir < 0 and random.random() >= .5:
        if paddle.centery < HEIGHT/2:
            paddle.y += 1
        elif paddle.centery > HEIGHT/2:
            paddle.y += -1
    elif Xdir > 0:
        if paddle.centery < ball.centery:
            paddle.y += 1
        elif paddle.centery > ball.centery:
            paddle.y += -1
    return paddle
 
#checks if paddle hits ball
def checkPaddles(ball,paddleOne,paddleTwo,Xdir, FPS):
    if Xdir < 0 and paddleOne.right == ball.left and paddleOne.top-7 <= ball.bottom and paddleOne.bottom+7 >= ball.top:
        FPS += 5
        return Xdir * -1, FPS
    elif Xdir > 0 and paddleTwo.left == ball.right and paddleTwo.top-7 <= ball.bottom and paddleTwo.bottom+7 >= ball.top:
        FPS += 5
        return Xdir * -1, FPS
    else:
        return Xdir, FPS
 
#checks if score increased or now zero
def checkScore(paddle,ball,score,Xdir):
    if Xdir < 0 and paddle.right == ball.left and paddle.top-7 <= ball.bottom and paddle.bottom+7 >= ball.top:
        return score + 1
    elif ball.right >= WIDTH-THICK:
        return score + 10
    return score
 
#displays current score
def displayScore(score):
    res = FONT.render('Score = %s' %(score),True,WHITE)
    resRect = res.get_rect()
    resRect.topleft = (WIDTH - 150, 25)
    DISPLAYSURF.blit(res,resRect)
 

 
#leaderboard function (endgame); main 2.0
def scoreboard(score):
    with open('highscores.csv','rb') as file:
        words = csv.reader(file)
        score_list = list(words)
        lnOne = score_list[0][0].split('.')
         
    pos,newHigh = compareScores(score,lnOne)
    if( newHigh ):
        name = getName()
        replaceScores(name,pos,score)
    else:
        finalScreen()
 
#Compares the player score to all high scores
def compareScores(newScore,listScores):
    x = 0
    while x < len(listScores):
        if int(newScore) >= int(listScores[x]):
            return x, True
        x += 1
    return -1, False
 
#get player name
def getName():
    pygame.time.wait(500)
    DISPLAYSURF.fill(BLACK)
    name = ""
    alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    
    check = True
    x1 = 0
    while check:
        displayBoard('WHAT IS YOUR FIRST INITIAL?',2)
        displayName(alphabet[x1],50)
        for action in pygame.event.get():
            if action.type == KEYDOWN:
                if action.key == K_w:
                    x1 += 1
                    if x1 >= 26:
                        x1 = 0
                elif action.key == K_s:
                    x1 -= 1
                    if x1 >= 26:
                        x1 = 25
                elif action.key == K_RETURN:
                    name += alphabet[x1]
                    check = False
        pygame.display.update()
        pygame.time.wait(200)
        DISPLAYSURF.fill(BLACK)
 
    pygame.time.wait(300)
     
    check = True
    x1 = 0
    while check:
        displayBoard('WHAT IS YOUR LAST INITIAL?',2)
        displayName(alphabet[x1],50)
        for action in pygame.event.get():
            if action.type == KEYDOWN:
                if action.key == K_w:
                    x1 += 1
                    if x1 >= 26:
                        x1 = 0
                elif action.key == K_s:
                    x1 -= 1
                    if x1 >= 26:
                        x1 = 25
                elif action.key == K_RETURN:
                    name += alphabet[x1]
                    check = False
        pygame.display.update()
        pygame.time.wait(200)
        DISPLAYSURF.fill(BLACK)
         
    return name
 
#displays name choosing stuff
def displayName(words,pos):
    res = FONT2.render('%s' %words,True,WHITE)
    resRect = res.get_rect()
    resRect.topleft = (25,pos)
    DISPLAYSURF.blit(res,resRect)
 
#replaces the old high score
def replaceScores(name,pos,score):
    #print name,pos,score
    #name -> new name
    #pos -> new pos
    #score -> new score
 
    score_list = []
     
    with open('highscores.csv','rb') as file:
        words = csv.reader(file)
        score_list = list(words)
         
    with open('highscores.csv','wb') as file:
        lnOne = score_list[0][0].split('.')
        ctr = 9
        while ctr > pos:
            lnOne[ctr] = lnOne[ctr-1]
            ctr -= 1
        lnOne[pos] = str(score)
        string = ""
        for x in lnOne:
            string += x
            string += "."
        file.write(string[0:-1] + '\n')
        ctr = 1
        while ctr < pos+2:
            file.write(score_list[ctr][0])
            file.write('\n')
            ctr += 1
        if pos < 9:
            string = "0" + str(pos+1) + "." + "            " + name + "            " + str(score) + "\n"
            file.write(string)
            ctr = pos+2
            while ctr < 10:
                string = score_list[ctr][0]
                num = int(string[:2]) + 1
                string = "0" + str(num) + string[2:]
                file.write(string)
                file.write('\n')
                ctr += 1
            string = score_list[10][0]
            string = "10" + string[2:]
            file.write(string)
        else:
            string = "10." + "            " + name + "            " + str(score) + "\n"
            file.write(string)
    finalScreen()
 
def finalScreen():
    DISPLAYSURF.fill(BLACK)
    ctr = 1
    with open('highscores.csv','rb') as file:
        words = csv.reader(file)
        score_list = list(words)
        for x in score_list:
            displayBoard(x[0],ctr)
            ctr += 1
        lnOne = score_list[0][0].split('.')
     
    pygame.display.update()
    pygame.time.wait(10000)
    
 
def displayBoard(words,pos):
    #print words
    res = FONT2.render('%s' %words,True,WHITE)
    resRect = res.get_rect()
    resRect.topleft = (25,pos*20-37)
    DISPLAYSURF.blit(res,resRect)
 
 
 
 
def mainPong():
    #basic setup stuff
    global FPS
    FPS = 100
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    global DISPLAYSURF
    DISPLAYSURF = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('Pong')
 
    #font info
    global FONT, FONT2
    FONT = pygame.font.Font('freesansbold.ttf',20)
    FONT2 = pygame.font.Font('incon.ttf',15)
 
    #setup starting pos
    ballX = (WIDTH - THICK)/2
    ballY = (HEIGHT - THICK)/2
    playerOnePos = (HEIGHT - PADDLESIZE)/2
    playerTwoPos = (HEIGHT - PADDLESIZE)/2
 
    #setup paddles, ball
    paddleOne = pygame.Rect(PADDLEOFF,playerOnePos,THICK,PADDLESIZE)
    paddleTwo = pygame.Rect(WIDTH-PADDLEOFF-THICK,playerTwoPos,THICK,PADDLESIZE)
    ball = pygame.Rect(ballX, ballY, THICK, THICK)
 
    #place paddles, ball initially
    setup()                 #draws background
    drawPaddle(paddleOne)   #draws user's paddle
    drawPaddle(paddleTwo)   #draws AI's paddle
    drawBall(ball)          #draws ball
 
    #ball directions:
    ##X-axis: -1 = left, 1 = right
    ##Y-axis: -1 = up, 1 = down
    ballDirX = -1
    ballDirY = -1
         
    score = 0
    topScore = 0
    while True:     #PONG game loop
        for action in pygame.event.get():
            if action.type == KEYDOWN:
                if action.key == K_ESCAPE:
                    if topScore > score:
                        scoreboard(topScore)
                    else:
                        scoreboard(score)
                    return
            elif action.type == MOUSEMOTION:
                mousex, mousey = action.pos
                paddleOne.y = mousey
             
        #place paddles, ball- updating version
        setup()                 #draws background
        drawPaddle(paddleOne)   #draws user's paddle
        drawPaddle(paddleTwo)   #draws AI's paddle
        drawBall(ball)          #draws ball
 
        ball = moveBall(ball,ballDirX,ballDirY)
        ball, ballDirX, ballDirY, score, topScore, FPS = checkEdges(ball,ballDirX,ballDirY,score,topScore,FPS)
        score = checkScore(paddleOne,ball,score,ballDirX)
        ballDirX,FPS = checkPaddles(ball,paddleOne,paddleTwo,ballDirX,FPS)
        paddle2 = AI(ball,ballDirX,paddleTwo)
        displayScore(score)
                     
        pygame.display.update()
        FPSCLOCK.tick(FPS)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~END CODE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#random color picker for the bird
def chooseColor():
    rnd = random.randint(0,5)
    if rnd == 0:
        return RED
    elif rnd == 1:
        return YELLOW
    elif rnd == 2:
        return PINK
    elif rnd == 3:
        return ORANGE
    elif rnd == 4:
        return BROWN
    else:
        return PURPLE

#draws the bird (body, eye, pupil)
def drawBird(bird,color):
    if bird.centery < 20:
        bird.centery = 20
    elif bird.centery > 280:
        bird.centery = 280
    pygame.draw.ellipse(DISPLAYSURF,color,bird,0)
    pygame.draw.ellipse(DISPLAYSURF,WHITE,(bird.centerx+1, bird.centery-7,12,9),0)
    pygame.draw.ellipse(DISPLAYSURF,BLACK,(bird.centerx+8, bird.centery-7,4,4),0)
    return bird

#draws the towers
def drawTower(tower):
    pygame.draw.rect(DISPLAYSURF,GREEN,tower,0)                                                         #bottom
    pygame.draw.rect(DISPLAYSURF,GREEN, (tower.left,0,tower.width,HEIGHT-tower.height-50) ,0)           #top
    pygame.draw.rect(DISPLAYSURF,GREEN, (tower.left-8,tower.top,tower.width+16,20) ,0)                  #bottom cross
    pygame.draw.rect(DISPLAYSURF,GREEN, (tower.left-8,HEIGHT-tower.height-50-20,tower.width+16,20) ,0)  #top cross

#manages tower existence and movement
def manageTower(tower,here,mark):
    if not here:
        if 0 == random.randint(0,249):
            here = True
            mark = True
            tower.centerx = random.randint(400,600)
            tower.height = random.randint(30,220)
            tower.bottom = 300
    elif tower.right <= 0:
        here = False
    else:
        tower.centerx -= 2
    return tower,here,mark

#makes sure towers are not too close
def checkTowers(towerA,towerB):
    if abs(towerA.centerx - towerB.centerx) <= 100 and towerA.right > 0 and towerB.right > 0:
        if towerA.centerx > towerB.centerx:
            towerA.centerx += 100
        else:
            towerB.centerx += 100
    return towerA,towerB

#checks to see if the bird collided with the tower
def checkCollide(bird,towerA,A_here,towerB,B_here):
    if A_here:
        if bird.right-3 > towerA.left and bird.left+3 < towerA.right and (bird.top+3 < HEIGHT-towerA.height-50 or bird.bottom-3 > towerA.top):
            #print bird.top, bird.bottom, 'towerA'
            return True
        elif bird.right-3 > towerA.left-8 and bird.left+3 <= towerA.right+8 and ((bird.bottom-3 > towerA.top and bird.top+3 < towerA.height-20) or (bird.bottom-3 > HEIGHT-towerA.top-70 and bird.top+3 < HEIGHT-towerA.height-50)):
            #print bird.top, bird.bottom, 'towerA', 'ex'
            return True
    if B_here:
        if bird.right-3 > towerB.left and bird.left+3 < towerB.right and (bird.top+3 < HEIGHT-towerB.height-50 or bird.bottom-3 > towerB.top):
            #print bird.top, bird.bottom
            return True
        elif bird.right-3 > towerB.left-8 and bird.left+3 < towerB.right+8 and ((bird.bottom-3 > towerB.top and bird.top+3 < towerB.height-20) or (bird.bottom-3 > HEIGHT-towerB.top-70 and bird.top+3 < HEIGHT-towerB.height-50)):
            #print bird.top, bird.bottom, 'ex'
            return True
    else:
        return False

#displays current score
def showScore(score):
    res = FONT.render('Score = %s' %(score),True,WHITE)
    resRect = res.get_rect()
    resRect.topleft = (WIDTH - 150, 25)
    DISPLAYSURF.blit(res,resRect)

def restartFB(towerA,A_here,towerB,B_here):
    towerA.x = 410
    towerB.x = random.randint(540,700)
    return towerA,True,True,towerB,True,True

def checkMark(mark,tower,bird,score):
    if tower.right < bird.left:
        return score+1,False
    else:
        return score,mark

#main function to run flappy bird
def mainBird():
    pygame.init()
    global DISPLAYSURF

    global FONT, FONT2,FONT_SIZE
    FONT_SIZE = 20
    FONT = pygame.font.Font('freesansbold.ttf',FONT_SIZE)
    FONT2 = pygame.font.Font('incon.ttf',15)

    FPS = 90
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('Flappy Bird')

    color = chooseColor()
    
    bird = pygame.Rect(50,150,17,17)
    drawBird(bird,color)

    towerA = pygame.Rect(250,170,25,130)
    towerB = pygame.Rect(150,170,25,130)
    towerC = pygame.Rect(450,170,25,130)        #TO BE ADDED

    ctr = 0
    score = 0
    scoreHigh = 0
    A_here = True
    B_here = True
    A_mark = True
    B_mark = True

    while True: #game loop
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if scoreHigh > score:
                        scoreboardB(scoreHigh)
                    else:
                        scoreboardB(score)
                    return
            elif event.type == MOUSEBUTTONDOWN:
                ctr += 5
            '''elif event.type == MOUSEMOTION:     #TEMP---- FOR DEV CHECK
                mousex, mousey = event.pos      #TEMPPPPPPPPPPPPPPPPPPP
                bird.y = mousey                 #TEMPPPPPPPPPPPPPPPPPPP'''

        DISPLAYSURF.fill(BLACK)

        #draw objects
        bird = drawBird(bird,color)
        if A_here:
            drawTower(towerA)
            if A_mark:
                score,A_mark = checkMark(A_mark,towerA,bird,score)
        if B_here:
            drawTower(towerB)
            if B_mark:
                score,B_mark = checkMark(B_mark,towerB,bird,score)
        showScore(score)

        #manage object movement and existence
        bird.centery += 1.2       #TEMP.... CHANGE TO 1.2
        if ctr > 0:
            tmp = int(ctr/5)+1
            bird.centery -= tmp * 8
            ctr -= tmp
        towerA,A_here,A_mark = manageTower(towerA,A_here,A_mark)
        towerB,B_here,B_mark = manageTower(towerB,B_here,B_mark)
        towerA,towerB = checkTowers(towerA,towerB)

        if checkCollide(bird,towerA,A_here,towerB,B_here):
            if score > scoreHigh:
                scoreHigh = score
            score = 0
            towerA,A_here,A_mark,towerB,B_here,B_mark = restartFB(towerA,A_here,towerB,B_here)

        pygame.display.update()
        FPSCLOCK.tick(FPS)



#leaderboard function (endgame); main 2.0
def scoreboardB(score):
    with open('highscores2.csv','rb') as file:
        words = csv.reader(file)
        score_list = list(words)
        lnOne = score_list[0][0].split('.')
         
    pos,newHigh = compareScoresB(score,lnOne)
    if( newHigh ):
        name = getNameB()
        replaceScoresB(name,pos,score)
    else:
        finalScreenB()
 
#Compares the player score to all high scores
def compareScoresB(newScore,listScores):
    x = 0
    while x < len(listScores):
        if int(newScore) >= int(listScores[x]):
            return x, True
        x += 1
    return -1, False
 
#get player name
def getNameB():
    pygame.time.wait(500)
    DISPLAYSURF.fill(BLACK)
    name = ""
    alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    
    check = True
    x1 = 0
    while check:
        displayBoardB('WHAT IS YOUR FIRST INITIAL?',2)
        displayNameB(alphabet[x1],50)
        for action in pygame.event.get():
            if action.type == KEYDOWN:
                if action.key == K_w:
                    x1 += 1
                    if x1 >= 26:
                        x1 = 0
                elif action.key == K_s:
                    x1 -= 1
                    if x1 >= 26:
                        x1 = 25
                elif action.key == K_RETURN:
                    name += alphabet[x1]
                    check = False
        pygame.display.update()
        pygame.time.wait(200)
        DISPLAYSURF.fill(BLACK)
 
    pygame.time.wait(300)
     
    check = True
    x1 = 0
    while check:
        displayBoardB('WHAT IS YOUR LAST INITIAL?',2)
        displayNameB(alphabet[x1],50)
        for action in pygame.event.get():
            if action.type == KEYDOWN:
                if action.key == K_w:
                    x1 += 1
                    if x1 >= 26:
                        x1 = 0
                elif action.key == K_s:
                    x1 -= 1
                    if x1 >= 26:
                        x1 = 25
                elif action.key == K_RETURN:
                    name += alphabet[x1]
                    check = False
        pygame.display.update()
        pygame.time.wait(200)
        DISPLAYSURF.fill(BLACK)
         
    return name
 
#displays name choosing stuff
def displayNameB(words,pos):
    res = FONT2.render('%s' %words,True,WHITE)
    resRect = res.get_rect()
    resRect.topleft = (25,pos)
    DISPLAYSURF.blit(res,resRect)
 
#replaces the old high score
def replaceScoresB(name,pos,score):
    #print name,pos,score
    #name -> new name
    #pos -> new pos
    #score -> new score
 
    score_list = []
     
    with open('highscores2.csv','rb') as file:
        words = csv.reader(file)
        score_list = list(words)
         
    with open('highscores2.csv','wb') as file:
        lnOne = score_list[0][0].split('.')
        ctr = 9
        while ctr > pos:
            lnOne[ctr] = lnOne[ctr-1]
            ctr -= 1
        lnOne[pos] = str(score)
        string = ""
        for x in lnOne:
            string += x
            string += "."
        file.write(string[0:-1] + '\n')
        ctr = 1
        while ctr < pos+2:
            file.write(score_list[ctr][0])
            file.write('\n')
            ctr += 1
        if pos < 9:
            string = "0" + str(pos+1) + "." + "            " + name + "            " + str(score) + "\n"
            file.write(string)
            ctr = pos+2
            while ctr < 10:
                string = score_list[ctr][0]
                num = int(string[:2]) + 1
                string = "0" + str(num) + string[2:]
                file.write(string)
                file.write('\n')
                ctr += 1
            string = score_list[10][0]
            string = "10" + string[2:]
            file.write(string)
        else:
            string = "10." + "            " + name + "            " + str(score) + "\n"
            file.write(string)
    finalScreenB()
 
def finalScreenB():
    DISPLAYSURF.fill(BLACK)
    ctr = 1
    with open('highscores2.csv','rb') as file:
        words = csv.reader(file)
        score_list = list(words)
        for x in score_list:
            displayBoardB(x[0],ctr)
            ctr += 1
        lnOne = score_list[0][0].split('.')
     
    pygame.display.update()
    pygame.time.wait(10000)
    
 
def displayBoardB(words,pos):
    #print words
    res = FONT2.render('%s' %words,True,WHITE)
    resRect = res.get_rect()
    resRect.topleft = (25,pos*20-37)
    DISPLAYSURF.blit(res,resRect)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
if __name__ == '__main__':
    main()

pygame.quit()
