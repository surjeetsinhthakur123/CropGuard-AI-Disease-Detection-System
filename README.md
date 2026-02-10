
# 🌱 CropGuard AI – Intelligent Crop Disease Detection System

CropGuard AI is a **full-stack AI-powered crop disease detection platform** designed to assist farmers using **computer vision, environmental intelligence, explainable AI, offline edge inference, and multilingual voice guidance**.

The system works in **both online (cloud AI)** and **offline (edge AI using TensorFlow Lite)** modes, making it suitable for real-world rural and low-connectivity environments.

---

## 🚀 Key Features

### 🖼️ AI-Based Disease Detection
- Upload crop images or capture via camera
- Automatic crop & disease identification using CNN
- Confidence-based severity analysis

### 🧠 Explainable AI (XAI)
- Grad-CAM heatmaps highlighting infected regions
- Transparent AI reasoning for predictions

### 🌦 Environmental Intelligence
- Temperature & humidity aware severity assessment
- Weather-based reliability scoring

### 📴 Offline Edge AI Support
- Works without internet using **TFLite**
- Offline predictions stored locally
- Automatic sync when internet is restored

### 🔊 Multilingual Voice Assistant
- AI-generated voice summary using Text-to-Speech
- Supported languages:
  - English 🇬🇧
  - Hindi 🇮🇳
  - Marathi 🇮🇳

### 📄 PDF Report Generation
- Downloadable crop health report
- QR code embedded summary
- Unicode font support for Indian languages

### 🧑‍🌾 Farmer Feedback Loop
- Correct / Incorrect prediction feedback
- Post-treatment outcome collection
- Feedback stored for AI improvement

---

## 🧰 Tech Stack

**Frontend**
- Streamlit
- HTML + CSS

**Backend**
- Flask (REST API)
- SQLite Database

**AI / ML**
- TensorFlow / Keras (CNN)
- TensorFlow Lite (Offline Edge AI)
- Grad-CAM (Explainable AI)

**Utilities**
- OpenCV
- gTTS (Voice)
- ReportLab (PDF)
- OpenWeather API

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/surjeetsinhthakur123/CropGuard-AI-Disease-Detection-System.git
cd CropGuard-AI
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Environment Variables
Create a `.env` file:
```env
WEATHER_API_KEY=your_openweather_api_key
```

### 5️⃣ Run Backend Server
```bash
cd backend
python app.py
```

### 6️⃣ Run Frontend Application
```bash
streamlit run app.py
```

---

## 🧠 AI Decision Modes

| Input Condition | AI Mode |
|----------------|--------|
| Image + Internet | CNN (Cloud AI) |
| Image + No Internet | TFLite (Edge AI) |
| No Image | Rule-Based Environmental AI |

---

## 📴 Offline Mode Workflow
1. Internet unavailable detected
2. Edge AI (TFLite) inference executed
3. Result saved locally
4. Auto-sync with backend when online

---

## 🧪 APIs Used

| Endpoint | Description |
|--------|------------|
| `/analyze` | Crop disease analysis |
| `/feedback` | Farmer feedback |
| `/sync-offline` | Offline data synchronization |
| `/weather` | Live weather information |

---

## 🎓 Use Cases
- Farmers & agricultural advisors
- Rural offline diagnostics
- AI in agriculture research
- College & internship projects

---

## 📌 Future Enhancements
- Mobile application
- More crop varieties
- Feedback-based model retraining
- IoT sensor integration
- Government agriculture system integration

---

## 👨‍💻 Author
**Surjeetsinh Nandkumar Thakur**  
BTech CSE | AI & Data Analytics  
🌱 *Building practical AI solutions for agriculture*

---

## ⭐ Support
If you find this project useful:
- ⭐ Star the repository
- 🍴 Fork it
- 📢 Share it with others
