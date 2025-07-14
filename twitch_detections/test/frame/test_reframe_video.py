#from twitch_detections.frame import reframe_video
import twitch_detections.frame as frame


if __name__ == "__main__":
    input_path = '../../videos/lucid_1s.webm'
    output_dir = 'lucid_1s_reframe'
    ROI = (100, 100, 100, 100)
    frame.reframe_video(input_path=input_path, output_dir=output_dir, x=ROI[0], y=ROI[1], w=ROI[2], h=ROI[3])