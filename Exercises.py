import math

class Exercise:

    #contains all general functionality used to analyze an exercise
    
    def __init__(self, landmarks):
        self.landmarks = landmarks


    #(a,b,c) are points contained in dictionaries with keys "x" and "y", z is disregarded
    def calculate_angle(a,b,c):
        
        BA = [a['x'] - b['x'], a['y'] - b['y']]
        BC = [c['x'] - b['x'], c['y'] - b['y']]

        dot_prod = (BA[0] * BC[0]) + (BA[1] * BC[1])

        mag_BA = math.sqrt((BA[0] ** 2) + (BA[1] ** 2))
        mag_BC = math.sqrt((BC[0] ** 2) + (BC[1] ** 2))

        cos_angle = dot_prod/ (mag_BA * mag_BC)
        cos_angle = max(min(cos_angle, 1.0), -1.0)

        angle = math.degrees(math.acos(cos_angle))
        return angle


class Squat(Exercise):


   #returns true or false depending if shoulders are over knees
   def check_shoulders_past_knees():
       pass
   
   #check if heels are raised
   def check_raised_heels():
       pass
   

   #check if hip and knee angles are algined
   def check_hip_knee_angles():
       pass



       


