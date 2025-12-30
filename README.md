# Nano Vision by Forzaclaudio

This is a collection of Machine Vision tasks available on the Nvidia Jetson Nano board. It uses droidcam to collect the video that is processed by this repo.

## How to use
Access to all the utilities from this module can be accessed as follows:

```python
import nano_vision
```
instantiate the classes relevant for your machine vision tasks.

## How to install
To install using pip run the following command
```
pip install .
```
to install for development do the following:
```
pip install . -e
```
## Tests and Coverage
To run tests and obtain current coverage run the following:

```bash
$ pytest --cov=nano_vision
```

## Links and references
- https://hizzely.hashnode.dev/instalasi-droidcam-cli-di-jetson-nano

- https://www.dev47apps.com/droidcam/linux/

- https://docs.nvidia.com/jetson/archives/r35.4.1/DeveloperGuide/text/SD/Multimedia/AcceleratedGstreamer.html

- https://stackoverflow.com/questions/21152303/how-to-use-gstreamer-to-save-webcam-video-to-file

- https://developer.ridgerun.com/wiki/index.php/How_to_Capture_Frames_from_Camera_with_OpenCV_in_Python

- https://github.com/miooochi/face_recognizer

- https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html

- https://github.com/computervisioneng/train-yolov8-custom-dataset-step-by-step-guide?tab=readme-ov-file

- https://github.com/computervisioneng/automatic-number-plate-recognition-python-yolov8?tab=readme-ov-file

- https://github.com/abewley/sort

- https://github.com/computervisioneng/yolo-license-plate-detection

- https://www.kaggle.com/code/tathagatbanerjee/machines-can-draw-neural-style-transfer-pytorch

- https://www.tensorflow.org/tutorials/generative/style_transfer