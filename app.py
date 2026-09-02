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

# Custom CSS for Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
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
    
    .score-badge {
        background: linear-gradient(135deg, #10B981, #059669);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        font-size: 1.4rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .reaction-card {
        background-color: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        margin-bottom: 0.75rem;
        border-radius: 0 8px 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 🎯 प्रश्नांची यादी (QUESTION BANK FOR QUIZ ZONE)
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
        },
        {
            "question": "AI ला योग्य उत्तर देण्यासाठी आपण दिलेल्या सूचनेला काय म्हणतात?",
            "options": ["Prompt (प्रॉमप्ट)", "Virus", "Algorithm Sheet", "Error"],
            "answer": "Prompt (प्रॉमप्ट)",
            "explanation": "AI कडून काम करून घेण्यासाठी दिलेल्या इनपुट सूचनेला 'Prompt' म्हणतात."
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
        },
        {
            "question": "दोन किंवा अधिक अभिक्रियाकारकांपासून एकच उत्पादित तयार होणाऱ्या अभिक्रियेला काय म्हणतात?",
            "options": ["संयोग अभिक्रिया", "अपघटन अभिक्रिया", "विस्थापन अभिक्रिया", "दुहेरी विस्थापन अभिक्रिया"],
            "answer": "संयोग अभिक्रिया",
            "explanation": "जेव्हा दोन किंवा अधिक अभिक्रियाकारके एकत्र येऊन एकच अंतिम उत्पादित तयार करतात, तेव्हा तिला संयोग (Combination) अभिक्रिया म्हणतात."
        }
    ]
}

