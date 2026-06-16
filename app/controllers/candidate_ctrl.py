import os
import re
import PyPDF2
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from app.services.candidate_service import CandidateService
from app.models.candidate import Candidate
from app.repositories.base_repository import BaseRepository
from bson import ObjectId
from app.social_analysis.social_engine import SocialAnalyzer

candidate_bp = Blueprint('candidate', __name__, url_prefix='/candidates')

@candidate_bp.route('/')
def list_candidates():
    keyword = request.args.get('q', '')
    skill = request.args.get('skill', '')
    min_exp = request.args.get('min_exp', type=int)
    page = request.args.get('page', 1, type=int)
    filters = {'q': keyword, 'skill': skill, 'min_exp': min_exp}
    service = CandidateService()
    candidates, total_pages, current_page = service.search(filters, page=page, per_page=10)
    return render_template('candidates/list.html', candidates=candidates, filters=filters, total_pages=total_pages, current_page=current_page)

@candidate_bp.route('/detail/<cand_id>')
def view_candidate(cand_id):
    service = CandidateService()
    candidate = service.get_by_id(cand_id)
    if not candidate:
        flash('Candidate not found', 'danger')
        return redirect(url_for('candidate.list_candidates'))
    recommended_jobs = service.get_recommended_jobs(cand_id)
    
    # Lấy thông tin AI đã phân loại từ mining_results
    mining_repo = BaseRepository('mining_results')
    cand_obj_id = ObjectId(cand_id) if isinstance(cand_id, str) and len(cand_id) == 24 else cand_id
    mining_data = mining_repo.collection.find_one({"candidate_id": cand_obj_id})
    ai_role = mining_data['cluster_name'] if mining_data else None

    return render_template('candidates/detail.html', candidate=candidate, recommended_jobs=recommended_jobs, ai_role=ai_role)

@candidate_bp.route('/delete/<cand_id>')
def delete_candidate(cand_id):
    CandidateService().delete(cand_id)
    flash('Candidate deleted!', 'success')
    return redirect(url_for('candidate.list_candidates'))
@candidate_bp.route('/create', methods=['GET', 'POST'])
def create_candidate():
    if request.method == 'POST':
        service = CandidateService()
        try:
            cv_file_path = None
            if 'cv_file' in request.files:
                file = request.files['cv_file']
                if file.filename != '':
                    filename = secure_filename(file.filename)
                    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
                    os.makedirs(upload_folder, exist_ok=True)
                    file_path = os.path.join(upload_folder, filename)
                    file.save(file_path)
                    cv_file_path = f"/static/uploads/{filename}"

            cv_image_path = None
            if 'cv_image' in request.files and request.files['cv_image'].filename != '':
                file = request.files['cv_image']
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.root_path, 'static', 'uploads', filename)
                file.save(file_path)
                cv_image_path = f"/static/uploads/{filename}"

            audio_path = None
            if 'audio_file' in request.files and request.files['audio_file'].filename != '':
                file = request.files['audio_file']
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.root_path, 'static', 'uploads', filename)
                file.save(file_path)
                audio_path = f"/static/uploads/{filename}"

            video_path = None
            if 'video_file' in request.files and request.files['video_file'].filename != '':
                file = request.files['video_file']
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.root_path, 'static', 'uploads', filename)
                file.save(file_path)
                video_path = f"/static/uploads/{filename}"

            social_links = {}
            if request.form.get('linkedin'): social_links['linkedin'] = request.form.get('linkedin')
            if request.form.get('github'): social_links['github'] = request.form.get('github')

            form_data = {
                "candidate_code": f"CV{service.repo.count_docs() + 1:03d}",
                "full_name": request.form.get('full_name'),
                "email": request.form.get('email'),
                "phone": request.form.get('phone', ''),
                "skills": [s.strip() for s in request.form.get('skills', '').split(',') if s.strip()],
                "certificates": [c.strip() for c in request.form.get('certificates', '').split(',') if c.strip()],
                "experience_years": int(request.form.get('experience_years', 0)),
                "profile_description": request.form.get('profile_description', ''),
                "cv_file_path": cv_file_path,
                "cv_image_path": cv_image_path,
                "audio_path": audio_path,
                "video_path": video_path,
                "social_links": social_links
            }
            service.create(form_data)
            flash('Candidate created successfully!', 'success')
            return redirect(url_for('candidate.list_candidates'))
        except Exception as e:
            flash(f'Error creating candidate: {e}', 'danger')
    return render_template('candidates/create.html')

@candidate_bp.route('/parse_cv', methods=['POST'])
def parse_cv():
    """API tự động trích xuất thông tin (Auto-fill) từ file CV ngay trên giao diện"""
    if 'cv_file' not in request.files or request.files['cv_file'].filename == '':
        return jsonify({"error": "No file uploaded"}), 400

    try:
        file = request.files['cv_file']
        pdf_reader = PyPDF2.PdfReader(file)
        extracted_text = ""
        for page in pdf_reader.pages:
            extracted_text += page.extract_text() + "\n"
            
        # Dùng Regex để tự động tìm Email và Số điện thoại trong CV
        email_match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', extracted_text)
        phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', extracted_text)
        
        extracted_data = {
            "full_name": file.filename.replace('.pdf', ''), # Tạm lấy tên file làm tên ứng viên
            "email": email_match.group(0) if email_match else "",
            "phone": phone_match.group(0) if phone_match else "",
            "skills": "", # Giữ trống để người dùng điền tay hoặc để AI phân tích chuyên sâu sau
            "experience_years": 0,
            "profile_description": extracted_text.replace('\n', ' ').strip()[:1000] # Lấy 1000 chữ đầu làm mô tả
        }
        return jsonify(extracted_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@candidate_bp.route('/parse_link', methods=['POST'])
def parse_link():
    """API tự động trích xuất thông tin (Auto-fill) từ Social Link"""
    data = request.get_json()
    github_url = data.get('github_url')
    if not github_url:
        return jsonify({"error": "No URL provided"}), 400
        
    profile = SocialAnalyzer().parse_github_profile(github_url)
    return jsonify({
        "full_name": profile.get("full_name", ""),
        "email": profile.get("email", ""),
        "skills": ", ".join(profile.get("skills", []))
    })

@candidate_bp.route('/edit/<cand_id>', methods=['GET', 'POST'])
def edit_candidate(cand_id):
    service = CandidateService()
    candidate = service.get_by_id(cand_id)
    if not candidate:
        flash('Candidate not found', 'danger')
        return redirect(url_for('candidate.list_candidates'))

    if request.method == 'POST':
        try:
            cv_file_path = candidate.cv_file_path
            if 'cv_file' in request.files:
                file = request.files['cv_file']
                if file.filename != '':
                    filename = secure_filename(file.filename)
                    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
                    os.makedirs(upload_folder, exist_ok=True)
                    file_path = os.path.join(upload_folder, filename)
                    file.save(file_path)
                    cv_file_path = f"/static/uploads/{filename}"

            service.update(cand_id, request.form, cv_file_path)
            flash('Candidate updated successfully!', 'success')
            return redirect(url_for('candidate.list_candidates'))
        except Exception as e:
            flash(f'Error updating candidate: {e}', 'danger')

    return render_template('candidates/edit.html', candidate=candidate)