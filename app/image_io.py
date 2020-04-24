import os
import shutil
from cv2 import imread, IMREAD_COLOR

def format_dir(name):
    if name[-1] != "/":
        return name + "/"
    
    return name

def load_images(image_dir):
    if image_dir[-1] != "/":
        image_dir += "/"
    
    filenames = os.listdir(image_dir)
    final_names = []
    results = []

    for i in range(len(filenames)):
        if filenames[i] == '.DS_Store':
            continue
        
        path = image_dir + filenames[i]
        
        if os.path.isfile(path):
            results.append(imread(path, IMREAD_COLOR))
            final_names.append(filenames[i])

    return final_names, results
    # return filenames, [imread(path, IMREAD_COLOR) for path in file_paths]

def save_group(grouping, src_path, dest_path):
    src_path = format_dir(src_path)
    dest_path = format_dir(dest_path)

    for group in grouping:

        this_dest = dest_path

        if group != "":
            this_dest = dest_path + group
            if not os.path.exists(this_dest):
                os.mkdir(this_dest)
        
        this_dest = format_dir(this_dest)
        
        for name in grouping[group]:
            shutil.copyfile(src_path + name, this_dest + name)