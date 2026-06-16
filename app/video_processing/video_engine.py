from app.utils.logger import SystemLogger

class VideoProcessor:
    def __init__(self):
        self.logger = SystemLogger.get_logger(self.__class__.__name__)

    def process_video(self, video_path):
        if not video_path: return ""
        self.logger.info(f"Mock Video Analysis: {video_path}")
        return "Video Metadata: Confident posture, clear speaking voice."