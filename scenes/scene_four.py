import pygame
from scenes.scene import Scene, GameObject


class SceneFour(Scene):
    def __init__(self):
        super().__init__()

        self.background = pygame.Surface((640, 480))
        self.background = pygame.image.load("scenes/server_room.png")
        self.background = self.background.convert()

        self.text_colour = pygame.Color("#F0F0F0")
        self.background_colour = pygame.Color("#141414")

        # set id
        self.id = "scene_4"

        # setup exits
        self.exit_north = "scene_3"
      
        santa = GameObject()
        santa.name = "display"
        santa.aliases.append("large display")
        santa.aliases.append("computer")
        santa.aliases.append("santa")
        santa.aliases.append("s.a.n.t.a")
        santa.aliases.append("ai")
        santa.detailed_description = ("Getting close to the display allows you to see a small silver plate in front"
                                      " of it and to read the words written on it:\n\n"
                                      "Super\n"
                                      "Accelerated\n"
                                      "Noel\n"
                                      "Transportation\n"
                                      "Algorithm\n\n"
                                      "[b]<AUTHORIZATION REQUIRED>[/b]\n")
        self.objects.append(santa)

    def update(self, time_delta):
        pass

    def render_back(self, screen):
        pass
        
    def render_front(self, screen):
        pass

    def get_description(self, player):
        description = ("As you enter through the door, lights flick on showing a large room, with an exceptionally "
                       "high ceiling.\n\n Giant steel grey boxes line all four walls climbing right to the ceiling."
                       " LEDs on each of the boxes flicker on and off intermittently.\n\n The center of the room is "
                       "taken up by a [b]large display[/b] mounted on a pillar-like plinth so that it is at head "
                       "height. There appear to be letters on the screen.\n\n Apart from the door you came in through "
                       "in the North, there are no other exits.")
        return description

    def activate_object(self, object_to_activate, player):
        description = "nothing much happens"

        if object_to_activate.name == "display":
            player.game_over = True
            description = ("As you move to touch the display, the sound cuts out and your vision goes white.\n\n"
                           "giant letters dance in front of your eyes:\n\n"
                           "[b]GAME OVER.[/b]\n\n"
                           "[i](To be continued....?)[/i]")
        result = (self, description, player)
        return result
