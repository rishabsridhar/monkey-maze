import pygame
import game_logic
import time
from levels import get_level

_FRAME_RATE = 60
_DELAY = 500

_INIT_WIDTH = (game_logic._WIDTH+2) * 20 * 2
_INIT_HEIGHT = (game_logic._HEIGHT+2) * 20 * 2
_SIZE = (_INIT_WIDTH, _INIT_HEIGHT)
_RED = (255,0,0)
_GREEN = (0,255,0)
_BLUE = (0,0,255)

class MonkeyMaze:

    def __init__(self):
        self._running = True
        self._player = player = game_logic.Player()
        self._gamestate = game_logic.GameState(player)
        self._setup_board()
        self._prev_time = pygame.time.get_ticks()
        self._background_img = pygame.image.load('sprites/background.png')
        self._tiles = self.get_tiles()

    def get_tiles(self):
        return {
            '#':pygame.image.load('sprites/wall.png'),
            '+':pygame.image.load('sprites/sand.png'),
            'O':pygame.image.load('sprites/rock.png'),
            '*':pygame.image.load('sprites/diamond.png'),
            '@':pygame.image.load('sprites/monkey.png'),
            'X':pygame.image.load('sprites/empty.png'), #exit
            '':pygame.image.load('sprites/empty.png'),
            ' ':pygame.image.load('sprites/empty.png'),
            'Y':pygame.image.load('sprites/exit.png'),
            'C':pygame.image.load('sprites/crab.png')
        }

    def _setup_board(self):
        self._gamestate.update_field()

    def _make_surface(self, size=_SIZE):
        self._surface = pygame.display.set_mode(_SIZE)

    def _draw_bg(self):
        self._surface.fill(_RED)
        w = self._surface.get_width()
        h = self._surface.get_height()
        scaled_img = pygame.transform.scale(self._background_img, (w,h))
        surface = pygame.display.get_surface()
        surface.blit(scaled_img, scaled_img.get_rect())

    def _draw_tile(self, tile:str, row:int, col:int):
        width = int(self._surface.get_width()/self._gamestate.boardWidth)
        height = int(self._surface.get_height()/self._gamestate.boardHeight)
        
        top_left_x = (col * width)
        top_left_y = (row * height)

        
        scaled_img = pygame.transform.scale(self._tiles[tile], (width, height))
        surface = pygame.display.get_surface()
        surface.blit(scaled_img, (top_left_x, top_left_y))

    def _draw_tiles(self):
        field = self._gamestate.get_field()
        for r, row in enumerate(field):
            for c, tile in enumerate(row):
                self._draw_tile(tile, r, c)


    def _redraw(self):
        self._draw_bg()
        self._draw_tiles()
        pygame.display.flip()

    def _handle_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.VIDEORESIZE:
            self._make_surface(event.size)
        if event.type == pygame.KEYDOWN:
            vector = ('x', 0)
            if event.key == pygame.K_UP:
                vector = vector = ('y', -1)
            elif event.key == pygame.K_DOWN:
                vector = ('y', 1)
            elif event.key == pygame.K_LEFT:
                vector = ('x', -1)
            elif event.key == pygame.K_RIGHT:
                vector = ('x', 1)
            elif event.key == pygame.K_r:
                self._gamestate.die()
            self._gamestate.move_player(vector)

            


    def _handle_events(self):
        for event in pygame.event.get():
            self._handle_event(event)

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        self._make_surface()
        while self._running:
            clock.tick(_FRAME_RATE)
            curr_time = pygame.time.get_ticks()
            if curr_time - self._prev_time > _DELAY:
                self._gamestate.next()
                self._prev_time = curr_time
            self._handle_events()
            self._redraw()
            
            


if __name__ == '__main__':
    MonkeyMaze().run()
