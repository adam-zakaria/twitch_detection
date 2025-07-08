#!/bin/bash
# Reuse an existing GPU instance instead of provisioning a new one

# Configurations
INSTANCE_ID="i-02a34bba08ac27886"  # Replace with your existing GPU instance ID
INSTANCE_IP="52.54.193.44" # Replace with your actual instance IP
SSH_USER="ubuntu"
KEY_PATH="~/.ssh/clip_micro.pem"
INSTANCE_NAME="gpu-instance"

echo "🚀 Checking instance state..."
INSTANCE_STATE=$(aws ec2 describe-instances \
  --instance-ids "$INSTANCE_ID" \
  --query 'Reservations[0].Instances[0].State.Name' \
  --output text)

if [[ "$INSTANCE_STATE" == "stopped" ]]; then
  echo "🔌 Starting instance..."
  aws ec2 start-instances --instance-ids "$INSTANCE_ID" --no-cli-pager
  echo "⏳ Waiting for instance to reach 'running' state..."
  aws ec2 wait instance-running --instance-ids "$INSTANCE_ID"
  echo "✅ Instance is now running."
elif [[ "$INSTANCE_STATE" == "running" ]]; then
  echo "✅ Instance is already running."
else
  echo "❌ Unexpected instance state: $INSTANCE_STATE. Exiting."
  exit 1
fi

echo "⏳ Waiting for instance status checks..."
aws ec2 wait instance-status-ok --instance-ids "$INSTANCE_ID"
echo "✅ Instance is fully initialized."

# Ensure the SSH alias is updated for the latest instance IP
echo -e "Host $INSTANCE_NAME\n  HostName $INSTANCE_IP\n  User $SSH_USER\n  IdentityFile $KEY_PATH\n  StrictHostKeyChecking no\n  UserKnownHostsFile=/dev/null\n" | cat - ~/.ssh/config > ~/.ssh/config.tmp && mv ~/.ssh/config.tmp ~/.ssh/config

# Run Python script remotely
echo "🚀 Running Python script on GPU instance..."
ssh "$INSTANCE_NAME" "rm -rf /home/ubuntu/Code/twitch_detection && git clone git@github.com:adam-zakaria/twitch_detection.git /home/ubuntu/Code/twitch_detection && cd /home/ubuntu/Code/twitch_detection/test/production && python gpu_process.py"

echo "🛑 Shutting down instance..."
aws ec2 stop-instances --instance-ids "$INSTANCE_ID" --no-cli-pager > /dev/null 2>&1
echo "✅ Instance has been powered down."

echo -e "\n🎯 All Done!"
