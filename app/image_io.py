from os import listdir
# from skimage.io import imread
from cv2 import imread, IMREAD_COLOR

def load_images(image_dir):
    if image_dir[-1] != "/":
        image_dir += "/"
    
    filenames = listdir(image_dir)
    file_paths = [image_dir + filename for filename in filenames]

    return filenames, [imread(path, IMREAD_COLOR) for path in file_paths]
