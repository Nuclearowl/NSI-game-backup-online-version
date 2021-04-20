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

BASE = "base"
UNIT_WORKER = "worker"
UNIT_INFANTRY = "infantry"
UNIT_CAVALRY ='cavalry'
UNIT_ARCHERS = "archer"
MAP_SIZE = 12

class Text:
    #cree une classe permettant de modifier et utuliser du text 
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
    def __init__(self):
        pygame.display.set_caption('Castillon')
        pygame.display.set_icon(pygame.image.load('grass.png'))
        self.title = Text('Castillon', pos=(0, 20))
        self.title.fontsize = 400
        self.title.fontcolor = Color('blue')
        self.title.set_font()
        self.title.render()
        self.title.pos = (Game.screen.get_width()/2 - self.title.rect.width / 2, 20)
        self.title.set_font()
        self.title.render()

        self.starter = Text('Start', pos=(20, Game.screen.get_height()/2))
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
    def __init__(self,game):
        self.game = game
        self.map = self.game.map
        self.screen_flip()
        self.tile_load()
        self.unit_types_setup()
        self.team_setup()

       #variables utiles plus tard
        self.tilesize = 600/MAP_SIZE
        self.clicking = True
        self.action = False
        self.currentsquare = None
        self.nextsquare = (0,0)
        
    def screen_flip(self):
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

    def tile_load(self):
        Battle.colorgen = [pygame.image.load("grass.png").convert(),pygame.image.load("grass.png").convert(),
                         pygame.image.load("grass.png").convert(),pygame.image.load("icelake.png").convert(),
                         pygame.image.load("sand.png").convert(),pygame.image.load("forest.png").convert(),
                         pygame.image.load("swamp.png").convert(),pygame.image.load("boulder.png").convert(),
                         pygame.image.load("snowy mountain.png").convert(),pygame.image.load("mountain.png").convert(),
                         pygame.image.load("lava.png").convert(),pygame.image.load("volcano.png").convert(),
                         pygame.image.load("water.png").convert_alpha(),pygame.image.load("water.png").convert(), ]
        Battle.blueunitimgs = [pygame.image.load("bluebase.png").convert(),pygame.image.load("bluecavalry.png").convert(),
        pygame.image.load("blueinfantry.png").convert()]
        Battle.redunitimgs = [pygame.image.load("redbase.png").convert(),pygame.image.load("redcavalry.png").convert(),
        pygame.image.load("redinfantry.png").convert()]
            #liste des images pertinentes sur ces tuiles/unites
        
        
    def unit_types_setup(self):
        self.unit_types = []
        self.unit_types.append(UnitType(BASE, 5, 0, 0, 0,(0,0,0),None,None))
        self.unit_types.append(UnitType(UNIT_INFANTRY, 3, 1, 1, 1,(0,1,2),None,None))
        self.unit_types.append(UnitType(UNIT_WORKER, 2, 1, 0, 0,(1,1,0),None,'harvest'))
        self.unit_types.append(UnitType(UNIT_CAVALRY, 3, 3, 1, 1,(1,1,2),None,'charge'))
        self.unit_types.append(UnitType(UNIT_ARCHERS, 2, 1, 3, 1,(1,1,1),None,None))
    
    def team_setup(self):
        self.teams = []
        self.teams.append(self.game.red)
        self.teams[0].units.append(Unit(self.teams[0], self.unit_types[0], self.map.find_tile(6,0)))
        self.teams[0].units.append(Unit(self.teams[0], self.unit_types[1], self.map.find_tile(6,2)))
        self.teams[0].units.append(Unit(self.teams[0], self.unit_types[1], self.map.find_tile(3,1)))
        self.teams[0].units.append(Unit(self.teams[0], self.unit_types[1], self.map.find_tile(9,1)))
        self.teams[0].units.append(Unit(self.teams[0], self.unit_types[3], self.map.find_tile(7,2)))
        self.teams.append(self.game.blue)
        self.teams[1].units.append(Unit(self.teams[1], self.unit_types[0], self.map.find_tile(5,11)))
        self.teams[1].units.append(Unit(self.teams[1], self.unit_types[1], self.map.find_tile(5,9)))
        self.teams[1].units.append(Unit(self.teams[1], self.unit_types[1], self.map.find_tile(2,10)))
        self.teams[1].units.append(Unit(self.teams[1], self.unit_types[1], self.map.find_tile(8,10)))
        
        
    def run(self):
        self.map.draw()
        Battle.running = True
        while Battle.running:
            #Prend tous les evenements du joueur
            for event in pygame.event.get():
                if event.type == QUIT:
                    #Permet de quitter l'application
                    Battle.running = False
                if event.type == MOUSEMOTION :
                        self.map.draw()
                        if self.currentsquare != None :
                            pygame.draw.rect(Game.screen, Color('red'), Rect((Game.screen.get_width() / 2) + self.tilesize * self.currentsquare[0], self.tilesize * self.currentsquare[1], self.tilesize, self.tilesize), 1)
                        # for i in range(MAP_SIZE):
                        #     for j in range(1, MAP_SIZE + 1):
                        #         pygame.draw.rect(Game.screen, Color('gray'), Rect((self.w / 2) + self.tilesize * i, self.tilesize * j, self.tilesize, self.tilesize), 1)
                        #         rect = self.colorgen[self.random_gen[i * MAP_SIZE + j - 1]].get_rect()
                        #         rect.topleft = self.w / 2 + self.tilesize * i, self.tilesize * j
                        #         Game.screen.blit(self.colorgen[self.random_gen[i * MAP_SIZE + j - 1]], rect)

                        for i in range(MAP_SIZE):
                            for j in range(1, MAP_SIZE + 1):
                                if Rect((Game.screen.get_width() / 2) + self.tilesize * i, self.tilesize * j, self.tilesize, self.tilesize).collidepoint(event.__getattribute__('pos')):
                                    break
                if event.type == MOUSEBUTTONDOWN :
                    self.clicking = True
                    self.map.draw()
                    if self.action !=True:
                        for i in range(MAP_SIZE):
                            for j in range(1, MAP_SIZE + 1):
                                if Rect((Game.screen.get_width() / 2) + self.tilesize * i, self.tilesize * j, self.tilesize, self.tilesize).collidepoint(event.__getattribute__('pos')):
                                    pygame.draw.rect(Game.screen, Color('red'), Rect((Game.screen.get_width() / 2) + self.tilesize * i, self.tilesize * j, self.tilesize, self.tilesize), 1)
                                    self.currentsquare = (i,j)
                                    break
                                
                        if self.game.turn.action.actionsbuttons != None:
                            for i in range(len(self.game.turn.action.actionsbuttons)):
                                if self.game.turn.action.actionsbuttons[i].rect.collidepoint(event.__getattribute__('pos')):
                                    self.game.turn.action.takeaction(self.game.turn.action.available_actions[i],self.game.contextWindow.chosenunit)
                        if self.currentsquare != None:
                                    pygame.draw.rect(Game.screen, Color('red'), Rect((Game.screen.get_width() / 2) + self.tilesize * self.currentsquare[0], self.tilesize * self.currentsquare[1], self.tilesize, self.tilesize), 1)

                if event.type == MOUSEBUTTONUP :
                    for i in range(MAP_SIZE) :
                        for j in range(1, MAP_SIZE+1):
                            if Rect((Game.screen.get_width() / 2) + self.tilesize * i, self.tilesize * j, self.tilesize, self.tilesize).collidepoint(event.__getattribute__('pos')):
                                self.game.contextWindow.set_description(i*MAP_SIZE+j-1)
                                self.game.contextWindow.draw()
                    self.clicking = False
                if event.type == WINDOWMAXIMIZED:
                    Game.screen.fill(Color('gray'))
                    self.game.contextWindow.draw()
                    self.game.map.draw()
                    self.game.turn.action.draw_window(self.game.turn.currentturn)
                    pygame.draw.rect(Game.screen, Color('red'), Rect((Game.screen.get_width() / 2) + self.tilesize * self.currentsquare[0], self.tilesize * self.currentsquare[1], self.tilesize, self.tilesize), 1)
                    #for i in range(MAP_SIZE):
                    #    for j in range(1, MAP_SIZE+1):
                    #        rect = self.colorgen[self.random_gen[i * MAP_SIZE + j - 1]].get_rect()
                    #        rect.topleft = self.w / 2 + self.tilesize * i, self.tilesize * j
                    #        Game.screen.blit(self.colorgen[self.random_gen[i * MAP_SIZE + j - 1]], rect)
                if event.type == WINDOWRESIZED:
                    Game.screen.fill(Color('gray'))
                    self.game.contextWindow.draw()
                    self.game.map.draw()
                    self.game.turn.action.draw_window(self.game.turn.currentturn)
                    pygame.draw.rect(Game.screen, Color('red'), Rect((Game.screen.get_width() / 2) + self.tilesize * self.currentsquare[0], self.tilesize * self.currentsquare[1], self.tilesize, self.tilesize), 1)
                    #for i in range(MAP_SIZE):
                    #    for j in range(1, MAP_SIZE+1):
                    #        rect = self.colorgen[self.random_gen[i * MAP_SIZE + j - 1]].get_rect()
                    #        rect.topleft = self.w / 2 + self.tilesize * i, self.tilesize * j
                    #        Game.screen.blit(self.colorgen[self.random_gen[i * MAP_SIZE + j - 1]], rect)
            pygame.display.update()
        pygame.quit()



