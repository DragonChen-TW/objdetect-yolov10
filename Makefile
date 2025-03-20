.PHONY: dev server client uv
default: dev
dev:
	uv run fastapi dev src/server/main.py
server:
	uv run fastapi run src/server/main.py
client:
	uv run src/client/client.py
uv:
	# "==========uv syncing......=========="
	uv sync
	# "==========uv locking......=========="
	uv lock
	# "==========making requirements.txt......=========="
	uv pip freeze > requirements.txt
