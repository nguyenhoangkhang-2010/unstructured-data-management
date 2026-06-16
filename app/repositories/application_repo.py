from app.repositories.base_repository import BaseRepository
from app.models.application import Application

class ApplicationRepository(BaseRepository):
    def __init__(self):
        super().__init__("applications")

    def get_all_applications_with_details(self):
        pipeline = [
            {
                '$lookup': {'from': 'candidates', 'localField': 'candidate_id', 'foreignField': '_id', 'as': 'candidate_info'}
            },
            {
                '$lookup': {'from': 'jobs', 'localField': 'job_id', 'foreignField': '_id', 'as': 'job_info'}
            },
            { '$unwind': '$candidate_info' },
            { '$unwind': '$job_info' }
        ]
        return list(self.collection.aggregate(pipeline))

    def get_paginated_applications_with_details(self, skip=0, limit=10):
        total = self.count_docs()
        pipeline = [
            {'$lookup': {'from': 'candidates', 'localField': 'candidate_id', 'foreignField': '_id', 'as': 'candidate_info'}},
            {'$lookup': {'from': 'jobs', 'localField': 'job_id', 'foreignField': '_id', 'as': 'job_info'}},
            {'$unwind': '$candidate_info'},
            {'$unwind': '$job_info'},
            {'$skip': skip},
            {'$limit': limit}
        ]
        return list(self.collection.aggregate(pipeline)), total

    def update_status(self, app_id, new_status):
        return self.update(app_id, {"status": new_status})