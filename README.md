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
* Couldn't get paddle to work on mac m2
* tesseract works out of the box
    * brew install tesseract
    * tesseract /Users/azakaria/Code/halo_dk_detection/sample.png sample_ocr # outputs to sample_orc.txt, with the detection (successful)
    * dk detection did not work
    * Interested in applying a color match
    * The white on the yellow white background is really hard to detect. However, I might've chosen bad frames, I want to try the duration of the medal and see if any detections are made.
    * So let's try tesseract on the whole duration. Let's get even more than we need.
# Current
* time_range is working: tested in time range, out of time range. there are a lot of ways it can be messed up though. It's hard to come up with a test case. we want a detection...maybe between 5-6AM we run the rest? i.e. 
python main.py detect && python main.py filter_and_extract && python main.py concat
I'm at least partially suspicious of this time based approach..let's try it. And we'll do small test cases. i.e. we can do it for an hour. we can also do it 1 minute to evaluate what happens (i.e. confirm good prints happen)
download 08:00-04:00 
detect, extract, concat, post, 4:01

So maybe this needs a main loop which decides what to do depending on what it is?
