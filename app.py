"""
AI-Based Movie Recommendation System (MRS)
Developed as a Streamlit application for the Final Exam assessment.

This system uses content-based filtering and rating-based ranking
to generate personalised movie recommendations for users.

Classes:
    Movie   – stores movie metadata and ratings
    User    – stores user profile, watch history, and ratings
    RecommendationEngine – core logic for recommendations and analytics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter, defaultdict
from datetime import datetime


# ──────────────────────────────────────────────
#  CUSTOM THEME – Red & Black Cinema Style
# ──────────────────────────────────────────────

CUSTOM_CSS = """
<style>
/* ── Import bold Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600&family=Inter:wght@200;300;400;500&display=swap');

/* ── Root colour variables ── */
:root {
    --bg-primary: #0a0a0a;
    --bg-secondary: #111111;
    --bg-card: #161212;
    --bg-card-hover: #1e1818;
    --red-primary: #e50914;
    --red-light: #ff3d47;
    --red-dark: #b20710;
    --gold-accent: #d4a853;
    --text-primary: #f5efe6;
    --text-secondary: #d4c8b8;
    --text-muted: #a89480;
    --border-color: #2a1f1f;
}

/* ── Global background ── */
.stApp, .main, [data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #0a0a0a 0%, #111111 50%, #0d0d0d 100%) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stHeader"] {
    background: rgba(10, 10, 10, 0.95) !important;
    backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--border-color);
}

/* ── Sidebar ── */
[data-testid="stSidebar"], [data-testid="stSidebar"] > div {
    background: linear-gradient(180deg, #0f0f0f 0%, #141414 100%) !important;
    border-right: 2px solid var(--red-primary) !important;
}

[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3, [data-testid="stSidebar"] label,
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Headings – Cormorant Garamond thin & elegant ── */
h1 {
    font-family: 'Cormorant Garamond', serif !important;
    color: var(--red-primary) !important;
    font-size: 3rem !important;
    font-weight: 300 !important;
    letter-spacing: 6px !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid var(--red-primary);
    padding-bottom: 12px !important;
    margin-bottom: 24px !important;
}

h2 {
    font-family: 'Cormorant Garamond', serif !important;
    color: var(--text-primary) !important;
    font-size: 1.7rem !important;
    font-weight: 400 !important;
    letter-spacing: 4px !important;
    text-transform: uppercase !important;
    border-left: 2px solid var(--red-primary);
    padding-left: 14px !important;
    margin-top: 28px !important;
}

h3 {
    font-family: 'Cormorant Garamond', serif !important;
    color: var(--red-light) !important;
    font-size: 1.3rem !important;
    font-weight: 400 !important;
    letter-spacing: 2px !important;
}

/* ── Body text ── */
p, li, span, div, label {
    color: var(--text-secondary) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 300 !important;
}

/* ── Buttons – Red cinema style ── */
.stButton > button {
    background: linear-gradient(135deg, var(--red-primary), var(--red-dark)) !important;
    color: #f5efe6 !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 400 !important;
    font-size: 0.85rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 0.6rem 2rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 12px rgba(229, 9, 20, 0.2) !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, var(--red-light), var(--red-primary)) !important;
    box-shadow: 0 4px 20px rgba(229, 9, 20, 0.35) !important;
    transform: translateY(-1px) !important;
}

/* ── Form submit buttons ── */
[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, var(--red-primary), var(--red-dark)) !important;
    color: #f5efe6 !important;
    border: none !important;
    font-weight: 400 !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    box-shadow: 0 2px 12px rgba(229, 9, 20, 0.2) !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 6px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 300 !important;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: var(--red-primary) !important;
    box-shadow: 0 0 0 2px rgba(229, 9, 20, 0.2) !important;
}

/* ── Slider ── */
.stSlider > div > div > div > div {
    background-color: var(--red-primary) !important;
}

