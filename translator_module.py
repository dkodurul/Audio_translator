from googletrans import Translator

class TextTranslator:
    def __init__(self, source_language='en', target_language='te'):
        self.translator = Translator()
        self.source_language = source_language
        self.target_language = target_language

    def translate_text(self, text):
        try:
            translated = self.translator.translate(text, src=self.source_language, dest=self.target_language)
            return translated.text
        except Exception as e:
            print(f"Translation failed: {e}")
            return None
