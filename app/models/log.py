from datetime import datetime

class Log:
    def __init__(self, user_action, entity_type, metadata=None, timestamp=None, _id=None):
        self._id = _id
        self.user_action = user_action
        self.entity_type = entity_type
        self.metadata = metadata or {}
        self.timestamp = timestamp or datetime.now()

    def to_dict(self):
        data = {
            "user_action": self.user_action,
            "entity_type": self.entity_type,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }
        if self._id:
            data['_id'] = self._id
        return data