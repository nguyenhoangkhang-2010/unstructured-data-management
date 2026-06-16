import re
import unicodedata
from underthesea import word_tokenize
from app.utils.logger import SystemLogger

class TextPreprocessor:
    def __init__(self):
        self.logger = SystemLogger.get_logger(self.__class__.__name__)

        self.vi_stopwords = {
            "và", "là", "của", "các", "có", "trong",
            "để", "một", "với", "cho", "được", "những"
        }

        self.en_stopwords = {
            "the", "a", "an", "is", "are", "was", "were",
            "of", "to", "for", "in", "on", "at", "by",
            "with", "from", "and", "or", "that", "this"
        }

        self.stopwords = self.vi_stopwords.union(self.en_stopwords)

    def clean(self, text):
        try:
            if not isinstance(text, str):
                return ""
            text = text.lower()
            text = re.sub(r'<.*?>', ' ', text)
            text = re.sub(r'http[s]?://\S+', ' ', text)
            text = re.sub(r'\S+@\S+', ' ', text)
            text = re.sub(r'\d+', ' ', text)
            text = re.sub(r'[^\w\s]', ' ', text)
            text = unicodedata.normalize("NFC", text)
            text = re.sub(r'\s+', ' ', text).strip()
            text = word_tokenize(text, format="text")
            tokens = text.split()
            tokens = [
                token
                for token in tokens
                if token not in self.stopwords
                and len(token) > 1
            ]

            return " ".join(tokens).replace("_", " ")

        except Exception as e:
            self.logger.error(f"Lỗi tiền xử lý: {e}")
            return ""