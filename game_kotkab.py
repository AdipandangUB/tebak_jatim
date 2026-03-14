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
        background: rgba(0, 0, 0, 0.6);  /* Overlay gelap untuk keterbacaan teks */
        z-index: 0;
    }}
    
    [data-testid="stSidebar"] > div:first-child {{
        position: relative;
        z-index: 1;
        background-color: transparent !important;
    }}
    
    /* Style untuk elemen di sidebar agar tetap terbaca */
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
    
    /* Style khusus untuk radio button */
    [data-testid="stSidebar"] .stRadio > div {{
        background-color: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 10px;
        backdrop-filter: blur(5px);
    }}
    
    [data-testid="stSidebar"] .stRadio label {{
        color: white !important;
    }}
    
    /* Style untuk button di sidebar */
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
    
    /* Style untuk metric di sidebar */
    [data-testid="stSidebar"] [data-testid="stMetricValue"],
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {{
        color: white !important;
    }}
    
    /* Style untuk expander */
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
    
    /* Style untuk selectbox */
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {{
        color: white !important;
    }}
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {{
        background-color: rgba(255, 255, 255, 0.2);
        border-color: rgba(255,255,255,0.3);
    }}
    
    /* Style untuk slider */
    [data-testid="stSidebar"] .stSlider label {{
        color: white !important;
    }}
    
    /* Style untuk divider */
    [data-testid="stSidebar"] hr {{
        border-color: rgba(255,255,255,0.3);
    }}
    </style>
    """

# Fungsi untuk mendapatkan background footer dengan kontrol brightness
def get_footer_background_html(image_url, brightness=0.7):
    """
    Mengembalikan HTML untuk background footer dengan kontrol brightness
    brightness: nilai antara 0-1 (0: sangat gelap, 1: normal)
    """
    overlay_opacity = 1 - brightness  # Semakin tinggi brightness, semakin rendah opacity overlay
    overlay_color = f"rgba(0, 0, 0, {overlay_opacity})"
    
    return f"""
    <style>
    /* Style untuk footer dengan background */
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
    
    /* Efek brightness pada gambar background */
    .footer-container {{
        filter: brightness({brightness});
    }}
    
    /* Pastikan konten tidak terpengaruh filter brightness */
    .footer-content {{
        position: relative;
        z-index: 2;
        color: white;
        text-align: center;
        padding: 15px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        filter: brightness(1); /* Reset brightness untuk konten */
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
    
    /* Style untuk garis pemisah footer */
    .footer-divider {{
        height: 3px;
        background: linear-gradient(90deg, transparent, #ffd700, transparent);
        margin: 20px 0 10px 0;
    }}
    </style>
    """

# Fungsi untuk membuat footer dengan background dan kontrol brightness
def create_footer_with_background(footer_text, image_url, brightness=0.7):
    """Membuat footer HTML dengan background image dan kontrol brightness"""
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

# Load GeoJSON dari file
def load_geojson(filename):
    """Memuat file GeoJSON dari direktori yang sama"""
    try:
        # Cek apakah file ada
        if not os.path.exists(filename):
            st.error(f"File {filename} tidak ditemukan di direktori: {os.getcwd()}")
            st.info("Pastikan file GeoJSON berada di folder yang sama dengan script Python")
            return None
        
        # Baca file
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Verifikasi struktur
        if data.get('type') != 'FeatureCollection':
            st.error("Format GeoJSON tidak valid: harus FeatureCollection")
            return None
        
        return data
    except Exception as e:
        st.error(f"Error membaca file: {str(e)}")
        return None

# Nama file GeoJSON
GEOJSON_FILE = "38 Provinsi Indonesia - Kabupaten.json"  # Sesuaikan dengan nama file Anda
SCOREBOARD_FILE = "scoreboard.json"  # File untuk menyimpan data papan skor

# URL background
SIDEBAR_BACKGROUND_URL = "https://rayadventure.com/wp-content/uploads/2018/06/tempat-wisata-di-jawa-timur.jpg"
FOOTER_BACKGROUND_URL = "https://awsimages.detik.net.id/community/media/visual/2025/05/08/peta-jawa-timur-1746688646408_169.jpeg?w=1200"

# Inisialisasi session state untuk brightness footer
if "footer_brightness" not in st.session_state:
    st.session_state.footer_brightness = 0.7  # Nilai default brightness

# Load data GeoJSON
geojson_data = load_geojson(GEOJSON_FILE)

# Jika gagal load, tampilkan pesan error dan hentikan
if geojson_data is None:
    st.stop()

# Filter hanya wilayah di Jawa Timur
def filter_jatim_features(features):
    """Filter fitur yang berada di Provinsi Jawa Timur"""
    jatim_features = []
    for feature in features:
        props = feature.get('properties', {})
        # Cek apakah provinsi adalah Jawa Timur
        if props.get('WADMPR') == 'Jawa Timur':
            # Gunakan WADMKK sebagai nama kabupaten/kota
            kab_kota = props.get('WADMKK', '')
            if kab_kota:  # Hanya tambahkan jika ada nama
                # Buat salinan feature dengan properti yang dimodifikasi
                new_feature = feature.copy()
                new_feature['properties'] = {
                    'name': kab_kota,  # Gunakan nama kabupaten/kota
                    'WADMKK': kab_kota,
                    'WADMPR': 'Jawa Timur'
                }
                jatim_features.append(new_feature)
    
    return jatim_features

# Filter fitur Jawa Timur
jatim_features = filter_jatim_features(geojson_data.get('features', []))

# Buat GeoJSON baru untuk Jawa Timur
jatim_geojson = {
    "type": "FeatureCollection",
    "features": jatim_features
}

# Ekstrak daftar nama wilayah (unik)
wilayah_set = set()
for feat in jatim_features:
    name = feat["properties"]["name"]
    wilayah_set.add(name)

wilayah_list = sorted(list(wilayah_set))
kota_list = [w for w in wilayah_list if w.startswith('Kota ')]
kab_list = [w for w in wilayah_list if w.startswith('Kabupaten ')]

# ==================== FUNGSI PENTING UNTUK PAPAN SKOR ====================

# Fungsi untuk memuat papan skor dari file
def load_scoreboard():
    """Memuat data papan skor dari file JSON"""
    if os.path.exists(SCOREBOARD_FILE):
        try:
            with open(SCOREBOARD_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Validasi format data
                if isinstance(data, list):
                    return data
                else:
                    return []
        except json.JSONDecodeError:
            # Jika file corrupt, buat file baru
            save_scoreboard([])
            return []
        except Exception as e:
            st.error(f"Error loading scoreboard: {str(e)}")
            return []
    else:
        # Buat file baru jika belum ada
        save_scoreboard([])
        return []

# Fungsi untuk menyimpan papan skor ke file
def save_scoreboard(scoreboard):
    """Menyimpan data papan skor ke file JSON"""
    try:
        # Pastikan scoreboard adalah list
        if not isinstance(scoreboard, list):
            scoreboard = []
        
        # Urutkan berdasarkan skor (tertinggi) dan timestamp (terbaru)
        scoreboard.sort(key=lambda x: (-x.get("skor", 0), -x.get("timestamp", 0)))
        
        # Simpan hanya 10 teratas
        scoreboard = scoreboard[:10]
        
        # Buat direktori jika belum ada
        os.makedirs(os.path.dirname(SCOREBOARD_FILE) if os.path.dirname(SCOREBOARD_FILE) else '.', exist_ok=True)
        
        with open(SCOREBOARD_FILE, 'w', encoding='utf-8') as f:
            json.dump(scoreboard, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Error saving scoreboard: {str(e)}")
        return False

# Fungsi untuk menambah skor baru
def add_score(nama, skor, level, total_soal, waktu_mulai=None, waktu_selesai=None):
    """Menambahkan skor baru ke papan skor dengan informasi waktu"""
    try:
        # Validasi input
        if not nama or not isinstance(skor, (int, float)) or not isinstance(total_soal, (int, float)):
            return False
        
        scoreboard = load_scoreboard()
        
        # Hitung durasi bermain jika waktu tersedia
        durasi = None
        if waktu_mulai and waktu_selesai:
            durasi_detik = waktu_selesai - waktu_mulai
            durasi = {
                "detik": round(durasi_detik, 1),
                "menit": round(durasi_detik / 60, 1),
                "format": f"{int(durasi_detik // 60)} menit {int(durasi_detik % 60)} detik"
            }
        
        # Buat entri baru dengan berbagai informasi waktu
        new_entry = {
            "nama": str(nama),
            "skor": int(skor),
            "level": str(level),
            "total_soal": int(total_soal),
            "persentase": round((int(skor) / int(total_soal)) * 100, 1),
            "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tanggal_lengkap": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "hari": datetime.now().strftime("%A"),
            "tanggal_only": datetime.now().strftime("%Y-%m-%d"),
            "jam": datetime.now().strftime("%H:%M:%S"),
            "tahun": datetime.now().year,
            "bulan": datetime.now().month,
            "timestamp": time.time(),
            "durasi": durasi,
            "waktu_mulai": waktu_mulai,
            "waktu_selesai": waktu_selesai
        }
        
        scoreboard.append(new_entry)
        
        # Simpan ke file
        if save_scoreboard(scoreboard):
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Error adding score: {str(e)}")
        return False

# Fungsi untuk mendapatkan papan skor yang sudah difilter
def get_filtered_scoreboard(level_filter="Semua Level", time_filter="Semua Waktu"):
    """Mendapatkan papan skor dengan filter level dan waktu"""
    scoreboard = load_scoreboard()
    
    # Filter berdasarkan level
    if level_filter != "Semua Level" and scoreboard:
        scoreboard = [s for s in scoreboard if s.get("level") == level_filter]
    
    # Filter berdasarkan waktu
    if time_filter != "Semua Waktu" and scoreboard:
        now = datetime.now()
        if time_filter == "Hari Ini":
            today_str = now.strftime("%Y-%m-%d")
            scoreboard = [s for s in scoreboard if s.get("tanggal_only") == today_str]
        elif time_filter == "7 Hari Terakhir":
            seven_days_ago = now.timestamp() - (7 * 24 * 3600)
            scoreboard = [s for s in scoreboard if s.get("timestamp", 0) >= seven_days_ago]
        elif time_filter == "30 Hari Terakhir":
            thirty_days_ago = now.timestamp() - (30 * 24 * 3600)
            scoreboard = [s for s in scoreboard if s.get("timestamp", 0) >= thirty_days_ago]
        elif time_filter == "Bulan Ini":
            scoreboard = [s for s in scoreboard if 
                         s.get("tahun") == now.year and 
                         s.get("bulan") == now.month]
    
    # Urutkan ulang setelah filter
    scoreboard.sort(key=lambda x: (-x.get("skor", 0), x.get("durasi", {}).get("detik", float('inf')), -x.get("timestamp", 0)))
    
    return scoreboard

# Fungsi untuk mendapatkan statistik papan skor
def get_scoreboard_stats(scoreboard):
    """Mendapatkan statistik dari papan skor"""
    if not scoreboard:
        return {
            "total_pemain": 0,
            "skor_tertinggi": 0,
            "rata_rata": 0,
            "level_populer": "-",
            "waktu_tercepat": None,
            "rata_rata_waktu": None
        }
    
    total_pemain = len(scoreboard)
    skor_tertinggi = max(s.get("skor", 0) for s in scoreboard)
    rata_rata = sum(s.get("skor", 0) for s in scoreboard) / total_pemain if total_pemain > 0 else 0
    
    # Hitung level paling populer
    level_counts = {}
    for s in scoreboard:
        level = s.get("level", "Unknown")
        level_counts[level] = level_counts.get(level, 0) + 1
    level_populer = max(level_counts.items(), key=lambda x: x[1])[0] if level_counts else "-"
    
    # Hitung waktu tercepat (hanya untuk yang sempurna)
    waktu_tercepat = None
    total_waktu = 0
    waktu_count = 0
    
    for s in scoreboard:
        if s.get("durasi") and s.get("durasi", {}).get("detik"):
            total_waktu += s["durasi"]["detik"]
            waktu_count += 1
            
            if s.get("skor") == s.get("total_soal"):  # Hanya untuk skor sempurna
                if not waktu_tercepat or s["durasi"]["detik"] < waktu_tercepat["detik"]:
                    waktu_tercepat = {
                        "nama": s.get("nama"),
                        "detik": s["durasi"]["detik"],
                        "format": s["durasi"]["format"]
                    }
    
    rata_rata_waktu = total_waktu / waktu_count if waktu_count > 0 else None
    
    return {
        "total_pemain": total_pemain,
        "skor_tertinggi": skor_tertinggi,
        "rata_rata": round(rata_rata, 1),
        "level_populer": level_populer,
        "waktu_tercepat": waktu_tercepat,
        "rata_rata_waktu": round(rata_rata_waktu, 1) if rata_rata_waktu else None
    }

# Fungsi untuk mendapatkan informasi waktu sekarang
def get_current_time_info():
    """Mengembalikan informasi waktu sekarang dalam berbagai format"""
    now = datetime.now()
    return {
        "tanggal_lengkap": now.strftime("%Y-%m-%d %H:%M:%S"),
        "tanggal": now.strftime("%Y-%m-%d"),
        "jam": now.strftime("%H:%M:%S"),
        "hari": now.strftime("%A"),
        "bulan": now.strftime("%B"),
        "tahun": now.year,
        "timestamp": time.time()
    }

# ==================== DATABASE INFORMASI WILAYAH ====================

def get_wilayah_info(nama_wilayah):
    """Mengembalikan informasi lengkap tentang suatu wilayah"""
    
    # Database informasi wilayah (dipersingkat untuk kejelasan)
    info_database = {
        "Kabupaten Banyuwangi": {
            "geografis": "Terletak di ujung timur Pulau Jawa, berbatasan dengan Selat Bali. Memiliki wilayah terluas di Jawa Timur dengan pantai indah dan pegunungan.",
            "demografi": "Penduduk: ±1,7 juta jiwa. Mayoritas suku Osing (penduduk asli Banyuwangi), Jawa, Madura, dan Bali.",
            "budaya": "Kesenian Gandrung Banyuwangi, Seblang, dan tari Jejer Jaran Dawuk. Tradisi Kebo-keboan dan ritual Petik Laut.",
            "keunikan": "Memiliki Kawah Ijen dengan api biru, Taman Nasional Alas Purwo, dan Pantai Plengkung (G-Land) yang terkenal di dunia.",
            "oleh_oleh": "Pisang agung, sale pisang, kopi khas Banyuwangi, keripik tempe, dan jenang Banyuwangi."
        },
        "Kabupaten Malang": {
            "geografis": "Wilayah pegunungan dengan udara sejuk, dikelilingi Gunung Semeru, Bromo, Arjuno, dan Kawi. Memiliki pantai selatan yang indah.",
            "demografi": "Penduduk: ±2,6 juta jiwa. Mayoritas suku Jawa dengan budaya Arek yang khas.",
            "budaya": "Tari Topeng Malangan, tradisi bersih desa, dan upacara adat Yadnya Karo di Suku Tengger.",
            "keunikan": "Kota Apel, wisata Jatim Park, Batu Secret Zoo, dan panorama Gunung Bromo dari sisi Malang.",
            "oleh_oleh": "Apel Malang, keripik buah, keripik tempe, bakso Malang, dan sari apel."
        },
        "Kota Malang": {
            "geografis": "Kota di dataran tinggi dengan suhu rata-rata 24°C, dikelilingi pegunungan dan terkenal dengan julukan Kota Pendidikan.",
            "demografi": "Penduduk: ±900 ribu jiwa. Masyarakat multietnis dengan banyak pendatang untuk pendidikan.",
            "budaya": "Budaya Arek yang dinamis, banyak seni musik modern dan tradisional, serta kafe dan tempat nongkrong artistik.",
            "keunikan": "Arsitektur kolonial Belanda yang masih terjaga, dijuluki Kota Bunga, dan memiliki banyak universitas ternama.",
            "oleh_oleh": "Keripik buah, keripik tempe, bakso Malang, wingko babat, dan kripik singkong."
        },
        "Kota Surabaya": {
            "geografis": "Kota pesisir utara, ibu kota Provinsi Jawa Timur, memiliki pelabuhan Tanjung Perak dan kawasan industri.",
            "demografi": "Penduduk: ±3 juta jiwa. Masyarakat multietnis dengan budaya urban yang dinamis.",
            "budaya": "Budaya Arek Surabaya, tari Remo, ludruk, dan tradisi 'arek Suroboyo' yang blak-blakan.",
            "keunikan": "Kota Pahlawan, Tugu Pahlawan, Jembatan Suramadu, House of Sampoerna, dan kuliner malam.",
            "oleh_oleh": "Kerupuk udang, terasi, sambal bu Rudy, wingko babat, dan spikok Surabaya."
        },
        "Kota Batu": {
            "geografis": "Kota wisata pegunungan dengan udara sejuk, dikelilingi Gunung Panderman, Arjuno, dan Anjasmoro.",
            "demografi": "Penduduk: ±200 ribu jiwa. Masyarakat dengan budaya agraris dan pariwisata.",
            "budaya": "Budaya Jawa Timuran dengan sentuhan modern karena pariwisata.",
            "keunikan": "Kota wisata, Jatim Park, Batu Night Spectacular, Selecta, petik apel, dan agro wisata.",
            "oleh_oleh": "Apel Batu, keripik apel, sari apel, sayuran organik, dan susu murni."
        }
    }
    
    # Kembalikan info jika ada, jika tidak ada kembalikan info default
    if nama_wilayah in info_database:
        return info_database[nama_wilayah]
    else:
        tipe = "Kota" if nama_wilayah.startswith("Kota ") else "Kabupaten"
        return {
            "geografis": f"{tipe} di Provinsi Jawa Timur dengan berbagai potensi sumber daya alam dan keindahan alam.",
            "demografi": f"Penduduk dengan keragaman budaya dan tradisi khas {tipe} di Jawa Timur.",
            "budaya": f"Memiliki kesenian tradisional dan adat istiadat yang masih dilestarikan masyarakat setempat.",
            "keunikan": f"Memiliki berbagai destinasi wisata dan potensi ekonomi yang menjadi ciri khas wilayah.",
            "oleh_oleh": f"Berbagai produk makanan khas dan kerajinan tangan dari {nama_wilayah}."
        }

# ==================== INISIALISASI SESSION STATE ====================

# Inisialisasi session state dengan variabel waktu
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
    st.session_state.show_save_form = False
    
    # Variabel waktu baru
    st.session_state.game_start_time = None
    st.session_state.game_end_time = None
    st.session_state.question_start_time = None
    st.session_state.total_game_duration = 0
    st.session_state.question_times = []
    st.session_state.average_answer_time = 0
    st.session_state.session_start_time = time.time()
    st.session_state.last_activity_time = time.time()

# ==================== FUNGSI MANAJEMEN WAKTU ====================

def start_game_timer():
    """Memulai timer untuk game"""
    st.session_state.game_start_time = time.time()
    st.session_state.game_end_time = None
    st.session_state.total_game_duration = 0
    st.session_state.question_times = []
    st.session_state.average_answer_time = 0

def start_question_timer():
    """Memulai timer untuk pertanyaan"""
    st.session_state.question_start_time = time.time()

def end_question_timer():
    """Mengakhiri timer untuk pertanyaan dan mencatat waktu"""
    if st.session_state.question_start_time:
        duration = time.time() - st.session_state.question_start_time
        st.session_state.question_times.append({
            "question_number": st.session_state.total_questions,
            "duration": duration,
            "correct": st.session_state.feedback.startswith("✅")
        })
        # Update rata-rata waktu menjawab
        total_time = sum(q["duration"] for q in st.session_state.question_times)
        st.session_state.average_answer_time = total_time / len(st.session_state.question_times)
        return duration
    return 0

def end_game_timer():
    """Mengakhiri timer game dan mencatat total waktu"""
    if st.session_state.game_start_time:
        st.session_state.game_end_time = time.time()
        st.session_state.total_game_duration = st.session_state.game_end_time - st.session_state.game_start_time
        return st.session_state.total_game_duration
    return 0

def format_duration(seconds):
    """Memformat durasi dalam detik ke format yang mudah dibaca"""
    if seconds is None:
        return "00:00"
    minutes = int(seconds // 60)
    seconds_remaining = int(seconds % 60)
    return f"{minutes:02d}:{seconds_remaining:02d}"

def get_session_duration():
    """Mendapatkan durasi sesi saat ini"""
    if st.session_state.session_start_time:
        return time.time() - st.session_state.session_start_time
    return 0

def update_last_activity():
    """Memperbarui waktu aktivitas terakhir"""
    st.session_state.last_activity_time = time.time()

# ==================== APLIKASI UTAMA ====================

# Terapkan background sidebar
st.markdown(get_background_image_html(SIDEBAR_BACKGROUND_URL), unsafe_allow_html=True)

# Terapkan background footer dengan brightness dari session state
st.markdown(get_footer_background_html(FOOTER_BACKGROUND_URL, st.session_state.footer_brightness), unsafe_allow_html=True)

# ==================== INPUT NAMA ====================

if not st.session_state.name_submitted:
    with st.empty():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("https://img.freepik.com/vektor-premium/peta-yang-digambar-tangan-dari-provinsi-jawa-timur-indonesia-desain-kartun-garis-sederhana-modern_242622-498.jpg", width=150)
            
            # Tampilkan waktu sekarang
            time_info = get_current_time_info()
            st.markdown(f"""
            <div style="text-align: center; margin: 10px 0; color: #666; font-size: 14px;">
                {time_info['hari']}, {time_info['tanggal']} | {time_info['jam']}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="text-align: center; margin: 20px 0;">
                <h1>🧩 Tebak Jawa Timur</h1>
                <p style="font-size: 18px; color: #666;">Selamat datang di game interaktif pembelajaran wilayah Jawa Timur!</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("name_form"):
                st.markdown("### 👤 Masukkan Nama Anda")
                name = st.text_input("Nama", placeholder="Contoh: Andi", max_chars=30)
                
                col_submit1, col_submit2, col_submit3 = st.columns([1, 2, 1])
                with col_submit2:
                    submitted = st.form_submit_button("🚀 Mulai Bermain", use_container_width=True, type="primary")
                
                if submitted:
                    if name.strip():
                        st.session_state.user_name = name.strip()
                        st.session_state.name_submitted = True
                        st.rerun()
                    else:
                        st.error("❌ Nama tidak boleh kosong!")
            
            st.markdown("---")
            st.markdown("""
            <div style="text-align: center; color: #666; font-size: 14px;">
                <p>✨ Fitur yang tersedia:</p>
                <p>🎮 Game Tebak Wilayah | 📚 Mode Belajar | 🌋 Bromo 3D | 🏆 Papan Skor</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.stop()

# Update waktu aktivitas terakhir
update_last_activity()

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
    
    # Sesuaikan jumlah opsi berdasarkan kesulitan
    if st.session_state.difficulty == "Mudah":
        num_options = 2
    elif st.session_state.difficulty == "Sulit":
        num_options = 6
    else:  # Normal
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
    
    # Mulai timer untuk pertanyaan baru
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
    st.session_state.show_save_form = False
    
    # Reset timer
    st.session_state.game_start_time = None
    st.session_state.game_end_time = None
    st.session_state.total_game_duration = 0
    st.session_state.question_times = []
    st.session_state.average_answer_time = 0
    
    pilih_wilayah()

# ==================== SIDEBAR NAVIGASI ====================

with st.sidebar:
    st.image("https://img.freepik.com/vektor-premium/peta-yang-digambar-tangan-dari-provinsi-jawa-timur-indonesia-desain-kartun-garis-sederhana-modern_242622-498.jpg", 
             width=100)
    st.title("🧩 Tebak Jatim")
    
    # Tampilkan waktu di sidebar
    time_info = get_current_time_info()
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 8px; border-radius: 10px; margin-bottom: 10px; text-align: center;">
        <p style="color: white; margin: 0; font-size: 12px;">{time_info['hari']}, {time_info['tanggal']}</p>
        <p style="color: white; margin: 0; font-size: 14px; font-weight: bold;">⏰ {time_info['jam']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 10px; border-radius: 10px; margin-bottom: 10px; text-align: center;">
        <p style="color: white; margin: 0;">👋 Halo, <strong>{st.session_state.user_name}</strong>!</p>
    </div>
    """, unsafe_allow_html=True)
    
    menu_options = ["🎮 Game", "📚 Belajar", "🌋 Bromo 3D", "🏆 Papan Skor", "⏱️ Statistik Waktu", "⚙️ Pengaturan", "ℹ️ Tentang"]
    selected_menu = st.radio(
        "Menu Navigasi",
        menu_options,
        index=0,
        label_visibility="collapsed",
        key="main_navigation"
    )
    
    st.session_state.current_page = selected_menu.split(" ")[1] if " " in selected_menu else selected_menu
    
    st.markdown("---")
    
    if st.button("🔄 Ganti Nama", use_container_width=True):
        st.session_state.name_submitted = False
        st.rerun()
    
    st.markdown("---")
    
    if "Game" in selected_menu:
        st.header("🎮 Kontrol Game")
        
        if not st.session_state.game_started or st.session_state.game_over:
            if st.button("🎲 Mulai Game Baru", use_container_width=True, type="primary"):
                reset_game()
                st.rerun()
        else:
            if st.button("🔄 Reset Game", use_container_width=True):
                reset_game()
                st.rerun()
        
        st.markdown("### 📊 Statistik")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Skor", st.session_state.score)
        with col2:
            st.metric("Soal", f"{st.session_state.total_questions}/{st.session_state.max_questions}")
        
        # Tampilkan waktu jika game sedang berjalan
        if st.session_state.game_started and not st.session_state.game_over:
            if st.session_state.game_start_time:
                current_duration = time.time() - st.session_state.game_start_time
                st.metric("⏱️ Waktu Bermain", format_duration(current_duration))
            
            if st.session_state.average_answer_time > 0:
                st.metric("⚡ Rata-rata Jawab", f"{st.session_state.average_answer_time:.1f} detik")
        
        with st.expander("⚙️ Pengaturan Cepat"):
            difficulty = st.selectbox(
                "Tingkat Kesulitan",
                ["Mudah", "Normal", "Sulit"],
                index=["Mudah", "Normal", "Sulit"].index(st.session_state.difficulty),
                key="game_difficulty"
            )
            if difficulty != st.session_state.difficulty:
                st.session_state.difficulty = difficulty
                st.rerun()
    
    elif "Belajar" in selected_menu:
        st.header("📚 Mode Belajar")
        st.markdown("""
        Pelajari bentuk dan lokasi setiap wilayah di Jawa Timur.
        
        **Fitur:**
        - Lihat semua wilayah dengan warna berbeda
        - **Klik wilayah** untuk melihat informasi lengkap
        """)
        
        st.markdown("### 📋 Statistik Wilayah")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Wilayah", len(wilayah_list))
        with col2:
            st.metric("Kabupaten", len(kab_list))
        with col3:
            st.metric("Kota", len(kota_list))
    
    elif "Bromo" in selected_menu:
        st.header("🌋 Gunung Bromo 3D")
        st.markdown("Visualisasi interaktif Gunung Bromo, ikon wisata Jawa Timur.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Ketinggian", "2.329 m")
        with col2:
            st.metric("Status", "Aktif")
    
    elif "Papan Skor" in selected_menu:
        st.header("🏆 Papan Skor")
        
        level_filter = st.selectbox(
            "Filter berdasarkan level:",
            ["Semua Level", "Mudah", "Normal", "Sulit"],
            key="scoreboard_level_filter"
        )
        
        time_filter = st.selectbox(
            "Filter berdasarkan waktu:",
            ["Semua Waktu", "Hari Ini", "7 Hari Terakhir", "30 Hari Terakhir", "Bulan Ini"],
            key="scoreboard_time_filter"
        )
        
        scoreboard = get_filtered_scoreboard(level_filter, time_filter)
        stats = get_scoreboard_stats(scoreboard)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Pemain", stats["total_pemain"])
        with col2:
            if scoreboard:
                st.metric("Skor Tertinggi", f"{stats['skor_tertinggi']}/{scoreboard[0]['total_soal']}")
    
    elif "Statistik Waktu" in selected_menu:
        st.header("⏱️ Statistik Waktu")
        
        session_duration = get_session_duration()
        st.metric("Durasi Sesi", format_duration(session_duration))
        
        if st.session_state.question_times:
            st.metric("Total Pertanyaan", len(st.session_state.question_times))
            st.metric("Rata-rata Waktu Jawab", f"{st.session_state.average_answer_time:.1f} detik")
            
            # Waktu tercepat
            fastest = min(st.session_state.question_times, key=lambda x: x["duration"])
            st.metric("⚡ Jawaban Tercepat", f"{fastest['duration']:.1f} detik (Soal {fastest['question_number']})")
    
    elif "Pengaturan" in selected_menu:
        st.header("⚙️ Pengaturan")
        st.session_state.max_questions = st.slider(
            "Jumlah Maksimum Soal",
            min_value=5,
            max_value=20,
            value=st.session_state.max_questions,
            step=5
        )
        
        # Tambahkan slider untuk mengatur brightness footer
        st.markdown("---")
        st.markdown("### 🎨 Pengaturan Tampilan Footer")
        new_brightness = st.slider(
            "Brightness Footer",
            min_value=0.3,
            max_value=1.0,
            value=st.session_state.footer_brightness,
            step=0.05,
            help="Atur kecerahan background footer (0.3 = gelap, 1.0 = terang)"
        )
        
        if new_brightness != st.session_state.footer_brightness:
            st.session_state.footer_brightness = new_brightness
            st.rerun()
    
    elif "Tentang" in selected_menu:
        st.header("ℹ️ Tentang Aplikasi")
        st.markdown("""
        **Tebak Jawa Timur** v2.3.0  
        Aplikasi interaktif untuk mempelajari bentuk kota dan kabupaten di Jawa Timur.
        
        **Fitur:**
        - 🧩 Tebak bentuk wilayah
        - 📚 Mode belajar interaktif
        - 🌋 Visualisasi 3D Gunung Bromo
        - 🏆 Papan skor dengan penyimpanan lokal
        - ⏱️ Statistik waktu bermain
        - 🎨 Kontrol brightness footer
        """)

# ==================== KONTEN UTAMA ====================

if "Game" in selected_menu:
    st.title("🧩 Tebak Bentuk Kota & Kabupaten di Jawa Timur")
    if st.session_state.game_started and not st.session_state.game_over:
        st.markdown(f"**Tingkat Kesulitan:** {st.session_state.difficulty} | **Soal:** {st.session_state.total_questions + 1}/{st.session_state.max_questions}")
        
        # Tampilkan timer jika game sedang berjalan
        if st.session_state.game_start_time:
            current_duration = time.time() - st.session_state.game_start_time
            col_timer1, col_timer2, col_timer3 = st.columns(3)
            with col_timer1:
                st.info(f"⏱️ **Waktu Total:** {format_duration(current_duration)}")
            with col_timer2:
                if st.session_state.question_start_time:
                    question_duration = time.time() - st.session_state.question_start_time
                    st.info(f"⚡ **Waktu Soal Ini:** {question_duration:.1f} detik")
            with col_timer3:
                if st.session_state.average_answer_time > 0:
                    st.info(f"📊 **Rata-rata:** {st.session_state.average_answer_time:.1f} detik")

elif "Belajar" in selected_menu:
    st.title("📚 Mode Belajar Wilayah Jawa Timur")
    st.markdown("**Klik wilayah pada peta** untuk melihat informasi lengkap!")

elif "Bromo" in selected_menu:
    st.title("🌋 Gunung Bromo - Visualisasi 3D Interaktif")
    
    col_bromo_left, col_bromo_right = st.columns([2, 1])
    
    with col_bromo_left:
        st.markdown("### Model 3D Gunung Bromo")
        st.components.v1.html("""
        <div style="width:100%; height:600px; position:relative; border-radius: 10px; overflow: hidden;">
            <iframe 
                title="Mount Bromo" 
                frameborder="0" 
                allowfullscreen 
                src="https://sketchfab.com/models/72f1c983ba4040eab89d75eb2b0d3e32/embed" 
                style="width:100%; height:100%; position:absolute; top:0; left:0;">
            </iframe>
        </div>
        """, height=620)
    
    with col_bromo_right:
        st.markdown("### 📍 Informasi Detail")
        st.markdown("""
        **Nama:** Gunung Bromo  
        **Tinggi:** 2.329 meter  
        **Koordinat:** 7°56′30″S 112°57′00″E  
        **Jenis:** Stratovolcano  
        **Status:** Aktif  
        
        **Karakteristik:**
        - Berdiri di tengah kaldera raksasa
        - Kawah berdiameter ±800 × 600 meter
        - Dikelilingi "Lautan Pasir" seluas 5.250 hektar
        """)

# Statistik singkat
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Ketinggian", "2.329 m")
        with col2:
            st.metric("Status", "Aktif")
        
        # Info tambahan dalam expander
        with st.expander("📖 Sejarah & Keunikan"):
            st.markdown("""
            **Sejarah:**
            Gunung Bromo terbentuk dari letusan gunung berapi purba yang menciptakan kaldera besar. Nama "Bromo" berasal dari kata "Brahma" (dewa dalam agama Hindu).
            
            **Keunikan:**
            - Memiliki kawah berdiameter ±800 meter
            - Dikelilingi lautan pasir seluas 5.250 hektar
            - Tempat upacara Kasada masyarakat Tengger
            - Pemandangan matahari terbit yang spektakuler
            
            **Ekosistem:**
            Kawasan ini memiliki keanekaragaman hayati yang unik dengan berbagai flora dan fauna yang beradaptasi dengan kondisi vulkanik.
            """)
        
        # Tips kunjungan
        with st.expander("🎫 Tips Kunjungan"):
            st.markdown("""
            **Waktu terbaik:** Mei - Oktober (musim kemarau)
            **Akses:** Dari Surabaya ±3-4 jam perjalanan darat
            **Tiket masuk:** Rp 29.000 - Rp 34.000 (weekday/weekend)
            **Wajib coba:** Jeep wisata, hiking ke kawah, melihat matahari terbit
            """)

elif "Papan Skor" in selected_menu:
    st.title("🏆 Papan Skor Pemain")
    st.markdown("Simpan skor kamu dan lihat peringkat dengan pemain lain!")
    
    level_filter = st.session_state.get("scoreboard_level_filter", "Semua Level")
    time_filter = st.session_state.get("scoreboard_time_filter", "Semua Waktu")
    
    col_filter_info, col_stats = st.columns([2, 1])
    with col_filter_info:
        st.info(f"📊 Menampilkan: **{level_filter}** | **{time_filter}**")
    with col_stats:
        scoreboard = get_filtered_scoreboard(level_filter, time_filter)
        stats = get_scoreboard_stats(scoreboard)
        st.metric("Total Pemain", stats["total_pemain"])
    
    # Tampilkan papan skor
    if scoreboard:
        df_data = []
        for i, player in enumerate(scoreboard[:10], 1):
            if i == 1:
                avatar = "👑"
            elif i == 2:
                avatar = "🥈"
            elif i == 3:
                avatar = "🥉"
            else:
                avatar = f"{i}."
            
            nama_display = player.get("nama", "Unknown")
            if player.get("nama") == st.session_state.user_name:
                nama_display = f"⭐ {player.get('nama')} (Kamu)"
            
            # Format durasi jika ada
            durasi_display = player.get("durasi", {}).get("format", "-") if player.get("durasi") else "-"
            
            df_data.append({
                "Peringkat": avatar,
                "Nama": nama_display,
                "Skor": f"{player.get('skor', 0)}/{player.get('total_soal', 0)}",
                "Persentase": f"{player.get('persentase', 0)}%",
                "Level": player.get('level', 'Unknown'),
                "Durasi": durasi_display,
                "Tanggal": player.get('tanggal', '')[:10] if player.get('tanggal') else ''
            })
        
        df = pd.DataFrame(df_data)
        
        st.dataframe(
            df,
            column_config={
                "Peringkat": st.column_config.TextColumn("Peringkat", width="small"),
                "Nama": st.column_config.TextColumn("Nama Pemain", width="medium"),
                "Skor": st.column_config.TextColumn("Skor", width="small"),
                "Persentase": st.column_config.TextColumn("%", width="small"),
                "Level": st.column_config.TextColumn("Level", width="small"),
                "Durasi": st.column_config.TextColumn("Durasi", width="medium"),
                "Tanggal": st.column_config.TextColumn("Tanggal", width="small"),
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Statistik tambahan
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        with col_stat1:
            st.metric("🏆 Juara 1", scoreboard[0].get("nama", "-") if scoreboard else "-")
        with col_stat2:
            st.metric("⭐ Skor Tertinggi", f"{stats['skor_tertinggi']}/{scoreboard[0].get('total_soal', 0)}" if scoreboard else "-")
        with col_stat3:
            st.metric("📊 Rata-rata Skor", f"{stats['rata_rata']}")
        with col_stat4:
            st.metric("🎯 Level Populer", stats["level_populer"])
        
        # Tampilkan informasi waktu tercepat jika ada
        if stats["waktu_tercepat"]:
            st.success(f"⚡ Waktu Tercepat (Skor Sempurna): {stats['waktu_tercepat']['format']} oleh {stats['waktu_tercepat']['nama']}")
    
    else:
        st.markdown("""
        <div style="text-align: center; padding: 50px; background-color: #f8f9fa; border-radius: 10px;">
            <h3 style="color: #666;">Belum ada skor tersimpan</h3>
            <p>Mainkan game dan simpan skor kamu untuk muncul di papan skor!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tampilkan skor pemain saat ini dengan informasi waktu
    st.markdown("---")
    st.markdown(f"### 📝 Skor Kamu: **{st.session_state.user_name}**")
    st.markdown(f"**Skor:** {st.session_state.score}/{st.session_state.max_questions} (Level: {st.session_state.difficulty})")
    
    if st.session_state.total_game_duration > 0:
        st.markdown(f"**Waktu Bermain:** {format_duration(st.session_state.total_game_duration)}")
    
    if st.session_state.average_answer_time > 0:
        st.markdown(f"**Rata-rata Waktu Jawab:** {st.session_state.average_answer_time:.1f} detik")
    
    # Tombol untuk menyimpan skor dari halaman papan skor
    if st.session_state.score > 0 and not st.session_state.score_saved:
        if st.button("💾 Simpan Skor Saya ke Papan Skor", use_container_width=True, type="primary"):
            # Akhiri timer game jika belum
            if st.session_state.game_start_time and not st.session_state.game_end_time:
                end_game_timer()
            
            if add_score(
                st.session_state.user_name, 
                st.session_state.score, 
                st.session_state.difficulty, 
                st.session_state.max_questions,
                st.session_state.game_start_time,
                st.session_state.game_end_time
            ):
                st.session_state.score_saved = True
                st.success(f"✅ Skor berhasil disimpan! {st.session_state.user_name} masuk papan skor.")
                st.rerun()
            else:
                st.error("❌ Gagal menyimpan skor. Silakan coba lagi.")
    elif st.session_state.score_saved:
        st.success("✅ Skor sudah disimpan ke papan skor!")
    
    with st.expander("🛠️ Pengaturan Admin"):
        st.warning("⚠️ Fitur ini akan menghapus semua data papan skor!")
        if st.button("🗑️ Reset Semua Skor", use_container_width=True):
            if os.path.exists(SCOREBOARD_FILE):
                os.remove(SCOREBOARD_FILE)
                st.success("✅ Papan skor berhasil direset!")
                st.rerun()
            else:
                st.info("Belum ada data papan skor.")

elif "Statistik Waktu" in selected_menu:
    st.title("⏱️ Statistik Waktu")
    
    col_time1, col_time2, col_time3 = st.columns(3)
    
    with col_time1:
        session_duration = get_session_duration()
        st.metric("Durasi Sesi", format_duration(session_duration))
    
    with col_time2:
        if st.session_state.game_start_time:
            if st.session_state.game_end_time:
                game_duration = st.session_state.total_game_duration
            else:
                game_duration = time.time() - st.session_state.game_start_time
            st.metric("Durasi Game Terakhir", format_duration(game_duration))
        else:
            st.metric("Durasi Game Terakhir", "-")
    
    with col_time3:
        st.metric("Total Pertanyaan", st.session_state.total_questions)
    
    # Statistik waktu menjawab
    if st.session_state.question_times:
        st.markdown("### 📊 Statistik Waktu Menjawab")
        
        # Dataframe statistik
        df_times = pd.DataFrame(st.session_state.question_times)
        df_times['duration_display'] = df_times['duration'].apply(lambda x: f"{x:.1f} detik")
        df_times['status'] = df_times['correct'].apply(lambda x: "✅ Benar" if x else "❌ Salah")
        
        st.dataframe(
            df_times[['question_number', 'duration_display', 'status']],
            column_config={
                "question_number": "Soal Ke-",
                "duration_display": "Waktu",
                "status": "Hasil"
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Grafik waktu menjawab
        st.markdown("### 📈 Grafik Waktu Menjawab")
        chart_data = pd.DataFrame({
            'Soal': df_times['question_number'],
            'Waktu (detik)': df_times['duration']
        })
        st.line_chart(chart_data.set_index('Soal'))
    
    else:
        st.info("Belum ada data waktu. Mulai game untuk melihat statistik waktu.")

elif "Pengaturan" in selected_menu:
    st.title("⚙️ Pengaturan Aplikasi")
    st.markdown("Sesuaikan pengalaman bermain Anda")
    
    tab_set1, tab_set2, tab_set3, tab_set4 = st.tabs(["🎮 Game", "🎨 Tampilan", "⏱️ Waktu", "🔊 Audio"])
    
    with tab_set1:
        st.markdown("### Pengaturan Permainan")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Maksimum Soal", min_value=5, max_value=30, value=st.session_state.max_questions, key="setting_max_questions")
        with col2:
            st.selectbox("Tingkat Kesulitan", ["Mudah", "Normal", "Sulit"], 
                        index=["Mudah", "Normal", "Sulit"].index(st.session_state.difficulty), 
                        key="setting_difficulty")
        
        if st.button("💾 Simpan Pengaturan Game", use_container_width=True):
            st.session_state.max_questions = st.session_state.setting_max_questions
            st.session_state.difficulty = st.session_state.setting_difficulty
            st.success("✅ Pengaturan game berhasil disimpan!")
    
    with tab_set2:
        st.markdown("### Pengaturan Visual")
        st.selectbox("Tema", ["Terang", "Gelap", "Kontras Tinggi"], key="setting_theme")
        st.selectbox("Ukuran Font", ["Kecil", "Sedang", "Besar"], key="setting_font")
        
        # Pengaturan brightness footer di tab tampilan
        st.markdown("---")
        st.markdown("#### 🎨 Pengaturan Footer")
        footer_brightness = st.slider(
            "Brightness Background Footer",
            min_value=0.3,
            max_value=1.0,
            value=st.session_state.footer_brightness,
            step=0.05,
            help="Atur kecerahan gambar background footer"
        )
        
        if footer_brightness != st.session_state.footer_brightness:
            st.session_state.footer_brightness = footer_brightness
            st.rerun()
        
        st.success("✅ Pengaturan visual akan diterapkan pada sesi berikutnya")
    
    with tab_set3:
        st.markdown("### Pengaturan Waktu")
        st.checkbox("Tampilkan timer di game", value=True, key="setting_show_timer")
        st.checkbox("Catat waktu menjawab", value=True, key="setting_record_time")
        st.success("✅ Pengaturan waktu akan diterapkan pada sesi berikutnya")
    
    with tab_set4:
        st.markdown("### Pengaturan Audio")
        st.checkbox("Efek Suara", value=True, key="setting_sound")
        st.slider("Volume", 0, 100, 70, key="setting_volume")
        st.success("✅ Pengaturan audio akan diterapkan pada sesi berikutnya")

elif "Tentang" in selected_menu:
    st.title("ℹ️ Tentang Aplikasi")
    
    col_about1, col_about2 = st.columns([2, 1])
    
    with col_about1:
        st.markdown("""
        ### Tebak Jawa Timur
        
        Aplikasi interaktif untuk mempelajari bentuk kota dan kabupaten di Jawa Timur 
        dengan cara yang menyenangkan dan edukatif.
        
        **Fitur Unggulan:**
        - **Tebak Game:** Tebak wilayah dari bentuknya
        - **Mode Belajar:** Eksplorasi semua wilayah dengan info lengkap
        - **Bromo 3D:** Visualisasi interaktif Gunung Bromo
        - **Info Wilayah:** Data geografis, demografi, budaya, dan oleh-oleh
        - **Papan Skor:** Kompetisi dengan pemain lain (penyimpanan lokal)
        - **Statistik Waktu:** Pantau waktu bermain dan kecepatan menjawab
        - **Kontrol Brightness:** Atur kecerahan background footer sesuai preferensi
        
        **Teknologi:**
        - Streamlit untuk antarmuka
        - Folium untuk peta interaktif
        - Sketchfab untuk model 3D
        - GeoJSON untuk data wilayah
        - JSON untuk penyimpanan papan skor
        """)
    
    with col_about2:
        st.image("https://img.freepik.com/vektor-premium/peta-yang-digambar-tangan-dari-provinsi-jawa-timur-indonesia-desain-kartun-garis-sederhana-modern_242622-498.jpg")
        st.markdown("**Versi:** 2.3.0")
        st.markdown("**Rilis:** Maret 2024")
        st.markdown("**Developer:** Tim Edukasi Geografi")

# Layout untuk halaman Game dan Belajar
if "Game" in selected_menu or "Belajar" in selected_menu:
    if "Belajar" in selected_menu:
        col_map, col_info = st.columns([2, 1])
    else:
        col_map = st.container()
        col_info = None
    
    with col_map if "Belajar" in selected_menu else st.container():
        m = folium.Map(
            location=[-7.5, 112.3], 
            zoom_start=8,
            tiles=None,
            control_scale=True,
            prefer_canvas=True
        )
        
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Satellite',
            overlay=False,
            control=False
        ).add_to(m)
        
        def style_function(feature):
            name = feature["properties"]["name"]
            
            if "Belajar" in selected_menu:
                return {
                    "fillColor": "#33cc33",
                    "color": "#ffffff",
                    "weight": 1.5,
                    "fillOpacity": 0.5,
                    "interactive": True
                }
            
            if st.session_state.game_started and not st.session_state.game_over and name == st.session_state.current_region:
                return {
                    "fillColor": "#ff0000",
                    "color": "#ff0000",
                    "weight": 3,
                    "fillOpacity": 0.7,
                    "interactive": True
                }
            else:
                return {
                    "fillColor": "#3388ff" if st.session_state.game_started else "#cccccc",
                    "color": "#ffffff",
                    "weight": 1.5,
                    "fillOpacity": 0.3 if st.session_state.game_started else 0.1,
                    "interactive": True
                }
        
        if "Belajar" in selected_menu:
            geojson_layer = folium.GeoJson(
                jatim_geojson,
                name="Wilayah Jatim",
                style_function=style_function,
                tooltip=folium.GeoJsonTooltip(
                    fields=["name"], 
                    aliases=["Klik untuk info detail:"],
                    style=("background-color: white; color: #333333; font-weight: bold; padding: 5px;")
                ),
                highlight_function=lambda x: {"fillColor": "#ffaa00", "color": "#ffaa00", "weight": 3, "fillOpacity": 0.7}
            ).add_to(m)
            
            geojson_layer.add_child(
                folium.GeoJsonPopup(
                    fields=["name"],
                    aliases=["Wilayah:"],
                    labels=True,
                    style="background-color: white; color: #333333;"
                )
            )
        else:
            folium.GeoJson(
                jatim_geojson,
                name="Wilayah Jatim",
                style_function=style_function,
            ).add_to(m)
        
        map_data = st_folium(
            m, 
            width=None, 
            height=500, 
            use_container_width=True,
            key="belajar_map" if "Belajar" in selected_menu else "game_map"
        )
        
        if "Belajar" in selected_menu and map_data and map_data.get("last_active_drawing"):
            last_click = map_data["last_active_drawing"]
            if last_click and "properties" in last_click and "name" in last_click["properties"]:
                st.session_state.selected_wilayah_info = last_click["properties"]["name"]
                st.rerun()
        
        if "Game" in selected_menu and not st.session_state.game_started and not st.session_state.game_over:
            if st.button("🎮 Mulai Game 10 Pertanyaan", use_container_width=True, type="primary"):
                start_game_timer()  # Mulai timer game
                pilih_wilayah()
                st.rerun()
    
    if "Belajar" in selected_menu and col_info is not None:
        with col_info:
            st.markdown("## 📋 Info Wilayah")
            
            if st.session_state.selected_wilayah_info:
                wilayah = st.session_state.selected_wilayah_info
                info = get_wilayah_info(wilayah)
                
                st.markdown(f"""
                <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                    <h3 style="color: #0066cc; margin-top: 0;">📍 {wilayah}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                info_tab1, info_tab2, info_tab3, info_tab4, info_tab5 = st.tabs(["🗺️ Geografis", "👥 Demografi", "🎭 Budaya", "✨ Keunikan", "🛍️ Oleh-oleh"])
                
                with info_tab1:
                    st.markdown(info["geografis"])
                with info_tab2:
                    st.markdown(info["demografi"])
                with info_tab3:
                    st.markdown(info["budaya"])
                with info_tab4:
                    st.markdown(info["keunikan"])
                with info_tab5:
                    st.markdown(info["oleh_oleh"])
                
                if st.button("🔄 Klik wilayah lain", use_container_width=True):
                    st.session_state.selected_wilayah_info = None
                    st.rerun()
            else:
                st.markdown("""
                <div style="background-color: #e8f4fd; padding: 20px; border-radius: 10px; text-align: center; border: 2px dashed #0066cc;">
                    <h4 style="color: #0066cc;">👆 Klik Wilayah di Peta</h4>
                    <p style="color: #666;">Klik pada salah satu wilayah di peta untuk melihat informasi lengkap!</p>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("📌 Atau pilih dari daftar"):
                    popular_regions = ["Kabupaten Banyuwangi", "Kabupaten Malang", "Kota Surabaya", "Kota Batu"]
                    for region in popular_regions:
                        if st.button(f"{region}", key=f"quick_{region}"):
                            st.session_state.selected_wilayah_info = region
                            st.rerun()
    
    if "Game" in selected_menu:
        with st.container():
            st.markdown("---")
            
            if st.session_state.game_over:
                # Akhiri timer game
                end_game_timer()
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown("## 🎮 Game Selesai!")
                    st.markdown(f"### Skor Akhir: **{st.session_state.score}/{st.session_state.max_questions}**")
                    
                    # Tampilkan informasi waktu
                    if st.session_state.total_game_duration > 0:
                        st.info(f"⏱️ **Total Waktu:** {format_duration(st.session_state.total_game_duration)}")
                    
                    if st.session_state.average_answer_time > 0:
                        st.info(f"⚡ **Rata-rata Waktu Jawab:** {st.session_state.average_answer_time:.1f} detik")
                    
                    if st.session_state.score == st.session_state.max_questions:
                        st.balloons()
                        st.markdown("### 🏆 Selamat! Nilai Sempurna!")
                        
                        # Tampilkan statistik khusus untuk nilai sempurna
                        if st.session_state.question_times:
                            fastest = min(st.session_state.question_times, key=lambda x: x["duration"])
                            st.success(f"⚡ **Jawaban Tercepat:** Soal {fastest['question_number']} dalam {fastest['duration']:.1f} detik!")
                    
                    elif st.session_state.score >= 7:
                        st.markdown("### 👍 Bagus! Terus belajar!")
                    elif st.session_state.score >= 5:
                        st.markdown("### 📚 Lumayan, coba lagi!")
                    else:
                        st.markdown("### 💪 Ayo coba lagi! Pasti bisa lebih baik!")
                    
                    # Form untuk menyimpan skor
                    if not st.session_state.score_saved and st.session_state.score > 0:
                        st.markdown("---")
                        st.markdown("### 📝 Simpan Skor ke Papan Skor")
                        
                        with st.form("save_score_form"):
                            st.markdown(f"Nama: **{st.session_state.user_name}**")
                            st.markdown(f"Skor: **{st.session_state.score}/{st.session_state.max_questions}** (Level: {st.session_state.difficulty})")
                            
                            if st.session_state.total_game_duration > 0:
                                st.markdown(f"Waktu: **{format_duration(st.session_state.total_game_duration)}**")
                            
                            if st.form_submit_button("💾 Simpan Skor", use_container_width=True, type="primary"):
                                if add_score(
                                    st.session_state.user_name, 
                                    st.session_state.score, 
                                    st.session_state.difficulty, 
                                    st.session_state.max_questions,
                                    st.session_state.game_start_time,
                                    st.session_state.game_end_time
                                ):
                                    st.session_state.score_saved = True
                                    st.success(f"✅ Skor berhasil disimpan! {st.session_state.user_name} masuk papan skor.")
                                    st.rerun()
                                else:
                                    st.error("❌ Gagal menyimpan skor. Silakan coba lagi.")
                    
                    elif st.session_state.score_saved:
                        st.success("✅ Skor sudah disimpan ke papan skor!")
                    
                    if st.button("🔄 Main Lagi", use_container_width=True, type="primary"):
                        reset_game()
                        st.rerun()
                    
                    # Tombol untuk melihat papan skor
                    if st.button("🏆 Lihat Papan Skor", use_container_width=True):
                        st.session_state.current_page = "Papan Skor"
                        st.rerun()
                    
            elif st.session_state.game_started:
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("### 📝 Pertanyaan")
                    st.markdown(f"**Wilayah manakah yang disorot MERAH pada peta?**")
                
                with col2:
                    st.markdown(f"### Soal {st.session_state.total_questions + 1}/{st.session_state.max_questions}")
                
                # Tampilkan timer untuk soal saat ini
                if st.session_state.question_start_time:
                    current_question_time = time.time() - st.session_state.question_start_time
                    st.progress(min(current_question_time / 60, 1.0), 
                              text=f"⏱️ Waktu menjawab: {current_question_time:.1f} detik")
                
                st.markdown("### Pilih Jawaban:")
                
                options = st.session_state.options
                col_ans1, col_ans2 = st.columns(2)
                
                answer_selected = None
                
                with col_ans1:
                    for i, opt in enumerate(options[:len(options)//2 + len(options)%2]):
                        if st.button(f"{opt}", key=f"opt_{i}", use_container_width=True, disabled=st.session_state.answered):
                            answer_selected = opt
                
                with col_ans2:
                    for i, opt in enumerate(options[len(options)//2 + len(options)%2:]):
                        if st.button(f"{opt}", key=f"opt_{i+len(options)//2 + len(options)%2}", use_container_width=True, disabled=st.session_state.answered):
                            answer_selected = opt
                
                if answer_selected and not st.session_state.answered:
                    # Catat waktu menjawab
                    question_time = end_question_timer()
                    
                    st.session_state.total_questions += 1
                    if answer_selected == st.session_state.correct_answer:
                        st.session_state.score += 1
                        st.session_state.feedback = f"✅ **Benar! Hebat! (Waktu: {question_time:.1f} detik)**"
                    else:
                        st.session_state.feedback = f"❌ **Maaf, jawaban yang benar adalah {st.session_state.correct_answer} (Waktu: {question_time:.1f} detik)**"
                    
                    st.session_state.answered = True
                    st.rerun()
                
                if st.session_state.feedback:
                    st.markdown("---")
                    col_feedback1, col_feedback2, col_feedback3 = st.columns([1, 2, 1])
                    with col_feedback2:
                        st.markdown(f"### {st.session_state.feedback}")
                        
                        if st.session_state.answered and st.session_state.total_questions < st.session_state.max_questions:
                            if st.button("➡️ Soal Berikutnya", use_container_width=True, type="primary"):
                                pilih_wilayah()
                                st.rerun()

if "Game" in selected_menu and st.session_state.game_started and not st.session_state.game_over:
    st.markdown("---")
    col_progress1, col_progress2, col_progress3, col_progress4 = st.columns([2, 1, 1, 1])
    with col_progress1:
        progress = st.session_state.total_questions / st.session_state.max_questions
        st.progress(progress, text=f"Progress: {st.session_state.total_questions}/{st.session_state.max_questions} soal")
    with col_progress2:
        st.markdown(f"### ⭐ Skor: {st.session_state.score}")
    with col_progress3:
        st.markdown(f"### 🎯 Target: {st.session_state.max_questions}")
    with col_progress4:
        if st.session_state.game_start_time:
            current_duration = time.time() - st.session_state.game_start_time
            st.markdown(f"### ⏱️ {format_duration(current_duration)}")

# Footer dengan background dan brightness yang dapat diatur
footer_text = {
    "Game": f"🗺️ Tebak Bentuk {len(wilayah_list)} Kota dan Kabupaten di Jawa Timur | Kesulitan: {st.session_state.difficulty}",
    "Belajar": f"📚 Mode Belajar: Klik wilayah untuk info lengkap | {len(wilayah_list)} wilayah tersedia",
    "Bromo": "🌋 Gunung Bromo 3D - Jelajahi keindahan gunung berapi aktif di Jawa Timur",
    "Papan Skor": "🏆 Papan Skor Tebak Jawa Timur | Simpan skor dan kalahkan pemain lain!",
    "Statistik Waktu": "⏱️ Statistik Waktu Bermain | Pantau performa dan kecepatan menjawab",
    "Pengaturan": "⚙️ Sesuaikan pengalaman bermain Anda di Tebak Jawa Timur",
    "Tentang": "ℹ️ Tebak Jawa Timur - Aplikasi Interaktif untuk Mempelajari Geografi"
}.get(selected_menu.split(" ")[1] if " " in selected_menu else selected_menu, "🧩 Tebak Jawa Timur")

# Tampilkan footer dengan background dan brightness dari session state
st.markdown(create_footer_with_background(footer_text, FOOTER_BACKGROUND_URL, st.session_state.footer_brightness), unsafe_allow_html=True)
