# 🤖 Assistive Medication Robot

An end-to-end **assistive robotics system** that safely identifies, verifies, and dispenses medication using **computer vision, a mobile robot, and a web application**. The project integrates **React**, **FastAPI**, **MongoDB**, and **Raspberry Pi–based robotics hardware** to demonstrate a real-world healthcare robotics solution.

---

## ✨ Features

* 🧠 **Pill recognition with computer vision** (ML-based verification)
* 🤖 **Autonomous robotic dispensing** (GoPiGo3 + robotic arm)
* 🌐 **React web application** for caregivers/patients
* ⚡ **FastAPI backend** for orchestration and control
* 🗄️ **MongoDB database** for schedules, patients, and logs
* 🔔 **Real-time status updates & confirmations**

---

## 🏗️ System Architecture

```
React Web App
      ↓ (REST API)
FastAPI Backend
      ↓
MongoDB  ←→  Robot Control Layer
                  ↓
        Computer Vision + ML
                  ↓
           GoPiGo3 + Arm
```

---

## 🛠️ Technology Stack

### Frontend

* React (JavaScript / TypeScript)
* REST API communication
* Mobile-friendly web UI

### Backend

* FastAPI (Python)
* RESTful APIs
* PyMongo / Motor

### Database

* MongoDB

### Robotics & Vision

* Raspberry Pi 5
* GoPiGo3 Robot Base
* Raspberry Pi Camera Module
* OpenCV, NumPy
* PCA9685 Servo Driver
* MG996R Servos

---


---

## 🚀 Getting Started

### 1️⃣ Prerequisites

* Node.js (v18+ recommended)
* Python 3.9+
* MongoDB (local or Atlas)
* Raspberry Pi OS (Bookworm)
* GoPiGo3 hardware (for full deployment)

---

## 🌐 Frontend (React App)

### Install Dependencies

```bash
cd frontend
npm install
```

### Run Development Server

```bash
npm start
```

The app will run at:

```
http://localhost:3000
```

---

## ⚙️ Backend (FastAPI)

### Create Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
MONGO_URI=mongodb://localhost:27017
DB_NAME=medication_robot
```

### Run FastAPI Server

```bash
uvicorn app.main:app --reload
```

Backend will be available at:

```
http://localhost:8000
```

Interactive API docs:

```
http://localhost:8000/docs
```

---

## 🤖 Robot & Vision (Raspberry Pi)

### Install System Dependencies

```bash
sudo apt update
sudo apt install python3-opencv python3-pip
```

### Install Python Libraries

```bash
pip3 install numpy opencv-python
```

### Run Robot Control Script

```bash
cd robot
python3 run_robot.py
```

> ℹ️ The vision system can also be tested on a **laptop webcam** before deploying to the Pi.

---

## 🗄️ MongoDB Collections (Example)

* `patients`
* `medications`
* `schedules`
* `dispense_logs`

---

## 🧪 Testing Modes

* **Laptop Mode:** Test ML + FastAPI without hardware
* **Pi Mode:** Full system integration

---

## 🔐 Safety & Reliability

* Pill verification before dispensing
* Confidence threshold for ML predictions
* Event logging in MongoDB
* Manual override via web app

---

## 🚧 Known Limitations

* Single-pill dispensing (current version)
* Android / web-first UI
* Limited dataset size for ML model

---

## 🔮 Future Improvements

* ROS2 integration
* Multi-pill storage & sorting
* Face recognition for patient ID
* iOS support
* Cloud-based ML updates

---

## 👤 Author

**Samuel Berhan**
Computer Science, Georgia State University

**Vivek Patel**
Computer Science, Georgia State University

---

## 📜 License

This project is for **academic and educational purposes**.

---


