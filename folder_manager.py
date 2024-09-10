import os
import shutil

class FolderManager:
    @staticmethod
    def create_output_folder(file_name):
        new_folder_name = f'output_{file_name}'
        os.makedirs(new_folder_name, exist_ok=True)
        return new_folder_name
    
    @staticmethod
    def clean_up(folder_path):
        files_to_keep = ['transcribed_text.txt', 'translated_text.txt', 'translated_speech.mp3']
        for filename in os.listdir(folder_path):
            if filename not in files_to_keep:
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                    else:
                        os.remove(file_path)
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")