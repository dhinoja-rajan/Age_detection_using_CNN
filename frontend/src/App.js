import React, { useState } from "react";

function App() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [predictedAge, setPredictedAge] = useState(null);
  const [loading, setLoading] = useState(false);

  // Handle file selection
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setImage(file);

    // Show image preview
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => setPreview(reader.result);
      reader.readAsDataURL(file);
    }
  };

  // Handle form submission with Fetch API
  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!image) {
      alert("Please select an image first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", image);

    try {
      setLoading(true);
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      setPredictedAge(data.predicted_age);
    } catch (error) {
      console.error("Error uploading image:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-6 rounded-xl shadow-lg w-96 text-center">
        <h1 className="text-2xl font-bold mb-4 text-gray-700">Age Detection</h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="block w-full p-2 border rounded-md"
          />

          {preview && (
            <img src={preview} alt="Preview" className="w-48 h-48 mx-auto mt-4 rounded-lg shadow-md" />
          )}

          <button
            type="submit"
            className="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition duration-200"
            disabled={loading}
          >
            {loading ? "Predicting..." : "Upload & Predict"}
          </button>
        </form>

        {predictedAge !== null && (
          <div className="mt-4 text-lg font-semibold text-gray-700">
            Predicted Age: <span className="text-blue-600">{predictedAge} years</span>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
