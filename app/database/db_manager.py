from pymongo import MongoClient
from app.config.settings import Config
from app.utils.logger import SystemLogger

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.logger = SystemLogger.get_logger("DatabaseManager")
            try:
                cls._instance.client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
                cls._instance.db = cls._instance.client[Config.DB_NAME]
                cls._instance.logger.info("Kết nối MongoDB thành công.")
            except Exception as e:
                cls._instance.logger.error(f"Lỗi kết nối MongoDB: {e}")
                raise
        return cls._instance

    def get_db(self): return self.db