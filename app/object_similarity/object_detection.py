import cv2
import numpy as np

from collections import defaultdict
from app.image_io import load_images

# Adapted from https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/
# Object classification NN from DarkNet

# Trying an OOP approach because facial recognition got messy
class ObjectDetection:
    def __init__(self):
        config_path = "app/object_similarity/data/yolov3.cfg"
        weight_path = "app/object_similarity/data/yolov3.weights"
        labels_path = "app/object_similarity/data/coco.names"

        self.net = cv2.dnn.readNetFromDarknet(config_path, weight_path)
        self.layer_names = self.net.getLayerNames()
        self.layer_names = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        self.labels = []

        with open(labels_path) as f:
            lines = f.readlines()
            self.labels = [line.strip() for line in lines]
    
    def load_directory(self, path):
        return load_images(path)

    def classify_image(self, image, confidence_thresh=0.5):
        blob = cv2.dnn.blobFromImage(image, 1/255.0, (416,416), swapRB=True, crop=False)
        self.net.setInput(blob)
        net_output = self.net.forward(self.layer_names)

        ids = set()

        for output in net_output:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > confidence_thresh:
                    ids.add(class_id)
        
        return ids

    def group_labels(self, classification, names):
        n = len(classification)

        grouping = defaultdict(lambda: [])

        for i in range(n):
            image_name = names[i]
            if len(classification[i]) == 0:
                grouping["none detected"].append(image_name)
                continue

            for class_id in classification[i]:
                label = self.labels[class_id]
                grouping[label].append(image_name)
        
        return grouping
