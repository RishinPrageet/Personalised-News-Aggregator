import sqlite3
import tensorflow_hub as hub
import tensorflow as tf
import numpy as np
from sklearn.cluster import KMeans

def cluster_news_articles(n_clusters=10):
    # Connect to the SQLite database (adjust the path if needed)
    conn = sqlite3.connect("news_aggregator.db")
    cursor = conn.cursor()
    
    # Query: Fetch up to 3000 news articles with non-null title and description.
    query = """
    SELECT id, title, description, link, image, published
    FROM news
    WHERE title IS NOT NULL AND description IS NOT NULL
    ORDER BY published DESC
    """
    cursor.execute(query)
    articles = cursor.fetchall()
    conn.close()
    
    if not articles:
        print("No articles found in the database.")
        return None, None, None, None

    # Prepare texts by combining title and description for each article.
    texts = []
    article_ids = []
    c=0
    for article in articles:
        article_id, title, description, link, image, published = article
        # Combine title and description into a single text.
        text = f"{title}. {description}"
        texts.append(text)
        article_ids.append(article_id)
        if image:
            c+=1
    
    
    # Load the Universal Sentence Encoder from TensorFlow Hub.
    model_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    print("Loading text embedding model...")
    embed = hub.load(model_url)
    print("Model loaded.")
    
    # Compute embeddings for all articles.
    embeddings = embed(texts).numpy()
    print(f"Computed embeddings for {len(embeddings)} articles.")
    
    # Cluster the embeddings using KMeans.
    print(f"Clustering articles into {n_clusters} clusters...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_assignments = kmeans.fit_predict(embeddings)
    
    # Create a dictionary mapping each cluster to a list of article IDs.
    clusters_dict = {}
    for article_id, cluster_id in zip(article_ids, cluster_assignments):
        clusters_dict.setdefault(cluster_id, []).append(article_id)
    
    # Print a summary of clusters.
    print("\nCluster Summary:")
    for cluster_id, ids in clusters_dict.items():
        print(f"Cluster {cluster_id}: {len(ids)} articles")
        print(ids)

    
    print(f'\n {c}')
    return cluster_assignments, article_ids, articles, clusters_dict

if __name__ == "__main__":
    clusters, ids, articles, clusters_dict = cluster_news_articles(n_clusters=10)
