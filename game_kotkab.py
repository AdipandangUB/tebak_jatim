import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import json
import os
import pandas as pd
from datetime import datetime
import time
import base64

# Konfigurasi halaman
st.set_page_config(
    page_title="Tebak Jawa Timur", 
    page_icon="🧩", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fungsi untuk mendapatkan background image sebagai base64
def get_background_image_html(image_url):
    """Mengembalikan HTML untuk background image"""
    return f"""
    <style>
    [data-testid="stSidebar"] {{
        background-image: url("{image_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    [data-testid="stSidebar"]::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.6);
        z-index: 0;
    }}
    
    [data-testid="stSidebar"] > div:first-child {{
        position: relative;
        z-index: 1;
        background-color: transparent !important;
    }}
    
    [data-testid="stSidebar"] .stImage,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] h5,
    [data-testid="stSidebar"] h6,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stRadio > div,
    [data-testid="stSidebar"] .stButton > button {{
        color: white !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
    }}
    
    [data-testid="stSidebar"] .stRadio > div {{
        background-color: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 10px;
        backdrop-filter: blur(5px);
    }}
    
    [data-testid="stSidebar"] .stRadio label {{
        color: white !important;
    }}
    
    [data-testid="stSidebar"] .stButton > button {{
        background-color: rgba(102, 126, 234, 0.8);
        color: white !important;
        border: 1px solid rgba(255,255,255,0.3);
        backdrop-filter: blur(5px);
    }}
    
    [data-testid="stSidebar"] .stButton > button:hover {{
        background-color: rgba(102, 126, 234, 1);
        border: 1px solid white;
    }}
    
    [data-testid="stSidebar"] [data-testid="stMetricValue"],
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {{
        color: white !important;
    }}
    
    [data-testid="stSidebar"] .streamlit-expanderHeader {{
        color: white !important;
        background-color: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
    }}
    
    [data-testid="stSidebar"] .streamlit-expanderContent {{
        background-color: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(5px);
        border-radius: 0 0 10px 10px;
    }}
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {{
        color: white !important;
    }}
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {{
        background-color: rgba(255, 255, 255, 0.2);
        border-color: rgba(255,255,255,0.3);
    }}
    
    [data-testid="stSidebar"] .stSlider label {{
        color: white !important;
    }}
    
    [data-testid="stSidebar"] hr {{
        border-color: rgba(255,255,255,0.3);
    }}
    </style>
    """

# Fungsi untuk mendapatkan background footer dengan kontrol brightness
def get_footer_background_html(image_url, brightness=0.7):
    """Mengembalikan HTML untuk background footer"""
    overlay_opacity = 1 - brightness
    overlay_color = f"rgba(0, 0, 0, {overlay_opacity})"
    
    return f"""
    <style>
    .footer-container {{
        position: relative;
        width: 100%;
        margin-top: 30px;
        padding: 20px 0;
        background-image: url("{image_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        border-radius: 15px 15px 0 0;
        overflow: hidden;
    }}
    
    .footer-container::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, {overlay_color} 0%, rgba(0,0,0,{overlay_opacity-0.2}) 100%);
        z-index: 1;
    }}
    
    .footer-container {{
        filter: brightness({brightness});
    }}
    
    .footer-content {{
        position: relative;
        z-index: 2;
        color: white;
        text-align: center;
        padding: 15px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        filter: brightness(1);
    }}
    
    .footer-content p {{
        margin: 5px 0;
        font-size: 14px;
    }}
    
    .footer-content .footer-title {{
        font-size: 16px;
        font-weight: bold;
        color: #ffd700;
        margin-bottom: 10px;
    }}
    
    .footer-content .footer-link {{
        color: #ffd700;
        text-decoration: none;
        font-weight: bold;
    }}
    
    .footer-content .footer-link:hover {{
        text-decoration: underline;
        color: #ffaa00;
    }}
    
    .footer-divider {{
        height: 3px;
        background: linear-gradient(90deg, transparent, #ffd700, transparent);
        margin: 20px 0 10px 0;
    }}
    </style>
    """

def create_footer_with_background(footer_text, image_url, brightness=0.7):
    """Membuat footer HTML"""
    current_time = datetime.now().strftime("%H:%M:%S")
    
    return f"""
    <div class="footer-divider"></div>
    <div class="footer-container" style="filter: brightness({brightness});">
        <div class="footer-content" style="filter: brightness(1);">
            <div class="footer-title">🧩 Tebak Jawa Timur</div>
            <p>{footer_text}</p>
            <p>⏰ {current_time} WIB | © 2026 Tebak Jawa Timur | Versi 2.3.0</p>
            <p>Fitur: Game Tebak Wilayah | Mode Belajar | Bromo 3D | Papan Skor | Statistik Waktu</p>
            <p style="font-size: 12px; margin-top: 10px;">
                <a href="#" class="footer-link">Tentang</a> | 
                <a href="#" class="footer-link">Kebijakan Privasi</a> | 
                <a href="#" class="footer-link">Kontak</a>
            </p>
        </div>
    </div>
    """

# OPTIMASI: Gunakan data GeoJSON JATIM yang sudah difilter (lebih kecil)
# Buat data GeoJSON sederhana untuk Jawa Timur (hanya 38 wilayah)
@st.cache_data(ttl=3600)  # Cache selama 1 jam
def load_jatim_geojson():
    """
    Memuat data GeoJSON Jawa Timur.
    Jika file besar, gunakan data minimal yang sudah difilter.
    """
    GEOJSON_FILE = "38 Provinsi Indonesia - Kabupaten.json"
    
    # Cek apakah file ada
    if not os.path.exists(GEOJSON_FILE):
        st.error(f"File {GEOJSON_FILE} tidak ditemukan!")
        return None
    
    try:
        # Baca file dengan streaming (lebih efisien)
        with open(GEOJSON_FILE, 'r', encoding='utf-8') as f:
            # OPTIMASI: Baca sebagian file jika terlalu besar
            data = json.load(f)
        
        # Filter hanya Jawa Timur
        if data.get('type') == 'FeatureCollection':
            features = data.get('features', [])
            
            # Filter fitur Jawa Timur
            jatim_features = []
            for feature in features:
                props = feature.get('properties', {})
                if props.get('WADMPR') == 'Jawa Timur':
                    kab_kota = props.get('WADMKK', '')
                    if kab_kota:
                        # OPTIMASI: Buat feature baru dengan data minimal
                        new_feature = {
                            "type": "Feature",
                            "properties": {
                                "name": kab_kota,
                                "WADMKK": kab_kota,
                                "WADMPR": "Jawa Timur"
                            },
                            "geometry": feature.get("geometry", {})
                        }
                        jatim_features.append(new_feature)
            
            # Buat GeoJSON baru
            jatim_geojson = {
                "type": "FeatureCollection",
                "features": jatim_features
            }
            
            return jatim_geojson
        else:
            st.error("Format GeoJSON tidak valid")
            return None
            
    except Exception as e:
        st.error(f"Error membaca file: {str(e)}")
        return None

# OPTIMASI: Gunakan data wilayah yang sudah diekstrak
@st.cache_data(ttl=3600)
def extract_wilayah_list(geojson_data):
    """Ekstrak daftar wilayah dari GeoJSON"""
    if not geojson_data:
        return [], [], []
    
    wilayah_set = set()
    for feat in geojson_data.get('features', []):
        name = feat["properties"].get("name", "")
        if name:
            wilayah_set.add(name)
    
    wilayah_list = sorted(list(wilayah_set))
    kota_list = [w for w in wilayah_list if w.startswith('Kota ')]
    kab_list = [w for w in wilayah_list if w.startswith('Kabupaten ')]
    
    return wilayah_list, kota_list, kab_list

# Nama file
SCOREBOARD_FILE = "scoreboard.json"

# URL background
SIDEBAR_BACKGROUND_URL = "https://rayadventure.com/wp-content/uploads/2018/06/tempat-wisata-di-jawa-timur.jpg"
FOOTER_BACKGROUND_URL = "https://awsimages.detik.net.id/community/media/visual/2025/05/08/peta-jawa-timur-1746688646408_169.jpeg?w=1200"

# Inisialisasi session state
if "footer_brightness" not in st.session_state:
    st.session_state.footer_brightness = 0.7

# OPTIMASI: Load data dengan progress indicator
with st.spinner("Memuat peta Jawa Timur..."):
    jatim_geojson = load_jatim_geojson()

if jatim_geojson is None:
    st.error("Gagal memuat data peta. Silakan refresh halaman.")
    st.stop()

# Ekstrak daftar wilayah
wilayah_list, kota_list, kab_list = extract_wilayah_list(jatim_geojson)

if not wilayah_list:
    st.error("Tidak ada data wilayah ditemukan")
    st.stop()

# ==================== FUNGSI PAPAN SKOR ====================

def load_scoreboard():
    """Memuat data papan skor dari file"""
    if os.path.exists(SCOREBOARD_FILE):
        try:
            with open(SCOREBOARD_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                return []
        except:
            return []
    else:
        save_scoreboard([])
        return []

def save_scoreboard(scoreboard):
    """Menyimpan data papan skor"""
    try:
        if not isinstance(scoreboard, list):
            scoreboard = []
        
        scoreboard.sort(key=lambda x: (-x.get("skor", 0), -x.get("timestamp", 0)))
        scoreboard = scoreboard[:10]
        
        os.makedirs(os.path.dirname(SCOREBOARD_FILE) if os.path.dirname(SCOREBOARD_FILE) else '.', exist_ok=True)
        
        with open(SCOREBOARD_FILE, 'w', encoding='utf-8') as f:
            json.dump(scoreboard, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

def add_score(nama, skor, level, total_soal, waktu_mulai=None, waktu_selesai=None):
    """Menambahkan skor baru"""
    try:
        if not nama or not isinstance(skor, (int, float)):
            return False
        
        scoreboard = load_scoreboard()
        
        durasi = None
        if waktu_mulai and waktu_selesai:
            durasi_detik = waktu_selesai - waktu_mulai
            durasi = {
                "detik": round(durasi_detik, 1),
                "format": f"{int(durasi_detik // 60)} menit {int(durasi_detik % 60)} detik"
            }
        
        new_entry = {
            "nama": str(nama),
            "skor": int(skor),
            "level": str(level),
            "total_soal": int(total_soal),
            "persentase": round((int(skor) / int(total_soal)) * 100, 1),
            "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tanggal_only": datetime.now().strftime("%Y-%m-%d"),
            "timestamp": time.time(),
            "durasi": durasi
        }
        
        scoreboard.append(new_entry)
        return save_scoreboard(scoreboard)
    except:
        return False

def get_filtered_scoreboard(level_filter="Semua Level", time_filter="Semua Waktu"):
    """Mendapatkan papan skor dengan filter"""
    scoreboard = load_scoreboard()
    
    if level_filter != "Semua Level" and scoreboard:
        scoreboard = [s for s in scoreboard if s.get("level") == level_filter]
    
    if time_filter != "Semua Waktu" and scoreboard:
        now = datetime.now()
        if time_filter == "Hari Ini":
            today_str = now.strftime("%Y-%m-%d")
            scoreboard = [s for s in scoreboard if s.get("tanggal_only") == today_str]
        elif time_filter == "7 Hari Terakhir":
            seven_days_ago = now.timestamp() - (7 * 24 * 3600)
            scoreboard = [s for s in scoreboard if s.get("timestamp", 0) >= seven_days_ago]
    
    scoreboard.sort(key=lambda x: (-x.get("skor", 0), -x.get("timestamp", 0)))
    return scoreboard

def get_current_time_info():
    """Info waktu sekarang"""
    now = datetime.now()
    return {
        "tanggal_lengkap": now.strftime("%Y-%m-%d %H:%M:%S"),
        "tanggal": now.strftime("%Y-%m-%d"),
        "jam": now.strftime("%H:%M:%S"),
        "hari": now.strftime("%A"),
        "timestamp": time.time()
    }

# ==================== DATABASE INFORMASI WILAYAH ====================

@st.cache_data(ttl=3600)
def get_wilayah_info(nama_wilayah):
    """Info wilayah (dengan caching)"""
    
    info_database = {
        "Kabupaten Banyuwangi": {
            "geografis": "Terletak di ujung timur Pulau Jawa, berbatasan dengan Selat Bali.",
            "demografi": "Penduduk: ±1,7 juta jiwa. Mayoritas suku Osing.",
            "budaya": "Kesenian Gandrung Banyuwangi, Seblang.",
            "keunikan": "Kawah Ijen dengan api biru, Taman Nasional Alas Purwo.",
            "oleh_oleh": "Pisang agung, kopi khas Banyuwangi."
        },
        "Kabupaten Malang": {
            "geografis": "Wilayah pegunungan dengan udara sejuk.",
            "demografi": "Penduduk: ±2,6 juta jiwa. Mayoritas suku Jawa.",
            "budaya": "Tari Topeng Malangan.",
            "keunikan": "Kota Apel, wisata Jatim Park.",
            "oleh_oleh": "Apel Malang, keripik buah."
        },
        "Kota Malang": {
            "geografis": "Kota di dataran tinggi dengan suhu rata-rata 24°C.",
            "demografi": "Penduduk: ±900 ribu jiwa.",
            "budaya": "Budaya Arek yang dinamis.",
            "keunikan": "Arsitektur kolonial Belanda.",
            "oleh_oleh": "Keripik buah, bakso Malang."
        },
        "Kota Surabaya": {
            "geografis": "Kota pesisir utara, ibu kota Provinsi Jawa Timur.",
            "demografi": "Penduduk: ±3 juta jiwa.",
            "budaya": "Budaya Arek Surabaya, tari Remo.",
            "keunikan": "Kota Pahlawan, Tugu Pahlawan.",
            "oleh_oleh": "Kerupuk udang, sambal bu Rudy."
        },
        "Kota Batu": {
            "geografis": "Kota wisata pegunungan dengan udara sejuk.",
            "demografi": "Penduduk: ±200 ribu jiwa.",
            "budaya": "Budaya Jawa Timuran.",
            "keunikan": "Kota wisata, Jatim Park.",
            "oleh_oleh": "Apel Batu, susu murni."
        }
    }
    
    if nama_wilayah in info_database:
        return info_database[nama_wilayah]
    else:
        tipe = "Kota" if nama_wilayah.startswith("Kota ") else "Kabupaten"
        return {
            "geografis": f"{tipe} di Provinsi Jawa Timur.",
            "demografi": "Penduduk dengan keragaman budaya.",
            "budaya": "Memiliki kesenian tradisional.",
            "keunikan": "Memiliki destinasi wisata.",
            "oleh_oleh": "Produk makanan khas."
        }

# ==================== INISIALISASI SESSION STATE ====================

if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "name_submitted" not in st.session_state:
    st.session_state.name_submitted = False
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.total_questions = 0
    st.session_state.max_questions = 10
    st.session_state.current_region = None
    st.session_state.options = []
    st.session_state.feedback = ""
    st.session_state.answered = False
    st.session_state.correct_answer = ""
    st.session_state.game_over = False
    st.session_state.questions_asked = []
    st.session_state.game_started = False
    st.session_state.current_page = "Game"
    st.session_state.difficulty = "Normal"
    st.session_state.selected_wilayah_info = None
    st.session_state.score_saved = False
    st.session_state.game_start_time = None
    st.session_state.game_end_time = None
    st.session_state.question_start_time = None
    st.session_state.total_game_duration = 0
    st.session_state.question_times = []
    st.session_state.average_answer_time = 0
    st.session_state.session_start_time = time.time()

# ==================== FUNGSI WAKTU ====================

def start_game_timer():
    st.session_state.game_start_time = time.time()
    st.session_state.game_end_time = None

def start_question_timer():
    st.session_state.question_start_time = time.time()

def end_question_timer():
    if st.session_state.question_start_time:
        duration = time.time() - st.session_state.question_start_time
        st.session_state.question_times.append({
            "question_number": st.session_state.total_questions + 1,
            "duration": duration
        })
        total_time = sum(q["duration"] for q in st.session_state.question_times)
        st.session_state.average_answer_time = total_time / len(st.session_state.question_times)
        return duration
    return 0

def end_game_timer():
    if st.session_state.game_start_time:
        st.session_state.game_end_time = time.time()
        st.session_state.total_game_duration = st.session_state.game_end_time - st.session_state.game_start_time

def format_duration(seconds):
    if seconds is None:
        return "00:00"
    minutes = int(seconds // 60)
    seconds_remaining = int(seconds % 60)
    return f"{minutes:02d}:{seconds_remaining:02d}"

# ==================== FUNGSI GAME ====================

def pilih_wilayah():
    if st.session_state.total_questions >= st.session_state.max_questions:
        st.session_state.game_over = True
        return
    
    available_regions = [w for w in wilayah_list if w not in st.session_state.questions_asked]
    
    if not available_regions:
        st.session_state.questions_asked = []
        available_regions = wilayah_list
    
    target = random.choice(available_regions)
    st.session_state.questions_asked.append(target)
    st.session_state.correct_answer = target
    
    # Sesuaikan jumlah opsi
    if st.session_state.difficulty == "Mudah":
        num_options = 2
    elif st.session_state.difficulty == "Sulit":
        num_options = 6
    else:
        num_options = 4
    
    others = [w for w in wilayah_list if w != target]
    num_options = min(num_options, len(others))
    options = random.sample(others, num_options) + [target]
    random.shuffle(options)
    
    st.session_state.options = options
    st.session_state.current_region = target
    st.session_state.answered = False
    st.session_state.feedback = ""
    st.session_state.game_started = True
    
    start_question_timer()

def reset_game():
    st.session_state.score = 0
    st.session_state.total_questions = 0
    st.session_state.game_over = False
    st.session_state.questions_asked = []
    st.session_state.current_region = None
    st.session_state.feedback = ""
    st.session_state.answered = False
    st.session_state.game_started = False
    st.session_state.score_saved = False
    st.session_state.game_start_time = None
    st.session_state.game_end_time = None
    st.session_state.question_times = []
    st.session_state.average_answer_time = 0
    pilih_wilayah()

# Terapkan background
st.markdown(get_background_image_html(SIDEBAR_BACKGROUND_URL), unsafe_allow_html=True)
st.markdown(get_footer_background_html(FOOTER_BACKGROUND_URL, st.session_state.footer_brightness), unsafe_allow_html=True)

# ==================== INPUT NAMA ====================

if not st.session_state.name_submitted:
    with st.empty():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("https://img.freepik.com/vektor-premium/peta-yang-digambar-tangan-dari-provinsi-jawa-timur-indonesia-desain-kartun-garis-sederhana-modern_242622-498.jpg", width=150)
            
            time_info = get_current_time_info()
            st.markdown(f"""
            <div style="text-align: center; margin: 10px 0; color: #666;">
                {time_info['hari']}, {time_info['tanggal']} | {time_info['jam']}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="text-align: center;">
                <h1>🧩 Tebak Jawa Timur</h1>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("name_form"):
                name = st.text_input("Nama", placeholder="Masukkan nama Anda")
                
                if st.form_submit_button("🚀 Mulai Bermain", use_container_width=True):
                    if name.strip():
                        st.session_state.user_name = name.strip()
                        st.session_state.name_submitted = True
                        st.rerun()
                    else:
                        st.error("Nama tidak boleh kosong!")
    st.stop()

# ==================== SIDEBAR ====================

with st.sidebar:
    st.image("https://img.freepik.com/vektor-premium/peta-yang-digambar-tangan-dari-provinsi-jawa-timur-indonesia-desain-kartun-garis-sederhana-modern_242622-498.jpg", width=100)
    st.title("🧩 Tebak Jatim")
    
    time_info = get_current_time_info()
    st.markdown(f"""
    <div style="background: #667eea; padding: 8px; border-radius: 10px; text-align: center; color: white;">
        {time_info['hari']}, {time_info['tanggal']} | {time_info['jam']}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"👋 Halo, **{st.session_state.user_name}**!")
    
    menu_options = ["🎮 Game", "📚 Belajar", "🌋 Bromo 3D", "🏆 Papan Skor", "⚙️ Pengaturan"]
    selected_menu = st.radio(
        "Menu",
        menu_options,
        index=0,
        label_visibility="collapsed"
    )
    
    st.session_state.current_page = selected_menu.split(" ")[1]
    
    st.markdown("---")
    
    if st.button("🔄 Ganti Nama", use_container_width=True):
        st.session_state.name_submitted = False
        st.rerun()
    
    st.markdown("---")
    
    if "Game" in selected_menu:
        st.header("🎮 Game")
        
        if not st.session_state.game_started or st.session_state.game_over:
            if st.button("🎲 Mulai Game Baru", use_container_width=True):
                reset_game()
                st.rerun()
        else:
            if st.button("🔄 Reset Game", use_container_width=True):
                reset_game()
                st.rerun()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Skor", st.session_state.score)
        with col2:
            st.metric("Soal", f"{st.session_state.total_questions}/{st.session_state.max_questions}")
        
        if st.session_state.game_started and not st.session_state.game_over:
            if st.session_state.game_start_time:
                current_duration = time.time() - st.session_state.game_start_time
                st.metric("⏱️ Waktu", format_duration(current_duration))
    
    elif "Papan Skor" in selected_menu:
        st.header("🏆 Papan Skor")
        
        level_filter = st.selectbox(
            "Level:",
            ["Semua Level", "Mudah", "Normal", "Sulit"]
        )
        
        time_filter = st.selectbox(
            "Waktu:",
            ["Semua Waktu", "Hari Ini", "7 Hari Terakhir"]
        )
        
        scoreboard = get_filtered_scoreboard(level_filter, time_filter)
        st.metric("Total Pemain", len(scoreboard))
    
    elif "Pengaturan" in selected_menu:
        st.header("⚙️ Pengaturan")
        st.session_state.max_questions = st.slider(
            "Jumlah Soal",
            5, 20, st.session_state.max_questions, 5
        )
        
        new_brightness = st.slider(
            "Brightness Footer",
            0.3, 1.0, st.session_state.footer_brightness, 0.05
        )
        
        if new_brightness != st.session_state.footer_brightness:
            st.session_state.footer_brightness = new_brightness
            st.rerun()

# ==================== KONTEN UTAMA ====================

if "Game" in selected_menu:
    st.title("🧩 Tebak Bentuk Wilayah")
    
    # Buat peta
    m = folium.Map(
        location=[-7.5, 112.3], 
        zoom_start=8,
        tiles=None,
        control_scale=True
    )
    
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite'
    ).add_to(m)
    
    def style_function(feature):
        name = feature["properties"]["name"]
        if st.session_state.game_started and not st.session_state.game_over and name == st.session_state.current_region:
            return {
                "fillColor": "#ff0000",
                "color": "#ff0000",
                "weight": 3,
                "fillOpacity": 0.7
            }
        else:
            return {
                "fillColor": "#3388ff" if st.session_state.game_started else "#cccccc",
                "color": "#ffffff",
                "weight": 1.5,
                "fillOpacity": 0.3 if st.session_state.game_started else 0.1
            }
    
    folium.GeoJson(
        jatim_geojson,
        style_function=style_function
    ).add_to(m)
    
    st_folium(m, width=None, height=500, use_container_width=True)
    
    # Kontrol game
    if not st.session_state.game_started and not st.session_state.game_over:
        if st.button("🎮 Mulai Game", use_container_width=True):
            start_game_timer()
            pilih_wilayah()
            st.rerun()
    
    elif st.session_state.game_over:
        end_game_timer()
        
        st.markdown("## 🎮 Game Selesai!")
        st.markdown(f"### Skor: **{st.session_state.score}/{st.session_state.max_questions}**")
        
        if st.session_state.total_game_duration > 0:
            st.info(f"⏱️ Waktu: {format_duration(st.session_state.total_game_duration)}")
        
        if st.session_state.score == st.session_state.max_questions:
            st.balloons()
        
        # Form simpan skor
        if not st.session_state.score_saved and st.session_state.score > 0:
            with st.form("save_score"):
                st.markdown(f"Nama: **{st.session_state.user_name}**")
                st.markdown(f"Skor: **{st.session_state.score}/{st.session_state.max_questions}**")
                
                if st.form_submit_button("💾 Simpan Skor"):
                    if add_score(
                        st.session_state.user_name, 
                        st.session_state.score, 
                        st.session_state.difficulty, 
                        st.session_state.max_questions,
                        st.session_state.game_start_time,
                        st.session_state.game_end_time
                    ):
                        st.session_state.score_saved = True
                        st.success("Skor tersimpan!")
                        st.rerun()
        
        if st.button("🔄 Main Lagi", use_container_width=True):
            reset_game()
            st.rerun()
    
    elif st.session_state.game_started:
        st.markdown(f"### Soal {st.session_state.total_questions + 1}/{st.session_state.max_questions}")
        st.markdown("**Wilayah manakah yang disorot MERAH?**")
        
        if st.session_state.question_start_time:
            current_time = time.time() - st.session_state.question_start_time
            st.progress(min(current_time / 60, 1.0), text=f"Waktu: {current_time:.1f} detik")
        
        # Tombol jawaban
        cols = st.columns(2)
        answer = None
        
        for i, opt in enumerate(st.session_state.options):
            with cols[i % 2]:
                if st.button(opt, key=f"ans_{i}", disabled=st.session_state.answered, use_container_width=True):
                    answer = opt
        
        if answer and not st.session_state.answered:
            question_time = end_question_timer()
            st.session_state.total_questions += 1
            
            if answer == st.session_state.correct_answer:
                st.session_state.score += 1
                st.session_state.feedback = f"✅ Benar! ({question_time:.1f} detik)"
            else:
                st.session_state.feedback = f"❌ Salah, jawabannya {st.session_state.correct_answer}"
            
            st.session_state.answered = True
            st.rerun()
        
        if st.session_state.feedback:
            st.markdown(f"### {st.session_state.feedback}")
            
            if st.session_state.answered and st.session_state.total_questions < st.session_state.max_questions:
                if st.button("➡️ Soal Berikutnya", use_container_width=True):
                    pilih_wilayah()
                    st.rerun()

elif "Belajar" in selected_menu:
    st.title("📚 Mode Belajar")
    st.markdown("Klik wilayah pada peta untuk melihat informasi")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        m = folium.Map(
            location=[-7.5, 112.3], 
            zoom_start=8,
            control_scale=True
        )
        
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri'
        ).add_to(m)
        
        geojson_layer = folium.GeoJson(
            jatim_geojson,
            style_function=lambda x: {
                "fillColor": "#33cc33",
                "color": "#ffffff",
                "weight": 1.5,
                "fillOpacity": 0.5
            },
            tooltip=folium.GeoJsonTooltip(
                fields=["name"], 
                aliases=["Klik untuk info:"]
            ),
            highlight_function=lambda x: {"fillColor": "#ffaa00", "fillOpacity": 0.7}
        ).add_to(m)
        
        map_data = st_folium(m, width=None, height=500, use_container_width=True)
        
        if map_data and map_data.get("last_active_drawing"):
            last_click = map_data["last_active_drawing"]
            if last_click and "properties" in last_click:
                st.session_state.selected_wilayah_info = last_click["properties"]["name"]
                st.rerun()
    
    with col2:
        st.markdown("## 📋 Info Wilayah")
        
        if st.session_state.selected_wilayah_info:
            wilayah = st.session_state.selected_wilayah_info
            info = get_wilayah_info(wilayah)
            
            st.markdown(f"### 📍 {wilayah}")
            
            tabs = st.tabs(["🗺️ Geografis", "👥 Demografi", "🎭 Budaya", "✨ Keunikan", "🛍️ Oleh-oleh"])
            
            with tabs[0]:
                st.write(info["geografis"])
            with tabs[1]:
                st.write(info["demografi"])
            with tabs[2]:
                st.write(info["budaya"])
            with tabs[3]:
                st.write(info["keunikan"])
            with tabs[4]:
                st.write(info["oleh_oleh"])
            
            if st.button("🔄 Klik wilayah lain"):
                st.session_state.selected_wilayah_info = None
                st.rerun()
        else:
            st.info("👆 Klik wilayah pada peta")

elif "Bromo" in selected_menu:
    st.title("🌋 Gunung Bromo 3D")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.components.v1.html("""
        <div style="width:100%; height:600px;">
            <iframe 
                src="https://sketchfab.com/models/72f1c983ba4040eab89d75eb2b0d3e32/embed" 
                style="width:100%; height:100%;" 
                frameborder="0" 
                allowfullscreen>
            </iframe>
        </div>
        """, height=620)
    
    with col2:
        st.markdown("### 📍 Informasi")
        st.markdown("""
        **Tinggi:** 2.329 m  
        **Status:** Aktif  
        **Lokasi:** Probolinggo, Pasuruan, Lumajang, Malang
        """)
        
        with st.expander("📖 Sejarah"):
            st.write("Gunung Bromo terbentuk dari letusan gunung berapi purba.")
        
        with st.expander("🎫 Tips"):
            st.write("Waktu terbaik: Mei-Oktober")

elif "Papan Skor" in selected_menu:
    st.title("🏆 Papan Skor")
    
    level_filter = st.session_state.get("scoreboard_level_filter", "Semua Level")
    time_filter = st.session_state.get("scoreboard_time_filter", "Semua Waktu")
    
    scoreboard = get_filtered_scoreboard(level_filter, time_filter)
    
    if scoreboard:
        df_data = []
        for i, player in enumerate(scoreboard[:10], 1):
            medals = {1: "👑", 2: "🥈", 3: "🥉"}
            avatar = medals.get(i, f"{i}.")
            
            nama = player.get("nama", "")
            if nama == st.session_state.user_name:
                nama = f"⭐ {nama} (Kamu)"
            
            df_data.append({
                "#": avatar,
                "Nama": nama,
                "Skor": f"{player.get('skor', 0)}/{player.get('total_soal', 0)}",
                "%": f"{player.get('persentase', 0)}%",
                "Level": player.get('level', '-'),
                "Tanggal": player.get('tanggal', '')[:10]
            })
        
        st.dataframe(
            pd.DataFrame(df_data),
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("Belum ada skor")
    
    # Skor pemain saat ini
    st.markdown("---")
    st.markdown(f"### Skor Kamu: **{st.session_state.user_name}**")
    st.write(f"{st.session_state.score}/{st.session_state.max_questions}")
    
    if st.session_state.score > 0 and not st.session_state.score_saved:
        if st.button("💾 Simpan Skor"):
            if add_score(
                st.session_state.user_name, 
                st.session_state.score, 
                st.session_state.difficulty, 
                st.session_state.max_questions,
                st.session_state.game_start_time,
                st.session_state.game_end_time
            ):
                st.session_state.score_saved = True
                st.success("Skor tersimpan!")
                st.rerun()

elif "Pengaturan" in selected_menu:
    st.title("⚙️ Pengaturan")
    
    tabs = st.tabs(["🎮 Game", "🎨 Tampilan"])
    
    with tabs[0]:
        st.number_input("Maks Soal", 5, 30, st.session_state.max_questions, key="max_q")
        st.selectbox("Kesulitan", ["Mudah", "Normal", "Sulit"], 
                    index=["Mudah", "Normal", "Sulit"].index(st.session_state.difficulty), 
                    key="diff")
        
        if st.button("Simpan"):
            st.session_state.max_questions = st.session_state.max_q
            st.session_state.difficulty = st.session_state.diff
            st.success("Tersimpan!")
    
    with tabs[1]:
        st.slider("Brightness Footer", 0.3, 1.0, st.session_state.footer_brightness, 0.05, key="bright")
        if st.session_state.bright != st.session_state.footer_brightness:
            st.session_state.footer_brightness = st.session_state.bright
            st.rerun()

# Footer
footer_text = {
    "Game": f"Tebak {len(wilayah_list)} Wilayah | Kesulitan: {st.session_state.difficulty}",
    "Belajar": f"Mode Belajar | {len(wilayah_list)} wilayah",
    "Bromo": "Gunung Bromo 3D",
    "Papan Skor": "Papan Skor",
    "Pengaturan": "Pengaturan"
}.get(st.session_state.current_page, "Tebak Jawa Timur")

st.markdown(create_footer_with_background(footer_text, FOOTER_BACKGROUND_URL, st.session_state.footer_brightness), unsafe_allow_html=True)
