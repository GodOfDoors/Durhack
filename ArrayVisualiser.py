import pygame
import numpy as np
from pygame import surfarray
import PixelArrayRules
import time
import Drip
import UserInterface as ui
# Create a function to update the image

# initializing Pygame
pygame.init()


width, height = 800, 600
# initialize the test pixel array
pixel_array = np.zeros((width, height, 3))
pixel_array[:, :, 0] = np.linspace(0, 255, height)  # Green gradient
pixel_array[:, :, 1] = np.linspace(0, 255, height)  # Green gradient
pixel_array[:, :, 2] = np.linspace(0, 255, height)  # Green gradient

# initialize the Pygame display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame display")

screen_ui = pygame.display.set_mode((640, 480))
screen_ui.fill((20, 20, 20))

# map pixel array to screen
surfarray.blit_array(screen, pixel_array)
# updates display
pygame.display.flip()

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

# define UI interface
attraction_grid = ui.InteractiveMatrix(0, 0, 200)
convolution_grid = ui.InteractiveMatrix(250, 0, 200)

# render UI
def render_ui():
    screen_ui.fill((20, 20, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        for object in objects:
            if hasattr(object, 'handle_event'):
                object.handle_event(event)

    for object in objects:
        object.process()

    pygame.display.flip()


# test image
temp = pygame.image.load("Test Image.jpg")
temp = alterImageSizeToFitScreen(temp)


# allows user to exit
running = True
print("Starting Simulation")
while running:
    render_ui()
    print("Display")
    time.sleep(0.1)

#    Del = np.insert(PixelArrayRules.Radiate(150, 10, 3, 5, np.delete(temp, [True,False,True], 2)),0, 0, 2)
#    Del = np.insert(Del,2, 0, 2)
#    temp = temp + Del
    temp = Drip.Drip(temp,200,40)
    surfarray.blit_array(screen, temp)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
