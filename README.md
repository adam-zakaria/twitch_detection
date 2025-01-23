# Install local dependencies
pip install -e /Users/azakaria/Code/utils
pip install -e ~/Code/cliptu/backend/cliptu/

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

# OCR
## Paddle
* Does not work out of the box
* https://github.com/PaddlePaddle/PaddleOCR/discussions/13060?converting=1
* Did the following and it works
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

# Current
* Get .ssh/config, .aws onto linux
* Run the full thing on aws gpu, see what happens. Also, could do detections on gpu but download on non gpu.
* Also, this is only double kills, so we'd want to do more. Also let's find a way to be excited about this instead of feeling very drained by it. Let's do a diagram!
