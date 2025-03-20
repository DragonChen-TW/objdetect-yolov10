# Object Detection - yolov10

## installation

This project use `uv` to manage Python version, pakcage dependencies and virtual environment.  
Yes, `uv` is the replacement of `pyenv`, `pip` and `venv`.

### install uv

```shell
# Install pipx through pip
pip install pipx

# Install uv through pipx
pipx install uv
```

So, what is the next? No, you are ready to run server/client.

`uv` will automatically create `venv`, donwload packages when you run `uv run SCRIPT.py`. And, that is blazing fast.

## run server

```shell
make server
# or in development
make dev
```

## test by shell

It will read and send one local jpg file to our server to get the result of object detection.

```shell
curl -X 'POST' \
  'http://127.0.0.1:8000/predict/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@./data/office_parkour1.jpg' -o detect.json
```

## test by client.py

It will get all the frames in given video file (`data/Parkour...mp4 there), and send them to server to do inference one by one. Then, it will open cv2 to stream these frames were detection by YOLOv10.

I only cut ~13 seconds out from the original video. About 400 frames under 30 FPS.

```shell
make client
```

## Try to speedup

Start from FPS around 18.

Some optimizations:
- try differnt compression package to minimize the size of jpg (use `simplejpeg` there)
- disable default verbose in server
- add stream=True in server
- add `torch.comple`
Did not applied because my GPU of development environment is too old.  
`RuntimeError: Found NVIDIA GeForce GTX 1060 6GB which is too old to be supported by the triton GPU compiler, which is used as the backend.`  
Could try another GPU card, colab or Cloud platform.

**Improve to around 21**

- only return information of bounding boxes instead the whole jpg.
**Improve to around 25 FPS**
- truncate the length of message (about half)
**Improve to around 28 FPS**

There is a cap of 30 FPS because that is the FPS of the original video.

At the final setting, YOLOv10m runs with 21 FPS, and YOLOv10l go with 17 FPS. 