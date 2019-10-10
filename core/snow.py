import random
import pygame
from core.snowflake import Snowflake
from pygame.locals import * 


class Snow:
    def __init__(self, width, height, screen):
        # plethora of fields
        self.width = width
        self.height = height
       
        self.snow_color = (255, 255, 255)
        self.back_snowflakes = []
        self.snowflake_back_counter = 0.0
        self.snowflake_back_frequency = 0.05
        
        self.front_snowflakes = []
        self.snowflake_front_counter = 0.0
        self.snowflake_front_frequency = 0.25
        
        self.snowflake_size = 2
        self.snowflake_line = [height] * width  # for collision detection
        self.wind_chance = 1
        self.wind_strength = 20
        self.show_text = True

        self.snow_surface = pygame.Surface((int(self.width), int(self.height)), flags=SRCALPHA)
        self.snow_surface.fill(pygame.Color("#00000000"))
        self.snow_surface.convert_alpha(screen)

        self.melt_counter = 0.0
        self.melt_freq = 2.5

    def update(self, time_delta):
        # do we need to add more snow?
        if self.snowflake_back_counter < self.snowflake_back_frequency:
            self.snowflake_back_counter += time_delta
        elif self.snowflake_back_counter >= self.snowflake_back_frequency:
            self.snowflake_back_counter = 0.0
            self.snowflake_size = random.randint(2, 3)
            snowflake = Snowflake(len(self.back_snowflakes), self.width, self.height,
                                  self.snowflake_size, self.snow_color)
            self.back_snowflakes.append(snowflake)

        if self.snowflake_front_counter < self.snowflake_front_frequency:
            self.snowflake_front_counter += time_delta
        elif self.snowflake_front_counter >= self.snowflake_front_frequency:
            self.snowflake_front_counter = 0.0
            self.snowflake_size = random.randint(2, 3)
            snowflake = Snowflake(len(self.front_snowflakes), self.width, self.height,
                                  self.snowflake_size, self.snow_color)
            self.front_snowflakes.append(snowflake)
            
        # what about some wind?
        w_chance = random.randint(0, 1000)
        w_strength = 0
        if w_chance <= self.wind_chance:
            w_strength = random.randint(-self.wind_strength, self.wind_strength)
            
        # let it snow, let it snow, let it snow
        for snowflake in self.back_snowflakes:
            if snowflake.enabled:
                if w_strength != 0:
                    snowflake.wind = w_strength
            snowflake.update(time_delta, self.snowflake_line, self.snow_surface)

        for snowflake in self.front_snowflakes:
            if snowflake.enabled:
                if w_strength != 0:
                    snowflake.wind = w_strength
            snowflake.update(time_delta, self.snowflake_line, self.snow_surface)

        self.back_snowflakes[:] = [flake for flake in self.back_snowflakes if not flake.should_die]
        self.front_snowflakes[:] = [flake for flake in self.front_snowflakes if not flake.should_die]

        self.melt_snow(time_delta)

    def melt_snow(self, time_delta):
        if self.melt_counter < self.melt_freq:
            self.melt_counter += time_delta
        elif self.melt_counter >= self.melt_freq:
            self.melt_counter = 0.0
            snow_pxarray = pygame.PixelArray(self.snow_surface)
            random.seed()
            row_num = 0
            for row in self.snowflake_line:
                row_height = row  # self.snowflake_line[row_num]
                neighbour_diff = 0
                for x in range(-3, 3):
                    neighbour_diff += row_height - self.snowflake_line[min(max(row_num+x, 0), self.width-1)]
                                                                                              
                chance_to_melt = (1.0 - (row_height/self.height)) * 5.0 - (neighbour_diff * 0.07)
                rand_melt = random.random()
                if rand_melt <= chance_to_melt:
                    snow_pxarray[row_num, min(row_height, self.height-1)] = pygame.Color("#00000000")
                    self.snowflake_line[row_num] = min(row_height+1, self.height)
                row_num += 1
            del snow_pxarray
            
    def render_back(self, screen):
        screen.blit(self.snow_surface, (0, 0))
        for snowflake in self.back_snowflakes:
            snowflake.draw(screen)

    def render_front(self, screen):
        for snowflake in self.front_snowflakes:
            snowflake.draw(screen)