/* ── Dataframes ── */
[data-testid="stDataFrame"], .stDataFrame {
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    background-color: var(--bg-secondary) !important;
    border-radius: 8px;
    padding: 4px;
}

.stTabs [data-baseweb="tab"] {
    color: var(--text-secondary) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 300 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    border-radius: 4px !important;
    font-size: 0.85rem !important;
}

.stTabs [aria-selected="true"] {
    background-color: var(--red-primary) !important;
    color: white !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, var(--bg-card), var(--bg-card-hover)) !important;
    border: 1px solid var(--border-color) !important;
    border-left: 4px solid var(--red-primary) !important;
    border-radius: 8px !important;
    padding: 16px 20px !important;
}

[data-testid="stMetricValue"] {
    color: var(--red-primary) !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-weight: 300 !important;
    font-size: 2.6rem !important;
    letter-spacing: 3px !important;
}

[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-weight: 300 !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    font-size: 0.75rem !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--red-dark); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--red-primary); }

/* ── Movie card grid ── */
.movie-card {
    background: linear-gradient(145deg, #141010, #1a1414);
    border: 1px solid #2a1f1f;
    border-radius: 10px;
    padding: 22px;
    text-align: center;
    transition: all 0.4s ease;
    min-height: 160px;
}

.movie-card:hover {
    border-color: var(--red-primary);
    transform: translateY(-3px);
    box-shadow: 0 6px 25px rgba(229, 9, 20, 0.15);
}

.movie-card h4 {
    font-family: 'Cormorant Garamond', serif !important;
    color: #f5efe6 !important;
    font-weight: 400 !important;
    font-size: 1.15rem !important;
    letter-spacing: 1px !important;
    margin-bottom: 8px !important;
}

.movie-card .genre-tag {
    display: inline-block;
    background: transparent;
    color: var(--red-primary);
    padding: 2px 12px;
    border: 1px solid var(--red-primary);
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 400;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.movie-card .rating-star {
    color: var(--gold-accent);
    font-size: 1.1rem;
    font-weight: 300;
    letter-spacing: 2px;
}

/* ── Hero banner ── */
.hero-banner {
    background: linear-gradient(135deg, #1a0000 0%, #0a0a0a 50%, #1a0000 100%);
    border: 1px solid #2a0000;
    border-radius: 16px;
    padding: 40px 32px;
    text-align: center;
    margin-bottom: 30px;
    position: relative;
    overflow: hidden;
}

.hero-banner::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, var(--red-primary), transparent);
}

.hero-banner h1 {
    border: none !important;
    margin: 0 !important;
    padding: 0 !important;
    font-size: 3.8rem !important;
    font-weight: 300 !important;
    letter-spacing: 10px !important;
}

.hero-banner p {
    color: var(--text-muted) !important;
    font-size: 1rem !important;
    margin-top: 10px !important;
    letter-spacing: 3px !important;
    font-weight: 300 !important;
    text-transform: uppercase !important;
}

/* ── Stats row ── */
.stat-box {
    background: linear-gradient(145deg, #141010, #1a1414);
    border: 1px solid #2a1f1f;
    border-top: 2px solid var(--red-primary);
    border-radius: 8px;
    padding: 22px;
    text-align: center;
}

.stat-box .stat-number {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.8rem;
    font-weight: 300;
    color: var(--red-primary);
    line-height: 1;
    letter-spacing: 2px;
}

.stat-box .stat-label {
    color: var(--text-muted);
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    font-weight: 300;
    margin-top: 8px;
}

/* ── Section divider ── */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #3a2020, transparent);
    margin: 30px 0;
}

/* ── Admin card ── */
.css-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 24px;
    margin-bottom: 16px;
}
</style>
"""


# ──────────────────────────────────────────────
#  PLOTLY THEME – matching red/black aesthetic
# ──────────────────────────────────────────────

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(20,16,16,1)",
    font=dict(family="Inter, sans-serif", color="#d4c8b8", size=12),
    title_font=dict(family="Cormorant Garamond, serif", color="#f5efe6", size=18),
    xaxis=dict(gridcolor="#2a1f1f", color="#a89480"),
    yaxis=dict(gridcolor="#2a1f1f", color="#a89480"),
    margin=dict(l=40, r=20, t=50, b=40),
)

RED_SCALE = ["#4a0000", "#8b0000", "#b20710", "#e50914", "#ff3d47", "#ff6b6b"]


# ──────────────────────────────────────────────
#  CLASS DEFINITIONS  (Section A – Question a)
# ──────────────────────────────────────────────

class Movie:
    """Represents a single movie in the database.

    Attributes:
        movie_id  (int)  : unique identifier
        title     (str)  : movie title
        genre     (str)  : genre category
        year      (int)  : release year
        ratings   (list) : list of float ratings given by users
    """

    def __init__(self, movie_id: int, title: str, genre: str, year: int):
        self.movie_id = movie_id
        self.title = title
        self.genre = genre
        self.year = year
        self.ratings: list[float] = []

    def add_rating(self, score: float) -> None:
        """Append a rating (1-5) to this movie's rating list."""
        self.ratings.append(score)

    def average_rating(self) -> float:
        """Return the mean rating, or 0.0 if no ratings exist."""
        if not self.ratings:
            return 0.0
        return sum(self.ratings) / len(self.ratings)

    def total_views(self) -> int:
        """Number of ratings equals number of times the movie was watched/rated."""
        return len(self.ratings)

    def __repr__(self) -> str:
        return f"Movie({self.movie_id}, '{self.title}', {self.genre}, {self.year})"


