from app.repositories.job_repo import JobRepository
from app.repositories.candidate_repo import CandidateRepository
from app.models.job import Job
from app.recommendation.matcher import AIMatcher
from app.utils.logger import LogService, SystemLogger
from app.repositories.base_repository import BaseRepository
from bson import ObjectId
from datetime import datetime

class RecommendationService:
    @staticmethod
    def save_scores(job_id, ranked_results):
        logger = SystemLogger.get_logger("RecommendationService")
        try:
            repo = BaseRepository("recommendation_results")
            # Xóa các gợi ý cũ của Job này trước khi lưu đợt mới
            repo.collection.delete_many({"job_id": ObjectId(job_id) if isinstance(job_id, str) else job_id})
            
            docs = []
            for rank, res in enumerate(ranked_results, 1):
                docs.append({
                    "candidate_id": ObjectId(res['candidate']._id) if isinstance(res['candidate']._id, str) else res['candidate']._id,
                    "job_id": ObjectId(job_id) if isinstance(job_id, str) else job_id,
                    "cosine_score": res['match_score'],
                    "rank": rank,
                    "timestamp": datetime.now()
                })
            if docs:
                repo.collection.insert_many(docs)
        except Exception as e:
            logger.error(f"Failed to save recommendation scores: {e}")

class JobService:
    def __init__(self):
        self.repo = JobRepository()
        self.cand_repo = CandidateRepository()
        self.ai_matcher = AIMatcher()

    def get_all(self):
        return self.repo.get_all_jobs()

    def get_paginated(self, page=1, per_page=9):
        skip = (page - 1) * per_page
        jobs, total = self.repo.get_paginated_jobs(skip, per_page)
        total_pages = (total + per_page - 1) // per_page
        return jobs, total_pages, page

    def get_by_id(self, job_id):
        doc = self.repo.find_by_id(job_id)
        return Job.from_dict(doc) if doc else None

    def update(self, job_id, form_data):
        sal = form_data.get('salary')
        update_data = {
            "title": form_data.get('title'),
            "description": form_data.get('description'),
            "required_skills": [s.strip() for s in form_data.get('required_skills', '').split(',') if s.strip()],
            "salary": int(sal) if sal and str(sal).strip() else 0
        }
        LogService.write_log("UPDATE", "Job", {"job_id": str(job_id)})
        return self.repo.update(job_id, update_data)

    def create(self, form_data):
        LogService.write_log("CREATE", "Job", {"title": form_data.get('title')})
        new_job = Job(**form_data)
        return self.repo.create_job(new_job)

    def delete(self, job_id):
        LogService.write_log("DELETE", "Job", {"job_id": str(job_id)})
        return self.repo.delete(job_id)

    def get_ranked_candidates_for_job(self, job_id):
        """AI Matching: Xếp hạng ứng viên phù hợp cho 1 Job"""
        job = self.get_by_id(job_id)
        if not job: return []
        
        candidates = self.cand_repo.get_all_candidates()
        if not candidates: return []

        # Xây dựng document văn bản cho Job
        job_doc = job.title + " " + job.description + " " + " ".join(job.required_skills)
        
        # Xây dựng document văn bản cho từng Candidate (multi-modal text fusion)
        cand_docs = []
        for c in candidates:
            fusion_text = f"{c.full_name} {' '.join(c.skills)} {c.profile_description} {c.ocr_text or ''} {c.transcript or ''}"
            cand_docs.append(fusion_text)
            
        scores = self.ai_matcher.calculate_match_scores(job_doc, cand_docs)
        
        ranked_results = [{"candidate": c, "match_score": s} for c, s in zip(candidates, scores) if s > 0]
        sorted_results = sorted(ranked_results, key=lambda x: x['match_score'], reverse=True)
        RecommendationService.save_scores(job_id, sorted_results)
        LogService.write_log("AI_MATCHING", "Recommendation", {"job_id": str(job_id), "candidates_ranked": len(sorted_results)})
        return sorted_results