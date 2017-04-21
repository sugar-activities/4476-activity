# layout.py
import pygame,g,utils,os,buttons,random

class Movie:
    def __init__(self):
        self.x=0; self.y=0; self.ind=0; self.imgs=[]
        self.ms=pygame.time.get_ticks(); self.n=0; self.active=True

    def update(self):
        if not self.active: return
        if self.n>20 and self.ind==random.randint(0,5):
            self.active=False; return
        ms=pygame.time.get_ticks()
        d=ms-self.ms
        if d<0 or d>50:
            self.n+=1
            self.ind=random.randint(0,len(self.imgs)-1)
            g.redraw=True
            self.ms=ms

    def draw(self):
        img=self.imgs[self.ind]
        g.screen.blit(img,(self.x+g.offset,self.y))

class Layout:
    def __init__(self,w,h,bgd=utils.WHITE):
        self.w=w; self.h=h; self.bgd=bgd
        self.surf=pygame.Surface((w,h))
        self.margin=g.sy(1)
        self.right=w-self.margin
        self.cs()
        self.font=g.font2
        self.colour=(0,0,0)
        self.set_font()
        self.green=[] # words to colour green
        self.magenta=[]

    def set_font(self):
        self.line_space=self.font.render('I',False,self.colour).get_height()

    def set_colour(self,col):
        if col=='pale':
            self.colour=(140,255,140)
        elif col=='blue':
            self.colour=(0,0,192)
        elif col=='green':
            self.colour=(0,192,0)
        else:
            self.colour=eval(col)

    def cs(self):
        self.surf.fill(self.bgd); self.x0=self.margin
        self.x=self.x0; self.y=0; self.colour=utils.BLACK
        self.mark=None; self.yk=None; self.pre=False
        self.maxx=0; self.maxy=0; self.code=False; self.fg=False
        self.movie=None; self.last=''; self.text=''
        g.mouse_locn=False; g.colors=False; g.rect_on=False; g.jig=False
        self.xy=[]; self.ystack=[]
        
    def do_line(self,l):
        if self.last=='.it':
            if not g.xo:
                if l=='terminal.png': l='command.png'
            self.img=utils.load_image(l,True)
            self.last='imgtext'; self.text=[]
        elif self.last=='imgtext':
            if l=='.e': self.last=''; self.image_text()
            else: self.text.append(l)
        elif self.last=='.movie':
            self.movie_start(l); self.last=''
        elif self.last=='.popimg':
            self.x+=popimg(l,self.x,self.y); self.last=''
        elif self.last[1:2]=='i':
            img=utils.load_image(l,True)
            d={'l':'left','c':'centre','r':'right'}
            self.image(img,d[self.last[2:3]])
            self.last=''
        elif l=='.jig':
            g.jig=True
        elif l=='.nm':
            self.x=g.sx(.2)
        elif l=='.pushy':
            self.ystack.append(self.y)
        elif l=='.popy':
            if len(self.ystack)>0: self.y=self.ystack.pop()
        elif l=='.pushxy':
            self.xy.append((self.x,self.y))
        elif l=='.popxy':
            if len(self.xy)>0: self.x,self.y=self.xy.pop()
        elif l=='.rect':
            g.rect_on=True
        elif l=='.mouse':
            g.mouse_locn=True
        elif l=='.color':
            g.colors=True
        elif l[:6]=='.popup':
            self.y+=popup(l[6:]+'.txt',self.x,self.y)
        elif l=='.pre':
            self.pre=True; self.do_line('.font3'); self.do_line('.colblue')
        elif l=='.endpre':
            self.pre=False; self.do_line('.font'); self.do_line('.col')
        elif l=='.code':
            self.code=True; self.do_line('.font3')
        elif l=='.fg':
            self.fg=True; self.do_line('.font3')
        elif l in ('.endcode','.efg'):
            self.code=False; self.fg=False
            self.do_line('.font'); self.do_line('.col')
        elif l=='.mark':
            self.mark=self.y
        elif l[:6]=='.inset':
            self.yk=self.y
            self.x0=self.w*eval(l[6:])
            self.x=self.x0; self.y=self.mark
        elif l=='.endinset':
            self.x0=self.margin; self.x=self.x0;self.y=self.yk
        elif l=='.col':
            self.colour=utils.BLACK
        elif l=='.pale':
            self.set_colour('pale')
        elif l[:4]=='.col':
            self.set_colour(l[4:])
        elif l=='.font':
            adj=False
            if self.font==g.font3:
                adj=True
                space=self.font.render(' ',False,self.colour).get_width()
            self.font=g.font2; self.set_font()
            if adj:
                diff=space-\
                    self.font.render(' ',False,self.colour).get_width()
                self.x-=diff
                if self.x<self.x0: self.x=self.x0
        elif l[:5]=='.font':
            self.font=eval('g.font'+l[5:]); self.set_font()
        elif l=='.n': self.newline()
        elif l=='.p': self.newpara()
        elif l=='.r': self.x=self.x0
        elif l=='.u': self.y-=self.line_space
        elif l=='.d': self.y+=self.line_space
        elif l=='.ff': self.cs()
        elif l=='.clear': self.x0=self.margin; self.x=self.x0
        elif l in ('.il','.ic','.ir','.it','.movie','.popimg'): self.last=l
        else:
            if self.code:               
                self.do_line('.colblue')
                s='>>>'
                if l[:4]=='    ' or l=='': s='...'
                self.do_text(s)
                self.do_line('.colgreen')
            if self.fg:
                self.do_line('.colgreen')
            self.do_text(l)
            if self.pre or self.code or self.fg: self.newline()
            
    def newline(self):
        self.x=self.x0; self.y+=self.line_space
        
    def newpara(self):
        self.x=self.x0; self.y+=self.line_space*1.3

    def movie_start(self,directory): # just dice at the moment
        self.movie=Movie()
        self.movie.x,self.movie.y=self.x,self.y
        for i in range(1,13):
            img=utils.load_image(str(i)+'.png',True,directory)
            self.movie.imgs.append(img)
        self.x0+=img.get_width()+g.sy(.4); self.x=self.x0
        
    def image(self,img,align='centre'):
        w=img.get_width(); h=img.get_height()
        if align=='left': x=self.margin
        elif align=='centre': x=(self.w-w)/2
        elif align=='right': x=self.right-w
        self.surf.blit(img,(x,self.y))
        self.y+=h
        if (self.x+w)>self.maxx: self.maxx=self.x+w
        if self.y>self.maxy: self.maxy=self.y

    def image_text(self):
        x0,x,y=self.x0,self.x,self.y
        self.image(self.img,'left')
        self.x0+=self.img.get_width()+g.sy(.4); self.x=self.x0; self.y=y
        for l in self.text:
            self.do_line(l)
        self.text=[]
        self.x0=x0
        y+=self.img.get_height()
        if y>self.y: self.y=y
        self.x=self.x0

    def do_text(self,s):
        space=self.font.render(' ',False,self.colour).get_width()
        for word in s.split(' '):
            col=self.colour; font=self.font
            w=word.rstrip(','); w=w.rstrip('.')
            if w in self.green: col=(0,150,0); font=g.font3
            if w in self.magenta: col=utils.MAGENTA; font=g.font3
            if not g.xo:
                if word=='Terminal': word='Command Prompt'
            wrd=font.render(word,True,col) # wrd is a surface
            w=wrd.get_width()
            if self.x+space+w>self.right: self.newline()
            self.surf.blit(wrd,(self.x,self.y))
            self.x+=space+w
            if self.x>self.maxx: self.maxx=self.x
            if self.y>self.maxy: self.maxy=self.y

