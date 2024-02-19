import pygame
import random
import player1
import player2
import ball
import button

#pygame prep
pygame.init()

#window settings
WIDTH,HEIGHT = 1280,720
window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("CAT BALL")


#define fonts
font = pygame.font.SysFont("arialblack",40)
TEXT_COL = (255,255,255)

#load button images
resume_img = pygame.image.load("resume.png").convert_alpha()
quit_img = pygame.image.load("quit.png").convert_alpha()
restart_img = pygame.image.load("restart.png").convert_alpha()

#create button instances
resume_button = button.Button(400,125,resume_img,1)
quit_button = button.Button(360,465,quit_img,1)
restart_button = button.Button(370,300,restart_img,1)

def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    window.blit(img,(x,y))

game_paused = False


#FPS settings
FPS = 30
clock = pygame.time.Clock()

#class game
class Game():
    def __init__(self,gamer1,gamer2,ball):
        #game paramaters
        self.gamer1 = gamer1
        self.gamer2 = gamer2
        self.ball_set = ball_set

        #background and gameover photos
        self.background = pygame.image.load("background.jpg")
        self.finish = pygame.image.load("gameover.jpg")
        self.menu_img = pygame.image.load("menu.jpg")

        #game paramaters
        self.player1_score = 0
        self.player2_score = 0
        self.score = 1
        self.counter = 45
        self.fps_counter = 0

        #game sounds
        self.game_font = pygame.font.Font("writing.ttf",35)
        self.corner_sound = pygame.mixer.Sound("point.wav")
        self.touch_sound = pygame.mixer.Sound("touch.wav")

        self.speed = 10
    def setGamer1(self,gamer1):
        self._gamer1 = gamer1

    def setGamer2(self,gamer2):
        self._gamer2 = gamer2

    def setBall_set(self,ball_sett):
        self._ball_set = ball_set

    def getGamer1(self,gamer1):
        return self._gamer1
    def getGamer2(self,gamer2):
        return self._gamer2
    def getBall_set(self,ball_set):
        return self._ball_set
    

    
    def update(self):
        self.fps_counter += 1
        if self.fps_counter == FPS:
            self.counter -= 1
            self.fps_counter = 0
            if self.counter == 0:
                self.end()
        
        self.touch()
        self.game_status()

    def draw(self):
        window.blit(self.background,(0,0))

        point1 = self.game_font.render("1.Player Score: "+str(self.player1_score),True,(255,160,122))
        point1_dest= point1.get_rect()
        point1_dest.topleft=(30,50)

        point2 = self.game_font.render("2.Player Score: "+str(self.player2_score),True,(255,160,122))
        point2_dest = point2.get_rect()
        point2_dest.topleft=(WIDTH-300,60)

        count_wrt = self.game_font.render("Time Left: "+str(self.counter),True,(255,0,0))
        count_wrt_dest = count_wrt.get_rect()
        count_wrt_dest.topleft=(WIDTH//2-120,60)

        window.blit(point1,point1_dest)
        window.blit(point2,point2_dest)
        window.blit(count_wrt,count_wrt_dest)

    def touch(self):
        if pygame.sprite.spritecollide(self.gamer1,self.ball_set,False):
            self.touch_sound.play()
            for ball in self.ball_set.sprites():
                ball.directionx *= -1
                if ball.speed <= 15:
                    ball.speed += 1
                
        if pygame.sprite.spritecollide(self.gamer2,self.ball_set,False):
            self.touch_sound.play()
            for ball in self.ball_set.sprites():
                ball.directionx *= -1
                if ball.speed <= 15:
                    ball.speed += 1

    def game_status(self):
        for ball in self.ball_set.sprites():
            if ball.rect.left <= 10:
                self.corner_sound.play()
                self.player2_score += self.score
            if ball.rect.right >= WIDTH-10:
                self.corner_sound.play()
                self.player1_score += self.score
        

    def end(self):
        ending = True
        global status
        window.blit(self.finish,(0,0))
        a = " CAT 1 WON "
        b = " CAT 2 WON"
        c = "  TIED!  "

        if self.player1_score>self.player2_score:
            winner = self.game_font.render(a,True,(255,160,122))
            winner_dest = winner.get_rect()
            winner_dest.topleft=(WIDTH//2-80,HEIGHT//2+150)

        if self.player2_score>self.player1_score:
            winner = self.game_font.render(b,True,(255,160,122))
            winner_dest = winner.get_rect()
            winner_dest.topleft=(WIDTH//2-80,HEIGHT//2+150)

        if self.player1_score == self.player2_score:
            winner = self.game_font.render(c,True,(255,160,122))
            winner_dest = winner.get_rect()
            winner_dest.topleft=(WIDTH//2-80,HEIGHT//2+150)

        window.blit(winner,winner_dest)
        pygame.display.update()
        while ending:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.restart()
                        ending = False
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        ending = False
                        status = False
                        

    def restart(self):
        self.player1_score = 0
        self.player2_score = 0
        self.counter = 45



#menu settings
    def menu(self):
        game_paused = True
        global status
        window.blit(self.menu_img,(0,0))
        
        pygame.display.update()
        while game_paused:
            if game_paused==True:
                if resume_button.draw(window):
                    game_paused = False
                if quit_button.draw(window):
                    status = False
                    pygame.quit()
                if restart_button.draw(window):
                    
                    self.restart()
                    
                    game_paused =False
                pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_paused = False
                    if event.type == pygame.QUIT:
                        status = False
                        game_paused = False
                        pygame.quit()

#player and ball settings
player1_set = pygame.sprite.Group()
gamer1 = player1.Player1()
player1_set.add(gamer1)

player2_set = pygame.sprite.Group()
gamer2 = player2.Player2()
player2_set.add(gamer2)

ball_set = pygame.sprite.Group()
ball1 = ball.Ball(random.randint(300,500),random.randint(300,500))
ball_set.add(ball1)

game = Game(gamer1,gamer2,ball_set)

#game loop
status = True
while status:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.menu()
                
        if event.type == pygame.QUIT:
            status = False

    #game set
    game.update()
    game.draw()
    
    #gamer set
    player1_set.update()
    player1_set.draw(window)

    player2_set.update()
    player2_set.draw(window)

    ball_set.update()
    ball_set.draw(window)

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
