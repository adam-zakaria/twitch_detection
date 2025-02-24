# Useful commands
pulumi up --stack dev --yes
pulumi destroy --stack dev --yes
pulumi stack rm dev --force --yes # Do not delete underlying resources


# General
Currently, a single instance is created at once. The AWS account has the quota set for 2 right now I believe. If any instance already exists and pulumi up --stack dev --yes is run, the new instance gets created before the old one is delete, so even if the old one takes a while to delete, the new one will be created.

     pulumi:pulumi:Stack             pulumi-ec2-project-dev                       
 +   ├─ aws:ec2:SecurityGroup        gpu-spot-security-group  created (2s)        
 +   ├─ aws:ec2:SpotInstanceRequest  gpu-spot-instance        created (11s)       
 -   ├─ aws:ec2:Instance             my-instance              deleted (272s)      
 -   ├─ aws:ec2:SecurityGroup        my-security-group        deleted (0.74s)     
 -   └─ pulumi:providers:aws         aws-provider             deleted (0.30s)   

Also, I believe the initial process channels takes a while to start up because models need to be downloaded.

# Install
## Pulumi globally
`curl -fsSL https://get.pulumi.com | sh; exec $SHELL`
## Pulumi SDK
`pip install pulumi`

# Login
The access token is in the access_token.txt file

# Run
`pulumi up --stack dev --yes`

# Errors
Pulumi may error with messages related uninstalled packages or python version. 
Try removing the venv folder in the project root and re-running the pulumi up command. It will recreate the venv with the current python version. To create the venv pulumi will use requirements.txt so it must be update with any missing packages, i.e.
pulumi>=3.0.0,<4.0.0
pulumi_aws

# Behavior
Pulumi will shut down the current GPU instance and create a new one, though I'm not sure if it's a spot instance....

# Spot pricing
Modify the spot_price variable in the __main__.py file to change the price.

# Organizing this for multiple machines
The initial try of doing this didn't work perfectly, but cursor tried to make it a little more complicated than necessary by trying not to reuse code and splitting it into multiple files and importing. We might instead want to just have separate files for each config and we could test them individually.

# To delete an AMI
Must unregister the AMI and delete the snapshot.

curl https://pyenv.run | bash

# Add to bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

# restart shell
exec "$SHELL"

pyenv install 3.13-dev

rsync ~/.ssh/id_ed25519* gpu:~/.ssh/
GIT_SSH_COMMAND='ssh -o StrictHostKeyChecking=no' git clone git@github.com:adam-zakaria/cliptu.git
cd cliptu
git submodule update --init

pyenv global 3.13-dev
pi boto3 requests psutil bs4 pyannote.audio torchaudio ffmpeg-python

flask flask-cors requests ffmpeg boto3 elasticsearch requests_aws4auth

One problem is that the branches are detatched when checked out.
I need to fix the branches..

# install elastic / kibana
## kibana
follow instructions here
https://www.elastic.co/guide/en/kibana/current/deb.html
add 5601 to the inbound security rule on aws 
sudo vi /etc/kibana/kibana.yml
server.host: "0.0.0.0"
control with systemctl

## elastic
i think defaults work...the code to connect is in test_es
I needed to do some disable verify certs and use credentials that i generated with some elastic reset creds


## generate creds / tokens
use the binaries in /usr/share/{kibana, elasticsearch}
sudo ./elasticsearch-create-enrollment-token --scope kibana
and for kibana verification look at the bottom of journalctl -u kibana 
the binary to get the verification token isn't working, but can be found in the logs

## kibana creds
elastic
Qcq_h+10MBmO78Y-ncu9

# More useful commands
## monitor gpu usage
watch -n 1 nvidia-smi

## this works but would require not exceeding the spot instance quota
ubuntu@ip-172-31-70-41:~/cliptu/pulumi$ pulumi up --replace urn:pulumi:dev::pulumi-ec2-project::aws:ec2/spotInstanceRequest:SpotInstanceRequest::gpu-spot-instance --yes

# CUDA, getting it working
Install python 3.11 with torch==2.3.0

faster-whisper requires cuDNN 8 for CUDA 12 and python 3.12 and torch 2.4.0 are cuDNN 9.

## Install cuda drivers and libs
sudo apt-get install -y cuda-drivers
sudo apt-get -y install cuda-toolkit

## Check directories for cuda files

## fix error where faster-whisper can't find cuda lib
export LD_LIBRARY_PATH=`python3 -c 'import os; import nvidia.cublas.lib; import nvidia.cudnn.lib; import torch; print(os.path.dirname(nvidia.cublas.lib.__file__) + ":" + os.path.dirname(nvidia.cudnn.lib.__file__) + ":" + os.path.dirname(torch.__file__) +"/lib")'`

## check gpus available
python3 -c "import torch; print(torch.cuda.device_count())"

## check for cuda files
* Cuda will install to:
/usr/local/cuda* 
(cuda, cuda-12, cuda-12.5), 

Installing cuda-drivers will install files like
* ubuntu@ip-172-31-80-34:~$ ls /usr/lib/x86_64-linux-gnu/libcuda.so
/usr/lib/x86_64-linux-gnu/libcuda.so
* nvidia-smi
The full list is on gpt4o
It does not include /usr/local/cuda*

cuda-toolkit will installl /usr/local/cuda*
but even after installing cuda-drivers and cuda-toolkit, the nvidia py module is not installed.

pyenv and py packages didn't install through pulumi, for some reason.

## nvcc 
* nvcc is the cuda compiler (it compiles programs that use cuda, i.e. it is absolutely necessary for GPU usage)

## installing torch 
installing torch installs the cudnn library. It's possible that the version of torch got upgraded, so really seems to be the problem, though it's not clear why. So torch installs nvidia.cudnn which includes libcudnn.so.9 but faster-whisper looks for libcudnn.so.8, maybe because my cuda library would suggest using 8? If I use python 10 I wonder if it'd make a difference.

so pytorch ships with its own cuda libs, i.e. cudnn, and faster whisper requires:
cuBLAS for CUDA 12
cuDNN 8 for CUDA 12

So maybe I just need to downgrade torch? But then will it work with my cuda? Maybe I won't use faster whisper for now.


## from online
Your locally installed CUDA toolkit won’t be used unless you build PyTorch from source or a custom CUDA extension since the PyTorch binaries ship with its own CUDA dependencies.

# Work Journal
## 8/23/2024, Decrease instance stop and start time: debug the security group hanging
Upon starting a new instance, the resource gets created, but the security group deletion of previous instance hangs.

Resources:
    + 3 to create
    - 2 to delete
    5 changes. 1 unchanged

Updating (dev)

View in Browser (Ctrl+O): https://app.pulumi.com/adam-zakaria/pulumi-ec2-project/dev/updates/56

     Type                            Name                     Status              
     pulumi:pulumi:Stack             pulumi-ec2-project-dev   running.            
 +   ├─ pulumi:providers:aws         aws-provider             created (1s)        
 +   ├─ aws:ec2:SecurityGroup        my-security-group        created (3s)        
 +   ├─ aws:ec2:Instance             my-instance              created (14s)       
 -   ├─ aws:ec2:SpotInstanceRequest  gpu-spot-instance        deleted (0.41s)     
 -   └─ aws:ec2:SecurityGroup        gpu-spot-security-group  deleting (71s)      
