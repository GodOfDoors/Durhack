import pygame
import numpy as np
from pygame import surfarray
import PixelArrayRules

# Create a function to update the image

# initializing Pygame
pygame.init()


width, height = 200, 150
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

# test image
temp = pygame.image.load("Test Image.jpg")
temp = alterImageSizeToFitScreen(temp)


# allows user to exit
running = True
while running:
    Del = np.insert(PixelArrayRules.Radiate(150, 10, 4, 5, np.delete(temp, [True,False,True], 2)),0, 0, 2)
    Del = np.insert(Del,2, 0, 2)
    temp = temp + Del
    surfarray.blit_array(screen, temp)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()