class Game:
    def __init__(self):
        pygame.init()
        self.rect = Rect(0, 0, 1280, 720)
        self.config = RESIZABLE
        Game.screen = pygame.display.set_mode(self.rect.size, self.config)
        self.menu = Menu()

    def run(self):
        if self.menu.run() == "battle":               
            self.red = Team("red",'red')
            self.blue = Team("blue",'blue') 
            self.map = Map()
            self.contextWindow = ContextWindow(self)
            self.battle = Battle(self)
            self.turn = Turn(self) 
            self.battle.run()
            
class Map:
    def __init__(self):
        self.random_gen = []
        self.tiles = []
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
            for j in range(MAP_SIZE):
                self.tiles.append(Tile(self.random_gen[MAP_SIZE*i + j], i, j))

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

    def find_tile(self, x, y):
        return self.tiles[MAP_SIZE*x + y]
    
    def draw(self):
        for i in self.tiles:
            i.draw()

class Tile:
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y
        if self.type == 5:
            self.resource_type = "wood:"
            self.resources = str(random.randint(1,3))
        elif self.type == 7:
            self.resource_type = "rock:"
            self.resources = str(random.randint(1,2))
        elif self.type == 9:
            self.resource_type = "metal:"
            self.resources = "1"
        else:
            self.resource_type = ""
            self.resources = ""
        self.unit = None

    def draw(self):
        # Terrain
        img = Battle.colorgen[self.type]
        rect = img.get_rect()
        rect.topleft = Game.screen.get_width() / 2 + rect.width * self.x, rect.height * (self.y + 1)
        Game.screen.blit(img, rect)

        # Unit?
        if self.unit:
            if self.unit.team.name == 'red':
                img = pygame.image.load('red'+str(self.unit.unit_type.name)+'.png')
            else:
                img = pygame.image.load('blue'+str(self.unit.unit_type.name)+'.png')
            rect = img.get_rect()
            rect.topleft = Game.screen.get_width() / 2 + rect.width * self.x, rect.height * (self.y + 1)
            img.set_colorkey(Color('black'))
            Game.screen.blit(img, rect)


