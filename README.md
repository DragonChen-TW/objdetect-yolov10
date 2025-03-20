## run server

```shell
make server
```

## test by shell

```shell
curl -X 'POST' \
  'http://127.0.0.1:8000/predict/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@./imgs/office_parkour1.jpg' -o detect.jpg
```

## test by client.py
```shell
make client
```

## Try to speedup

Start from FPS around 18.

Some optimizations:
- disable default verbose in server
- add stream=True in server
- add `torch.comple`
Did not applied because my GPU of development environment is too old.  
`RuntimeError: Found NVIDIA GeForce GTX 1060 6GB which is too old to be supported by the triton GPU compiler, which is used as the backend. Triton only supports devices of CUDA Capability >= 7.0, but your device is of CUDA capability 6.1`
Could try another GPU card, colab or Cloud platform.
