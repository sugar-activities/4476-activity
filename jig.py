# jig.py

import pygame,utils,g,random

pieces=[]

class Piece:
    def __init__(self,img,x,y):
        self.x=x; self.y=y; self.img=img
        
class Jig:
    def __init__(self):
        pic=utils.load_image('jig.jpg')
        nc=4; nr=3; w=pic.get_width()/nc; h=pic.get_height()/nr
        x0=g.sx(.5); y0=g.sy(2.2); npieces=nr*nc
        y=y0
        for r in range(nr):
            x=x0
            for c in range(nc):
                piece=Piece(pic.subsurface(x-x0,y-y0,w,h),x,y)
                pieces.append(piece)
                x+=w
            y+=h
        self.carry=None; self.empty=None; self.w=w; self.h=h
        self.shuffle()

    def shuffle(self):
        if self.carry!=None:
            pieces[self.empty].img=self.carry
            self.carry=None
        n=len(pieces)
        for i in range(100):
            r=random.randint(0,n-1)
            k=pieces[0].img; pieces[0].img=pieces[r].img; pieces[r].img=k

    def draw(self):
        for piece in pieces:
            x=piece.x; y=piece.y; img=piece.img
            if img != None:
                g.screen.blit(img,(x,y))
            else:
                pygame.draw.rect(g.screen,utils.BLUE,(x,y,self.w,self.h))
        if self.carry!=None:
            x,y=g.pos
            g.screen.blit(self.carry,(x-self.w/2,y-self.h/2))

    def mouse(self):
        ind=0
        for piece in pieces:
            x=piece.x; y=piece.y
            rect=pygame.Rect(x,y,self.w,self.h)
            if rect.collidepoint(g.pos):
                if self.carry==None:
                    self.carry=pieces[ind].img
                    pieces[ind].img=None
                    self.empty=ind
                else:
                    pieces[self.empty].img=pieces[ind].img
                    pieces[ind].img=self.carry
                    self.carry=None
                return True
            ind=ind+1
        return False
    
            
        
        
        
