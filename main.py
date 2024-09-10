import os
from folder_manager import FolderManager
from audio_converter import AudioConverter
from audio_chunker import AudioChunker
from audio_recognizer import AudioRecognizer
from translator_module import TextTranslator
from text_to_speech import TextToSpeech
from text_saver import TextSaver

def main(mp3_file_path):
    base_file_name = os.path.splitext(os.path.basename(mp3_file_path))[0]
    output_folder = FolderManager.create_output_folder(base_file_name)

    wav_file_path = os.path.join(output_folder, 'converted_audio.wav')
    AudioConverter.convert_mp3_to_wav(mp3_file_path, wav_file_path)

    chunk_paths = AudioChunker.chunk_audio(wav_file_path, output_folder)

    recognizer = AudioRecognizer(language='en')
    translator = TextTranslator(source_language='en', target_language='te')

    combined_text = ""
    for chunk_path in chunk_paths:
        recognized_text = recognizer.recognize_speech(chunk_path)
        if recognized_text:
            combined_text += recognized_text + " "
    
    if combined_text.strip():
        TextSaver.save_text_files(combined_text, "", output_folder)

        translated_text = translator.translate_text(combined_text)
        if translated_text:
            TextSaver.save_text_files("", translated_text, output_folder)
            TextToSpeech.convert_text_to_speech(translated_text, os.path.join(output_folder, 'translated_speech.mp3'))

    FolderManager.clean_up(output_folder)

if __name__ == "__main__":
    main('C:/Users/dkodurul_stu/WIP-Projects/sample.mp3')