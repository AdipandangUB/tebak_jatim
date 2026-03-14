import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import json
import os
import pandas as pd
from datetime import datetime
import time

# Konfigurasi halaman
st.set_page_config(
    page_title="Tebak Jawa Timur", 
    page_icon="🧩", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cache untuk loading data
@st.cache_data
def load_geojson(filename):
    """Memuat file GeoJSON dengan caching"""
    try:
        if not os.path.exists(filename):
            st.error(f"File {filename} tidak ditemukan")
            return None
        
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if data.get('type') != 'FeatureCollection':
            st.error("Format GeoJSON tidak valid")
            return None
        
        return data
    except Exception as e:
        st.error(f"Error membaca file: {str(e)}")
        return None

@st.cache_data
def process_geojson_features(features):
    """Memproses fitur GeoJSON dengan caching"""
    wilayah_dict = {}
    
    for feature in features:
        props = feature.get('properties', {})
        
        if props.get('WADMPR') != 'Jawa Timur':
            continue
        
        kab_kota = props.get('WADMKK', '')
        nama_obj = props.get('NAMOBJ', '')
        
        wilayah_name = kab_kota.strip() if kab_kota and kab_kota.strip() else (nama_obj.strip() if nama_obj else None)
        
        if wilayah_name and wilayah_name not in wilayah_dict:
            new_feature = {
                "type": "Feature",
                "properties": {"name": wilayah_name},
                "geometry": feature.get('geometry')
            }
            wilayah_dict[wilayah_name] = new_feature
    
    return list(wilayah_dict.values())

# Inisialisasi session state minimal
def init_session_state():
    """Inisialisasi session state dengan nilai default"""
    defaults = {
        "user_name": "",
        "name_submitted": False,
        "score": 0,
        "total_questions": 0,
        "max_questions": 10,
        "current_region": None,
        "options": [],
        "feedback": "",
        "answered": False,
        "correct_answer": "",
        "game_over": False,
        "questions_asked": [],
        "game_started": False,
        "current_page": "Game",
        "difficulty": "Normal",
        "selected_wilayah_info": None,
        "score_saved": False,
        "footer_brightness": 0.7,
        "game_start_time": None,
        "game_end_time": None,
        "question_start_time": None,
        "question_times": [],
        "session_start_time": time.time()
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Constants
GEOJSON_FILE = "kabkot_jatim.geojson"
SCOREBOARD_FILE = "scoreboard.json"
SIDEBAR_BACKGROUND_URL = "https://rayadventure.com/wp-content/uploads/2018/06/tempat-wisata-di-jawa-timur.jpg"
FOOTER_BACKGROUND_URL = "https://awsimages.detik.net.id/community/media/visual/2025/05/08/peta-jawa-timur-1746688646408_169.jpeg?w=1200"

# Load data
geojson_data = load_geojson(GEOJSON_FILE)
if geojson_data is None:
    st.stop()

all_features = geojson_data.get('features', [])
jatim_features = process_geojson_features(all_features)

jatim_geojson = {
    "type": "FeatureCollection",
    "features": jatim_features
}

wilayah_list = sorted([f["properties"]["name"] for f in jatim_features])
kota_list = [w for w in wilayah_list if w.startswith('Kota ')]
kab_list = [w for w in wilayah_list if w.startswith('Kabupaten ')]

# ==================== FUNGSI PAPAN SKOR ====================

@st.cache_data(ttl=60)
def load_scoreboard():
    """Memuat data papan skor dengan caching"""
    if os.path.exists(SCOREBOARD_FILE):
        try:
            with open(SCOREBOARD_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except:
            return []
    return []

def save_scoreboard(scoreboard):
    """Menyimpan data papan skor"""
    try:
        scoreboard.sort(key=lambda x: (-x.get("skor", 0), -x.get("timestamp", 0)))
        scoreboard = scoreboard[:10]
        
        with open(SCOREBOARD_FILE, 'w', encoding='utf-8') as f:
            json.dump(scoreboard, f, indent=2, ensure_ascii=False)
        
        # Clear cache setelah menyimpan
        st.cache_data.clear()
        return True
    except:
        return False

def add_score(nama, skor, level, total_soal, waktu_mulai=None, waktu_selesai=None):
    """Menambahkan skor baru"""
    try:
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

# ==================== FUNGSI GAME ====================

def pilih_wilayah():
    """Memilih wilayah untuk pertanyaan berikutnya"""
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
    
    # Tentukan jumlah opsi berdasarkan kesulitan
    option_counts = {"Mudah": 2, "Normal": 4, "Sulit": 6}
    num_options = min(option_counts.get(st.session_state.difficulty, 4), len(wilayah_list) - 1)
    
    others = [w for w in wilayah_list if w != target]
    options = random.sample(others, num_options) + [target]
    random.shuffle(options)
    
    st.session_state.options = options
    st.session_state.current_region = target
    st.session_state.answered = False
    st.session_state.feedback = ""
    st.session_state.game_started = True
    st.session_state.question_start_time = time.time()

def reset_game():
    """Reset state game"""
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
    
    pilih_wilayah()

def get_wilayah_info(nama_wilayah):
    """Mengembalikan informasi wilayah"""
    return {
        "geografis": f"Wilayah di Jawa Timur dengan berbagai potensi sumber daya alam.",
        "demografi": f"Penduduk dengan keragaman budaya dan tradisi khas.",
        "budaya": f"Memiliki kesenian tradisional yang masih dilestarikan.",
        "keunikan": f"Memiliki destinasi wisata dan potensi ekonomi khas.",
        "oleh_oleh": f"Produk makanan khas dan kerajinan tangan."
    }

def format_duration(seconds):
    """Format durasi"""
    if seconds is None:
        return "00:00"
    minutes = int(seconds // 60)
    seconds_remaining = int(seconds % 60)
    return f"{minutes:02d}:{seconds_remaining:02d}"

# ==================== SIDEBAR ====================

with st.sidebar:
    st.image("https://img.freepik.com/vektor-premium/peta-yang-digambar-tangan-dari-provinsi-jawa-timur-indonesia-desain-kartun-garis-sederhana-modern_242622-498.jpg", width=100)
    st.title("🧩 Tebak Jatim")
    
    now = datetime.now()
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 8px; border-radius: 10px; margin-bottom: 10px; text-align: center;">
        <p style="color: white; margin: 0;">{now.strftime('%A, %d %B %Y')}</p>
        <p style="color: white; margin: 0; font-weight: bold;">⏰ {now.strftime('%H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.name_submitted:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 10px; border-radius: 10px; margin-bottom: 10px; text-align: center;">
            <p style="color: white; margin: 0;">👋 Halo, <strong>{st.session_state.user_name}</strong>!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Menu navigasi sederhana
    menu_options = ["🎮 Game", "📚 Belajar", "🌋 Bromo 3D", "🏆 Papan Skor", "⚙️ Pengaturan"]
    selected_menu = st.radio("Menu", menu_options, label_visibility="collapsed")
    st.session_state.current_page = selected_menu.split(" ")[1]
    
    st.markdown("---")
    
    if st.button("🔄 Ganti Nama", use_container_width=True):
        st.session_state.name_submitted = False
        st.rerun()
    
    # Kontrol game di sidebar
    if "Game" in selected_menu and st.session_state.name_submitted:
        st.markdown("---")
        st.header("🎮 Kontrol Game")
        
        if not st.session_state.game_started or st.session_state.game_over:
            if st.button("🎲 Mulai Game Baru", use_container_width=True, type="primary"):
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
        
        if st.session_state.game_started and not st.session_state.game_over and st.session_state.game_start_time:
            current_duration = time.time() - st.session_state.game_start_time
            st.metric("⏱️ Waktu", format_duration(current_duration))

# ==================== INPUT NAMA ====================

if not st.session_state.name_submitted:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://img.freepik.com/vektor-premium/peta-yang-digambar-tangan-dari-provinsi-jawa-timur-indonesia-desain-kartun-garis-sederhana-modern_242622-498.jpg", width=150)
        
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <h1>🧩 Tebak Jawa Timur</h1>
            <p style="font-size: 18px;">Game interaktif pembelajaran wilayah Jawa Timur!</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("name_form"):
            name = st.text_input("Nama", placeholder="Masukkan nama Anda", max_chars=30)
            
            if st.form_submit_button("🚀 Mulai Bermain", use_container_width=True, type="primary"):
                if name.strip():
                    st.session_state.user_name = name.strip()
                    st.session_state.name_submitted = True
                    st.rerun()
                else:
                    st.error("❌ Nama tidak boleh kosong!")
    st.stop()

# ==================== KONTEN UTAMA ====================

# Game Page
if "Game" in selected_menu:
    st.title("🧩 Tebak Bentuk Kota & Kabupaten di Jawa Timur")
    
    # Game logic
    if not st.session_state.game_started and not st.session_state.game_over:
        if st.button("🎮 Mulai Game 10 Pertanyaan", use_container_width=True, type="primary"):
            st.session_state.game_start_time = time.time()
            pilih_wilayah()
            st.rerun()
    
    # Map container
    m = folium.Map(location=[-7.5, 112.3], zoom_start=8, tiles=None, control_scale=True)
    folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                    attr='Esri', name='Satellite').add_to(m)
    
    def style_function(feature):
        name = feature["properties"]["name"]
        if st.session_state.game_started and not st.session_state.game_over and name == st.session_state.current_region:
            return {"fillColor": "#ff0000", "color": "#ff0000", "weight": 3, "fillOpacity": 0.7}
        return {"fillColor": "#3388ff", "color": "#ffffff", "weight": 1.5, "fillOpacity": 0.3}
    
    folium.GeoJson(jatim_geojson, name="Wilayah Jatim", style_function=style_function).add_to(m)
    
    st_folium(m, width=None, height=500, use_container_width=True, key="game_map")
    
    # Game interface
    if st.session_state.game_started and not st.session_state.game_over:
        st.markdown(f"**Tingkat Kesulitan:** {st.session_state.difficulty}")
        st.markdown(f"### Soal {st.session_state.total_questions + 1}/{st.session_state.max_questions}")
        st.markdown("**Wilayah manakah yang disorot MERAH pada peta?**")
        
        # Timer
        if st.session_state.question_start_time:
            current_time = time.time() - st.session_state.question_start_time
            st.progress(min(current_time / 60, 1.0), text=f"⏱️ Waktu: {current_time:.1f} detik")
        
        # Answer buttons
        cols = st.columns(2)
        for i, opt in enumerate(st.session_state.options):
            with cols[i % 2]:
                if st.button(opt, key=f"ans_{i}", use_container_width=True, disabled=st.session_state.answered):
                    question_time = time.time() - st.session_state.question_start_time
                    st.session_state.total_questions += 1
                    
                    if opt == st.session_state.correct_answer:
                        st.session_state.score += 1
                        st.session_state.feedback = f"✅ Benar! (Waktu: {question_time:.1f} detik)"
                    else:
                        st.session_state.feedback = f"❌ Salah! Jawaban: {st.session_state.correct_answer} (Waktu: {question_time:.1f} detik)"
                    
                    st.session_state.question_times.append({"time": question_time, "correct": opt == st.session_state.correct_answer})
                    st.session_state.answered = True
                    st.rerun()
        
        # Feedback and next question
        if st.session_state.feedback:
            st.markdown(f"### {st.session_state.feedback}")
            if st.session_state.total_questions < st.session_state.max_questions:
                if st.button("➡️ Soal Berikutnya", use_container_width=True, type="primary"):
                    pilih_wilayah()
                    st.rerun()
    
    # Game over
    elif st.session_state.game_over:
        if not st.session_state.game_end_time:
            st.session_state.game_end_time = time.time()
        
        game_duration = st.session_state.game_end_time - st.session_state.game_start_time if st.session_state.game_start_time else 0
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("## 🎮 Game Selesai!")
            st.markdown(f"### Skor Akhir: **{st.session_state.score}/{st.session_state.max_questions}**")
            st.info(f"⏱️ **Total Waktu:** {format_duration(game_duration)}")
            
            if st.session_state.score == st.session_state.max_questions:
                st.balloons()
                st.markdown("### 🏆 Nilai Sempurna!")
            
            # Save score
            if not st.session_state.score_saved and st.session_state.score > 0:
                if st.button("💾 Simpan Skor", use_container_width=True, type="primary"):
                    if add_score(st.session_state.user_name, st.session_state.score, 
                               st.session_state.difficulty, st.session_state.max_questions,
                               st.session_state.game_start_time, st.session_state.game_end_time):
                        st.session_state.score_saved = True
                        st.success("✅ Skor tersimpan!")
                        st.rerun()
            
            if st.button("🔄 Main Lagi", use_container_width=True, type="primary"):
                reset_game()
                st.rerun()

# Belajar Page
elif "Belajar" in selected_menu:
    st.title("📚 Mode Belajar Wilayah Jawa Timur")
    st.markdown("**Klik wilayah pada peta untuk melihat informasi!**")
    
    col_map, col_info = st.columns([2, 1])
    
    with col_map:
        m = folium.Map(location=[-7.5, 112.3], zoom_start=8, tiles=None, control_scale=True)
        folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                        attr='Esri').add_to(m)
        
        geojson = folium.GeoJson(
            jatim_geojson,
            name="Wilayah Jatim",
            style_function=lambda x: {"fillColor": "#33cc33", "color": "#ffffff", "weight": 1.5, "fillOpacity": 0.5},
            tooltip=folium.GeoJsonTooltip(fields=["name"], aliases=["Wilayah:"]),
            highlight_function=lambda x: {"fillColor": "#ffaa00", "fillOpacity": 0.7}
        ).add_to(m)
        
        map_data = st_folium(m, width=None, height=500, use_container_width=True, key="belajar_map")
        
        if map_data and map_data.get("last_active_drawing"):
            props = map_data["last_active_drawing"].get("properties", {})
            if props and "name" in props:
                st.session_state.selected_wilayah_info = props["name"]
    
    with col_info:
        st.markdown("## 📋 Info Wilayah")
        if st.session_state.selected_wilayah_info:
            wilayah = st.session_state.selected_wilayah_info
            info = get_wilayah_info(wilayah)
            
            st.markdown(f"### 📍 {wilayah}")
            tabs = st.tabs(["🗺️ Geografis", "👥 Demografi", "🎭 Budaya", "✨ Keunikan"])
            
            with tabs[0]: st.write(info["geografis"])
            with tabs[1]: st.write(info["demografi"])
            with tabs[2]: st.write(info["budaya"])
            with tabs[3]: st.write(info["keunikan"])
        else:
            st.info("👆 Klik wilayah di peta untuk melihat informasi")

# Bromo 3D Page
elif "Bromo" in selected_menu:
    st.title("🌋 Gunung Bromo - Visualisasi 3D")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.components.v1.html("""
        <div style="width:100%; height:600px; border-radius: 10px; overflow: hidden;">
            <iframe src="https://sketchfab.com/models/72f1c983ba4040eab89d75eb2b0d3e32/embed" 
                    style="width:100%; height:100%;" frameborder="0" allowfullscreen></iframe>
        </div>
        """, height=620)
    
    with col2:
        st.markdown("""
        ### Informasi
        **Tinggi:** 2.329 m  
        **Status:** Aktif  
        **Lokasi:** Probolinggo, Pasuruan, Lumajang, Malang
        
        **Keunikan:**
        - Kawah aktif di tengah kaldera
        - Lautan pasir seluas 5.250 ha
        - Upacara Kasada masyarakat Tengger
        """)

# Papan Skor Page
elif "Papan Skor" in selected_menu:
    st.title("🏆 Papan Skor Pemain")
    
    # Filter
    col1, col2 = st.columns(2)
    with col1:
        level_filter = st.selectbox("Level", ["Semua Level", "Mudah", "Normal", "Sulit"])
    with col2:
        time_filter = st.selectbox("Waktu", ["Semua Waktu", "Hari Ini", "7 Hari", "30 Hari"])
    
    # Load and filter scoreboard
    scoreboard = load_scoreboard()
    
    if scoreboard:
        df = pd.DataFrame(scoreboard)
        
        # Apply filters
        if level_filter != "Semua Level":
            df = df[df["level"] == level_filter]
        
        if time_filter == "Hari Ini":
            today = datetime.now().strftime("%Y-%m-%d")
            df = df[df["tanggal_only"] == today]
        elif time_filter == "7 Hari":
            cutoff = time.time() - (7 * 24 * 3600)
            df = df[df["timestamp"] >= cutoff]
        elif time_filter == "30 Hari":
            cutoff = time.time() - (30 * 24 * 3600)
            df = df[df["timestamp"] >= cutoff]
        
        # Sort and display
        df = df.sort_values(["skor", "timestamp"], ascending=[False, False]).head(10)
        df["peringkat"] = range(1, len(df) + 1)
        df["skor_display"] = df["skor"].astype(str) + "/" + df["total_soal"].astype(str)
        
        st.dataframe(
            df[["peringkat", "nama", "skor_display", "level", "tanggal"]],
            column_config={
                "peringkat": "Peringkat",
                "nama": "Nama",
                "skor_display": "Skor",
                "level": "Level",
                "tanggal": "Tanggal"
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("Belum ada skor tersimpan")
    
    # Current user score
    st.markdown("---")
    st.markdown(f"### Skor Anda: {st.session_state.user_name}")
    st.write(f"**{st.session_state.score}/{st.session_state.max_questions}** (Level: {st.session_state.difficulty})")

# Pengaturan Page
elif "Pengaturan" in selected_menu:
    st.title("⚙️ Pengaturan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎮 Game")
        max_q = st.slider("Maksimum Soal", 5, 20, st.session_state.max_questions)
        difficulty = st.selectbox("Kesulitan", ["Mudah", "Normal", "Sulit"], 
                                 index=["Mudah", "Normal", "Sulit"].index(st.session_state.difficulty))
        
        if st.button("💾 Simpan Pengaturan Game"):
            st.session_state.max_questions = max_q
            st.session_state.difficulty = difficulty
            st.success("✅ Pengaturan tersimpan")
    
    with col2:
        st.markdown("### 🎨 Tampilan")
        brightness = st.slider("Kecerahan Footer", 0.3, 1.0, st.session_state.footer_brightness, 0.05)
        
        if brightness != st.session_state.footer_brightness:
            st.session_state.footer_brightness = brightness
            st.rerun()
    
    st.markdown("---")
    if st.button("🗑️ Reset Semua Skor", use_container_width=True):
        if os.path.exists(SCOREBOARD_FILE):
            os.remove(SCOREBOARD_FILE)
            st.cache_data.clear()
            st.success("✅ Papan skor direset")
            st.rerun()

# ==================== FOOTER ====================

footer_texts = {
    "Game": f"🎮 Tebak Bentuk {len(wilayah_list)} Wilayah | Kesulitan: {st.session_state.difficulty}",
    "Belajar": f"📚 Mode Belajar | {len(wilayah_list)} Wilayah Tersedia",
    "Bromo": "🌋 Gunung Bromo 3D",
    "Papan Skor": "🏆 Papan Skor",
    "Pengaturan": "⚙️ Pengaturan Aplikasi"
}

footer_text = footer_texts.get(selected_menu.split(" ")[1], "🧩 Tebak Jawa Timur")

# Footer dengan brightness
st.markdown(f"""
<style>
.footer-container {{
    position: relative;
    width: 100%;
    margin-top: 30px;
    padding: 20px 0;
    background-image: url("{FOOTER_BACKGROUND_URL}");
    background-size: cover;
    background-position: center;
    border-radius: 15px 15px 0 0;
    filter: brightness({st.session_state.footer_brightness});
}}
.footer-content {{
    text-align: center;
    padding: 15px;
    color: white;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
}}
</style>

<div class="footer-container">
    <div class="footer-content">
        <div style="font-weight: bold; margin-bottom: 10px;">🧩 Tebak Jawa Timur</div>
        <p>{footer_text}</p>
        <p>⏰ {datetime.now().strftime('%H:%M:%S')} WIB | © 2026</p>
    </div>
</div>
""", unsafe_allow_html=True)
