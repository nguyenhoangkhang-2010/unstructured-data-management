from datetime import datetime

class Job:
    def __init__(self, job_code, title, description, required_skills, salary, created_at=None, _id=None):
        self._id = _id
        self.job_code = job_code
        self.title = title
        self.description = description
        self.required_skills = required_skills if isinstance(required_skills, list) else [required_skills]
        self.salary = salary
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        data = {
            "job_code": self.job_code,
            "title": self.title,
            "description": self.description,
            "required_skills": self.required_skills,
            "salary": self.salary,
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
            job_code=data.get('job_code', 'N/A'),
            title=data.get('title', ''),
            description=data.get('description', ''),
            required_skills=data.get('required_skills', []),
            salary=data.get('salary', 0),
            created_at=data.get('created_at')
        )