class User:
    """Represents a registered user of the platform.

    Attributes:
        user_id       (int)  : unique identifier
        name          (str)  : display name
        password      (str)  : simple password for login
        watch_history (list) : list of (movie_id, timestamp) tuples
        ratings       (dict) : {movie_id: score} mapping
    """

    def __init__(self, user_id: int, name: str, password: str):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.watch_history: list[tuple[int, str]] = []
        self.ratings: dict[int, float] = {}

    def rate_movie(self, movie_id: int, score: float) -> None:
        """Record or update a rating for a movie and log the watch event."""
        self.ratings[movie_id] = score
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.watch_history.append((movie_id, timestamp))

    def watched_genres(self, movie_db: dict) -> list[str]:
        """Return a list of genres the user has watched (may contain duplicates)."""
        return [movie_db[mid].genre for mid, _ in self.watch_history if mid in movie_db]

    def watch_count(self) -> int:
        """Total number of watch events for this user."""
        return len(self.watch_history)

    def __repr__(self) -> str:
        return f"User({self.user_id}, '{self.name}')"


class RecommendationEngine:
    """Core engine that ties movies, users, and recommendation logic together.

    Attributes:
        movies (dict) : {movie_id: Movie} lookup table
        users  (dict) : {user_id: User}  lookup table
    """

    def __init__(self):
        self.movies: dict[int, Movie] = {}
        self.users: dict[int, User] = {}

    # ---------- database helpers ----------

    def add_movie(self, movie: Movie) -> None:
        self.movies[movie.movie_id] = movie

    def remove_movie(self, movie_id: int) -> bool:
        return self.movies.pop(movie_id, None) is not None

    def add_user(self, user: User) -> None:
        self.users[user.user_id] = user

    def next_movie_id(self) -> int:
        return max(self.movies.keys(), default=0) + 1

    def next_user_id(self) -> int:
        return max(self.users.keys(), default=0) + 1

    # ---------- recommendation logic (Section A-b) ----------

    def recommend_by_genre(self, user: User, top_n: int = 5) -> list[Movie]:
        """Content-based filtering: suggest unwatched movies whose genre
        matches the user's most-watched genres, sorted by avg rating."""
        genre_counts = Counter(user.watched_genres(self.movies))
        if not genre_counts:
            return []
        preferred = {g for g, _ in genre_counts.most_common()}
        rated_ids = set(user.ratings.keys())
        candidates = [
            m for m in self.movies.values()
            if m.movie_id not in rated_ids and m.genre in preferred
        ]
        candidates.sort(key=lambda m: (-m.average_rating(), m.title))
        return candidates[:top_n]

    def recommend_by_rating(self, user: User, top_n: int = 5) -> list[Movie]:
        """Rating-based filtering: suggest the highest-rated movies the
        user has not watched yet."""
        rated_ids = set(user.ratings.keys())
        candidates = [m for m in self.movies.values() if m.movie_id not in rated_ids]
        candidates.sort(key=lambda m: (-m.average_rating(), m.title))
        return candidates[:top_n]

    def combined_recommendations(self, user: User, top_n: int = 5) -> list[Movie]:
        """Merge genre-based and rating-based recommendations, removing
        duplicates while preserving order, then trim to top_n."""
        genre_recs = self.recommend_by_genre(user, top_n)
        rating_recs = self.recommend_by_rating(user, top_n)
        seen: set[int] = set()
        merged: list[Movie] = []
        for movie in genre_recs + rating_recs:
            if movie.movie_id not in seen:
                seen.add(movie.movie_id)
                merged.append(movie)
        return merged[:top_n]

    # ---------- analytics (Section A-c) ----------

    def most_popular_genre(self) -> str:
        """Return the genre with the highest total ratings count."""
        genre_views: Counter = Counter()
        for m in self.movies.values():
            genre_views[m.genre] += m.total_views()
        if not genre_views:
            return "N/A"
        return genre_views.most_common(1)[0][0]

    def top_trending_movies(self, n: int = 3) -> list[Movie]:
        """Trending = movies ranked by (total_views * avg_rating)."""
        scored = [(m, m.total_views() * m.average_rating()) for m in self.movies.values()]
        scored.sort(key=lambda pair: -pair[1])
        return [m for m, _ in scored[:n]]

    def total_watch_count_per_user(self) -> dict[str, int]:
        return {u.name: u.watch_count() for u in self.users.values()}

    def top_active_users(self, n: int = 5) -> list[tuple[str, int]]:
        counts = self.total_watch_count_per_user()
        return sorted(counts.items(), key=lambda x: -x[1])[:n]

    def most_watched_movies(self, n: int = 5) -> list[Movie]:
        return sorted(self.movies.values(), key=lambda m: -m.total_views())[:n]

    # ---------- search (Section B-a) ----------

    def search_movies(self, title_kw: str = "", genre: str = "", year: int = 0) -> list[Movie]:
        """Search movies by title keyword, genre, and/or year."""
        results = list(self.movies.values())
        if title_kw:
            kw = title_kw.lower()
            results = [m for m in results if kw in m.title.lower()]
        if genre:
            results = [m for m in results if m.genre.lower() == genre.lower()]
        if year:
            results = [m for m in results if m.year == year]
        return results


