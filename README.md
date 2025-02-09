# CV Workout Helper

This project provides real-time feedback for exercises using computer vision. It utilizes OpenCV and MediaPipe's BlazePose model to detect key landmarks on the user's body while performing exercises. The system gives feedback on posture and identifies areas that need improvement. Both webcam input and mp4 video inputs can be taken, webcam input will provide live feedback and mp4 input will return a fully annotated video.


### Live recognition

This feature takes webcam input and overlays feedback for users to make live adjustments. Landmark connections will appear white if exercise is being performed correctly. When form deviates problem areas will be highlighted red.


### Video annotation

This feature mimics the same functionallity as live recognition except it takes a video input. Playback provides valuable insights in highlighting problem areas and bad habits.

## Setup/Prerequisites

Before running the application, you need to install the required packages. You can install them using `pip`:

```
pip install opencv-python 
pip install mediapipe
pip install numpy
```


#### For live recognition:
- Ensure your device has a webcam connected
- run ``` python live_recognition.py ``` Ensure entire body is visible for most accurate results

#### For video annotation:
- take the input video and add it to the reasources folder
- change the ``input_video_path`` in the ``video_processor.py`` file
- run ``python video_processor.py``
- Output video will appear at the path of ``output_video_path`` which is also found in ``video_processor.py`` file