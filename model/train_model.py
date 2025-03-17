import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping

# Load the saved .npy files
X_train = np.load("../dataset/X_train.npy")
X_test = np.load("../dataset/X_test.npy")
y_train = np.load("../dataset/y_train.npy")
y_test = np.load("../dataset/y_test.npy")

# Print shape to verify data
print(f"Train Data Shape: {X_train.shape}, Train Labels: {y_train.shape}")
print(f"Test Data Shape: {X_test.shape}, Test Labels: {y_test.shape}")

def build_model():
    model = keras.Sequential([
        layers.Conv2D(32, (3, 3), activation="relu", input_shape=(200, 200, 3)),
        layers.MaxPooling2D(2, 2),

        layers.Conv2D(64, (3, 3), activation="relu"),
        layers.MaxPooling2D(2, 2),

        layers.Conv2D(128, (3, 3), activation="relu"),
        layers.MaxPooling2D(2, 2),

        layers.Flatten(),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.2),
        layers.Dense(1, activation="linear")  # Output layer (Age Prediction)
    ])
    
    # model.compile(optimizer="adam", loss="mean_squared_error", metrics=["mae"])
    model.compile(optimizer="adam", loss="huber", metrics=["mae"])
    return model

model = build_model()
model.summary()

# Add early stopping
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
# Train the model
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

# Save the trained model
model.save("../model/age_detection_model.h5")
print("Model saved successfully!")

# plt.plot(history.history["loss"], label="Train Loss")
# plt.plot(history.history["val_loss"], label="Validation Loss")
# plt.legend()
# plt.title("Loss Curve")
# plt.show()

# plt.plot(history.history["mae"], label="Train MAE")
# plt.plot(history.history["val_mae"], label="Validation MAE")
# plt.legend()
# plt.title("Mean Absolute Error Curve")
# plt.show()


y_pred = model.predict(X_test)

plt.scatter(y_test, y_pred)
plt.xlabel("Actual Age")
plt.ylabel("Predicted Age")
plt.title("Age Prediction Accuracy")
plt.show()
