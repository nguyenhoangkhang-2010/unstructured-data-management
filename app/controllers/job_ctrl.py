from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.job_service import JobService

job_bp = Blueprint('job', __name__, url_prefix='/jobs')

@job_bp.route('/')
def list_jobs():
    page = request.args.get('page', 1, type=int)
    service = JobService()
    jobs, total_pages, current_page = service.get_paginated(page=page, per_page=9) # 9 cards per page looks good for 3-col grid
    return render_template('jobs/list.html', jobs=jobs, total_pages=total_pages, current_page=current_page)

@job_bp.route('/create', methods=['GET', 'POST'])
def create_job():
    if request.method == 'POST':
        service = JobService()
        form_data = {
            "job_code": f"JOB{service.repo.count_docs() + 1:03d}",
            "title": request.form.get('title'),
            "description": request.form.get('description'),
            "required_skills": request.form.get('required_skills', '').split(','),
            "salary": int(request.form.get('salary', 0))
        }
        service.create(form_data)
        return redirect(url_for('job.list_jobs'))
    return render_template('jobs/create.html')

@job_bp.route('/edit/<job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    service = JobService()
    job = service.get_by_id(job_id)
    if not job:
        flash('Job not found!', 'danger')
        return redirect(url_for('job.list_jobs'))
        
    if request.method == 'POST':
        try:
            service.update(job_id, request.form)
            flash('Job updated successfully!', 'success')
            return redirect(url_for('job.list_jobs'))
        except Exception as e:
            flash(f'Error updating job: {e}', 'danger')
    return render_template('jobs/edit.html', job=job)

@job_bp.route('/detail/<job_id>')
def view_job(job_id):
    service = JobService()
    job = service.get_by_id(job_id)
    if not job: return redirect(url_for('job.list_jobs'))
    ranked_candidates = service.get_ranked_candidates_for_job(job_id)
    return render_template('jobs/detail.html', job=job, ranked_candidates=ranked_candidates)

@job_bp.route('/delete/<job_id>')
def delete_job(job_id):
    JobService().delete(job_id)
    return redirect(url_for('job.list_jobs'))