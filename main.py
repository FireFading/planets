import pygame

from planet import Planet

from settings import AU, colors, FPS, HEIGHT, WIDTH

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System")


def planets_list():
    sun = Planet(0, 0, 30, 1.98892 * 10**30, colors.YELLOW)
    sun.sun = True

    earth = Planet(-1 * AU, 0, 16, 5.9742 * 10**24, colors.BLUE)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * AU, 0, 12, 6.39 * 10**23, colors.RED)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(-0.387 * AU, 0, 8, 0.330 * 10**24, colors.GRAY)
    mercury.y_vel = 47.4 * 1000

    venus = Planet(-0.723 * AU, 0, 14, 4.8685 * 10**24, colors.WHITE)
    venus.y_vel = 35.02 * 1000

    return [sun, earth, mars, mercury, venus]


def main():
    run = True
    clock = pygame.time.Clock()

    planets = planets_list()
    is_scaled = 0
    is_timesteped = 0
    is_orbit = 1

    while run:
        clock.tick(FPS)
        window.fill(colors.BLACK)

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
                    Planet.TIME_STEP *= 0.99
                    is_timesteped = -1

                if event.key == pygame.K_RIGHT:
                    Planet.TIME_STEP *= 1.01
                    is_timesteped = 1

                if event.key == pygame.K_o:
                    is_orbit *= -1

                if event.key == pygame.K_SPACE:
                    planets = planets_list()
                    window.fill(colors.BLACK)
                    is_scaled = 0
                    is_timesteped = 0
                    Planet.SCALE = 200 / Planet.AU
                    Planet.TIME_STEP = 3600 * 24

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    is_scaled = 0

                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    is_timesteped = 0

        if is_scaled == 1:
            Planet.SCALE *= 1.01
            for planet in planets:
                planet.r *= 1.01
        elif is_scaled != 0:
            for planet in planets:
                planet.r *= 0.99
            Planet.SCALE *= 0.99

        if is_timesteped == 1:
            Planet.TIME_STEP *= 1.01
        elif is_scaled != 0:
            Planet.TIME_STEP *= 0.99

        if is_orbit == -1:
            for planet in planets:
                planet.orbit = []

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
