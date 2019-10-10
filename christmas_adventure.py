import os

from core.text_render import render_adventure_text
from core.functions import show_inventory, try_scene_change, examine_object
from core.functions import take_object, activate_object, combine_objects
from core.core_strings import get_instructions
from core.setup import setup_starting_inventory
from core.snow import Snow
import scenes.scene_one as s1
import scenes.scene_two as s2
import scenes.scene_three as s3
import scenes.scene_four as s4

import pygame
from pygame.locals import *


# ---------------------------------------
# Scroll down to line 63 for Challenge 1!
# ---------------------------------------
class Player:
    def __init__(self):
        self.returned_drone = False
        self.game_over = False


pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.display.set_caption('A Christmas Adventure')
screen = pygame.display.set_mode((640, 480))

background_colour = pygame.Color("#F0F0F0")

snow_render = Snow(640, 480, screen)

have_started = False
scenes = []
scene_1 = s1.SceneOne(snow_render)
scenes.append(scene_1)
scenes.append(s2.SceneTwo(snow_render))
scenes.append(s3.SceneThree(snow_render))
scenes.append(s4.SceneFour())
active_scene = scene_1
inventory = []

inventory = setup_starting_inventory(inventory)

player = Player()


# ---------------------------------------------------------------------------------
# This code parses inputted text to try and find usable game commands
#
# The functions 'inputText' variable is a string with all the letters of
# keyboard input the player has entered since the last press of the 'enter' key.
# ---------------------------------------------------------------------------------
def parse(input_text):
    command = input_text
    object1 = None
    object2 = None

    # --------------------------------------------------------------------------------------
    # Challenge 1
    # -------------
    #
    # Properly handle upper case player input. Right now the parser only deals with
    # lower case letters, if you turn on caps lock, or add some capital letters with shift,
    # it won't be able to understand you.
    #
    # Try the .lower() method on the input text to change all input into lower case.
    #
    # Hints:
    #
    # - You can find more documentation on the string .lower() function
    #   at this link: http://www.tutorialspoint.com/python/string_lower.htm
    #
    # ----------------------------------------
    # Challenge 2 is on line 85!
    # --------------------------------------------------------------------------------------

    # the .split() function splits the input_text string variable into a python list of individual words
    words = input_text.split()

    # ---------------------------------------------------------------------------------------
    # Challenge 2
    # -------------
    #
    # See if you can change the parser so that it understands four new synonyms
    # for the current commands.
    # 
    # For example:
    # - 'study' or 'inspect' could be used for 'examine'
    # - 'pick up' could be used for 'take'
    # - 'press', 'use' or 'operate' could be used for 'activate'
    # ---------------------------------------
    #  See if you can beat the text adventure or, add a new scene!
    # ----------------------------------------------------------------------
    if len(words) > 0:        
        found_examine_words = False
        remaining_words_index = 0
        if words[0] == "examine":
            remaining_words_index = 1
            found_examine_words = True
        if words[0] == "look" and words[1] == "at":
            remaining_words_index = 2
            found_examine_words = True
            
        if found_examine_words:
            if len(words) > remaining_words_index:
                remaining_words = ""
                for i in range(remaining_words_index, len(words)):
                    remaining_words += words[i]
                    if i < len(words)-1:
                        remaining_words += " "
                command = "examine"
                object1 = remaining_words

        if (words[0] == "take") and len(words) > 1:
            remaining_words = ""
            for i in range(1, len(words)):
                remaining_words += words[i]
                if i < len(words)-1:
                    remaining_words += " "
            command = "take"
            object1 = remaining_words

        if ((words[0] == "activate") or (words[0] == "press")) and len(words) > 1:
            remaining_words = ""
            for i in range(1, len(words)):
                remaining_words += words[i]
                if i < len(words)-1:
                    remaining_words += " "
            command = "activate"
            object1 = remaining_words
        
        if (words[0] == "use" or words[0] == "combine") and len(words) > 3:
            # find linking preposition between objects
            for i in range(1, len(words)):
                if words[i] == "on" or words[i] == "with":
                    object1 = ""
                    for j in range(1, i):
                        object1 += words[j]
                        if j < i-1:
                            object1 += " "
                    object2 = ""
                    for k in range(i+1, len(words)):
                        object2 += words[k]
                        if k < len(words)-1:
                            object2 += " "
            command = "combine"

    return command, object1, object2


def process_command(command, object1, object2):
    global have_started
    global active_scene
    global inventory
    global player
    
    output = "Press enter to begin"
    if have_started:
        output = "Command not understood"
    
    if command == "":
        active_scene.reset_fade_timer()
        output = active_scene.get_description(player)
        if not have_started:
            active_scene.reboot_scene()
            have_started = True
        else:
            active_scene.is_first_visit = False
    elif command == "help":
        output = get_instructions()
    elif have_started:
        if command == "inventory":
            output = show_inventory(inventory)
        elif command == "north" or command == "south" or command == "east" or command == "west":
            result = try_scene_change(active_scene, scenes, command, player)
            active_scene = result[0]
            output = result[1]
        elif command == "examine":
            if object1 is not None:
                output = examine_object(active_scene, inventory, object1)
            else:
                output = "Examine what?"
        elif command == "take":
            if object1 is not None:
                result = take_object(active_scene, inventory, object1)
                active_scene = result[0]
                inventory = result[1]
                output = result[2]
            else:
                output = "take what?"
        elif command == "activate":
            if object1 is not None:
                result = activate_object(active_scene, inventory, object1, player)
                active_scene = result[0]
                inventory = result[1]
                player = result[2]
                output = result[3]
            else:
                output = "activate what?"
        elif command == "combine":
            if object1 is not None and object2 is not None:
                result = combine_objects(active_scene, inventory, object1, object2)
                active_scene = result[0]
                inventory = result[1]
                output = result[2]
            else:
                output = "Combination - utter failure"

    return output


font = pygame.font.Font("data/Gabriola.ttf", 18)
bold_font = pygame.font.Font("data/Gabriola.ttf", 18)
bold_font.set_bold(True)
italic_font = pygame.font.Font("data/Gabriola.ttf", 18)
italic_font.set_italic(True)
header_font = pygame.font.Font("data/AGENCYB.TTF", 18)


adventure_output = "[h]A Christmas Adventure[/h]\n\nType 'help' for instructions\n\nPress enter to begin"
entered_keys = ""

running = True
clock = pygame.time.Clock()

while running:
    frameTime = clock.tick(60)
    time_delta = frameTime / 1000.0
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                if player.game_over:
                    running = False
                else:
                    parsed_command = parse(entered_keys)
                    adventure_output = process_command(parsed_command[0], parsed_command[1], parsed_command[2])
                    entered_keys = ""
            elif event.key == K_BACKSPACE:
                if len(entered_keys) > 0:
                    entered_keys = entered_keys[:-1]
            else:
                entered_keys += event.unicode

    active_scene.update(time_delta)
    screen.blit(active_scene.background, (0, 0))  # draw the background

    active_scene.render_back(screen)
    render_adventure_text(screen, adventure_output, entered_keys, font, bold_font, italic_font, header_font,
                          active_scene, player, time_delta)
    active_scene.render_front(screen)
    
    pygame.display.flip()  # flip all our drawn stuff onto the screen

pygame.quit()  # exited game loop so quit pygame
