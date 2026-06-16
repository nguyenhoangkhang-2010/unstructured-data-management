from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.utils.logger import SystemLogger

class AIMatcher:
    """AI Matching Engine sử dụng TF-IDF và Cosine Similarity"""
    def __init__(self):
        self.logger = SystemLogger.get_logger(self.__class__.__name__)
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def calculate_match_scores(self, source_doc, target_docs):
        if not target_docs:
            return []
        try:
            # Gom source và targets vào 1 ma trận để tính TF-IDF
            all_docs = [source_doc] + target_docs
            tfidf_matrix = self.vectorizer.fit_transform(all_docs)
            # Tính độ tương đồng Cosine
            cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
            return [round(score * 100, 2) for score in cosine_sim]
        except Exception as e:
            self.logger.error(f"Matching Error: {e}")
            return [0.0] * len(target_docs)