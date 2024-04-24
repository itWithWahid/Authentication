import cv2
import numpy as np
import dlib
import time
import threading

# initialize the threshold for the blink detection and the number of blinks
threshold = 0.2
eye_closed = False
blinks = 0
last_time = time.time()
status = False
verificationStatus = False
face_match_1 = False

# initialize dlib's face detector and face landmark predictor
detector = dlib.get_frontal_face_detector()
face_landmarks = "model_assets/shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(face_landmarks)

# Load the pre-trained face recognition model
dlib_face_recognition_resnet_model_v1 = "model_assets/dlib_face_recognition_resnet_model_v1.dat"
face_rec_model = dlib.face_recognition_model_v1(dlib_face_recognition_resnet_model_v1)

def aspect_ratio(landmarks, eye_range):
    # Get the eye coordinates
    eye = np.array(
        [np.array([landmarks.part(i).x, landmarks.part(i).y])
            for i in eye_range]
    )
    # compute the euclidean distances
    B = np.linalg.norm(eye[0] - eye[3])
    A = np.linalg.norm(eye[1] - eye[5]) + np.linalg.norm(eye[2] - eye[4])
    # Use the euclidean distance to compute the aspect ratio
    ear = A / (2.0 * B)
    return ear

def eye_blink(frame, target_face_features_array):
    global threshold, eye_closed, blinks, last_time
    
    frame = cv2.resize(frame, (600, 450))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # detect faces in the grayscale frame
    rects = detector(gray, 0)
    
    # loop over the face detections
    for rect in rects:
        landmarks = predictor(gray, rect)
        
        # Use the coordinates of each eye to compute the eye aspect ratio.
        left_aspect_ratio = aspect_ratio(landmarks, range(42, 48))
        right_aspect_ratio = aspect_ratio(landmarks, range(36, 42))
        ear = (left_aspect_ratio + right_aspect_ratio) / 2.0
        
        # if the eye aspect ratio is below the blink threshold, set the eye_closed flag to True.
        if ear < threshold:
            eye_closed = True
        # if the eye aspect ratio is above the blink threshold and
        # the eye_closed flag is True, increment the number of blinks.
        elif ear >= threshold and eye_closed:
            blinks += 1
            eye_closed = False
            
    # If 5 seconds have passed since the last blink, reset the blink count to zero
    if time.time() - last_time >= 10:
        blinks = 0
        last_time = time.time()
    if blinks > 1:
        if face_match(frame,target_face_features_array):
            return True
        else:
            return False
    else:
        return False

def face_match(frame, target_face_features):
    
    # Convert the frame to grayscale for face detection
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect faces in the frame
    frame_faces = detector(frame_gray)
    
    # Extract face features from the frame
    frame_face_features = []
    for face in frame_faces:
        landmarks = predictor(frame_gray, face)
        frame_face_features.append(face_rec_model.compute_face_descriptor(frame, landmarks))
    frame_face_features = np.array(frame_face_features)
    
    try:
        # Calculate the Euclidean distances between all pairs of features
        distances = np.linalg.norm(target_face_features[:, np.newaxis] - frame_face_features, axis=2)
    except:
        return False
    # Check if any distance is below the threshold for a match
    match = np.any(distances < 0.35)
    
    return match

def face_matching_worker(frame, target_face_features_array):
    global face_match_1
    match = face_match(frame, target_face_features_array)
    if match:
        face_match_1 = True

def target_face_features(target_image_path):
    # Load the target image
    target_image = cv2.imread(target_image_path)
    # Detect faces in the target image
    target_faces = detector(target_image)
    if len(target_faces) == 0:
        return False
    # Extract face features from the target image
    target_face_features = []
    for face in target_faces:
        landmarks = predictor(target_image, face)
        target_face_features.append(face_rec_model.compute_face_descriptor(target_image, landmarks))
    # Convert the feature lists to numpy arrays for efficient computation
    target_face_features_array = np.array(target_face_features)
    return target_face_features_array

def gen_frames(id,image_path):
    global verificationStatus
    global face_match_1
    status = False
    is_face_match = False
    verificationStatus = False
    frame_count = 0
    execution_time = 0
    _start_time = time.time()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    target_face_features_array = target_face_features(image_path)
    
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    while True:
        success, frame = cap.read()
        frame_count += 1
        
        if time.time()-_start_time >= 60:
            cv2.putText(frame, "Failed", (50, 300), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 255), 5)
            cap.release()
            
        
        if not success:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            if  len(faces) == 1:
                cv2.putText(frame, f"Exe Time{execution_time}", (50, 200), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                cv2.putText(frame, f"Frame Count {frame_count}", (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

                if frame_count % 50 == 0 and not is_face_match:
                    
                    start_time = time.time()
                    t = threading.Thread(target=face_matching_worker, args=(frame, target_face_features_array))
                    t.start()
                    execution_time = time.time() - start_time
                
                if face_match_1:
                    cv2.putText(frame, "F_M", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                    status = eye_blink(frame=frame,target_face_features_array=target_face_features_array)
                
                if status:
                        verificationStatus = True
                        cv2.putText(frame, "MATCH!!!", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 0), 5)
                        cap.release()
                else:
                    cv2.putText(frame, f"face match{face_match_1}", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                    cv2.putText(frame, "Processing", (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "NONE OR MULTIPLE FACE", (50, 450), cv2.FONT_HERSHEY_PLAIN , 2, (0, 255, 0), 2)
                
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    cap.release()
    
def check_face_recognition():
    global verificationStatus
    return verificationStatus