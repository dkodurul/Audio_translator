import os
from pydub import AudioSegment

class AudioChunker:
    @staticmethod
    def chunk_audio(wav_file_path, output_folder, chunk_length_ms=60000):
        audio = AudioSegment.from_wav(wav_file_path)
        chunk_paths = []
        for i in range(0, len(audio), chunk_length_ms):
            chunk = audio[i:i + chunk_length_ms]
            chunk_path = os.path.join(output_folder, f"chunk_{i // chunk_length_ms}.wav")
            chunk.export(chunk_path, format="wav")
            chunk_paths.append(chunk_path)
        return chunk_paths