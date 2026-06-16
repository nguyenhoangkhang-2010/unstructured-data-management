from app.utils.logger import SystemLogger

class AudioProcessor:
    def __init__(self):
        self.logger = SystemLogger.get_logger(self.__class__.__name__)

    def speech_to_text(self, audio_path):
        if not audio_path: return ""
        self.logger.info(f"Mock Speech-to-Text: {audio_path}")
        return "Transcript: Giao tiếp tốt, tư duy phân tích hệ thống rõ ràng."