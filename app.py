import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
import re
import urllib.request
import urllib.parse

# Page configuration
st.set_page_config(
    page_title="AI गुरूकुल | ऋषिकेश चव्हाण",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# 💾 डेटाबेस व GOOGLE SHEETS सिंक व्यवस्था (HYBRID STORAGE)
# -------------------------------------------------------------
DATA_FILE = "gurukul_database.json"

def load_database():
    default_structure = {
        "class_access_code": "GURUKUL10",
        "google_sheet_webhook": "", # गुगल शीट वेब ॲप URL
        "student_logins": [
            {"नाव": "आर्यन पाटील", "इयत्ता": "१० वी (10th)", "रोल नं": "12", "ईमेल": "aryan.patil@example.com", "लॉगिन वेळ": "2026-09-02 10:15"},
            {"नाव": "सिया कुलकर्णी", "इयत्ता": "९ वी (9th)", "रोल नं": "24", "ईमेल": "siya.k@example.com", "लॉगिन वेळ": "2026-09-02 11:30"}
        ],
        "reaction_submissions": [],
        "doubt_records": [
            {"विद्यार्थी": "आर्यन पाटील", "इयत्ता": "१० वी", "शंका": "विस्थापन आणि दुहेरी विस्थापन अभिक्रियेतील मुख्य फरक काय?", "वेळ": "2026-09-02 10:20"}
        ]
    }
    
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(default_structure, f, ensure_ascii=False, indent=4)
        return default_structure
    
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default_structure

def save_database(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"डेटा स्थानिक सेव्ह करताना अडचण: {e}")

# गुगल शीटवर थेट डेटा पाठवणारे फंक्शन (Google Sheets Cloud Sync)
def send_to_google_sheet(payload_dict):
    webhook_url = st.session_state.db_data.get("google_sheet_webhook", "").strip()
    if not webhook_url:
        return False
    try:
        data = json.dumps(payload_dict).encode('utf-8')
        req = urllib.request.Request(
            webhook_url,
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status in [200, 302]
    except Exception:
        return False

# ॲप सुरू होताच डेटा लोड करणे
if "db_data" not in st.session_state:
    st.session_state.db_data = load_database()

if "logged_student" not in st.session_state:
    st.session_state.logged_student = None

def persist_all():
    save_database(st.session_state.db_data)

# -------------------------------------------------------------
# 🎨 CSS स्टाईलिंग
# -------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    .hero-box {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 50%, #06B6D4 100%);
        color: white;
        padding: 2.2rem 2rem;
        border-radius: 18px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.25);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        opacity: 0.95;
    }
    .feature-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.4rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        height: 100%;
    }
    .login-box {
        background: #ffffff;
        border: 2px solid #3b82f6;
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.12);
        max-width: 600px;
        margin: auto;
    }
    .user-welcome-chip {
        background-color: #ecfdf5;
        border: 1px solid #10b981;
        color: #065f46;
        padding: 0.7rem 1.2rem;
        border-radius: 10px;
        display: inline-block;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        border-left: 5px solid #3b82f6;
        box-shadow: 0 4px 10px rgba(0,0,0,0.04);
        text-align: center;
    }
    .kpi-num {
        font-size: 2rem;
        font-weight: 700;
        color: #1e3a8a;
    }
    .kpi-title {
        font-size: 0.9rem;
        color: #64748b;
    }
    .reaction-card {
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-left: 5px solid #2563eb;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 🎯 प्रश्नांचा डेटा (QUIZ DATA)
# -------------------------------------------------------------
QUIZ_DATABASE = {
    "🤖 कृत्रिम बुद्धिमत्ता (AI & IT)": [
        {
            "question": "संगणकाला स्वतः शिकण्याची व निर्णय घेण्याची क्षमता देणाऱ्या तंत्रज्ञानाला काय म्हणतात?",
            "options": ["हार्डवेअर (Hardware)", "मशीन लर्निंग / AI", "ऑपरेटिंग सिस्टीम", "फोटोशॉप"],
            "answer": "मशीन लर्निंग / AI",
            "explanation": "Machine Learning हा AI चा भाग असून संगणक डेटावरून आपोआप शिकतो."
        },
        {
            "question": "ChatGPT आणि Gemini हे AI च्या कोणत्या प्रकारात मोडतात?",
            "options": ["Robotic Hardware", "Generative AI (LLM)", "Antivirus Tool", "Database"],
            "answer": "Generative AI (LLM)",
            "explanation": "हे Large Language Models (LLM) असून नवीन मजकूर तयार करतात."
        }
    ],
    "🔬 सामान्य विज्ञान (Science)": [
        {
            "question": "पाण्याचे रासायनिक सूत्र (Chemical Formula) काय आहे?",
            "options": ["CO2", "NaCl", "H2O", "O2"],
            "answer": "H2O",
            "explanation": "हायड्रोजन आणि ऑक्सिजन मिळून पाणी (H2O) तयार होते."
        },
        {
            "question": "पृथ्वीच्या पृष्ठभागावर गुरुत्वीय त्वरण ($g$) चे सरासरी मूल्य किती असते?",
            "options": ["$9.8 \\text{ m/s}^2$", "$8.9 \\text{ m/s}^2$", "$10.5 \\text{ m/s}^2$", "$0 \\text{ m/s}^2$"],
            "answer": "$9.8 \\text{ m/s}^2$",
            "explanation": "पृथ्वीवरील सरासरी गुरुत्वीय त्वरण $9.8 \\text{ m/s}^2$ असते."
        }
    ]
}

# -------------------------------------------------------------
# 🧪 रासायनिक अभिक्रियांचा संपूर्ण सराव डेटा (२० अभिक्रिया)
# -------------------------------------------------------------
REACTION_OPTIONS = [
    "➕ संयोग अभिक्रिया (Combination)",
    "💥 अपघटन अभिक्रिया (Decomposition)",
    "🔄 विस्थापन अभिक्रिया (Displacement)",
    "🔀 दुहेरी विस्थापन अभिक्रिया (Double Displacement)"
]

REACTIONS_DATA = [
    {"id": 1, "reaction": r"\text{Li}_2\text{O} + \text{H}_2\text{O} \longrightarrow 2\text{LiOH}", "correct": "➕ संयोग अभिक्रिया (Combination)"},
    {"id": 2, "reaction": r"2\text{KClO}_3 \xrightarrow{\Delta} 2\text{KCl} + 3\text{O}_2\uparrow", "correct": "💥 अपघटन अभिक्रिया (Decomposition)"},
    {"id": 3, "reaction": r"\text{Mg} + 2\text{AgNO}_3 \longrightarrow \text{Mg(NO}_3)_2 + 2\text{Ag}", "correct": "🔄 विस्थापन अभिक्रिया (Displacement)"},
    {"id": 4, "reaction": r"\text{Pb(NO}_3)_2 + 2\text{KI} \longrightarrow \text{PbI}_2\downarrow + 2\text{KNO}_3", "correct": "🔀 दुहेरी विस्थापन अभिक्रिया (Double Displacement)"},
    {"id": 5, "reaction": r"2\text{NO} + \text{O}_2 \longrightarrow 2\text{NO}_2", "correct": "➕ संयोग अभिक्रिया (Combination)"},
    {"id": 6, "reaction": r"\text{NH}_4\text{NO}_3 \xrightarrow{\Delta} \text{N}_2\text{O} + 2\text{H}_2\text{O}", "correct": "💥 अपघटन अभिक्रिया (Decomposition)"},
    {"id": 7, "reaction": r"\text{Ni} + 2\text{HCl} \longrightarrow \text{NiCl}_2 + \text{H}_2\uparrow", "correct": "🔄 विस्थापन अभिक्रिया (Displacement)"},
    {"id": 8, "reaction": r"\text{Al}_2(\text{SO}_4)_3 + 6\text{NaOH} \longrightarrow 2\text{Al(OH)}_3\downarrow + 3\text{Na}_2\text{SO}_4", "correct": "🔀 दुहेरी विस्थापन अभिक्रिया (Double Displacement)"},
    {"id": 9, "reaction": r"\text{P}_4 + 6\text{Cl}_2 \longrightarrow 4\text{PCl}_3", "correct": "➕ संयोग अभिक्रिया (Combination)"},
    {"id": 10, "reaction": r"2\text{Al(OH)}_3 \xrightarrow{\Delta} \text{Al}_2\text{O}_3 + 3\text{H}_2\text{O}", "correct": "💥 अपघटन अभिक्रिया (Decomposition)"},
    {"id": 11, "reaction": r"\text{Cl}_2 + 2\text{NaBr} \longrightarrow 2\text{NaCl} + \text{Br}_2", "correct": "🔄 विस्थापन अभिक्रिया (Displacement)"},
    {"id": 12, "reaction": r"\text{CuSO}_4 + 2\text{KOH} \longrightarrow \text{Cu(OH)}_2\downarrow + \text{K}_2\text{SO}_4", "correct": "🔀 दुहेरी विस्थापन अभिक्रिया (Double Displacement)"},
    {"id": 13, "reaction": r"\text{SO}_3 + \text{H}_2\text{O} \longrightarrow \text{H}_2\text{SO}_4", "correct": "➕ संयोग अभिक्रिया (Combination)"},
    {"id": 14, "reaction": r"2\text{Ag}_2\text{O} \xrightarrow{\Delta} 4\text{Ag} + \text{O}_2\uparrow", "correct": "💥 अपघटन अभिक्रिया (Decomposition)"},
    {"id": 15, "reaction": r"\text{Cr}_2\text{O}_3 + 2\text{Al} \longrightarrow \text{Al}_2\text{O}_3 + 2\text{Cr}", "correct": "🔄 विस्थापन अभिक्रिया (Displacement)"},
    {"id": 16, "reaction": r"\text{AgNO}_3 + \text{KBr} \longrightarrow \text{AgBr}\downarrow + \text{KNO}_3", "correct": "🔀 दुहेरी विस्थापन अभिक्रिया (Double Displacement)"},
    {"id": 17, "reaction": r"\text{BaO} + \text{CO}_2 \longrightarrow \text{BaCO}_3", "correct": "➕ संयोग अभिक्रिया (Combination)"},
    {"id": 18, "reaction": r"2\text{NaHCO}_3 \xrightarrow{\Delta} \text{Na}_2\text{CO}_3 + \text{H}_2\text{O} + \text{CO}_2\uparrow", "correct": "💥 अपघटन अभिक्रिया (Decomposition)"},
    {"id": 19, "reaction": r"\text{Sn} + 2\text{AgNO}_3 \longrightarrow \text{Sn(NO}_3)_2 + 2\text{Ag}", "correct": "🔄 विस्थापन अभिक्रिया (Displacement)"},
    {"id": 20, "reaction": r"\text{FeCl}_3 + 3\text{NH}_4\text{OH} \longrightarrow \text{Fe(OH)}_3\downarrow + 3\text{NH}_4\text{Cl}", "correct": "🔀 दुहेरी विस्थापन अभिक्रिया (Double Displacement)"}
]

# Helper to validate email format
def is_valid_email(email_str):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email_str.strip()) is not None

