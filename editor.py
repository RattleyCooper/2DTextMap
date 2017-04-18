

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

    def build(self, map_text, game_map, map_objects):
        self.place_tokens(map_text, game_map)
        self.place_objects(game_map, map_objects)

    def place_objects(self, game_map, map_objects):
        """
        Place the map objects onto the game map based on the game map tokens.

        :return:
        """

        # Get a list of game_object_token
        map_object_tokens = []
        map_objects_list = list(map_objects.values())
        if map_objects is not None:
            map_object_tokens = [map_object.token for map_object in map_objects.values()]

        # Go through game map tokens and place the objects into the game map.
        for (y, x), char in game_map.tokens.items():
            if char in map_object_tokens:
                map_object = map_objects_list[map_object_tokens.index(char)]
                obj = map_object(y, x)
                obj.place(game_map)
                continue

            game_map.objects[y, x] = char
            continue

    def place_tokens(self, map_text, game_map):
        """
        Place map tokens onto the game map.  Tokens denote map objects whether
        they are walls, floors, doors, etc.

        :return:
        """

        # Go through rows and place tokens on a 2D map.
        rows = [[char for char in line] for line in map_text.split('\n') if line != '']
        row_number = 0
        for row in rows:
            character_number = 0
            for character in row:
                game_map.tokens[row_number, character_number] = character
                character_number += 1
            row_number += 1


if __name__ == '__main__':
    import curses
    from map_objects import Wall, VerticalDoor, HorizontalDoor, Floor, Treasure, Food, Water
    from time import sleep

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

        maps = [box1, box2, box3]
        curses.curs_set(0)
        animation_speed = 0.00025

        # Build each box and present it onto the screen in an animated fashion.
        for map_text in maps:
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
            map_builder = MapBuilder()
            map_builder.build(map_text, game_map, map_objects)

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
