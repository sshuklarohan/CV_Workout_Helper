import math
import mediapipe as mp
import numpy as np
mp_pose = mp.solutions.pose


class Exercise:

    #contains all general functionality used to analyze an exercise
    
    def __init__(self, landmarks):
        self.landmarks = landmarks
        self.visible_side = "RIGHT"
        self.leniency_multiplier = 1

    def check_valid(self):
        pass


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
    
    def get_visible_side(self):
        left_side_landmarks = [
            mp_pose.PoseLandmark.LEFT_SHOULDER,
            mp_pose.PoseLandmark.LEFT_ELBOW,
            mp_pose.PoseLandmark.LEFT_WRIST,
            mp_pose.PoseLandmark.LEFT_HIP,
            mp_pose.PoseLandmark.LEFT_KNEE,
            mp_pose.PoseLandmark.LEFT_ANKLE,
        ]
        right_side_landmarks = [
            mp_pose.PoseLandmark.RIGHT_SHOULDER,
            mp_pose.PoseLandmark.RIGHT_ELBOW,
            mp_pose.PoseLandmark.RIGHT_WRIST,
            mp_pose.PoseLandmark.RIGHT_HIP,
            mp_pose.PoseLandmark.RIGHT_KNEE,
            mp_pose.PoseLandmark.RIGHT_ANKLE,
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
        errors = {}



    def check_shoulder_knee_valid(self):
        print("side is " + self.visible_side)
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
            return True
       
        hip_angle = self.calculate_angle(shoulder, hip, knee)
        knee_angle = self.calculate_angle(hip, knee, ankle)

        if np.abs(hip_angle - knee_angle) > 20 * self.leniency_multiplier:
            return False
        else:
            return True

        





       


