import cv2
import mediapipe as mp
from Exercises import Squat
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic
mp_pose = mp.solutions.pose
highlight_style = mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=3, circle_radius=2)
squat = Squat()        




input_video_path = "reasources/input.mp4"  
output_video_path = "reasources/output.mp4"

cap = cv2.VideoCapture(input_video_path)


fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define codec and create VideoWriter
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))


with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      break


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
    cv2.imshow("Resizable Window", cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
out.release()
cv2.destroyAllWindows()
