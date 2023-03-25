import math

import pygame
from settings import colors, G, HEIGHT, WIDTH, AU


class Planet:
    SCALE = 200 / AU
    TIME_STEP = 3600 * 24

    def __init__(self, x, y, r, m, color):
        self.x = x
        self.y = y
        self.r = r
        self.m = m
        self.color = color

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, window):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(window, self.color, False, updated_points, 2)

        if not self.sun:
            distance_text = pygame.font.SysFont("arial", 14).render(
                f"{round(self.distance_to_sun/1000, 1)}km", 1, colors.WHITE
            )
            window.blit(distance_text, (x + self.r + 2, y + self.r + 2))

        pygame.draw.circle(window, self.color, (x, y), self.r)

    def attraction(self, object):
        other_x = object.x
        other_y = object.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y

        distance = math.sqrt(distance_x**2 + distance_y**2)

        if object.sun:
            self.distance_to_sun = distance

        force = G * self.m * object.m / distance**2
        alpha = math.atan2(distance_y, distance_x)

        force_x = math.cos(alpha) * force
        force_y = math.sin(alpha) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0

        for planet in planets:
            if planet == self:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.m * self.TIME_STEP
        self.y_vel += total_fy / self.m * self.TIME_STEP

        self.x += self.x_vel * self.TIME_STEP
        self.y += self.y_vel * self.TIME_STEP
        self.orbit.append((self.x, self.y))
