from this import d
import pygame
import math


WIDTH, HEIGHT = 800, 800
FPS = 60
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 13)
GRAY = (80, 71, 78)
BLACK = (0, 0, 0)

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System")


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 200 / AU
    TIMESTEP = 3600 * 24
    
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
            distance_text = pygame.font.SysFont("arial", 14).render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
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
        
        force = self.G * self.m * object.m / distance**2
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
        
        self.x_vel += total_fx / self.m * self.TIMESTEP
        self.y_vel += total_fy / self.m * self.TIMESTEP
        
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def planets_list():
    sun = Planet(0, 0, 30, 1.98892 * 10**30, YELLOW)
    sun.sun = True
    
    earth = Planet(-1 * Planet.AU, 0, 16, 5.9742 * 10**24, BLUE)
    earth.y_vel = 29.783 * 1000 
    
    mars = Planet(-1.524 * Planet.AU, 0, 12, 6.39 * 10**23, RED)
    mars.y_vel = 24.077 * 1000
    
    mercury = Planet(-0.387 * Planet.AU, 0, 8, 0.330 * 10**24, GRAY)
    mercury.y_vel = 47.4 * 1000
    
    venus = Planet(-0.723 * Planet.AU, 0, 14, 4.8685 * 10**24, WHITE)
    venus.y_vel = 35.02 * 1000
    
    planets = [sun, earth, mars, mercury, venus]
    return planets


def main():
    run = True
    clock = pygame.time.Clock()
    
    planets = planets_list()
    is_scaled = 0
    is_timesteped = 0
    is_orbit = 1
    
    while run:
        clock.tick(FPS)
        window.fill(BLACK)
        
        for planet in planets:
            planet.update_position(planets)
            planet.draw(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    Planet.SCALE *= 1.01
                    for planet in planets:
                        planet.r *= 1.01
                    is_scaled = 1
                
                if event.key == pygame.K_DOWN:
                    Planet.SCALE *= 0.99
                    for planet in planets:
                        planet.r *= 0.99
                    is_scaled = -1
                
                if event.key == pygame.K_LEFT:
                    Planet.TIMESTEP *= 0.99
                    is_timesteped = -1
                
                if event.key == pygame.K_RIGHT:
                    Planet.TIMESTEP *= 1.01
                    is_timesteped = 1
                    
                if event.key == pygame.K_o:
                    is_orbit *= -1
            
                if event.key == pygame.K_SPACE:
                    planets = planets_list()
                    window.fill(BLACK)
                    is_scaled = 0
                    is_timesteped = 0
                    Planet.SCALE = 200 / Planet.AU
                    Planet.TIMESTEP = 3600 * 24
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    is_scaled = 0
                
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    is_timesteped = 0
            
        if is_scaled != 0:
            if is_scaled == 1:
                Planet.SCALE *= 1.01
                for planet in planets:
                        planet.r *= 1.01
            else:
                for planet in planets:
                        planet.r *= 0.99
                Planet.SCALE *= 0.99
            
        if is_timesteped != 0:
            if is_timesteped == 1:
                Planet.TIMESTEP *= 1.01
            else:
                Planet.TIMESTEP *= 0.99
                
        if is_orbit == -1:
            for planet in planets:
                planet.orbit = []
                
        pygame.display.update()
                
    pygame.quit()
    

main()