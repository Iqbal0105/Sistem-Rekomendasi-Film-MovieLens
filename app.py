import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import recommender
from concurrent.futures import ThreadPoolExecutor

# Set page configuration with a premium Netflix-like title and icon
st.set_page_config(
    page_title="Movieflix AI - Sistem Rekomendasi Film",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Netflix-Themed Premium CSS Styling
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    /* Main body overrides */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #141414 !important;
        color: #e5e5e5 !important;
    }
    
    .stApp {
        background-color: #141414 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        color: #ffffff !important;
        font-weight: 800;
    }
    
    /* Netflix Red Logo Brand */
    .brand-logo {
        color: #E50914;
        font-family: 'Outfit', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        letter-spacing: -2px;
        text-transform: uppercase;
        margin-bottom: 0.1rem;
        display: inline-block;
    }
    
    .brand-sub {
        font-size: 1rem;
        color: #aaa;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Netflix Cinema Hero Banner */
    .hero-banner {
        background: linear-gradient(180deg, rgba(30,30,30,0.95) 0%, rgba(20,20,20,0.95) 100%);
        border: 1px solid rgba(229, 9, 20, 0.15);
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2.5rem;
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.5);
    }
    
    .hero-poster-container {
        border-radius: 8px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.7);
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.1;
        margin-bottom: 0.5rem;
    }
    
    .hero-meta {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
        flex-wrap: wrap;
    }
    
    .hero-year {
        font-size: 1rem;
        color: #ffffff;
        font-weight: bold;
    }
    
    .hero-match {
        font-size: 0.95rem;
        color: #46d369; /* Netflix Green match */
        font-weight: 700;
    }
    
    .hero-cf-badge {
        font-size: 0.85rem;
        font-weight: 700;
        color: #e50914;
        background: rgba(229, 9, 20, 0.15);
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        border: 1px solid rgba(229, 9, 20, 0.3);
    }
    
    .hero-desc {
        font-size: 1.05rem;
        color: #cccccc;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }
    
    /* Netflix Cards Layout */
    .movie-card {
        background: #181818;
        border: 1px solid #2f2f2f;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        transition: transform 0.4s cubic-bezier(0.165, 0.84, 0.44, 1), border-color 0.4s ease, box-shadow 0.4s ease;
        margin-bottom: 1.5rem;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .movie-card:hover {
        transform: translateY(-8px) scale(1.03);
        border-color: #E50914;
        box-shadow: 0 12px 30px rgba(229, 9, 20, 0.25);
    }
    
    .movie-card-img-container {
        position: relative;
        width: 100%;
        aspect-ratio: 2/3;
        overflow: hidden;
        background-color: #2a2a2a;
    }
    
    .movie-card-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .movie-card-content {
        padding: 1rem;
        display: flex;
        flex-direction: column;
        flex-grow: 1;
    }
    
    .card-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.3rem;
        line-height: 1.3;
        height: 3.0rem;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    
    .card-meta {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.5rem;
    }
    
    .card-match {
        font-size: 0.85rem;
        color: #46d369;
        font-weight: 700;
    }
    
    .card-year {
        font-size: 0.85rem;
        color: #999999;
        background: rgba(255,255,255,0.08);
        padding: 0.1rem 0.4rem;
        border-radius: 4px;
    }
    
    .card-rating-row {
        font-size: 0.85rem;
        color: #fbbf24;
        margin-bottom: 0.6rem;
    }
    
    .card-desc {
        font-size: 0.85rem;
        color: #aaaaaa;
        line-height: 1.4;
        margin-bottom: 0.8rem;
        height: 3.6rem;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    
    .card-genres {
        display: flex;
        flex-wrap: nowrap;
        gap: 0.3rem;
        margin-top: auto;
        height: 1.6rem;
        overflow: hidden;
    }
    
    /* Genre Badges */
    .genre-badge {
        font-size: 0.7rem;
        font-weight: 600;
        color: #cccccc;
        background: rgba(255, 255, 255, 0.08);
        padding: 0.15rem 0.4rem;
        border-radius: 3px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #181818 !important;
        border-right: 1px solid #2f2f2f;
    }
    
    /* Tabs Overrides */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        border-bottom: 1px solid #2f2f2f;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Outfit', sans-serif;
        font-size: 1.1rem;
        color: #999999;
        background-color: transparent !important;
        padding-bottom: 0.75rem;
    }
    
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        border-bottom-color: #E50914 !important;
        font-weight: bold;
    }
    
    /* Button Custom styling */
    .stButton>button {
        background-color: #E50914 !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        font-weight: bold !important;
        padding: 0.5rem 1.5rem !important;
        transition: background-color 0.2s;
    }
    
    .stButton>button:hover {
        background-color: #b80710 !important;
    }
    
    /* Metric Card Styling */
    .metric-box {
        background: #181818;
        border: 1px solid #2f2f2f;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-sizing: border-box;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- DATA LOADING & CACHING -----------------

@st.cache_data
def get_cached_movies():
    return recommender.load_movies()

@st.cache_resource
def get_cached_content_matrix(movies_df):
    return recommender.get_content_model(movies_df)

@st.cache_resource
def get_cached_collaborative_matrix():
    return recommender.load_collaborative_model()

# Loading details helper with caching (BeautifulSoup)
@st.cache_data(show_spinner=False)
def get_movie_details_cached(tmdb_id):
    """Cached details retrieval (poster url and plot overview)."""
    poster, desc = recommender.fetch_tmdb_details(tmdb_id)
    if not poster:
        # High quality aesthetic cinematic poster placeholder
        poster = "https://images.unsplash.com/photo-1594909122845-11baa439b7bf?q=80&w=300&auto=format&fit=crop"
    return poster, desc

def load_details_in_parallel(recs_df):
    """Loads TMDb details (posters, synopses) concurrently to ensure maximum performance."""
    if recs_df.empty:
        return []
    records = list(recs_df.itertuples())
    with ThreadPoolExecutor(max_workers=len(records)) as executor:
        results = list(executor.map(lambda r: get_movie_details_cached(r.tmdbId), records))
    return results

# Load Core Data
with st.spinner("🚀 Memuat database film & konfigurasi sistem..."):
    try:
        movies_df = get_cached_movies()
        tfidf_matrix = get_cached_content_matrix(movies_df)
        item_sim_df = get_cached_collaborative_matrix()
    except Exception as e:
        st.error(f"Gagal memuat dataset: {e}")
        st.stop()

# ----------------- SIDEBAR PANEL -----------------

st.sidebar.markdown("<div style='color: #E50914; font-family: Outfit; font-size: 2rem; font-weight: 900; letter-spacing:-1px; text-transform:uppercase; margin-bottom: 1rem;'>MOVIEFLIX</div>", unsafe_allow_html=True)
st.sidebar.subheader("Pilih Film Favorit Anda")

# Get unique genres list
all_genres = movies_df['genres'].str.split('|').explode()
unique_genres = sorted(all_genres[(all_genres != '(no genres listed)') & (all_genres.notna())].unique().tolist())

selected_genre = st.sidebar.selectbox(
    "Filter berdasarkan Genre:",
    options=["Semua Genre"] + unique_genres
)

# Filter movies based on selected genre
if selected_genre != "Semua Genre":
    filtered_df = movies_df[movies_df['genres'].str.contains(selected_genre, case=False, na=False)]
else:
    filtered_df = movies_df

# Setup selectbox for movie selection based on filtered list
movie_titles = filtered_df['title'].tolist()
movie_to_id = dict(zip(filtered_df['title'], filtered_df['movieId']))

if len(movie_titles) > 0:
    options_list = ["Semua"] + movie_titles
    selected_title = st.sidebar.selectbox(
        "Cari judul film:",
        options=options_list,
        index=0,
        key=f"movie_select_{selected_genre}"
    )
    if selected_title == "Semua":
        is_browse_mode = True
    else:
        is_browse_mode = False
        selected_movie_id = movie_to_id[selected_title]
        selected_movie_info = movies_df[movies_df['movieId'] == selected_movie_id].iloc[0]
else:
    st.sidebar.warning("Tidak ada film di genre ini.")
    st.stop()

# Tampilkan semua rekomendasi yang relevan (dibatasi 24 film demi performa pemuatan gambar)
top_n = 24

st.sidebar.markdown("---")

# ----------------- MAIN PAGES & HERO BANNER -----------------

st.markdown("<div class='brand-logo'>Movieflix</div>", unsafe_allow_html=True)
st.markdown("<div class='brand-sub'>Sistem rekomendasi film cerdas dengan citra poster dan sinopsis sinematik</div>", unsafe_allow_html=True)

if not is_browse_mode:
    # Fetch Selected Movie Poster & Description
    with st.spinner("Mengunduh poster film terpilih..."):
        selected_poster, selected_desc = get_movie_details_cached(selected_movie_info['tmdbId'])

    # Render Cinema Hero Banner (Netflix Style)
    is_in_cf = selected_movie_id in item_sim_df.index
    cf_status_text = "POPULER DI USER" if is_in_cf else "KLASIK/INDIE"
    selected_stars = "".join(["★" for _ in range(int(round(selected_movie_info['avg_rating'])))]) + "".join(["☆" for _ in range(5 - int(round(selected_movie_info['avg_rating'])))])

    st.markdown("### 🎬 Film Terpilih")
    col_hero_p, col_hero_d = st.columns([1, 4])
    with col_hero_p:
        st.markdown(f"""
        <div class='hero-poster-container'>
            <img src='{selected_poster}' style='width: 100%; aspect-ratio: 2/3; object-fit: cover; display: block;'>
        </div>
        """, unsafe_allow_html=True)

    with col_hero_d:
        selected_genres = selected_movie_info['genres'].split('|')
        genre_badges = "".join([f"<span class='genre-badge'>{g}</span>" for g in selected_genres])
        
        st.markdown(f"""
        <div class='hero-banner'>
            <div class='hero-title'>{selected_movie_info['title']}</div>
            <div class='hero-meta'>
                <span class='hero-year'>{selected_movie_info['year'] if selected_movie_info['year'] > 0 else 'N/A'}</span>
                <span style='color: #fbbf24; font-weight: bold;'>{selected_stars} {selected_movie_info['avg_rating']:.2f}/5.0</span>
                <span style='color: #888;'>({int(selected_movie_info['num_ratings']):,} voting)</span>
                <span class='hero-match'>98% Cocok</span>
                <span class='hero-cf-badge'>{cf_status_text}</span>
            </div>
            <div class='hero-desc'>{selected_desc}</div>
            <div style='margin-top: 1rem;'>
                <span style='color: #999; font-size: 0.9rem; font-weight: bold; margin-right: 0.5rem;'>GENRE:</span>
                {genre_badges}
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown(f"### 🎬 Kategori Film: {selected_genre}")

# Tabs Navigation
tab1, tab2, tab3 = st.tabs([
    "🎯 Rekomendasi Genre Serupa (Content-Based)", 
    "👥 Rekomendasi Pilihan Penonton (Collaborative)", 
    "📊 Analitik Dataset"
])

# ----------------- TAB 1: CONTENT-BASED FILTERING -----------------
with tab1:
    if is_browse_mode:
        st.markdown(f"#### Jelajahi Semua Film Terpopuler - {selected_genre}")
        st.write(f"Daftar film paling populer di genre **{selected_genre}** berdasarkan jumlah rating terbanyak dari penonton.")
        
        # Get top 24 movies in this genre sorted by num_ratings descending
        browse_movies = filtered_df.sort_values(by='num_ratings', ascending=False).head(top_n)
        
        if browse_movies.empty:
            st.info("Tidak ada film yang ditemukan untuk kategori ini.")
        else:
            with st.spinner("Mengunduh poster film..."):
                browse_details = load_details_in_parallel(browse_movies)
                
            cols = st.columns(4)
            for i, row in enumerate(browse_movies.itertuples()):
                col_target = cols[i % 4]
                poster_url, description = browse_details[i]
                
                item_stars = "".join(["★" for _ in range(int(round(row.avg_rating)))]) + "".join(["☆" for _ in range(5 - int(round(row.avg_rating)))])
                item_genres = row.genres.split('|')[:3]
                genres_html = "".join([f"<span class='genre-badge'>{g}</span>" for g in item_genres])
                
                with col_target:
                    st.markdown(f"""
                    <div class='movie-card'>
                        <div class='movie-card-img-container'>
                            <img class='movie-card-img' src='{poster_url}'>
                        </div>
                        <div class='movie-card-content'>
                            <div class='card-title'>{row.title}</div>
                            <div class='card-meta'>
                                <span style='color: #E50914; font-weight: bold; font-size: 0.85rem;'>TRENDING</span>
                                <span class='card-year'>{row.year if row.year > 0 else 'N/A'}</span>
                            </div>
                            <div class='card-rating-row'>
                                {item_stars} <span style='color: #cbd5e1; font-weight: bold;'>{row.avg_rating:.1f}</span>
                                <span style='color: #777; font-size: 0.75rem;'>({int(row.num_ratings):,})</span>
                            </div>
                            <div class='card-desc'>{description}</div>
                            <div class='card-genres'>{genres_html}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='margin-bottom: 0.2rem;'>Karena Anda Menonton " + selected_movie_info['title'] + "</h3>", unsafe_allow_html=True)
        st.write("Rekomendasi genre sejenis berdasarkan kemiripan representasi teks TF-IDF.")
        
        with st.spinner("Menghitung rekomendasi genre..."):
            recs_content = recommender.recommend_by_content(selected_movie_id, movies_df, tfidf_matrix, top_n)
            
        if recs_content.empty:
            st.info("Tidak ada rekomendasi content-based yang ditemukan.")
        else:
            # Fetch posters/descriptions concurrently
            with st.spinner("Mengunduh poster film rekomendasi..."):
                recs_details = load_details_in_parallel(recs_content)
                
            # Display as a Netflix Grid (4 columns)
            cols = st.columns(4)
            for i, row in enumerate(recs_content.itertuples()):
                col_target = cols[i % 4]
                poster_url, description = recs_details[i]
                
                # Format rating stars
                item_stars = "".join(["★" for _ in range(int(round(row.avg_rating)))]) + "".join(["☆" for _ in range(5 - int(round(row.avg_rating)))])
                match_pct = int(row.similarity * 100)
                
                item_genres = row.genres.split('|')[:3] # Show max 3 genres on card
                genres_html = "".join([f"<span class='genre-badge'>{g}</span>" for g in item_genres])
                
                with col_target:
                    st.markdown(f"""
                    <div class='movie-card'>
                        <div class='movie-card-img-container'>
                            <img class='movie-card-img' src='{poster_url}'>
                        </div>
                        <div class='movie-card-content'>
                            <div class='card-title'>{row.title}</div>
                            <div class='card-meta'>
                                <span class='card-match'>{match_pct}% Match</span>
                                <span class='card-year'>{row.year if row.year > 0 else 'N/A'}</span>
                            </div>
                            <div class='card-rating-row'>
                                {item_stars} <span style='color: #cbd5e1; font-weight: bold;'>{row.avg_rating:.1f}</span>
                                <span style='color: #777; font-size: 0.75rem;'>({int(row.num_ratings):,})</span>
                            </div>
                            <div class='card-desc'>{description}</div>
                            <div class='card-genres'>{genres_html}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# ----------------- TAB 2: COLLABORATIVE FILTERING -----------------
with tab2:
    if is_browse_mode:
        st.markdown("#### Film Terpopuler Sepanjang Masa (Semua Kategori)")
        st.write("Saran film paling populer dan memiliki ulasan terbanyak dari seluruh kategori/genre di database MovieLens.")
        
        # Get overall top 24 movies sorted by num_ratings descending
        browse_overall = movies_df.sort_values(by='num_ratings', ascending=False).head(top_n)
        
        if browse_overall.empty:
            st.info("Tidak ada film terpopuler yang ditemukan.")
        else:
            with st.spinner("Mengunduh poster film terpopuler..."):
                browse_details_overall = load_details_in_parallel(browse_overall)
                
            cols = st.columns(4)
            for i, row in enumerate(browse_overall.itertuples()):
                col_target = cols[i % 4]
                poster_url, description = browse_details_overall[i]
                
                item_stars = "".join(["★" for _ in range(int(round(row.avg_rating)))]) + "".join(["☆" for _ in range(5 - int(round(row.avg_rating)))])
                
                item_genres = row.genres.split('|')[:3]
                genres_html = "".join([f"<span class='genre-badge'>{g}</span>" for g in item_genres])
                
                with col_target:
                    st.markdown(f"""
                    <div class='movie-card'>
                        <div class='movie-card-img-container'>
                            <img class='movie-card-img' src='{poster_url}'>
                        </div>
                        <div class='movie-card-content'>
                            <div class='card-title'>{row.title}</div>
                            <div class='card-meta'>
                                <span style='color: #46d369; font-weight: bold; font-size: 0.85rem;'>TRENDING GLOBAL</span>
                                <span class='card-year'>{row.year if row.year > 0 else 'N/A'}</span>
                            </div>
                            <div class='card-rating-row'>
                                {item_stars} <span style='color: #cbd5e1; font-weight: bold;'>{row.avg_rating:.1f}</span>
                                <span style='color: #777; font-size: 0.75rem;'>({int(row.num_ratings):,})</span>
                            </div>
                            <div class='card-desc'>{description}</div>
                            <div class='card-genres'>{genres_html}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='margin-bottom: 0.2rem;'>Rekomendasi Lain yang Mungkin Anda Sukai</h3>", unsafe_allow_html=True)
        st.write("Saran film berdasarkan pola kesamaan rating dari pengguna lain di database MovieLens.")
        
        if not is_in_cf:
            st.warning("""
            ⚠️ **Film ini belum populer di database kami.**
            
            Sistem Collaborative Filtering kami memerlukan minimal 4.000 rating untuk memproses rekomendasi yang akurat.
            Silakan beralih ke tab **Rekomendasi Genre Serupa** atau pilih film populer (seperti Toy Story, Inception, Pulp Fiction, dll) untuk melihat hasil collaborative.
            """)
        else:
            with st.spinner("Mencari kecocokan pola rating..."):
                recs_collab = recommender.recommend_by_collaborative(selected_movie_id, item_sim_df, movies_df, top_n)
                
            if recs_collab.empty:
                st.info("Tidak ada rekomendasi collaborative yang ditemukan.")
            else:
                with st.spinner("Mengunduh poster film rekomendasi..."):
                    recs_details = load_details_in_parallel(recs_collab)
                    
                cols = st.columns(4)
                for i, row in enumerate(recs_collab.itertuples()):
                    col_target = cols[i % 4]
                    poster_url, description = recs_details[i]
                    
                    # Format rating stars
                    item_stars = "".join(["★" for _ in range(int(round(row.avg_rating)))]) + "".join(["☆" for _ in range(5 - int(round(row.avg_rating)))])
                    match_pct = int(row.similarity * 100)
                    
                    item_genres = row.genres.split('|')[:3]
                    genres_html = "".join([f"<span class='genre-badge'>{g}</span>" for g in item_genres])
                    
                    with col_target:
                        st.markdown(f"""
                        <div class='movie-card'>
                            <div class='movie-card-img-container'>
                                <img class='movie-card-img' src='{poster_url}'>
                            </div>
                            <div class='movie-card-content'>
                                <div class='card-title'>{row.title}</div>
                                <div class='card-meta'>
                                    <span class='card-match'>{match_pct}% Cocok</span>
                                    <span class='card-year'>{row.year if row.year > 0 else 'N/A'}</span>
                                </div>
                                <div class='card-rating-row'>
                                    {item_stars} <span style='color: #cbd5e1; font-weight: bold;'>{row.avg_rating:.1f}</span>
                                    <span style='color: #777; font-size: 0.75rem;'>({int(row.num_ratings):,})</span>
                                </div>
                                <div class='card-desc'>{description}</div>
                                <div class='card-genres'>{genres_html}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

# ----------------- TAB 3: STATS & INSIGHTS -----------------
with tab3:
    st.markdown("### Statistik Ringkas Data MovieLens 32M")
    
    # Grid of Metrics
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown(f"""
        <div class='metric-box'>
            <div style='font-size: 2rem; font-weight: 800; color: #E50914;'>{len(movies_df):,}</div>
            <div style='font-size: 0.85rem; color: #888; text-transform: uppercase;'>Total Film terindeks</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown("""
        <div class='metric-box'>
            <div style='font-size: 2rem; font-weight: 800; color: #E50914;'>32,000,204</div>
            <div style='font-size: 0.85rem; color: #888; text-transform: uppercase;'>Total rating user</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""
        <div class='metric-box'>
            <div style='font-size: 2rem; font-weight: 800; color: #E50914;'>{item_sim_df.shape[0]:,}</div>
            <div style='font-size: 0.85rem; color: #888; text-transform: uppercase;'>Film Populer (Model CF)</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m4:
        st.markdown("""
        <div class='metric-box'>
            <div style='font-size: 2rem; font-weight: 800; color: #E50914;'>26,179</div>
            <div style='font-size: 0.85rem; color: #888; text-transform: uppercase;'>User Aktif (Model CF)</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Distribusi Rilis Film Berdasarkan Dekade")
        valid_years = movies_df[movies_df['year'] > 0]['year']
        
        fig, ax = plt.subplots(figsize=(8, 4), facecolor='#141414')
        ax.set_facecolor('#141414')
        
        sns.histplot(valid_years, bins=30, kde=True, color='#E50914', ax=ax)
        
        # Style adjustments for dark theme
        ax.tick_params(colors='#aaaaaa')
        ax.xaxis.label.set_color('#aaaaaa')
        ax.yaxis.label.set_color('#aaaaaa')
        ax.set_xlabel("Tahun Rilis", fontsize=10)
        ax.set_ylabel("Jumlah Film", fontsize=10)
        ax.spines['bottom'].set_color('#2f2f2f')
        ax.spines['left'].set_color('#2f2f2f')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        
        st.pyplot(fig)
        
    with col_chart2:
        st.subheader("Top 10 Genre Film Paling Dominan")
        all_genres = movies_df['genres'].str.split('|').explode()
        all_genres = all_genres[all_genres != '(no genres listed)']
        genre_counts = all_genres.value_counts().head(10)
        
        fig, ax = plt.subplots(figsize=(8, 4), facecolor='#141414')
        ax.set_facecolor('#141414')
        
        # Use single hue argument to avoid seaborn warnings
        sns.barplot(x=genre_counts.values, y=genre_counts.index, hue=genre_counts.index, palette='rocket', legend=False, ax=ax)
        
        ax.tick_params(colors='#aaaaaa')
        ax.xaxis.label.set_color('#aaaaaa')
        ax.yaxis.label.set_color('#aaaaaa')
        ax.set_xlabel("Jumlah Film", fontsize=10)
        ax.set_ylabel("Genre", fontsize=10)
        ax.spines['bottom'].set_color('#2f2f2f')
        ax.spines['left'].set_color('#2f2f2f')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        
        st.pyplot(fig)
