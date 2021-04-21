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

UNIT_BASE = "Base"
UNIT_WORKER = "Worker"
UNIT_INFANTRY = "Infantry"
UNIT_CAVALRY ='Cavalry'
UNIT_ARCHER = "Archer"
ACTION_END_TURN = "End Turn"
ACTION_ATTACK = "Attack"
ACTION_MOVE = "Move"
ACTION_CHARGE = "Charge"
ACTION_HARVEST = "Harvest"
MAP_SIZE = 12

class Text:
    #cree une classe permettant de modifier et utuliser du text 
    def __init__(self, text, x, y, font = 60, color = "black"):
        self.text = text
        self.pos = (x, y)
        self.fontname = None
        self.fontsize = font
        self.fontcolor = Color(color)
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
    
    def erase(self):
        pygame.draw.rect(Game.screen, Color('gray'), self.rect)

    def draw(self):
        Game.screen.blit(self.img, self.rect)

class Menu:
    #permet de creer et gerer le jeu et l'ecran
    def __init__(self):
        pygame.display.set_caption('Castillon')
        pygame.display.set_icon(pygame.image.load('grass.png'))
        self.title = Text('Castillon', 0, 20, 400, 'blue')
        self.title.pos = (Game.screen.get_width()/2 - self.title.rect.width / 2, 20)
        self.title.set_font()
        self.title.render()
        self.starter = Text('Start', 20, Game.screen.get_height()/2, 100)
        
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
        self.currentaction = ''
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
        self.unit_types.append(UnitType(UNIT_BASE, 5, 0, 0, 0,(0,0,0),None,None))
        self.unit_types.append(UnitType(UNIT_INFANTRY, 3, 1, 1, 1,(0,1,2),None,None))
        self.unit_types.append(UnitType(UNIT_WORKER, 2, 1, 0, 0,(1,1,0),None,ACTION_HARVEST))
        self.unit_types.append(UnitType(UNIT_CAVALRY, 3, 3, 1, 1,(1,1,2),None,ACTION_CHARGE))
        self.unit_types.append(UnitType(UNIT_ARCHER, 2, 1, 3, 1,(1,1,1),None,None))
    
    def team_setup(self):
        self.teams = []
        self.teams.append(Team("Red",'red'))
        self.teams[0].units.append(Unit(self.teams[0], self.unit_types[0], self.map.find_tile(6,0)))
        self.teams[0].units.append(Unit(self.teams[0], self.unit_types[1], self.map.find_tile(6,2)))
        self.teams[0].units.append(Unit(self.teams[0], self.unit_types[1], self.map.find_tile(3,1)))
        self.teams[0].units.append(Unit(self.teams[0], self.unit_types[1], self.map.find_tile(9,1)))
        self.teams[0].units.append(Unit(self.teams[0], self.unit_types[3], self.map.find_tile(7,2)))
        self.teams.append(Team("Blue",'blue'))
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
                        self.game.turn.action.tileselectiondraw(self.game.turn.action.moveablespaces)
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
                    if self.action != True :
                        for i in range(MAP_SIZE):
                            for j in range(1, MAP_SIZE + 1):
                                if Rect((Game.screen.get_width() / 2) + self.tilesize * i, self.tilesize * j, self.tilesize, self.tilesize).collidepoint(event.__getattribute__('pos')):
                                    pygame.draw.rect(Game.screen, Color('red'), Rect((Game.screen.get_width() / 2) + self.tilesize * i, self.tilesize * j, self.tilesize, self.tilesize), 1)
                                    self.currentsquare = (i,j)
                                    self.action = False
                                    self.game.contextWindow.set_description(i*MAP_SIZE+j-1)
                                    self.game.contextWindow.draw()
                                    break
                                
                        if self.game.turn.action.action_buttons != None:
                            for i in range(len(self.game.turn.action.action_buttons)):
                                if self.game.turn.action.action_buttons[i].rect.collidepoint(event.__getattribute__('pos')):
                                    self.game.turn.action.take_action(self.game.turn.action.available_actions[i],self.game.contextWindow.chosen_unit)
                                    self.currentaction = self.game.turn.action.available_actions[i]
                        if self.currentsquare != None:
                                    pygame.draw.rect(Game.screen, Color('red'), Rect((Game.screen.get_width() / 2) + self.tilesize * self.currentsquare[0], self.tilesize * self.currentsquare[1], self.tilesize, self.tilesize), 1)
                         
                    if self.action:
                        for i in range(MAP_SIZE):
                            for j in range(1, MAP_SIZE + 1):
                                if Rect((Game.screen.get_width() / 2) + self.tilesize * i, self.tilesize * j, self.tilesize, self.tilesize).collidepoint(event.__getattribute__('pos')):
                                    if self.game.map.find_tile(i,j-1) in self.game.turn.action.moveablespaces:
                                        if self.currentaction == ACTION_MOVE:
                                            self.game.turn.action.movement(self.game.map.find_tile(i,j-1),self.game.turn.action.tile)
                                        if self.currentaction == ACTION_ATTACK:
                                            a = 1
                                    else:
                                        self.action = False
                                        self.currentaction = None
                                        self.game.turn.action.moveablespaces = []
                            
                if event.type == MOUSEBUTTONUP :
                    for i in range(MAP_SIZE) :
                        for j in range(1, MAP_SIZE+1):
                            if Rect((Game.screen.get_width() / 2) + self.tilesize * i, self.tilesize * j, self.tilesize, self.tilesize).collidepoint(event.__getattribute__('pos')):
                                a = 1
                    self.clicking = False
                if event.type == WINDOWMAXIMIZED:
                    Game.screen.fill(Color('gray'))
                    self.game.contextWindow.draw()
                    self.game.map.draw()
                    self.game.turn.action.tileselectiondraw(self.game.turn.action.moveablespaces)
                    self.game.turn.action.draw_window(self.game.turn.current_team)
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
                    self.game.turn.action.tileselectiondraw(self.game.turn.action.moveablespaces)
                    self.game.turn.action.draw_window(self.game.turn.current_team)
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
            if i >= MAP_SIZE :
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
            self.resource_type = "Wood:"
            self.resources = str(random.randint(1,3))
        elif self.type == 7:
            self.resource_type = "Rock:"
            self.resources = str(random.randint(1,2))
        elif self.type == 9:
            self.resource_type = "Metal:"
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
            img = pygame.image.load(self.unit.team.color + str(self.unit.unit_type.name)+'.png')
            rect = img.get_rect()
            rect.topleft = Game.screen.get_width() / 2 + rect.width * self.x, rect.height * (self.y + 1)
            img.set_colorkey(Color('black'))
            Game.screen.blit(img, rect)


