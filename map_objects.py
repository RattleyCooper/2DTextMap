

class MapObject(object):
    token = str
    drawing = ''
    color = 0
    ch_number = 0

    def __init__(self, y, x):
        self.y, self.x = y, x

    def place(self, game_map):
        game_map.objects[self.y, self.x] = self


class Treasure(MapObject):
    token = '$'
    color = 203
    drawing = '$'
    ch_number = None


class Food(MapObject):
    token = 'f'
    color = 11
    drawing = ''
    ch_number = None


class Floor(MapObject):
    token = ' '
    drawing = ' '
    color = 10
    ch_number = 32


class Wall(MapObject):
    token = '#'
    color = 10
    drawing = None
    ch_number = None

    def check_wall_borders(self, x, y, game_map):
        """
        Check the borders of the given coordinates.

        :param x:
        :param y:
        :param game_map:
        :return dict borders:
        """

        target_coordinates = self.get_target_coordinates(x, y)
        north_piece, south_piece, east_piece, west_piece = False, False, False, False
        for direction, target_coordinate in target_coordinates.items():
            try:
                target = game_map.tokens[target_coordinate]
                if target == '#':
                    if direction == 'n':
                        north_piece = True
                    elif direction == 's':
                        south_piece = True
                    elif direction == 'e':
                        east_piece = True
                    elif direction == 'w':
                        west_piece = True
            except KeyError:
                pass

        borders = {
            'n': north_piece,
            's': south_piece,
            'e': east_piece,
            'w': west_piece
        }
        return borders

    def get_target_coordinates(self, x, y):
        """
        Get the x/y coordinates of possible target locations directly surrounding the given x and y
        as a dict.  The keys for the returned dict will be 'n', 's', 'e', 'w', 'nw', 'ne', 'sw' &
        'se'.

        let 'T' equal the given x/y and let `#` represent possible target locations surrounding
        the given x/y:

            ###
            #T#
            ###

        :param x:
        :param y:
        :return dict:
        """

        n_target_coordinates = y - 1, x
        s_target_coordinates = y + 1, x
        e_target_coordinates = y, x + 1
        w_target_coordinates = y, x - 1
        ne_target_coordinates = y - 1, x + 1
        nw_target_coordinates = y - 1, x - 1
        se_target_coordinates = y + 1, x + 1
        sw_target_coordinates = y + 1, x - 1

        return {
            'n': n_target_coordinates,
            's': s_target_coordinates,
            'e': e_target_coordinates,
            'w': w_target_coordinates,
            'nw': nw_target_coordinates,
            'ne': ne_target_coordinates,
            'sw': sw_target_coordinates,
            'se': se_target_coordinates
        }

    def place(self, game_map):
        """
        Place a wall at the given coordinates.  This method will figure out which character
        to use based on the current map data.

        :param game_map:
        :return:
        """

        x, y = self.x, self.y

        borders = self.check_wall_borders(x, y, game_map)
        n_piece = borders['n']
        s_piece = borders['s']
        e_piece = borders['e']
        w_piece = borders['w']

        char_num = 0
        debug_char = ' '

        # Upper left corner.
        if (not n_piece and not w_piece) and (e_piece and s_piece):
            # 4194412   -   ┌
            char_num = 4194412
            debug_char = '┌'

        elif (not n_piece and not s_piece) and (e_piece or w_piece):
            # 4194417   -   ─
            char_num = 4194417
            debug_char = '─'
            self.color = 12

        elif (not w_piece and not e_piece) and (n_piece or s_piece):
            # 4194424     -   │
            char_num = 4194424
            debug_char = '│'

        elif (not n_piece and not e_piece) and (s_piece and w_piece):
            # 4194411     -   ┐
            char_num = 4194411
            debug_char = '┐'

        elif (not s_piece and not e_piece) and (n_piece and w_piece):
            # 4194410       -    ┘
            char_num = 4194410
            debug_char = '┘'

        elif (not s_piece and not w_piece) and (n_piece and e_piece):
            # 4194413       -   └
            char_num = 4194413
            debug_char = '└'

        elif (not n_piece) and (w_piece and s_piece and e_piece):
            # 4194423       -    ┬
            char_num = 4194423
            debug_char = '┬'

        elif (not s_piece) and (w_piece and e_piece and n_piece):
            # 4194422       -    ┴
            char_num = 4194422
            debug_char = '┴'

        elif (not e_piece) and (n_piece and s_piece and w_piece):
            # 4194421       -    ┤
            char_num = 4194421
            debug_char = '┤'

        elif (not w_piece) and (n_piece and s_piece and e_piece):
            # 4194420       -    ├
            char_num = 4194420
            debug_char = '├'

        elif n_piece and s_piece and e_piece and w_piece:
            # 4194414       -    ┼
            char_num = 4194414
            debug_char = '┼'

        self.ch_number = char_num
        self.drawing = debug_char

        game_map.objects[self.y, self.x] = self
        return


class VerticalDoor(MapObject):
    token = '|'
    drawing = '▒'
    color = 233
    ch_number = 4194401


class HorizontalDoor(MapObject):
    token = '-'
    drawing = '▒'
    color = 233
    ch_number = 4194401


class Water(MapObject):
    token = 'w'
    drawing = '▒'
    color = 22
    ch_number = 4194401
