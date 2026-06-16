from app.utils.logger import SystemLogger

class OCREngine:
    def __init__(self):
        self.logger = SystemLogger.get_logger(self.__class__.__name__)

    def extract_text(self, image_path):
        self.logger.info(f"Mock OCR Extraction cho: {image_path}")
        if not image_path:
            return ""
        
        # Mock data trả về khi chưa cấu hình pytesseract binary
        return "OCR Extracted Data: Kỹ năng Python, MongoDB, Machine Learning (Mock)."