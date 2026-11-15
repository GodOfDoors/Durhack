
def image_to_array(Image_Name):
    import numpy as np
    from PIL import Image as image

# Opens the image as "image" file
    im = image.open(Image_Name)

# Converts it to numpy array and returns
# Deletes alpha value
    im = np.asarray(im)
    return np.delete(im, [False,True,True,True], 2)



# If testing change this to the path of the test image used
# image_to_array("Test Image.jpg")