from copy import deepcopy
import random
from levels import get_level

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
        'locked': 'Y',
        'exit': 'X'
    }

    def __init__(self, player):
        self.field = self.empty_board()
        self.player = player
        self.level = 1
        self.diamonds = 0
        self.enemies = set()
        self.add_player()

    def __str__(self):
        s = ''
        for row in self.field:
            s += ''.join(row) + '\n'
        return s[:-1]

    def get_field(self):
        return deepcopy(self.field)

    def empty_board(self, base='+'):
        field = []
        for _ in range(12):
            field.append([base]*19)

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
        if vector[0] == 'x':
            new_pos = (self.player.x+vector[1], self.player.y)
        else:
            new_pos = (self.player.x, self.player.y+vector[1])
        if self.get_field()[new_pos[1]][new_pos[0]] == 'X':
            self.next_level()
            return True
        if self.get_field()[new_pos[1]][new_pos[0]] == 'O' and vector[0] == 'x':
            if vector[0] == 'x' and self.get_field()[new_pos[1]][new_pos[0]+vector[1]] == ' ':
                self.field[new_pos[1]][new_pos[0]+vector[1]] = 'O'
                self.delete_player()
                self.player.x, self.player.y = new_pos[0], new_pos[1]
                self.add_player()
        
        if self.get_field()[new_pos[1]][new_pos[0]] not in ['#', 'O', 'Y']:
            self.delete_player()
            self.player.x, self.player.y = new_pos[0], new_pos[1]
            if self.get_field()[new_pos[1]][new_pos[0]] == '*':
                self.player.diamonds += 1
                if self.player.diamonds == self.diamonds:
                    self.field[-2][-1] = 'X'
            self.add_player()

    def move_crab(self, enemy, j, i):
        if enemy.dir == 'L':
            if self.field[j][i-1] == '@':
                self.player.lives -= 1
                self.die()
            elif self.field[j][i-1] not in ['#','O','+','*']:
                self.field[j][i-1], self.field[j][i] = 'C', ' '
                enemy.y, enemy.x = j, i-1
            else:
                enemy.dir = 'D'
        elif enemy.dir == 'R':
            if self.field[j][i+1] == '@':
                self.player.lives -= 1
                self.die()
            elif self.field[j][i+1] not in ['#','O','+','*']:
                self.field[j][i+1], self.field[j][i] = 'C', ' '
                enemy.y, enemy.x = j, i+1
            else:
                enemy.dir = 'U'
        elif enemy.dir == 'D':
            if self.field[j+1][i] == '@':
                self.player.lives -= 1
                self.die()
            elif self.field[j+1][i] not in ['#','O','+']:
                self.field[j+1][i], self.field[j][i] = 'C', ' '
                enemy.y, enemy.x = j+1, i
            else:
                enemy.dir = 'R'
        elif enemy.dir == 'U':
            if self.field[j-1][i] == '@':
                self.player.lives -= 1
                self.die()
            elif self.field[j-1][i] not in ['#','O','+']:
                self.field[j-1][i], self.field[j][i] = 'C', ' '
                enemy.y, enemy.x = j-1, i
            else:
                enemy.dir = 'L'
            


    def random_add(self, symbol:str, number:int):
        for _ in range(number):
            x = random.randint(1, self.boardWidth-1)
            y = random.randint(1, self.boardHeight-1)
            try:
                if self.field[y][x] not in ['@','#','X','Y']:
                    self.field[y][x] = symbol
            except IndexError:
                print(x,y)
        self.diamonds = self.__str__().count('*')

    def count_diamonds(self):
        return sum([i.count('*') for i in self.field])

    def get_start_enemies(self):
        e = set()
        for i,row in enumerate(self.field):
            for j in range(len(row)):
                if row[j] in ['C']:
                    e.add(Enemy(j,i))
        self.enemies = e
        return e


    def update_field(self):
        self.field = get_level(self.level)
        self.get_start_enemies()
        self.diamonds = self.count_diamonds()
        self.add_player()

    def next_level(self):
        self.player.die()
        self.level += 1
        self.update_field()
        self.get_start_enemies()

    def get_enemy_at_pos(self, j,i):
        
        for e in self.enemies:
            if e.pos() == (i,j):
                return e
            
        print('POS: ',str(j), str(i), self.enemies)


    def next(self):
        '''Moves enemies and  drops diamonds/rocks'''
        cache = set()
        for i in range(self.boardWidth):
            for j in range(self.boardHeight):
                if self.field[j][i] in ['O','*']:
                    if self.field[j+1][i] == ' ' and (j, i) not in cache:
                        cache.add((j+1, i))
                        print(cache, self.player.position())
                        self.field[j+1][i] = self.field[j][i]
                        self.field[j][i] = ' '
                    if self.field[j+1][i] == '@' and (j, i) in cache: #j+1
                        cache.add((j+1, i))
                        #cache.add((j+1, i))
                        self.field[j+1][i] = self.field[j][i]
                        self.field[j][i] = ' '
                        self.player.lives -= 1
                        self.die()
                        return True
                if self.field[j][i] in ['C'] and (j,i) not in cache:
                    enemy = self.get_enemy_at_pos(j,i)
                    if enemy:
                        if enemy.dir == 'R':
                            cache.add((j,i+1))
                        elif enemy.dir == 'D':
                            cache.add((j+1,i)) 
                        self.move_crab(enemy, j,i)
                    
    
    def reset_board(self):
        self.update_field()

    def get_init_player_pos(self):
        for i,r in enumerate(get_level(self.level)):
            for j,x in enumerate(r):
                if x == '@':
                    return (i,j)



    def die(self):
        player_x, player_y = self.get_init_player_pos()
        self.player.die(player_x, player_y)
        print(f'Ouch! {self.player.lives} lives left.')
        self.reset_board()
        if self.player.lives < 1:
            self.game_over()

    def game_over(self):
        print(f'GAME OVER. You found {self.player.diamonds} out of {self.diamonds} diamonds!')
        quit()
            

class Player:
    def __init__(self, x=1, y=1):
        self.x, self.y = x, y
        self.diamonds = 0
        self.lives = 3

    def position(self):
        return (self.x, self.y)

    def die(self, x=1,y=1):
        self.diamonds = 0
        self.x, self.y = 1,1
        return (self.x, self.y)

class Enemy:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.dir = 'L'
    
    def pos(self):
        return (self.x, self.y)

    def move(self):
        pass

class Crab(Enemy):
    def __init__(self, x, y):
        Enemy.__init__(self, x, y)
        self.dir = 'L'


if __name__ == '__main__':
    player = Player()
    game = GameState(player)
    print(game)
    
