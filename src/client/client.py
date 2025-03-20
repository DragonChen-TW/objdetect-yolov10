from io import BytesIO
import time
from typing import List

import requests
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import simplejpeg as sjpg
import cv2

# Define the API URL
API_URL = 'http://127.0.0.1:8000/predict/'
VIDEO_NAME = 'media/Parkour PARKOUR - The Office US.mp4'

def read_frames_from_video(video_name: str) -> List[bytes]:
    cap = cv2.VideoCapture(video_name)

    # check whether the video files is opened correctly
    if not cap.isOpened():
        print('Error: Cannot open video file')

    # read all frames out
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # convert to jpg by Pillow
        frame = Image.fromarray(frame)
        output_frame = BytesIO()
        frame.save(output_frame, format='JPEG')
        output_frame = output_frame.getvalue()
        frames.append(output_frame)

    cap.release()

    return frames

def inference_img_by_api(frame: bytes) -> np.ndarray:
    # Send the POST request to the API
    response = requests.post(
        API_URL,
        files={'file': frame},
    )
    # # Parse the response image
    # detected_frame = sjpg.decode_jpeg(response.content)

    res_content = BytesIO(response.content)
    detected_frame = Image.open(res_content)
    detected_frame = np.array(detected_frame)

    return detected_frame

def main():
    frames = read_frames_from_video(VIDEO_NAME)
    frames_count = len(frames)

    t = time.time()
    i = 0
    while True:
        frame = frames[i]

        detected_frame = inference_img_by_api(frame)

        # Show the detected frame from server's YOLOv10
        cv2.imshow('YOLOv10 detect', detected_frame)
        
        # Wait for 1ms or exit when press q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        i += 1
        if i >= frames_count:
            break

    total_time = time.time() - t
    print('FPS:', frames_count / total_time)

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()