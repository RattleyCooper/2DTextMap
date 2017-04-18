import curses
from editor import Map, MapBuilder
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
            'floor': Ground,
            'treasure': Treasure,
            'food': Food,
            'water': Water
        }

        #
        MapBuilder.build(map_text, game_map, map_objects)

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
