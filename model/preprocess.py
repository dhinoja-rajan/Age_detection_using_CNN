import os
import cv2
import numpy as np
import pandas as pd
import shutil
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

dataset_path = "D:/AI ENGINEERING/Datasets/CNN/UTKface_inthewild/part3"  # Update with actual path
image_size = (200, 200)  # Resize images to 200x200

def get_age_from_filename(filename):
    try:
        age = int(filename.split("_")[0])  # Extract age from filename
        return age
    except:
        return None

images = []
ages = []

for file in os.listdir(dataset_path):
    path = os.path.join(dataset_path, file)
    
    if file.endswith(".jpg"):  # Process only image files
        age = get_age_from_filename(file)
        
        if age is not None:
            img = cv2.imread(path)  # Read image
            img = cv2.resize(img, image_size)  # Resize
            img = img / 255.0  # Normalize (0-1 range)
            
            images.append(img)
            ages.append(age)

# Convert lists to NumPy arrays
images = np.array(images)
ages = np.array(ages)

print(f"Total Images Processed: {len(images)}")

plt.figure(figsize=(10, 5))
for i in range(5):
    plt.subplot(1, 5, i+1)
    plt.imshow(images[i])
    plt.title(f"Age: {ages[i]}")
    plt.axis("off")
plt.show()

X_train, X_test, y_train, y_test = train_test_split(images, ages, test_size=0.2, random_state=42)

print(f"Training samples: {len(X_train)}, Testing samples: {len(X_test)}")

np.save("../dataset/X_train.npy", X_train)
np.save("../dataset/X_test.npy", X_test)
np.save("../dataset/y_train.npy", y_train)
np.save("../dataset/y_test.npy", y_test)

print("Preprocessed data saved successfully!")
