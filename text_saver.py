import os

class TextSaver:
    @staticmethod
    def save_text_files(transcribed_text, translated_text, output_folder):
        transcribed_file_path = os.path.join(output_folder, 'transcribed_text.txt')
        translated_file_path = os.path.join(output_folder, 'translated_text.txt')
        
        if transcribed_text.strip():
            with open(transcribed_file_path, 'w', encoding='utf-8') as f:
                f.write(transcribed_text)
        
        if translated_text.strip():
            with open(translated_file_path, 'w', encoding='utf-8') as f:
                f.write(translated_text)