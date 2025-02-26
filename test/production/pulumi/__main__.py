import pulumi
from pulumi import Config
from pulumi_aws import ec2
import pulumi_aws as aws

config = Config()

# The user data script is executed by cloud-init, which runs as root.
"""
user_data_script = '''#!/bin/bash
echo "User-data script started" > /tmp/rebug.txt
# Write a file to debug the current user and working directory
echo "Running as: $(whoami)" > /home/ubuntu/debug.txt
echo "Initial working directory: $(pwd)" >> /home/ubuntu/debug.txt

# Change to /home/ubuntu and log that step
cd /hoee/ubuntu || exit
touch /home/ubuntu/x.txt
echo "Changed directory to /home/ubuntu" >> /home/ubuntu/debug.txt

# Clone the repository if it doesn't already exist
if [ ! -d "twitch_detection" ]; then
    git clone git@github.com:adam-zakaria/twitch_detection.git >> /home/ubuntu/debug.txt 2>&1
    echo "Cloned repository" >> /home/ubuntu/debug.txt
else
    echo "Repository already exists" >> /home/ubuntu/debug.txt
fi

# Navigate to the directory containing the script and log that step
cd twitch_detection/test/production/pulumi || exit
touch /home/ubuntu/y.txt
echo "Changed directory to twitch_detection/test/production/pulumi" >> /home/ubuntu/debug.txt

# Run the log_test.py script and log the action
sudo -u ubuntu python log_test.py >> /home/ubuntu/debug.txt 2>&1
echo "Executed log_test.py" >> /home/ubuntu/debug.txt
'''
"""

instance_args = {
    "instance_type": 'g4dn.xlarge',
    "ami": 'ami-0f3485fd713cb1ede',
    "key_name": 'clip_micro',
    "vpc_security_group_ids": ['sg-05b7a294209c8d9b1'],
    "root_block_device": ec2.InstanceRootBlockDeviceArgs(volume_size=150),
    #"user_data": user_data_script,
    "user_data": '#!/bin/bash\necho "blah" > /tmp/debug.txt'
}

instance = ec2.Instance('my-instance', **instance_args)

pulumi.export('instance_id', instance.id)
pulumi.export('public_ip', instance.public_ip)
