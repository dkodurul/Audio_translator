from gtts import gTTS
import os

class TextToSpeech:
    @staticmethod
    def convert_text_to_speech(text, output_file):
        try:
            # Initialize gTTS with the text, language set to Telugu ('te'), and slow set to False
            tts = gTTS(text=text, lang='te', slow=False)
            # Save the generated speech to an MP3 file
            tts.save(output_file)
            print(f"Audio saved to {output_file}")
        except Exception as e:
            print(f"Failed to convert text to speech: {e}")