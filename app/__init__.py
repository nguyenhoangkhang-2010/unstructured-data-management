from flask import Flask
from app.config.settings import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.controllers.dashboard_ctrl import dashboard_bp
    from app.controllers.mining_ctrl import mining_bp
    from app.controllers.candidate_ctrl import candidate_bp
    from app.controllers.job_ctrl import job_bp
    from app.controllers.application_ctrl import application_bp
    from app.controllers.report_ctrl import report_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(mining_bp)
    app.register_blueprint(candidate_bp)
    app.register_blueprint(job_bp)
    app.register_blueprint(application_bp)
    app.register_blueprint(report_bp)

    return app