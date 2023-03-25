from dataclasses import dataclass


WIDTH, HEIGHT = 800, 800
FPS = 60

AU = 149.6e6 * 1000
G = 6.67428e-11
SCALE = 200 / AU
TIME_STEP = 3600 * 24


@dataclass
class Colors:
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    BLUE = (100, 149, 237)
    RED = (188, 39, 13)
    GRAY = (80, 71, 78)
    BLACK = (0, 0, 0)


colors = Colors()
