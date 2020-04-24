# VisionProject
Image sorter final project for CSCI 5722: Computer Vision

# Installing and Running

## Installing

Github will not let me upload the object detection weights file. To configure object detection, download the weights file from [https://pjreddie.com/media/files/yolov3.weights](https://pjreddie.com/media/files/yolov3.weights) and put yolov3.weights in app/object_similarity/data. Or edit the config and weight paths in `object_detection.py` to use the `yolov3-tiny` versions (performance will be worse with these).

Python Dependencies:
* Python 3.7
* PytQt5 (GUI library)
* opencv (python library version 3.4.2 or above) (most of the image processing)
* numpy (stats / matrix stuff)
* skimage (some image processing)

To install these dependencies, use conda and the provided `environment.yml` file to create a new conda environment.
```bash
$ conda env create -f environment.yml
```
This should install the right dependencies and the correct version of OpenCV. This project uses SIFT which is patented and disabled on some distributions of OpenCV. The `defaults` channel distribution used in `environment.yml` should have SIFT enabled; if not, you may want to try [other methods](https://www.pyimagesearch.com/opencv-tutorials-resources-guides/) like pip or compiling from source.

## Running

To run the code, open a command line and activate this project's python environment using conda
```bash
$ conda activate dohertyCV
```
then run `main.py`
```bash
$ python main.py
```

A window with buttons should appear. Each button will group the images in a user specified directory (but not a subdirectory) the following way:

* "Group by visual features": simple pixel by pixel similarity
* "Group using facial recognition": group by the number of faces in each image. (For example, group all images containing 2 faces together, or separate into a group of portraits and a group of non-portraits)
* "Group using object recognition": group by the objects a neural net detects in the image. For example, if an image contains a person and a bicycle, it will be put in the "person" group and the "bicycle" group.
* "Group using SIFT feature comparison": Group images by how similar their SIFT features are. This one is very slow.

Groupings can be saved to disk by pressing the save button and choosing a directory from the file explorer. This will create a sub-directory for each group in the selected directory and copy the original image files into those sub-directories. Images that are not part of any group will be saved to the selected directory.

Currently, the program does not know the difference between an image file and a non-image file, so make sure the directory you would like to sort only contains image files. It will ignore any sub-directories it encounters though.

## Uninstalling

To uninstall the conda environment, run 
```bash
$ conda deactivate
$ conda env remove --name dohertyCV
```

# Code structure

I apologize in advance for the spaghetti code. I had to learn QT as I went (tkinter crashed my computer), so a lot of this code is hacking around PyQt widgets, app windows, and other GUI stuff. For the most part, GUI code files end in `_widget.py`. Each widget file imports computer vision code from the other file in the same module. For widgets that use a progress bar, most of the processing code is in the `External` class.

# Sources and References

This project uses a facial recognition haar cascade and a YOLO object recognition neural net. I did not have the time, data, or compute power to train these classifiers myself, so I used pre-trained classifiers. The facial recognition cascades (app/cascades/data) were taken from the [opencv git repository](https://github.com/opencv/opencv/tree/master/data/haarcascades), and the YOLO neural net (app/object_similarity/data) was taken from [Darknet](https://pjreddie.com/darknet/yolo/). The object recognition code that uses that neural net was adapted from this [article](https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/).
