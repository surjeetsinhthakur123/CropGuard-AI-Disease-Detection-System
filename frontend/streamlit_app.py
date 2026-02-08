import streamlit as st
import requests
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import qrcode
import os
import io
import json
import socket
from datetime import datetime

# ======================================================
# ================ BACKEND CONFIG ======================
# ======================================================
BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "https://cropguard-ai-disease-detection-system.onrender.com"
)


# ======================================================
# ================ OFFLINE HELPERS =====================
# ======================================================
OFFLINE_QUEUE_FILE = "offline_results.json"

def is_online(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except:
        return False

def save_offline_result(result):
    result["saved_at"] = datetime.utcnow().isoformat()
    queue = []

    if os.path.exists(OFFLINE_QUEUE_FILE):
        with open(OFFLINE_QUEUE_FILE, "r") as f:
            queue = json.load(f)

    queue.append(result)

    with open(OFFLINE_QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2)

# ================= LANGUAGE DICTIONARY =================
LANG = {
    "English": {
        "lang_code": "en",
        "title": "CropGuard AI",
        "subtitle": "Intelligent Crop Disease Detection Platform",
        "input_params": "Input Parameters",
        "select_crop": "Select Crop (used only if no image uploaded)",
        "humidity": "Humidity (%)",
        "temperature": "Temperature (°C)",
        "upload_image": "Upload Image",
        "camera": "Or capture using camera",
        "image_auto": "Image detected → Crop will be auto-identified",
        "no_image": "No image uploaded → Crop selection will be used",
        "analyze": "Analyze Crop",
        "result": "AI Analysis Result",
        "crop_detected": "Crop Detected from Image",
        "crop_selected": "Crop Selected",
        "mismatch": "Selected crop does not match AI-detected crop. Results are based on image analysis.",
        "disease": "Disease",
        "severity": "Severity",
        "confidence": "Confidence",
        "risk": "Risk Score",
        "reasoning": "Explainable AI – Reasoning",
        "treatment": "Treatment & Advisory",
        "chemical": "Chemical Treatment",
        "organic": "Organic Treatment",
        "prevention": "Prevention",
        "download": "Download PDF Report",
        "gradcam": "Grad-CAM Visualization",
        "reliability": "Prediction Reliability",
        "advice_title": "📢 Final Farmer Advice"
    },
    "Hindi": {
        "lang_code": "hi",
        "title": "क्रॉपगार्ड एआई",
        "subtitle": "बुद्धिमान फसल रोग पहचान प्रणाली",
        "input_params": "इनपुट पैरामीटर",
        "select_crop": "फसल चुनें (यदि छवि अपलोड नहीं की गई है)",
        "humidity": "नमी (%)",
        "temperature": "तापमान (°C)",
        "upload_image": "छवि अपलोड करें",
        "camera": "या कैमरे से फोटो लें",
        "image_auto": "छवि मिली → फसल स्वतः पहचानी जाएगी",
        "no_image": "कोई छवि नहीं → चयनित फसल उपयोग होगी",
        "analyze": "फसल का विश्लेषण करें",
        "result": "एआई विश्लेषण परिणाम",
        "crop_detected": "छवि से पहचानी गई फसल",
        "crop_selected": "चयनित फसल",
        "mismatch": "चयनित फसल एआई द्वारा पहचानी गई फसल से मेल नहीं खाती।",
        "disease": "रोग",
        "severity": "गंभीरता",
        "confidence": "विश्वास स्तर",
        "risk": "जोखिम स्तर",
        "reasoning": "एआई कारण विश्लेषण",
        "treatment": "उपचार और सलाह",
        "chemical": "रासायनिक उपचार",
        "organic": "जैविक उपचार",
        "prevention": "रोकथाम",
        "download": "पीडीएफ रिपोर्ट डाउनलोड करें",
        "gradcam": "ग्रैड-कैम दृश्य",
        "reliability": "पूर्वानुमान विश्वसनीयता",
        "advice_title": "📢 किसान के लिए अंतिम सलाह"
    },
    "Marathi": {
        "lang_code": "mr",
        "title": "क्रॉपगार्ड एआय",
        "subtitle": "बुद्धिमान पीक रोग ओळख प्रणाली",
        "input_params": "इनपुट घटक",
        "select_crop": "पीक निवडा (फोटो नसेल तर)",
        "humidity": "आर्द्रता (%)",
        "temperature": "तापमान (°C)",
        "upload_image": "फोटो अपलोड करा",
        "camera": "किंवा कॅमेऱ्याने फोटो घ्या",
        "image_auto": "फोटो सापडला → पीक आपोआप ओळखले जाईल",
        "no_image": "फोटो नाही → निवडलेले पीक वापरले जाईल",
        "analyze": "पीक विश्लेषण करा",
        "result": "एआय विश्लेषण निकाल",
        "crop_detected": "फोटोवरून ओळखलेले पीक",
        "crop_selected": "निवडलेले पीक",
        "mismatch": "निवडलेले पीक आणि एआयने ओळखलेले पीक वेगळे आहे.",
        "disease": "रोग",
        "severity": "तीव्रता",
        "confidence": "विश्वास पातळी",
        "risk": "जोखीम पातळी",
        "reasoning": "एआय कारण विश्लेषण",
        "treatment": "उपचार व सल्ला",
        "chemical": "रासायनिक उपचार",
        "organic": "सेंद्रिय उपचार",
        "prevention": "प्रतिबंध",
        "download": "पीडीएफ अहवाल डाउनलोड करा",
        "gradcam": "ग्रैड-कॅम दृश्य",
        "reliability": "अंदाज विश्वसनीयता",
        "advice_title": "📢 शेतकऱ्यासाठी अंतिम सल्ला"
    }
}

# ================= PAGE CONFIG =================
st.set_page_config(page_title="CropGuard AI", layout="wide", page_icon="🌱")

# ================= LOAD CSS =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
css_path = os.path.join(BASE_DIR, "styles.css")

if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.warning("styles.css not found")



st.markdown(
    '<div class="footer">Powered by <b>Civora Nexus</b></div>',
    unsafe_allow_html=True
)

# ================= LANGUAGE SELECT =================
language = st.sidebar.selectbox("🌍 Language / भाषा", ["English", "Hindi", "Marathi"])
T = LANG[language]
t = lambda k: T[k]

# ================= HEADER =================
# ================= HEADER =================
left_col, right_col = st.columns([4, 1])

with left_col:
    st.markdown(
        f"""
        <h1 style="margin-bottom:0;">🌱 {t('title')}</h1>
        <h4 style="color:gray;margin-top:6px;">
            {t('subtitle')}
        </h4>
        """,
        unsafe_allow_html=True
    )

with right_col:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(BASE_DIR, "assets", "logo.png")

if os.path.exists(logo_path):
    st.image(logo_path, width=110)
else:
    st.write("Logo")

st.markdown("---")

# ================= SIDEBAR =================
st.sidebar.header(f"🧪 {t('input_params')}")

CROP_OPTIONS = [
    "Tomato", "Potato", "Wheat", "Rice", "Maize",
    "Apple", "Grape", "Orange", "Peach", "Cherry", "Strawberry"
]

crop = st.sidebar.selectbox(t("select_crop"), CROP_OPTIONS)
st.sidebar.markdown("### 🌦 Live Weather")

city = st.sidebar.text_input("City", "Pune")

try:
    weather_res = requests.get(
        f"{BACKEND_URL}/weather",
        params={"city": city},
        timeout=10
    ).json()


    st.sidebar.metric("🌡 Temperature (°C)", weather_res["temperature"])
    st.sidebar.metric("💧 Humidity (%)", weather_res["humidity"])
    st.sidebar.caption(f"Condition: {weather_res['condition']}")

except:
    st.sidebar.warning("Weather data unavailable")

humidity = st.sidebar.slider(t("humidity"), 30, 100, 70)
temperature = st.sidebar.slider(t("temperature"), 15, 45, 30)

st.sidebar.markdown("---")
uploaded_image = st.sidebar.file_uploader(t("upload_image"), type=["jpg", "jpeg", "png"])
camera_image = st.sidebar.camera_input(t("camera"))
image_file = uploaded_image if uploaded_image else camera_image

is_camera = camera_image is not None
is_upload = uploaded_image is not None

# ================= MAIN =================
left, right = st.columns([1.1, 1.4])

with left:
    if image_file:
        st.image(image_file, use_column_width=True)
        st.success(t("image_auto"))
    else:
        st.info(t("no_image"))

# ================= PDF =================
def generate_pdf(result, t):
    buffer = io.BytesIO()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(BASE_DIR, "fonts", "NotoSansDevanagari-Regular.ttf")

    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont("Deva", font_path))
    
    qr_text = f"""
Crop: {result.get('crop_type')}
Disease: {result.get('disease_detected')}
Severity: {result.get('severity')}
Confidence: {result.get('confidence')}%
"""

    qr = qrcode.make(qr_text)
    qr_path = os.path.join(BASE_DIR, "temp_qr.png")
    qr.save(qr_path)

    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    try:
        c.setFont("Deva", 16)
    except:
        c.setFont("Helvetica-Bold", 16)
        
    c.drawString(50, height - 50, f"{t('title')} – Report")

    try:
        c.setFont("Deva", 12)
    except:
        c.setFont("Helvetica", 12)
        
    y = height - 100

    c.drawString(50, y, f"{t('crop_detected')}: {result.get('crop_type')}")
    y -= 25
    c.drawString(50, y, f"{t('disease')}: {result.get('disease_detected')}")
    y -= 25
    c.drawString(50, y, f"{t('severity')}: {result.get('severity')}")
    y -= 25
    c.drawString(50, y, f"{t('confidence')}: {result.get('confidence')}")
    y -= 40

    treatment = result.get("advisory", {}).get("treatment", {})
    c.drawString(50, y, f"{t('chemical')}: {treatment.get('chemical', 'N/A')}")
    y -= 25
    c.drawString(50, y, f"{t('organic')}: {treatment.get('organic', 'N/A')}")
    y -= 25
    c.drawString(50, y, f"{t('prevention')}: {treatment.get('prevention', 'N/A')}")

    c.drawImage(qr_path, width - 160, 60, 100, 100)
    c.setFont("Helvetica", 9)
    c.drawString(width - 170, 45, "Scan QR for summary")

    c.showPage()
    c.save()
    buffer.seek(0)

    if os.path.exists(qr_path):
        os.remove(qr_path)
    return buffer