def render(layout,filename): # eg data/1.txt
    layout.cs()
    fname=os.path.join('data',filename)
    f=open(fname,'r')
    for line in f.readlines():
        l=line.rstrip()
        layout.do_line(l)
    f.close()
    return layout.maxx,layout.maxy+layout.line_space

def popup(filename,x,y): # eg data/1a.txt - x,y is the button posn
    layout=Layout(g.w-2*g.offset,g.h,(255,255,220))
    maxx,maxy=render(layout,filename)
    border=g.sy(.15); b2=2*border
    surf=pygame.Surface((maxx+b2,maxy+b2))
    surf.fill(utils.MAGENTA)
    surf.blit(layout.surf,(border,border),(0,0,maxx,maxy))
    bu=buttons.Button("yellow",(x+g.offset,y),False)
    dy=bu.up.get_height()
    y+=dy/4
    if (x+maxx+b2)>layout.w: x=layout.w-maxx-b2
    if (y+maxy+b2)>g.screen.get_height(): y=g.screen.get_height()-maxy-b2
    g.popups.append((bu,filename,surf,x+g.offset,y))
    return dy

def popimg(filename,x,y): # eg data/pic.png
    img=utils.load_image(filename); w=img.get_width(); h=img.get_height()
    border=g.sy(.15); b2=2*border
    surf=pygame.Surface((w+b2,h+b2))
    surf.fill(utils.MAGENTA)
    surf.blit(img,(border,border))
    bu=buttons.Button("yellow",(x+g.offset,y),False)
    dy=bu.up.get_height()
    y+=dy/4
    if (x+w+b2)>(g.w-2*g.offset): x-=(x+w+b2)-(g.w-2*g.offset)
    if (y+h+b2)>g.h: y=g.screen.get_height()-h-b2
    g.popups.append((bu,filename,surf,x+g.offset,y))
    return dy

def toc():
    layout=Layout(g.w-2*g.offset,g.screen.get_height())
    maxx,maxy=render(layout,'toc_head.txt')
    fname=os.path.join('data','toc.txt')
    f=open(fname,'r')
    layout.y=maxy-layout.line_space
    n=0; sy=layout.y
    layout.green=['sum','append','len','max','min','def','return',\
                  'for','in','range','import','reverse','sort','return',\
                  'print','if','True','False','random.randint','gedit','while']
    layout.magenta=['double','triple','total','hasvowel','big2',
                    'squares','shuffle','times','dice','pg.py']
    layout.x0=layout.margin/2; layout.x=layout.x0
    first=True # 1st of pair of lines
    for line in f.readlines():
        s=''
        if first: n+=1; s=str(n)+'.'
        if n>9: layout.x=layout.w/2+g.sy(.2)
        if first:
            bu=buttons.Button("blue",(layout.x+g.offset,layout.y),False)
            bu.off()
            g.toc.append((bu,n))
            dx=bu.up.get_width(); dy=bu.up.get_height()
            layout.y+=dy/4
        l=line.rstrip()
        layout.x+=dx
        layout.do_text(s+l)
        layout.newline()
        if n==9:
            if not first: layout.y=sy
        first=not first
    f.close()
    return layout


    


                         
                         
                               
        
    
        
        
        
