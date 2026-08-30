import streamlit as st
import pandas as pd
import time
from datetime import datetime

st.set_page_config(
    page_title="AI गुरूकुल | Teacher & AI Learning Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Main container and font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Hero Banner styling */
    .hero-box {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 50%, #06B6D4 100%);
        color: white;
        padding: 2.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.25);
    }
    
    .hero-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.15rem;
        opacity: 0.95;
    }

    /* Cards styling */
    .feature-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.08);
        border-color: #3b82f6;
    }

    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .badge-ai {
        background-color: #ede9fe;
        color: #6d28d9;
    }
    
    .badge-school {
        background-color: #dbeafe;
        color: #1d4ed8;
    }
    
    /* Quiz Score Box */
    .score-badge {
        background: linear-gradient(135deg, #10B981, #059669);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        font-size: 1.3rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.markdown("### 👨‍🏫 **शिक्षक प्रोफाईल**")
    st.markdown("""
    **नाव:**  ऋषिकेश रसिक महेश चव्हाण    
    **पद:** Secondary School Teacher & AI Educator    
    **विषय:** विज्ञान, गणित आणि Artificial Intelligence (AI)
    """)
    st.divider()
    
    selected_page = st.radio(
        "📌 **मेनू निवडा:**",
        [
            "🏠 मुख्य पान (Home)", 
            "📚 शालेय अभ्यासक्रम (Subjects)", 
            "🤖 AI लॅब & टूल्स (AI Lab)", 
            "📝 सराव चाचणी (Quiz Zone)",
            "📬 शंका विचारा (Doubt Box)"
        ]
    )
    
    st.divider()
    st.info("💡 *'भविष्यातील शिक्षण तंत्रज्ञानासोबत!'*")

if selected_page == "🏠 मुख्य पान (Home)":
    st.markdown("""
    <div class="hero-box">
        <div class="hero-title">विद्यार्थ्यांचे स्मार्ट लर्निंग पोर्टल 🚀</div>
        <div class="hero-subtitle">शालेय शिक्षणासोबतच शिका भविष्यातील <b>Artificial Intelligence (AI)</b> तंत्रज्ञान सोप्या मराठी आणि इंग्रजीतून!</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <span class="badge badge-school">शालेय शिक्षण</span>
            <h4>📖 संकल्पना स्पष्टीकरण</h4>
            <p>इयत्ता ८ वी ते १० वी साठी विज्ञान, गणित व संगणक विषयांच्या सोप्या भाषेत नोट्स व मार्गदर्शन.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="feature-card">
            <span class="badge badge-ai">नवीन युग</span>
            <h4>🤖 AI चे प्रात्यक्षिक</h4>
            <p>Prompt Engineering, Machine Learning व AI टूल्स कसे वापरावे याचे थेट प्रॅक्टिकल ज्ञान.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="feature-card">
            <span class="badge badge-school">मूल्यमापन</span>
            <h4>🎯 सराव आणि प्रश्नमंजुषा</h4>
            <p>स्वयं-मूल्यमापनासाठी इंटरॅक्टिव्ह क्विझ, कोडिंग कोडी आणि तत्काळ निकाल.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    st.subheader("📢 ताज्या घडामोडी व सूचना (Notice Board)")
    st.info("📌 **नवीन बॅच:** रविवारपासून ' लवकरच ")

elif selected_page == "📚 शालेय अभ्यासक्रम (Subjects)":
    st.header("📚 शालेय अभ्यासक्रम व साहित्य")
    st.write("येथून तुम्ही प्रकरणांनुसार नोट्स आणि व्हिडिओ मार्गदर्शन पाहू शकता.")
    
    subject = st.selectbox("विषय निवडा:", ["विज्ञान आणि तंत्रज्ञान (Science)", "गणित (Mathematics)", "माहिती तंत्रज्ञान (IT/Coding)"])
    
    if subject == "विज्ञान आणि तंत्रज्ञान (Science)":
        with st.expander("🔬 धडा १: गुरुत्वाकर्षण (Gravitation) - महत्त्वाचे मुद्दे", expanded=True):
            st.markdown("""
            - **न्यूटनचा वैश्विक गुरुत्वाकर्षणाचा सिद्धांत:** विश्वातील प्रत्येक वस्तू इतर वस्तूला एका विशिष्ट बलाने आकर्षित करते.
            - **सूत्र:** $F = G \\frac{m_1 m_2}{r^2}$
            - **अभ्यास प्रश्न:** गुरुत्वीय त्वरण ($g$) चे मूल्य पृथ्वीच्या पृष्ठभागावर किती असते? ($9.8 \\text{ m/s}^2$)
            """)
            st.button("📥 PDF नोट्स डाउनलोड करा (Sample)")
            
        with st.expander("⚡ धडा २: विद्युत धारा व चुंबकत्व"):
            st.write("या प्रकरणाच्या नोट्स लवकरच अपडेट केल्या जातील.")

    elif subject == "माहिती तंत्रज्ञान (IT/Coding)":
        st.subheader("💻 कोडिंगच्या मूलभूत गोष्टी (Python & Logic)")
        st.code("""
# विद्यार्थ्यांसाठी पहिला पायथन प्रोग्रॅम
student_name = "आर्यन"
marks = 95

print(f"अभिनंदन {student_name}! तुमचे गुण {marks}% आहेत.")
        """, language="python")

elif selected_page == "🤖 AI लॅब & टूल्स (AI Lab)":
    st.header("🤖 AI लॅब - प्रत्यक्ष शिकूया AI कसे काम करते!")
    st.write("विद्यार्थ्यांसाठी कृत्रिम बुद्धिमत्तेचे (AI) सोपे प्रात्यक्षिक मॉडेल्स.")
    
    ai_demo = st.radio("लॅब प्रयोग निवडा:", [
        "1. AI भावना ओळखक (Sentiment Analyzer)",
        "2. प्रॉमप्ट इंजिनिअरिंग ट्रेनर (Prompt Playground)",
        "3. मशीन लर्निंग अंदाज (Simple Prediction Demo)"
    ])
    
    if ai_demo == "1. AI भावना ओळखक (Sentiment Analyzer)":
        st.subheader("🔍 वाक्यातील भावना ओळखा (Text Sentiment)")
        user_text = st.text_input("कोणतेही इंग्रजी किंवा सोपे मराठी वाक्य टाका:", "I love studying Science and AI!")
        
        if st.button("भावना तपासा (Analyze)"):
            positive_words = ["love", "good", "great", "awesome", "आव आवडते", "छान", "उत्तम"]
            negative_words = ["hate", "bad", "difficult", "कठीण", "वाईट"]
            
            text_lower = user_text.lower()
            if any(w in text_lower for w in positive_words):
                st.success("😊 **सकारात्मक भावना (Positive Sentiment):** हे वाक्य आनंद किंवा आवड दर्शवते!")
            elif any(w in text_lower for w in negative_words):
                st.warning("😟 **नकारात्मक/चिंता भावना (Negative Sentiment):** या वाक्यात काही अडचण किंवा नाराजी वाटते.")
            else:
                st.info("😐 **तटस्थ (Neutral Sentiment):** हे एक सामान्य माहिती देणारे वाक्य आहे.")

    elif ai_demo == "2. प्रॉमप्ट इंजिनिअरिंग ट्रेनर (Prompt Playground)":
        st.subheader("✍️ AI ला चांगला प्रश्न (Prompt) कसा विचारावा?")
        st.markdown("""
        AI कडून अचूक उत्तर मिळवण्यासाठी **ROLE + TASK + CONTEXT** पद्धत वापरा:
        """)
        role = st.selectbox("भूमिका (Role):", ["एक विज्ञान शिक्षक", "एक इतिहासकार", "एक अंतराळवीर"])
        topic = st.text_input("विषय (Topic):", "सूर्यमालेतील ग्रह")
        
        st.markdown("##### 🚀 तयार झालेला स्मार्ट प्रॉमप्ट:")
        generated_prompt = f"तुम्ही '{role}' आहात. कृपया शालेय विद्यार्थ्यांना समजेल अशा सोप्या भाषेत '{topic}' या विषयावर ३ महत्त्वाचे मुद्दे समजावून सांगा."
        st.code(generated_prompt, language="text")

elif selected_page == "📝 सराव चाचणी (Quiz Zone)":
    st.header("📝 झटपट सराव क्विझ (AI & Science Quiz)")
    
    with st.form("quiz_form"):
        st.subheader("प्रश्न १: संगणकाला स्वतः शिकण्याची क्षमता देणाऱ्या तंत्रज्ञानाला काय म्हणतात?")
        q1 = st.radio("पर्याय निवडा:", ["Hardware", "Machine Learning / AI", "Operating System", "Photoshop"], key="q1")
        
        st.subheader("प्रश्न २: पाण्याचे रासायनिक सूत्र (Chemical Formula) काय आहे?")
        q2 = st.radio("पर्याय निवडा:", ["CO2", "NaCl", "H2O", "O2"], key="q2")
        
        submitted = st.form_submit_button("उत्तर जमा करा (Submit Quiz)")
        
        if submitted:
            score = 0
            if q1 == "Machine Learning / AI":
                score += 1
            if q2 == "H2O":
                score += 1
            st.session_state.quiz_score = score
            
    if st.session_state.quiz_score is not None:
        st.markdown(f"""
        <div class="score-badge">
            🎉 तुमचे गुण: {st.session_state.quiz_score} / २
        </div>
        """, unsafe_allow_html=True)
        if st.session_state.quiz_score == 2:
            st.balloons()
            st.success("उत्कृष्ट! तुमचे सर्व उत्तरे बरोबर आहेत.")

elif selected_page == "📬 शंका विचारा (Doubt Box)":
    st.header("📬 शिक्षकांना शंका विचारा (Ask Your Teacher)")
    st.write("अभ्यासात काही अडचण असल्यास खालील फॉर्म भरून प्रश्न पाठवा.")
    
    with st.form("doubt_form"):
        s_name = st.text_input("तुमचे नाव (Student Name):")
        s_class = st.selectbox("इयत्ता (Class):", ["८ वी (8th)", "९ वी (9th)", "१० वी (10th)", "इतर"])
        s_question = st.text_area("तुमचा प्रश्न किंवा शंका (Your Question):")
        
        send_btn = st.form_submit_button("प्रश्न पाठवा (Send)")
        if send_btn:
            if s_name and s_question:
                st.success(f"धन्यवाद {s_name}! तुमचा प्रश्न नोंदवला गेला आहे. शिक्षक लवकरच उत्तर देतील.")
            else:
                st.error("कृपया तुमचे नाव आणि प्रश्न पूर्ण भरा.")

st.divider()
st.markdown("<p style='text-align: center; color: gray;'>© 2026 AI Shikshak Portal | विद्यार्थ्यांच्या उज्ज्वल भविष्यासाठी समर्पित</p>", unsafe_allow_html=True)
