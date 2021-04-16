import pygame
from pygame.locals import *
import time
import random
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAP_SIZE = 12

class Text:
    #cree une classe permettant de modifier et utuliser du text TOTO
    def __init__(self, text, pos,**options):
        self.text = text
        self.pos = pos
        self.fontname = None
        self.fontsize = 72
        self.fontcolor = Color("black")
        self.set_font()
        self.render()
    def set_font(self):
        #cree un objet font qui a une taille et un nom
        self.font = pygame.font.Font(self.fontname,self.fontsize)
    def render(self):
        #permet de creer une image a partir du texte
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos
    def draw(self):
        #affiche le texte
        Game.screen.blit(self.img, self.rect)

class Menu:
    #permet de creer et gerer le jeu et l'ecran
    def __init__(self, game):

        self.game = game
        self.w = Game.screen.get_width()
        self.h = Game.screen.get_height()
        pygame.display.set_caption('Castillon')
        pygame.display.set_icon(pygame.image.load('grass.png'))
        self.title = Text('Castillon', pos=(0, 20))
        self.title.fontsize = 400
        self.title.fontcolor = Color('blue')
        self.title.set_font()
        self.title.render()
        self.title.pos = (self.w/2 - self.title.rect.width / 2, 20)
        self.title.set_font()
        self.title.render()

        self.starter = Text('Start', pos=(20, self.h/2))
        self.starter.fontsize = 100
        self.starter.set_font()
        self.starter.render()

        Menu.running = True
        self.shortcut ={  }

    def run(self):
        #boucle principale permettant le fonctionnement du jeu et detecte les actions du joueur

        Game.screen.fill(Color('light green'))
        self.title.draw()
        self.starter.draw()
        while Menu.running == True:
            pygame.display.update()
            #Prend tout les evenements du joueur
            for event in pygame.event.get():
                if event.type == QUIT:
                    #Permet de quitter l'application
                    Menu.running = False
                if event.type == KEYDOWN:
                    #permet de verifier si l'utulisateur veut donner des commandes
                    self.shortcuts(event)
                #permet de changer la couleur du texte quand la souris est dessus
                if event.type == MOUSEMOTION:
                    if self.starter.rect.collidepoint(event.__getattribute__('pos')):
                        rect = Rect(self.starter.rect.left, self.starter.rect.top, self.starter.rect.right,
                                    self.starter.rect.bottom)
                        pygame.draw.rect(Game.screen, Color('light green'), rect)
                        self.starter.fontcolor = Color('yellow')
                        self.starter.render()
                        self.starter.draw()

                    if self.starter.rect.collidepoint(event.__getattribute__('pos'))!= True and self.starter.fontcolor != Color('black'):
                        rect = Rect(self.starter.rect.left, self.starter.rect.top, self.starter.rect.right,
                                    self.starter.rect.bottom)
                        pygame.draw.rect(Game.screen, Color('light green'), rect)
                        self.starter.fontcolor = Color('black')
                        self.starter.render()
                        self.starter.draw()
                #redessine l'ecran dans le cas de changement de la taille de l'ecran
                if event.type == WINDOWMAXIMIZED:
                    Game.screen.fill(Color('light green'))
                    self.title.draw()
                    self.starter.draw()
                if event.type == WINDOWRESIZED:
                    Game.screen.fill(Color('light green'))
                    self.title.draw()
                    self.starter.draw()
                #fait fonctionner les options du menu
                if event.type == MOUSEBUTTONDOWN:
                    if self.starter.rect.collidepoint(event.__getattribute__('pos')):
                        return "battle"
        pygame.quit()
    def shortcuts(self,event):
        #verifier un dictionnaire afin de pouvoir executer les commandes     INUTILE POUR LE MOMENT
        key = event.key
        mod = event.mod
        if (key,mod) in self.shortcut:
            exec(self.shortcut[key,mod])
    #commence veritablement le jeu

