

class Map(object):
    """
    Container that holds all the objects on the game map.

    Access objects on the map easily:

        for (y, x), map_object in self.objects.items():
            stdscr.addstr(y, x, map_object.display, curses.color_pair(map_object.color))

        # Move an object.
        if isinstance(self.objects[y, x], Treasure):
            # do something
            pass
    """
    def __init__(self):
        # Container to hold coordinates.
        self.tokens = {}
        self.objects = {}


class MapBuilder(object):
    """
    Builds maps based off of a text representation of said map.  This does not draw anything, just creates
    a simple interface for converting the text to coordinates that hold the correct objects for displaying
    the map.
    """

    @staticmethod
    def build(map_text, game_map, map_objects):
        """
        Populate the game_map with the given map_objects, based on the tokens in the map_text.

        map_text        -   Text with "tokens"(characters that correspond to specific map
                            objects) and any other characters that should be built.

        game_map        -   Map object with a `tokens` attribute and an `objects` attribute.

        map_objects     -   A dictionary of map objects that have not been instantiated.

        :param map_text: str
        :param game_map: Map
        :param map_objects: dict
        :return game_map: Map
        """

        MapBuilder.place_tokens(map_text, game_map)
        MapBuilder.place_objects(game_map, map_objects)

        return game_map

    @staticmethod
    def place_objects(game_map, map_objects):
        """
        Place the map_objects onto the game_map.

        :return:
        """

        # Get a list of map_object_tokens
        map_object_tokens = []
        map_objects_list = list(map_objects.values())
        if map_objects is not None:
            map_object_tokens = [map_object.token for map_object in map_objects.values()]

        # Go through game map tokens and place the corresponding objects into the game map.
        for (y, x), token in game_map.tokens.items():
            # If the token on the game map corresponds to an object token, place the
            # object on the map instead of the token.
            if token in map_object_tokens:
                map_object = map_objects_list[map_object_tokens.index(token)]
                obj = map_object(y, x)
                obj.place(game_map)
                continue

            # Place the token on the map since there was no
            # game object with a corresponding token.
            game_map.objects[y, x] = token
            continue

        return

    @staticmethod
    def place_tokens(map_text, game_map):
        """
        Place map tokens onto the game_map based on the map_text.  Tokens represent map objects whether
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

        return


if __name__ == '__main__':
    import curses
    from map_objects import Wall, VerticalDoor, HorizontalDoor, Ground, Treasure, Food, Water
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
#$         #f                             #             #
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

        # Build each map and present it onto the screen in an animated fashion.
        for map_text in maps:
            # Instantiate the Map object and assemble dict of MapObjects.
            game_map = Map()
            map_objects = {
                'vdoor': VerticalDoor,
                'hdoor': HorizontalDoor,
                'wall': Wall,
                'ground': Ground,
                'treasure': Treasure,
                'food': Food,
                'water': Water
            }

            # Populate the Map object with MapObjects.
            MapBuilder.build(map_text, game_map, map_objects)
            # Draw the map!
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
