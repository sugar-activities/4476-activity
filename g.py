# g.py - globals
import pygame,utils,random

app='Python Tute'
ver='21'
ver='22'
# color swatch fixed
ver='23'
# while in TOC colored
ver='24'
# page numerals, page titles
# screenw,h at top of pg.py
ver='25'
# font initially g.font2
ver='26'
# if popup up click just clears it
# added pale
ver='27'
# variable name 'l' avoided
#  page 5 last button
#  page 6
ver='28'
# 11.txt - screengrabs, 17b.txt 
ver='29'
# 11.txt

UP=(264,273)
DOWN=(258,274)
LEFT=(260,276)
RIGHT=(262,275)
CROSS=(259,120)
CIRCLE=(265,111)
SQUARE=(263,32)
TICK=(257,13)
NUMBERS={pygame.K_1:1,pygame.K_2:2,pygame.K_3:3,pygame.K_4:4,\
           pygame.K_5:5,pygame.K_6:6,pygame.K_7:7,pygame.K_8:8,\
           pygame.K_9:9,pygame.K_0:0}

def init(): # called by run()
    random.seed()
    global redraw
    global screen,w,h,font1,font2,font3,clock
    global factor,offset,imgf,message,version_display
    global pos,pointer
    redraw=True
    version_display=False
    screen = pygame.display.get_surface()
    pygame.display.set_caption(app)
    screen.fill(utils.WHITE)
    pygame.display.flip()
    w,h=screen.get_size()
    if float(w)/float(h)>1.5: #widescreen
        offset=(w-4*h/3)/2 # we assume 4:3 - centre on widescreen
    else:
        h=int(.75*w) # allow for toolbar - works to 4:3
        offset=0
    factor=float(h)/24 # measurement scaling factor (32x24 = design units)
    imgf=float(h)/900 # image scaling factor - all images built for 1200x900
    clock=pygame.time.Clock()
    if pygame.font:
        t=int(32*imgf); font1=pygame.font.Font('Arial.ttf',t)
        t=int(24*imgf); font2=pygame.font.Font('Arial.ttf',t)
        t=int(26*imgf); font3=pygame.font.Font('courbd.ttf',t)
    message=''
    pos=pygame.mouse.get_pos()
    pointer=utils.load_image('pointer.png',True)
    pygame.mouse.set_visible(False)
    
    # this activity only
    global page,last_page,popups,toc,toc_showing,xo
    global mouse_locn,colors,colors_img,colors_xy
    global rect,rect_dx,rect_dy,rect_on,rect_ms,jig
    page=1; last_page=18; popups=[]; toc=[] # two lists for buttons
    toc_showing=False; mouse_locn=False; colors=False
    colors_img=utils.load_image('colors.png'); colors_xy=(sx(1),sy(17.05))
    rect=pygame.Rect(0,0,sy(5),sy(3)); rect_dx,rect_dy=2,2; rect_on=False
    rect_ms=0; jig=False
    xo=True
    
def sx(f): # scale x function
    return int(f*factor+offset+.5)

def sy(f): # scale y function
    return int(f*factor+.5)
