from datetime import datetime
from bson import ObjectId

class Application:
    def __init__(self, candidate_id, job_id, status="Pending", apply_date=None, _id=None):
        self._id = _id
        self.candidate_id = candidate_id
        self.job_id = job_id
        self.status = status
        self.apply_date = apply_date or datetime.now()

    def to_dict(self):
        data = {
            "candidate_id": ObjectId(self.candidate_id) if isinstance(self.candidate_id, str) else self.candidate_id,
            "job_id": ObjectId(self.job_id) if isinstance(self.job_id, str) else self.job_id,
            "status": self.status,
            "apply_date": self.apply_date
        }
        if self._id:
            data['_id'] = self._id
        return data

    @classmethod
    def from_dict(cls, data):
        if not data: return None
        return cls(
            _id=data.get('_id'),
            candidate_id=data.get('candidate_id'),
            job_id=data.get('job_id'),
            status=data.get('status', 'Pending'),
            apply_date=data.get('apply_date')
        )