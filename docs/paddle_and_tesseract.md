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