"""
Laptop CV Demo
Runs on:
- Laptop webcam (live stream until quit)
- Static image fallback
Adds simple overlays to trace face and pill regions.
"""

import os
import time
from datetime import datetime

import cv2

# ----------------------------
# MOCK DATABASES
# ----------------------------

PATIENT_DATABASE = {
    "patient_1": {"name": "Sami Berhan", "required_pill": "tic tac"},
    "patient_2": {"name": "Mary Smith", "required_pill": "Vitamin D"},
}

PILL_DATABASE = {
    "red_round": "tic tac",
    "white_oval": "Vitamin D",
}

# How long to show the window (ms). None = run until key press (q or Esc).
DISPLAY_DURATION_MS = None
WINDOW_NAME = "Demo Frame"
FONT = cv2.FONT_HERSHEY_SIMPLEX
TEXT_COLOR = (255, 255, 255)
STATUS_OK_COLOR = (0, 200, 0)
STATUS_BAD_COLOR = (0, 0, 255)
INSTRUCTION_COLOR = (180, 180, 180)
FACE_COLOR = (0, 200, 255)
PILL_COLOR = (255, 170, 0)

# ----------------------------
# MOCK CV FUNCTIONS
# ----------------------------

def identify_patient(frame):
    # Demo logic (pretend face recognition)
    return "patient_1"


def identify_pill(frame):
    # Demo logic (pretend pill detection)
    return "red_round"


# ----------------------------
# HELPERS
# ----------------------------

def analyze_frame(frame):
    patient_id = identify_patient(frame)
    patient = PATIENT_DATABASE.get(patient_id)

    pill_id = identify_pill(frame)
    detected_pill = PILL_DATABASE.get(pill_id, "Unknown pill")

    is_ok = bool(patient) and detected_pill == patient["required_pill"]
    return patient, detected_pill, is_ok


def report_detection(patient, detected_pill, is_ok):
    patient_name = patient["name"] if patient else "Unknown"

    print("\nPatient Identified:")
    print(f"  Name: {patient_name}")

    print("\nPill Detected:")
    print(f"  Pill Type: {detected_pill}")

    print("\nMedication Check:")
    if is_ok:
        print("  Correct pill")
        print("  Administering medication")
    elif not patient or detected_pill == "Unknown pill":
        print("  Unable to verify pill/patient")
    else:
        print("  Incorrect pill")
        print("  Dispensing aborted")

    print("\nTimestamp:", datetime.now())


def overlay_text(frame, patient, detected_pill, is_ok):
    name = patient["name"] if patient else "Unknown"
    status = "Correct pill" if is_ok else "Incorrect pill"
    cv2.putText(frame, "Press q/Esc to quit", (20, 30), FONT, 0.6, INSTRUCTION_COLOR, 2, cv2.LINE_AA)
    cv2.putText(frame, f"Patient: {name}", (20, 60), FONT, 0.7, TEXT_COLOR, 2, cv2.LINE_AA)
    cv2.putText(frame, f"Pill: {detected_pill}", (20, 90), FONT, 0.7, TEXT_COLOR, 2, cv2.LINE_AA)
    cv2.putText(frame, status, (20, 120), FONT, 0.7, STATUS_OK_COLOR if is_ok else STATUS_BAD_COLOR, 2, cv2.LINE_AA)
    return frame


def draw_boxes(frame, face_boxes, pill_boxes):
    for (x, y, w, h) in face_boxes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), FACE_COLOR, 2)
        cv2.putText(frame, "face", (x, y - 10), FONT, 0.5, FACE_COLOR, 2, cv2.LINE_AA)
    for (x, y, w, h) in pill_boxes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), PILL_COLOR, 2)
        cv2.putText(frame, "pill", (x, y - 10), FONT, 0.5, PILL_COLOR, 2, cv2.LINE_AA)
    return frame


def load_demo_frame():
    if os.path.exists("demo_image.jpg"):
        fallback = cv2.imread("demo_image.jpg")
        if fallback is not None:
            return fallback
        print("[camera] demo_image.jpg exists but could not be loaded")
    raise RuntimeError("No webcam and no usable demo_image.jpg found")


def load_face_cascade():
    cascade_path = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
    if not os.path.exists(cascade_path):
        print("[face] Haar cascade file not found; skipping face tracing")
        return None
    cascade = cv2.CascadeClassifier(cascade_path)
    if cascade.empty():
        print("[face] Failed to load Haar cascade; skipping face tracing")
        return None
    return cascade


def detect_faces(frame, cascade):
    if cascade is None:
        return []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
    return faces


def detect_pills(frame):
    # Simple color-based heuristic to highlight bright/white/red regions
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    white_mask = cv2.inRange(hsv, (0, 0, 150), (180, 50, 255))
    red_mask_1 = cv2.inRange(hsv, (0, 120, 70), (10, 255, 255))
    red_mask_2 = cv2.inRange(hsv, (160, 120, 70), (179, 255, 255))
    mask = cv2.bitwise_or(white_mask, red_mask_1)
    mask = cv2.bitwise_or(mask, red_mask_2)
    mask = cv2.medianBlur(mask, 5)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    pill_boxes = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w * h < 400:  # filter tiny noise
            continue
        pill_boxes.append((x, y, w, h))
    return pill_boxes


# ----------------------------
# MAIN
# ----------------------------

def main(display_ms=DISPLAY_DURATION_MS):
    cap = cv2.VideoCapture(0)
    info_printed = False
    start_time = time.time()
    face_cascade = load_face_cascade()

    if cap.isOpened():
        print("[camera] Using laptop webcam; press q or Esc to quit")
        while True:
            success, frame = cap.read()
            if not success:
                print("[camera] Frame read failed; falling back to demo image")
                break

            patient, detected_pill, is_ok = analyze_frame(frame)

            if not info_printed:
                report_detection(patient, detected_pill, is_ok)
                info_printed = True

            face_boxes = detect_faces(frame, face_cascade)
            pill_boxes = detect_pills(frame)

            annotated = overlay_text(frame.copy(), patient, detected_pill, is_ok)
            annotated = draw_boxes(annotated, face_boxes, pill_boxes)
            cv2.imshow(WINDOW_NAME, annotated)

            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                break

            if display_ms is not None:
                elapsed_ms = (time.time() - start_time) * 1000
                if elapsed_ms >= display_ms:
                    break
        cap.release()
        cv2.destroyAllWindows()

        if info_printed:
            return
    else:
        print("[camera] Webcam unavailable; using demo image")

    frame = load_demo_frame()
    patient, detected_pill, is_ok = analyze_frame(frame)
    report_detection(patient, detected_pill, is_ok)

    face_boxes = detect_faces(frame, face_cascade)
    pill_boxes = detect_pills(frame)

    annotated = overlay_text(frame.copy(), patient, detected_pill, is_ok)
    annotated = draw_boxes(annotated, face_boxes, pill_boxes)

    wait_time = 0 if display_ms is None else max(int(display_ms), 1)
    cv2.imshow(WINDOW_NAME, annotated)
    cv2.waitKey(wait_time)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
