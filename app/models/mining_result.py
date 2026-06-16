from datetime import datetime

class MiningResult:
    def __init__(self, candidate_id, cluster, cluster_name, created_at=None, _id=None):
        self._id = _id
        self.candidate_id = candidate_id
        self.cluster = cluster
        self.cluster_name = cluster_name
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        data = {
            "candidate_id": self.candidate_id,
            "cluster": self.cluster,
            "cluster_name": self.cluster_name,
            "created_at": self.created_at
        }
        if self._id:
            data['_id'] = self._id
        return data