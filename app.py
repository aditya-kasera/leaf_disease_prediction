from typing import Dict

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image

# import os
# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf

app = FastAPI()

# Allow requests from the specific origins where your frontend applications are hosted
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000" ,"http://127.0.0.1:5500" ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


MODEL = tf.keras.models.load_model("resnet50_mode4.h5")
CLASS_NAMES = ['Anthracnose',
 'Bacterial postule',
 'FLS',
 'Iron deficiency',
 'PSS(Puprle seed stain)',
 'RAB']


@app.get("/ping")
async def ping():
    return "hello jagrati"


def read_file_as_image(data) -> dict[str, str | float]:
    # image = np.array(Image.open(BytesIO(data)))
    # Open the image and resize it to (256, 256)
    image = Image.open(BytesIO(data))
    image = image.resize((256, 256))
    # Convert the image to a NumPy array
    image = np.array(image)
    return image



@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = read_file_as_image(await file.read())
    # [256,256,3] it's batch ===== [[256 ]]
    img_batch = np.expand_dims(image, 0)

    predictions = MODEL.predict(img_batch)          
    print(predictions)
    print(np.argmax(predictions[0] ))
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])

    # return {
    #     'class': predicted_class,
    #     'confidence': float(confidence)
    # }
    return {
        'class': predicted_class,
        'confidence': f"{float(confidence) * 100:.2f}%"
        # Convert confidence to percentage with two decimal places and add %
    }


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
