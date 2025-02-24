import pulumi
from pulumi import Config
from pulumi_aws import ec2
import pulumi_aws as aws

# Load the configuration
config = Config()

# Define the EC2 instance arguments
instance_args = {
    "instance_type": 't4g.medium',
    "ami": 'ami-0b512064c274bdd4e',
    "key_name": 'clip_micro',
    "availability_zone": 'us-east-1a',
    "root_block_device": ec2.InstanceRootBlockDeviceArgs(volume_size=64)
}

# Create the instance
instance = ec2.Instance('my-instance', **instance_args)

# Export the instance's ID and public IP
pulumi.export('instance_id', instance.id)
pulumi.export('public_ip', instance.public_ip)
