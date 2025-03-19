# uv

```shell
# Install pipx through pip
pip install pipx

# Install uv through pipx
pipx install uv
```

# start project (first time only)
```shell
uv init PROJECT_NAME -p 3.10
uv venv
``

# add dependencies

```shell
# PyTorch
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

# HuggingFace
uv pip install transformers

# fastapi
uv add fastapi[standard]

# YOLOv10
uv add ultralytics
uv pip install git+https://github.com/THU-MIG/yolov10.git
```