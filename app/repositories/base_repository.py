from app.database.db_manager import DatabaseManager
from app.utils.logger import SystemLogger
from bson import ObjectId

class BaseRepository:
    def __init__(self, collection_name):
        self.db = DatabaseManager().get_db()
        self.collection = self.db[collection_name]
        self.logger = SystemLogger.get_logger(self.__class__.__name__)

    def insert(self, document):
        return self.collection.insert_one(document).inserted_id

    def find_all(self, query=None): 
        return list(self.collection.find(query or {}))
        
    def find_paginated(self, query=None, skip=0, limit=10):
        return list(self.collection.find(query or {}).skip(skip).limit(limit))

    def find_by_id(self, doc_id):
        try:
            return self.collection.find_one({"_id": ObjectId(doc_id)})
        except:
            return None
            
    def update(self, doc_id, update_data):
        try:
            obj_id = ObjectId(str(doc_id).strip()) if not isinstance(doc_id, ObjectId) else doc_id
            return self.collection.update_one({"_id": obj_id}, {"$set": update_data})
        except Exception as e:
            self.logger.error(f"MongoDB Update Error for {doc_id}: {e}")
            raise e
        
    def delete(self, doc_id):
        return self.collection.delete_one({"_id": ObjectId(doc_id)})
    
    def count_docs(self, query=None): return self.collection.count_documents(query or {})