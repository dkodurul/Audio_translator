import speech_recognition as sr

class AudioRecognizer:
    def __init__(self, language='en'):
        self.recognizer = sr.Recognizer()
        self.language = language

    def recognize_speech(self, audio_file):
        with sr.AudioFile(audio_file) as source:
            audio = self.recognizer.record(source)
            try:
                text = self.recognizer.recognize_google(audio, language=self.language)
                print(f"Recognized text from {audio_file}: {text}")  # Debug print
                return text
            except sr.UnknownValueError:
                print(f"Could not understand audio from {audio_file}")
                return None
            except sr.RequestError as e:
                print(f"Could not request results from {audio_file}; {e}")
                return None