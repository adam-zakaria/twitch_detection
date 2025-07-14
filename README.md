# Build
From project root
`poetry build`
creates:
dist/twitch_detections-0.1.0-py3-none-any.whl
dist/twitch_detections-0.1.0.tar.gz

# Install
`poetry install` (initiates a venv and installs the package)
or
`pip install -e .` (works from anywhere)

# Run
`poetry shell`
`pm2 start 'python subprocesses.py' --name 'subprocesses'`

# Add packages to project
poetry add <packages>