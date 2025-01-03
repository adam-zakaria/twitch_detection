import sys
import whisper
import os

def transcribe_audio(model_name, file_name):
     # Load the model
     model = whisper.load_model(model_name)

     # Transcribe the audio file
     result = model.transcribe(file_name)

     # Output the transcription
     print(result['text'])

if __name__ == "__main__":
     if len(sys.argv) != 3:
         print("Usage: python script.py <model>
 <audio_file>")
         sys.exit(1)

     # Take command-line arguments
     model_name = sys.argv[1]
     audio_file = sys.argv[2]

     # Transcribe the audio file
     transcribe_audio(model_name, audio_file)
