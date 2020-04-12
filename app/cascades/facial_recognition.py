import cv2
from app.image_io import load_images

# face_detector = cv2.CascadeClassifier("app/cascades/data/lbpcascade_frontalface_improved.xml")
# face_detector = cv2.CascadeClassifier("app/cascades/data/haarcascade_frontalface_default.xml")
face_detector = cv2.CascadeClassifier("app/cascades/data/haarcascade_frontalface_alt.xml")

def detect_faces(images):
    gray_images = [cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) for image in images]

    n = len(gray_images)
    results = []

    for i in range(n):
        result = face_detector.detectMultiScale(gray_images[i], scaleFactor=1.2, minNeighbors=4, minSize=(30,30))
        results.append(result)
    
    return results

def detect_face(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return face_detector.detectMultiScale(gray_image)

def group_faces_binary(faces, names):
    contains_faces = [len(face) != 0 for face in faces]
    
    groups = {"Portraits":[], "Not Portraits": []}

    for i in range(len(faces)):
        if contains_faces[i]:
            groups["Portraits"].append(names[i])
        else:
            groups["Not Portraits"].append(names[i])
    
    return groups

def group_faces_count(faces, names):
    groups = {}

    for i in range(len(faces)):
        count = str(len(faces[i]))
        
        if count in groups:
            groups[count].append(names[i])
        else:
            groups[count] = [names[i]]
    
    return groups
