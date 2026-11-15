import numpy as np

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

def attraction(pixel_array, attraction_mat):
    """Implements how color chanels attract/repel each other as defined by the attraction matrix.
    The function implements the movement of a channel value symmetrially, so if a channel value
    moves, it is subtracted from the origin pixel's channel and added to the destination pixel's
    channel."""
    width = len(pixel_array)
    height = len(pixel_array[0])
    
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
    return  conservative_clip(pixel_array + delta)

def convolution(pixel_array, convolution_mat):
    """Convolutes over all channels in pixel_array as defined by convolution_mat."""
    width = len(pixel_array)
    height = len(pixel_array[0])

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

# Radiation causes a decay to nearby pixels after a threshold value of colour intensity is reached.

# pass the array including only the colour values that are wanted
def Radiate(Threshold, Levels, RadMax, RadChange, Array):
# The array to return later
    OutArray = np.zeros(Array.shape)
    Width = (Array.shape)[0]
    Height = (Array.shape)[1]
# Pixels we're looking at
    PixThresh = Array > Threshold
# Iterates through those pixels and finds their radii



    for i in range(len(np.nonzero(PixThresh)[0])):
        x = np.nonzero(PixThresh)[0][i]
        y = np.nonzero(PixThresh)[1][i]
        RadMaxSpec = int(np.ceil((Array[x][y][0] - Threshold)/Levels))
#        print(i,x,y,RadMax,RadMaxSpec)
        if RadMaxSpec > RadMax:
            RadMaxSpec = RadMax
        if RadMaxSpec+x+1 > Width or x-RadMaxSpec < 0:
            continue
        if RadMaxSpec+y+1 > Height or y-RadMaxSpec < 0:
            continue
# Iterates through affected pixels and adds their effect
        for u in range(-RadMaxSpec, RadMaxSpec+1):
            CirclePixels = int(np.sqrt(RadMaxSpec**2-(u)**2))
            Start =(y-CirclePixels)
            End = (y+CirclePixels)
            OutArray[x-u][Start:End+1] += RadChange
            OutArray[x][y] += -(2*CirclePixels+1)*RadChange


    return OutArray
# Returns the map that should be added to the array to produce the new frame


# This commented line is the format to remove the non red values from the image
# Arr = np.delete(Arr, [False,True,True], 2)
# Radiate(200, 10, 4, 1, (ImageToPixelArray.image_to_array("Test Image.jpg")))


# Example Implementations
# For Green
"""
    M = np.insert(Radiation.Radiate(100, 10, 4, 1, np.delete(NewFrame, [True,False,True], 2)),0, 0, 2)
    M = np.insert(M,2, 0, 2)
"""
# For Red
"""
    M = np.insert(Radiation.Radiate(100, 10, 4, 1, np.delete(NewFrame, [False,True,True], 2)),1, 0, 2)
    M = np.insert(M,1, 0, 2)
"""
# For Blue
"""
    M = np.insert(Radiation.Radiate(100, 10, 4, 1, np.delete(NewFrame, [True,True,False], 2)),0, 0, 2)
    M = np.insert(M,0, 0, 2)
"""




