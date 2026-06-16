from app.repositories.candidate_repo import CandidateRepository
from app.repositories.base_repository import BaseRepository
from app.utils.logger import LogService
from app.models.candidate import Candidate
from app.utils.logger import SystemLogger
from app.ocr.ocr_engine import OCREngine
from app.audio_processing.audio_engine import AudioProcessor
from app.social_analysis.social_engine import SocialAnalyzer
from app.video_processing.video_engine import VideoProcessor
from app.recommendation.recommender import JobRecommender
from app.repositories.job_repo import JobRepository
import pandas as pd

class DashboardService:
    def __init__(self):
        self.cand_repo = CandidateRepository()
        self.job_repo = BaseRepository("jobs")
        self.app_repo = BaseRepository("applications")
        self.log_repo = BaseRepository("logs")
        
    def get_dashboard_stats(self):
        return {
            "total_candidates": self.cand_repo.count_docs(),
            "total_jobs": self.job_repo.count_docs(),
            "total_applications": self.app_repo.count_docs()
        }
        
    def get_dashboard_charts_data(self):
        skills_data = self.cand_repo.get_top_skills_aggregation()
        labels = [s['_id'] for s in skills_data]
        values = [s['count'] for s in skills_data]
        return {"skill_labels": labels, "skill_values": values}
        
    def get_recent_logs(self):
        pipeline = [
            {"$sort": {"timestamp": -1}},
            {"$limit": 5}
        ]
        return list(self.log_repo.collection.aggregate(pipeline))

class CandidateService:
    def __init__(self): self.repo = CandidateRepository()
    
    def get_all(self):
        return self.repo.get_all_candidates()
        
    def get_by_id(self, cand_id):
        return self.repo.get_candidate_by_id(cand_id)

    def search(self, filters, page=1, per_page=10):
        skip = (page - 1) * per_page
        candidates, total = self.repo.search_candidates_paginated(filters, skip, per_page)
        total_pages = (total + per_page - 1) // per_page
        return candidates, total_pages, page

    def delete(self, cand_id):
        LogService.write_log("DELETE", "Candidate", {"candidate_id": str(cand_id)})
        return self.repo.delete(cand_id)

    def create(self, form_data):
        # Multi-modal extraction pipelines
        ocr_text = OCREngine().extract_text(form_data.get('cv_image_path'))
        transcript = AudioProcessor().speech_to_text(form_data.get('audio_path'))
        social_features = SocialAnalyzer().extract_features(form_data.get('social_links'))
        video_meta = VideoProcessor().process_video(form_data.get('video_path'))
        
        form_data['ocr_text'] = ocr_text
        form_data['transcript'] = transcript
        
        if social_features:
            form_data['skills'].extend(social_features)
        LogService.write_log("CREATE", "Candidate", {"name": form_data.get('full_name')})
             
        new_candidate = Candidate(**form_data)
        return self.repo.create_candidate(new_candidate)
        
    def update(self, cand_id, form_data, cv_file_path=None):
        update_data = {
            "full_name": form_data.get('full_name'),
            "email": form_data.get('email'),
            "phone": form_data.get('phone', ''),
            "skills": [s.strip() for s in form_data.get('skills', '').split(',') if s.strip()],
            "certificates": [c.strip() for c in form_data.get('certificates', '').split(',') if c.strip()],
            "experience_years": int(form_data.get('experience_years', 0)),
            "profile_description": form_data.get('profile_description', '')
        }
        if cv_file_path:
            update_data["cv_file_path"] = cv_file_path
        LogService.write_log("UPDATE", "Candidate", {"candidate_id": str(cand_id)})
        return self.repo.update_candidate(cand_id, update_data)

    def get_recommended_jobs(self, cand_id):
        candidate = self.get_by_id(cand_id)
        if not candidate: return []
        all_jobs = JobRepository().get_all_jobs()
        return JobRecommender().recommend_jobs_for_candidate(candidate, all_jobs)

    def get_dataframe_for_mining(self):
        candidates = self.get_all()
        data = [c.to_dict() for c in candidates]
        return pd.DataFrame(data)