import pulumi
from pulumi import Config
from pulumi_aws import ec2
import pulumi_aws as aws

# Load the configuration
config = Config()

user_data_script =     """
git clone git@github.com:adam-zakaria/twitch_detection.git

# Navigate to the directory containing the script
cd twitch_detection/test/production/pulumi

# Run the log_test.py script
python log_test.py
"""

instance_args = {
    "instance_type": 'g4dn.xlarge',
    "ami": 'ami-0f3485fd713cb1ede',
    "key_name": 'clip_micro',
    "vpc_security_group_ids": ['sg-05b7a294209c8d9b1'],
    "root_block_device": ec2.InstanceRootBlockDeviceArgs(volume_size=64),
    "user_data": user_data_script,  # This script runs on instance boot.

}

# Create the instance
instance = ec2.Instance('my-instance', **instance_args)

# Export the instance's ID and public IP
pulumi.export('instance_id', instance.id)
pulumi.export('public_ip', instance.public_ip)
