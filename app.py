from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from typing import Optional

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input: str, image: Optional[Image.Image]) -> str:
    if input != "":
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text

# Set up the Streamlit page
st.set_page_config(page_title="Gemini Image Demo")
st.header("Gemini Application")

# Text input
input_prompt: str = st.text_input("Input prompt:", key="input")

# Image uploader
uploaded_image = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
img: Optional[Image.Image] = None

if uploaded_image is not None:
    st.success(f"Image '{uploaded_image.name}' uploaded successfully!")
    img = Image.open(uploaded_image)
    st.image(img, caption=f"Uploaded Image: {uploaded_image.name}", use_column_width=True)
else:
    st.info("Please upload an image file.")

# Submit button
submit = st.button("Tell me about the image")

# Generate and display the response
if submit:
    response = get_gemini_response(input_prompt, img)
    st.subheader("The response is...")
    st.write(response)