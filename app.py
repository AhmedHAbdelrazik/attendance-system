#Ahmed Hossam
import streamlit as st
import os
import cv2
import numpy as np
import pandas as pd
from database import add_student, mark_attendance, get_attendance_report, clear_attendance_records
from face import photo_to_encode, identify_student,check_if_registered
from liveness import check_liveness
import face_recognition


st.set_page_config(page_title="Smart Attendance System", layout="wide")
st.title("🎓 Smart AI Attendance System")
tab1, tab2, tab3 = st.tabs(["📝 Registration", "🎥 Live Attendance", "📊 Reports"])


with tab1:
    st.subheader("Student Registration Portal")
    st.write("Register a new student (Once per student).")

    student_name = st.text_input("Enter Student Full Name:")
    
    photo_method = st.radio("Choose Photo Method:", ("Upload Photo", "Take Live Photo"))
    
    image_data = None 

    if photo_method == "Upload Photo":
        image_data = st.file_uploader("Upload a clear face photo", type=['jpg', 'png', 'jpeg'])
    else:
        image_data = st.camera_input("Take a live photo")

    if st.button("Register Student"):
        if student_name and image_data:
            with open("temp_image.jpg", "wb") as f:
                f.write(image_data.getbuffer())
            
            st.info("Extracting Face Vector...")
            encoding = photo_to_encode("temp_image.jpg")
            
            if encoding is not None:
                is_registered, existing_name = check_if_registered(encoding)
                
                if not is_registered: 
                    student_id = add_student(student_name, encoding)
                    st.success(f"✅ Success! {student_name} has been registered with ID: {student_id}")
                else:
                    st.warning(f"⚠️ Student Already exist with name: {existing_name}!")
                    
            else:
                st.error("❌ No face detected. Please use a clearer photo.")
            
            import os  
            if os.path.exists("temp_image.jpg"):
                os.remove("temp_image.jpg")
                
        else:
            st.warning("⚠️ Please provide both a Name and a Photo.")



with tab2:
    st.subheader("Real-Time Face Recognition")
    run_attendance = st.toggle("Start Class Attendance Camera")

    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)

    while run_attendance:
        ret, frame = camera.read()
        if not ret:
            st.error("Camera not found!")
            break

        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        for face_loc in face_locations:
            top, right, bottom, left = face_loc
    
            is_real = check_liveness(frame, face_loc) 
            
            if is_real:
                current_encodings = face_recognition.face_encodings(rgb_frame, [face_loc])
                if len(current_encodings) > 0:
                    current_encoding = current_encodings[0]
                    student_id, student_name = identify_student(current_encoding)
                    
                    if student_id:
                        is_new = mark_attendance(student_id) 
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                        cv2.putText(frame, f"{student_name}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                        if is_new:
                            st.toast(f"✅ {student_name}", icon="⭐")
                    else:
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255), 2)
                        cv2.putText(frame, "Unknown", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            else:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, "FAKE FACE", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(display_frame)



with tab3:
    st.subheader("Class Attendance Report")
    
    if st.button("Refresh Data"):
        df = get_attendance_report()
        
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download as CSV (Excel)",
                data=csv,
                file_name='Daily_Attendance.csv',
                mime='text/csv',
            )
        else:
            st.warning("No attendance records found yet.")


    st.markdown("---") 
    st.subheader("⚠️ System Reset")
    st.write("Use this ONLY after downloading the Excel file, to prepare for the next lecture.")
    
    if st.button("🗑️ Clear Attendance (Start New Lecture)"):
        clear_attendance_records()
        st.success("✅ All attendance records cleared! Ready for the next class.")        