from app.repositories.base_repository import BaseRepository
from app.models.job import Job

class JobRepository(BaseRepository):
    def __init__(self):
        super().__init__("jobs")

    def get_all_jobs(self):
        docs = self.find_all()
        return [Job.from_dict(doc) for doc in docs]

    def get_paginated_jobs(self, skip=0, limit=9):
        total = self.count_docs()
        docs = self.find_paginated({}, skip, limit)
        return [Job.from_dict(doc) for doc in docs], total

    def create_job(self, job: Job):
        return self.insert(job.to_dict())