import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI गुरूकुल | Teacher & Student Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# 💾 डेटा स्टोरेज आणि सेशन स्टेट (SESSION STORAGE INITIALIZATION)
# -------------------------------------------------------------
if "logged_student" not in st.session_state:
    st.session_state.logged_student = None

if "current_rxn_idx" not in st.session_state:
    st.session_state.current_rxn_idx = 0

if "student_logins" not in st.session_state:
    st.session_state.student_logins = [
        {"नाव": "आर्यन पाटील", "इयत्ता": "१० वी (10th)", "रोल नं": "12", "ईमेल": "aryan.patil@example.com", "लॉगिन वेळ": "2026-09-02 10:15"},
        {"नाव": "सिया कुलकर्णी", "इयत्ता": "९ वी (9th)", "रोल नं": "24", "ईमेल": "siya.k@example.com", "लॉगिन वेळ": "2026-09-02 11:30"},
        {"नाव": "रोहन शिंदे", "इयत्ता": "१० वी (10th)", "रोल नं": "08", "ईमेल": "rohan.shinde@example.com", "लॉगिन वेळ": "2026-09-02 14:05"}
    ]

if "doubt_records" not in st.session_state:
    st.session_state.doubt_records = [
        {"विद्यार्थी": "आर्यन पाटील", "इयत्ता": "१० वी", "शंका": "विस्थापन आणि दुहेरी विस्थापन अभिक्रियेतील मुख्य फरक काय?", "वेळ": "2026-09-02 10:20"},
        {"विद्यार्थी": "सिया कुलकर्णी", "इयत्ता": "९ वी", "शंका": "गुरुत्वीय त्वरण चंद्रावर किती असते?", "वेळ": "2026-09-02 11:45"}
    ]

# -------------------------------------------------------------
# 🎨 डिझाईन आणि CSS स्टाईलिंग (CUSTOM CSS)
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
        font-size: 2.3rem;
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
        padding: 2rem;
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.12);
        max-width: 550px;
        margin: auto;
    }

    .user-welcome-chip {
        background-color: #ecfdf5;
        border: 1px solid #10b981;
        color: #065f46;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        display: inline-block;
        font-weight: 600;
        margin-bottom: 1rem;
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
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 🎯 प्रश्नांची यादी (QUIZ DATA)
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
            "explanation": "हे Large Language Models (LLM) असून नवीन माहिती व मजकूर तयार (Generate) करतात."
        }
    ],
    "🔬 सामान्य विज्ञान (Science)": [
        {
            "question": "पाण्याचे रासायनिक सूत्र (Chemical Formula) काय आहे?",
            "options": ["CO2", "NaCl", "H2O", "O2"],
            "answer": "H2O",
            "explanation": "हायड्रोजनचे दोन अणू आणि ऑक्सिजनचा एक अणू मिळून पाणी (H2O) तयार होते."
        },
        {
            "question": "पृथ्वीच्या पृष्ठभागावर गुरुत्वीय त्वरण ($g$) चे सरासरी मूल्य किती असते?",
            "options": ["$9.8 \\text{ m/s}^2$", "$8.9 \\text{ m/s}^2$", "$10.5 \\text{ m/s}^2$", "$0 \\text{ m/s}^2$"],
            "answer": "$9.8 \\text{ m/s}^2$",
            "explanation": "पृथ्वीच्या गुरुत्वाकर्षणामुळे वस्तूवर प्रयुक्त होणारे सरासरी त्वरण $9.8 \\text{ m/s}^2$ असते."
        }
    ]
}