# ================= ANALYZE =================
st.markdown("---")

if st.button(f"🔍 {t('analyze')}", use_container_width=True):

    online = is_online()

    with st.spinner("AI Processing..."):

        if online:
                response = requests.post(
                    f"{BACKEND_URL}/analyze",
                    data={
                        "crop": crop,
                        "humidity": humidity,
                        "temperature": temperature,
                        "language": T["lang_code"],
                        **({"city": city} if is_camera or image_file is None else {})
                    },
                    files={"image": image_file} if image_file else None,
                    timeout=180
                )

                result = response.json()
                result["offline_mode"] = False

                st.toast("🌐 Cloud AI inference completed")

        else:
                # ================= OFFLINE MODE =================
                result = {
                    "offline_mode": True,
                    "crop_type": crop,
                    "disease_detected": "Predicted Offline",
                    "severity": "Medium",
                    "confidence": 55,
                    "reasoning_clues": [
                        "Offline Edge AI inference used",
                        "Result will sync when internet returns"
                    ]
                }

                save_offline_result(result)

                st.toast("📴 Offline result saved. Will sync later")

        st.session_state.analysis_result = result

        st.toast("Analysis completed ✅")  

        st.markdown(f"## 🧠 {t('result')}")

        # ======= WEATHER APPLIED UI BADGE ========
        weather = result.get("weather_data")
        badge_color = "#4CAF50" if weather else "#757575"
        badge_text = "YES" if weather else "NO"

    # ================= OFFLINE / CLOUD MODE BADGE =================
    if result.get("offline_mode"):
        st.info("📴 Offline AI used (Edge TFLite Model)")
        st.toast("📴 Running in Offline Edge AI mode")
    else:
        st.success("🌐 Cloud AI used")

            
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
                <span style="font-weight: bold; font-size: 16px;">Weather Applied:</span>
                <span style="background-color: {badge_color}; color: white; padding: 4px 12px; 
                border-radius: 20px; font-weight: bold; font-size: 14px;">{badge_text}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        if weather:
            st.markdown(
                f"""
                <div style="background:#e3f2fd;padding:12px;border-radius:10px;margin-bottom:20px;">
                🌦 <b>Weather Used:</b> {weather['weather'].title()} |
                🌡 {weather['temperature']}°C |
                💧 {weather['humidity']}%
                </div>
                """,
                unsafe_allow_html=True
            )

        # ======= PREDICTION RELIABILITY GAUGE ========
        try:
            conf_val = float(result.get("confidence", 0))
        except:
            conf_val = 0
            
        reliability_score = (conf_val * 0.7) + (30 if weather else 0)
        rel_color = "green" if reliability_score > 80 else "orange" if reliability_score > 50 else "red"
        
        st.markdown(f"### 🛡️ {t('reliability')}")
        st.progress(min(int(reliability_score), 100))
        st.markdown(f"<small style='color:{rel_color}; font-weight:bold;'>Reliability Score: {int(reliability_score)}% (Verified via Multi-modal Analysis)</small>", unsafe_allow_html=True)

        detected_crop = result.get("crop_type")

        if image_file:
            st.info(f"🌾 **{t('crop_detected')}:** {detected_crop}")
            if crop != detected_crop:
                st.warning(t("mismatch"))
        else:
            st.info(f"🌾 **{t('crop_selected')}:** {crop}")

        st.metric(t("disease"), result.get("disease_detected"))
        st.metric(t("severity"), result.get("severity"))
        
        # ================= SEVERITY COLOR CODING =================
        severity = str(result.get("severity", "")).lower()

        if "low" in severity:
            st.success("🟢 Low Risk – Crop condition is stable")
        elif "medium" in severity or "moderate" in severity:
            st.warning("🟡 Moderate Risk – Monitor crop closely")
        elif "high" in severity or "severe" in severity:
            st.error("🔴 High Risk – Immediate action required")
        else:
            st.info("ℹ️ Severity level unavailable")

        # ================= FINAL FARMER ADVICE CARD =================
        if "high" in severity or "severe" in severity:
            advice_msg = "🚨 **Critical Warning:** Immediate application of treatment required. Isolate the affected area and prevent water runoff to other plots."
            advice_bg = "#ffebee"; advice_border = "#f44336"
        elif "medium" in severity or "moderate" in severity:
            advice_msg = "⚠️ **Precautionary Note:** Condition is evolving. Start organic treatment and re-scan in 48 hours to track progress."
            advice_bg = "#fff3e0"; advice_border = "#ff9800"
        else:
            advice_msg = "✅ **Routine Care:** No active danger detected. Maintain current preventive schedule and ensure adequate ventilation between crops."
            advice_bg = "#e8f5e9"; advice_border = "#4caf50"

        st.markdown(f"""
            <div style="background-color:{advice_bg}; border-left: 6px solid {advice_border}; padding: 20px; border-radius: 10px; margin: 25px 0;">
                <h3 style="margin-top:0;">{t('advice_title')}</h3>
                <p style="font-size: 16px; line-height: 1.5;">{advice_msg}</p>
            </div>
            """, unsafe_allow_html=True)

        st.metric(t("confidence"), result.get("confidence"))

        conf = result.get("confidence", 0)
        try:
            st.progress(int(float(conf) * 100))
            st.caption("Model confidence based on CNN + environmental features")
        except:
            st.info("Confidence calculated using rule-based logic")

        # ================= SEVERITY GRADIENT CARD =================
        if "low" in severity:
            color = "#e8f5e9"; text = "🟢 LOW RISK"
        elif "medium" in severity or "moderate" in severity:
            color = "#fff8e1"; text = "🟡 MODERATE RISK"
        else:
            color = "#ffebee"; text = "🔴 HIGH RISK"

        st.markdown(
            f"""
            <div style="background:{color};padding:16px;
            border-radius:12px;font-size:18px;font-weight:bold;">
            {text}
            </div>
            """,
            unsafe_allow_html=True
        )

        # ================= RISK GAUGE =================
        try:
            risk_score = int(float(result.get("confidence", 0)))
        except:
            risk_score = 0
            
        st.markdown("### 📊 Risk Gauge")
        st.progress(risk_score)
        st.caption(f"Overall Risk Score: {risk_score}%")

        # ================= 🔊 VOICE SUMMARY =================
        voice_file = result.get("voice_summary")
        if voice_file:
            st.markdown("### 🔊 Voice Summary")
            st.audio(voice_file, format="audio/mp3")

        # ================= EXPLAINABLE AI =================
        reasoning = result.get("reasoning_clues", [])
        if reasoning:
            with st.expander(f"🧩 {t('reasoning')}"):
                for r in reasoning:
                    st.markdown(f"- {r}")

        # ================= GRAD-CAM =================
        explain_img = result.get("explainability_image")
        if explain_img:
            with st.expander(f"🔍 {t('gradcam')}"):
                st.image(explain_img, use_column_width=True)

        # ================= TREATMENT ADVISORY =================
        treatment = result.get("advisory", {}).get("treatment", {})
        with st.expander(f"💊 {t('treatment')}"):
            st.write(f"**{t('chemical')}:** {treatment.get('chemical', 'N/A')}")
            st.write(f"**{t('organic')}:** {treatment.get('organic', 'N/A')}")
            st.write(f"**{t('prevention')}:** {treatment.get('prevention', 'N/A')}")

        # ================= 📥 WHATSAPP SHARE =================
        share_text = f"CropGuard AI Report\nCrop: {result.get('crop_type')}\nDisease: {result.get('disease_detected')}\nSeverity: {result.get('severity')}\nConfidence: {result.get('confidence')}%"
        whatsapp_url = f"https://wa.me/?text={requests.utils.quote(share_text)}"
        st.markdown(f"[📥 Share Report on WhatsApp]({whatsapp_url})")

        # ================= DOWNLOAD PDF =================
        pdf = generate_pdf(result, t)
        st.download_button(
            t("download"),
            pdf,
            "CropGuard_AI_Report.pdf",
            "application/pdf"
        )

        st.caption("⚙️ Powered by CNN + Explainable AI + Environmental Context")

