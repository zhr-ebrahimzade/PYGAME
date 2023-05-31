import sys
import pygame
import copy
from settings import *
from player import *
from Enemy import *

class Program:

    pygame.init()
    vec = pygame.math.Vector2  # for 2-D surface

    def __init__(self):
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()  # to control the frames per second( to keep track of time)
        self.running = True
        self.state = "Start"
        self.cell_width = MAZE_WIDTH // COLUMNS
        self.cell_height = MAZE_HEIGHT // ROWS
        self.walls = []
        self.coins=[]
        self.enemies=[]
        self.enemy_pos = []
        self.player_pos=None
        self.load()
        self.player=Player(self,vec(self.player_pos))
        self.make_enemies()



    def run(self):
        while self.running:
            if self.state == "Start":
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == "playing":
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == "game over":
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            else:  # so the game doesn't crash
                self.running = False
            self.clock.tick(FPS)  # This can be used to help limit the runtime speed of a game

        pygame.quit()
        sys.exit()

    # ############################################ HELP FUNCTIONS #########################################

    def draw_text(self, words, screen,pos, size,color,font_name, centered=False, custom_font=False):
        if custom_font:
            custom_font = pygame.font.Font(font_name, size)
            text = custom_font.render(words, True, color)
            text_size=text.get_size()
        else:
            system_font = pygame.font.SysFont(font_name, size)
            text = system_font.render(words, True, color)
            text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0]//2
            pos[1] = pos[1] - text_size[1]//2
            self.window.blit(text, pos)

    def load(self):
        self.start_maze = pygame.image.load("images\\start_maze.jpg")
        self.start_maze = pygame.transform.scale(self.start_maze, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background = pygame.image.load("images\\maze.png")
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))


        # we are opening walls file
        # we are creating walls list with cordinate of walls
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))
                    elif char == "C":
                        self.coins.append(vec(xidx, yidx))
                    elif char == "P":
                        self.player_pos = [xidx, yidx]
                    elif char in ["2", "3", "4", "5"]:
                        self.enemy_pos.append([xidx, yidx])
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (xidx*self.cell_width, yidx*self.cell_height,
                                                                  self.cell_width, self.cell_height))

        print(self.walls)
    def make_enemies(self):
        for idx,pos in enumerate(self.enemy_pos):
            self.enemies.append(Enemy(self,vec(pos),idx))

    def draw_grid(self):
        for x in range(WINDOW_WIDTH//self.cell_width):
            pygame.draw.line(self.background, YELLOW, (x * self.cell_width, 0), (x * self.cell_width, WINDOW_HEIGHT))
        for x in range(WINDOW_HEIGHT // self.cell_height):
            pygame.draw.line(self.background, YELLOW, (0, x * self.cell_height), (WINDOW_WIDTH, x * self.cell_height))
        # for coin in self.coins:
        #     pygame.draw.rect(self.background,YELLOW,(coin.x*self.cell_width,
        #                      coin.y*self.cell_height,self.cell_width,self.cell_height))

    def reset(self):
        self.player.lives = 3
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        self.coins = []
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
        self.state = "playing"
    # ############################################ START FUNCTIONS #########################################
    def start_events(self):
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                self.running = False
            if events.type == pygame.KEYDOWN or events.type == pygame.K_SPACE:
                self.state = "playing"

    def start_update(self):
        pass

    def start_draw(self):
        self.window.fill(BLACK)
        self.window.blit(self.start_maze, (0, WINDOW_HEIGHT // 2 + 50))
        self.draw_text("PAC-MAN",self.window,[WINDOW_WIDTH//2,WINDOW_HEIGHT//2], PAC_MAN,WHITE,PAC_MAN_FONT, centered=True, custom_font=True)
        # self.draw_text("HIGHEST SCORE ",self.window,[300,40], HIGHEST_SCORE,WHITE,PAC_MAN_FONT, centered=True, custom_font=True)

        pygame.display.set_caption("PAC_MAN Start")
        pygame.display.update()

    # ############################################ PLAYING FUNCTIONS #########################################
    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type== pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    self.player.move(vec(-1,0))  # one step back is minus
                if event.key==pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key==pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key==pygame.K_DOWN:
                    self.player.move(vec(0, 1))
    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

    def playing_draw(self):

        self.window.fill(BLACK)
        self.window.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.draw_coins()
        #self.draw_grid()
        self.draw_text("CURRENT SCORE: {}".format(self.player.current_score),self.window,[120 ,15],16,GRAY,"arial", centered=True, custom_font=False)
        self.draw_text("HIGHEST SCORE: ",self.window,[450 ,15],16,GRAY,"arial", centered=True, custom_font=False)
        pygame.display.set_caption("PAC_MAN playing")
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()
    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = "game over"
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0


    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.window,COIN_COLOR,(int(coin.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,
                                                int(coin.y*self.cell_height)+self.cell_width//2+TOP_BOTTOM_BUFFER//2),5)

# ############################################ GAME OVER FUNCTIONS #########################################
    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_update(self):
        pass

    def game_over_draw(self):
        self.window.fill(BLACK)
        quit_text = "Press the escape button to QUIT"
        again_text = "Press SPACE bar to PLAY AGAIN"
        self.draw_text("GAME OVER", self.window,[WINDOW_WIDTH//2, 100], 52,WHITE,"arial", centered=True, custom_font=False)
        self.draw_text(again_text, self.window, [
                       WINDOW_WIDTH//2, WINDOW_HEIGHT//2],  36, (255, 212, 128), "arial", centered=True, custom_font=False)
        self.draw_text(quit_text, self.window, [
                       WINDOW_WIDTH//2, WINDOW_HEIGHT//1.5],  36, (255, 212, 128), "arial", centered=True,custom_font=False)
        pygame.display.update()