class ContextWindow:
    def __init__(self,game):
        self.game = game
        self.title_entries = ["Grass","Grass","Grass","Icy Lake","Sand","Forest","Swamp","Boulder","Snowy Mountain","Mountain","Lava","Volcano","Water",'Water']
        self.textentries = ["A good place to settle","A good place to settle","A good place to settle","Warmer clothes are needed to survive here","Nothing useful here","A source of wood","A good place to hide","Ideal for a quarry","Cold and desolate","Difficult to traverse","Hot and dangerous","An active hasard","A boat is needed to traverse this",'A boat is needed to traverse this']
        self.clickableinfo = 0
        self.clickabledescription = 0
        self.info = Text("", 40, 152)
        self.description = Text("", 40, 152)
        self.resourcename = Text("", 40, 188)
        self.resources = Text("", 40, 188)
        self.actions = []
        self.chosen_unit = None
        self.unit_text = Text("", 40, 152)
        self.unit_life = Text("", 40, 152)

    def set_description(self, tilenb):
        self.actions.clear()
        self.clickableinfo = self.title_entries[self.game.map.tiles[tilenb].type]
        self.clickabledescription = self.textentries[self.game.map.tiles[tilenb].type]
        self.resourcetext = self.game.map.tiles[tilenb].resource_type
        self.resourcenb = self.game.map.tiles[tilenb].resources
        self.chosen_unit = self.game.map.tiles[tilenb].unit
        # This unit can play this turn
        if self.chosen_unit != None and self.chosen_unit.team == self.game.turn.current_team:
            for action in self.chosen_unit.actions:
                self.actions.append(action)

    def draw(self):
        # Terrain
        self.info.erase()
        self.info = Text("Terrain = " +  self.clickableinfo, 40, 120)
        self.info.draw()
        self.description.erase()
        self.description = Text(self.clickabledescription, 40, 192, 40)
        self.description.draw()
        self.resourcename.erase()
        self.resourcename = Text(self.resourcetext, 40, 228, 40) 
        self.resourcename.draw()
        self.resources.erase()
        self.resources = Text(self.resourcenb, 50+self.resourcename.rect.width, 228, 40)
        self.resources.draw()

        # Unit
        self.unit_text.erase()
        self.unit_life.erase()
        if self.chosen_unit != None:
            self.unit_text = Text("Unit = " + self.chosen_unit.team.name + "'s " + self.chosen_unit.unit_type.name, 40, 270, 60, self.chosen_unit.team.color)
            self.unit_text.draw()
            self.unit_life = Text("Life = " + str(self.chosen_unit.life), 40, 330, 40)
            self.unit_life.draw()

        # Actions
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
        self.life = unit_type.max_life
        self.tile = tile
        self.actions = unit_type.actions
        tile.unit = self