# ──────────────────────────────────────────────
#  SAMPLE DATA LOADER
# ──────────────────────────────────────────────

def load_sample_data(engine: RecommendationEngine) -> None:
    """Populate the engine with a starter dataset of 20 movies and 4 users."""
    sample_movies = [
        (1, "The Matrix", "Sci-Fi", 1999),
        (2, "Inception", "Sci-Fi", 2010),
        (3, "Interstellar", "Sci-Fi", 2014),
        (4, "The Dark Knight", "Action", 2008),
        (5, "John Wick", "Action", 2014),
        (6, "Mad Max: Fury Road", "Action", 2015),
        (7, "The Shawshank Redemption", "Drama", 2004),
        (8, "Forrest Gump", "Drama", 1994),
        (9, "The Godfather", "Drama", 1972),
        (10, "Superbad", "Comedy", 2007),
        (11, "The Hangover", "Comedy", 2009),
        (12, "Step Brothers", "Comedy", 2008),
        (13, "Conjuring", "Horror", 2013),
        (14, "Get Out", "Horror", 2017),
        (15, "Parasite", "Thriller", 2019),
        (16, "Gone Girl", "Thriller", 2014),
        (17, "Spirited Away", "Animation", 2001),
        (18, "Coco", "Animation", 2017),
        (19, "Avengers: Endgame", "Action", 2019),
        (20, "Dune", "Sci-Fi", 2021),
    ]
    for mid, title, genre, year in sample_movies:
        engine.add_movie(Movie(mid, title, genre, year))

    users_data = [
        (1, "Alice", "alice123"),
        (2, "Bob", "bob123"),
        (3, "Charlie", "charlie123"),
        (4, "Diana", "diana123"),
    ]
    for uid, name, pwd in users_data:
        engine.add_user(User(uid, name, pwd))

    seed_ratings = {
        1: {1: 5, 2: 4.5, 4: 5, 7: 4, 13: 3, 17: 4.5, 19: 5},
        2: {3: 5, 5: 4, 6: 4.5, 9: 5, 15: 4.5, 20: 4},
        3: {2: 4, 8: 3.5, 10: 4, 11: 3, 14: 4.5, 16: 4},
        4: {1: 4, 3: 4.5, 12: 3, 17: 5, 18: 5, 20: 4.5},
    }
    for uid, movie_ratings in seed_ratings.items():
        user = engine.users[uid]
        for mid, score in movie_ratings.items():
            user.rate_movie(mid, score)
            engine.movies[mid].add_rating(score)


