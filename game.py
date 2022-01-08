"""
 *****************************************************************************
   FILE:  game.py

   AUTHOR: A.J. Zuckerman

   ASSIGNMENT: Final project

   DATE: 11/17/19

   DESCRIPTION: Creates the boardgame Azul in a playable window

 *****************************************************************************
"""

import random
from cs110graphics import *

class Game():
    """This class creates a game"""

    def __init__(self, win):
        """constructor for game class"""

        self._win = win
        self._round = True
        self._tile_count = 0

        self._button_list = []

        #makes 3 buttons for player select
        for num in range(0, 3):
            self._button_list.append(Button(self._win, num, self.set_num_players))

        self._num_players = 0

        self._turn = 0
        self._num_facs = 0

        self._player_list = []

        self._tile_colors = ['blue', 'red', 'black', 'white', 'yellow']

        self._factory_list = []
        self._tile_list = []

    def start_game(self):
        """begins game"""

        #set this inside start game b/c player num chosen by button
        self._num_facs = self._num_players * 2 + 1

        street = Street(self._win, self._player_list, self._turn, self)

        for num in range(0, self._num_players * 2 + 1):
            self._factory_list.append(Factory(self._win, num, self._tile_colors, self._player_list, self._turn, self, street))

        for factory in self._factory_list:
            sub_list = factory.get_tile_list_f()
            for tile in sub_list:
                self._tile_list.append(tile)

        street_tile_list = street.get_tile_list_s()

        for tile in street_tile_list:
            self._tile_list.append(tile)
            #tile list to be able to count when round is done

        for num in range(0, self._num_players):
            self._player_list.append(Player(num, self._win, self._tile_list, self))

    def change_turn(self):
        """changes the turn"""

        self._turn = (self._turn + 1) % self._num_players

    def get_turn(self):
        """accessor for turn"""

        return self._turn

    def get_players(self):
        """accessor for board loist"""

        return self._player_list

    def reset_turn(self):
        """subracts one from turn"""

        self._turn -= 1

    def add_tile_count(self):
        """adds one to tile count when tile is moved"""

        self._tile_count += 1

    def check_round(self):
        """checks if round has been completed"""

        total_tiles = self._num_facs * 4 + 1

        #eevry tile needs to be played for round to end
        if self._tile_count == total_tiles:
            return True
        else:
            return False

    def reset_round(self):
        """resets the round and gets in ready for next one"""

        self._factory_list = []

        street = Street(self._win, self._player_list, self._turn, self)

        for num in range(0, self._num_players * 2 + 1):
            self._factory_list.append(Factory(self._win, num, self._tile_colors, self._player_list, self._turn, self, street))

        self._tile_list = []

        for factory in self._factory_list:
            sub_list = factory.get_tile_list_f()
            for tile in sub_list:
                self._tile_list.append(tile)

        street_tile_list = street.get_tile_list_s()

        for tile in street_tile_list:
            self._tile_list.append(tile)

        board_list = []

        #basically same function as start game just doesn't make new boards
        for player in self._player_list:
            board_list.append(player.get_board())

        for board in board_list:
            board.new_round()

        self._tile_count = 0

    def set_turn(self, new_turn):
        """sets turn to player with green tile at the end of the round"""

        self._turn = new_turn

    def check_game(self):
        """checks if game is over"""

        game_ended = False

        board_list = []

        for player in self._player_list:
            board_list.append(player.get_board())

        for board in board_list:
            if board.game_over():
                game_ended = True

        #adds bonus scores if game has ended
        if game_ended:
            for board in board_list:
                board.add_score()
            self.end_game(board_list)

    def end_game(self, brd_list):
        """calculates winner and ends game"""

        winner = [brd_list[0]]
        #checks to see if anyone has a higher score, list because ties possible
        for entry in range(1, self._num_players):
            score = brd_list[entry].get_score()
            if score > winner[0].get_score():
                winner = [brd_list[entry]]
            if score == winner[0].get_score():
                if winner[0] != brd_list[entry]:
                    winner.append(brd_list[entry])

        length_win = len(winner)

        if length_win == 1:
            win_text = Text(self._win, 'Player' + ' ' + str(winner[0].get_player_num() + 1) + ' wins!', 40, (600, 465))
        if length_win == 2:
            win_text = Text(self._win, 'Player' + ' ' + str(winner[0].get_player_num() + 1) + ' and Player ' + str(winner[1].get_player_num() + 1) + ' tie!', 40, (600, 465))
        if length_win == 3:
            win_text = Text(self._win, 'Player' + ' ' + str(winner[0].get_player_num() + 1) + ' and Player ' + str(winner[1].get_player_num() + 1)  + ' and Player ' + str(winner[2].get_player_num() + 1) + ' tie!', 40, (600, 465))
        if length_win == 4:
            win_text = Text(self._win, 'Player' + ' ' + str(winner[0].get_player_num() + 1) + ' and Player ' + str(winner[1].get_player_num() + 1)  + ' and Player ' + str(winner[2].get_player_num() + 1) + ' and Player ' + str(winner[3].get_player_num() + 1) + ' tie!', 40, (600, 465))

        win_text.set_depth(-100)
        self._win.add(win_text)

    def set_num_players(self, num):
        """sets number of players for the game and begins game"""

        #called from button class
        self._num_players = num
        self.start_game()
        self.remove_buttons()

    def remove_buttons(self):
        """removes the buttons"""

        for button in self._button_list:
            button.remove()


