import curses
from map_objects import Wall, VerticalDoor, HorizontalDoor, Floor, Treasure, Food, Water
from time import sleep


class Map(object):
    """
    Container that holds all the objects on the game map.
    """
    def __init__(self):
        # Container to hold coordinates.
        self.tokens = {}
        self.objects = {}


class MapBuilder(object):
    """
    Builds boxes based off of a text representation of said box.  This does not draw anything, just creates
    a simple interface for converting the text to coordinates that hold the correct characters for
    displaying the box.
    """
    def __init__(self, map_text, game_map, map_objects=None):
        # Parse the input
        self.map_text = map_text
        self.rows = [[char for char in line] for line in map_text.split('\n') if line != '']

        self.game_map = game_map
        self.map_objects = map_objects

        # Run methods to build up the Map object.
        self.place_tokens()
        self.place_objects()

    def place_objects(self):
        """
        Place the map objects onto the game map based on the game map tokens.

        :return:
        """

        game_object_tokens = []
        if self.map_objects is not None:
            game_object_tokens = [o.token for o in self.map_objects.values()]

        # Go through game map tokens and place the objects into the game map.
        for (y, x), char in self.game_map.tokens.items():
            if char in game_object_tokens:
                game_objects = [o for o in self.map_objects.values() if o.token == char]
                if game_objects:
                    obj = game_objects[0](y, x)
                    obj.place(self.game_map)
                    continue

            self.game_map.objects[y, x] = char
            continue

    def place_tokens(self):
        """
        Place map tokens onto the game map.  Tokens denote map objects whether
        they are walls, floors, doors, etc.

        :return:
        """

        row_number = 0
        for row in self.rows:
            character_number = 0
            for character in row:
                self.game_map.tokens[row_number, character_number] = character
                character_number += 1
            row_number += 1


def main(stdscr):
    # Place map tokens into some strings.
    box1 = """
        ##############                                       ##############
        #            #########################################            #
        #            #                                       #            #
        #            #######                           #######            #
        #            #     #                           #     #            #
        #            #     #                           #     #            #
        ###########################             ###########################
           #  #      #            #             #            #     #  #
           #  #      #            #             #            #     #  #
           #  ########            ####### #######            #######  #
           #         #            #     # #     #            #        #
           #         #            #     # #     #            #        #
           #         #########################################        #
           #               #      #             #      #              #
           #               #      #             #      #              #
           #               ########  r/python   ########              #
           #                      #             #                     #
           #                      #             #                     #
           #                      ###############                     #
           #                                                          #
           ############################################################
    """

    box2 = """
         ########
         ########
          #    #
          #    #
    ###################################################################
    #                                                                 #
    #                                                                 #
    #                                                                 #
    #                                                                 #
    #                                                                 #
    ###################################################################
       #                                                           #
       #   #########                                   #########   #
       #   #   #   #                                   #   #   #   #
       #   #########                                   #########   #
       #   #   #   #                                   #   #   #   #
       #   #########             /r/python             #########   #
       #                                                           #
       #   #########            ###########            #########   #
       #   #   #   #            #         #            #   #   #   #
       #   #########            #         #            #########   #
       #   #   #   #            #         #            #   #   #   #
       #   #########            #        *#            #########   #
       #                        #         #                        #
       #                        #         #                        #
       #############################################################
    """

    box3 = """
    #########################################################
    #          #f                             #             #
    #          #                              |             #
    #          #                              |             #
    #####--#####                              #             #
    #                                         #             #
    |                 ###########             #             #
    |                 #wwwwwwwww#             ###############
    |                 #wwwwwwwww#             #            $#
    #                 #wwwwwwwww#             #             #
    #                 ###########             #             #
    #                                         |             #
    #                                         |             #
    #                                         #             #
    #########################################################
    """

    boxes = [box1, box2, box3]
    curses.curs_set(0)
    animation_speed = 0.00025

    # Build each box and present it onto the screen in an animated fashion.
    for box in boxes:
        # Build the box(converts tokens to wall pieces).

        game_map = Map()
        map_objects = {
            'vdoor': VerticalDoor,
            'hdoor': HorizontalDoor,
            'wall': Wall,
            'floor': Floor,
            'treasure': Treasure,
            'food': Food,
            'water': Water
        }
        map_builder = MapBuilder(box, game_map, map_objects=map_objects)
        for (y, x), obj in game_map.objects.items():
            try:
                stdscr.addch(y, x, obj.ch_number, curses.color_pair(obj.color))
            except AttributeError:
                stdscr.addstr(y, x, obj)
            except TypeError:
                stdscr.addstr(y, x, obj.drawing, curses.color_pair(obj.color))
            stdscr.refresh()
            sleep(animation_speed)

        sleep(5)
        stdscr.clear()


try:
    s = curses.initscr()
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    main(s)
finally:
    try:
        curses.nocbreak()
    except curses.error:
        import sys
        sys.exit()

    s.keypad(False)
    curses.echo()
    curses.endwin()
