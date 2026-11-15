import pygame
import numpy as np
from pygame import surfarray
import PixelArrayRules
import time
import Drip
import UserInterface as ui
import sys
# Create a function to update the image

# initializing Pygame
pygame.init()


width, height = 800, 600
# initialize the test pixel array
# pixel_array = np.zeros((width, height, 3))
# pixel_array[:, :, 0] = np.linspace(0, 255, height)  # Green gradient
# pixel_array[:, :, 1] = np.linspace(0, 255, height)  # Green gradient
# pixel_array[:, :, 2] = np.linspace(0, 255, height)  # Green gradient

# initialize the Pygame display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame display")

screen_ui = pygame.display.set_mode((640, 480))
screen_ui.fill((20, 20, 20))


# map pixel array to screen
# surfarray.blit_array(screen, pixel_array)
# updates display
# pygame.display.flip()

# Function to alter image size to fit (with black borders if necessary)
# input image surface object (already loaded image)
# width, height
def alterImageSizeToFitScreen(image_surface):
    img_height = image_surface.get_height()
    img_width = image_surface.get_width()

    # if image height bigger
    if img_height > img_width:
        scale_amount = img_height / height
        image_surface = pygame.transform.scale_by(image_surface, (width, height))
        start_draw_at = (width / 2) - (img_width - 2)   # centre the image
        screen.blit(image_surface, (start_draw_at, 0))
    # if image width bigger (or they the same)
    else:
        scale_amount = img_width / width
        image_surface = pygame.transform.scale(image_surface, (width, height))
        img_height = image_surface.get_height()
        start_draw_at = (height / 2) - (img_height / 2)   # centre the image
        screen.blit(image_surface, (0, start_draw_at))

    surf_array = pygame.surfarray.array3d(image_surface)
    pygame.display.flip()
    return surf_array


# render UI
def render_ui():
    screen_ui.fill((20, 20, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        for object in ui.objects:
            if hasattr(object, 'handle_event'):
                object.handle_event(event)

    for object in ui.objects:
        object.process()

    pygame.display.flip()


# test image
global temp 
temp = pygame.image.load("Test Image.jpg")
temp = alterImageSizeToFitScreen(temp)


def Exit():
    global temp
    print("Starting")
    screen = pygame.display.set_mode((800, 600))
    running = True
    while running:

        if not np.any(radiate_vec) == 0:
            Del = np.insert(PixelArrayRules.Radiate((radiate_vec[0]),(radiate_vec[1]),(radiate_vec[2]),(radiate_vec[3]), np.delete(temp, [False,True,True], 2)),1, 0, 2)
            Del = np.insert(Del,1, 0, 2)
            temp = temp + Del

        if not np.any(drip_vec) == 0:
            temp = Drip.Drip(temp,drip_vec[0],drip_vec[1])

        if not np.any(attraction_grid) == 0:
            temp = PixelArrayRules.attraction(temp,attraction_grid)

        if not np.any(convolution_grid) == 0:
            temp = PixelArrayRules.convolution(temp,convolution_grid)

        surfarray.blit_array(screen, temp)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()


# define UI interface
attraction_grid = ui.InteractiveMatrix(30, 30, 200)
convolution_grid = ui.InteractiveMatrix(360, 30, 200)
run_button = ui.Button(555,360,60,40,"Run",Exit,True)
radiate_vec = ui.InteractiveVector(30, 340, 210, 385, 340, np.zeros(4))
drip_vec = ui.InteractiveVector(30, 420, 210, 385, 420, np.zeros(2))
# allows user to exit
running = True
condition = True
print("Starting Simulation")
while running:
    render_ui()
    time.sleep(0.1)