# ──────────────────────────────────────────────
#  SESSION STATE INITIALISATION
# ──────────────────────────────────────────────

def init_state() -> RecommendationEngine:
    if "engine" not in st.session_state:
        engine = RecommendationEngine()
        load_sample_data(engine)
        st.session_state.engine = engine
    if "logged_in_user" not in st.session_state:
        st.session_state.logged_in_user = None
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False
    return st.session_state.engine


# ──────────────────────────────────────────────
#  HELPER FUNCTIONS
# ──────────────────────────────────────────────

def movies_to_df(movies: list[Movie]) -> pd.DataFrame:
    if not movies:
        return pd.DataFrame(columns=["Title", "Genre", "Year", "Avg Rating", "Views"])
    rows = [{
        "Title": m.title, "Genre": m.genre, "Year": m.year,
        "Avg Rating": round(m.average_rating(), 2), "Views": m.total_views(),
    } for m in movies]
    return pd.DataFrame(rows)


def render_movie_cards(movies: list[Movie], cols_per_row: int = 4) -> None:
    """Display movies as styled cards in a grid layout."""
    for i in range(0, len(movies), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(movies):
                m = movies[idx]
                avg = m.average_rating()
                stars = "★" * int(round(avg)) + "☆" * (5 - int(round(avg)))
                with col:
                    st.markdown(f"""
                    <div class="movie-card">
                        <h4>{m.title}</h4>
                        <span class="genre-tag">{m.genre}</span>
                        <p style="color:#a89480!important;font-size:0.85rem;margin:8px 0 4px 0;font-weight:300;">{m.year}</p>
                        <div class="rating-star">{stars}</div>
                        <p style="color:#d4c8b8!important;font-size:0.8rem;font-weight:300;">{avg:.1f}/5 · {m.total_views()} views</p>
                    </div>
                    """, unsafe_allow_html=True)


def render_stat_boxes(stats: list[tuple[str, str]]) -> None:
    cols = st.columns(len(stats))
    for col, (number, label) in zip(cols, stats):
        with col:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{number}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)


def styled_plotly(fig) -> None:
    fig.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)


# ──────────────────────────────────────────────
#  PAGE: Home / Browse & Search  (Section B-a)
# ──────────────────────────────────────────────