class Battle:
    def __init__(self, game):
        self.game = game

        #effets speciaux
        Game.screen.fill(Color('white'))
        pygame.display.flip()
        time.sleep(0.2)
        Game.screen.fill(Color('gray'))
        pygame.display.flip()
        time.sleep(0.2)
        Game.screen.fill(Color('black'))
        pygame.display.flip()
        time.sleep(0.2)
        Game.screen.fill(Color('gray'))
        time.sleep(0.2)
        #reverifie la taille de l'ecran pour plus tard
        self.w = Game.screen.get_width()
        self.h = Game.screen.get_height()
        #code pour l'initialization du jeu
            #liste des tuiles possibles
        self.colorgen = [pygame.image.load("grass.png").convert(),pygame.image.load("grass.png").convert(),
                         pygame.image.load("grass.png").convert(),pygame.image.load("icelake.png").convert(),
                         pygame.image.load("sand.png").convert(),pygame.image.load("forest.png").convert(),
                         pygame.image.load("swamp.png").convert(),pygame.image.load("boulder.png").convert(),
                         pygame.image.load("snowy mountain.png").convert(),pygame.image.load("mountain.png").convert(),
                         pygame.image.load("lava.png").convert(),pygame.image.load("volcano.png").convert(),
                         pygame.image.load("water.png").convert(),pygame.image.load("water.png").convert(), ]
            #liste des informations pertinentes sur ces tuiles
        self.title_entries = ["grass","grass","grass","ice","sand","forest","swamp","boulder","snowy mountain","mountain","lava","volcano","water",'water']
        self.textentries = ["a good place to settle","a good place to settle","a good place to settle","warmer clothes are needed to survive here","nothing usefull here","a source of wood","a good place to hide","ideal for a quarry","cold and desolate","difficult to traverse","hot and dangerous","an active hasard","a boat is needed to traverse this",'a boat is needed to traverse this']
        self.blueunits = {}
        self.redunits = {}
        self.turn = "blue"
        self.info = Text('', pos=(40, 80))
        self.description = Text('', pos=(40, 152))
        #variables utiles plus tard
        self.tilesize = 600/MAP_SIZE
        self.clicking = True
        self.tilep = False
        self.tileselect = 0
        self.buildings = []
        self.swapped = False
        self.currentsquare =(0,0)
        self.nextsquare= (0,0)
        self.random_gen = []

    def create_map(self):
        # generation de monde random
        for i in range(MAP_SIZE**2):
            self.random_gen.append(random.randint(0,13))
        for i in range(len(self.random_gen)):
            #Des parametres afin d'empecher certains scenarios detrimentales au jeu et creer un map logique
            if self.random_gen[i] == 11:
                self.tilenextto(i,7,necessaryadjacentcolors=(10,None))
            if self.random_gen[i] == 10:
                self.tilenextto(i,9,None,(11,None))
            if self.random_gen[i] == 8:
                self.tilenextto(i,9,(10,11))
            if self.random_gen[i] == 9:
                self.tilenextto(i,10,(11,None),None)
            if self.random_gen[i] >=12:
                if self.tilenextto(i, 3, (8,None)):
                    None
                else :
                    self.tilenextto(i, 7, (10, 11))
            if self.random_gen[i] == 6:
                self.tilenextto(i,5,necessaryadjacentcolors=(12,13))
            if self.random_gen[i] == 5:
                if self.tilenextto(i,7,(10,11)):
                    None
                else :
                    self.tilenextto(i,6,(12,13))
            if self.random_gen[i] == 4:
                self.tilenextto(i, 2, necessaryadjacentcolors=(12,13))
            if self.random_gen[i] == 3:
                self.tilenextto(i, 2, (10, 11),(8,12,13))
            if self.random_gen[i] <= 2:
                self.tilenextto(i,4,(12,13))
        for i in range(len(self.random_gen)):
            #Vu que le programme va de tuile en tuile certains bugs peuvent se passer sur la generation il faut donc refaire le programme d'avant de maniere independante
            if self.random_gen[i] == 11:
                self.tilenextto(i,7,necessaryadjacentcolors=(10,None))
            if self.random_gen[i] == 10:
                self.tilenextto(i,9,None,(11,None))
            if self.random_gen[i] == 8:
                self.tilenextto(i,9,(10,11))
            if self.random_gen[i] == 9:
                self.tilenextto(i,10,(11,None),None)
            if self.random_gen[i] >=12:
                if self.tilenextto(i, 3, (8,None)):
                    None
                else :
                    self.tilenextto(i, 7, (10, 11))
            if self.random_gen[i] == 6:
                self.tilenextto(i,5,necessaryadjacentcolors=(12,13))
            if self.random_gen[i] == 5:
                if self.tilenextto(i,7,(10,11)):
                    None
                else :
                    self.tilenextto(i,6,(12,13))
            if self.random_gen[i] == 4:
                self.tilenextto(i, 2, necessaryadjacentcolors=(12,13))
            if self.random_gen[i] == 3:
                self.tilenextto(i, 2, (10, 11),(8,12,13))
            if self.random_gen[i] <= 2:
                self.tilenextto(i,4,(12,13))



        #for i in range(MAP_SIZE):
         #   for j in range(1, MAP_SIZE + 1):
          #      #pygame.draw.rect(Game.screen, self.colorgen[self.random_gen[i*MAP_SIZE+j-1]], Rect(self.w / 2 + self.tilesize * i, self.tilesize * j, self.tilesize, self.tilesize))
           #     rect = self.colorgen[self.random_gen[i*MAP_SIZE+j-1]].get_rect()
            #    rect.topleft = self.w / 2 + self.tilesize * i,self.tilesize * j
             #   Game.screen.blit(self.colorgen[self.random_gen[i * MAP_SIZE + j - 1]], rect)

    def tilenextto(self,i,newcolor,illegaladjacentcolors = None,necessaryadjacentcolors = None):
        necessary = 0
        if necessaryadjacentcolors is None:
            necessary = 1
        if illegaladjacentcolors is not None:
            if i % MAP_SIZE != 0:
                if self.random_gen[i - 1] in illegaladjacentcolors:
                    self.random_gen[i] = newcolor
            if (i+1) % MAP_SIZE != 0:
                if self.random_gen[i + 1] in illegaladjacentcolors:
                    self.random_gen[i] = newcolor
            if i < MAP_SIZE ** 2 - MAP_SIZE :
                if self.random_gen[i + MAP_SIZE] in illegaladjacentcolors:
                    self.random_gen[i] = newcolor
            if i > MAP_SIZE - 1:
                if self.random_gen[i - MAP_SIZE] in illegaladjacentcolors:
                    self.random_gen[i] = newcolor
        if necessaryadjacentcolors is not None:
            if i % MAP_SIZE != 0:
                if self.random_gen[i - 1] in necessaryadjacentcolors:
                    necessary = 1
            if (i+1) % MAP_SIZE != 0:
                if self.random_gen[i + 1]  in necessaryadjacentcolors:
                    necessary = 1
            if i < MAP_SIZE ** 2 - MAP_SIZE :
                if self.random_gen[i + MAP_SIZE] in necessaryadjacentcolors:
                    necessary = 1
            if i > MAP_SIZE - 1:
                if self.random_gen[i - MAP_SIZE] in necessaryadjacentcolors:
                    necessary = 1
        if necessary == 0:
            self.random_gen[i] = newcolor
        if self.random_gen[i] == newcolor:
            return True

    def run(self):
        #self.create_map()
        Battle.running = True
        while Battle.running:
            #Prend tous les evenements du joueur
            for event in pygame.event.get():
                if event.type == QUIT:
                    #Permet de quitter l'application
                    Battle.running = False
                if event.type == MOUSEMOTION :
                    if self.clicking == False :

                        self.game.map.draw()
                        # for i in range(MAP_SIZE):
                        #     for j in range(1, MAP_SIZE + 1):
                        #         pygame.draw.rect(Game.screen, Color('gray'), Rect((self.w / 2) + self.tilesize * i, self.tilesize * j, self.tilesize, self.tilesize), 1)
                        #         rect = self.colorgen[self.random_gen[i * MAP_SIZE + j - 1]].get_rect()
                        #         rect.topleft = self.w / 2 + self.tilesize * i, self.tilesize * j
                        #         Game.screen.blit(self.colorgen[self.random_gen[i * MAP_SIZE + j - 1]], rect)

                        for i in range(MAP_SIZE):
                            for j in range(1, MAP_SIZE + 1):
                                if Rect((self.w / 2) + self.tilesize * i, self.tilesize * j, self.tilesize, self.tilesize).collidepoint(event.__getattribute__('pos')):
                                    pygame.draw.rect(Game.screen, Color('gray'), Rect((self.w / 2) + self.tilesize * i, self.tilesize * j, self.tilesize, self.tilesize), 1)
                                    pygame.draw.rect(Game.screen, Color('red'), Rect((self.w / 2) + self.tilesize * i, self.tilesize * j, self.tilesize, self.tilesize), 1)
                                    self.clickableinfo = self.title_entries[self.game.map.random_gen[i*MAP_SIZE+j-1]]
                                    self.clickabledescription = self.textentries[self.game.map.random_gen[i*MAP_SIZE+j-1]]
                                    break
                    elif self.swapped :
                        for i in range(MAP_SIZE):
                            for j in range(1, MAP_SIZE + 1):
                                if Rect((self.w / 2) + self.tilesize * i, self.tilesize * j, self.tilesize, self.tilesize).collidepoint(event.__getattribute__('pos')):
                                    self.nextsquare = (i,j)
                        self.Movement(self.currentsquare,self.nextsquare)
                if event.type == MOUSEBUTTONDOWN :
                    self.clicking = True
                    for i in range(MAP_SIZE):
                        for j in range(1, MAP_SIZE + 1):
                            if Rect((self.w / 2) + self.tilesize * i, self.tilesize * j, self.tilesize, self.tilesize).collidepoint(event.__getattribute__('pos')):
                                self.currentsquare = (i,j)
                                break
                if event.type == MOUSEBUTTONUP :
                    self.swapped = True
                    for i in range(MAP_SIZE) :
                        for j in range(1, MAP_SIZE+1):
                            if Rect((self.w / 2) + self.tilesize * i, self.tilesize * j, self.tilesize, self.tilesize).collidepoint(event.__getattribute__('pos')):
                                pygame.draw.rect(Game.screen, Color('gray'), self.info.rect)
                                self.info = Text(self.clickableinfo, pos=(40,80))
                                self.info.draw()
                                pygame.draw.rect(Game.screen, Color('gray'), self.description.rect, )
                                self.description = Text(self.clickabledescription, pos=(40, 152))
                                self.description.fontsize = 36
                                self.description.set_font()
                                self.description.render()
                                self.description.draw()
                    self.clicking = False
                if event.type == WINDOWMAXIMIZED:
                    Game.screen.fill(Color('gray'))
                    self.info.draw()
                    self.description.draw()
                    Game.map.draw()
                    #for i in range(MAP_SIZE):
                    #    for j in range(1, MAP_SIZE+1):
                    #        rect = self.colorgen[self.random_gen[i * MAP_SIZE + j - 1]].get_rect()
                    #        rect.topleft = self.w / 2 + self.tilesize * i, self.tilesize * j
                    #        Game.screen.blit(self.colorgen[self.random_gen[i * MAP_SIZE + j - 1]], rect)
                if event.type == WINDOWRESIZED:
                    Game.screen.fill(Color('gray'))
                    self.info.draw()
                    self.description.draw()
                    Game.map.draw()
                    #for i in range(MAP_SIZE):
                    #    for j in range(1, MAP_SIZE+1):
                    #        rect = self.colorgen[self.random_gen[i * MAP_SIZE + j - 1]].get_rect()
                    #        rect.topleft = self.w / 2 + self.tilesize * i, self.tilesize * j
                    #        Game.screen.blit(self.colorgen[self.random_gen[i * MAP_SIZE + j - 1]], rect)
            pygame.display.update()
        pygame.quit()

    def Movement(self,originalsquare,nextsquare):
        if originalsquare != nextsquare:
            rect = self.game.map.colorgen[self.game.map.tiles[nextsquare[0]* MAP_SIZE + nextsquare[1] - 1].type].get_rect()
            rect.topleft = self.w / 2 + self.tilesize * originalsquare[0], self.tilesize * originalsquare[1]
            Game.screen.blit(self.game.map.colorgen[self.game.map.tiles[originalsquare[0] * MAP_SIZE + originalsquare[1] - 1].type], rect)
            rect = self.game.map.colorgen[self.game.map.tiles[originalsquare[0] * MAP_SIZE + originalsquare[1] - 1].type].get_rect()
            rect.topleft = self.w / 2 + self.tilesize * nextsquare[0], self.tilesize * nextsquare[1]
            Game.screen.blit(self.game.map.colorgen[self.game.map.tiles[nextsquare[0] * MAP_SIZE + nextsquare[1] - 1].type], rect)
            a = self.game.map.tiles[originalsquare[0] * MAP_SIZE + originalsquare[1] - 1].type
            self.game.map.tiles[originalsquare[0] * MAP_SIZE + originalsquare[1] - 1].type = self.game.map.tiles[nextsquare[0]* MAP_SIZE + nextsquare[1] - 1].type
            self.game.map.tiles[nextsquare[0] * MAP_SIZE + nextsquare[1] - 1].type = a
            self.swapped = False


