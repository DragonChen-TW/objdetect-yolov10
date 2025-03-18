# uv

- Install pipx through pip
`pip install pipx`
- Install uv through pipx
`pipx install uv`

# start project (first time only)
`uv init PROJECT_NAME -p 3.10`
``

# add dependencies

- PyTorch
Add below block to `pyproject.toml`
```yaml
[[tool.uv.index]]
name = "pytorch-cu126"
url = "https://download.pytorch.org/whl/cu126"
explicit = true

[tool.uv.sources]
torch = [
  { index = "pytorch-cu126", marker = "sys_platform == 'linux' or sys_platform == 'win32'" },
]
torchvision = [
  { index = "pytorch-cu126", marker = "sys_platform == 'linux' or sys_platform == 'win32'" },
]
```