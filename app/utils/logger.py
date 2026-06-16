import logging
import sys

class SystemLogger:
    @staticmethod
    def get_logger(name):
        logger = logging.getLogger(name)
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

class LogService:
    @staticmethod
    def write_log(user_action, entity_type, metadata=None):
        logger = SystemLogger.get_logger("LogService")
        try:
            from app.repositories.base_repository import BaseRepository
            from app.models.log import Log
            repo = BaseRepository("logs")
            log_entry = Log(user_action=user_action, entity_type=entity_type, metadata=metadata)
            repo.insert(log_entry.to_dict())
        except Exception as e:
            logger.error(f"Failed to write log to MongoDB: {e}")