# Drip

import numpy as np
import ImageToPixelArray

def Drip(Array, Threshold, Distance):

    OutArray = np.zeros(Array.shape)
    width = len(Array[0])
    height = len(Array[1])

    PixThresh = Array > Threshold
# Iterates through those pixels and finds their radii

    for i in range(len(np.nonzero(PixThresh)[0])):
        for c in [0,1,2]:
            x = np.nonzero(PixThresh)[0][i]
            y = np.nonzero(PixThresh)[1][i]
            if y < height-Distance and Array[x][y+1][c] > Threshold and Array[x][y+2][c] > Threshold and Array[x][y+3][c] >Threshold:
                if x > 1 and x < width-1 and Array[x-1][y+3][c] > Threshold and Array[x+1][y+3][c] > Threshold:
                    temp = [Array[x][y][c],Array[x][y+1][c],Array[x][y+2][c],Array[x][y+3][c],Array[x-1][y+3][c],Array[x+1][y+3][c]]
                    for d in range(0,Distance):
                        Array[x][y+d][c],Array[x-1][y+3+d][c],Array[x+1][y+3+d][c] = Array[x][y+4+d][c],Array[x-1][y+4+d][c],Array[x+1][y+4+d][c]
                    Array[x][y+Distance][c] = temp[0]
                    Array[x][y+Distance+1][c] = temp[1]
                    Array[x][y+Distance+2][c] = temp[2]
                    Array[x][y+Distance+3][c] = temp[3]
                    Array[x+1][y+Distance+3][c] = temp[4]
                    Array[x+1][y+Distance+3][c] = temp[5]
    return Array
                    
                
                





# Teleport(ImageToPixelArray.image_to_array("Test Image.jpg"), 100, 1)