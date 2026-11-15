import numpy as np
import ImageToPixelArray


# pass the array including only the colour values that are wanted
def Radiate(Threshold, Levels, RadMax, RadChange, Array):
# The array to return later
    OutArray = np.zeros(Array.shape)
    Height = (Array.shape)[0]
    Width = (Array.shape)[1]
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
        for u in range(-RadMaxSpec, RadMaxSpec):
            CirclePixels = int(np.sqrt(RadMaxSpec**2-(u)**2))
            Start =(y-CirclePixels)
            End = (y+CirclePixels)
            OutArray[x-(u)][Start:End] += RadChange
            OutArray[u+x][y] += -(2*CirclePixels+1)*RadChange


    return OutArray
# Returns the map that should be added to the array to produce the new frame


# This commented line is the format to remove the non red values from the image
# Arr = np.delete(Arr, [False,True,True], 2)
# Radiate(200, 10, 4, 1, (ImageToPixelArray.image_to_array("Test Image.jpg")))



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