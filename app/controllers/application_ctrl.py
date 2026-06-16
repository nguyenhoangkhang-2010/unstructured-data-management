from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.application_service import ApplicationService
from app.services.candidate_service import CandidateService
from app.services.job_service import JobService

application_bp = Blueprint('application', __name__, url_prefix='/applications')

@application_bp.route('/')
def list_applications():
    page = request.args.get('page', 1, type=int)
    service = ApplicationService()
    applications, total_pages, current_page = service.get_paginated(page=page, per_page=10)
    return render_template('applications/list.html', applications=applications, total_pages=total_pages, current_page=current_page)

@application_bp.route('/update_status/<app_id>', methods=['POST'])
def update_status(app_id):
    ApplicationService().update_status(app_id, request.form.get('status'))
    return redirect(url_for('application.list_applications'))

@application_bp.route('/create', methods=['GET', 'POST'])
def create_application():
    if request.method == 'POST':
        form_data = {
            "candidate_id": request.form.get('candidate_id'),
            "job_id": request.form.get('job_id'),
            "status": request.form.get('status', 'Pending')
        }
        ApplicationService().create(form_data)
        flash('Application created successfully!', 'success')
        return redirect(url_for('application.list_applications'))
    
    candidates = CandidateService().get_all()
    jobs = JobService().get_all()
    return render_template('applications/create.html', candidates=candidates, jobs=jobs)

@application_bp.route('/delete/<app_id>')
def delete_application(app_id):
    ApplicationService().delete(app_id)
    flash('Application deleted successfully!', 'success')
    return redirect(url_for('application.list_applications'))