import pygame
from scenes.scene import Scene, GameObject


class SceneThree(Scene):
    def __init__(self, snow_render):
        super().__init__()

        self.background = pygame.Surface((640, 480))
        self.background = pygame.image.load("scenes/city_background.png")
        self.background = self.background.convert()

        self.text_colour = pygame.Color("#141414")
        self.background_colour = pygame.Color("#F0F0F0")

        # set id
        self.id = "scene_3"

        # create exits
        self.exit_north = "scene_1"

        self.door_open = False

        # create objects
        button = GameObject()
        button.name = "button"
        button.aliases.append("red button")
        button.aliases.append("big red button")
        button.detailed_description = "It's a tempting big red button."
        self.objects.append(button)

        panel = GameObject()
        panel.name = "panel"
        panel.aliases.append("display panel")
        panel.aliases.append("electronic display panel")
        panel.aliases.append("small electronic display panel")
        panel.detailed_description = ("The panel reads: 7,456,292,324/7,456,292,325"
                                      "<br><br>"
                                      "One unit still missing."
                                      "<br><br>"
                                      "Project N.P. Closed until issue resolved.")
        self.objects.append(panel)

        self.snow_render = snow_render

    def update(self, time_delta):
        self.snow_render.update(time_delta)

    def render_back(self, screen):
        self.snow_render.render_back(screen)
        
    def render_front(self, screen):
        self.snow_render.render_front(screen)
    
    def get_description(self, player):
        description = ("The alley continues for awhile before reaching a dead end at a windowless building."
                       " The main feature of the building is a new-looking door set into a steel door frame."
                       "<br><br>"
                       "Moonlight is the main source of light here, this far from the street lights, which makes"
                       " it easy to make out a <b>small electronic display panel</b> glowing next to the door."
                       "<br><br>"
                       "There is a <b><font color=#AA0000>big red button</font></b> set directly underneath the panel."
                       "<br><br>")
        
        if self.door_open:
            description += ("The door is currently open."
                            "<br><br>")
        else:
            description += ("The door is currently closed."
                            "<br><br>")
            
        description += "Other than the door to the South, there is an exit to the North back down the alley."
        if player.returned_drone:
            for obj in self.objects:
                if obj.name == "panel":
                    obj.detailed_description = "All systems normal. Project N.P. is awaiting operator"
        return description

    def activate_object(self, object_to_activate, player):
        description = "nothing much happens"
        if object_to_activate.name == "button":
            if player.returned_drone:
                description = "You press the button and the door slides open. You can now head south into the building."
                self.door_open = True
                self.exit_south = "scene_4"
            else:
                description = ("You limber up your finger and prepare yourself mentally for excitement. It's not "
                               "every day you get to press a big, red button."
                               "<br><br>"
                               "Sadly, reality fails to live up to"
                               " your dreams and nothing happens when you hit the button. Not even when you press it,"
                               " like, fifteen times to be sure.")

        result = (self, description, player)
        return result