# -------------------------------------------------------------
# 🧭 SIDEBAR NAVIGATION
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("### 👨‍🏫 **शिक्षक प्रोफाईल**")
    st.markdown("""
    **नाव:** ऋषिकेश चव्हाण  
    **विषय:** गणित, विज्ञान आणि AI
    """)
    st.divider()

    if st.session_state.logged_student:
        st.success(f"👤 **लॉगिन विद्यार्थी:**\n**{st.session_state.logged_student['नाव']}** ({st.session_state.logged_student['इयत्ता']})")
        if st.button("🚪 लॉगआउट (Logout)", key="logout_btn", use_container_width=True):
            st.session_state.logged_student = None
            st.rerun()
        st.divider()

    selected_page = st.radio(
        "📌 **मेनू निवडा:**",
        [
            "🏠 मुख्य पान (Home)", 
            "📚 शालेय अभ्यासक्रम (Subjects) 🔒", 
            "🤖 AI लॅब & टूल्स (AI Lab)", 
            "📝 सराव चाचणी (Quiz Zone)",
            "📬 शंका विचारा (Doubt Box)",
            "📊 शिक्षक डॅशबोर्ड (Teacher Admin) 🔐"
        ]
    )
    st.divider()
    
    # Cloud sync status indicator
    if st.session_state.db_data.get("google_sheet_webhook"):
        st.caption("🟢 **Google Sheet Cloud Sync: Active**")
    else:
        st.caption("🟡 **डेटाबेस मोड: Local Permanent File**")

