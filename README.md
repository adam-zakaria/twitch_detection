# Install local dependencies
pip install -e ~/Code/utils
pip install -e ~/Code/cliptu/backend/cliptu/

# OCR
## Paddle
* Does not work out of the box on MacOS m2 or Ubuntu (our GPU AMI)
* There are different packages for the CPU and GPU builds:
https://www.paddlepaddle.org.cn/documentation/docs/en/install/pip/linux-pip_en.html#installation

## Ubuntu (AWS)
Paddle's latest supported CUDA is 12.3, as detailed from the link below. We used ChatGPT to install 12.3: 
`sudo apt-get install -y cuda-toolkit-12-3`
I'm not sure we need the NVIDIA driver, but we might (specifically, the legacy one, needed by g4dnxl's T4 GPU)
`sudo apt-get install -y cuda-drivers`
From:
https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=22.04&target_type=deb_network

Then we can install paddle:
```
python3 -m pip install paddlepaddle-gpu==3.0.0b1 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/ paddleocr
```
From:
https://www.paddlepaddle.org.cn/documentation/docs/en/install/pip/linux-pip_en.html#span-id-gpu-gpu-version-of-paddlepaddle-span

## MacOS M2
* https://github.com/PaddlePaddle/PaddleOCR/discussions/13060?converting=1
Instructions from above are below:
```
python3 -m venv env
source ./env/bin/activate
python3 -m pip install "paddleocr>=2.6rc"
pip3 install paddlepaddle==0.0.0 -f https://www.paddlepaddle.org.cn/whl/mac/cpu/develop.html
```
Always source the activate before using the model.

## Tesseract works out of the box
* brew install tesseract
* tesseract /Users/azakaria/Code/halo_dk_detection/sample.png sample_ocr # outputs to sample_orc.txt, with the detection (successful)
* dk detection did not work
* Interested in applying a color match
* The white on the yellow white background is really hard to detect. However, I might've chosen bad frames, I want to try the duration of the medal and see if any detections are made.
* So let's try tesseract on the whole duration. Let's get even more than we need.

# Torch
I'm a little confused because nvcc is reporting 12.6, but I thought we installed 12.3 from above.

ubuntu@ip-172-31-75-23:~/Code/twitch_detection$ nvcc --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2024 NVIDIA Corporation
Built on Tue_Oct_29_23:50:19_PDT_2024
Cuda compilation tools, release 12.6, V12.6.85

Regardless, we installed libcudnn8 to do parallel frame processing with torch and it seems to be working.

ubuntu@ip-172-31-75-23:~/Code/twitch_detection$ sudo apt install libcudnn8 libcudnn8-dev

ubuntu@ip-172-31-75-23:~/Code/twitch_detection$ python -c "import torch; print(torch.cuda.is_available())"
True

# Preprocessing frame resize / Batch Processing
We've discovered that the frame resize operation takes about the same time as the ocr inference, and were hoping we could easily preprocess resize all the frames. We learned that decoded images are way bigger than there encoded size in the video so even a minute video that's 40mb can be gigabytes when they are decoded / decompressed frames. So we tried to batch process the frames. We tried 100, it crashed the gpu. We tried 1 and learned the tensor operation seems to be very slow. I'd think the next step would be trying 50 frames and see if it's worth it, but it's possible our approach is also just off.


# Style Decisions
We try to have explicit arguments for the pipeline functions to make them more reusable, testable, and modular. Inevitably, we will want to reuse, test or modify them elsewhere. It seems that explicit interfaces better enables this. This is worth explanation because inevitably I ask myself well if we know where everything will be written, why even have all this extra info and typing? Because code evolves and we reuse and modify it and that is a high priority. So yeah, we're not necessarily thinking of just this situation, but everything that is done in the life of the software.

# Experiments
## `compare_medal_cv.py`
Shows that the dk medal has slight transparency.

This tempts me to try a few approaches. All can likely benefit from preprocessing.
* Recognizing 'Double kill' (or close) (PaddleOCR) (OCR That specializes in noisy situations). Remember, text will be whitish.
* A fuzzy color approach, we should still be within some blue range. Could do the same iterated bb on the column. Could do experiments in photopea to see how the different bgs change the colors. Using the medals, and adding my own circle and background layers.
* Finetune YOLO with the ROIs
* Circle + stars general shape detection should be possible but unsure how - maybe return to template matching. Maybe template matching + ROI.

Creating embeddings (like text embeddings and semantic search) is an interesting idea but this seems like a large dataset kind of approach.

## `tesseract.py`
* With a 3 second sample clip which was difficult (white on yellow background) (dk on bazaar), a few frames detected at least  'dou'. Very promising! 
* Next we want to test this against the whole video and see if it gets all of them.
* working on extract.py

# Test video (clip)(zsh escaped) 'Lucid - Greatest Hits / Best Clips | Halo Infinite LAN':
yt-dlp -S vcodec:h265,acodec:aac "https://www.youtube.com/watch?v=Kl5QHzEwbLQ" --download-sections "*00:25-00:26"

# Current
* the clips are extracted properly, but the concat is not working.

# todo
* optimize speed - talk to gpt, can do a lot. skip frames, batch images, etc.
* on front upload twitch streams to s3, on front spawn gpu, on gpu download streams from s3 and upload concat.mp4