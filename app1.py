import numpy as np
import matplotlib.pyplot as plt 
from tkinter.filedialog import askopenfilename
import tifffile as tiff
import cv2 
import matplotlib.image as mpimg
import streamlit as st
from googletrans import Translator, LANGUAGES
import pytesseract 
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

#========================  INPUT IMAGE===========================

file_upload = st.file_uploader("Upload Image",['png','jpg'])

if file_upload is None:
    st.text("Kindly Upload input Image")
else:
    img = mpimg.imread(file_upload)
    st.image(img, caption='Input Image')
    st.write("---------------------------------")

    #============================ 4.TEXT EXTRACTION ====================
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    trans_text = pytesseract.image_to_string(img, lang='eng')

    st.write("Extracted Text", trans_text)
    
    # ----------------------- Translation Section ----------------------
    
    # Language options for translation
    language_names = list(LANGUAGES.values())
    language_codes = list(LANGUAGES.keys())

    # Layout for selecting languages
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Source language selection
        src_language = st.selectbox("Source Language", language_names, index=language_names.index('english'))
        src_language_code = language_codes[language_names.index(src_language)]
        st.write(trans_text)
        
        # Save input text to a file for processing
        if st.button("Submit"):
            try:
                with open('inputtext.txt', 'w') as file1:
                    file1.write(trans_text)
            except Exception as e:
                st.error(f"Error writing input text to file: {e}")
    
    with col2:
        # Destination language selection
        dest_language = st.selectbox("Destination Language", language_names, index=language_names.index('spanish'))
        dest_language_code = language_codes[language_names.index(dest_language)]

        # Read input text from file
        try:
            with open('inputtext.txt', 'r') as file1:
                input_text = file1.read().strip()
        except Exception as e:
            st.error(f"Error reading from file: {e}")
            input_text = ""
        
        # Translate text
        if input_text:
            translated_text = GoogleTranslator(source=src_language_code, target=dest_language_code).translate(input_text)
            st.text_area("", value=translated_text, height=200, disabled=True)

            # ======================== Speech Conversion ==========================
            # Language options for speech conversion
            speech_language_names = list(LANGUAGES.values())
            speech_language_codes = list(LANGUAGES.keys())
            
            # Allow the user to choose a language for speech
            speech_lang = st.selectbox("Choose Speech Language", speech_language_names, index=speech_language_names.index(dest_language))
            speech_lang_code = speech_language_codes[speech_language_names.index(speech_lang)]
            
            # Convert the translated text to speech using gTTS
            if st.button("Convert to Speech"):
                tts = gTTS(text=translated_text, lang=speech_lang_code, slow=False)
                speech_file = "translated_speech.mp3"
                tts.save(speech_file)
                
                # Provide the option to download the speech file
                st.audio(speech_file, format="audio/mp3")
                st.download_button(label="Download Speech", data=open(speech_file, 'rb').read(), file_name="translated_speech.mp3")

        else:
            st.text_area("", value="Translation could not be performed. Check inputs and try again.", height=200, disabled=True)
    
    st.write("---------------------------------------------------------------------------------------")
