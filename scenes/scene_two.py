import pygame
from scenes.scene import Scene, GameObject


class SceneTwo(Scene):
    
    def __init__(self, snow_render):
        super().__init__()

        self.background = pygame.Surface((640, 480))
        self.background = pygame.image.load("scenes/city_background.png")
        self.background = self.background.convert()

        self.text_colour = pygame.Color("#141414")
        self.background_colour = pygame.Color("#F0F0F0")

        # set id
        self.id = "scene_2"

        # create exits
        self.exit_south = "scene_1"
        
        # propeller fate
        self.b_discovered_propeller_fate = False

        # create scene objects
        poster = GameObject()
        poster.pick_upable = False
        poster.name = "poster"
        poster.aliases.append("ripped poster")
        poster.aliases.append("torn poster")
        poster.detailed_description = ("Looking more closely at the poster you can see it is for the latest Marvel "
                                       "film - '<i>Doomworld</i>'. The most interesting thing about it though, is the "
                                       "rip itself, it's been made in small rhythmic sections rather than a "
                                       "single tear. "
                                       "<br><br>"
                                       "<i>This was done by a machine.</i>"
                                       "<br><br>"
                                       "Examining the area of wall around the poster reveals some green marks that "
                                       "match the case of the drone from the alley. You are convinced the drone hit "
                                       "the wall here, and probably lost it's propeller at the same time."
                                       "<br><br>"
                                       "You can't see the propeller on the ground.")
        poster.activate_description = ("This poster doesn't have one of those built in animations when you wave your "
                                       "hand in front of it. You're not sure if this is because of the damage, or "
                                       "because it's just a cheap poster.")
        self.objects.append(poster)
        
        shops = GameObject()
        shops.name = "shops"
        shops.aliases.append("shop fronts")
        shops.detailed_description = ("It's not really late enough for shops to be closed, you assume that these"
                                      " particular shops are always closed. VR shopping hasn't made it any easier"
                                      " for the high street.")
        self.objects.append(shops)

        rubbish_bin = GameObject()
        rubbish_bin.name = "bin"
        rubbish_bin.aliases.append("rubbish bin")
        rubbish_bin.detailed_description = ("It's a rubbish bin. You don't want to poke around in it without"
                                            " good reason.")
        self.objects.append(rubbish_bin)

        cleanbot = GameObject()
        cleanbot.name = "cleanbot"
        cleanbot.aliases.append("clean bot")
        cleanbot.aliases.append("robot")
        cleanbot.detailed_description = ("It's a Cleanbot. They are everywhere, a fact of life, and old people are"
                                         " constantly complaining about them.")
        self.objects.append(cleanbot)

        cookievend = GameObject()
        cookievend.name = "cookievend"
        cookievend.aliases.append("cookie-vend")
        cookievend.aliases.append("cookie vend")
        cookievend.aliases.append("vending machine")
        cookievend.detailed_description = ("Mmm Cookie-Vend cookies. Not the healthiest snack, but who cares? You "
                                           "wish you had your Pay-Band... Or any money on your Pay-Band")
        self.objects.append(cookievend)

        self.snow_render = snow_render

    def update(self, time_delta):
        self.snow_render.update(time_delta)

    def render_back(self, screen):
        self.snow_render.render_back(screen)
        
    def render_front(self, screen):
        self.snow_render.render_front(screen)
        
    def get_description(self, player):
        description = ("The alley mouth opens out onto a quiet street. A few closed <b>shop fronts</b> are visible"
                       " across the road. Heading east down the street would take you home, but you feel that there"
                       " is still something left undone here."
                       "<br><br>"
                       "There is a <b>Cleanbot</b> silently patrolling up"
                       " and down the pavement on this side of the road, its sensors alert for any rubbish. To the"
                       " right of the alley mouth is the <b>bin</b> in which the Cleanbot deposits what it finds. "
                       "To the left of the alley mouth is a <b>Cookie-Vend</b>, the glow of it's holographic display"
                       " adding to the colour from the street lights."
                       "<br><br>"
                       )
        for obj in self.objects:
            if obj.name == "poster":
                description += ("There is a <b>ripped poster</b> next to the vending machine, right on the corner "
                                "of the alley mouth."
                                "<br><br>")
            if obj.name == "propeller":
                description += "There is a <b>propeller</b> in the bin." \
                               "<br><br>"

        description += "There is an exit to the south - back up the alley."
        
        return description

    def examine_object(self, object_name):
        if object_name == "poster":
            self.b_discovered_propeller_fate = True
            for obj in self.objects:
                if obj.name == "bin":
                    obj.detailed_description = ("You are convinced the propeller must have ended up in the bin. "
                                                "Steeling your nose, you poke around inside for a while, until your "
                                                "prize is revealed. There is a quadcopter propeller in the bin")
                if obj.name == "cleanbot":
                    obj.detailed_description = ("If you know cleanbots, and you do, it probably scooped up the fallen"
                                                " propeller from the drone and deposited it in the bin.")
        if object_name == "bin" and self.b_discovered_propeller_fate:
            propeller = GameObject()
            propeller.name = "propeller"
            propeller.aliases.append("quadcopter propeller")
            propeller.pick_upable = True
            propeller.detailed_description = ("A Propeller for a quadcopter. It looks to be intact, even the little"
                                              " screw that attaches it to the drone is still in place.")
            self.objects.append(propeller)
