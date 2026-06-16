import re
import requests
from app.utils.logger import SystemLogger

class SocialAnalyzer:
    def __init__(self):
        self.logger = SystemLogger.get_logger(self.__class__.__name__)

    def extract_features(self, social_links):
        if not social_links:
            return []
            
        self.logger.info(f"Đang quét Social Links thật: {social_links}")
        features = []
        
        # 1. Trích xuất ngôn ngữ lập trình từ GitHub API
        github_url = social_links.get('github', '')
        if github_url:
            try:
                # Lấy username từ link (VD: https://github.com/defunkt -> defunkt)
                match = re.search(r'github\.com/([^/]+)', github_url)
                if match:
                    username = match.group(1)
                    # Gọi GitHub API lấy danh sách Repositories
                    response = requests.get(f"https://api.github.com/users/{username}/repos?per_page=10", timeout=5)
                    if response.status_code == 200:
                        repos = response.json()
                        for repo in repos:
                            lang = repo.get('language')
                            if lang:
                                features.append(lang)
                        if features:
                            features.append("Open Source Contributor")
            except Exception as e:
                self.logger.error(f"Lỗi khi cào dữ liệu GitHub: {e}")
                
        # 2. LinkedIn (Mô phỏng do cơ chế chống Bot)
        linkedin_url = social_links.get('linkedin', '')
        if linkedin_url:
            features.append("Active LinkedIn Networker")
            
        # Trả về danh sách kỹ năng duy nhất (không trùng lặp)
        return list(set(features)) if features else ["Active Networker"]

    def parse_github_profile(self, github_url):
        """Auto-fill API: Lấy thông tin cá nhân từ GitHub"""
        if not github_url: return {}
        profile = {"full_name": "", "email": "", "skills": []}
        try:
            match = re.search(r'github\.com/([^/]+)', github_url)
            if match:
                username = match.group(1)
                # Lấy Tên và Email
                user_resp = requests.get(f"https://api.github.com/users/{username}", timeout=5)
                if user_resp.status_code == 200:
                    data = user_resp.json()
                    profile['full_name'] = data.get('name') or username
                    profile['email'] = data.get('email') or ""
                
                # Lấy ngôn ngữ lập trình làm kỹ năng
                repo_resp = requests.get(f"https://api.github.com/users/{username}/repos?per_page=10", timeout=5)
                if repo_resp.status_code == 200:
                    profile['skills'] = list(set([r.get('language') for r in repo_resp.json() if r.get('language')]))
            return profile
        except Exception as e:
            self.logger.error(f"Lỗi Auto-fill GitHub Profile: {e}")
            return profile

    def parse_linkedin_profile(self, linkedin_url):
        """Auto-fill API: Lấy thông tin cá nhân từ LinkedIn (Mô phỏng do Anti-Bot)"""
        if not linkedin_url: return {}
        profile = {"full_name": "", "email": "", "skills": []}
        try:
            # Trích xuất username từ URL: linkedin.com/in/hoangkhang2411 -> hoangkhang2411
            match = re.search(r'linkedin\.com/in/([^/]+)', linkedin_url)
            if match:
                username = match.group(1).replace('-', ' ').title()
                profile['full_name'] = username
                # Mô phỏng dữ liệu kỹ năng mềm vì LinkedIn chặn cào dữ liệu công khai
                profile['skills'] = ["Leadership", "Project Management", "Communication", "Active Networker"]
            return profile
        except Exception as e:
            self.logger.error(f"Lỗi Auto-fill LinkedIn Profile: {e}")
            return profile