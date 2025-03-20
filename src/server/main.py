from io import BytesIO

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response

import numpy as np
import torch
from PIL import Image
from ultralytics import YOLO
import simplejpeg as sjpg

app = FastAPI()

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

# Load the pre-trained object detection model
model = YOLO('yolov10n')
model.to(device)

@app.post('/predict/')
async def predict(file: UploadFile = File(...)):
    # Read the image
    image_data = await file.read()
    image = Image.open(BytesIO(image_data))

    # Perform object detection
    predictions = model(
        image,
        device=device,
        verbose=False,

        stream=True,
        # half=True,
    )

    # detected_image = predictions[0].plot()
    detected_image = next(predictions).plot()
    detected_image = np.ascontiguousarray(detected_image[..., ::-1]) # convert to RGB

    # by Pillow
    frame = Image.fromarray(detected_image)
    detected_image = BytesIO()
    frame.save(detected_image, format='JPEG')
    detected_image_buffer = detected_image.getvalue()

    return Response(content=detected_image_buffer, media_type='image/jpg')
