import cv2
import numpy as np
import os

# Direct deep imports to completely bypass the 'solutions' attribute bug
import mediapipe.python.solutions.face_mesh as mp_face_mesh

# Initialize Face Mesh directly
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1, 
    refine_landmarks=True, 
    min_detection_confidence=0.5, 
    min_tracking_confidence=0.5
)

# Landmark points for Left and Right Eyes
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

# Thresholds
EAR_THRESHOLD = 0.22  
CONSECUTIVE_FRAMES = 20  

FRAME_COUNTER = 0

def calculate_ear(landmarks, eye_indices, img_w, img_h):
    """Calculates the Eye Aspect Ratio (EAR)"""
    pts = []
    for idx in eye_indices:
        lm = landmarks[idx]
        pts.append(np.array([lm.x * img_w, lm.y * img_h]))
    
    p1, p2, p3, p4, p5, p6 = pts[0], pts[1], pts[2], pts[3], pts[4], pts[5]
    
    vertical_1 = np.linalg.norm(p2 - p6)
    vertical_2 = np.linalg.norm(p3 - p5)
    horizontal = np.linalg.norm(p1 - p4)
    
    ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
    return ear

def play_alarm():
    """Triggers a quick Windows beep sound"""
    if os.name == 'nt':
        import winsound
        winsound.Beep(2000, 600)
# Start Webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Webcam feed not detected.")
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    results = face_mesh.process(rgb_frame)
    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            
            left_ear = calculate_ear(face_landmarks.landmark, LEFT_EYE, w, h)
            right_ear = calculate_ear(face_landmarks.landmark, RIGHT_EYE, w, h)
            avg_ear = (left_ear + right_ear) / 2.0
            
            for idx in LEFT_EYE + RIGHT_EYE:
                lm = face_landmarks.landmark[idx]
                cv2.circle(frame, (int(lm.x * w), int(lm.y * h)), 2, (0, 255, 0), -1)

            if avg_ear < EAR_THRESHOLD:
                FRAME_COUNTER += 1
                if FRAME_COUNTER >= CONSECUTIVE_FRAMES:
                    cv2.putText(frame, "!!! DROWSINESS ALERT !!!", (30, 80),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
                    play_alarm()
            else:
                FRAME_COUNTER = 0 
                
            cv2.putText(frame, f"EAR: {avg_ear:.2f}", (30, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    cv2.imshow('Drowsiness Detector', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()