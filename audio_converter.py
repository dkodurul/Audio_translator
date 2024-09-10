from pydub import AudioSegment

class AudioConverter:
    @staticmethod
    def convert_mp3_to_wav(mp3_file_path, wav_file_path):
        audio = AudioSegment.from_mp3(mp3_file_path)
        audio.export(wav_file_path, format="wav")