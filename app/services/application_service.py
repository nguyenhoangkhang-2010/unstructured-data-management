from app.repositories.application_repo import ApplicationRepository
from app.models.application import Application
from app.utils.logger import LogService

class ApplicationService:
    def __init__(self):
        self.repo = ApplicationRepository()

    def get_all_with_details(self):
        return self.repo.get_all_applications_with_details()

    def get_paginated(self, page=1, per_page=10):
        skip = (page - 1) * per_page
        applications, total = self.repo.get_paginated_applications_with_details(skip, per_page)
        total_pages = (total + per_page - 1) // per_page
        return applications, total_pages, page

    def update_status(self, app_id, status):
        LogService.write_log("UPDATE_STATUS", "Application", {"app_id": str(app_id), "status": status})
        return self.repo.update_status(app_id, status)
        
    def create(self, form_data):
        LogService.write_log("CREATE", "Application", {"job_id": str(form_data.get('job_id'))})
        new_app = Application(**form_data)
        return self.repo.insert(new_app.to_dict())
        
    def delete(self, app_id):
        LogService.write_log("DELETE", "Application", {"app_id": str(app_id)})
        return self.repo.delete(app_id)