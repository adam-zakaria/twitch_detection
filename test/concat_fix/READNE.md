# FFMPEG versions
We were on ffmpeg 4.4.2 (Ubuntu) but the latest is 7.1 so we want to update.

The issue is im on an older Ubuntu

Looking at the packages I see the latest ffmpeg on ubuntu is actually the latest ffmpeg publishes
7:7.1-3ubuntu3

but for my OS (I think ubuntu 22) we are only only 4.4.2
7:4.4.2-0ubuntu0.22.04.1	

source docs: https://launchpad.net/ubuntu/+source/ffmpeg

We were able to build 7.1 from source. Unfortunately, GPU support turned out to be a pain - see below.

# GPU support
This is a little complicated.

For GPU accelerated reencoding, ffmpeg using NVENC - NVIDIA Encoding (library). NVENC versions are tied to GPUs. Tesla T4 supports up to NVENC 12.1, but the latest FFMPEG (7.1) expects 13. We tried to reinstall an ffmpeg version that expects 12.1, but it's being a pain in the ass. 

Furthermore, it's not even definite that GPU acceleration will really help us. By default, it encodes a lot faster with much lower quality. This aligns with its intent to be used for real time encoding. Chatgpt says it can be tuned to have near indistinguishable quality, but still fast, but given how much a pita this has been, we're going to put it away for now and revisit if we need the speed.