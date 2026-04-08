
https://github.com/user-attachments/assets/cb86bc87-dda4-4bc0-8bf0-e7534c9ba4ef
<div align="center">
  <video src="https://github.com/user-attachments/assets/ee362a30-050c-4652-b910-d3efa30092f8" autoplay loop muted width="800"></video>
</div>

# 🎓 Smart AI Attendance System

A real-time face recognition attendance system built with Python and Streamlit. It identifies students via webcam, protects against spoofing attacks, and automatically logs attendance to a local SQLite database — no paper, no manual roll calls.

---

## 🚨 The Problem

Taking attendance manually — whether in a university lecture hall, a workplace, or any group setting — wastes a significant amount of time. The instructor has to call out names one by one, wait for responses, and write everything down by hand.

Beyond the time cost, the traditional method has a serious integrity problem: **when the group is large, students can mark attendance on behalf of absent classmates.** There is no reliable way to verify that the person whose name was written actually showed up.

---

## 💡 The Solution

This project solves both problems using **face recognition**. The system identifies each person by their face in real time — no names called, no paper passed around. Attendance is marked automatically the moment a registered face appears in front of the camera.

To close the remaining loophole — someone holding up a photo or a phone screen in front of the camera — the system includes an **anti-spoofing model** that analyzes skin texture and screen light emissions to distinguish a real, live face from a fake one. If a fake is detected, attendance is not recorded.

---

## ✨ Features

- **Dual Registration Methods** — Register a student via live webcam capture *or* by uploading a photo. The upload option ensures the system works even when lighting is poor, camera quality is low, or no webcam is available at registration time.
- **Duplicate Face Detection** — Before saving a new student, the system compares their face encoding against everyone already registered. If a match is found, it returns the existing student's name and blocks the duplicate entry.
- **Anti-Spoofing / Liveness Detection** — A deep learning model analyzes each detected face for signs of being fake (a printed photo, a phone screen, etc.) by examining skin texture and reflected light. Only real, live faces pass through to recognition.
- **Real-Time Face Recognition** — During a session, the webcam continuously detects and identifies registered students without any manual input.
- **Once-Per-Day Attendance Guard** — Each student is marked present only once per calendar day, regardless of how many times their face appears in the frame.
- **Exportable Attendance Report** — All present students are collected into a sheet showing name, date, and exact timestamp. The report can be downloaded as a CSV file compatible with Excel.
- **Session Reset** — After downloading the report, the instructor can clear all attendance records with one click to prepare for the next lecture or shift.

---

## 🗂️ Project Structure

```
├── app.py               # Main Streamlit application
├── face.py              # Face encoding, identification, and duplicate check
├── liveness.py          # Anti-spoofing / liveness detection
├── database.py          # SQLite database setup and queries
├── attendance.db        # Auto-generated SQLite database
├── requirements.txt     # Python dependencies
├── environment.yml      # Conda environment definition
├── resources/
│   └── anti_spoof_models/
│       └── 4_0_0_300x300_MultiFTNet.pth   # Liveness model weights
└── src/
    └── anti_spoof_predict.py              # Anti-spoof model inference
```

---



## 🖥️ Usage

### 📝 Tab 1 — Registration

1. Enter the student's full name.
2. Upload a clear face photo **or** take one with the webcam.
3. Click **Register Student**.
4. The system checks for duplicates before saving.

<img width="1916" height="899" alt="Screenshot 2026-04-08 161112" src="https://github.com/user-attachments/assets/252a4681-2f8b-4c66-ae3f-5917d5f53aaf" />


### 🎥 Tab 2 — Live Attendance

1. Toggle **Start Class Attendance Camera** to begin.
2. The webcam will detect faces in real time.
3. Each detected face is checked for liveness — fake faces are rejected.
4. Recognized students are marked present (once per day) and highlighted in **green**.
5. Unknown faces are highlighted in **yellow**; fake faces in **red**.

<img width="1188" height="616" alt="Screenshot 2026-04-08 161146" src="https://github.com/user-attachments/assets/eb0d546e-3af3-4b04-895d-3487729f0a43" />


### 📊 Tab 3 — Reports

1. Click **Refresh Data** to view today's attendance.
2. Download the report as a `.csv` file.
3. Click **Clear Attendance** after downloading to reset for the next lecture.


<img width="1901" height="878" alt="Screenshot 2026-04-08 161231" src="https://github.com/user-attachments/assets/3fd383a3-2d8f-411f-a0d7-c0cfc8c8d7e9" />

---

## 🗃️ Database Schema

**Students**

| Column        | Type    | Description                  |
|---------------|---------|------------------------------|
| id            | INTEGER | Primary key (auto-increment) |
| name          | TEXT    | Student full name            |
| face_encoding | BLOB    | Pickled 128-d face vector    |

