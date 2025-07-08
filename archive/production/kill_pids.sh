#!/bin/bash
# Script: kill_twitch.sh
# Description: Kills all processes whose command lines contain "twitch"

# List processes matching "twitch", exclude the grep process itself,
# then extract the second field (PID) using awk.
pids=$(ps aux | grep twitch | grep -v grep | awk '{print $2}')

# Check if any PIDs were found
if [ -z "$pids" ]; then
    echo "No processes containing 'twitch' found."
    exit 0
fi

echo "Killing the following PIDs:"
echo "$pids"

# Kill each process with SIGKILL (-9)
for pid in $pids; do
    kill -9 "$pid" && echo "Killed PID $pid" || echo "Failed to kill PID $pid"
done
