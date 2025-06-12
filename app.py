import numpy as np
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename
import tifffile as tiff
import cv2
import matplotlib.image as mpimg
import base64
import streamlit as st
from gtts import gTTS
from PIL import Image

# Custom CSS for font and background
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Finlandica:ital,wght@0,400..700;1,400..700&family=Zain:wght@200;300;400;700;800;900&display=swap');
    /* Set background color */
    body {
        background-color: #f0f2f6;
    }

    /* Set font family and size */
    .stApp {
        font-family: "Zain", cursive;
        font-size: 16px;
        color: #000000;
        background-size: cover;
    }

    /* Style for headings */
    h1, h2, h3 {
        color: #31333F;
        font-weight: bold;
    }

    /* Style for buttons */
    .stButton button {
        background-color: #1E90FF;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
    }

    .stButton button:hover {
        background-color: #1C86EE;
    }

    /* Style for text areas */
    .stTextArea textarea {
         font-family: "Zain", cursive;
        font-color: #000000;
     
        border: 1px solid #D3D3D3;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
    }

    /* Style for select boxes */
    .stSelectbox select {
        background-color: #FFFFFF;
        border: 1px solid #D3D3D3;
        border-radius: 5px;
        padding: 10px;
        font-size: 26px;
    }

    /* Style for images */
    .stImage img {
        border-radius: 5px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* Style for audio player */
    .stAudio audio {
        border-radius: 5px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* Style for download button */
    .stDownloadButton button {
        background-color: #28A745;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
    }

    .stDownloadButton button:hover {
        background-color: #218838;
    }

    /* Custom background image */
    .stApp {
        background-image: url('data:image/png;base64,{{background_image}}');
        background-size: cover;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set the title of the app
st.markdown(f'<h1 style="color:#31333F;text-align: center;font-size:36px;">{"Photo to Text Converter App for the Visually Impaired"}</h1>', unsafe_allow_html=True)

# Add background image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('data:image/png;base64,{encoded_string}');
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
add_bg_from_local('neww.jpg')

# Upload image
st.write("--------------------------------------------------------------------------------------------------")
file_upload = st.file_uploader("Upload Image", ['png', 'jpg'])

if file_upload is None:
    st.text("Kindly Upload input Image")
else:
    # Load the image using PIL
    img = Image.open(file_upload)
    
    # Display the image
    st.image(img, caption='Input Image')
    st.write("----------------------------------------------------------------------------")
    
    # Convert the image to grayscale if it's not already
    if img.mode != 'L':
        img = img.convert('L')
    
    # Save the image to a temporary file or convert it to a format that pytesseract can handle
    img.save("temp_image.png")
    
    # Use pytesseract to extract text
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r'F:\project\CODE\CODE\tesseract\tesseract.exe'
    trans_text = pytesseract.image_to_string("temp_image.png", lang='eng')
    
    print()
    print("----------------------------------------------")
    print(" EXTRACTED TEXT")
    print("----------------------------------------------")
    print()
    print(trans_text)
    
    st.markdown(f'<h2 style="color:#31333F;text-align: center;font-size:24px; font-we">{"Extracted Text"}</h2>', unsafe_allow_html=True)
    st.write("-------------------------------------------------")
    st.write(trans_text)
    st.write("---------------------------------------------------------------------------------------")
    
    # Text Translation
    st.markdown(f'<h2 style="color:#31333F;text-align: center;font-size:28px;font-weight:bold;">{"Text Translation"}</h2>', unsafe_allow_html=True)
    
    from googletrans import Translator, LANGUAGES
    
    # Define language options
    language_names = list(LANGUAGES.values())
    language_codes = list(LANGUAGES.keys())
    
    # Layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Source language selection
        src_language = st.selectbox("Source Language", language_names, index=language_names.index('english'))
        src_language_code = language_codes[language_names.index(src_language)]
        
        # Save source language to file
        try:
            with open('source.txt', 'w') as file2:
                file2.write(src_language_code)
        except Exception as e:
            st.error(f"Error writing source language to file: {e}")
        
        # Input text area
        st.write(trans_text)
        
        if st.button("Submit"):
            # Save input text to file
            try:
                with open('inputtext.txt', 'w') as file1:
                    file1.write(trans_text)
            except Exception as e:
                st.error(f"Error writing input text to file: {e}")
    
    with col2:
        # Destination language selection
        dest_language = st.selectbox("Destination Language", language_names, index=language_names.index('spanish'))
        dest_language_code = language_codes[language_names.index(dest_language)]
        
        try:
            # Read source language code from file
            with open('source.txt', 'r') as file11:
                src_language_code = file11.read().strip()
            
            # Read input text from file
            with open('inputtext.txt', 'r') as file1:
                input_text = file1.read().strip()
        except Exception as e:
            st.error(f"Error reading from file: {e}")
            src_language_code = ""
            input_text = ""
    
        # Translate text
        if src_language_code and dest_language_code:
            from deep_translator import GoogleTranslator
            translated_text = GoogleTranslator(source=src_language_code, target=dest_language_code).translate(trans_text)
            st.text_area("", value=translated_text, height=200, disabled=True)
        else:
            st.text_area("", value="Translation could not be performed. Check inputs and try again.", height=200, disabled=True)
    
    st.write("---------------------------------------------------------------------------------------")
    
    # Speech Translation
    st.markdown(f'<h2 style="color:#31333F;text-align: center;font-size:28px;">{"Speech Translation"}</h2>', unsafe_allow_html=True)
    
    speech_language_names = list(LANGUAGES.values())
    speech_language_codes = list(LANGUAGES.keys())
    
    # Allow the user to choose a language for speech
    speech_lang = st.selectbox("Choose Speech Language", speech_language_names, index=speech_language_names.index(dest_language))
    speech_lang_code = speech_language_codes[speech_language_names.index(speech_lang)]
    
    if st.button("Convert to Speech"):
        tts = gTTS(text=translated_text, lang=speech_lang_code, slow=False)
        speech_file = "translated_speech.mp3"
        tts.save(speech_file)
        
        st.audio(speech_file, format="audio/mp3")
        st.download_button(label="Download Speech", data=open(speech_file, 'rb').read(), file_name="translated_speech.mp3")