class Button(EventHandler):
    """This is the class that creates buttons"""

    def __init__(self, win, num, function):
        """constructor for button class"""

        self._win = win
        self._num = num
        self._function = function

        self._body = Square(self._win, 100, (350 + 150 * self._num, 400))
        self._label = Text(self._win, str(self._num + 2), 50, (350 + 150 * self._num, 400))

        self._body.set_depth(3)
        self._label.set_depth(1)

        self._body.add_handler(self)
        self._label.add_handler(self)

        self._win.add(self._body)
        self._win.add(self._label)

    def handle_mouse_release(self, event):
        """returns number of players on press"""

        self._function(self._num + 2)

    def remove(self):
        """removes buttons from window"""

        self._win.remove(self._body)
        self._win.remove(self._label)


class Player:
    """This is the class that creates player"""

    def __init__(self, num, win, tile_list, game):
        """constructor for the player class"""

        self._player_num = num
        self._win = win
        self._tile_list = tile_list
        self._game = game

        grid = []

        #makes staircase, each row is longer
        for row in range(1, 6):
            col = ['e'] * row
            grid.append(col)

        #scoring grid in lighter colors (purple is white)
        color_grid = [['cornflowerblue', 'palegoldenrod', 'lightcoral', 'grey', 'mediumpurple'],
                      ['mediumpurple', 'cornflowerblue', 'palegoldenrod', 'lightcoral', 'grey'],
                      ['grey', 'mediumpurple', 'cornflowerblue', 'palegoldenrod', 'lightcoral'],
                      ['lightcoral', 'grey', 'mediumpurple', 'cornflowerblue', 'palegoldenrod'],
                      ['palegoldenrod', 'lightcoral', 'grey', 'mediumpurple', 'cornflowerblue']]

        minus_list = ['e', 'e', 'e', 'e', 'e', 'e', 'e']

        scoring_grid = []

        for row in range(5):
            col = ['e', 'e', 'e', 'e', 'e']
            scoring_grid.append(col)


        self._board = Board(self._win, self._player_num, grid, color_grid, minus_list, scoring_grid, self._game)

    def get_board(self):
        """accessor for board in player class"""

        return self._board

