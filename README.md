# 🎬 Movie Recommender System

A **Content-Based Movie Recommendation System** built using **Python, Machine Learning, and Streamlit**.  
This application recommends movies similar to a selected movie based on textual features and displays movie posters using the **TMDB API**.

---

## 📌 Project Overview

This project implements a content-based filtering approach where movie overviews are transformed into numerical vectors using NLP techniques. The system computes similarity scores and recommends the most similar movies to the user.

The application is deployed locally using **Streamlit** to provide an interactive user interface.

---

## 🚀 Features

- ✅ Content-based movie recommendations  
- ✅ NLP using **CountVectorizer**  
- ✅ Similarity computation using **Cosine Similarity**  
- ✅ Interactive **Streamlit web interface**  
- ✅ Adjustable Top-N recommendations  
- ✅ Optional genre filtering  
- ✅ Real-time movie posters using **TMDB API**

---

## 🛠️ Tech Stack

- Python
- Pandas
- Scikit-learn
- Streamlit
- TMDB API
- Pickle

---

## 🧠 How It Works

1. Movie overview text is converted into numerical vectors using **CountVectorizer**
2. Cosine similarity is calculated between all movie vectors
3. The similarity matrix is stored as `similarity.pkl`
4. When a user selects a movie, the system retrieves the top similar movies based on similarity scores
5. Movie posters are fetched dynamically using the TMDB API

---
## 📂 Project Structure

├── app.py
├── main.py
├── build_similarity.py
├── movies_list.pkl
├── similarity.pkl
├── dataset.csv
├── README.md
## 📂 Project Structure

