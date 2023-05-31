import pygame.math
# from pygame import *
from settings import *

# import program_class

vec = pygame.math.Vector2


class Player:

    def __init__(self, program, pos):
        self.program = program
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(1, 0)
        self.stored_dir = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        self.lives = 3

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed
        if self.time_to_move():
            if self.stored_dir is not None:
                self.direction = self.stored_dir
            self.able_to_move = self.can_move()

        # this is the setting of grid position in reference to pixel position
        self.grid_pos[0] = (self.pix_pos[
                                0] - TOP_BOTTOM_BUFFER + self.program.cell_width // 2) // self.program.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[
                                1] - TOP_BOTTOM_BUFFER + self.program.cell_height // 2) // self.program.cell_height + 1

        if self.on_coin():
            self.eat_coin()

    def draw(self):
        pygame.draw.circle(self.program.window, PLAYER_COLOR, (int(self.pix_pos.x), int(self.pix_pos.y)),
                           self.program.cell_width // 2 - 2)

        # drawing player lives
        for x in range(self.lives):
            pygame.draw.circle(self.program.window, PLAYER_COLOR, (30 + 20 * x, WINDOW_HEIGHT - 15), 7)

        # drawing the grid pos rect
        # pygame.draw.rect(self.program.window, RED, (self.grid_pos[0]*self.program.cell_width+TOP_BOTTOM_BUFFER//2,
        #                  self.grid_pos[1]*self.program.cell_height+TOP_BOTTOM_BUFFER//2,
        #                  self.program.cell_width, self.program.cell_height),1)

    def on_coin(self):
        if self.grid_pos in self.program.coins:
            if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.program.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                    return True
            if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.program.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                    return True
        return False

    def eat_coin(self):
        self.program.coins.remove(self.grid_pos)
        self.current_score += 1

    def get_pix_pos(self):
        pix = vec(
            (self.grid_pos.x * self.program.cell_width + TOP_BOTTOM_BUFFER // 2 + self.program.cell_width // 2),
            (self.grid_pos.y * self.program.cell_height) + TOP_BOTTOM_BUFFER // 2 + self.program.cell_height // 2)
        return pix

    def move(self, direction):
        self.stored_dir = direction

    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.program.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.program.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    def can_move(self):
        for wall in self.program.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True
