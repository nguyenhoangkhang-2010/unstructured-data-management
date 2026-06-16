import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from app.config.settings import Config

class DataVisualizer:
    def __init__(self):
        self.output_dir = Config.STATIC_OUTPUTS
        os.makedirs(self.output_dir, exist_ok=True)

    def plot_cluster_distribution(self, df):
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.countplot(data=df, y='role_prediction', hue='role_prediction', legend=False, palette='viridis', order=df['role_prediction'].value_counts().index, ax=ax)
        ax.set_title('Phân bố Ứng viên theo Cụm Kỹ năng (K-Means)')
        path = os.path.join(self.output_dir, 'cluster_dist.png')
        fig.tight_layout()
        fig.savefig(path)
        plt.close(fig)
        return 'outputs/cluster_dist.png'

    def generate_wordclouds(self, df):
        paths = []
        for role in df['role_prediction'].unique():
            text = " ".join(df[df['role_prediction'] == role]['clean_profile'])
            
            # Bỏ qua nếu text trống để tránh lỗi WordCloud
            if not text.strip():
                continue
                
            wc = WordCloud(width=600, height=300, background_color='white').generate(text)
            
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.imshow(wc, interpolation='bilinear')
            ax.axis('off')
            ax.set_title(role)
            
            path = os.path.join(self.output_dir, f"wc_{role.replace(' ', '_')}.png")
            fig.savefig(path)
            plt.close(fig)
            paths.append(f"outputs/wc_{role.replace(' ', '_')}.png")
        return paths