class UnitType:
    def __init__(self, name, max_life, move, range, hits, cost, spawn_types, special_actions):
        self.name = name
        self.max_life = max_life
        self.move = move
        self.range = range
        self.hits = hits
        self.spawn_types = spawn_types
        self.special_actions = special_actions
        self.actions = []
        if self.move != 0:
            self.actions.append(ACTION_MOVE)
        if self.hits != 0:
            self.actions.append(ACTION_ATTACK)
        if self.special_actions != None:
            self.actions.append(self.special_actions)

class Turn:
    def __init__(self, game):
        self.game = game
        self.action = Action(game, self)
        self.current_team = game.battle.teams[0]
        self.action.draw_window(self.current_team)
        
    def change_turn(self):
        if self.current_team == self.game.battle.teams[0]:
            self.current_team = self.game.battle.teams[1]
        else:
            self.current_team = self.game.battle.teams[0]
        self.action.draw_window(self.current_team)

class Action:
    def __init__(self, game, turn):
        self.game = game
        self.turn = turn
        self.turn_indicator = Text('', 40, 20)
        self.available_actions = []
        self.action_buttons = []    
        self.first_turn()
        self.moveablespaces = []
    
    def draw_window(self, team):
        pygame.draw.rect(Game.screen, Color('gray'), self.turn_indicator.rect )
        self.turn_indicator = Text(team.name + "'s turn", 40, 20, 80)
        self.turn_indicator.fontcolor = Color(team.color)
        self.turn_indicator.set_font()
        self.turn_indicator.render()
        self.turn_indicator.draw()
    
    def draw_buttons(self, actions):
        self.actions = actions
        
        if self.firstturn == False:
            self.available_actions.clear()
            for i in range (len(self.actions)):
                self.available_actions.append(self.actions[i])
            self.available_actions.append(ACTION_END_TURN)
        if self.action_buttons != None:
            for actionbutton in self.action_buttons:
                actionbutton.erase()
        self.action_buttons.clear()
        for i in range (len(self.available_actions)):
            self.action_buttons.append(Text(self.available_actions[i], 40, 404+56*i))
            pygame.draw.rect(Game.screen, Color('light blue'), self.action_buttons[i].rect )
            self.action_buttons[i].draw()
            
    def first_turn(self):
        self.firstturn = False
        self.available_actions.append('place base') 
        #self.draw_buttons(None)

    def take_action(self,action,unit):
        if action == ACTION_MOVE:
            self.movselect(unit)
        if action == ACTION_ATTACK:
            self.atkselect(unit)
        if action == ACTION_END_TURN:
            self.endturn()

    def movselect(self,unit):
        self.movrange = unit.unit_type.move
        self.tile = unit.tile
        self.x = unit.tile.x
        self.y = unit.tile.y
        self.moveablespaces = [self.tile]
        self.tempmovspaces = []
        for i in range (self.movrange):
            for tile in self.moveablespaces:
                if tile.x < MAP_SIZE:
                    if self.game.map.find_tile(tile.x+1,tile.y) not in  self.tempmovspaces:
                        self.tempmovspaces.append(self.game.map.find_tile(tile.x+1,tile.y))
                if tile.x > 0:
                    if self.game.map.find_tile(tile.x-1,tile.y) not in  self.tempmovspaces:
                        self.tempmovspaces.append(self.game.map.find_tile(tile.x-1,tile.y))
                if tile.y < MAP_SIZE  :
                    if self.game.map.find_tile(tile.x,tile.y+1) not in  self.tempmovspaces:
                        self.tempmovspaces.append(self.game.map.find_tile(tile.x,tile.y+1))
                if tile.y > 0:
                    if self.game.map.find_tile(tile.x,tile.y-1) not in  self.tempmovspaces:
                        self.tempmovspaces.append(self.game.map.find_tile(tile.x,tile.y-1))
            for tile in self.tempmovspaces:
                self.moveablespaces.append(tile)
            self.tempmovspaces.clear()
        self.moveablespaces.remove(self.tile)
        self.tileselectiondraw(self.moveablespaces)
        self.game.battle.action = True
    def tileselectiondraw(self,tiles):
        for tile in tiles:
            img = Battle.colorgen[12].copy()
            alpha = 60
            img.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
            rect = img.get_rect()
            rect.topleft = Game.screen.get_width() / 2 + rect.width * tile.x, rect.height * (tile.y + 1)
            Game.screen.blit(img, rect)
    def atkselect(self,unit): 
        a = 1

    def movement(self,new_tile,old_tile):
        new_tile.unit = old_tile.unit
        old_tile.unit = None
        self.moveablespaces = []
        self.game.contextWindow.set_description(new_tile.x*MAP_SIZE+new_tile.y)
        self.game.contextWindow.draw()
        self.game.map.draw()

    def attack(self):
        a=1
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
