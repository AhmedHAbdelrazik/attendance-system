#Ahmed Hossam
import numpy as np 
import cv2
from src.anti_spoof_predict import AntiSpoofPredict 
liveness_model = AntiSpoofPredict(device_id= -1)
MODEL_WEIGHTS = "./resources/anti_spoof_models/4_0_0_300x300_MultiFTNet.pth"

def check_liveness(frame, face_loc):
    try:
        top, right, bottom, left = face_loc
        face_img = frame[top:bottom, left:right]

        if face_img.size == 0:
            print("Liveness Error: empty face crop")
            return False

        face_img = cv2.resize(face_img, (300, 300))
        
        prediction = liveness_model.predict(face_img, MODEL_WEIGHTS)
        if isinstance(prediction, (list, tuple)):
            prediction = prediction[0]

        label = np.argmax(prediction)
        value = prediction[0][label]

        real_prob = prediction[0][0]
        fake_prob = prediction[0][1] if prediction.shape[1] > 1 else 1 - real_prob
        print(f"Liveness Probs: real={real_prob:.2f}, fake={fake_prob:.2f}")
        
        print(f"Liveness Debug: Label={label}, Conf={value:.2f}")

        if real_prob > 0.90:
            return True
        return False
    except Exception as e:
        print(f"Liveness Error: {e}")
        return False
        