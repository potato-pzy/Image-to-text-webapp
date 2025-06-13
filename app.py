import numpy as np
import matplotlib.pyplot as plt
import cv2
import base64
import streamlit as st
from gtts import gTTS
from PIL import Image
import os
import subprocess
from pathlib import Path
import shutil
import platform
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Configure Streamlit page
st.set_page_config(
    page_title="OCR Vision - Photo to Text",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS for modern UI with mobile responsiveness
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .stApp {
        font-family: "Inter", sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-container {
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 15px;
        }
        
        .hero-title {
            font-size: 2rem !important;
        }
        
        .hero-subtitle {
            font-size: 1rem !important;
        }
        
        .card-title {
            font-size: 1.2rem !important;
        }
        
        .feature-card {
            padding: 1rem !important;
        }
        
        .stButton > button {
            width: 100%;
            margin: 0.5rem 0;
        }
    }
    
    @media (max-width: 480px) {
        .hero-title {
            font-size: 1.5rem !important;
        }
        
        .main-container {
            padding: 0.75rem;
            border-radius: 10px;
        }
    }
    
    /* Hero section */
    .hero-title {
        font-family: "Poppins", sans-serif;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(45deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        text-align: center;
        color: #E0E0E0;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(5px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
    }
    
    .card-title {
        font-family: "Poppins", sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: #FFD700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        background: linear-gradient(45deg, #FF5252, #26C6DA);
    }
    
    /* File uploader */
    .stFileUploader > div > div {
        background: rgba(255, 255, 255, 0.1);
        border: 2px dashed rgba(255, 255, 255, 0.3);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div > div:hover {
        border-color: #FFD700;
        background: rgba(255, 215, 0, 0.1);
    }
    
    /* Text areas */
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        color: #ffffff;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 10px;
        border: none;
        backdrop-filter: blur(10px);
    }
    
    /* Progress indicators */
    .progress-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Audio player styling */
    audio {
        width: 100%;
        border-radius: 10px;
    }
    
    /* Download button special styling */
    .download-btn {
        background: linear-gradient(45deg, #4CAF50, #45a049);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    }
    
    .download-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4);
    }
    
    /* Divider */
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        margin: 2rem 0;
        border-radius: 1px;
    }
    
    /* Status indicators */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        margin: 0.5rem 0;
    }
    
    .status-success {
        background: rgba(76, 175, 80, 0.2);
        color: #4CAF50;
        border: 1px solid rgba(76, 175, 80, 0.3);
    }
    
    .status-processing {
        background: rgba(255, 193, 7, 0.2);
        color: #FFC107;
        border: 1px solid rgba(255, 193, 7, 0.3);
    }
    
    /* Mobile specific adjustments */
    @media (max-width: 768px) {
        .stFileUploader > div > div {
            padding: 1rem;
        }
        
        .stTextArea > div > div > textarea {
            font-size: 0.9rem;
        }
        
        .divider {
            margin: 1rem 0;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state variables
if 'translated_text' not in st.session_state:
    st.session_state.translated_text = ""
if 'speech_file' not in st.session_state:
    st.session_state.speech_file = ""
if 'translation_ready' not in st.session_state:
    st.session_state.translation_ready = False

# Hero Section
st.markdown("""
<div class="main-container">
    <h1 class="hero-title">👁️ OCR Vision</h1>
    <p class="hero-subtitle">Transform images into text with AI-powered OCR technology</p>
</div>
""", unsafe_allow_html=True)

# Features showcase
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="card-title">📸 Image Upload</div>
        <p>Upload any image with text and let our AI extract it instantly</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="card-title">🌍 Translation</div>
        <p>Translate extracted text to over 100 languages automatically</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="card-title">🔊 Text-to-Speech</div>
        <p>Convert translated text to natural-sounding speech</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Main application section
st.markdown("""
<div class="main-container">
    <div class="card-title">📤 Upload Your Image</div>
</div>
""", unsafe_allow_html=True)

# Upload image with enhanced UI
file_upload = st.file_uploader(
    "Choose an image file", 
    ['png', 'jpg', 'jpeg'], 
    help="Upload a clear image containing text for best OCR results"
)

if file_upload is None:
    st.markdown("""
    <div class="feature-card">
        <p style="text-align: center; font-size: 1.1rem; color: #E0E0E0;">
            📝 Please upload an image to begin text extraction
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Load the image using PIL
    img = Image.open(file_upload)
    
    # Display the image with enhanced styling
    st.markdown("""
    <div class="main-container">
        <div class="card-title">🖼️ Uploaded Image</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the image
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(img, caption='Your uploaded image', use_container_width=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Convert the image to grayscale if it's not already
    if img.mode != 'L':
        img = img.convert('L')
    
    # Save the image to a temporary file
    img.save("temp_image.png")
    
    # OCR Processing
    import pytesseract

    # Determine if we're running locally or on cloud
    is_windows = platform.system() == 'Windows'

    # Show processing status
    st.markdown("""
    <div class="main-container">
        <div class="card-title">⚡ Processing Status</div>
        <div class="status-badge status-processing">🔄 Initializing OCR Engine...</div>
    </div>
    """, unsafe_allow_html=True)

    if is_windows:
        # Local Windows setup - use bundled Tesseract
        current_dir = os.path.dirname(os.path.abspath(__file__))
        tesseract_dir = os.path.join(current_dir, 'tesseract')
        tesseract_cmd = os.path.join(tesseract_dir, 'tesseract.exe')
        tessdata_dir = os.path.join(tesseract_dir, 'tessdata')

        # Verify Tesseract exists
        if not os.path.isfile(tesseract_cmd):
            st.error(f"❌ Tesseract executable not found at: {tesseract_cmd}")
            st.stop()

        # Set Tesseract command path
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        os.environ['TESSDATA_PREFIX'] = tessdata_dir
        
        st.markdown('<div class="status-badge status-success">✅ Local Tesseract Ready</div>', unsafe_allow_html=True)
    else:
        # Cloud deployment - use system Tesseract
        if not shutil.which('tesseract'):
            st.error("❌ System Tesseract not found. Please check deployment configuration.")
            st.stop()
        
        st.markdown('<div class="status-badge status-success">✅ System Tesseract Ready</div>', unsafe_allow_html=True)

    # Perform OCR with progress indication
    try:
        with st.spinner('🔍 Extracting text from image...'):
            trans_text = pytesseract.image_to_string("temp_image.png", lang='eng')
            
        if not trans_text.strip():
            st.warning("⚠️ No text was extracted from the image. Please try with a clearer image.")
            st.stop()
    except Exception as e:
        st.error(f"❌ Error during text extraction: {str(e)}")
        st.stop()
    
    # Display extracted text
    st.markdown("""
    <div class="main-container">
        <div class="card-title">📝 Extracted Text</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.text_area("", value=trans_text, height=200, disabled=True, key="extracted_text")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Translation Section
    st.markdown("""
    <div class="main-container">
        <div class="card-title">🌐 Text Translation</div>
    </div>
    """, unsafe_allow_html=True)
    
    from googletrans import Translator, LANGUAGES
    
    # Define language options
    language_names = list(LANGUAGES.values())
    language_codes = list(LANGUAGES.keys())
    
    # Layout for translation
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Source Language**")
        src_language = st.selectbox("", language_names, index=language_names.index('english'), key="src_lang")
        src_language_code = language_codes[language_names.index(src_language)]
        
        st.markdown("**Original Text**")
        st.text_area("", value=trans_text, height=150, disabled=True, key="source_text")
        
        translate_btn = st.button("🔄 Translate Text", key="translate_btn")
    
    with col2:
        st.markdown("**Target Language**")
        dest_language = st.selectbox("", language_names, index=language_names.index('spanish'), key="dest_lang")
        dest_language_code = language_codes[language_names.index(dest_language)]
        
        st.markdown("**Translated Text**")
        
        if translate_btn:
            try:
                with st.spinner('🔄 Translating text...'):
                    from deep_translator import GoogleTranslator
                    translated_text = GoogleTranslator(source=src_language_code, target=dest_language_code).translate(trans_text)
                
                # Update session state
                st.session_state.translated_text = translated_text
                st.session_state.translation_ready = True
                
                st.text_area("", value=translated_text, height=150, disabled=True, key="translated_text_display")
                
            except Exception as e:
                st.error(f"❌ Translation error: {str(e)}")
                translated_text = "Translation failed. Please try again."
                st.text_area("", value=translated_text, height=150, disabled=True, key="translated_text_error")
        else:
            # Show previous translation if available
            if st.session_state.translation_ready and st.session_state.translated_text:
                st.text_area("", value=st.session_state.translated_text, height=150, disabled=True, key="previous_translation")
            else:
                st.text_area("", value="Click 'Translate Text' to see translation here", height=150, disabled=True, key="placeholder_text")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Speech Section
    if st.session_state.translation_ready and st.session_state.translated_text:
        st.markdown("""
        <div class="main-container">
            <div class="card-title">🔊 Text-to-Speech</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Layout for speech
        col1, col2 = st.columns([1, 1])
        
        with col1:
            speech_language_names = list(LANGUAGES.values())
            speech_language_codes = list(LANGUAGES.keys())
            
            speech_lang = st.selectbox("Choose Speech Language", speech_language_names, 
                                     index=speech_language_names.index(dest_language), key="speech_lang")
            speech_lang_code = speech_language_codes[speech_language_names.index(speech_lang)]
            
            if st.button("🎤 Generate Speech", key="speech_btn"):
                try:
                    with st.spinner('🎵 Converting text to speech...'):
                        tts = gTTS(text=st.session_state.translated_text, lang=speech_lang_code, slow=False)
                        speech_file = "translated_speech.mp3"
                        tts.save(speech_file)
                        
                        st.session_state.speech_file = speech_file
                        
                    st.success("✅ Speech generated successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Speech generation error: {str(e)}")
        
        with col2:
            if st.session_state.speech_file and os.path.exists(st.session_state.speech_file):
                st.markdown("**🎧 Audio Player**")
                st.audio(st.session_state.speech_file, format="audio/mp3")
                
                with open(st.session_state.speech_file, 'rb') as audio_file:
                    st.download_button(
                        label="📥 Download Audio",
                        data=audio_file.read(),
                        file_name="translated_speech.mp3",
                        mime="audio/mp3"
                    )

# Footer
st.markdown("""
<div class="main-container" style="margin-top: 3rem;">
    <p style="text-align: center; color: #B0B0B0; font-size: 0.9rem;">
        🚀 Powered by Tesseract OCR & Google Translate | Built with ❤️ using Streamlit
    </p>
</div>
""", unsafe_allow_html=True)