class Board():
    """This class creates a board"""

    def __init__(self, win, num_player, grid, cg, ml, sg, game):
        """Constructor for board class"""

        self._win = win
        self._num_play = num_player
        self._grid = grid
        self._cg = cg
        self._ml = ml
        self._sg = sg
        self._game = game
        self.depth = 5
        self._score = 0

        self._text = Text(self._win, 'Player' + ' ' + str(self._num_play + 1), 20, (350 + 400 * self._num_play, 25))
        self._win.add(self._text)

        self._score_num = Text(self._win, str(self._score), 15, (520 + 400 * self._num_play, 110))

        self._count = 0
        self._row = 0
        self._o_loc = ''

        self.draw()

    def draw(self):
        """Adds board to the graphics window"""

        #draws staircase grid empty when 'e' and with color when colored
        for row in range(len(self._grid)):
            for col in range(row + 1):
                if self._grid[row][col] == 'e':
                    squ = Square(self._win, 30, (300 + 400 * self._num_play - 30 * col, 60 + 30 * row))
                    self._win.add(squ)
                    Fillable.set_fill_color(squ, 'peachpuff')
                    squ.set_depth(self.depth)
                else:
                    squ = Square(self._win, 30, (300 + 400 * self._num_play - 30 * col, 60 + 30 * row))
                    self._win.add(squ)
                    Fillable.set_fill_color(squ, self._grid[row][col])
                    squ.set_depth(self.depth - 1)

                    #cg sets its own colors
        for row in range(len(self._cg)):
            for col in range(len(self._cg)):
                squ = Square(self._win, 30, (350 + 30 * col + 400 * self._num_play, 60 + 30 * row))
                self._win.add(squ)
                Fillable.set_fill_color(squ, self._cg[row][col])
                squ.set_depth(self.depth)

        minus_text = Text(self._win, '-1     -1     -2     -2     -2     -3     -3', 10, (270 + 400 * self._num_play, 210))
        self._win.add(minus_text)

        score_text = Text(self._win, 'Score:', 15, (520 + 400 * self._num_play, 90))
        self._win.add(score_text)

        self._win.add(self._score_num)

        #same as staircase
        for num in range(7):
            if self._ml[num] == 'e':
                squ = Square(self._win, 30, (360 + 400 * self._num_play - 30 * num, 240))
                self._win.add(squ)
                Fillable.set_fill_color(squ, 'peachpuff')
                squ.set_depth(self.depth)
            else:
                squ = Square(self._win, 30, (360 + 400 * self._num_play - 30 * num, 240))
                self._win.add(squ)
                Fillable.set_fill_color(squ, self._ml[num])
                squ.set_depth(self.depth - 1)

    def is_in_bounds(self, xc, yc, color, tile):
        """sees if the grid has space to make it have tiles"""

        count = 0
        for row in range(len(self._grid)):
            for col in range(row + 1):
                if xc < 300 + 400 * self._num_play - 30 * col + 15 and xc > 300 + 400 * self._num_play - 30 * col - 15 and yc < 75 + 30 * row and yc > 45 + 30 * row:
                    xc = 300 + 400 * self._num_play - 30 * col
                    yc = 60 + 30 * row
                    #goes through rows and cols to see if a placed tile is
                    #in range then sets it to the middle of the square
                    row = int((yc - 60)/30)
                    #converts yc back to row then checks if row is empty
                    #or color is the same
                    for entry in range(len(self._grid[row])):
                        if self._grid[row][entry] != color:
                            count += 1
                            if self._grid[row][entry] == 'e':
                                count -= 1
                                if count != 0:
                                    return False, False
                    for index in range(len(self._cg)):
                        if self._cg[row][index] == color:
                            return False, False
                    if color != 'green':
                        return (xc, yc), self._grid
                        #same thing for minus list
        for entry in range(len(self._ml)):
            if xc < 360 + 400 * self._num_play - 30 * entry + 15 and xc > 360 + 400 * self._num_play - 30 * entry - 15 and yc < 255 and yc > 225:
                xc = 360 + 400 * self._num_play - 30 * entry
                yc = 240
                return (xc, yc), self._ml
        return False, False

    def check_row_same(self, tuple_loc, place):
        """checks if row is the same if a tile was already placed"""

        if place == self._grid:
            if tuple_loc != False:
                if int((tuple_loc[1] - 60)/30) != self._row:
                    return False
        return tuple_loc

    def change_board(self, tuple_loc, color, tile, place):
        """changes the grid"""

        if place == self._grid:
            xc = tuple_loc[0]
            yc = tuple_loc[1]
            col = int((xc - (300 + 400 * self._num_play))/-30)
            row = int((yc - 60)/30)
            self._grid[row][col] = color
            #tile goes away board gets colored in
            self._win.remove(tile)
            self.draw()

        if place == self._ml:
            xc = tuple_loc[0]
            entry = int((xc - (360 + 400 * self._num_play))/-30)
            self._ml[entry] = color
            self._win.remove(tile)
            self.draw()

    def new_round(self):
        """saves completed rows in cg and saves uncompleted rows in grid"""

        #loops through bopard and saves rows that are not full then
        #moves complete rows to scoring grid
        for row in range(len(self._grid)):
            count = 0
            for col in range(row + 1):
                if self._grid[row][col] != 'e':
                    base_color = self._grid[row][col]
                    for entry in range(len(self._grid[row])):
                        if base_color != self._grid[row][entry]:
                            count += 1
                    if count == 0:
                        placed_row, placed_col = self.save_color(base_color, row)
                        self.grid_reset(row)
                        self.score_board(placed_row, placed_col)

        self.score_ml()
        self._score_num.set_text(str(self._score))

        #sets turn to person with the green (one) tile
        for entry in range(len(self._ml)):
            if self._ml[entry] == 'green':
                self._game.set_turn(self._num_play)
        self.reset_ml()

        #draws everything on top of the old stuff
        self.depth -= 2
        self.draw()

    def save_color(self, color, row):
        """saves color in cg and updates score grid"""

        for col in range(len(self._cg[row])):
            if color == 'blue':
                if self._cg[row][col] == 'cornflowerblue':
                    self._cg[row][col] = 'blue'
                    self._sg[row][col] = 'f'
                    return row, col

            if color == 'red':
                if self._cg[row][col] == 'lightcoral':
                    self._cg[row][col] = 'red'
                    self._sg[row][col] = 'f'
                    return row, col

            if color == 'yellow':
                if self._cg[row][col] == 'palegoldenrod':
                    self._cg[row][col] = 'yellow'
                    self._sg[row][col] = 'f'
                    return row, col

            if color == 'black':
                if self._cg[row][col] == 'grey':
                    self._cg[row][col] = 'black'
                    self._sg[row][col] = 'f'
                    return row, col

            if color == 'white':
                if self._cg[row][col] == 'mediumpurple':
                    self._cg[row][col] = 'white'
                    self._sg[row][col] = 'f'
                    return row, col

    def score_board(self, p_row, p_col):
        """scores main game board automatically"""

        row_check = False
        col_check = False
        tile_score = 0

        #very similar to word search just checks if tiles exist next to new tile
        #and scores points for adjacent rows and cols
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dir in directions:
            count = 0
            for num in range(1, 6):
                score_row = p_row + dir[0] * num
                score_col = p_col + dir[1] * num
                dir_count = count
                if self.score_in_bounds(score_row, score_col):
                    if self._sg[score_row][score_col] == 'f':
                        count += 1
                        if dir == (-1, 0) or dir == (1, 0):
                            row_check = True
                        if dir == (0, -1) or dir == (0, 1):
                            col_check = True
                    else:
                        break
            tile_score += dir_count

        #needs to score one for itself in the row and col scores
        if row_check:
            tile_score += 1
        if col_check:
            tile_score += 1
        #if it's touching nothing needs to score for itself
        if tile_score == 0:
            tile_score += 1

        self._score += tile_score

    def score_ml(self):
        """scores minus list automatically"""

        #indices are drawn backwards so six and five are the farthest to the
        #left on the board
        for num in range(len(self._ml)):
            if self._ml[num] != 'e':
                if num == 6 or num == 5:
                    self._score -= 1
                if num == 4 or num == 3 or num == 2:
                    self._score -= 2
                if num == 1 or num == 0:
                    self._score -= 3

    def score_in_bounds(self, row, col):
        """checks if scoring grid chekcer is in bounds"""

        if 0 <= row <= len(self._sg) - 1 and 0 <= col <= len(self._sg) - 1:
            return True
        return False

    def game_over(self):
        """checks if a row is filled and if game is over"""

        for row in range(len(self._sg)):
            if self._sg[row] == ['f', 'f', 'f', 'f', 'f']:
                return True
        return False

    def add_score(self):
        """adds special scores for end of game"""

        #score for full row
        for row in range(len(self._sg)):
            if self._sg[row] == ['f', 'f', 'f', 'f', 'f']:
                self._score += 2

        #score for full col
        for col in range(len(self._sg)):
            count = 0
            for row in range(len(self._sg)):
                if self._sg[row][col] == 'f':
                    count += 1
            if count == 5:
                self._score += 7

        color_list = ['blue', 'red', 'black', 'white', 'yellow']

        #score for 5 of one color
        for color in color_list:
            color_count = 0
            for row in range(len(self._cg)):
                for col in range(len(self._cg)):
                    if self._cg[row][col] == color:
                        color_count += 1
            if color_count == 5:
                self._score += 10

        self._score_num.set_text(str(self._score))

    def grid_reset(self, row):
        """resets grid for rows that are full"""

        self._grid[row] = ['e'] * (row + 1)

    def reset_ml(self):
        """resets minus list at the end of the round"""

        self._ml = ['e', 'e', 'e', 'e', 'e', 'e', 'e']

    def get_count(self):
        """accessor for count"""

        return self._count

    def get_row(self):
        """accessor for row"""

        return self._row

    def change_row(self, new_row):
        """mutator for row"""

        self._row = new_row

    def change_count(self, new_count):
        """mutator for count"""

        self._count = new_count

    def get_score(self):
        """accessor for score"""

        return self._score

    def get_player_num(self):
        """accessor of player number"""

        return self._num_play

    def change_o_loc(self, new_loc):
        """changes saved o loc for last tile"""

        self._o_loc = new_loc

    def check_o_loc_same(self, tile_loc, tuple_loc):
        """checks if o locs are the same for second tile"""

        if self._o_loc == tile_loc:
            return tuple_loc
        else:
            return False


