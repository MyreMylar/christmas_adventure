import pygame
from scenes.scene import Scene, GameObject


class DroneObject(GameObject):
    def __init__(self):
        super().__init__()
        self.half_fixed = False
        self.fixed = False

    def combine(self, object_to_combine_with, scene, inventory):
        if object_to_combine_with.name == "propeller" and not self.half_fixed:
            self.half_fixed = True
            description = ("You attach the propeller onto the drone loosely. It'll fall off again if the screw "
                           "isn't tightened.")
            self.detailed_description = ("The drone now has four propellers again, but one of them is still loose."
                                         " It's not safe to fly yet.")
            self.activate_description = "Not without tightening the loose screw."
            inventory[:] = [x for x in inventory if not (x.name == object_to_combine_with.name)]
            return True, scene, inventory, description
        elif object_to_combine_with.name == "screwdriver" and self.half_fixed and not self.fixed:
            self.fixed = True
            self.should_remove_on_activate = True
            description = ("You tighten the screw holding the loose propeller. The little LED on the side of the case"
                           " flicks to green. Perhaps you should activate it now?")
            self.detailed_description = "The drone looks as good as new"
            self.activate_description = ("You throw the drone gently in the air and it catches itself hovering steady"
                                         " for a moment. Then suddenly it whizzes off high into the sky.")
            return True, scene, inventory, description
        else:      
            return super().combine(object_to_combine_with, scene, inventory)

    def set_player_flag_on_activate(self, player):
        if self.fixed:
            player.returned_drone = True
        return player


class SceneOne(Scene):
    def __init__(self, snow_render):
        super().__init__()

        self.background = pygame.Surface((640, 480))
        self.background = pygame.image.load("scenes/city_background.png")
        self.background = self.background.convert()

        self.text_colour = pygame.Color("#141414")
        self.background_colour = pygame.Color("#F0F0F0")

        # set id
        self.id = "scene_1"

        # create exits
        self.exit_north = "scene_2"
        self.exit_south = "scene_3"
        
        # create scene objects
        drone = DroneObject()
        drone.pick_upable = True
        drone.name = "drone"
        drone.aliases.append("quadcopter")
        drone.aliases.append("quadcopter drone")
        drone.detailed_description = ("A sleek, green quadcopter drone with a damaged rotor. An LED flashes silently on"
                                      " the side of the case, there is a small switch next to it. Peering more closely"
                                      " at it you can make out lettering engraved on the plastic case. Three letters;"
                                      " 'E', 'L' and 'F'.")
        drone.activate_description = ("Toggling the switch off and on deactivates the LED but nothing else happens."
                                      "The three remaining rotors do not spin. ")
        self.objects.append(drone)

        snow = GameObject()
        snow.name = "snow"
        snow.aliases.append("snowflakes")
        snow.detailed_description = ("The snow drifts lazily to the ground. It's been another mild winter, this is the"
                                     " first snow you've seen for years")
        self.objects.append(snow)
        self.snow_render = snow_render

    def update(self, time_delta):
        self.snow_render.update(time_delta)

    def render_back(self, screen):
        self.snow_render.render_back(screen)
        
    def render_front(self, screen):
        self.snow_render.render_front(screen)

    def get_description(self, player):

        description = ("It is the night before Christmas Eve. The sun set a few hours ago but you can still make"
                       " out your surroundings thanks to the orange glow of an old street light. The walls, that"
                       " make up the sides of the alley you stand in, loom above you - their exact height, far out"
                       " of sight above."
                       "<br><br>"
                       "<b>Snowflakes</b> fall gently all around."
                       "<br><br>")

        for obj in self.objects:
            if obj.name == "drone":
                description += ("There is a light coating of snow on the concrete of the alley's floor, but not enough"
                                " to conceal the object directly in front of you. Which is the only thing, at first"
                                " glance, that is obviously entirely out of place. It is a <b>quadcopter drone</b>. "
                                "One of the rotors is missing and a red LED flashes silently illuminating the nearby "
                                "snow."
                                "<br><br>")
                       
        description += "There are exits to the north and south"
                       
        return description

    def activate_object(self, object_to_activate, player):
        description = "nothing much happens"

        if object_to_activate.name == "snow":
            description = "You try to catch some snow on your tongue"
        if object_to_activate.name == "drone":
            description = "You should probably try and pick it up before fiddling with it."
        
        result = (self, description, player)
        return result
