from datetime import datetime

class Candidate:
    def __init__(self, candidate_code, full_name, email, phone, skills, certificates, experience_years, profile_description, cv_file_path=None, cv_image_path=None, audio_path=None, video_path=None, social_links=None, ocr_text=None, transcript=None, created_at=None, _id=None):
        self._id = _id
        self.candidate_code = candidate_code
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.skills = skills if isinstance(skills, list) else [skills]
        self.certificates = certificates if isinstance(certificates, list) else [certificates]
        self.experience_years = experience_years
        self.profile_description = profile_description
        self.cv_file_path = cv_file_path
        self.cv_image_path = cv_image_path
        self.audio_path = audio_path
        self.video_path = video_path
        self.social_links = social_links if isinstance(social_links, dict) else {}
        self.ocr_text = ocr_text
        self.transcript = transcript
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        data = {
            "candidate_code": self.candidate_code,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "skills": self.skills,
            "certificates": self.certificates,
            "experience_years": self.experience_years,
            "profile_description": self.profile_description,
            "cv_file_path": self.cv_file_path,
            "cv_image_path": self.cv_image_path,
            "audio_path": self.audio_path,
            "video_path": self.video_path,
            "social_links": self.social_links,
            "ocr_text": self.ocr_text,
            "transcript": self.transcript,
            "created_at": self.created_at
        }
        if self._id:
            data['_id'] = self._id
        return data

    @classmethod
    def from_dict(cls, data):
        if not data: return None
        return cls(
            _id=data.get('_id'),
            candidate_code=data.get('candidate_code', 'N/A'),
            full_name=data.get('full_name', ''),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            skills=data.get('skills', []),
            certificates=data.get('certificates', []),
            experience_years=data.get('experience_years', 0),
            profile_description=data.get('profile_description', ''),
            cv_file_path=data.get('cv_file_path'),
            cv_image_path=data.get('cv_image_path'),
            audio_path=data.get('audio_path'),
            video_path=data.get('video_path'),
            social_links=data.get('social_links', {}),
            ocr_text=data.get('ocr_text'),
            transcript=data.get('transcript'),
            created_at=data.get('created_at')
        )