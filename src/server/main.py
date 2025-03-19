from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from PIL import Image
import torch
import numpy as np
from io import BytesIO
from ultralytics import YOLO
import simplejpeg as sjpg

app = FastAPI()

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

# Load the pre-trained object detection model
model = YOLO('yolov10n')
model.eval()  # Set the model to evaluation mode
model.to(device)

@app.post(
    "/predict/",
    # responses = {
    #     200: {'content': {'image/jpg': {}}},
    # },
    # response_class=Response,
)
async def predict(file: UploadFile = File(...)):
    # Read the image
    image_data = await file.read()
    image = Image.open(BytesIO(image_data)).convert("RGB")

    # Perform object detection
    predictions = model(image)

    detected_image = predictions[0].plot()
    print(detected_image.shape)
    detected_image = np.ascontiguousarray(detected_image[..., ::-1]) # convert to RGB
    detected_image_buffer = sjpg.encode_jpeg(detected_image)

    return Response(content=detected_image_buffer, media_type='image/jpg')
