import pygame
import numpy as np
from pygame import surfarray

# Create a function to update the image

# initializing Pygame
pygame.init()


width, height = 400, 300
# initialize the test pixel array
pixel_array = np.zeros((width, height, 3))
pixel_array[:, :, 0] = np.linspace(0, 255, height)  # Green gradient
pixel_array[:, :, 1] = np.linspace(0, 255, height)  # Green gradient
pixel_array[:, :, 2] = np.linspace(0, 255, height)  # Green gradient

# initialize the Pygame display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame display")

# map pixel array to screen
surfarray.blit_array(screen, pixel_array)
# updates display
pygame.display.flip()

# allows user to exit
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()