# -------------------------------------------------------------
# 🧪 रासायनिक अभिक्रियांचा संपूर्ण सराव डेटा (२० अभिक्रिया)
# -------------------------------------------------------------
REACTIONS_DATA = [
    {
        "id": 1,
        "reaction": r"\text{Li}_2\text{O} + \text{H}_2\text{O} \longrightarrow 2\text{LiOH}",
        "type": "➕ संयोग अभिक्रिया (Combination)",
        "explanation": "लिथियम ऑक्साइड आणि पाणी ही दोन अभिक्रियाकारके एकत्र येऊन लिथियम हायड्रॉक्साइड हे एकच उत्पादित तयार होते."
    },
    {
        "id": 2,
        "reaction": r"2\text{KClO}_3 \xrightarrow{\Delta} 2\text{KCl} + 3\text{O}_2\uparrow",
        "type": "💥 अपघटन अभिक्रिया (Decomposition)",
        "explanation": "उष्णता दिल्याने पोटॅशियम क्लोरेट या एकाच संयुगाचे विघटन होऊन दोन वेगळी उत्पादिते मिळतात."
    },
    {
        "id": 3,
        "reaction": r"\text{Mg} + 2\text{AgNO}_3 \longrightarrow \text{Mg(NO}_3)_2 + 2\text{Ag}",
        "type": "🔄 विस्थापन अभिक्रिया (Displacement)",
        "explanation": "मॅग्नेशियम हा सिल्व्हरपेक्षा जास्त क्रियाशील असल्याने तो सिल्व्हर नायट्रेटमधून सिल्व्हरला विस्थापित करतो."
    },
    {
        "id": 4,
        "reaction": r"\text{Pb(NO}_3)_2 + 2\text{KI} \longrightarrow \text{PbI}_2\downarrow + 2\text{KNO}_3",
        "type": "🔀 दुहेरी विस्थापन अभिक्रिया (Double Displacement)",
        "explanation": "अभिक्रियाकारकांमधील आयनांची अदलाबदल होऊन लेड आयोडाइडचा पिवळा अवक्षेप (Precipitate) तयार होतो."
    },
    {
        "id": 5,
        "reaction": r"2\text{NO} + \text{O}_2 \longrightarrow 2\text{NO}_2",
        "type": "➕ संयोग अभिक्रिया (Combination)",
        "explanation": "नायट्रिक ऑक्साइड आणि ऑक्सिजन एकत्र येऊन नायट्रोजन डायऑक्साइड हे एकच उत्पादित बनते."
    },
    {
        "id": 6,
        "reaction": r"\text{NH}_4\text{NO}_3 \xrightarrow{\Delta} \text{N}_2\text{O} + 2\text{H}_2\text{O}",
        "type": "💥 अपघटन अभिक्रिया (Decomposition)",
        "explanation": "अमोनियम नायट्रेटला उष्णता दिल्यावर त्याचे विघटन होऊन डायनायट्रोजन ऑक्साइड आणि पाणी तयार होते."
    },
    {
        "id": 7,
        "reaction": r"\text{Ni} + 2\text{HCl} \longrightarrow \text{NiCl}_2 + \text{H}_2\uparrow",
        "type": "🔄 विस्थापन अभिक्रिया (Displacement)",
        "explanation": "निकेल हा हायड्रोजनपेक्षा जास्त क्रियाशील असल्याने तो आम्लातील हायड्रोजनला विस्थापित करतो."
    },
    {
        "id": 8,
        "reaction": r"\text{Al}_2(\text{SO}_4)_3 + 6\text{NaOH} \longrightarrow 2\text{Al(OH)}_3\downarrow + 3\text{Na}_2\text{SO}_4",
        "type": "🔀 दुहेरी विस्थापन अभिक्रिया (Double Displacement)",
        "explanation": "आयनांच्या परस्पर देवाणघेवाणीमुळे अल्युमिनियम हायड्रॉक्साइडचा अवक्षेप तयार होतो."
    },
    {
        "id": 9,
        "reaction": r"\text{P}_4 + 6\text{Cl}_2 \longrightarrow 4\text{PCl}_3",
        "type": "➕ संयोग अभिक्रिया (Combination)",
        "explanation": "फॉस्फरस आणि क्लोरीन हे दोन मूलद्रव्ये एकत्र येऊन फॉस्फरस ट्रायक्लोराइड हे एकच उत्पादित बनवतात."
    },
    {
        "id": 10,
        "reaction": r"2\text{Al(OH)}_3 \xrightarrow{\Delta} \text{Al}_2\text{O}_3 + 3\text{H}_2\text{O}",
        "type": "💥 अपघटन अभिक्रिया (Decomposition)",
        "explanation": "उष्णतेच्या प्रभावामुळे अल्युमिनियम हायड्रॉक्साइडचे अपघटन होऊन अल्युमिना व पाण्याची वाफ तयार होते."
    },
    {
        "id": 11,
        "reaction": r"\text{Cl}_2 + 2\text{NaBr} \longrightarrow 2\text{NaCl} + \text{Br}_2",
        "type": "🔄 विस्थापन अभिक्रिया (Displacement)",
        "explanation": "अधिक क्रियाशील क्लोरीन हॅलोजन हा ब्रोमाइड आयनाला विस्थापित करून मुक्त ब्रोमीन तयार करतो."
    },
    {
        "id": 12,
        "reaction": r"\text{CuSO}_4 + 2\text{KOH} \longrightarrow \text{Cu(OH)}_2\downarrow + \text{K}_2\text{SO}_4",
        "type": "🔀 दुहेरी विस्थापन अभिक्रिया (Double Displacement)",
        "explanation": "दोन संयुगांमधील आयनांची अदलाबदल होऊन कॉपर हायड्रॉक्साइडचा निळा अवक्षेप मिळतो."
    },
    {
        "id": 13,
        "reaction": r"\text{SO}_3 + \text{H}_2\text{O} \longrightarrow \text{H}_2\text{SO}_4",
        "type": "➕ संयोग अभिक्रिया (Combination)",
        "explanation": "सल्फर ट्रायऑक्साइड आणि पाणी एकत्र येऊन सल्फ्यूरिक आम्ल हे एकमेव उत्पादित बनते."
    },
    {
        "id": 14,
        "reaction": r"2\text{Ag}_2\text{O} \xrightarrow{\Delta} 4\text{Ag} + \text{O}_2\uparrow",
        "type": "💥 अपघटन अभिक्रिया (Decomposition)",
        "explanation": "उष्णतेमुळे सिल्व्हर ऑक्साइडचे विघटन होऊन सिल्व्हर धातू आणि ऑक्सिजन वायू वेगळे होतात."
    },
    {
        "id": 15,
        "reaction": r"\text{Cr}_2\text{O}_3 + 2\text{Al} \longrightarrow \text{Al}_2\text{O}_3 + 2\text{Cr}",
        "type": "🔄 विस्थापन अभिक्रिया (Displacement)",
        "explanation": "अल्युमिनियम हा क्रोमियमपेक्षा अधिक क्रियाशील असल्याने तो ऑक्साईडमधून क्रोमियमला विस्थापित करतो."
    },
    {
        "id": 16,
        "reaction": r"\text{AgNO}_3 + \text{KBr} \longrightarrow \text{AgBr}\downarrow + \text{KNO}_3",
        "type": "🔀 दुहेरी विस्थापन अभिक्रिया (Double Displacement)",
        "explanation": "सिल्व्हर आणि पोटॅशियमच्या आयनांची अदलाबदल होऊन सिल्व्हर ब्रोमाइडचा फिकट पिवळा अवक्षेप मिळतो."
    },
    {
        "id": 17,
        "reaction": r"\text{BaO} + \text{CO}_2 \longrightarrow \text{BaCO}_3",
        "type": "➕ संयोग अभिक्रिया (Combination)",
        "explanation": "बेरियम ऑक्साईड आणि कार्बन डायऑक्साईड यांच्या संयोगातून बेरियम कार्बोनेट तयार होते."
    },
    {
        "id": 18,
        "reaction": r"2\text{NaHCO}_3 \xrightarrow{\Delta} \text{Na}_2\text{CO}_3 + \text{H}_2\text{O} + \text{CO}_2\uparrow",
        "type": "💥 अपघटन अभिक्रिया (Decomposition)",
        "explanation": "सोडियम बायकार्बोनेट (खाण्याचा सोडा) तापविल्यावर त्याचे अपघटन होऊन सोडियम कार्बोनेट, पाणी आणि कार्बन डायऑक्साईड मिळतात."
    },
    {
        "id": 19,
        "reaction": r"\text{Sn} + 2\text{AgNO}_3 \longrightarrow \text{Sn(NO}_3)_2 + 2\text{Ag}",
        "type": "🔄 विस्थापन अभिक्रिया (Displacement)",
        "explanation": "टिन (Sn) हा सिल्व्हरपेक्षा जास्त क्रियाशील असल्याने सिल्व्हरचे विस्थापन करतो."
    },
    {
        "id": 20,
        "reaction": r"\text{FeCl}_3 + 3\text{NH}_4\text{OH} \longrightarrow \text{Fe(OH)}_3\downarrow + 3\text{NH}_4\text{Cl}",
        "type": "🔀 दुहेरी विस्थापन अभिक्रिया (Double Displacement)",
        "explanation": "आयनांच्या देवाणघेवाणीतून फेरिक हायड्रॉक्साइडचा लालसर-तपकिरी अवक्षेप तयार होतो."
    }
]

