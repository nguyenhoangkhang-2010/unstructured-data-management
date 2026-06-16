import os
import pandas as pd
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from app.config.settings import Config
from app.utils.logger import SystemLogger
from app.repositories.base_repository import BaseRepository
from app.utils.logger import LogService
from app.models.mining_result import MiningResult

class MiningService:
    @staticmethod
    def save_results(silhouette, inertia, clusters_dist, df, model_version="kmeans_v1"):
        logger = SystemLogger.get_logger("MiningService")
        try:
            # 1. Lưu các chỉ số đánh giá tổng thể vào mining_metrics
            metrics_repo = BaseRepository('mining_metrics')
            data = {
                "silhouette_score": silhouette,
                "inertia": inertia,
                "clusters": clusters_dist,
                "timestamp": datetime.now(),
                "model_version": model_version
            }
            metrics_repo.insert(data)
            
            # 2. Lưu từng kết quả ứng viên vào mining_results
            repo = BaseRepository('mining_results')
            repo.collection.delete_many({}) # Xóa dữ liệu cũ
            
            docs = []
            for index, row in df.iterrows():
                result = MiningResult(
                    candidate_id=row['_id'],
                    cluster=int(row['cluster_id']),
                    cluster_name=row['role_prediction']
                )
                docs.append(result.to_dict())
                
            if docs:
                repo.collection.insert_many(docs)
        except Exception as e:
            logger.error(f"Database Error while saving mining results: {e}")

class CandidateMiner:
    def __init__(self):
        self.logger = SystemLogger.get_logger(self.__class__.__name__)
        self.n_clusters = 10
        # Thêm các từ sáo rỗng thường gặp trong CV vào bộ lọc từ nhiễu (stopwords)
        custom_stopwords = list(ENGLISH_STOP_WORDS) + ['experience', 'skills', 'strong', 'drive', 'years', 'business', 'decisions', 'excellent', 'working', 'knowledge']
        self.vectorizer = TfidfVectorizer(max_features=1500, stop_words=custom_stopwords)
        self.model = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)
        self.mining_repo = BaseRepository('mining_results')
        self.cluster_names = {}

    def process(self, df, text_col='clean_profile'):
        self.logger.info("Bắt đầu trích xuất đặc trưng TF-IDF và K-Means...")
        X = self.vectorizer.fit_transform(df[text_col])
        labels = self.model.fit_predict(X)
        
        df['cluster_id'] = labels
        
        terms = self.vectorizer.get_feature_names_out()
        order_centroids = self.model.cluster_centers_.argsort()[:, ::-1]
        
        for i in range(self.n_clusters):
            # Lọc bỏ dấu gạch dưới do thư viện NLP tiếng Việt tự nối các từ tiếng Anh
            top_words = [terms[ind].replace('_', ' ').title() for ind in order_centroids[i, :3]]
            self.cluster_names[i] = "Nhóm: " + " - ".join(top_words)
            
        df['role_prediction'] = df['cluster_id'].apply(lambda x: self.cluster_names[x])
        
        silhouette = silhouette_score(X, labels)
        inertia = self.model.inertia_
        
        clusters_dist = df['role_prediction'].value_counts().to_dict()
        MiningService.save_results(silhouette, inertia, clusters_dist, df)
        LogService.write_log("RUN_MINING", "AI_Pipeline", {"silhouette": silhouette, "inertia": inertia})
        return df, silhouette, inertia

    def export_report(self, df, silhouette, inertia):
        os.makedirs(Config.OUTPUT_FOLDER, exist_ok=True)
        df.to_csv(os.path.join(Config.OUTPUT_FOLDER, 'mined_candidates.csv'), index=False)
        
        with open(os.path.join(Config.OUTPUT_FOLDER, 'mining_report.txt'), 'w', encoding='utf-8') as f:
            f.write("=== CANDIDATE MINING REPORT ===\n")
            f.write(f"Algorithm: K-Means (K={self.n_clusters})\n")
            f.write(f"Silhouette Score: {silhouette:.4f}\n")
            f.write(f"Inertia: {inertia:.4f}\n\n")
            f.write("Cluster Distribution:\n")
            f.write(df['role_prediction'].value_counts().to_string())