# -------------------------------------------------------------
# 1. HOME PAGE
# -------------------------------------------------------------
if selected_page == "🏠 मुख्य पान (Home)":
    st.markdown("""
    <div class="hero-box">
        <div class="hero-title">विद्यार्थ्यांचे स्मार्ट लर्निंग पोर्टल 🚀</div>
        <div class="hero-subtitle">शालेय शिक्षणासोबतच शिका भविष्यातील <b>Artificial Intelligence (AI)</b> तंत्रज्ञान सोप्या भाषेत!</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>📖 सुरक्षित अभ्यासक्रम</h4>
            <p>विद्यार्थी वर्ग कोडसह सुरक्षित लॉगिन करून रासायनिक अभिक्रिया व नोट्सचा अभ्यास करू शकतात.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🤖 AI चे प्रात्यक्षिक</h4>
            <p>Prompt Engineering, Machine Learning व AI टूल्स कसे वापरावे याचे थेट प्रॅक्टिकल मार्गदर्शन.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>📊 गुगल शीट क्लाउड सिंक</h4>
            <p>सर्व विद्यार्थ्यांचा डेटा आणि निकाल Google Sheets व शिक्षक डॅशबोर्डवर कायम सुरक्षित राहतो.</p>
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. SUBJECTS PAGE (STUDENT LOGIN GATE)
# -------------------------------------------------------------
elif selected_page == "📚 शालेय अभ्यासक्रम (Subjects) 🔒":
    if st.session_state.logged_student is None:
        st.markdown("""
        <div class="login-box">
            <h3 style="text-align: center; color: #1E3A8A; margin-bottom: 0.5rem;">🔐 विद्यार्थी प्रवेश (Student Login)</h3>
            <p style="text-align: center; color: #64748B; font-size: 0.95rem;">शालेय अभ्यासक्रम पाहण्यासाठी तुमची माहिती आणि शिक्षकांनी दिलेला वर्ग कोड टाका.</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")

        col_l1, col_center, col_l2 = st.columns([1, 2, 1])
        with col_center:
            with st.container(border=True):
                s_name = st.text_input("विद्यार्थ्याचे पूर्ण नाव (Full Name):", placeholder="उदा. राहुल सचिन पाटील")
                s_class = st.selectbox("इयत्ता (Class):", ["८ वी (8th)", "९ वी (9th)", "१० वी (10th)"])
                s_roll = st.text_input("हजेरी क्रमांक / रोल नंबर (Roll No):", placeholder="उदा. 15")
                s_email = st.text_input("ईमेल आयडी (Email ID):", placeholder="उदा. rahul@example.com")
                
                current_code = st.session_state.db_data.get("class_access_code", "GURUKUL10")
                entered_code = st.text_input("🔑 वर्ग प्रवेश कोड (Class Code):", placeholder="शिक्षकांनी दिलेला कोड टाका")

                if st.button("🚀 वर्गात प्रवेश करा", type="primary", use_container_width=True):
                    if not s_name.strip() or not s_roll.strip():
                        st.error("❌ कृपया नाव आणि हजेरी क्रमांक भरा.")
                    elif not is_valid_email(s_email):
                        st.error("❌ कृपया वैध ईमेल आयडी (उदा. name@gmail.com) टाका.")
                    elif entered_code.strip() != current_code:
                        st.error("❌ चुकीचा वर्ग कोड! शिक्षकांनी दिलेला योग्य कोड प्रविष्ट करा.")
                    else:
                        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                        student_info = {
                            "नाव": s_name.strip(),
                            "ईमेल": s_email.strip(),
                            "इयत्ता": s_class,
                            "रोल नं": s_roll.strip(),
                            "लॉगिन वेळ": now_str
                        }
                        st.session_state.logged_student = student_info
                        
                        # स्थानिक डेटाबेसमध्ये कायमस्वरूपी सेव्ह
                        st.session_state.db_data["student_logins"].append(student_info)
                        persist_all()
                        
                        # Google Sheets वर ऑटो-सिंक
                        send_to_google_sheet({
                            "type": "attendance",
                            "data": student_info
                        })
                        
                        st.success("🎉 स्वागत आहे! अभ्यासक्रम उघडत आहे...")
                        st.rerun()

    else:
        # Student logged in
        st.markdown(f"""
        <div class="user-welcome-chip">
            👋 स्वागत आहे, <b>{st.session_state.logged_student['नाव']}</b> | इयत्ता: <b>{st.session_state.logged_student['इयत्ता']}</b> | रोल नं: <b>{st.session_state.logged_student['रोल नं']}</b>
        </div>
        """, unsafe_allow_html=True)

        st.header("📚 शालेय अभ्यासक्रम व शैक्षणिक साहित्य")
        subject = st.selectbox("विषय निवडा:", ["विज्ञान आणि तंत्रज्ञान (Science)", "माहिती तंत्रज्ञान (IT/Coding)"])
        
        if subject == "विज्ञान आणि तंत्रज्ञान (Science)":
            tab1, tab2 = st.tabs(["🔬 धडा ३: रासायनिक अभिक्रिया आणि समीकरणे", "🪐 धडा १: गुरुत्वाकर्षण (Gravitation)"])
            
            with tab1:
                st.subheader("🧪 धडा ३: रासायनिक अभिक्रिया आणि समीकरणे")
                st.markdown("""
                रासायनिक अभिक्रियांचे प्रामुख्याने **४ मुख्य प्रकार** असतात:
                1. **➕ संयोग (Combination):** दोन किंवा अधिक अभिक्रियाकारकांपासून एकच उत्पादित तयार होते.
                2. **💥 अपघटन (Decomposition):** एकाच अभिक्रियाकारकाचे विघटन होऊन दोन किंवा अधिक उत्पादिते मिळतात.
                3. **🔄 विस्थापन (Displacement):** अधिक क्रियाशील मूलद्रव्य कमी क्रियाशील मूलद्रव्याला विस्थापित करते.
                4. **🔀 दुहेरी विस्थापन (Double Displacement):** आयनांची अदलाबदल होऊन अवक्षेप तयार होतो.
                """)
                st.divider()

                st.markdown("### 📝 रासायनिक अभिक्रियांचे प्रकार ओळखण्याचा सराव (१ ते २०)")
                st.info("💡 **विद्यार्थ्यांसाठी सूचना:** खालील सर्व २० अभिक्रियांचे काळजीपूर्वक निरीक्षण करा आणि योग्य पर्याय निवडून शेवटी **'माझी सर्व उत्तरे शिक्षकांकडे जमा करा'** बटण दाबा.")

                with st.form("reactions_practice_form"):
                    student_answers = {}
                    for r in REACTIONS_DATA:
                        st.markdown(f"""
                        <div class="reaction-card">
                            <h4 style="color: #1e3a8a; margin-bottom: 0.5rem;">अभिक्रिया क्रमांक {r['id']}:</h4>
                        </div>
                        """, unsafe_allow_html=True)
                        st.latex(r["reaction"])
                        
                        student_answers[r["id"]] = st.radio(
                            f"अभिक्रिया क्र. {r['id']} चा प्रकार ओळखा:",
                            REACTION_OPTIONS,
                            key=f"rxn_q_{r['id']}",
                            index=None
                        )
                        st.markdown("---")

                    submit_reactions = st.form_submit_button("📤 माझी सर्व उत्तरे शिक्षकांकडे जमा करा (Submit Test)", use_container_width=True, type="primary")

                if submit_reactions:
                    score = 0
                    detailed_breakdown = []
                    
                    for r in REACTIONS_DATA:
                        chosen = student_answers.get(r["id"])
                        is_correct = (chosen == r["correct"])
                        if is_correct:
                            score += 1
                        
                        detailed_breakdown.append({
                            "अभिक्रिया क्र": f"अभिक्रिया {r['id']}",
                            "रासायनिक समीकरण": r["reaction"],
                            "विद्यार्थ्याचे उत्तर": chosen if chosen else "उत्तर दिले नाही",
                            "योग्य उत्तर": r["correct"],
                            "निकाल": "बरोबर ✅" if is_correct else "चूक ❌"
                        })

                    now_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                    submission_record = {
                        "विद्यार्थी": st.session_state.logged_student["नाव"],
                        "इयत्ता": st.session_state.logged_student["इयत्ता"],
                        "रोल नं": st.session_state.logged_student["रोल नं"],
                        "ईमेल": st.session_state.logged_student["ईमेल"],
                        "तारीख व वेळ": now_time,
                        "गुण": f"{score} / {len(REACTIONS_DATA)}",
                        "तपशील": detailed_breakdown
                    }
                    
                    # स्थानिक डेटाबेसमध्ये सेव्ह
                    st.session_state.db_data["reaction_submissions"].append(submission_record)
                    persist_all()

                    # Google Sheet वर थेट निकाल ऑटो-सिंक
                    send_to_google_sheet({
                        "type": "quiz_result",
                        "data": {
                            "विद्यार्थी": submission_record["विद्यार्थी"],
                            "इयत्ता": submission_record["इयत्ता"],
                            "रोल नं": submission_record["रोल नं"],
                            "ईमेल": submission_record["ईमेल"],
                            "तारीख व वेळ": submission_record["तारीख व वेळ"],
                            "प्राप्त गुण": submission_record["गुण"]
                        }
                    })

                    st.balloons()
                    st.success(f"🎉 **अभिनंदन, {st.session_state.logged_student['नाव']}!** तुमची उत्तरे शिक्षकांकडे यशस्वीरीत्या सबमिट झाली आहेत.")
                    st.info("📌 तुमचे गुण आणि सविस्तर मूल्यमापन ऋषिकेश चव्हाण सरांच्या Google Sheet व डॅशबोर्डवर कायमस्वरूपी नोंदवले गेले आहे.")

            with tab2:
                st.subheader("🪐 धडा १: गुरुत्वाकर्षण (Gravitation) - महत्त्वाचे मुद्दे")
                st.markdown("""
                - **न्यूटनचा वैश्विक गुरुत्वाकर्षणाचा सिद्धांत:** $F = G \\frac{m_1 m_2}{r^2}$
                - **गुरुत्वीय त्वरण ($g$):** पृथ्वीच्या पृष्ठभागावर सरासरी $9.8 \\text{ m/s}^2$ असते.
                """)

        elif subject == "माहिती तंत्रज्ञान (IT/Coding)":
            st.subheader("💻 पायथन कोडिंगच्या मूलभूत संकल्पना")
            st.code('print("नमस्कार, ऋषिकेश चव्हाण सरांच्या AI क्लासमध्ये आपले स्वागत आहे!")', language="python")

# -------------------------------------------------------------
# 3. AI LAB
# -------------------------------------------------------------
elif selected_page == "🤖 AI लॅब & टूल्स (AI Lab)":
    st.header("🤖 AI लॅब - प्रत्यक्ष शिका AI टूल्स")
    role = st.selectbox("भूमिका निवडा (Role):", ["एक विज्ञान शिक्षक", "एक रोबोटिक्स तज्ज्ञ"])
    topic = st.text_input("विषय (Topic):", "रासायनिक संयुगे")
    st.markdown("##### 🚀 तयार झालेला स्मार्ट प्रॉमप्ट:")
    st.code(f"तुम्ही '{role}' आहात. शालेय विद्यार्थ्यांना '{topic}' सोप्या भाषेत ३ मुद्द्यांत समजावून सांगा.", language="text")

# -------------------------------------------------------------
# 4. QUIZ ZONE
# -------------------------------------------------------------
elif selected_page == "📝 सराव चाचणी (Quiz Zone)":
    st.header("📝 सराव प्रश्नमंजुषा (Interactive Quiz)")
    selected_topic = st.selectbox("🎯 क्विझचा विषय निवडा:", list(QUIZ_DATABASE.keys()))
    questions = QUIZ_DATABASE[selected_topic]
    user_answers = {}

    with st.form("quiz_form"):
        for i, q in enumerate(questions, start=1):
            st.markdown(f"#### **प्रश्न {i}:** {q['question']}")
            user_answers[i] = st.radio("पर्याय:", q["options"], key=f"q_{i}", index=None)
        submit_btn = st.form_submit_button("🏁 उत्तरे जमा करा")

    if submit_btn:
        score = 0
        for i, q in enumerate(questions, start=1):
            if user_answers.get(i) == q["answer"]:
                score += 1
                st.success(f"✅ प्रश्न {i}: बरोबर!")
            else:
                st.error(f"❌ प्रश्न {i}: चूक! योग्य उत्तर: {q['answer']}")
        st.info(f"तुमचे एकूण गुण: {score} / {len(questions)}")

# -------------------------------------------------------------
# 5. DOUBT BOX
# -------------------------------------------------------------
elif selected_page == "📬 शंका विचारा (Doubt Box)":
    st.header("📬 शिक्षकांना शंका विचारा (Ask Your Teacher)")
    default_name = st.session_state.logged_student["नाव"] if st.session_state.logged_student else ""
    
    with st.form("doubt_box_form"):
        s_name = st.text_input("विद्यार्थ्याचे नाव:", value=default_name)
        s_class = st.selectbox("इयत्ता:", ["८ वी (8th)", "९ वी (9th)", "१० वी (10th)", "इतर"])
        s_question = st.text_area("तुमची शंका किंवा प्रश्न:")
        send = st.form_submit_button("शंका पाठवा (Submit)")
        
        if send:
            if s_name.strip() and s_question.strip():
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                doubt_item = {
                    "विद्यार्थी": s_name.strip(),
                    "इयत्ता": s_class,
                    "शंका": s_question.strip(),
                    "वेळ": now_str
                }
                st.session_state.db_data["doubt_records"].append(doubt_item)
                persist_all()
                
                # Google Sheets सिंक
                send_to_google_sheet({
                    "type": "doubt",
                    "data": doubt_item
                })
                
                st.success("धन्यवाद! तुमची शंका नोंदवली गेली असून ऋषिकेश चव्हाण सरांच्या डॅशबोर्ड व Google Sheet वर दिसेल.")
            else:
                st.error("कृपया सर्व माहिती भरा.")

# -------------------------------------------------------------
# 6. TEACHER & ADMIN DASHBOARD
# -------------------------------------------------------------
elif selected_page == "📊 शिक्षक डॅशबोर्ड (Teacher Admin) 🔐":
    st.header("📊 शिक्षक नियंत्रण कक्ष (Teacher Admin Dashboard)")
    st.write("विद्यार्थ्यांची उपस्थिती, लॉगिन रेकॉर्ड, रासायनिक अभिक्रियांचे निकाल व कायमस्वरूपी Google Sheets डेटा.")

    teacher_password = st.text_input("🔑 शिक्षकांचा गुप्त पासवर्ड टाका (Teacher PIN):", type="password")
    
    if teacher_password == "gurukul123":
        st.success("प्रवेश मंजूर झाला! स्वागत आहे ऋषिकेश चव्हाण सर 👨‍🏫")
        
        logins = st.session_state.db_data.get("student_logins", [])
        submissions = st.session_state.db_data.get("reaction_submissions", [])
        doubts = st.session_state.db_data.get("doubt_records", [])

        st.divider()

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-num">{len(logins)}</div>
                <div class="kpi-title">एकूण हजेरी रेकॉर्ड्स</div>
            </div>
            """, unsafe_allow_html=True)
        with kpi2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-num">{len(submissions)}</div>
                <div class="kpi-title">जमा झालेल्या चाचण्या</div>
            </div>
            """, unsafe_allow_html=True)
        with kpi3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-num">{len(doubts)}</div>
                <div class="kpi-title">विद्यार्थ्यांच्या शंका</div>
            </div>
            """, unsafe_allow_html=True)
        with kpi4:
            has_sheet = "सक्रिय 🟢" if st.session_state.db_data.get("google_sheet_webhook") else "बंद ⚪"
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-num" style="font-size: 1.5rem; padding-top: 0.4rem;">{has_sheet}</div>
                <div class="kpi-title">Google Sheets क्लाउड</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        tab_dash1, tab_dash2, tab_dash3, tab_dash4, tab_dash5 = st.tabs([
            "📋 विद्यार्थी हजेरी (Attendance)", 
            "🧪 रासायनिक अभिक्रिया निकाल (Results)",
            "📊 Google Sheets जोडणी (Cloud Setup)",
            "⚙️ वर्ग कोड व शंका (Settings & Doubts)",
            "💾 डेटा बॅकअप (Master Backup)"
        ])

        with tab_dash1:
            st.subheader("विद्यार्थी हजेरी आणि लॉगिन तपशील (पहिल्या दिवसापासूनचा संपूर्ण डेटा)")
            if logins:
                df_logins = pd.DataFrame(logins)
                st.dataframe(df_logins, use_container_width=True)
                csv_data = df_logins.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 संपूर्ण हजेरी रिपोर्ट डाउनलोड करा (Download CSV)",
                    data=csv_data,
                    file_name=f"student_attendance_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("अद्याप कोणत्याही विद्यार्थ्याने लॉगिन केलेले नाही.")

        with tab_dash2:
            st.subheader("🧪 रासायनिक अभिक्रिया सराव चाचणीचे मूल्यमापन (Student Submissions)")
            if submissions:
                summary_data = []
                for sub in submissions:
                    summary_data.append({
                        "विद्यार्थी": sub["विद्यार्थी"],
                        "इयत्ता": sub["इयत्ता"],
                        "रोल नं": sub["रोल नं"],
                        "ईमेल": sub["ईमेल"],
                        "तारीख व वेळ": sub["तारीख व वेळ"],
                        "प्राप्त गुण (Score)": sub["गुण"]
                    })
                df_results = pd.DataFrame(summary_data)
                st.dataframe(df_results, use_container_width=True)

                st.divider()
                st.markdown("#### 🔍 वैयक्तिक विद्यार्थ्याची सविस्तर उत्तरपत्रिका तपासणे:")
                student_names = [f"{s['विद्यार्थी']} (रोल नं: {s['रोल नं']}) - {s['तारीख व वेळ']}" for s in submissions]
                chosen_idx = st.selectbox("विद्यार्थी निवडा:", range(len(student_names)), format_func=lambda i: student_names[i])
                
                selected_sub = submissions[chosen_idx]
                st.info(f"👤 **विद्यार्थी:** {selected_sub['विद्यार्थी']} | **एकूण गुण:** {selected_sub['गुण']}")
                
                df_details = pd.DataFrame(selected_sub["तपशील"])
                st.dataframe(df_details[["अभिक्रिया क्र", "विद्यार्थ्याचे उत्तर", "योग्य उत्तर", "निकाल"]], use_container_width=True)

                csv_sub = df_results.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 रासायनिक अभिक्रिया निकाल डाऊनलोड करा (Download CSV)",
                    data=csv_sub,
                    file_name=f"reaction_results_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("अद्याप कोणत्याही विद्यार्थ्याने रासायनिक अभिक्रिया चाचणी सबमिट केलेली नाही.")

        with tab_dash3:
            st.subheader("📊 थेट Google Sheets सह ऑटोमॅटिक सिंक (Cloud Integration)")
            st.markdown("""
            विद्यार्थ्याने सबमिट करताच त्याचा डेटा **थेट तुमच्या Google Drive मधील Excel Sheet मध्ये** जमा होण्यासाठी खालील रकान्यात तुमच्या Google Apps Script Web App ची URL पेस्ट करा:
            """)
            
            cur_webhook = st.session_state.db_data.get("google_sheet_webhook", "")
            new_webhook = st.text_input("🔗 Google Sheets Webhook URL:", value=cur_webhook, placeholder="https://script.google.com/macros/s/.../exec")
            
            col_save, col_test = st.columns([1, 1])
            with col_save:
                if st.button("💾 Google Sheet URL जतन करा", use_container_width=True):
                    st.session_state.db_data["google_sheet_webhook"] = new_webhook.strip()
                    persist_all()
                    st.success("✅ Google Sheets लिंक यशस्वीरित्या जोडली गेली आहे!")
                    st.rerun()
            with col_test:
                if st.button("🧪 टेस्ट डेटा पाठवून तपासा", use_container_width=True):
                    if new_webhook.strip():
                        test_ok = send_to_google_sheet({
                            "type": "attendance",
                            "data": {
                                "नाव": "टेस्ट विद्यार्थी",
                                "ईमेल": "test@gmail.com",
                                "इयत्ता": "१० वी",
                                "रोल नं": "99",
                                "लॉगिन वेळ": datetime.now().strftime("%Y-%m-%d %H:%M")
                            }
                        })
                        if test_ok:
                            st.success("🎉 उत्कृष्ट! Google Sheet मध्ये टेस्ट एन्ट्री यशस्वीरीत्या झाली आहे!")
                        else:
                            st.warning("⚠️ डेटा पाठवला आहे, कृपया तुमच्या Google Sheet मध्ये तपासा.")
                    else:
                        st.error("कृपया आधी URL टाका.")

            st.info("💡 **टीप:** Google Sheet ची मोफत लिंक कशी तयार करायची यासाठी सोबत दिलेली **`google_sheets_guide.md`** फाईल पहा. अवघ्या २ मिनिटांत हे सुरू होते.")

        with tab_dash4:
            st.subheader("⚙️ विद्यार्थ्यांसाठी वर्ग प्रवेश कोड (Class Access Code)")
            cur_code = st.session_state.db_data.get("class_access_code", "GURUKUL10")
            new_code = st.text_input("चालू वर्ग कोड बदला:", value=cur_code)
            if st.button("💾 नवीन कोड सेव्ह करा", key="save_code_btn"):
                if new_code.strip():
                    st.session_state.db_data["class_access_code"] = new_code.strip()
                    persist_all()
                    st.success(f"✅ नवीन वर्ग कोड: `{new_code.strip()}`")
                    st.rerun()
                else:
                    st.error("कोड रिकामा ठेवू नका.")

            st.divider()
            st.subheader("📬 विद्यार्थ्यांच्या शंका")
            if doubts:
                df_doubts = pd.DataFrame(doubts)
                st.dataframe(df_doubts, use_container_width=True)
            else:
                st.info("कोणत्याही विद्यार्थ्याची शंका प्रलंबित नाही.")

        with tab_dash5:
            st.subheader("💾 संपूर्ण डेटाबेस बॅकअप (Permanent Master Backup)")
            st.write("स्थानिक डेटाबेसची मास्टर कॉपी डाउनलोड करा:")
            
            db_json_str = json.dumps(st.session_state.db_data, ensure_ascii=False, indent=4)
            st.download_button(
                label="📦 संपूर्ण डेटाबेस बॅकअप डाऊनलोड करा (JSON)",
                data=db_json_str.encode('utf-8'),
                file_name=f"gurukul_master_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json"
            )

    elif teacher_password != "":
        st.error("चुकीचा पासवर्ड! कृपया योग्य पासवर्ड टाका.")
    else:
        st.warning("⚠️ हा भाग केवळ शिक्षकांसाठी राखीव आहे. कृपया वरील बॉक्समध्ये पासवर्ड प्रविष्ट करा.")

st.divider()
st.markdown("<p style='text-align: center; color: gray;'>© 2026 AI गुरूकुल | ऋषिकेश चव्हाण (गणित, विज्ञान आणि AI)</p>", unsafe_allow_html=True)