def page_home(engine: RecommendationEngine):
    # hero banner
    st.markdown("""
    <div class="hero-banner">
        <h1>🎬 CINEMAX MRS</h1>
        <p>Your AI-Powered Movie Recommendation System</p>
    </div>
    """, unsafe_allow_html=True)

    # quick stats
    total_movies = len(engine.movies)
    total_users = len(engine.users)
    total_ratings = sum(m.total_views() for m in engine.movies.values())
    top_genre = engine.most_popular_genre()

    render_stat_boxes([
        (str(total_movies), "Movies"),
        (str(total_users), "Users"),
        (str(total_ratings), "Ratings"),
        (top_genre, "Top Genre"),
    ])

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # --- search filters ---
    st.subheader("Search Movies")
    col1, col2, col3 = st.columns(3)
    with col1:
        kw = st.text_input("🔍 Title keyword", key="search_kw")
    with col2:
        genres = sorted({m.genre for m in engine.movies.values()})
        genre = st.selectbox("🎭 Genre", ["All"] + genres, key="search_genre")
    with col3:
        years = sorted({m.year for m in engine.movies.values()})
        year = st.selectbox("📅 Year", [0] + years,
                            format_func=lambda y: "All" if y == 0 else str(y),
                            key="search_year")

    results = engine.search_movies(
        title_kw=kw,
        genre="" if genre == "All" else genre,
        year=year,
    )

    st.subheader(f"Results — {len(results)} movies found")
    render_movie_cards(results)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # --- rate a movie (Section B-a i) ---
    st.subheader("Rate a Movie")
    user = st.session_state.logged_in_user
    if user is None:
        st.info("⚡ Log in from the sidebar to rate movies and unlock recommendations.")
        return

    movie_names = {m.movie_id: f"{m.title} ({m.year})" for m in engine.movies.values()}
    selected_id = st.selectbox("Select a movie", list(movie_names.keys()),
                               format_func=lambda x: movie_names[x], key="rate_select")
    score = st.slider("Your rating", 1.0, 5.0, 3.0, 0.5, key="rate_slider")

    if st.button("🎬 Submit Rating"):
        user.rate_movie(selected_id, score)
        engine.movies[selected_id].add_rating(score)
        st.success(f"✅ Rated **{engine.movies[selected_id].title}** → {score}/5")
        st.rerun()


# ──────────────────────────────────────────────
#  PAGE: User Dashboard  (Section B-b)
# ──────────────────────────────────────────────

def page_dashboard(engine: RecommendationEngine):
    user = st.session_state.logged_in_user
    if user is None:
        st.warning("⚡ Please log in to view your dashboard.")
        return

    st.title(f"📊 {user.name}'s Dashboard")

    render_stat_boxes([
        (str(user.watch_count()), "Movies Watched"),
        (str(len(user.ratings)), "Ratings Given"),
        (f"{sum(user.ratings.values()) / len(user.ratings):.1f}" if user.ratings else "0", "Avg Rating"),
    ])

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # --- Top-N recommendations ---
    st.subheader("🎯 Recommended For You")
    top_n = st.slider("Number of recommendations", 3, 10, 5, key="topn")
    recs = engine.combined_recommendations(user, top_n)
    if recs:
        render_movie_cards(recs)
    else:
        st.info("Rate a few movies first so we can personalise your feed!")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # --- Trending & popular genres ---
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("🔥 Trending Movies")
        trending = engine.top_trending_movies(5)
        st.dataframe(movies_to_df(trending), use_container_width=True, hide_index=True)

    with col_right:
        st.subheader("🏆 Popular Genres")
        st.metric("Top Genre", engine.most_popular_genre())
        genre_counts = Counter(m.genre for m in engine.movies.values() for _ in m.ratings)
        if genre_counts:
            df_genre = pd.DataFrame(genre_counts.items(), columns=["Genre", "Total Ratings"])
            fig = px.pie(df_genre, names="Genre", values="Total Ratings",
                         title="Ratings by Genre", hole=0.45,
                         color_discrete_sequence=RED_SCALE)
            styled_plotly(fig)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # --- Watch history table ---
    st.subheader("📜 Watch History & Rating Log")
    if user.watch_history:
        history_rows = []
        for mid, ts in user.watch_history:
            m = engine.movies.get(mid)
            if m:
                history_rows.append({
                    "Movie": m.title, "Genre": m.genre,
                    "Your Rating": user.ratings.get(mid, "–"), "Watched On": ts,
                })
        st.dataframe(pd.DataFrame(history_rows), use_container_width=True, hide_index=True)
    else:
        st.info("You haven't watched anything yet.")

    # --- Ratings bar chart ---
    st.subheader("📈 Your Ratings Overview")
    if user.ratings:
        rated_data = [{"Movie": engine.movies[mid].title, "Rating": score}
                      for mid, score in user.ratings.items() if mid in engine.movies]
        df_rated = pd.DataFrame(rated_data).sort_values("Rating", ascending=False)
        fig2 = px.bar(df_rated, x="Movie", y="Rating", title="Movies You Rated",
                       color="Rating",
                       color_continuous_scale=["#4a0000", "#e50914", "#ff6b6b"],
                       range_y=[0, 5])
        styled_plotly(fig2)


