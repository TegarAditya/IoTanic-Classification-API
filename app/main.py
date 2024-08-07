import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

load_dotenv()

PORT = int(os.getenv("PORT", 8000))

app = FastAPI()

origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL = tf.keras.models.load_model("./model.h5", compile=False)

CLASS_NAMES = ["Healthy Rice Leaf", "Bacterial Leaf Blight", "Brown Spot", "Leaf Scald", "Leaf Blast",
               "Narrow Brown Leaf Spot", "Rice Hispa", "Sheath Blight"]

supported_content_types = ["image/jpeg", "image/png", "image/webp", "image/avif"]


@app.get("/ping")
async def ping():
    return "Hello, I am alive"


def read_file_as_image(data) -> np.ndarray:
    try:
        image = Image.open(BytesIO(data))

        if image.mode != "RGB":
            image = image.convert("RGB")

        if image.format != "JPEG":
            buffer = BytesIO()
            image.save(buffer, format="JPEG")
            buffer.seek(0)
            image = Image.open(buffer)

        return np.array(image)
    except Exception as e:
        print(f"Error in image processing: {e}")
        raise


@app.post("/predict")
async def predict(
        file: UploadFile = File(...)
):
    if file.content_type not in supported_content_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f'File {file.filename} has unsupported extension type',
        )

    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)

    predictions = MODEL.predict(img_batch)
    try:
        predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
        confidence = np.max(predictions[0])
        return {
            'class': predicted_class,
            'confidence': float(confidence)
        }
    except Exception as e:
        print(e)
        return {
            'class': 'N/A',
            'confidence': 'N/A'
        }


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=PORT)