class ContextWindow:
    def __init__(self,game):
        self.game = game
        self.title_entries = ["grass","grass","grass","ice","sand","forest","swamp","boulder","snowy mountain","mountain","lava","volcano","water",'water']
        self.textentries = ["a good place to settle","a good place to settle","a good place to settle","warmer clothes are needed to survive here","nothing usefull here","a source of wood","a good place to hide","ideal for a quarry","cold and desolate","difficult to traverse","hot and dangerous","an active hasard","a boat is needed to traverse this",'a boat is needed to traverse this']
        self.clickableinfo = 0
        self.clickabledescription = 0
        self.info = Text("", pos=(40, 152))
        self.description = Text("", pos=(40, 152))
        self.resourcename = Text("", pos=(40, 188))
        self.resources = Text("", pos=(40, 188))
        self.actions = []
        self.chosenunit = None
        

    def set_description(self, tilenb):
        self.actions.clear()
        self.clickableinfo = self.title_entries[self.game.map.tiles[tilenb].type]
        self.clickabledescription = self.textentries[self.game.map.tiles[tilenb].type]
        self.resourcetext = self.game.map.tiles[tilenb].resource_type
        self.resourcenb = self.game.map.tiles[tilenb].resources
        if self.game.map.tiles[tilenb].unit != None:
            self.chosenunit = self.game.map.tiles[tilenb].unit
            for action in self.chosenunit.actions:
                self.actions.append(action)

    def draw(self):
        pygame.draw.rect(Game.screen, Color('gray'), self.info.rect)
        pygame.draw.rect(Game.screen, Color('gray'), self.description.rect )
        pygame.draw.rect(Game.screen, Color('gray'), self.resourcename.rect )
        pygame.draw.rect(Game.screen, Color('gray'), self.resources.rect )
        self.info = Text(self.clickableinfo, pos=(40,120))
        self.description = Text(self.clickabledescription, pos=(40, 192))
        self.resourcename = Text(self.resourcetext, pos =(40,228)) 
        self.resources = Text(self.resourcenb, pos =(50+self.resourcename.rect.width,228))
        self.description.fontsize = 36
        self.description.set_font()
        self.description.render()
        self.resourcename.fontsize = 36
        self.resourcename.set_font()
        self.resourcename.render()
        self.resources.fontsize = 36
        self.resources.set_font()
        self.resources.render()
        self.description.draw()
        self.info.draw()
        self.resourcename.draw()
        self.resources.draw()
        self.game.turn.action.draw_buttons(self.actions)

        
