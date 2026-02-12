import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
movies = pd.read_csv("dataset.csv")

# Use overview column (confirmed to exist)
movies["overview"] = movies["overview"].fillna("").astype(str)

# Vectorize
cv = CountVectorizer(stop_words="english", max_features=5000)
vectors = cv.fit_transform(movies["overview"])

# Similarity matrix
similarity = cosine_similarity(vectors)

# Save correctly as pickle (binary)
with open("similarity.pkl", "wb") as f:
    pickle.dump(similarity, f)

print("✅ similarity.pkl created correctly")
