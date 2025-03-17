from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
from PIL import Image
import io

# Initialize FastAPI app
app = FastAPI()

# Allow all origins for debugging (use specific origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model
model = tf.keras.models.load_model("../model/age_detection_model.h5")
print("✅ Model Loaded Successfully!")

# Preprocess image
def preprocess_image(image: Image.Image):
    image = image.resize((200, 200))  # Resize to match CNN input shape
    image = np.array(image) / 255.0   # Normalize (0-1)
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

# API endpoint for age prediction
@app.post("/predict")
async def predict_age(file: UploadFile = File(...)):
    # Read uploaded image
    image = Image.open(io.BytesIO(await file.read()))
    image = preprocess_image(image)
    
    # Predict age
    prediction = model.predict(image)
    age = int(prediction[0][0])  # Extract age value
    
    return {"predicted_age": age}

# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
