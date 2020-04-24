import cv2
import numpy as np
from app.image_io import load_images
from collections import defaultdict

class FeatureAnalyzer:
    def __init__(self):
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)

        self.sift = cv2.xfeatures2d.SIFT_create()
        self.flann = cv2.FlannBasedMatcher(index_params, {})
    
    def get_descriptors(self, image):
        return self.sift.detectAndCompute(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), None)[1]
    
    def feat_similarity(self, desc1, desc2):
        matches12 = self.flann.match(desc1, desc2)

        dists = []

        for i in range(len(matches12)):
            image1_index = matches12[i].queryIdx
            image2_index = matches12[i].trainIdx
            
            first_desc = desc1[image1_index]
            second_desc = desc2[image2_index]
            
            dists.append(1 - np.sum(np.abs(first_desc - second_desc)) / (len(first_desc) * 255))
        return np.mean(dists)
    

    # Very slow and threshold should be higher
    def similarity_pairs(self, descs, threshold=0.8):
        n = len(descs)

        pairs = []

        for i in range(n):
            for j in range(i+1, n):
                similarity = self.feat_similarity(descs[i], descs[j])

                if similarity > threshold:
                    pairs.append((i,j))
        
        return pairs

    # Also very slow and too strict
    def percent_in_common_pairs(self, descs, threshold=0.1):
        pairs = []
        n = len(descs)

        # Lowe's ratio test
        for i in range(n):
            for j in range(i+1, n):
                matches = self.flann.knnMatch(descs[i], descs[j], k=2)
                ratio_thresh = 0.7
                good_matches = 0

                for k in range(len(matches)):
                    if matches[k][0].distance < ratio_thresh * matches[k][1].distance:
                        good_matches += 1
                
                percent = good_matches / len(matches)
                if percent > threshold:
                    pairs.append((i,j))
        
        return pairs

    # Still very slow but gives the best results
    def mean_distance_pairs(self, descs):
        n = len(descs)
        dist_matrix = np.ones([n,n]) * np.inf

        for i in range(n):
            for j in range(i+1, n):
                match = self.flann.match(descs[i], descs[j])
                mean_dist = np.mean([m.distance for m in match])
                
                dist_matrix[i,j] = mean_dist
                dist_matrix[j,i] = mean_dist
        
        pairs = []
        for i in range(n):
            j = np.argmin(dist_matrix[i,:])
            pairs.append((i,j))
        
        return pairs
    
    def mean_distance(self, desc1, desc2):
        match = self.flann.match(desc1, desc2)
        return np.mean([m.distance for m in match])

def group_from_matrix(matrix, names):
    n = len(matrix)

    pairs = []

    for i in range(n):
        name = names[i]
        j = np.argmin(matrix[i,:])
        pairs.append((name, names[j]))
    
    groups = defaultdict(lambda: set())

    for i,j in pairs:
        i_set = groups[i]
        j_set = groups[j]
        
        combo = i_set.union(j_set)
        combo.add(i)
        combo.add(j)

        for x in combo:
            groups[x] = combo

    clusters = set(map(lambda s: tuple(s), groups.values()))
    grouping = {}

    i = 0
    for cluster in clusters:
        grouping[f"group {i}"] = cluster
        i += 1
    
    return grouping

