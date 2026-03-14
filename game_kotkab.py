import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import json
import os
import pandas as pd
from datetime import datetime
import time

# Konfigurasi halaman - HARUS di paling atas
st.set_page_config(
    page_title="Tebak Jawa Timur", 
    page_icon="🧩", 
    layout="wide"
)

# ==================== FUNGSI SEDERHANA ====================

@st.cache_data
def load_data():
    """Load GeoJSON data dengan caching"""
    try:
        if not os.path.exists("kabkot_jatim.geojson"):
            st.error("File kabkot_jatim.geojson tidak ditemukan!")
            return None, []
        
        with open("kabkot_jatim.geojson", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Ekstrak nama wilayah
        wilayah_list = []
        for feature in data.get('features', []):
            props = feature.get('properties', {})
            name = props.get('WADMKK') or props.get('NAMOBJ', '')
            if name and name not in wilayah_list:
                wilayah_list.append(name)
        
        return data, sorted(wilayah_list)
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, []

@st.cache_data
def load_scoreboard():
    """Load scoreboard dengan caching"""
    try:
        if os.path.exists("scoreboard.json"):
            with open("scoreboard.json", 'r') as f:
                return json.load(f)
        return []
    except:
        return []

def save_scoreboard(data):
    """Save scoreboard"""
    try:
        with open("scoreboard.json", 'w') as f:
            json.dump(data[:10], f, indent=2)
        st.cache_data.clear()
        return True
    except:
        return False

# ==================== INITIALIZATION ====================

# Load data
geojson_data, WILAYAH_LIST = load_data()

if geojson_data is None:
    st.stop()

# Session state minimal
if 'page' not in st.session_state:
    st.session_state.page = 'game'
if 'name' not in st.session_state:
    st.session_state.name = ''
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.question_num = 0
    st.session_state.max_questions = 10
    st.session_state.current_region = None
    st.session_state.options = []
    st.session_state.answered = False
    st.session_state.feedback = ''
    st.session_state.questions_asked = []
    st.session_state.difficulty = 'Normal'

# ==================== FUNGSI GAME ====================

def start_game():
    """Mulai game baru"""
    st.session_state.game_started = True
    st.session_state.score = 0
    st.session_state.question_num = 0
    st.session_state.questions_asked = []
    next_question()

def next_question():
    """Siapkan pertanyaan berikutnya"""
    if st.session_state.question_num >= st.session_state.max_questions:
        st.session_state.game_started = False
        return
    
    # Pilih wilayah
    available = [w for w in WILAYAH_LIST if w not in st.session_state.questions_asked]
    if not available:
        st.session_state.questions_asked = []
        available = WILAYAH_LIST
    
    target = random.choice(available)
    st.session_state.questions_asked.append(target)
    st.session_state.current_region = target
    
    # Buat opsi jawaban
    others = [w for w in WILAYAH_LIST if w != target]
    option_count = {'Mudah': 2, 'Normal': 4, 'Sulit': 6}[st.session_state.difficulty]
    options = random.sample(others, min(option_count, len(others))) + [target]
    random.shuffle(options)
    
    st.session_state.options = options
    st.session_state.answered = False
    st.session_state.feedback = ''
    st.session_state.question_num += 1

def check_answer(answer):
    """Cek jawaban"""
    if answer == st.session_state.current_region:
        st.session_state.score += 1
        st.session_state.feedback = "✅ Benar!"
    else:
        st.session_state.feedback = f"❌ Salah! Jawaban: {st.session_state.current_region}"
    
    st.session_state.answered = True

# ==================== SIDEBAR ====================

with st.sidebar:
    st.title("🧩 Tebak Jatim")
    
    # Input nama
    if not st.session_state.name:
        st.session_state.name = st.text_input("Nama Anda", placeholder="Masukkan nama")
        if st.session_state.name:
            st.rerun()
    else:
        st.success(f"👋 Halo, {st.session_state.name}!")
        
        # Navigasi
        page = st.radio("Menu", ["🎮 Game", "📚 Belajar", "🏆 Papan Skor", "⚙️ Pengaturan"])
        st.session_state.page = page.split(" ")[1].lower()
        
        if st.button("🔄 Ganti Nama"):
            st.session_state.name = ''
            st.rerun()
        
        # Kontrol game
        if st.session_state.page == 'game' and not st.session_state.game_started:
            if st.button("🎮 Mulai Game", type="primary", use_container_width=True):
                start_game()
                st.rerun()
        
        # Statistik game
        if st.session_state.game_started:
            st.markdown("---")
            st.markdown(f"**Skor:** {st.session_state.score}")
            st.markdown(f"**Soal:** {st.session_state.question_num}/{st.session_state.max_questions}")
            st.progress(st.session_state.question_num / st.session_state.max_questions)

# ==================== HALAMAN GAME ====================

if st.session_state.page == 'game':
    st.title("🎮 Tebak Wilayah Jawa Timur")
    
    if st.session_state.game_started:
        # Peta
        m = folium.Map(location=[-7.5, 112.3], zoom_start=8, control_scale=True)
        
        # Style function untuk highlight wilayah yang ditanyakan
        def style_function(feature):
            name = feature['properties'].get('WADMKK') or feature['properties'].get('NAMOBJ', '')
            if name == st.session_state.current_region:
                return {'fillColor': '#ff0000', 'color': '#ff0000', 'weight': 3, 'fillOpacity': 0.7}
            return {'fillColor': '#3388ff', 'color': '#ffffff', 'weight': 1, 'fillOpacity': 0.3}
        
        folium.GeoJson(geojson_data, style_function=style_function).add_to(m)
        st_folium(m, width=None, height=400, key="game_map")
        
        # Pertanyaan
        st.markdown(f"### Soal {st.session_state.question_num}/{st.session_state.max_questions}")
        st.markdown("**Wilayah manakah yang berwarna MERAH?**")
        
        # Tombol jawaban
        if not st.session_state.answered:
            cols = st.columns(2)
            for i, opt in enumerate(st.session_state.options):
                with cols[i % 2]:
                    if st.button(opt, key=f"btn_{i}", use_container_width=True):
                        check_answer(opt)
                        st.rerun()
        else:
            # Feedback
            st.markdown(f"### {st.session_state.feedback}")
            
            if st.session_state.question_num < st.session_state.max_questions:
                if st.button("➡️ Soal Berikutnya", type="primary", use_container_width=True):
                    next_question()
                    st.rerun()
            else:
                st.markdown("## 🎮 Game Selesai!")
                st.markdown(f"### Skor Akhir: {st.session_state.score}/{st.session_state.max_questions}")
                
                # Simpan skor
                if st.button("💾 Simpan Skor", type="primary", use_container_width=True):
                    scoreboard = load_scoreboard()
                    scoreboard.append({
                        'nama': st.session_state.name,
                        'skor': st.session_state.score,
                        'total': st.session_state.max_questions,
                        'level': st.session_state.difficulty,
                        'tanggal': datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    if save_scoreboard(scoreboard):
                        st.success("✅ Skor tersimpan!")
                        st.rerun()
                
                if st.button("🔄 Main Lagi", use_container_width=True):
                    start_game()
                    st.rerun()
    
    else:
        # Tampilan sebelum game dimulai
        st.info("👈 Klik 'Mulai Game' di sidebar untuk bermain!")
        
        # Preview peta
        m = folium.Map(location=[-7.5, 112.3], zoom_start=8)
        folium.GeoJson(geojson_data, style_function=lambda x: {'fillColor': '#3388ff', 'fillOpacity': 0.3}).add_to(m)
        st_folium(m, width=None, height=400)

# ==================== HALAMAN BELAJAR ====================

elif st.session_state.page == 'belajar':
    st.title("📚 Mode Belajar")
    st.markdown(f"**Total Wilayah:** {len(WILAYAH_LIST)} (Klik pada peta untuk info)")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        m = folium.Map(location=[-7.5, 112.3], zoom_start=8)
        
        folium.GeoJson(
            geojson_data,
            style_function=lambda x: {'fillColor': '#33cc33', 'fillOpacity': 0.5},
            tooltip=folium.GeoJsonTooltip(fields=['WADMKK', 'NAMOBJ'], aliases=['Kab/Kota:', 'Nama:']),
            highlight_function=lambda x: {'fillColor': '#ffaa00', 'fillOpacity': 0.7}
        ).add_to(m)
        
        map_data = st_folium(m, width=None, height=500)
        
        if map_data and map_data.get('last_active_drawing'):
            props = map_data['last_active_drawing'].get('properties', {})
            wilayah = props.get('WADMKK') or props.get('NAMOBJ', '')
            if wilayah:
                st.session_state['selected'] = wilayah
    
    with col2:
        if 'selected' in st.session_state:
            st.markdown(f"### 📍 {st.session_state.selected}")
            st.markdown("""
            **Informasi:**
            - Provinsi: Jawa Timur
            - Klik wilayah lain untuk info lebih lanjut
            """)
        else:
            st.info("👆 Klik wilayah di peta")

# ==================== HALAMAN PAPAN SKOR ====================

elif st.session_state.page == 'papan skor':
    st.title("🏆 Papan Skor")
    
    scoreboard = load_scoreboard()
    
    if scoreboard:
        # Sorting
        scoreboard.sort(key=lambda x: (-x['skor'], x['total']))
        
        # Tampilkan 10 teratas
        for i, entry in enumerate(scoreboard[:10], 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            
            with st.container():
                cols = st.columns([1, 3, 2, 2, 3])
                cols[0].markdown(f"**{medal}**")
                cols[1].markdown(f"**{entry['nama']}**")
                cols[2].markdown(f"{entry['skor']}/{entry['total']}")
                cols[3].markdown(entry['level'])
                cols[4].markdown(entry['tanggal'][:10])
                st.divider()
    else:
        st.info("Belum ada skor. Mainkan game dan simpan skor Anda!")

# ==================== HALAMAN PENGATURAN ====================

elif st.session_state.page == 'pengaturan':
    st.title("⚙️ Pengaturan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎮 Pengaturan Game")
        max_q = st.slider("Jumlah Soal", 5, 20, st.session_state.max_questions)
        difficulty = st.selectbox("Kesulitan", ["Mudah", "Normal", "Sulit"], 
                                 index=["Mudah", "Normal", "Sulit"].index(st.session_state.difficulty))
        
        if st.button("Simpan Pengaturan"):
            st.session_state.max_questions = max_q
            st.session_state.difficulty = difficulty
            st.success("✅ Pengaturan tersimpan!")
    
    with col2:
        st.markdown("### 🗑️ Admin")
        if st.button("Reset Semua Skor", type="secondary"):
            if os.path.exists("scoreboard.json"):
                os.remove("scoreboard.json")
                st.cache_data.clear()
                st.success("✅ Skor direset!")
                st.rerun()

# ==================== FOOTER ====================

st.markdown("---")
col1, col2, col3 = st.columns(3)
with col2:
    st.markdown(f"""
    <div style='text-align: center; color: #666;'>
        <p>🧩 Tebak Jawa Timur | {datetime.now().strftime('%H:%M:%S')} WIB</p>
    </div>
    """, unsafe_allow_html=True)