class Game:
    def __init__(self):
        pygame.init()
        self.rect = Rect(0, 0, 1280, 720)
        self.config = RESIZABLE
        Game.screen = pygame.display.set_mode(self.rect.size, self.config)
        self.menu = Menu(self)

    def run(self):
        if self.menu.run() == "battle":
            self.battle = Battle(self)
            self.map = Map()
            self.contextWindow = ContextWindow()
            self.battle.run()

class Map:
    def __init__(self):
        self.w = Game.screen.get_width()
        self.random_gen = []
        self.tiles = []
        self.colorgen = [pygame.image.load("grass.png").convert(), pygame.image.load("grass.png").convert(),
                         pygame.image.load("grass.png").convert(), pygame.image.load("icelake.png").convert(),
                         pygame.image.load("sand.png").convert(), pygame.image.load("forest.png").convert(),
                         pygame.image.load("swamp.png").convert(), pygame.image.load("boulder.png").convert(),
                         pygame.image.load("snowy mountain.png").convert(), pygame.image.load("mountain.png").convert(),
                         pygame.image.load("lava.png").convert(), pygame.image.load("volcano.png").convert(),
                         pygame.image.load("water.png").convert(), pygame.image.load("water.png").convert(), ]
        self.generate_tiles()

    def generate_tiles(self):
        for i in range(MAP_SIZE**2):
            self.random_gen.append(random.randint(0,13))
        for i in range(len(self.random_gen)):
            #Des parametres afin d'empecher certains scenarios detrimentales au jeu et creer un map logique
            if self.random_gen[i] == 11:
                self.tilenextto(i,7,necessaryadjacentcolors=(10,None))
            if self.random_gen[i] == 10:
                self.tilenextto(i,9,None,(11,None))
            if self.random_gen[i] == 8:
                self.tilenextto(i,9,(10,11))
            if self.random_gen[i] == 9:
                self.tilenextto(i,10,(11,None),None)
            if self.random_gen[i] >=12:
                if self.tilenextto(i, 3, (8,None)):
                    None
                else :
                    self.tilenextto(i, 7, (10, 11))
            if self.random_gen[i] == 6:
                self.tilenextto(i,5,necessaryadjacentcolors=(12,13))
            if self.random_gen[i] == 5:
                if self.tilenextto(i,7,(10,11)):
                    None
                else :
                    self.tilenextto(i,6,(12,13))
            if self.random_gen[i] == 4:
                self.tilenextto(i, 2, necessaryadjacentcolors=(12,13))
            if self.random_gen[i] == 3:
                self.tilenextto(i, 2, (10, 11),(8,12,13))
            if self.random_gen[i] <= 2:
                self.tilenextto(i,4,(12,13))
        for i in range(len(self.random_gen)):
            #Vu que le programme va de tuile en tuile certains bugs peuvent se passer sur la generation il faut donc refaire le programme d'avant de maniere independante
            if self.random_gen[i] == 11:
                self.tilenextto(i,7,necessaryadjacentcolors=(10,None))
            if self.random_gen[i] == 10:
                self.tilenextto(i,9,None,(11,None))
            if self.random_gen[i] == 8:
                self.tilenextto(i,9,(10,11))
            if self.random_gen[i] == 9:
                self.tilenextto(i,10,(11,None),None)
            if self.random_gen[i] >=12:
                if self.tilenextto(i, 3, (8,None)):
                    None
                else :
                    self.tilenextto(i, 7, (10, 11))
            if self.random_gen[i] == 6:
                self.tilenextto(i,5,necessaryadjacentcolors=(12,13))
            if self.random_gen[i] == 5:
                if self.tilenextto(i,7,(10,11)):
                    None
                else :
                    self.tilenextto(i,6,(12,13))
            if self.random_gen[i] == 4:
                self.tilenextto(i, 2, necessaryadjacentcolors=(12,13))
            if self.random_gen[i] == 3:
                self.tilenextto(i, 2, (10, 11),(8,12,13))
            if self.random_gen[i] <= 2:
                self.tilenextto(i,4,(12,13))
        for i in range(MAP_SIZE):
            for j in range(1, MAP_SIZE + 1):
                self.tiles.append(Tile(self.random_gen[MAP_SIZE*i+j-1], (i, j)))
    def tilenextto(self,i,newcolor,illegaladjacentcolors = None,necessaryadjacentcolors = None):
        necessary = 0
        if necessaryadjacentcolors is None:
            necessary = 1
        if illegaladjacentcolors is not None:
            if i % MAP_SIZE != 0:
                if self.random_gen[i - 1] in illegaladjacentcolors:
                    self.random_gen[i] = newcolor
            if (i+1) % MAP_SIZE != 0:
                if self.random_gen[i + 1] in illegaladjacentcolors:
                    self.random_gen[i] = newcolor
            if i < MAP_SIZE ** 2 - MAP_SIZE :
                if self.random_gen[i + MAP_SIZE] in illegaladjacentcolors:
                    self.random_gen[i] = newcolor
            if i > MAP_SIZE - 1:
                if self.random_gen[i - MAP_SIZE] in illegaladjacentcolors:
                    self.random_gen[i] = newcolor
        if necessaryadjacentcolors is not None:
            if i % MAP_SIZE != 0:
                if self.random_gen[i - 1] in necessaryadjacentcolors:
                    necessary = 1
            if (i+1) % MAP_SIZE != 0:
                if self.random_gen[i + 1]  in necessaryadjacentcolors:
                    necessary = 1
            if i < MAP_SIZE ** 2 - MAP_SIZE :
                if self.random_gen[i + MAP_SIZE] in necessaryadjacentcolors:
                    necessary = 1
            if i > MAP_SIZE - 1:
                if self.random_gen[i - MAP_SIZE] in necessaryadjacentcolors:
                    necessary = 1
        if necessary == 0:
            self.random_gen[i] = newcolor
        if self.random_gen[i] == newcolor:
            return True

    def draw(self):
        for i in range(len(self.tiles)):
            img = self.colorgen[self.tiles[i].type]
            rect = img.get_rect()
            rect.topleft = self.w / 2 + rect.width * self.tiles[i].id[0], rect.height * self.tiles[i].id[1]
            Game.screen.blit(img, rect)

class Tile:
    def __init__(self,type,id):
        self.type = type
        self.id = id


class ContextWindow:
    def __init__(self):
        a = 1

class Team:
    def __init__(self):
        a = 1

    def setup_units(self):
        a = 1

class Unit:
    def __init__(self):
        a=1

class Turn:
    def __init__(self):
        a = 1

class Action:
    def __init__(self):
        a = 1

#class GlobalWindow:
#    def __init__(self):
#        a = 1

if __name__ == '__main__':
    g = Game()
    g.run()
