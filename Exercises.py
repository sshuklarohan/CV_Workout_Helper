import math
import cv2
import mediapipe as mp
import numpy as np
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

class Exercise:

    #contains all general functionality used to analyze an exercise
    
    def __init__(self):
        self.visible_side = "RIGHT"
        self.leniency_multiplier = 1

    def check_valid(self):
        pass
    

    def update_landmarks(self, landmarks):
        self.landmarks = landmarks


    #(a,b,c) are points contained in dictionaries with keys "x" and "y", z is disregarded
    def calculate_angle(self,a,b,c):
        
        BA = [a.x - b.x, a.y - b.y]
        BC = [c.x - b.x, c.y - b.y]

        dot_prod = (BA[0] * BC[0]) + (BA[1] * BC[1])

        mag_BA = math.sqrt((BA[0] ** 2) + (BA[1] ** 2))
        mag_BC = math.sqrt((BC[0] ** 2) + (BC[1] ** 2))

        cos_angle = dot_prod/ (mag_BA * mag_BC)
        cos_angle = max(min(cos_angle, 1.0), -1.0)

        angle = math.degrees(math.acos(cos_angle))
        return angle
    
    def set_visible_side(self):
        left_side_landmarks = [
            mp_pose.PoseLandmark.LEFT_SHOULDER,
            mp_pose.PoseLandmark.LEFT_HIP,
            mp_pose.PoseLandmark.LEFT_KNEE,
        ]
        right_side_landmarks = [
            mp_pose.PoseLandmark.RIGHT_SHOULDER,
            mp_pose.PoseLandmark.RIGHT_HIP,
            mp_pose.PoseLandmark.RIGHT_KNEE,
        ]

        # Calculate visibility for the left side
        left_visibility = sum(
            1 for lm in left_side_landmarks if self.landmarks.landmark[lm] and self.landmarks.landmark[lm].visibility > 0.5 
        )

        right_visibility = sum(
            1 for lm in right_side_landmarks if self.landmarks.landmark[lm] and self.landmarks.landmark[lm].visibility > 0.5 
        )

        if left_visibility > right_visibility:
            self.visible_side = "LEFT"
        else:
            self.visible_side = "RIGHT"


class Squat(Exercise):

    #check if entire exercise is valid(per frame analysis)
    def check_valid(self):
        #self.set_visible_side()
        errors = []
        highlight_connections = []
        lms = mp_pose.PoseLandmark

        if not self.check_shoulder_knee_valid():
            errors.append("shoulder past Knee")
            highlight_connections.append((lms.LEFT_SHOULDER, lms.LEFT_HIP))
            highlight_connections.append((lms.RIGHT_SHOULDER, lms.RIGHT_HIP))
            highlight_connections.append((lms.LEFT_KNEE, lms.LEFT_ANKLE))
            highlight_connections.append((lms.RIGHT_KNEE, lms.RIGHT_ANKLE))

        if not self.check_heels_valid():
            errors.append("heels raised off ground")
            highlight_connections.append((lms.LEFT_HEEL, lms.LEFT_FOOT_INDEX))
            highlight_connections.append((lms.RIGHT_HEEL, lms.RIGHT_FOOT_INDEX))
        
        angle_err = self.check_hip_knee_angles_valid()
        if  angle_err == 1:
            errors.append("leaning forward too much")
            highlight_connections.append((lms.LEFT_HIP, lms.LEFT_KNEE))
            highlight_connections.append((lms.RIGHT_HIP, lms.RIGHT_KNEE))
            highlight_connections.append((lms.LEFT_HIP, lms.LEFT_SHOULDER))
            highlight_connections.append((lms.RIGHT_HIP, lms.RIGHT_SHOULDER))
        elif angle_err == -1:
            errors.append("leaning back too much")
            highlight_connections.append((lms.LEFT_HIP, lms.LEFT_KNEE))
            highlight_connections.append((lms.RIGHT_HIP, lms.RIGHT_KNEE))
            highlight_connections.append((lms.LEFT_HIP, lms.LEFT_SHOULDER))
            highlight_connections.append((lms.RIGHT_HIP, lms.RIGHT_SHOULDER))

        return errors, highlight_connections
    

        highlight_connections = []
    




    def check_shoulder_knee_valid(self):
        if self.visible_side == "LEFT":
            shoulder = self.landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER] if self.landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER] else None
            knee = self.landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE] if self.landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE] else None
        else:
            shoulder = self.landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER] if self.landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER] else None
            knee = self.landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE] if self.landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE] else None
        
        if shoulder is None or knee is None:
            return True

        if shoulder.x - knee.x > 0.1 * self.leniency_multiplier:
            return False
        else:
            return True 

   
   #check if heels are raised
    def check_heels_valid(self):
        if self.visible_side == "LEFT":
           heel = self.landmarks.landmark[mp_pose.PoseLandmark.LEFT_HEEL] if self.landmarks.landmark[mp_pose.PoseLandmark.LEFT_HEEL] else None
           index = self.landmarks.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX] if self.landmarks.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX] else None
        else:
           heel = self.landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HEEL] if self.landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HEEL] else None
           index = self.landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX] if self.landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX] else None

        if heel is None or index is None:
            return True
       
        if heel.y - index.y > 0.2 * self.leniency_multiplier:
           return False
        else:
           return True
       
   

   #check if hip and knee angles are algined
    def check_hip_knee_angles_valid(self):
        if self.visible_side == "LEFT":
            hip = self.landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP] if self.landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP] else None
            knee = self.landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE] if self.landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE] else None
            shoulder = self.landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER] if self.landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER] else None
            ankle = self.landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE] if self.landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE] else None
        else:
            hip = self.landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP] if self.landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP] else None
            knee = self.landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE] if self.landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE] else None
            shoulder = self.landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER] if self.landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER] else None
            ankle = self.landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE] if self.landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE] else None

        if hip is None or knee is None or shoulder is None or ankle is None:
            return 0
       
        hip_angle = self.calculate_angle(shoulder, hip, knee)
        knee_angle = self.calculate_angle(hip, knee, ankle)

        if (hip_angle - knee_angle) > 20 * self.leniency_multiplier:
            return 1
        elif (hip_angle - knee_angle) < -20 * self.leniency_multiplier:
            return -1
        else:
            return 0




highlight_style = mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=3, circle_radius=2)
squat = Squat()        
# For webcam input:
cap = cv2.VideoCapture(0)
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    if results.pose_landmarks:
        squat.update_landmarks(results.pose_landmarks)
        errors,highlight_connections = squat.check_valid()

        # Draw the pose annotation on the image.
        base = list(set(mp_pose.POSE_CONNECTIONS) - set(highlight_connections))
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            base,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            highlight_connections,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
            connection_drawing_spec=highlight_style)

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()



       


