.PHONY: server client uv
default: server
server:
	uv run fastapi dev src/server/main.py
client:
	uv run src/client/client.py
uv:
	# "==========uv syncing......=========="
	uv sync
	# "==========uv locking......=========="
	uv lock
	# "==========making requirements.txt......=========="
	uv pip freeze > requirements.txt
