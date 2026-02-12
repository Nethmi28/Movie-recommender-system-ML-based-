import streamlit as st
import pandas as pd
import pickle
import requests

TMDB_API_KEY = "2057b8fc63edf50458e27410b00bf1ed"

st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("Movie Recommender System")

movies = pd.read_csv("dataset.csv")  # columns: id, title
similarity = pickle.load(open("similarity.pkl", "rb"))

# ---------- TMDB helpers ----------
@st.cache_data(ttl=24*3600)
def tmdb_genre_map():
    """Returns dict: {genre_id: genre_name}"""
    url = "https://api.themoviedb.org/3/genre/movie/list"
    params = {"api_key": TMDB_API_KEY, "language": "en-US"}
    r = requests.get(url, params=params, timeout=10)
    data = r.json()
    genres = data.get("genres", [])
    return {g["id"]: g["name"] for g in genres}

@st.cache_data(ttl=24*3600)
def tmdb_search_first(movie_title: str):
    """Return first TMDB search result dict or None"""
    url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": movie_title}
    r = requests.get(url, params=params, timeout=10)
    data = r.json()
    results = data.get("results", [])
    return results[0] if results else None

@st.cache_data(ttl=24*3600)
def tmdb_movie_details(tmdb_id: int):
    """Return movie details JSON (includes genres)"""
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
    params = {"api_key": TMDB_API_KEY, "language": "en-US"}
    r = requests.get(url, params=params, timeout=10)
    return r.json()

def fetch_poster_by_path(poster_path: str):
    if not poster_path:
        return None
    return "https://image.tmdb.org/t/p/w500" + poster_path

# ---------- Sidebar controls ----------
genre_id_to_name = tmdb_genre_map()
genre_name_to_id = {v: k for k, v in genre_id_to_name.items()}

st.sidebar.header("Filters")

top_n = st.sidebar.slider("Number of recommendations", min_value=5, max_value=20, value=5, step=1)

genre_options = ["All"] + sorted(list(genre_name_to_id.keys()))
genre_choice = st.sidebar.selectbox("Genre filter (TMDB)", genre_options, index=0)

selected_genre_id = None if genre_choice == "All" else genre_name_to_id[genre_choice]

# ---------- UI selector ----------
movie_list = movies["title"].astype(str).values
selected_movie = st.selectbox("Select a movie you like:", movie_list)

# ---------- Recommender ----------
def recommend_indices(movie_title: str, top_k: int):
    idx = movies[movies["title"] == movie_title].index[0]
    distances = similarity[idx]
    ranked = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    # skip itself at [0]
    return [i for i, _ in ranked[1:top_k+1]]

def passes_genre_filter(title: str, genre_id: int | None) -> bool:
    """If no filter -> True. Else check TMDB genres for this title."""
    if genre_id is None:
        return True

    res = tmdb_search_first(title)
    if not res:
        return False

    tmdb_id = res.get("id")
    details = tmdb_movie_details(tmdb_id)
    genres = details.get("genres", [])
    genre_ids = {g["id"] for g in genres}
    return genre_id in genre_ids

def recommend_with_optional_genre(movie_title: str, top_n: int, genre_id: int | None):
    """
    We may need to pull more than top_n from similarity list
    because genre filtering can remove items.
    """
    # pull a bigger pool to survive filtering
    pool_size = max(50, top_n * 8)
    candidate_idxs = recommend_indices(movie_title, pool_size)

    results = []
    for i in candidate_idxs:
        title = str(movies.iloc[i]["title"])
        if passes_genre_filter(title, genre_id):
            results.append(title)
        if len(results) >= top_n:
            break

    return results

# ---------- Button action ----------
if st.button("Show recommendations"):
    with st.spinner("Building recommendations..."):
        rec_titles = recommend_with_optional_genre(selected_movie, top_n, selected_genre_id)

    st.subheader(f"Recommended movies ({len(rec_titles)}):")

    if len(rec_titles) == 0:
        st.warning("No movies matched the selected genre filter. Try 'All' or a different genre.")
    else:
        cols = st.columns(min(5, len(rec_titles)))
        col_i = 0

        for t in rec_titles:
            # poster from TMDB search (fast)
            res = tmdb_search_first(t)
            poster_url = fetch_poster_by_path(res.get("poster_path")) if res else None

            with cols[col_i]:
                if poster_url:
                    st.image(poster_url, use_container_width=True)
                st.caption(t)

            col_i = (col_i + 1) % len(cols)
