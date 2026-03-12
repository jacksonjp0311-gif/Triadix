python -m pip install --upgrade pip
pip install -e .[dev]
pytest -q
triadix run --blocks 12