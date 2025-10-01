# Build
`poetry build`
creates:
dist/twitch_detections-0.1.0-py3-none-any.whl
dist/twitch_detections-0.1.0.tar.gz

# Install
`poetry install` Installs project dependencies
`pip install -e .` Installs the project itself

# Run
`source /Users/azakaria/Library/Caches/pypoetry/virtualenvs/twitch-detections-UsLtH0Yo-py3.13/bin/activate`
`pm2 start 'python -u schedule_events.py' --name 'twitch'`

# Add packages to project
`poetry add <packages>`

# Launch venv
`source /home/ubuntu/.cache/pypoetry/virtualenvs/twitch-detections-0p2BiuAg-py3.13/bin/activate`

# Additional commands
`pm2 flush`
`tail -n 100000 /home/ubuntu/.pm2/logs/twitch-out.log`