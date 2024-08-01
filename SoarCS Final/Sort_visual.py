import pygame as pg
import random
import time
pg.init()

width = 500
height = 500
win = pg.display.set_mode((width,height))
pg.display.set_caption("Sort_Visual")

font = pg.font.SysFont('Georgia',28,bold=True)
nmRandom = font.render('Random', True, 'white')
nmStart = font.render('Start', True, 'white')

btnRandom = pg.Rect(125,100,150,60)
btnStart = pg.Rect(375,100,110,60)

# Gets 5 random number and puts them in a arra
arr = [random.randint(50, 150)*2 for _ in range(20)]

class rect():
    @staticmethod
    def draw(win,color,width,height,x,y):
        pg.draw.rect(win,color,(width,height,x,y))

# creates random height of square
running = True
frameRate = pg.time.Clock()

def bubbleSort(arr, height):
    for i in range(len(arr)):
         for j in range(0,len(arr)-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                win.fill((0,0,0))
                for k in range(20):
                    rect.draw(win,(255,0,0),k*25,height - arr[k],20,arr[k])
                pg.display.flip()
                pg.time.delay(25)
while running:
    # win.fill((0,0,0))
    for i in range(0,20):
        rect.draw(win,(255,0,0),i*25,height - arr[i],20,arr[i])
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            
# Restart sorting
        if event.type == pg.MOUSEBUTTONDOWN:
            if btnRandom.collidepoint(event.pos):
                arr = [random.randint(50, 150)*2 for _ in range(20)]
                win.fill((0,0,0))

            sorted = all(a <= b for a, b in zip(arr, arr[1:]))
            if btnStart.collidepoint(event.pos):
                     if not sorted:
                        start = time.time()
                        bubbleSort(arr,height)
                        end = time.time()
                        length = str(end - start)
                        timer = font.render("Timer: "+length, True, (255, 255, 255))
                        win.blit(timer, timer.get_rect())
                        pg.display.flip()

    x,y = pg.mouse.get_pos()
    if btnRandom.x <= x <= btnRandom.x + 150 and btnRandom.y <= y <= btnRandom.y + 60:
        pg.draw.rect(win,(200,0,0,),btnRandom)
    else:
        pg.draw.rect(win,(255,0,0), btnRandom)
    win.blit(nmRandom,(btnRandom.x +10, btnRandom.y+10))

    if btnStart.x <= x <= btnStart.x + 110 and btnStart.y <= y <= btnStart.y + 60:
        pg.draw.rect(win,(200,0,0,),btnStart)
    else:
        pg.draw.rect(win,(255,0,0), btnStart)
    win.blit(nmStart,(btnStart.x +20, btnStart.y+10))
       
    pg.display.flip()
    frameRate.tick(60)
pg.quit()