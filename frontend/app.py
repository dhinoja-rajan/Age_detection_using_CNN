import streamlit as st
import requests
from PIL import Image
import io

# FastAPI backend URL (running locally on port 8000)
API_URL = "http://127.0.0.1:8000/predict"

# Set up Streamlit app title
st.title("Age Detection App using CNN")

# File uploader
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.markdown("**Uploaded Image:**")
    st.image(image, use_container_width=True)

    # Prepare the image for sending to FastAPI
    img_byte_array = io.BytesIO()
    image.save(img_byte_array, format="PNG")
    img_byte_array = img_byte_array.getvalue()

    # Send the image to the FastAPI backend for prediction
    response = requests.post(API_URL, files={"file": img_byte_array})

    if response.status_code == 200:
        result = response.json()
        age = result.get("predicted_age")
        st.write(f"Predicted Age: **{age}** years")
    else:
        st.write("Error in prediction. Please try again.")
