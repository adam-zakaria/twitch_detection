import pulumi
from pulumi import Config
from pulumi_aws import ec2
import pulumi_aws as aws

# Load the configuration
config = Config()

instance_args = {
    "instance_type": 'g4dn.xlarge',
    "ami": 'ami-0f3485fd713cb1ede',
    "key_name": 'clip_micro',
    "vpc_security_group_ids": ['sg-05b7a294209c8d9b1'],
    "root_block_device": ec2.InstanceRootBlockDeviceArgs(volume_size=64),
}

# Create the instance
instance = ec2.Instance('my-instance', **instance_args)

# Export the instance's ID and public IP
pulumi.export('instance_id', instance.id)
pulumi.export('public_ip', instance.public_ip)
