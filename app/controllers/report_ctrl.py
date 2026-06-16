import os
from flask import Blueprint, render_template, send_file, flash, redirect, url_for
from app.config.settings import Config

report_bp = Blueprint('report', __name__, url_prefix='/reports')

@report_bp.route('/')
def index():
    # Kiểm tra xem các file kết quả đã tồn tại hay chưa
    csv_exists = os.path.exists(os.path.join(Config.OUTPUT_FOLDER, 'mined_candidates.csv'))
    txt_exists = os.path.exists(os.path.join(Config.OUTPUT_FOLDER, 'mining_report.txt'))
    png_exists = os.path.exists(os.path.join(Config.STATIC_OUTPUTS, 'cluster_dist.png'))
    
    return render_template('reports/index.html', csv_exists=csv_exists, txt_exists=txt_exists, png_exists=png_exists)

@report_bp.route('/download/<file_type>')
def download_report(file_type):
    if file_type == 'csv':
        file_path = os.path.join(Config.OUTPUT_FOLDER, 'mined_candidates.csv')
        filename = 'mined_candidates.csv'
    elif file_type == 'txt':
        file_path = os.path.join(Config.OUTPUT_FOLDER, 'mining_report.txt')
        filename = 'mining_report.txt'
    elif file_type == 'png':
        file_path = os.path.join(Config.STATIC_OUTPUTS, 'cluster_dist.png')
        filename = 'cluster_distribution.png'
    else:
        return redirect(url_for('report.index'))

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name=filename)
    else:
        return redirect(url_for('report.index'))