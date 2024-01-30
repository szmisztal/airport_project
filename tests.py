import pygame
import sys
from airplane import Airplane

airplanes = {}
airplane_1_coords = Airplane.establish_init_airplane_coordinates()
airplane_2_coords = Airplane.establish_init_airplane_coordinates()
airplane_1_obj = Airplane(airplane_1_coords)
airplane_2_obj = Airplane(airplane_2_coords)
airplane_1_obj.id = 1
airplane_2_obj.id = 2
airplane_1 = airplane_1_obj.parse_airplane_obj_to_json()
airplane_2 = airplane_2_obj.parse_airplane_obj_to_json()
airplanes.update(airplane_1)
airplanes.update(airplane_2)
print(airplanes)

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Airport Traffic Visualization")

WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

AIRPORT_WIDTH = 500
AIRPORT_HEIGHT = 500

AIRPORT_X = (SCREEN_WIDTH - AIRPORT_WIDTH) // 2
AIRPORT_Y = (SCREEN_HEIGHT - AIRPORT_HEIGHT) // 2


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    pygame.draw.rect(screen, GREEN, (AIRPORT_X, AIRPORT_Y, AIRPORT_WIDTH, AIRPORT_HEIGHT))
    for airplane_id, airplane_details in airplanes.items():
        airplane_x = airplane_details["coordinates"][0] / 10
        airplane_y = airplane_details["coordinates"][1] / 10
        airplane_z = airplane_details["coordinates"][2] / 10
        print(airplane_x, airplane_y, airplane_z)
        pygame.draw.circle(screen, RED, (airplane_x, airplane_y), 2)
    pygame.display.flip()

pygame.quit()
sys.exit()
