"AI-Based Movie Recommendation System,,,,, Streamlit App"

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter, defaultdict
from datetime import datetime

# Abit complicated but this the Theme CSS

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400&family=Inter:wght@200;300;400&display=swap');
:root{--r:#e50914;--rd:#b20710;--rl:#ff3d47;--bg:#0a0a0a;--card:#161212;--bdr:#2a1f1f;--t1:#f5efe6;--t2:#d4c8b8;--tm:#a89480;--gold:#d4a853}
.stApp,[data-testid="stAppViewContainer"]{background:linear-gradient(180deg,#0a0a0a,#111,#0d0d0d)!important;color:var(--t1)!important;font-family:'Inter',sans-serif!important}
[data-testid="stHeader"]{background:rgba(10,10,10,.95)!important;border-bottom:1px solid var(--bdr)}
[data-testid="stSidebar"],[data-testid="stSidebar"]>div{background:linear-gradient(180deg,#0f0f0f,#141414)!important;border-right:2px solid var(--r)!important}
[data-testid="stSidebar"] *{color:var(--t1)!important}
h1{font-family:'Cormorant Garamond',serif!important;color:var(--r)!important;font-size:3rem!important;font-weight:300!important;letter-spacing:6px!important;text-transform:uppercase!important;border-bottom:1px solid var(--r);padding-bottom:12px!important}
h2{font-family:'Cormorant Garamond',serif!important;color:var(--t1)!important;font-size:1.7rem!important;font-weight:400!important;letter-spacing:4px!important;text-transform:uppercase!important;border-left:2px solid var(--r);padding-left:14px!important;margin-top:28px!important}
h3{font-family:'Cormorant Garamond',serif!important;color:var(--rl)!important;font-size:1.3rem!important;font-weight:400!important;letter-spacing:2px!important}
p,li,span,div,label{color:var(--t2)!important;font-family:'Inter',sans-serif!important;font-weight:300!important}
.stButton>button,[data-testid="stFormSubmitButton"]>button{background:linear-gradient(135deg,var(--r),var(--rd))!important;color:var(--t1)!important;border:none!important;border-radius:4px!important;font-weight:400!important;letter-spacing:2px!important;text-transform:uppercase!important;padding:.6rem 2rem!important;box-shadow:0 2px 12px rgba(229,9,20,.2)!important}
.stButton>button:hover{background:linear-gradient(135deg,var(--rl),var(--r))!important;transform:translateY(-1px)!important}
.stTextInput>div>div>input,.stNumberInput>div>div>input,.stSelectbox>div>div{background-color:var(--card)!important;color:var(--t1)!important;border:1px solid var(--bdr)!important;font-weight:300!important}
.stTextInput>div>div>input:focus,.stNumberInput>div>div>input:focus{border-color:var(--r)!important;box-shadow:0 0 0 2px rgba(229,9,20,.2)!important}
.stSlider>div>div>div>div{background-color:var(--r)!important}
.stTabs [data-baseweb="tab-list"]{background-color:#111!important;border-radius:8px;padding:4px}
.stTabs [data-baseweb="tab"]{color:var(--t2)!important;font-weight:300!important;text-transform:uppercase!important;letter-spacing:1.5px!important;font-size:.85rem!important}
.stTabs [aria-selected="true"]{background-color:var(--r)!important;color:#fff!important}
[data-testid="stMetric"]{background:var(--card)!important;border:1px solid var(--bdr)!important;border-left:4px solid var(--r)!important;border-radius:8px!important;padding:16px 20px!important}
[data-testid="stMetricValue"]{color:var(--r)!important;font-family:'Cormorant Garamond',serif!important;font-weight:300!important;font-size:2.6rem!important;letter-spacing:3px!important}
[data-testid="stMetricLabel"]{color:var(--tm)!important;font-weight:300!important;text-transform:uppercase!important;letter-spacing:2px!important;font-size:.75rem!important}
::-webkit-scrollbar{width:8px}::-webkit-scrollbar-track{background:var(--bg)}::-webkit-scrollbar-thumb{background:var(--rd);border-radius:4px}
.movie-card{background:linear-gradient(145deg,#141010,#1a1414);border:1px solid var(--bdr);border-radius:10px;padding:22px;text-align:center;transition:all .4s ease;min-height:160px}
.movie-card:hover{border-color:var(--r);transform:translateY(-3px);box-shadow:0 6px 25px rgba(229,9,20,.15)}
.movie-card h4{font-family:'Cormorant Garamond',serif!important;color:var(--t1)!important;font-weight:400!important;font-size:1.15rem!important;letter-spacing:1px!important;margin-bottom:8px!important}
.movie-card .genre-tag{display:inline-block;color:var(--r);padding:2px 12px;border:1px solid var(--r);border-radius:20px;font-size:.7rem;letter-spacing:1.5px;text-transform:uppercase}
.movie-card .rating-star{color:var(--gold);font-size:1.1rem;letter-spacing:2px}
.hero-banner{background:linear-gradient(135deg,#1a0000,#0a0a0a,#1a0000);border:1px solid #2a0000;border-radius:16px;padding:40px 32px;text-align:center;margin-bottom:30px;position:relative;overflow:hidden}
.hero-banner::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,transparent,var(--r),transparent)}
.hero-banner h1{border:none!important;margin:0!important;padding:0!important;font-size:3.8rem!important;letter-spacing:10px!important}
.hero-banner p{color:var(--tm)!important;font-size:1rem!important;margin-top:10px!important;letter-spacing:3px!important;text-transform:uppercase!important}
.stat-box{background:linear-gradient(145deg,#141010,#1a1414);border:1px solid var(--bdr);border-top:2px solid var(--r);border-radius:8px;padding:22px;text-align:center}
.stat-box .stat-number{font-family:'Cormorant Garamond',serif;font-size:2.8rem;font-weight:300;color:var(--r);line-height:1;letter-spacing:2px}
.stat-box .stat-label{color:var(--tm);font-size:.7rem;text-transform:uppercase;letter-spacing:2.5px;font-weight:300;margin-top:8px}
.section-divider{height:1px;background:linear-gradient(90deg,transparent,#3a2020,transparent);margin:30px 0}
.css-card{background:var(--card);border:1px solid var(--bdr);border-radius:8px;padding:24px;margin-bottom:16px}
</style>
"""

# theme FOR THE ONE AND ONLY Movie Recommendor

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

# Classes

class Movie:
    "Stores movie metadata and user ratings."

    def __init__(self, movie_id: int, title: str, genre: str, year: int):
        self.movie_id = movie_id
        self.title = title
        self.genre = genre
        self.year = year
        self.ratings: list[float] = []

    def add_rating(self, score: float) -> None:
        """This function Adds rating 1-5"""
        self.ratings.append(score)

    def average_rating(self) -> float:
        """defines Mean rating or 0.0 if none."""
        if not self.ratings:
            return 0.0
        return sum(self.ratings) / len(self.ratings)

    def total_views(self) -> int:
        """Count ratings"""
        return len(self.ratings)

    def __repr__(self) -> str:
        return f"Movie({self.movie_id}, '{self.title}', {self.genre}, {self.year})"

class User:
    "Simple. This stores user profile, watch history, and ratings."

    def __init__(self, user_id: int, name: str, password: str):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.watch_history: list[tuple[int, str]] = []
        self.ratings: dict[int, float] = {}

    def rate_movie(self, movie_id: int, score: float) -> None:
        """Record rating and log watch event."""
        self.ratings[movie_id] = score
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.watch_history.append((movie_id, timestamp))

    def watched_genres(self, movie_db: dict) -> list[str]:
        """List of genres watched (with duplicates)."""
        return [movie_db[mid].genre for mid, _ in self.watch_history if mid in movie_db]

    def watch_count(self) -> int:
        "Total watch events."
        return len(self.watch_history)

    def __repr__(self) -> str:
        return f"User({self.user_id}, '{self.name}')"

class RecommendationEngine:
    """recommendation engine: recommendations, search, and analytics."""

    def __init__(self):
        self.movies: dict[int, Movie] = {}
        self.users: dict[int, User] = {}

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

    # -- Recommendations --

    def recommend_by_genre(self, user: User, top_n: int = 5) -> list[Movie]:
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
        """Highest-rated un-watched movies."""
        rated_ids = set(user.ratings.keys())
        candidates = [m for m in self.movies.values() if m.movie_id not in rated_ids]
        candidates.sort(key=lambda m: (-m.average_rating(), m.title))
        return candidates[:top_n]

    def combined_recommendations(self, user: User, top_n: int = 5) -> list[Movie]:
        
        genre_recs = self.recommend_by_genre(user, top_n)
        rating_recs = self.recommend_by_rating(user, top_n)
        seen: set[int] = set()
        merged: list[Movie] = []
        for movie in genre_recs + rating_recs:
            if movie.movie_id not in seen:
                seen.add(movie.movie_id)
                merged.append(movie)
        return merged[:top_n]

    # Analytics

    def most_popular_genre(self) -> str:
        """genre with most ratings"""
        genre_views: Counter = Counter()
        for m in self.movies.values():
            genre_views[m.genre] += m.total_views()
        if not genre_views:
            return "N/A"
        return genre_views.most_common(1)[0][0]

    def top_trending_movies(self, n: int = 3) -> list[Movie]:
        """Special formula : Ranked by views * avg_rating."""
        scored = [(m, m.total_views() * m.average_rating()) for m in self.movies.values()]
        scored.sort(key=lambda pair: -pair[1])
        return [m for m, _ in scored[:n]]

    def total_watch_count_per_user(self) -> dict[str, int]:
        return {u.name: u.watch_count() for u in self.users.values()}

    def top_active_users(self, n: int = 5) -> list[tuple[str, int]]:
        return sorted(self.total_watch_count_per_user().items(), key=lambda x: -x[1])[:n]

    def most_watched_movies(self, n: int = 5) -> list[Movie]:
        return sorted(self.movies.values(), key=lambda m: -m.total_views())[:n]

    # Search

    def search_movies(self, title_kw: str = "", genre: str = "", year: int = 0) -> list[Movie]:
        """Got title keyword, genre, and/or year """
        results = list(self.movies.values())
        if title_kw:
            kw = title_kw.lower()
            results = [m for m in results if kw in m.title.lower()]
        if genre:
            results = [m for m in results if m.genre.lower() == genre.lower()]
        if year:
            results = [m for m in results if m.year == year]
        return results

# Sample data Broski

def load_sample_data(engine: RecommendationEngine) -> None:
    """Load 30 movies, 4 users, and seed ratings."""
    sample_movies = [
        (1, "Stalker", "Sci-Fi", 1979),
        (2, "Solaris", "Sci-Fi", 1972),
        (3, "Moon", "Sci-Fi", 2009),
        (4, "Coherence", "Sci-Fi", 2013),
        (5, "The Raid", "Action", 2011),
        (6, "Hard Boiled", "Action", 1992),
        (7, "Oldboy", "Action", 2003),
        (8, "A Prophet", "Crime", 2009),
        (9, "City of God", "Crime", 2002),
        (10, "A Separation", "Drama", 2011),
        (11, "The Lives of Others", "Drama", 2006),
        (12, "In the Mood for Love", "Drama", 2000),
        (13, "Yi Yi", "Drama", 2000),
        (14, "The Handmaiden", "Thriller", 2016),
        (15, "Caché", "Thriller", 2005),
        (16, "Tell No One", "Thriller", 2006),
        (17, "The Hunt", "Thriller", 2012),
        (18, "Amélie", "Comedy", 2001),
        (19, "The Grand Budapest Hotel", "Comedy", 2014),
        (20, "Four Lions", "Comedy", 2010),
        (21, "Hausu", "Horror", 1977),
        (22, "The Wailing", "Horror", 2016),
        (23, "Audition", "Horror", 1999),
        (24, "Persepolis", "Animation", 2007),
        (25, "Paprika", "Animation", 2006),
        (26, "Waltz with Bashir", "Animation", 2008),
        (27, "Wings of Desire", "Fantasy", 1987),
        (28, "Pan's Labyrinth", "Fantasy", 2006),
        (29, "Amores Perros", "Drama", 2000),
        (30, "Cinema Paradiso", "Drama", 1988),
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
        1: {1: 4.5, 3: 4, 7: 5, 12: 5, 14: 4.5, 18: 4, 25: 4.5, 30: 5},
        2: {2: 4, 5: 5, 8: 4.5, 9: 5, 11: 4, 17: 4.5, 22: 4, 28: 5},
        3: {4: 4, 6: 4.5, 10: 5, 15: 3.5, 19: 4, 21: 3, 24: 4.5, 27: 4},
        4: {3: 4.5, 13: 4, 16: 4, 20: 3.5, 23: 4, 26: 5, 29: 4.5, 30: 4},
    }
    for uid, movie_ratings in seed_ratings.items():
        user = engine.users[uid]
        for mid, score in movie_ratings.items():
            user.rate_movie(mid, score)
            engine.movies[mid].add_rating(score)

# Session  

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

# emmm, this is helpers

def movies_to_df(movies: list[Movie]) -> pd.DataFrame:
    if not movies:
        return pd.DataFrame(columns=["Title", "Genre", "Year", "Avg Rating", "Views"])
    rows = [{
        "Title": m.title, "Genre": m.genre, "Year": m.year,
        "Avg Rating": round(m.average_rating(), 2), "Views": m.total_views(),
    } for m in movies]
    return pd.DataFrame(rows)

def render_movie_cards(movies: list[Movie], cols_per_row: int = 4) -> None:
    """Display movies as styled card grid."""
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

# Home page 

def page_home(engine: RecommendationEngine):
    # hero banner
    st.markdown("""
    <div class="hero-banner">
        <h1>🎬 CINEMAX MRS</h1>
        <p>Your AI-Powered Movie Recommendation System</p>
    </div>
    """, unsafe_allow_html=True)

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

    # search filters
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

    # Rate Moviessssss
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

# Dashboard Boui

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

    # trendddds
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

    # De watch histoiry table
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

    # Ratings bar chart
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

# Admin console 

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

# -- Sidebar --

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

# Mian

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
