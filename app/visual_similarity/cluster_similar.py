import numpy as np
from skimage.transform import resize
from skimage.color import gray2rgb
from app.image_io import load_images
from collections import defaultdict

def vectorize(image, width=300, height=300):
    """
    Convert an image to a vector
    resizing converts uints to floats between 0 and 1
    """

    # Of all the things in this file, this is the bottleneck
    # TODO: Refactor to use cv2 resize?
    new_image = resize(image, [height, width])
    shape = new_image.shape

    if len(shape) == 2:
        new_image = gray2rgb(new_image)
    
    return new_image.flatten()

def similarity(u, v):
    """
    Find percent similarity [0,1] between 1D vectors u and v
    """

    diffs = np.abs(u - v)
    return 1 - np.sum(diffs)/u.size

def group_pairs(pairs):

    groups = defaultdict(lambda: set())

    for i,j in pairs:
        i_set = groups[i]
        j_set = groups[j]
        
        combo = i_set.union(j_set)
        combo.add(i)
        combo.add(j)

        for x in combo:
            groups[x] = combo

    return set(map(lambda s: tuple(s), groups.values()))


def group_images(path, threshold=0.8):
    names, images = load_images(path)
    vectors = [vectorize(image) for image in images]
    
    not_grouped = set(names)
    pairs = []

    n = len(vectors)

    for i in range(n):
        for j in range(i+1, n):
            if similarity(vectors[i], vectors[j]) >= threshold:
                i_name = names[i]
                j_name = names[j]

                pairs.append((i_name, j_name))
                
                if i_name in not_grouped:
                    not_grouped.remove(i_name)
                if j_name in not_grouped:
                    not_grouped.remove(j_name)
    groups = group_pairs(pairs)
    return list(groups.union(not_grouped))