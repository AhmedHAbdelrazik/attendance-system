import face_recognition
import cv2
import numpy as np
from database import get_all_students


def photo_to_encode(pic_path):
    known_image = face_recognition.load_image_file(pic_path)
    known_encoding = face_recognition.face_encodings(known_image)
    if len(known_encoding) > 0:
       return  known_encoding[0]
    else:
        print("no face recognation")


def check_if_registered(new_encoding):
    students_data = get_all_students() 

    if not students_data:
        print("no students registered before")
        return False, None
    else:
        known_names = [row[1] for row in students_data]
        known_encodings = [row[2] for row in students_data]

        matches = face_recognition.compare_faces(known_encodings, new_encoding, tolerance=0.6)

    if True in matches:
        first_match_index = matches.index(True)
        matched_name = known_names[first_match_index]
        return True, matched_name
    return False, None


"""
def frame_to_encode(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
    if len(encodings) > 0:
        return encodings[0], face_locations[0]
    return None, None  
"""
def identify_student(current_face_encoding):

    students_data = get_all_students()
    if not students_data:
        return None, "No students registered in database."

    known_encodings = [row[2] for row in students_data]
    known_ids = [row[0] for row in students_data]
    known_names = [row[1] for row in students_data]

    matches = face_recognition.compare_faces(known_encodings, current_face_encoding, tolerance=0.6)
    face_distances = face_recognition.face_distance(known_encodings, current_face_encoding)

    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
        student_id = known_ids[best_match_index]
        student_name = known_names[best_match_index]
        return student_id, student_name

    return None, "Unknown"



