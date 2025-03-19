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