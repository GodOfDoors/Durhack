import numpy as np
import pygame
from pygame import surfarray

pygame.init()

width, height = 300, 300
pixel_array = np.zeros((width, height, 3))
pixel_array[:, :, 0] = np.linspace(0, 255, height)
pixel_array[:, :, 1] = np.linspace(0, 255, height)
pixel_array[:, :, 2] = np.linspace(0, 255, height)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame display")
surfarray.blit_array(screen, pixel_array.astype(np.uint8))
pygame.display.flip()

attraction_mat = np.array([[1, 0, 1],
                           [1, 0, -1],
                           [0, 1, 1]])

def attraction():
    """Implements how color chanels attract/repel each other as defined by the attraction matrix.
    The function implements the movement of a channel value symmetrially, so if a channel value
    moves, it is subtracted from the origin pixel's channel and added to the destination pixel's
    channel."""
    delta = np.zeros_like(pixel_array)
    for x in range(width - 1):
        for y in range(height - 1):
            try:
                opr1 = (1/255) * (attraction_mat @ pixel_array[x+1, y]) * pixel_array[x, y]
                opr2 = (1/255) * (attraction_mat @ pixel_array[x, y+1]) * pixel_array[x, y]
            except IndexError:
                pass

            delta[x,   y  ] += opr1 + opr2
            delta[x+1, y  ] -= opr1
            delta[x,   y+1] -= opr2
    return delta

convolution_mat = np.array([[1, 2, 1],
                            [2, 4, 2],
                            [1, 2, 1]])* (1/16)

def convolution():
    """Convolutes over all channels in pixel_array as defined by convolution_mat."""
    new_pixel_array = np.zeros_like(pixel_array)
    for x in range(0, width):
        for y in range(0, height):
            for i in range(3):
                for j in range(3):
                    try:
                        new_pixel_array[x+1, y+1] += convolution_mat[i, j] * pixel_array[x+i, y+j]
                    except IndexError:
                        pass
    return new_pixel_array

def conservative_clip(excess, low=0.0, high=255.0):
    """Clips pixel_array to [low, high], then push the leftover mass back into pixels
    that still have headroom. This function doesn't push into the nearest available pixels.
    This function guarantees the number of each chanel is preserved."""
    clip = np.clip(excess, low, high)
    for ch in range(3):
        err = excess[..., ch].sum() - clip[..., ch].sum()   # net excess (>0) or deficit (<0)
        room = (high - clip[..., ch]) if err > 0 else (clip[..., ch] - low)
        sum_room = room.sum()
        if sum_room > 0:
            clip[..., ch] += err * room / sum_room
        else:
            clip[..., ch] += err / clip[..., ch].size
    return clip

running = True
while running:
    for _ in range(3):
        pixel_array = conservative_clip(pixel_array + attraction())
    pixel_array = convolution()

    surfarray.blit_array(screen, pixel_array.astype(np.uint8))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
