from io import BytesIO
import json
import time
from typing import List, Tuple

import requests
import torch
import numpy as np
from PIL import Image
import cv2
from ultralytics.engine.results import Results

# Define the API URL
API_URL = 'http://127.0.0.1:8000/predict/'
VIDEO_NAME = 'data/Parkour PARKOUR - The Office US.mp4'
with open('data/label_names.json') as f:
    LABEL_NAMES = json.load(f)
    LABEL_NAMES = {int(k): v for k, v in LABEL_NAMES.items()}

def read_frames_from_video(video_name: str) -> Tuple[List[np.ndarray], List[bytes]]:
    cap = cv2.VideoCapture(video_name)

    print('Width:', cap.get(cv2.CAP_PROP_FRAME_WIDTH), 'Height:', cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print('Video FPS:', cap.get(cv2.CAP_PROP_FPS))

    # check whether the video files is opened correctly
    if not cap.isOpened():
        print('Error: Cannot open video file')

    # read all frames out
    raw_frames = []
    frames = []
    while True:
        ret, raw_frame = cap.read()
        if not ret:
            break
        raw_frames.append(raw_frame)

        # convert to jpg by Pillow
        frame = Image.fromarray(raw_frame)
        output_frame = BytesIO()
        frame.save(output_frame, format='JPEG')
        frame_bytes = output_frame.getvalue()
        frames.append(frame_bytes)

    cap.release()

    return raw_frames, frames

def inference_img_by_api(
    raw_frame: np.ndarray,
    frame: bytes,
) -> Results:
    # Send the POST request to the API
    response = requests.post(
        API_URL,
        files={'file': frame},
    )

    # Parse the response json
    boxes_data = response.json()['boxes']
    boxes_data = torch.tensor(boxes_data, dtype=torch.float32)
    if boxes_data.ndim == 1:
        boxes_data = boxes_data.view(0, 6)

    # results in client
    result = Results(
        raw_frame,
        None,
        names=LABEL_NAMES,
        boxes=boxes_data,
    )

    return result

def main():
    # get frames
    raw_frames, frames = read_frames_from_video(VIDEO_NAME)
    frames_count = len(frames)

    t = time.time()
    i = 0
    while True:
        raw_frame = raw_frames[i]
        frame = frames[i]

        # inference by accessing API
        result = inference_img_by_api(raw_frame, frame)

        # draw the YOLO detection
        detected_image = result.plot()

        # display the detected frame and FPS
        current_fps = i / (time.time() - t + 0.00001)
        cv2.putText(detected_image, f'FPS: {current_fps: 6.2f}', (0, 25),
                    cv2.FONT_HERSHEY_SIMPLEX,1,  (50, 50, 255),
                    2, cv2.LINE_AA)
        cv2.imshow('YOLOv10 detect', detected_image)

        # Wait for 1ms or exit when press q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        i += 1
        if i >= frames_count:
            break

    total_time = time.time() - t + 0.00001
    print('FPS:', i / total_time)

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()