# Sidebar Navigation
with st.sidebar:
    st.markdown("### 👨‍🏫 **शिक्षक प्रोफाईल**")
    st.markdown("""
    **नाव:** प्रा. राहुल सावंत  
    **पद:** Secondary School Teacher & AI Educator  
    **अनुभव:** १०+ वर्षे शिक्षण क्षेत्रात  
    **विषय:** विज्ञान, गणित आणि Artificial Intelligence
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
    st.info("💡 *'शिक्षणासोबतच शिका भविष्यातील तंत्रज्ञान!'*")

# 1. HOME PAGE
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
            <p>स्वयं-मूल्यमापनासाठी इंटरॅक्टिव्ह क्विझ, कोडिंग कोडी आणि तत्काळ निकाल व स्पष्टीकरण.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    st.subheader("📢 ताज्या घडामोडी व सूचना (Notice Board)")
    st.info("📌 **नवीन अपडेट:** 'धडा ३: रासायनिक अभिक्रिया आणि समीकरणे' यावर २० नवीन अभिक्रियांचा विशेष सराव विभाग अभ्यासक्रमात जोडला गेला आहे!")

# 2. SUBJECTS PAGE
elif selected_page == "📚 शालेय अभ्यासक्रम (Subjects)":
    st.header("📚 शालेय अभ्यासक्रम व शैक्षणिक साहित्य")
    st.write("येथून तुम्ही प्रकरणांनुसार नोट्स, रासायनिक समीकरणे आणि सराव पाहू शकता.")
    
    subject = st.selectbox("विषय निवडा:", ["विज्ञान आणि तंत्रज्ञान (Science)", "माहिती तंत्रज्ञान (IT/Coding)"])
    
    if subject == "विज्ञान आणि तंत्रज्ञान (Science)":
        tab1, tab2 = st.tabs(["🔬 धडा ३: रासायनिक अभिक्रिया आणि समीकरणे", "🪐 धडा १: गुरुत्वाकर्षण (Gravitation)"])
        
        with tab1:
            st.subheader("🧪 धडा ३: रासायनिक अभिक्रिया आणि समीकरणे (Chemical Reactions & Equations)")
            st.markdown("""
            रासायनिक अभिक्रियांचे प्रामुख्याने **४ मुख्य प्रकार** असतात:
            1. **➕ संयोग (Combination):** दोन किंवा अधिक अभिक्रियाकारकांपासून एकच उत्पादित तयार होते.
            2. **💥 अपघटन (Decomposition):** एकाच अभिक्रियाकारकाचे विघटन होऊन दोन किंवा अधिक उत्पादिते मिळतात.
            3. **🔄 विस्थापन (Displacement):** अधिक क्रियाशील मूलद्रव्य कमी क्रियाशील मूलद्रव्याला त्याच्या संयुगातून विस्थापित करते.
            4. **🔀 दुहेरी विस्थापन (Double Displacement):** अभिक्रियाकारकांमधील आयनांची अदलाबदल होऊन अवक्षेप तयार होतो.
            """)
            
            st.divider()
            st.markdown("### 🎯 पाठ्यपुस्तकाबाहेरील रंजक २० अभिक्रियांचा विशेष सराव")
            
            mode = st.radio("सराव मोड निवडा:", ["📋 सर्व २० अभिक्रियांची यादी व उत्तरे", "🎮 इंटरॅक्टिव्ह सोडवून पहा (Interactive Practice)"], horizontal=True)
            
            if mode == "📋 सर्व २० अभिक्रियांची यादी व उत्तरे":
                for r in REACTIONS_DATA:
                    with st.expander(f"अभिक्रिया {r['id']}: ${r['reaction']}$"):
                        st.markdown(f"**अभिक्रियेचा प्रकार:** `{r['type']}`")
                        st.write(f"💡 **स्पष्टीकरण:** {r['explanation']}")
            
            elif mode == "🎮 इंटरॅक्टिव्ह सोडवून पहा (Interactive Practice)":
                st.info("विद्यार्थी स्वतः प्रत्येक अभिक्रिया पाहून तिचा प्रकार ओळखून उत्तर बरोबर आहे का ते तपासू शकतात!")
                
                selected_rxn_idx = st.selectbox(
                    "अभिक्रिया निवडा:", 
                    range(len(REACTIONS_DATA)),
                    format_func=lambda i: f"अभिक्रिया {REACTIONS_DATA[i]['id']}"
                )
                
                curr = REACTIONS_DATA[selected_rxn_idx]
                st.markdown(f"### रासायनिक समीकरण:")
                st.latex(curr["reaction"])
                
                options_list = [
                    "➕ संयोग अभिक्रिया (Combination)",
                    "💥 अपघटन अभिक्रिया (Decomposition)",
                    "🔄 विस्थापन अभिक्रिया (Displacement)",
                    "🔀 दुहेरी विस्थापन अभिक्रिया (Double Displacement)"
                ]
                
                user_choice = st.radio("ही कोणत्या प्रकारची रासायनिक अभिक्रिया आहे? 🤔", options_list, key=f"rxn_quiz_{selected_rxn_idx}")
                
                if st.button("उत्तर तपासा (Check Answer)", key=f"btn_{selected_rxn_idx}"):
                    if user_choice == curr["type"]:
                        st.success(f"🎉 **अगदी बरोबर!** हे `{curr['type']}` चे उदाहरण आहे.")
                    else:
                        st.error(f"❌ **चूक!** योग्य उत्तर आहे: `{curr['type']}`")
                    st.info(f"💡 **स्पष्टीकरण:** {curr['explanation']}")

        with tab2:
            st.subheader("🪐 धडा १: गुरुत्वाकर्षण (Gravitation) - महत्त्वाचे मुद्दे")
            st.markdown("""
            - **न्यूटनचा वैश्विक गुरुत्वाकर्षणाचा सिद्धांत:** विश्वातील प्रत्येक वस्तू इतर वस्तूला एका विशिष्ट बलाने आकर्षित करते.
            - **सूत्र:** $F = G \\frac{m_1 m_2}{r^2}$
            - **अभ्यास प्रश्न:** गुरुत्वीय त्वरण ($g$) चे मूल्य पृथ्वीच्या पृष्ठभागावर किती असते? ($9.8 \\text{ m/s}^2$)
            """)
            st.button("📥 PDF नोट्स डाउनलोड करा (Sample)")

    elif subject == "माहिती तंत्रज्ञान (IT/Coding)":
        st.subheader("💻 कोडिंगच्या मूलभूत गोष्टी (Python & Logic)")
        st.code("""
# विद्यार्थ्यांसाठी पहिला पायथन प्रोग्रॅम
student_name = "आर्यन"
marks = 95

print(f"अभिनंदन {student_name}! तुमचे गुण {marks}% आहेत.")
        """, language="python")

# 3. AI LAB PAGE
elif selected_page == "🤖 AI लॅब & टूल्स (AI Lab)":
    st.header("🤖 AI लॅब - प्रत्यक्ष शिकूया AI कसे काम करते!")
    st.write("विद्यार्थ्यांसाठी कृत्रिम बुद्धिमत्तेचे (AI) सोपे प्रात्यक्षिक मॉडेल्स.")
    
    ai_demo = st.radio("लॅब प्रयोग निवडा:", [
        "1. AI भावना ओळखक (Sentiment Analyzer)",
        "2. प्रॉमप्ट इंजिनिअरिंग ट्रेनर (Prompt Playground)"
    ])
    
    if ai_demo == "1. AI भावना ओळखक (Sentiment Analyzer)":
        st.subheader("🔍 वाक्यातील भावना ओळखा (Text Sentiment)")
        user_text = st.text_input("कोणतेही इंग्रजी किंवा सोपे वाक्य टाका:", "I love studying Science and AI!")
        
        if st.button("भावना तपासा (Analyze)"):
            positive_words = ["love", "good", "great", "awesome", "छान", "उत्तम", "आवडते"]
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
        role = st.selectbox("भूमिका (Role):", ["एक विज्ञान शिक्षक", "एक इतिहासकार", "एक संगणक तज्ज्ञ"])
        topic = st.text_input("विषय (Topic):", "सौरऊर्जेचे महत्त्व")
        
        st.markdown("##### 🚀 तयार झालेला स्मार्ट प्रॉमप्ट:")
        generated_prompt = f"तुम्ही '{role}' आहात. शालेय विद्यार्थ्यांना समजेल अशा सोप्या भाषेत '{topic}' या विषयावर ३ महत्त्वाचे मुद्दे समजावून सांगा."
        st.code(generated_prompt, language="text")

# 4. QUIZ ZONE (DYNAMIC QUESTIONS)
elif selected_page == "📝 सराव चाचणी (Quiz Zone)":
    st.header("📝 सराव प्रश्नमंजुषा (Interactive Quiz)")
    st.write("विषय निवडा, प्रश्नांची उत्तरे द्या आणि तत्काळ गुण व स्पष्टीकरण तपासा!")
    
    selected_topic = st.selectbox("🎯 क्विझचा विषय निवडा:", list(QUIZ_DATABASE.keys()))
    current_questions = QUIZ_DATABASE[selected_topic]
    
    user_answers = {}
    
    with st.form("interactive_quiz_form"):
        for i, q in enumerate(current_questions, start=1):
            st.markdown(f"#### **प्रश्न {i}:** {q['question']}")
            user_answers[i] = st.radio(
                "योग्य पर्याय निवडा:", 
                q["options"], 
                key=f"q_{selected_topic}_{i}",
                index=None
            )
            st.write("")
        
        submit_btn = st.form_submit_button("🏁 उत्तरे जमा करा (Submit Answers)")
        
    if submit_btn:
        score = 0
        total = len(current_questions)
        
        st.divider()
        st.subheader("📊 तुमचा निकाल आणि उत्तर स्पष्टीकरण:")
        
        for i, q in enumerate(current_questions, start=1):
            ans = user_answers.get(i)
            if ans == q["answer"]:
                score += 1
                st.success(f"✅ **प्रश्न {i}: बरोबर!** (तुमचे उत्तर: {ans})")
            else:
                st.error(f"❌ **प्रश्न {i}: चूक!** (तुमचे उत्तर: {ans if ans else 'दिले नाही'}) | **बरोबर उत्तर:** {q['answer']}")
            
            if "explanation" in q:
                st.caption(f"💡 *स्पष्टीकरण:* {q['explanation']}")
                
        st.markdown(f"""
        <div class="score-badge">
            🎉 तुमचे एकूण गुण: {score} / {total}
        </div>
        """, unsafe_allow_html=True)
        
        if score == total:
            st.balloons()
            st.success("अतिशय उत्कृष्ट! तुम्ही १००% गुण मिळवले आहेत!")
        elif score >= total / 2:
            st.info("छान प्रयत्न! आणखी थोडा अभ्यास केल्यास पैकीच्या पैकी गुण मिळतील.")
        else:
            st.warning("पुन्हा प्रयत्न करा आणि संकल्पना समजून घ्या.")

# 5. DOUBT BOX
elif selected_page == "📬 शंका विचारा (Doubt Box)":
    st.header("📬 शिक्षकांना शंका विचारा (Ask Your Teacher)")
    st.write("अभ्यासात काही अडचण असल्यास खालील फॉर्म भरून प्रश्न विचारा.")
    
    with st.form("doubt_form"):
        s_name = st.text_input("तुमचे नाव (Student Name):")
        s_class = st.selectbox("इयत्ता (Class):", ["८ वी (8th)", "९ वी (9th)", "१० वी (10th)", "इतर"])
        s_question = st.text_area("तुमचा प्रश्न किंवा शंका (Your Question):")
        
        send_btn = st.form_submit_button("प्रश्न पाठवा (Send)")
        if send_btn:
            if s_name and s_question:
                st.success(f"धन्यवाद {s_name}! तुमचा प्रश्न नोंदवला गेला आहे. शिक्षक लवकरच उत्तर देतील.")
            else:
                st.error("कृपया नाव आणि प्रश्न पूर्ण भरा.")

st.divider()
st.markdown("<p style='text-align: center; color: gray;'>© 2026 AI Shikshak Portal | विद्यार्थ्यांच्या उज्ज्वल भविष्यासाठी समर्पित</p>", unsafe_allow_html=True)
