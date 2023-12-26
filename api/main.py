from fastapi import FastAPI, File, UploadFile
from io import BytesIO
from PIL import Image # Image class from Pillow
import numpy as np
import tensorflow as tf
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()

CLASS_NAMES = [
    'Tomato_Bacterial_spot',
    'Tomato_Early_blight',
    'Tomato_Healthy',
    'Tomato_Late_blight',
    'Tomato_Leaf_Mold',
    'Tomato_Mosaic_virus',
    'Tomato_Septoria_leaf_spot',
    'Tomato_Spider_mites',
    'Tomato_Target_Spot',
    'Tomato_Yellow_Leaf_Curl_Virus'
]

# Load your model
MODEL_PATH = '/Users/aaryanpotdar/Desktop/Personal_Projects/TomatoDiseaseClassification/models/1'
model = tf.keras.models.load_model(MODEL_PATH)

@app.get("/")
async def root():
    # return {"message": "Test Message for Tomato Disease Classification model"}
    return FileResponse('api/index.html')

def read_image(file) -> np.ndarray:
    image = Image.open(BytesIO(file))
    image = image.resize((256, 256))
    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    return image

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = read_image(await file.read()) # async routine so we call await.
                                          # if first request takes time it will be put in suspend mode and second request will be served
    prediction = model.predict(image)
    # prediction = [[10 values]] -> arr in arr so we must use prection[0]
    predicted_class = np.argmax(prediction, axis=1)[0]
    confidence = prediction[0][predicted_class]

    return {"predicted_class": CLASS_NAMES[int(predicted_class)],
            "confidence": float(confidence)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)