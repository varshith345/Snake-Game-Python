import pygame
from pygame.locals import *
import time
import random

SIZE=40
BACKGROUND_COLOR=(110,110,5)

class Apple:
    def __init__(self,parent_screen):
        self.parent_screen=parent_screen
        self.image=pygame.image.load("apple.jpg").convert()
        self.x=120
        self.y=120
        
    def draw(self):
        self.parent_screen.blit(self.image,((self.x,self.y)))
        pygame.display.flip()
      
    def move(self):
        self.x=random.randint(0,24)*SIZE
        self.y=random.randint(0,19)*SIZE
          
     
            
class Snake:
    def __init__(self,parent_screen,length):
        self.parent_screen=parent_screen
        self.block=pygame.image.load("block.jpg").convert()
        self.length=length
        self.x=[40]*length
        self.y=[40]*length
        self.direction='down'
        
    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()
     
    def move_left(self):
        self.direction='left'
    def move_right(self):
        self.direction='right'
    def move_up(self):
        self.direction='up'
    def move_down(self):
        self.direction='down'   
        
    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]
            
        if self.direction=='left':
            self.x[0]-=SIZE
        if self.direction=='right':
            self.x[0]+=SIZE
        if self.direction=='up':
            self.y[0]-=SIZE 
        if self.direction=='down':
            self.y[0]+=SIZE
            
        self.draw()  
        
    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)                                     

class Game:
    def __init__(self):
        pygame.init()
        self.surface=pygame.display.set_mode((1000,800))
        pygame.mixer.init()
        self.play_background_music()
        
        self.snake=Snake(self.surface,1)
        self.snake.draw()
        self.apple=Apple(self.surface)
        self.apple.draw()
        
    def play_background_music(self):
        pygame.mixer.music.load('bg_music_1.mp3')
        pygame.mixer.music.play(-1,0) 
      
    def render_background(self):
        bg=pygame.image.load('background.jpg')
        self.surface.blit(bg,(0,0))
            
    def play_sound(self,sound_name):
        if sound_name=="crash":
            sound=pygame.mixer.Sound("crash.mp3")
        elif sound_name=="ding":
            sound=pygame.mixer.Sound("ding.mp3")  
        pygame.mixer.Sound.play(sound)             
        
    def is_collision(self,x1,y1,x2,y2):
        if x1>=x2 and x1< x2+SIZE:
            if y1>=y2 and y1< y2+SIZE:
                return True
        return False
    
    def display_score(self):
        font=pygame.font.SysFont('arial',30)
        score=font.render(f"Score: {self.snake.length}",True,(200,200,200))
        self.surface.blit(score,(850,10))        
        
    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw() 
        self.display_score()
        pygame.display.flip()
        
        if self.snake.x[0]<0 or self.snake.y[0]>800 or self.snake.x[0]>1000 or self.snake.y[0]<0:
            self.play_sound("crash")
            raise "Hit Boundary"
        
        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()  
            
        for i in range(2,self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                self.play_sound("crash")
                raise "Collosion Occured"    
           
    def show_game_over(self):
        self.render_background()
        font=pygame.font.SysFont('arial',30)
        line1=font.render(f"Game is Over! Your score is {self.snake.length}",True,(255,255,255)) 
        self.surface.blit(line1,(200,300))
        line2=font.render(f"To play Again press ENTER. To exit press ESCAPE!",True,(255,255,255)) 
        self.surface.blit(line2,(200,350))
        pygame.mixer.music.pause()
        pygame.display.flip()
         
    def reset(self):
        self.snake=Snake(self.surface,1)
        self.apple=Apple(self.surface)            
        
    def run(self):   
        rng=True
        pause=False
        
        while rng:
            for evt in pygame.event.get():
                if evt.type==KEYDOWN:
                    if evt.key==K_ESCAPE:
                        rng=False
                    if evt.key==K_RETURN:
                        pygame.mixer.music.unpause()
                        pause=False
                        
                    if not pause:
                            if evt.key==K_LEFT:
                                self.snake.move_left()
                            if evt.key==K_RIGHT:
                                self.snake.move_right()
                            if evt.key==K_UP:
                                self.snake.move_up()
                            if evt.key==K_DOWN:
                                self.snake.move_down()
                                  
                elif evt.type==QUIT:
                    rng=False 
            
            try:
                if not pause:
                    self.play()
                    
            except Exception as e:
                self.show_game_over()
                pause=True
                self.reset()                
            
            time.sleep(.3)                            

if __name__=="__main__":
    game=Game()
    game.run()