# ──────────────────────────────────────────────
#  PAGE: Admin Console  (Section B-c)
# ──────────────────────────────────────────────

ADMIN_KEY = "admin2025"

def page_admin(engine: RecommendationEngine):
    st.title("🔒 Admin Console")

    if not st.session_state.admin_logged_in:
        st.markdown("""
        <div class="css-card" style="max-width:420px;margin:40px auto;text-align:center;">
            <h3 style="color:#f5efe6!important;">🔐 Administrator Access</h3>
            <p style="font-size:0.9rem;letter-spacing:1px;">Enter the admin key to continue</p>
        </div>
        """, unsafe_allow_html=True)
        key = st.text_input("Enter admin key", type="password")
        if st.button("🔐 Authenticate"):
            if key == ADMIN_KEY:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("❌ Invalid admin key.")
        return

    st.success("✅ Authenticated as Administrator")
    tab_manage, tab_analytics = st.tabs(["🎬 Movie Management", "📊 Engagement Analytics"])

    with tab_manage:
        st.subheader("Add New Movie")
        with st.form("add_movie_form"):
            new_title = st.text_input("Title")
            new_genre = st.text_input("Genre")
            new_year = st.number_input("Year", 1900, 2030, 2024)
            if st.form_submit_button("➕ Add Movie"):
                if new_title and new_genre:
                    mid = engine.next_movie_id()
                    engine.add_movie(Movie(mid, new_title, new_genre, int(new_year)))
                    st.success(f"✅ Added: {new_title} (ID {mid})")

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        st.subheader("Edit Movie")
        if engine.movies:
            edit_id = st.selectbox("Select movie to edit", list(engine.movies.keys()),
                                   format_func=lambda x: f"{engine.movies[x].title} (ID {x})",
                                   key="edit_select")
            m = engine.movies[edit_id]
            with st.form("edit_movie_form"):
                ed_title = st.text_input("Title", value=m.title)
                ed_genre = st.text_input("Genre", value=m.genre)
                ed_year = st.number_input("Year", 1900, 2030, m.year)
                if st.form_submit_button("💾 Save Changes"):
                    m.title, m.genre, m.year = ed_title, ed_genre, int(ed_year)
                    st.success(f"✅ Updated movie ID {edit_id}")

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        st.subheader("Remove Movie")
        if engine.movies:
            del_id = st.selectbox("Select movie to remove", list(engine.movies.keys()),
                                   format_func=lambda x: f"{engine.movies[x].title} (ID {x})",
                                   key="del_select")
            if st.button("🗑️ Delete Movie"):
                title = engine.movies[del_id].title
                engine.remove_movie(del_id)
                st.success(f"✅ Removed: {title}")
                st.rerun()

    with tab_analytics:
        total_ratings = sum(m.total_views() for m in engine.movies.values())
        render_stat_boxes([
            (str(len(engine.movies)), "Total Movies"),
            (str(len(engine.users)), "Total Users"),
            (str(total_ratings), "Total Ratings"),
        ])

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        st.subheader("Most-Watched Movies")
        most_watched = engine.most_watched_movies(5)
        df_mw = movies_to_df(most_watched)
        st.dataframe(df_mw, use_container_width=True, hide_index=True)
        if not df_mw.empty:
            fig_mw = px.bar(df_mw, x="Title", y="Views", title="Most-Watched Movies",
                            color="Views",
                            color_continuous_scale=["#4a0000", "#e50914", "#ff3d47"])
            styled_plotly(fig_mw)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        st.subheader("Top Active Users")
        active = engine.top_active_users(5)
        if active:
            df_active = pd.DataFrame(active, columns=["User", "Watch Count"])
            st.dataframe(df_active, use_container_width=True, hide_index=True)
            fig_au = px.bar(df_active, x="User", y="Watch Count", title="Most Active Users",
                            color="Watch Count",
                            color_continuous_scale=["#4a0000", "#e50914"])
            styled_plotly(fig_au)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        st.subheader("Trending Movie List")
        render_movie_cards(engine.top_trending_movies(5))


