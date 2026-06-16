from flask import Blueprint, render_template
from app.services.candidate_service import DashboardService
from app.services.job_service import JobService

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/')

@dashboard_bp.route('/')
def index():
    # This is the new public-facing homepage
    service = JobService()
    jobs = service.get_all() # Get some jobs to display
    return render_template('index.html', jobs=jobs)

@dashboard_bp.route('/dashboard')
def dashboard_home():
    service = DashboardService()
    stats = service.get_dashboard_stats()
    chart_data = service.get_dashboard_charts_data()
    recent_logs = service.get_recent_logs()
    return render_template('dashboard.html', stats=stats, chart_data=chart_data, recent_logs=recent_logs)