from flask import Blueprint, render_template
from app.services.candidate_service import CandidateService
from app.preprocessing.text_cleaner import TextPreprocessor
from app.mining.kmeans_clustering import CandidateMiner
from app.visualization.visualizer import DataVisualizer

mining_bp = Blueprint('mining', __name__, url_prefix='/mining')

@mining_bp.route('/')
def run_mining():
    df = CandidateService().get_dataframe_for_mining()
    if df.empty: return "Không có dữ liệu khai phá.", 400

    df['clean_profile'] = df['profile_description'].apply(TextPreprocessor().clean)
    mined_df, silhouette, inertia = CandidateMiner().process(df)
    CandidateMiner().export_report(mined_df, silhouette, inertia)

    dist_img = DataVisualizer().plot_cluster_distribution(mined_df)
    wc_imgs = DataVisualizer().generate_wordclouds(mined_df)

    return render_template('mining.html', silhouette=silhouette, inertia=inertia, dist_img=dist_img, wc_imgs=wc_imgs)