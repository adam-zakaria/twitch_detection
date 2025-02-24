import pulumi
from pulumi_aws import ec2

# Create a new security group
security_group = ec2.SecurityGroup('gpu-spot-security-group',
                                   description='Allow HTTP and SSH',
                                   ingress=[
                                       {'protocol': 'tcp', 'from_port': 22, 'to_port': 22, 'cidr_blocks': ['0.0.0.0/0']},
                                       {'protocol': 'tcp', 'from_port': 80, 'to_port': 80, 'cidr_blocks': ['0.0.0.0/0']}
                                   ],
                                   egress=[
                                       {'protocol': '-1', 'from_port': 0, 'to_port': 0, 'cidr_blocks': ['0.0.0.0/0']},
                                   ])

# Define the EC2 spot instance with the security group attached
spot_instance_request = ec2.SpotInstanceRequest('gpu-spot-instance',
    instance_type='g4dn.2xlarge',
    # Ubuntu 22.04, my custom ami
    #ami='ami-0fe1ad41646b09845',
    # Ubuntu 22.04
    ami='ami-07d9b9ddc6cd8dd30', 
    key_name='clip_micro',
    vpc_security_group_ids=[security_group.id],
    spot_price='0.5',  # Set your maximum spot price
    wait_for_fulfillment=True,
    root_block_device=ec2.InstanceRootBlockDeviceArgs(
        volume_size=64
    ),
    user_data=f"""#!/bin/bash
rsync ~/.zshrc gpu:~/.bashrc
# Update and install necessary packages
sudo apt update && sudo apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev git libsndfile1 unzip \
xclip ffmpeg nodejs npm

# unable to locate package python-openssl
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

#######
# everything to here installed successfully
#######

# Setup for pyenv and Python installation, assumes pyenv init in bashrc
curl https://pyenv.run | bash
pyenv install 3.12
pyenv global 3.12

python -m pip install torch==2.3.0 numpy requests ffmpeg boto3 elasticsearch requests_aws4auth psutil bs4 pyannote.audio torchaudio ffmpeg-python openai-whisper faster-whisper yt-dlp

# Clone the specified repository and initialize submodules
# GIT_SSH_COMMAND='ssh -o StrictHostKeyChecking=no' git clone git@github.com:adam-zakaria/cliptu.git cliptu
# cd cliptu
# git submodule update --init

# Prepare .aws directory for credentials
cd ~/.aws
rsync credentials gpu:~/.aws/

# Install drivers from here
# https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=20.04&target_type=deb_local
# driver installer + driver installer (legacy installer)
# but probably just use an ami with packages preinstalled

# TODO: add this to the bashrc
# really...just rsync the .bashrc
export CUDA_VISIBLE_DEVICES=0

export LD_LIBRARY_PATH=`python3 -c 'import os; import nvidia.cublas.lib; import nvidia.cudnn.lib; import torch; print(os.path.dirname(nvidia.cublas.lib.__file__) + ":" + os.path.dirname(nvidia.cudnn.lib.__file__) + ":" + os.path.dirname(torch.__file__) +"/lib")'`
""")

# Export the instance's ID and public IP
pulumi.export('spot_instance_id', spot_instance_request.spot_instance_id)
pulumi.export('public_ip', spot_instance_request.public_ip)