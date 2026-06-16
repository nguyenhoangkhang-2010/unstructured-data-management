from app.recommendation.matcher import AIMatcher
from app.utils.logger import SystemLogger

class JobRecommender:
    """Hệ thống gợi ý Việc làm cho Ứng viên (Recommendation Engine)"""
    def __init__(self):
        self.logger = SystemLogger.get_logger(self.__class__.__name__)
        self.matcher = AIMatcher()

    def recommend_jobs_for_candidate(self, candidate, all_jobs):
        if not candidate or not all_jobs: 
            return []
        
        # Tạo text tổng hợp từ CV (Multi-modal fusion)
        cand_doc = f"{candidate.full_name} {' '.join(candidate.skills)} {candidate.profile_description} {candidate.ocr_text or ''} {candidate.transcript or ''}"
        
        job_docs = []
        for job in all_jobs:
            job_text = f"{job.title} {job.description} {' '.join(job.required_skills)}"
            job_docs.append(job_text)
            
        scores = self.matcher.calculate_match_scores(cand_doc, job_docs)
        ranked_jobs = [{"job": job, "match_score": score} for job, score in zip(all_jobs, scores) if score > 0]
        return sorted(ranked_jobs, key=lambda x: x['match_score'], reverse=True)