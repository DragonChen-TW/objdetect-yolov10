import requests
from PIL import Image
# import io
import matplotlib.pyplot as plt
# import json
import simplejpeg as sjpg

# Define the API URL
url = 'http://127.0.0.1:8000/predict/'

# Read the image file
image_paths = [f'imgs/office_parkour{i}.jpg' for i in range(1, 11)]
image_path = image_paths[0]

with open(image_path, 'rb') as f:
    files = {'file': f}
    
    # Send the POST request to the API
    response = requests.post(url, files=files)

# Parse the response image
img = sjpg.decode_jpeg(response.content)

# Show the image with bounding boxes
plt.imshow(img)
plt.axis('off')  # Turn off axis
plt.show()
