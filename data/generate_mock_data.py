import sys, os, random
from datetime import datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from faker import Faker
from app.database.db_manager import DatabaseManager

fake = Faker()
def generate():
    db = DatabaseManager().get_db()
    # Xóa dữ liệu cũ
    db.candidates.delete_many({})
    db.jobs.delete_many({})
    db.applications.delete_many({})
    db.mining_results.delete_many({})

    skills = ["Python", "Java", "React", "NodeJS", "Machine Learning", "SQL", "Cyber Security", "C++", "Docker", "AWS", "Data Analysis", "Frontend"]
    desc_templates = [
        "I am a Backend developer with 5 years experience in Python, building robust REST APIs.",
        "Passionate frontend developer skilled in React, Vue and creating excellent UI/UX.",
        "Data analyst with strong SQL, Tableau, and visualization skills to drive business decisions.",
        "Cyber security expert specializing in penetration testing and secure infrastructure.",
        "AI Engineer implementing deep learning, NLP models and K-Means for data clustering."
    ]

    print("Đang tạo 300 Ứng viên...")
    candidates = []
    for i in range(1, 301):
        candidates.append({
            "candidate_code": f"CV{i:03d}",
            "full_name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "skills": random.sample(skills, random.randint(3, 6)),
            "certificates": [fake.word().capitalize() + " Certificate"],
            "experience_years": random.randint(1, 10),
            "profile_description": random.choice(desc_templates) + " " + fake.text(100),
            "cv_file_path": f"/uploads/cv_{i:03d}.pdf",
            "cv_image_path": f"/uploads/img_{i:03d}.jpg",
            "audio_path": f"/uploads/voice_{i:03d}.mp3",
            "video_path": f"/uploads/vid_{i:03d}.mp4",
            "social_links": {"linkedin": f"linkedin.com/in/{fake.first_name()}", "github": f"github.com/{fake.user_name()}"},
            "created_at": datetime.now() - timedelta(days=random.randint(1, 365))
        })
    res_cand = db.candidates.insert_many(candidates)
    cand_ids = res_cand.inserted_ids
    
    print("Đang tạo 30 Tin Tuyển dụng...")
    jobs = []
    for i in range(1, 31):
        jobs.append({
            "job_code": f"JOB{i:03d}",
            "title": fake.job(),
            "description": fake.text(200),
            "required_skills": random.sample(skills, random.randint(2, 5)),
            "salary": random.randint(1000, 5000),
            "created_at": datetime.now() - timedelta(days=random.randint(1, 30))
        })
    res_jobs = db.jobs.insert_many(jobs)
    job_ids = res_jobs.inserted_ids

    print("Đang tạo 1000 Đơn ứng tuyển với ObjectIDs thực...")
    apps = [{"candidate_id": random.choice(cand_ids), "job_id": random.choice(job_ids), "status": random.choice(["Pending", "Reviewed", "Interview", "Rejected", "Hired"]), "apply_date": datetime.now() - timedelta(days=random.randint(1, 30))} for _ in range(1000)]
    db.applications.insert_many(apps)

    print("Hoàn tất tạo Mock Data!")

if __name__ == "__main__":
    generate()
