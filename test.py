import cv2
import mediapipe as mp
from Exercises import Squat
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

image = cv2.imread('./reasources/image.png')

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as holistic:
    
    results = holistic.process(image)
    

    if results.pose_landmarks:
        for idx, landmark in enumerate(results.pose_landmarks.landmark):
            print(f"Landmark {idx}: x={landmark.x}, y={landmark.y}, z={landmark.z}, visibility={landmark.visibility}")

    sq = Squat(results.pose_landmarks)
    sq.get_visible_side()
    print(sq.check_shoulder_knee_valid() and sq.check_heels_valid() and sq.check_hip_knee_angles_valid())



    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_holistic.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles
        .get_default_pose_landmarks_style())
    
    # Overlay text on the image
    text = "this is how you add text"
    position = (50, 50)  # (x, y) coordinates of the text
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (0, 255, 0)  # Green color in BGR
    thickness = 2
    cv2.putText(image, text, position, font, font_scale, color, thickness, cv2.LINE_AA)
 # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Holistic', image)
cv2.waitKey(0)

