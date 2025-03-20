from io import BytesIO
import json
import re

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response

import torch
from PIL import Image
from ultralytics import YOLO

app = FastAPI()

# Load the pre-trained object detection model
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
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
        conf=0.35,

        stream=True,
        # half=True,
    )

    # prepare data to response
    pred = next(predictions).cpu()
    boxes_data = pred.boxes.data
    content = json.dumps({
        'boxes': boxes_data.tolist(),
    }, indent=None)

    # lower decimal precision to reduce the length of message
    content = re.sub(r"(\.[0-9]{3})[0-9]*", r"\1", content)
    
    return Response(content=content, media_type='application/json')