class Team:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.units = []

class Unit:
    def __init__(self, team, unit_type, tile):
        self.team = team
        self.unit_type = unit_type
        self.life = unit_type.life
        self.tile = tile
        self.actions = unit_type.actions
        tile.unit = self

class UnitType:
    def __init__(self, name, life, move, range, hits,cost,spawn_types,specialactions):
        self.name = name
        self.life = life
        self.move = move
        self.range = range
        self.hits = hits
        self.spawn_types = spawn_types
        self.specialactions = specialactions
        self.actions = []
        if self.move != 0:
            self.actions.append("move")
        if self.hits != 0:
            self.actions.append("attack")
        if self.specialactions != None:
            self.actions.append(self.specialactions)

class Turn:
    def __init__(self,game):
        self.action = Action(game,self)
        self.currentturn = 0
        self.action.draw_window(self.currentturn)
    def change_turn(self):
        if self.currentturn == 0:
            self.currentturn = 1
        else:
            self.currentturn =0
        self.action.draw_window(self.currentturn)

        


class Action:
    def __init__(self,game,turn):
        self.game = game
        self.turn = turn
        self.turn_indicator = Text('',pos = (40,20))
        self.available_actions = []
        self.actionsbuttons = []    
        self.first_turn()
    
    def draw_window(self,turn):
        pygame.draw.rect(Game.screen, Color('gray'), self.turn_indicator.rect )
        if turn == 1 :
            self.turn_indicator = Text("blue's turn",pos = (40,20))
        if turn == 0 :
            self.turn_indicator = Text("red's turn",pos = (40,20))
        self.turn_indicator.draw()
    
    def draw_buttons(self,actions):
        self.actions = actions
        
        if self.firstturn == False:
            self.available_actions.clear()
            for i in range (len(self.actions)):
                self.available_actions.append(self.actions[i])
            self.available_actions.append('end turn')
        if self.actionsbuttons != None:
            for actionbutton in self.actionsbuttons:
                pygame.draw.rect(Game.screen, Color('gray'), actionbutton.rect )
        self.actionsbuttons.clear()
        for i in range (len(self.available_actions)):
            self.actionsbuttons.append(Text(self.available_actions[i], pos =(40,264+56*i)) )
            pygame.draw.rect(Game.screen, Color('light blue'), self.actionsbuttons[i].rect )
            self.actionsbuttons[i].draw()
            
    def first_turn(self):
        self.firstturn = False
        self.available_actions.append('place base') 
        #self.draw_buttons(None)

    def takeaction(self,action,unit):
        if action == 'move':
            self.movement(unit)
        if action == 'attack':
            self.attack(unit)
        if action == 'end turn':
            self.endturn()
    def movement(self,unit):
        self.movrange = unit.unit_type.move
        self.x = unit.tile.x
        self.y = unit.tile.y
        self.moveablespaces = []
        for i in range (-self.movrange,self.movrange+1):
            if i> 0:
                for j in range (self.movrange):
                    if self.game.map.find_tile(self.x+self.movrange-i-j,self.y+i) not in self.moveablespaces :
                        self.moveablespaces.append(self.game.map.find_tile(self.x+self.movrange-i-j,self.y+i))

                    if self.game.map.find_tile(self.x+i,self.y+self.movrange-i-j) not in self.moveablespaces :
                        self.moveablespaces.append(self.game.map.find_tile(self.x + i,self.y + self.movrange - i-j))
            if i < 0:
                for j in range (self.movrange):
                    if self.game.map.find_tile(self.x-self.movrange-i-j,self.y+i) not in self.moveablespaces :
                        self.moveablespaces.append(self.game.map.find_tile(self.x-self.movrange-i-j,self.y+i))

                    if self.game.map.find_tile(self.x+i,self.y-self.movrange-i-j) not in self.moveablespaces :
                        self.moveablespaces.append(self.game.map.find_tile(self.x + i,self.y - self.movrange  i-j))
        self.tileselectiondraw(self.moveablespaces)
    def tileselectiondraw(self,tiles):
        for tile in tiles:
            img = Battle.colorgen[12].copy()
            alpha = 60
            img.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
            rect = img.get_rect()
            rect.topleft = Game.screen.get_width() / 2 + rect.width * tile.x, rect.height * (tile.y + 1)
            Game.screen.blit(img, rect)
    def attack(self,unit): 
        a = 1

    def placebase(self):
        s = 1

    def endturn(self):
        self.turn.change_turn()


#class GlobalWindow:
#    def __init__(self):
#        a = 1

if __name__ == '__main__':
    g = Game()
    g.run()
