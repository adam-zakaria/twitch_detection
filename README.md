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
`pm2 start 'python -u main.py' --name 'twitch'`

# Add packages to project
poetry add <packages>

# Additional commands
`pm2 flush`

# Thoughts
The job start time can b inferred fom the file naem, the time is in the filename.

1157, so the job processing should start at 1257.
if the pm2 logs could be cleared for each start that could be good.