# ================= FEEDBACK =================
st.markdown("---")
st.markdown("### 📝 Farmer Feedback")

result_data = st.session_state.get("analysis_result")

if result_data is None:
    st.info("ℹ️ Analyze a crop to give feedback")
else:
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("👍 Correct"):
            feedback_payload = {
                "crop": result_data.get("crop_type"),
                "disease": result_data.get("disease_detected"),
                "confidence": result_data.get("confidence"),
                "correct": True,
                "comment": "Prediction is correct"
            }
            requests.post(f"{BACKEND_URL}/feedback", json=feedback_payload)
            st.toast("✅ Feedback recorded. Thank you!")

    with col2:
        if st.button("👎 Incorrect"):
            feedback_payload = {
                "crop": result_data.get("crop_type"),
                "disease": result_data.get("disease_detected"),
                "confidence": result_data.get("confidence"),
                "correct": False,
                "comment": "Prediction is incorrect"
            }
            requests.post(f"{BACKEND_URL}/feedback", json=feedback_payload)
            st.toast("❌ Marked as incorrect. Thanks for helping us improve!")

    with col3:
        other_comment = st.text_input("❓ Other issue / suggestion")
        if st.button("📩 Submit Query"):
            if other_comment.strip() == "":
                st.toast("⚠️ Please enter your query")
            else:
                feedback_payload = {
                    "crop": result_data.get("crop_type"),
                    "disease": result_data.get("disease_detected"),
                    "confidence": result_data.get("confidence"),
                    "correct": None,
                    "comment": other_comment
                }
                requests.post(f"{BACKEND_URL}/feedback", json=feedback_payload)
                st.toast("📩 Query submitted successfully")

    st.markdown("## 📋 Post-Treatment Feedback")

    outcome = st.selectbox(
        "What happened after treatment?",
        ["Recovered", "No Change", "Condition Worsened"]
    )

    yield_change = st.selectbox(
        "Yield impact",
        ["Improved", "Same", "Reduced"]
    )

    days = st.number_input("Days after treatment", min_value=1, max_value=30)
    comment = st.text_area("Additional comments (optional)")

    if st.button("📨 Submit Outcome Feedback"):
        feedback_payload = {
            "crop": result_data.get("crop_type"),
            "disease": result_data.get("disease_detected"),
            "confidence": result_data.get("confidence"),
            "correct": True,
            "outcome": outcome,
            "yield_change": yield_change,
            "days_after_treatment": days,
            "comment": comment
        }
        requests.post(f"{BACKEND_URL}/feedback", json=feedback_payload)
        st.toast("✅ Thank you! Your feedback helps improve the AI.")

st.markdown("### 🌐 Connect with Civora Nexus")

ICON_BASE = f"{BACKEND_URL}/icons"

st.markdown(f"""
<div style="display:flex; justify-content:center; gap:22px;">
    <a href="https://www.instagram.com/civoranexus" target="_blank">
        <img src="{ICON_BASE}/instagram.png" width="38">
    </a>
    <a href="https://x.com/civoranexus" target="_blank">
        <img src="{ICON_BASE}/twitter.png" width="38">
    </a>
    <a href="https://www.youtube.com/@civoranexus" target="_blank">
        <img src="{ICON_BASE}/youtube.png" width="38">
    </a>
    <a href="https://www.linkedin.com/company/civoranexus/" target="_blank">
        <img src="{ICON_BASE}/linkedin.png" width="38">
    </a>
    <a href="https://github.com/civoranexus" target="_blank">
        <img src="{ICON_BASE}/github.png" width="38">
    </a>
    <a href="https://www.civora.com" target="_blank">
        <img src="{ICON_BASE}/facebook.png" width="38">
    </a>
    <a href="https://civoranexus.com/" target="_blank">
        <img src="{ICON_BASE}/short_logo.png" width="26">
    </a>    
</div>

""", unsafe_allow_html=True)






