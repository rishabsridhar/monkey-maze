from copy import deepcopy
import random

_WIDTH = 19
_HEIGHT = 12

class GameState:
    boardWidth = 19
    boardHeight = 12
    tiles = {
        'wall': '#',
        'sand': '+',
        'rock': 'O',
        'gem': '*',
        'player': '@',
        'exit': 'X'
    }

    def __init__(self, player):
        self.field = self.empty_board()
        self.player = player
        self.add_player()

    def __str__(self):
        s = ''
        for row in self.field:
            s += ''.join(row) + '\n'
        return s[:-1]

    def get_field(self):
        return deepcopy(self.field)

    def empty_board(self):
        # for ROW in board: for i in ROW
        #field = [['+']*self.boardWidth]*self.boardHeight
        field = []
        for _ in range(12):
            field.append(['+']*19)

        field[0], field[len(field)-1] = ['#']*self.boardWidth, ['#']*self.boardWidth
        for row in field:
            row[0], row[-1] = '#', '#'
        field[-2][-2] = 'X'
        return field

    def add_player(self):
        self.field[self.player.y][self.player.x] = '@'

    def delete_player(self):
       self.field[self.player.y][self.player.x] = ' '

    def move_player(self, vector:(str, int)):
        #vector[1] = 1 if vector[1] > 0 else -1
        if vector[0] == 'x':
            new_pos = (self.player.x+vector[1], self.player.y)
        else:
            new_pos = (self.player.x, self.player.y+vector[1])
        if self.get_field()[new_pos[1]][new_pos[0]] == 'X':
            #print(f'GAME OVER. You found {self.player.diamonds} out of {self.diamonds} diamonds!')
            self.game_over()
            return True
        if self.get_field()[new_pos[1]][new_pos[0]] == 'O' and vector[0] == 'x':
            if vector[0] == 'x' and self.get_field()[new_pos[1]][new_pos[0]+vector[1]] == ' ':
                self.field[new_pos[1]][new_pos[0]+vector[1]] = 'O'
                self.delete_player()
                self.player.x, self.player.y = new_pos[0], new_pos[1]
                self.add_player()
        
        if self.get_field()[new_pos[1]][new_pos[0]] not in ['#', 'O']:
            self.delete_player()
            self.player.x, self.player.y = new_pos[0], new_pos[1]
            if self.get_field()[new_pos[1]][new_pos[0]] == '*':
                self.player.diamonds += 1
                print(f'GOT A DIAMOND!!! {self.player.diamonds} found so far out of {self.diamonds}')
            self.add_player()

    def random_add(self, symbol:str, number:int):
        for _ in range(number):
            x = random.randint(1, self.boardWidth-1)
            y = random.randint(1, self.boardHeight-1)
            try:
                if self.field[y][x] not in ['@','#','X']:
                    self.field[y][x] = symbol
            except IndexError:
                print(x,y)
        self.diamonds = self.__str__().count('*')

    def next(self):
        '''Moves enemies and  drops diamonds/rocks'''
        #Drops
        cache = set()
        for i in range(self.boardWidth):
            for j in range(self.boardHeight):
                if self.field[j][i] in ['O','*']:
                    if self.field[j+1][i] == ' ' and (j, i) not in cache:
                        cache.add((j+1, i))
                        self.field[j+1][i] = self.field[j][i]
                        self.field[j][i] = ' '
                    elif self.field[j+1][i] == '@' and (j, i) in cache:
                        cache.add((j+1, i))
                        self.die()
                        return True
    
    def reset_board(self):
        self.field = self.empty_board()
        self.player.die()
        self.add_player()
        ''''''
        self.random_add('O', 5)
        self.random_add('*', 8)

    def die(self):
        self.player.die()
        print(f'Ouch! {self.player.lives} lives left.')
        self.reset_board()
        if self.player.lives < 1:
            self.game_over()

    def game_over(self):
        print(f'GAME OVER. You found {self.player.diamonds} out of {self.diamonds} diamonds!')
        quit()
            

class Player:
    def __init__(self):
        self.x, self.y = 1, 1
        self.diamonds = 0
        self.lives = 3

    def position(self):
        return (self.x, self.y)

    def die(self):
        self.diamonds = 0
        self.x, self.y = 1,1
        return (self.x, self.y)

    


if __name__ == '__main__':
    player = Player()
    game = GameState(player)
    print(game)
    