**Attendance**

| Column      | Type     | Description                          |
|-------------|----------|--------------------------------------|
| id          | INTEGER  | Primary key (auto-increment)         |
| student_id  | INTEGER  | Foreign key → Students.id            |
| timestamp   | DATETIME | Auto-set to local date/time on insert|

---

## 🧰 Tech Stack

| Library              | Purpose                          |
|----------------------|----------------------------------|
| Streamlit            | Web UI                           |
| face_recognition     | Face encoding & matching (dlib)  |
| OpenCV               | Webcam capture & frame rendering |
| PyTorch              | Liveness detection model         |
| SQLite               | Local attendance database        |
| Pandas               | Report generation & CSV export   |

---

## 🔬 How It Works

The system is built around the `face_recognition` library, which is powered by **dlib** — a high-performance C++ machine learning library.

**1. Encoding a face**
When a student is registered, the model processes their photo and plots **128 landmark points** across the face. These points are converted into a **128-dimensional vector** (a list of 128 numbers) that uniquely represents that face. This vector is called a *face encoding*.

**2. Storing encodings**
SQLite does not natively support NumPy arrays, so each encoding is serialized into binary format using Python's `pickle` library before being stored in the database as a `BLOB`.

**3. Recognizing a face**
During a live attendance session, each frame from the webcam is processed the same way — a 128-d encoding is extracted for every detected face. The system then computes the **Euclidean distance** between the live encoding and every stored encoding. If the distance is below `0.6` (the similarity threshold), the faces are considered a match and the student is identified.

**4. Liveness check**
Before recognition even happens, the anti-spoofing model (based on [Silent-Face-Anti-Spoofing](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing)) analyzes the face crop from the webcam frame. It examines skin texture and light reflection patterns to determine whether the face is real or a reproduction. Only faces with a real-face probability above **90%** are passed to the recognition step.

**5. Logging attendance**
Once a student is identified as real and recognized, the system checks whether they have already been marked today. If not, their `student_id` and a local timestamp are inserted into the `Attendance` table. The supervisor can then export this table as a CSV and reset it for the next session.

---

## ⚠️ Notes

- The database file `attendance.db` is created automatically on first run.
- Liveness detection requires the anti-spoof model weights to be present — the app will not mark attendance without them.
- The system marks each student **once per calendar day** regardless of how many times their face appears.
- For best recognition accuracy, register students in good lighting with a clear, front-facing photo.

---

## ☁️ Deployment Notes — Why This App Must Run Locally

Deploying this project to **Streamlit Community Cloud** was attempted but ultimately not feasible due to two fundamental constraints:

### 1. 🧱 Heavy Dependencies
The core libraries this project relies on — primarily `face_recognition` (which is built on top of `dlib`) and `PyTorch` (required for the liveness detection model) — are computationally heavy and have complex native build requirements. Streamlit Community Cloud's free tier does not provide sufficient resources (memory, build time, or compute) to install and run these libraries reliably. Build processes consistently failed or timed out during deployment attempts.

### 2. 📷 Camera Access Limitation
The live attendance feature depends on direct access to the machine's physical webcam via `cv2.VideoCapture(0)`. This approach works perfectly when the app runs on a local machine because it opens the system camera directly. On remote cloud servers, however, there is no physical camera device attached — the server has no hardware webcam to connect to. While Streamlit does provide a `st.camera_input()` widget that captures a single frame through the browser, it cannot support a continuous real-time video stream, which is essential for the live recognition loop in Tab 2.

### ✅ Running the Project Locally — Step by Step

Since cloud deployment is not viable, follow these steps to run the project on your own machine:

**Step 1 — Prerequisites**

Make sure you have the following installed:
- Python **3.10** (other versions may cause compatibility issues with `dlib`)
- **CMake** (required to build `dlib`):
  - Windows: `winget install Kitware.CMake`
  - macOS: `brew install cmake`
  - Linux: `sudo apt install cmake`
- A working **webcam** connected to your machine

**Step 2 — Clone the repository**

```bash
git clone https://github.com/your-username/smart-attendance-system.git
cd smart-attendance-system
```

**Step 3 — Install dependencies**

```bash
pip install -r requirements.txt
```

> ⚠️ Make sure you're using **Python 3.10**. Other versions may cause compatibility issues with `dlib` and `face_recognition`.

**Step 4 — Download the anti-spoofing model weights**

Download the model file from the [Silent-Face-Anti-Spoofing](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing) repository and place it at:

```
resources/anti_spoof_models/4_0_0_300x300_MultiFTNet.pth
```

**Step 5 — Run the app**

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 👨‍💻 Author

**Ahmed Hossam**