# -------------------------------------------------------------
# 🧪 रासायनिक अभिक्रियांचा संपूर्ण सराव डेटा (२० अभिक्रिया)
# -------------------------------------------------------------
REACTIONS_DATA = [
    {"id": 1, "reaction": r"\text{Li}_2\text{O} + \text{H}_2\text{O} \longrightarrow 2\text{LiOH}", "type": "➕ संयोग अभिक्रिया (Combination)", "explanation": "लिथियम ऑक्साइड आणि पाणी एकत्र येऊन एकच उत्पादित तयार होते."},
    {"id": 2, "reaction": r"2\text{KClO}_3 \xrightarrow{\Delta} 2\text{KCl} + 3\text{O}_2\uparrow", "type": "💥 अपघटन अभिक्रिया (Decomposition)", "explanation": "उष्णतेने एकाच संयुगाचे विघटन होऊन दोन वेगळी उत्पादिते मिळतात."},
    {"id": 3, "reaction": r"\text{Mg} + 2\text{AgNO}_3 \longrightarrow \text{Mg(NO}_3)_2 + 2\text{Ag}", "type": "🔄 विस्थापन अभिक्रिया (Displacement)", "explanation": "मॅग्नेशियम हा सिल्व्हरपेक्षा जास्त क्रियाशील असल्याने सिल्व्हरला विस्थापित करतो."},
    {"id": 4, "reaction": r"\text{Pb(NO}_3)_2 + 2\text{KI} \longrightarrow \text{PbI}_2\downarrow + 2\text{KNO}_3", "type": "🔀 दुहेरी विस्थापन अभिक्रिया (Double Displacement)", "explanation": "आयनांची अदलाबदल होऊन लेड आयोडाइडचा पिवळा अवक्षेप तयार होतो."},
    {"id": 5, "reaction": r"2\text{NO} + \text{O}_2 \longrightarrow 2\text{NO}_2", "type": "➕ संयोग अभिक्रिया (Combination)", "explanation": "नायट्रिक ऑक्साइड आणि ऑक्सिजन एकत्र येऊन नायट्रोजन डायऑक्साइड बनते."},
    {"id": 6, "reaction": r"\text{NH}_4\text{NO}_3 \xrightarrow{\Delta} \text{N}_2\text{O} + 2\text{H}_2\text{O}", "type": "💥 अपघटन अभिक्रिया (Decomposition)", "explanation": "अमोनियम नायट्रेटला उष्णता दिल्यावर त्याचे विघटन होते."},
    {"id": 7, "reaction": r"\text{Ni} + 2\text{HCl} \longrightarrow \text{NiCl}_2 + \text{H}_2\uparrow", "type": "🔄 विस्थापन अभिक्रिया (Displacement)", "explanation": "निकेल हायड्रोजनपेक्षा जास्त क्रियाशील असल्याने हायड्रोजनचे विस्थापन करतो."},
    {"id": 8, "reaction": r"\text{Al}_2(\text{SO}_4)_3 + 6\text{NaOH} \longrightarrow 2\text{Al(OH)}_3\downarrow + 3\text{Na}_2\text{SO}_4", "type": "🔀 दुहेरी विस्थापन अभिक्रिया (Double Displacement)", "explanation": "आयनांच्या परस्पर देवाणघेवाणीमुळे अल्युमिनियम हायड्रॉक्साइडचा अवक्षेप तयार होतो."},
    {"id": 9, "reaction": r"\text{P}_4 + 6\text{Cl}_2 \longrightarrow 4\text{PCl}_3", "type": "➕ संयोग अभिक्रिया (Combination)", "explanation": "फॉस्फरस आणि क्लोरीन एकत्र येऊन फॉस्फरस ट्रायक्लोराइड हे एकच उत्पादित बनते."},
    {"id": 10, "reaction": r"2\text{Al(OH)}_3 \xrightarrow{\Delta} \text{Al}_2\text{O}_3 + 3\text{H}_2\text{O}", "type": "💥 अपघटन अभिक्रिया (Decomposition)", "explanation": "उष्णतेने अल्युमिनियम हायड्रॉक्साइडचे अपघटन होऊन अल्युमिना व पाण्याची वाफ मिळते."},
    {"id": 11, "reaction": r"\text{Cl}_2 + 2\text{NaBr} \longrightarrow 2\text{NaCl} + \text{Br}_2", "type": "🔄 विस्थापन अभिक्रिया (Displacement)", "explanation": "क्लोरीन ब्रोमाइड आयनाला विस्थापित करतो."},
    {"id": 12, "reaction": r"\text{CuSO}_4 + 2\text{KOH} \longrightarrow \text{Cu(OH)}_2\downarrow + \text{K}_2\text{SO}_4", "type": "🔀 दुहेरी विस्थापन अभिक्रिया (Double Displacement)", "explanation": "आयनांच्या अदलाबदलीने कॉपर हायड्रॉक्साइडचा निळा अवक्षेप मिळतो."},
    {"id": 13, "reaction": r"\text{SO}_3 + \text{H}_2\text{O} \longrightarrow \text{H}_2\text{SO}_4", "type": "➕ संयोग अभिक्रिया (Combination)", "explanation": "सल्फर ट्रायऑक्साइड आणि पाणी एकत्र येऊन सल्फ्यूरिक आम्ल तयार होते."},
    {"id": 14, "reaction": r"2\text{Ag}_2\text{O} \xrightarrow{\Delta} 4\text{Ag} + \text{O}_2\uparrow", "type": "💥 अपघटन अभिक्रिया (Decomposition)", "explanation": "उष्णतेमुळे सिल्व्हर ऑक्साइडचे अपघटन होते."},
    {"id": 15, "reaction": r"\text{Cr}_2\text{O}_3 + 2\text{Al} \longrightarrow \text{Al}_2\text{O}_3 + 2\text{Cr}", "type": "🔄 विस्थापन अभिक्रिया (Displacement)", "explanation": "अल्युमिनियम क्रोमियमला विस्थापित करतो."},
    {"id": 16, "reaction": r"\text{AgNO}_3 + \text{KBr} \longrightarrow \text{AgBr}\downarrow + \text{KNO}_3", "type": "🔀 दुहेरी विस्थापन अभिक्रिया (Double Displacement)", "explanation": "सिल्व्हर ब्रोमाइडचा फिकट पिवळा अवक्षेप तयार होतो."},
    {"id": 17, "reaction": r"\text{BaO} + \text{CO}_2 \longrightarrow \text{BaCO}_3", "type": "➕ संयोग अभिक्रिया (Combination)", "explanation": "बेरियम ऑक्साईड आणि कार्बन डायऑक्साईड एकत्र येऊन बेरियम कार्बोनेट बनते."},
    {"id": 18, "reaction": r"2\text{NaHCO}_3 \xrightarrow{\Delta} \text{Na}_2\text{CO}_3 + \text{H}_2\text{O} + \text{CO}_2\uparrow", "type": "💥 अपघटन अभिक्रिया (Decomposition)", "explanation": "खाण्याचा सोडा तापविल्यावर त्याचे अपघटन होते."},
    {"id": 19, "reaction": r"\text{Sn} + 2\text{AgNO}_3 \longrightarrow \text{Sn(NO}_3)_2 + 2\text{Ag}", "type": "🔄 विस्थापन अभिक्रिया (Displacement)", "explanation": "टिन (Sn) सिल्व्हरचे विस्थापन करतो."},
    {"id": 20, "reaction": r"\text{FeCl}_3 + 3\text{NH}_4\text{OH} \longrightarrow \text{Fe(OH)}_3\downarrow + 3\text{NH}_4\text{Cl}", "type": "🔀 दुहेरी विस्थापन अभिक्रिया (Double Displacement)", "explanation": "फेरिक हायड्रॉक्साइडचा लालसर-तपकिरी अवक्षेप तयार होतो."}
]

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

    # Logged In status indicator
    if st.session_state.logged_student:
        st.success(f"👤 **लॉगिन:** {st.session_state.logged_student['नाव']} ({st.session_state.logged_student['इयत्ता']})")
        if st.button("🚪 लॉगआउट (Logout)", key="logout_btn"):
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
    st.info("💡 *'शिक्षणासोबतच शिका भविष्यातील तंत्रज्ञान!'*")

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
            <p>विद्यार्थी हजेरीसह लॉग-इन करून विज्ञान व गणिताच्या विशेष नोट्स आणि अभिक्रियांचा सराव करू शकतात.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🤖 AI चे प्रात्यक्षिक</h4>
            <p>Prompt Engineering, Machine Learning व AI टूल्स कसे वापरावे याचे थेट प्रॅक्टिकल ज्ञान.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>📊 शिक्षक डॅशबोर्ड</h4>
            <p>कोणता विद्यार्थी कधी आला, त्याने कोणत्या शंका विचारल्या हे सर्व शिक्षकांना एकाच डॅशबोर्डवर उपलब्ध.</p>
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. SUBJECTS PAGE (WITH STUDENT LOGIN GATE)
# -------------------------------------------------------------
elif selected_page == "📚 शालेय अभ्यासक्रम (Subjects) 🔒":
    # Check if student is logged in
    if st.session_state.logged_student is None:
        st.markdown("""
        <div class="login-box">
            <h3 style="text-align: center; color: #1E3A8A;">🔐 विद्यार्थी प्रवेश (Student Login)</h3>
            <p style="text-align: center; color: #64748B;">शालेय अभ्यासक्रम व रासायनिक अभिक्रियांचा सराव पाहण्यासाठी कृपया तुमची माहिती भरा.</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")

        col_a, col_b, col_c = st.columns([1, 2, 1])
        with col_b:
            with st.form("student_login_form"):
                s_name = st.text_input("विद्यार्थ्याचे पूर्ण नाव (Full Name):", placeholder="उदा. राहुल शर्मा")
                s_email = st.text_input("ईमेल आयडी (Email ID):", placeholder="उदा. student@example.com")
                s_class = st.selectbox("इयत्ता (Class):", ["८ वी (8th)", "९ वी (9th)", "१० वी (10th)"])
                s_roll = st.text_input("हजेरी क्रमांक / रोल नंबर (Roll No):", placeholder="उदा. 15")
                
                login_submit = st.form_submit_button("🚀 अभ्यासक्रमात प्रवेश करा (Enter Classroom)", use_container_width=True)
                
                if login_submit:
                    if s_name.strip() and s_roll.strip() and s_email.strip():
                        # Save student state
                        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                        student_data = {
                            "नाव": s_name.strip(),
                            "ईमेल": s_email.strip(),
                            "इयत्ता": s_class,
                            "रोल नं": s_roll.strip(),
                            "लॉगिन वेळ": now_str
                        }
                        st.session_state.logged_student = student_data
                        st.session_state.student_logins.append(student_data)
                        st.success("लॉगिन यशस्वी झाले! अभ्यासक्रम उघडत आहे...")
                        st.rerun()
                    else:
                        st.error("कृपया तुमचे नाव, ईमेल आयडी आणि हजेरी क्रमांक भरा.")
    else:
        # Student is logged in: Show subjects content
        st.markdown(f"""
        <div class="user-welcome-chip">
            👋 स्वागत आहे, <b>{st.session_state.logged_student['नाव']}</b> (इयत्ता: {st.session_state.logged_student['इयत्ता']} | रोल नं: {st.session_state.logged_student['रोल नं']})
        </div>
        """, unsafe_allow_html=True)

        st.header("📚 शालेय अभ्यासक्रम व शैक्षणिक साहित्य")
        subject = st.selectbox("विषय निवडा:", ["विज्ञान आणि तंत्रज्ञान (Science)", "माहिती तंत्रज्ञान (IT/Coding)"])
        
        if subject == "विज्ञान आणि तंत्रज्ञान (Science)":
            tab1, tab2 = st.tabs(["🔬 धडा ३: रासायनिक अभिक्रिया आणि समीकरणे", "🪐 धडा १: गुरुत्वाकर्षण (Gravitation)"])
            
            with tab1:
                st.subheader("🧪 धडा ३: रासायनिक अभिक्रिया आणि समीकरणे (Chemical Reactions & Equations)")
                st.markdown("""
                रासायनिक अभिक्रियांचे प्रामुख्याने **४ मुख्य प्रकार** असतात:
                1. **➕ संयोग (Combination):** दोन किंवा अधिक अभिक्रियाकारकांपासून एकच उत्पादित तयार होते.
                2. **💥 अपघटन (Decomposition):** एकाच अभिक्रियाकारकाचे विघटन होऊन दोन किंवा अधिक उत्पादिते मिळतात.
                3. **🔄 विस्थापन (Displacement):** अधिक क्रियाशील मूलद्रव्य कमी क्रियाशील मूलद्रव्याला विस्थापित करते.
                4. **🔀 दुहेरी विस्थापन (Double Displacement):** आयनांची अदलाबदल होऊन अवक्षेप तयार होतो.
                """)
                st.divider()
                st.markdown("### 📝 रासायनिक अभिक्रियांचे प्रकार ओळखण्याचा सराव (प्रश्नपत्रिका)")
                st.info("💡 **विद्यार्थ्यांसाठी सूचना:** खाली दिलेल्या २० रासायनिक अभिक्रियांचे काळजीपूर्वक निरीक्षण करा आणि अभिक्रिया कोणत्या प्रकारात मोडते (संयोग, अपघटन, विस्थापन की दुहेरी विस्थापन) ते आपल्या वहीत नोंदवा.")
                
                # Render clean list of 20 reactions without revealing answers
                col_rxn1, col_rxn2 = st.columns(2)
                half = len(REACTIONS_DATA) // 2
                
                with col_rxn1:
                    for r in REACTIONS_DATA[:half]:
                        with st.container(border=True):
                            st.markdown(f"**प्रश्न {r['id']}.** खालील रासायनिक अभिक्रियेचा प्रकार ओळखा:")
                            st.latex(r["reaction"])
                            st.caption("प्रकार: ______________________________")

                with col_rxn2:
                    for r in REACTIONS_DATA[half:]:
                        with st.container(border=True):
                            st.markdown(f"**प्रश्न {r['id']}.** खालील रासायनिक अभिक्रियेचा प्रकार ओळखा:")
                            st.latex(r["reaction"])
                            st.caption("प्रकार: ______________________________")

            with tab2:
                st.subheader("🪐 धडा १: गुरुत्वाकर्षण (Gravitation) - महत्त्वाचे मुद्दे")
                st.markdown("""
                - **न्यूटनचा वैश्विक गुरुत्वाकर्षणाचा सिद्धांत:** $F = G \\frac{m_1 m_2}{r^2}$
                - **गुरुत्वीय त्वरण ($g$):** पृथ्वीच्या पृष्ठभागावर सरासरी $9.8 \\text{ m/s}^2$ असते.
                """)

        elif subject == "माहिती तंत्रज्ञान (IT/Coding)":
            st.subheader("💻 पायथन कोडिंगच्या मूलभूत संकल्पना")
            st.code('print("नमस्कार, AI गुरूकुल मध्ये आपले स्वागत आहे!")', language="python")

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
    
    # Auto-fill name if logged in
    default_name = st.session_state.logged_student["नाव"] if st.session_state.logged_student else ""
    
    with st.form("doubt_box_form"):
        s_name = st.text_input("विद्यार्थ्याचे नाव:", value=default_name)
        s_class = st.selectbox("इयत्ता:", ["८ वी (8th)", "९ वी (9th)", "१० वी (10th)", "इतर"])
        s_question = st.text_area("तुमची शंका किंवा प्रश्न:")
        send = st.form_submit_button("शंका पाठवा (Submit)")
        
        if send:
            if s_name and s_question:
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.session_state.doubt_records.append({
                    "विद्यार्थी": s_name,
                    "इयत्ता": s_class,
                    "शंका": s_question,
                    "वेळ": now_str
                })
                st.success("धन्यवाद! तुमची शंका नोंदवली गेली असून शिक्षक डॅशबोर्डवर शिक्षकांना दिसेल.")
            else:
                st.error("कृपया सर्व माहिती भरा.")

# -------------------------------------------------------------
# 6. TEACHER & ADMIN DASHBOARD (SECURE ACCESS)
# -------------------------------------------------------------
elif selected_page == "📊 शिक्षक डॅशबोर्ड (Teacher Admin) 🔐":
    st.header("📊 शिक्षक नियंत्रण कक्ष (Teacher Admin Dashboard)")
    st.write("विद्यार्थ्यांची उपस्थिती, लॉगिन रेकॉर्ड आणि विचारलेल्या शंकांचे विश्लेषण.")

    # Password Protection for Teacher (Default password hint removed)
    teacher_password = st.text_input("🔑 शिक्षकांचा गुप्त पासवर्ड टाका (Teacher PIN):", type="password")
    
    if teacher_password == "gurukul123":
        st.success("प्रवेश मंजूर झाला! स्वागत आहे ऋषिकेश चव्हाण सर 👨‍🏫")
        st.divider()

        # Key Metrics Row
        kpi1, kpi2, kpi3 = st.columns(3)
        with kpi1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-num">{len(st.session_state.student_logins)}</div>
                <div class="kpi-title">एकूण नोंदणीकृत / लॉगिन विद्यार्थी</div>
            </div>
            """, unsafe_allow_html=True)
        with kpi2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-num">{len(st.session_state.doubt_records)}</div>
                <div class="kpi-title">विद्यार्थ्यांनी विचारलेल्या शंका</div>
            </div>
            """, unsafe_allow_html=True)
        with kpi3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-num">{len(REACTIONS_DATA)}</div>
                <div class="kpi-title">सक्रिय रासायनिक अभिक्रिया सराव</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.write("")

        tab_dash1, tab_dash2 = st.tabs(["📋 विद्यार्थी हजेरी व लॉगिन यादी (Login Logs)", "📬 आलेल्या शंका (Student Doubts)"])

        with tab_dash1:
            st.subheader("विद्यार्थी हजेरी आणि लॉगिन तपशील")
            if st.session_state.student_logins:
                df_logins = pd.DataFrame(st.session_state.student_logins)
                st.dataframe(df_logins, use_container_width=True)
                
                # Download CSV report
                csv_data = df_logins.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 हजेरी रिपोर्ट डाउनलोड करा (Download CSV)",
                    data=csv_data,
                    file_name=f"student_attendance_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("अद्याप कोणत्याही विद्यार्थ्याने लॉगिन केलेले नाही.")

        with tab_dash2:
            st.subheader("विद्यार्थ्यांनी विचारलेल्या शंकांचे व्यवस्थापन")
            if st.session_state.doubt_records:
                df_doubts = pd.DataFrame(st.session_state.doubt_records)
                st.dataframe(df_doubts, use_container_width=True)
            else:
                st.info("अद्याप कोणत्याही विद्यार्थ्याची शंका आलेली नाही.")

    elif teacher_password != "":
        st.error("चुकीचा पासवर्ड! कृपया योग्य पासवर्ड टाका.")
    else:
        st.warning("⚠️ हा भाग केवळ शिक्षकांसाठी राखीव आहे. कृपया वरील बॉक्समध्ये पासवर्ड प्रविष्ट करा.")

st.divider()
st.markdown("<p style='text-align: center; color: gray;'>© 2026 AI गुरूकुल | ऋषिकेश चव्हाण</p>", unsafe_allow_html=True)
