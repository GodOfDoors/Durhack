import numpy as np
import ImageToPixelArray


# pass the array including only the colour values that are wanted
def Radiate(Threshold, Levels, RadMax, RadChange, Array):
# The array to return later
    OutArray = np.empty(Array.shape)
# Pixels we're looking at
    RayTo = np.empty(Array.shape)
    PixThresh = Array > Threshold
# Iterates through those pixels and finds their radii
    for i in np.nonzero(PixThresh):
        RadMaxSpec = np.ceil((Array[i] - Threshold)/Levels)
        if RadMaxSpec > RadMax:
            RadMaxSpec = RadMax
# Iterates through affected pixels and adds their effect
        for u in range(-RadMaxSpec, RadMaxSpec):
            CirclePixels = RadMaxSpec**2-(i[0]+u)**2
            OutArray[[i[0],CirclePixels]:[i[0],CirclePixels]] = RadChange
    print(OutArray)
    return OutArray



# This commented line is the format to remove the non red values from the image
# Arr = np.delete(Arr, [False,True,True,True], 2)
# Radiate(200, 10, 4, 1, (ImageToPixelArray.image_to_array("Test Image.jpg")))