class Tile(EventHandler):
    """This class creates tiles"""

    def __init__(self, win, color, xc, yc, bs, turn, game, o_loc):
        """constructor for tile class"""

        self._win = win
        self._color = color
        self._xc = xc
        self._yc = yc
        self._bs = bs
        self._turn = turn
        self._game = game
        self._o_loc = o_loc
        self._move = False

    def draw(self):
        """Adds tile to graphics window"""

        self._body = Square(self._win, 30, (self._xc, self._yc))
        self._win.add(self._body)
        self._body.add_handler(self)
        Fillable.set_fill_color(self._body, self._color)
        self._body.set_depth(2)

    def set_location(self, loc):
        """sets location of a tile"""
        self._xc = loc[0]
        self._yc = loc[1]

    def handle_mouse_release(self, event):
        """Allows tiles to be moved"""

        self.set_location(event.get_mouse_location())

        self._move = True

        players = self._game.get_players()
        current_player = players[self._game.get_turn()] #turn
        board = current_player.get_board() #gets board of the player
        tuple_loc, place = board.is_in_bounds(self._xc, self._yc, self._color, self._body)
        #checks if this is their first tile placed
        if board.get_count() != 0:
            #checks if tile placed in same row
            tuple_loc = board.check_row_same(tuple_loc, place)
            #checks if tile is from same original location
            tuple_loc = board.check_o_loc_same(self._o_loc, tuple_loc)
        if tuple_loc != False:
            board.change_row(int((tuple_loc[1] - 60)/30))
            board.change_board(tuple_loc, self._color, self._body, place)
            #says that this board has already moved
            self._game.add_tile_count()
            self._game.change_turn()
            self._win.remove(self._body)
            self._o_loc.remove_tile(self._color)
            #remove tile color from the list
            if self._o_loc.check_match(self._color):
                #check if more tiles of same color and reset turn
                self._game.reset_turn()
                board.change_count(1)
                board.change_o_loc(self._o_loc)
            else:
                #moves other tiles to street if they are not the same color
                self._o_loc.tile_to_street()
                board.change_count(0)
                #check if round and game are over
            if self._game.check_round():
                self._game.reset_round()
                self._game.check_game()

    def get_tile_loc(self):
        """accessor for tile location"""

        return self._xc, self._yc

    def get_move(self):
        """accessor for if the tile has moved"""

        return self._move

    def get_color(self):
        """accessor for tile color"""

        return self._color

    def get_body(self):
        """accessor for tile body"""

        return self._body

    def change_o_loc(self, loc):
        """mutator for original location"""

        self._o_loc = loc

