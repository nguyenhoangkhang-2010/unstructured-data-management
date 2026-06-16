from app.repositories.base_repository import BaseRepository
from app.models.candidate import Candidate

class CandidateRepository(BaseRepository):
    def __init__(self):
        super().__init__("candidates")

    def get_all_candidates(self):
        docs = self.find_all()
        return [Candidate.from_dict(doc) for doc in docs]

    def create_candidate(self, candidate: Candidate):
        return self.insert(candidate.to_dict())

    def get_candidate_by_id(self, candidate_id):
        doc = self.find_by_id(candidate_id)
        return Candidate.from_dict(doc) if doc else None
        
    def update_candidate(self, cand_id, update_data):
        return self.update(cand_id, update_data)

    def search_candidates(self, query_str):
        query = {"$or": [
            {"full_name": {"$regex": query_str, "$options": "i"}},
            {"skills": {"$regex": query_str, "$options": "i"}}
        ]}
        return [Candidate.from_dict(doc) for doc in self.find_all(query)]
        
    def search_candidates_paginated(self, filters, skip=0, limit=10):
        query = {}
        conditions = []
        
        if filters.get('q'):
            conditions.append({"$or": [{"full_name": {"$regex": filters['q'], "$options": "i"}}, {"email": {"$regex": filters['q'], "$options": "i"}}]})
        if filters.get('skill'):
            conditions.append({"skills": {"$regex": filters['skill'], "$options": "i"}})
        if filters.get('min_exp') is not None:
            conditions.append({"experience_years": {"$gte": filters['min_exp']}})
            
        if conditions:
            query["$and"] = conditions
            
        total = self.count_docs(query)
        docs = self.find_paginated(query, skip, limit)
        return [Candidate.from_dict(doc) for doc in docs], total

    def get_top_skills_aggregation(self):
        pipeline = [
            {"$unwind": "$skills"},
            {"$group": {"_id": "$skills", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]
        return list(self.collection.aggregate(pipeline))