# ──────────────────────────────────────────────
#  SIDEBAR: Navigation & Authentication
# ──────────────────────────────────────────────

def sidebar_login(engine: RecommendationEngine):
    st.sidebar.markdown("""
    <div style="text-align:center;padding:10px 0 20px 0;">
        <span style="font-family:'Cormorant Garamond',serif;font-size:2.4rem;color:#e50914;letter-spacing:8px;font-weight:300;">
            CINEMAX
        </span>
        <br>
        <span style="font-size:0.65rem;color:#a89480;letter-spacing:3px;text-transform:uppercase;font-weight:300;">
            Movie Recommendation System
        </span>
    </div>
    """, unsafe_allow_html=True)

    user = st.session_state.logged_in_user

    if user:
        st.sidebar.success(f"Logged in as **{user.name}**")
        if st.sidebar.button("🚪 Logout"):
            st.session_state.logged_in_user = None
            st.session_state.admin_logged_in = False
            st.rerun()
    else:
        auth_tab = st.sidebar.radio("Account", ["Login", "Register"])
        if auth_tab == "Login":
            uname = st.sidebar.text_input("Username", key="login_name")
            upwd = st.sidebar.text_input("Password", type="password", key="login_pwd")
            if st.sidebar.button("🔑 Login"):
                found = next(
                    (u for u in engine.users.values()
                     if u.name.lower() == uname.lower() and u.password == upwd), None)
                if found:
                    st.session_state.logged_in_user = found
                    st.rerun()
                else:
                    st.sidebar.error("Invalid credentials.")
        else:
            new_name = st.sidebar.text_input("Choose a username", key="reg_name")
            new_pwd = st.sidebar.text_input("Choose a password", type="password", key="reg_pwd")
            if st.sidebar.button("📝 Register"):
                if new_name and new_pwd:
                    uid = engine.next_user_id()
                    new_user = User(uid, new_name, new_pwd)
                    engine.add_user(new_user)
                    st.session_state.logged_in_user = new_user
                    st.rerun()
                else:
                    st.sidebar.error("Fill in both fields.")

    st.sidebar.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    page = st.sidebar.selectbox("Navigate", ["🏠 Home", "📊 Dashboard", "🔒 Admin Console"])
    return page


# ──────────────────────────────────────────────
#  MAIN APP ENTRY POINT
# ──────────────────────────────────────────────

def main():
    st.set_page_config(
        page_title="CINEMAX — Movie Recommendation System",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    engine = init_state()
    page = sidebar_login(engine)

    if page == "🏠 Home":
        page_home(engine)
    elif page == "📊 Dashboard":
        page_dashboard(engine)
    elif page == "🔒 Admin Console":
        page_admin(engine)


if __name__ == "__main__":
    main()