class Factory():
    """This class creates factories"""

    def __init__(self, win, num, tc, bs, turn, game, street):
        """constructor for factory class"""

        factory_grid = [['e', 'e'], ['e', 'e']]

        self._win = win
        self._num = num
        self._tc = tc
        self._fg = factory_grid
        self._bs = bs
        self._turn = turn
        self._game = game
        self._street = street
        self._tile_list = []

        self.draw()

    def draw(self):
        """Adds factory to graphics window"""

        cir = Circle(self._win, 70, (200 + 180 * self._num, 400))
        self._win.add(cir)
        Fillable.set_fill_color(cir, 'lightskyblue')
        cir.set_depth(5)

        for row in range(len(self._fg)):
            for col in range(len(self._fg)):
                self._fg[row][col] = random.choice(self._tc)

        #creates tiles on the factory
        for row in range(len(self._fg)):
            for col in range(len(self._fg)):
                tile = Tile(self._win, self._fg[row][col], 180 + 180 * self._num + 40 * col, 380 + 40 * row, self._bs, self._turn, self._game, self)
                tile.draw()
                self._tile_list.append(tile)

    def get_tile_list_f(self):
        """accessor for tile list"""

        return self._tile_list

    def check_match(self, color):
        """checks if there is more than one of the same color"""

        for row in range(len(self._fg)):
            for col in range(len(self._fg)):
                if self._fg[row][col] == color:
                    return True
        return False

    def remove_tile(self, color):
        """removes tile from grid"""

        for row in range(len(self._fg)):
            for col in range(len(self._fg)):
                if self._fg[row][col] == color:
                    self._fg[row][col] = 'e'
                    return

    def tile_to_street(self):
        """moves tiles that don't match color to the street"""

        for row in range(len(self._fg)):
            for col in range(len(self._fg)):
                if self._fg[row][col] != 'e':
                    tile = self._tile_list[2 * row + col]
                    self._win.remove(tile.get_body())
                    tile.set_location((random.randint(750, 950), random.randint(600, 700)))
                    tile.draw()
                    #give strett tile list color of tile moved
                    self._street.add_color(tile.get_color())
                    tile.change_o_loc(self._street)


