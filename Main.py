#======================== IMPORT PACKAGES ===========================

import numpy as np
import matplotlib.pyplot as plt 
from tkinter.filedialog import askopenfilename
import tifffile as tiff
import cv2 
import matplotlib.image as mpimg

    
#============================ 2.INPUT IMAGE ====================


filename = askopenfilename()
img = mpimg.imread(filename)
plt.imshow(img, cmap='gray')
plt.title("Original Image")
plt.show()


#============================ 2.IMAGE PREPROCESSING ====================

#==== RESIZE IMAGE ====

resized_image = cv2.resize(img,(300,300))
img_resize_orig = cv2.resize(img,((50, 50)))

fig = plt.figure()
plt.title('RESIZED IMAGE')
plt.imshow(resized_image, cmap='gray')
plt.axis ('off')
plt.show()
   

#==== GRAYSCALE IMAGE ====

try:            
    gray11 = cv2.cvtColor(img_resize_orig, cv2.COLOR_BGR2GRAY)
    
except:
    gray11 = img_resize_orig
   
fig = plt.figure()
plt.title('GRAY SCALE IMAGE')
plt.imshow(gray11,cmap="gray")
plt.axis ('off')
plt.show()


#============================ 3.FEATURE EXTRACTION ====================

# === MEAN MEDIAN VARIANCE ===

mean_val = np.mean(gray11)
median_val = np.median(gray11)
var_val = np.var(gray11)
Test_features = [mean_val,median_val,var_val]


print()
print("----------------------------------------------")
print(" MEAN, VARIANCE, MEDIAN ")
print("----------------------------------------------")
print()
print("1. Mean Value     =", mean_val)
print()
print("2. Median Value   =", median_val)
print()
print("3. Variance Value =", var_val)



#============================ 4.TEXT EXTRACTION ====================


import pytesseract 
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
text = pytesseract.image_to_string(img,lang = 'eng')


print()
print("----------------------------------------------")
print(" EXTRACTED TEXT")
print("----------------------------------------------")
print()
print(text)




#============================ 5.TEXT CONVERSION ====================

from deep_translator import GoogleTranslator

# Text to be translated
text_to_translate = text

# Translate to Spanish (es)
translated_text = GoogleTranslator(source='en', target='ta').translate(text_to_translate)

# Print the translated text
print(f"Original text: {text_to_translate}")
print(f"Translated text: {translated_text}")



#============================ 6.SPEECH CONVERSION ====================


from gtts import gTTS
import os

# Text to be converted to speech
text = text_to_translate

# Language in which you want to convert
language = 'ta'  # 'en' for English, you can change it to another language (e.g., 'es' for Spanish)

# Passing the text and language to the engine
tts = gTTS(text=text, lang=language, slow=False)

# Saving the converted audio to a file
tts.save("output.mp3")

# Playing the converted audio (optional)
os.system("start output.mp3")  # For Windows
# os.system("mpg321 output.mp3")  # For Linux, if mpg321 is installed










