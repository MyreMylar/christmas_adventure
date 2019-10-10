import random
import pygame.gfxdraw


class Snowflake:
    def __init__(self, uid, width, height, radius, color):
        self.uid = uid
        self.width = width
        self.height = height
        self.radius = radius
        self.color = color
        self.gravity = random.uniform(5, 15)
        self.pos = [random.randint(-50, self.width+50), 0]
        self.enabled = True
        self.wind = 0
        self.speed = random.uniform(1.0, 2.0)
        self.melt_time = random.uniform(35.0, 70.0)
        self.should_die = False

    def update(self, time_delta, snowflake_line, snow_surface):
        if self.enabled:  
            speed = time_delta * self.speed
            if not self.collision_check(snow_surface, snowflake_line):
                self.pos[1] += self.gravity * speed
            else:
                self.should_die = True
            if self.wind != 0:
                w = ((self.wind/self.radius) * time_delta)
                self.pos[0] += w
                # self.wind -= w

    def collision_check(self, snow_surface, snowflake_line):        
        # check if it's hit the resting snow
        x = int(self.pos[0])
        y = int(self.pos[1])
        r = self.radius

        points = snowflake_line[x-r:x+r]
        lowest_point = 0

        collided = False
        for p in points:
            if y >= p:
                collided = True
                for i in range(x-r, x+r):
                    if 0 <= i < self.width:
                        if snowflake_line[i] > lowest_point:
                            lowest_point = snowflake_line[i]
                            
        # check if it's on the bottom of the screen
        if self.pos[1] >= self.height:
            collided = True

        if collided:
            snow_pxarray = pygame.PixelArray(snow_surface)
            for i in range(x-r, x+r):
                if 0 <= i < self.width:
                    if snowflake_line[i] == lowest_point:
                        snowflake_line[i] = snowflake_line[i]-2
                        snow_pxarray[i, snowflake_line[i]+1] = pygame.Color("#FFFFFFFF")
                        snow_pxarray[i, snowflake_line[i]] = pygame.Color("#FFFFFFFF")
                    else:
                        diff = lowest_point - snowflake_line[i]
                        if diff < 2:
                            snowflake_line[i] = snowflake_line[i]-1
                            snow_pxarray[i, snowflake_line[i]] = pygame.Color("#FFFFFFFF")
                        
                    # Add more snow in the middle
                    if i == x or i == x-1 or i == x+1:
                        snowflake_line[i] = snowflake_line[i]-1
                        snow_pxarray[i, snowflake_line[i]] = pygame.Color("#FFFFFFFF")

            del snow_pxarray

        return collided                 

    def draw(self, surface):
        pygame.gfxdraw.filled_circle(surface, int(self.pos[0]), int(self.pos[1]), self.radius, self.color)        
        pygame.gfxdraw.aacircle(surface, int(self.pos[0]), int(self.pos[1]), self.radius, self.color)