class Street():
    """This class creates the street"""

    def __init__(self, win, bs, turn, game):
        """constructor for street class"""

        self._win = win
        self._bs = bs
        self._turn = turn
        self._game = game
        self._tile_list = []
        self._color_list = []

        self.draw()

    def draw(self):
        """draws the street"""

        rec = Rectangle(self._win, 400, 200, (900, 650))
        self._win.add(rec)
        Fillable.set_fill_color(rec, 'peachpuff')
        rec.set_depth(5)

        #one tile
        tile = Tile(self._win, 'green', 900, 650, self._bs, self._turn, self._game, self)
        tile.draw()
        self._tile_list.append(tile)
        self._color_list.append(tile.get_color())

    def get_tile_list_s(self):
        """accessor for tile list"""

        return self._tile_list

    def add_color(self, color):
        """mutator for tile list to add tiles when moved from factory"""

        self._color_list.append(color)

    def check_match(self, color):
        """checks if there is more than one of the same color"""

        for entry in range(len(self._color_list)):
            if self._color_list[entry] == color:
                return True
            if self._color_list[entry] == 'green':
                return True
        return False

    def remove_tile(self, color):
        """removes tile from grid"""

        for entry in range(len(self._color_list)):
            if self._color_list[entry] == color:
                self._color_list[entry] = 'e'
                return

    def tile_to_street(self):
        """here so there is no error in handle_mouse_release so does nothing"""

        return


def main(win):
    """The main function"""

    #graphics set up
    win.set_background('lightpink')
    win.set_height(800)
    win.set_width(1800)

    my_game = Game(win)


if __name__ == "__main__":
    StartGraphicsSystem(main)
