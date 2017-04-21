#!/usr/bin/python
# Tute.py
"""
    Copyright (C) 2011  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import g,pygame,utils,sys,buttons,load_save,layout,jig
try:
    import gtk
except:
    pass

class Tute:

    def __init__(self):
        self.journal=True # set to False if we come in via main()
        self.canvas=None # set to the pygame canvas if we come in via activity.py

    def display(self):
        g.screen.fill(utils.WHITE)
        if g.toc_showing:
            g.screen.blit(self.toc.surf,(g.offset,0))
            buttons.draw()
            return
        g.screen.blit(self.layout.surf,(g.offset,0))
        if g.jig:
            self.jig.draw()
        if g.mouse_locn:
            x,y=pygame.mouse.get_pos()
            m='('+str(x)+','+str(y)+')'; cxy=(g.sx(29),g.sy(1.2))
            utils.message(g.screen,g.font1,m,cxy,5)
        if g.colors:
            g.screen.blit(g.colors_img,g.colors_xy)
            if utils.mouse_on_img(g.colors_img,g.colors_xy):
                c=g.screen.get_at(pygame.mouse.get_pos())
                r,g1,b='0','0','0'
                if c[0]>200: r='255'
                if c[1]>200: g1='255'
                if c[2]>200: b='255'
                m='('+r+','+g1+','+b+')'; cxy=(g.sx(5.3),g.sy(19.5))
                utils.message(g.screen,g.font1,m,cxy,5)
        if self.layout.movie!=None: self.layout.movie.draw()
        buttons.on(['fd','back'])
        if g.page==1: buttons.off('back')
        elif g.page==g.last_page: buttons.off('fd')
        buttons.draw()
        if g.rect_on:
            pygame.draw.rect(g.screen,utils.GREEN,g.rect)
        if self.popup!=None: surf,x,y=self.popup; g.screen.blit(surf,(x,y))

    def update(self):
        if g.rect_on:
            ms=pygame.time.get_ticks()
            d=ms-g.rect_ms
            if d<0 or d>20:
                g.rect.x+=g.rect_dx
                if g.rect.x<0 or g.rect.x>(g.screen.get_width()-g.rect.w):
                    g.rect_dx=-g.rect_dx
                g.rect.y+=g.rect_dy
                if g.rect.y<0 or g.rect.y>(g.screen.get_height()-g.rect.h):
                    g.rect_dy=-g.rect_dy
                g.redraw=True
                g.rect_ms=ms
            
    def do_click(self):
        if self.bu!=None:
            self.bu.on(); self.bu=None; self.popup=None; return
        if g.rect_on:
            if g.rect.collidepoint(pygame.mouse.get_pos()):
                g.rect_on=False
        if g.jig:
            if self.jig.mouse(): g.redraw=True

    def do_button(self,bu):
        if bu=='toc':
            for (bu,filename,surf,x,y) in g.popups: bu.off()
            buttons.off(['fd','back','toc'])
            for (bu,n) in g.toc: bu.on()
            g.toc_showing=True
        if bu=='blue':
            for (bu,n) in g.toc:
                if bu.mouse_on():
                    if g.page!=n: g.page=n; self.render()
                    if g.jig: self.jig.shuffle()
                    break
            for (bu,filename,surf,x,y) in g.popups: bu.on()
            buttons.on(['toc'])
            for (bu,n) in g.toc: bu.off()
            g.toc_showing=False           
        if bu=='fd':
            g.page+=1; self.render()
            if g.jig: self.jig.shuffle()
        if bu=='back':
            g.page-=1; self.render()
            if g.jig: self.jig.shuffle()
        if bu=='yellow':
            for (bu,filename,surf,x,y) in g.popups:
                if bu.mouse_on():
                    if self.bu!=None: self.bu.on()
                    self.popup=surf,x,y; bu.off(); self.bu=bu; return

    def do_key(self,key):
        if key==pygame.K_v: g.version_display=not g.version_display; return

    def buttons_setup(self):
        dx=g.sy(2.4); bx=g.sx(16)-dx; by=g.sy(20.2)
        buttons.Button("back",(bx,by),True); bx+=dx
        buttons.Button("toc",(bx,by),True); bx+=dx
        buttons.Button("fd",(bx,by),True)

    def render(self):
        for (bu,filename,surf,x,y) in g.popups: bu.drop()
        self.popup=None; self.bu=None; g.popups=[]
        filename=str(g.page)+'.txt'
        layout.render(self.layout,filename)

    def flush_queue(self):
        flushing=True
        while flushing:
            flushing=False
            if self.journal:
                while gtk.events_pending(): gtk.main_iteration()
            for event in pygame.event.get(): flushing=True

    def run(self):
        g.init()
        if not self.journal: utils.load(); g.xo=False
        load_save.retrieve()
        self.toc=layout.toc()
        self.layout=layout.Layout(g.w-2*g.offset,int(g.h*19/24))
        self.render()
        self.jig=jig.Jig()
        self.buttons_setup()
        if self.canvas<>None: self.canvas.grab_focus()
        ctrl=False
        pygame.key.set_repeat(600,120); key_ms=pygame.time.get_ticks()
        going=True
        while going:
            if self.journal:
                # Pump GTK messages.
                while gtk.events_pending(): gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    if not self.journal: utils.save()
                    going=False
                elif event.type == pygame.MOUSEMOTION:
                    g.pos=event.pos
                    g.redraw=True
                    if self.canvas<>None: self.canvas.grab_focus()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    g.redraw=True
                    if event.button==1:
                        bu=''
                        if self.bu==None: bu=buttons.check()
                        if bu!='': self.do_button(bu); self.flush_queue()
                        else: self.do_click()
                elif event.type == pygame.KEYDOWN:
                    # throttle keyboard repeat
                    if pygame.time.get_ticks()-key_ms>110:
                        key_ms=pygame.time.get_ticks()
                        if ctrl:
                            if event.key==pygame.K_q:
                                if not self.journal: utils.save()
                                going=False; break
                            else:
                                ctrl=False
                        if event.key in (pygame.K_LCTRL,pygame.K_RCTRL):
                            ctrl=True; break
                        self.do_key(event.key); g.redraw=True
                        self.flush_queue()
                elif event.type == pygame.KEYUP:
                    ctrl=False
            if not going: break
            if self.layout.movie!=None: self.layout.movie.update()
            self.update()
            if g.redraw:
                self.display()
                if g.version_display: utils.version_display()
                g.screen.blit(g.pointer,g.pos)
                pygame.display.flip()
                g.redraw=False
            g.clock.tick(40)

if __name__=="__main__":
    pygame.init()
    pygame.display.set_mode((1024,768),pygame.FULLSCREEN)
    game=Tute()
    game.journal=False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
