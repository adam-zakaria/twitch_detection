import pulumi
from pulumi import Config
from pulumi_aws import ec2
import pulumi_aws as aws

"""
This is used to spin up a g4dn xl gpu server
"""


# Load the configuration
config = Config()
#instance_type_config = config.require("instance_type")  # "spot" or "ondemand"

# Create a new security group
security_group = ec2.SecurityGroup('my-security-group',
                                   description='Allow HTTP and SSH',
                                   ingress=[
                                       {'protocol': 'tcp', 'from_port': 22, 'to_port': 22, 'cidr_blocks': ['0.0.0.0/0']},
                                       {'protocol': 'tcp', 'from_port': 80, 'to_port': 80, 'cidr_blocks': ['0.0.0.0/0']}
                                   ],
                                   egress=[
                                       {'protocol': '-1', 'from_port': 0, 'to_port': 0, 'cidr_blocks': ['0.0.0.0/0']},
                                   ])

# Define the EC2 instance arguments
instance_args = {
    "instance_type": 'g4dn.xlarge',
    #"ami": 'ami-07d9b9ddc6cd8dd30',
    "ami": 'ami-0fe1ad41646b09845',
    "key_name": 'clip_micro',
    "vpc_security_group_ids": [security_group.id],
    "root_block_device": ec2.InstanceRootBlockDeviceArgs(volume_size=64),
}

# Create the instance
#instance = ec2.Instance('my-instance', **instance_args)
instance = ec2.Instance('my-instance',
                        **instance_args,
                        opts=pulumi.ResourceOptions(provider=aws.Provider("aws-provider", region="us-east-1")))

# Export the instance's ID and public IP
pulumi.export('instance_id', instance.id)
pulumi.export('public_ip', instance.public_ip)
