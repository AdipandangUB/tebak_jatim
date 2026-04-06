import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import json
import os
import pandas as pd
from datetime import datetime, timezone, timedelta

# Timezone WIB (UTC+7)
WIB = timezone(timedelta(hours=7))

def now_wib() -> datetime:
    """Mengembalikan waktu saat ini dalam zona waktu WIB (GMT+7)."""
    return datetime.now(WIB)
import time

# ==================== KONFIGURASI HALAMAN ====================
st.set_page_config(
    page_title="Sepiro Jawa Timur, Sampeyan",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== KONSTANTA ====================
GEOJSON_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kabkotjatim_ok.geojson")

SIDEBAR_BACKGROUND_URL = "https://rayadventure.com/wp-content/uploads/2018/06/tempat-wisata-di-jawa-timur.jpg"
FOOTER_BACKGROUND_URL = "https://static.promediateknologi.id/crop/0x0:0x0/0x0/webp/photo/p2/231/2024/09/11/Bisa-melihat-sunrise-yang-menakjubkan-di-Gunung-Bromo-Gambar-dari-Elizaveta-G-Shutterstock-213080307.png"
MUSIC_VIDEO_ID = "H1tWb3axAdA"


# ==================== DATABASE LOGO KABUPATEN DAN KOTA ====================

# Database logo untuk Kabupaten
LOGO_KABUPATEN = {
    "Bangkalan": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT_5FVeEeDgFlKsS3FhvSy21TttLuBVNZJT7w&s",
    "Banyuwangi": "https://upload.wikimedia.org/wikipedia/commons/f/f5/Lambang_Kabupaten_Banyuwangi.png",
    "Blitar": "https://upload.wikimedia.org/wikipedia/commons/9/94/Lambang_Kabupaten_Blitar.webp",
    "Bojonegoro": "https://upload.wikimedia.org/wikipedia/commons/1/18/Logo_Kabupaten_Bojonegoro.png",
    "Bondowoso": "https://upload.wikimedia.org/wikipedia/commons/9/93/Lambang_Bondowoso.png",
    "Gresik": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Lambang_Kabupaten_Gresik.png/1280px-Lambang_Kabupaten_Gresik.png",
    "Jember": "https://upload.wikimedia.org/wikipedia/commons/a/a3/Lambang-kabupaten-jember.png",
    "Jombang": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Seal_of_Jombang_Regency.svg/1920px-Seal_of_Jombang_Regency.svg.png",
    "Kediri": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Logo_Kabupaten_Kediri_%28Seal_of_Kediri_Regency%29.svg/960px-Logo_Kabupaten_Kediri_%28Seal_of_Kediri_Regency%29.svg.png",
    "Lamongan": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Lambang_Kabupaten_Lamongan.png/1280px-Lambang_Kabupaten_Lamongan.png",
    "Lumajang": "https://upload.wikimedia.org/wikipedia/commons/f/f4/Lambang_Kabupaten_Lumajang.png",
    "Madiun": "https://upload.wikimedia.org/wikipedia/commons/d/d2/Logo_kabupaten_madiun.gif",
    "Magetan": "https://upload.wikimedia.org/wikipedia/commons/7/7f/Logo_Kabupaten_Magetan_Vector.jpg",
    "Malang": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Logo_Kabupaten_Malang_-_Seal_of_Malang_Regency.svg/1280px-Logo_Kabupaten_Malang_-_Seal_of_Malang_Regency.svg.png",
    "Mojokerto": "https://upload.wikimedia.org/wikipedia/commons/e/e9/Lambang_Kabupaten_Mojokerto.png",
    "Nganjuk": "https://upload.wikimedia.org/wikipedia/commons/a/ac/NganjukLogoNew.png",
    "Ngawi": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Lambang_Kabupaten_Ngawi_%28svg%29.svg/1280px-Lambang_Kabupaten_Ngawi_%28svg%29.svg.png",
    "Pacitan": "https://img.favpng.com/23/4/1/regency-gemaharjo-pucangombo-kayen-logo-png-favpng-JfrCwheRDqTBDpZ164kEaLNES_t.jpg",
    "Pamekasan": "https://pamekasankab.go.id/img/lambang.jpg",
    "Pasuruan": "https://upload.wikimedia.org/wikipedia/commons/9/9a/Lambang_Kabupaten_Pasuruan.png",
    "Ponorogo": "https://upload.wikimedia.org/wikipedia/commons/4/4b/Lambang_Kabupaten_Ponorogo.png",
    "Probolinggo": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Flag_of_Probolinggo_Registry.png",
    "Sampang": "https://upload.wikimedia.org/wikipedia/commons/3/3a/Lambang_Kabupaten_Sampang.png",
    "Sidoarjo": "https://upload.wikimedia.org/wikipedia/commons/0/06/Lambang_Kabupaten_Sidoarjo.jpeg",
    "Situbondo": "https://upload.wikimedia.org/wikipedia/commons/b/bd/Lambang_Kabupaten_Situbondo.png",
    "Sumenep": "https://upload.wikimedia.org/wikipedia/commons/b/b9/Lambang_Kabupaten_Sumenep.png",
    "Trenggalek": "https://upload.wikimedia.org/wikipedia/commons/4/49/Trenggalek_coat_of_arms.png",
    "Tuban": "https://upload.wikimedia.org/wikipedia/commons/c/c8/Lambang_Kabupaten_Tuban.webp",
    "Tulungagung": "https://upload.wikimedia.org/wikipedia/commons/e/e1/Lambang-tulungagung.png"
}

# Database logo untuk Kota
LOGO_KOTA = {
    "Batu": "https://upload.wikimedia.org/wikipedia/commons/b/b1/Logo_kota_batu_%281%29.png",
    "Blitar": "https://upload.wikimedia.org/wikipedia/commons/5/55/Lambang_Kota_Blitar.png",
    "Kediri": "https://upload.wikimedia.org/wikipedia/commons/2/2d/Lambang_Kota_Kediri.png",
    "Madiun": "https://upload.wikimedia.org/wikipedia/commons/e/ec/Lambang_Kota_Madiun.png",
    "Malang": "https://upload.wikimedia.org/wikipedia/commons/e/ef/Logo_Kota_Malang_color.png",
    "Mojokerto": "https://upload.wikimedia.org/wikipedia/commons/9/98/Coat_of_arms_of_the_City_of_Mojokerto.svg",
    "Pasuruan": "https://upload.wikimedia.org/wikipedia/commons/e/e5/Logo_Kota_Pasuruan.png",
    "Probolinggo": "https://upload.wikimedia.org/wikipedia/commons/4/4d/Lambang_Kota_Probolinggo.png",
    "Surabaya": "https://upload.wikimedia.org/wikipedia/commons/b/ba/City_of_Surabaya_Logo.svg"
}

# Fungsi untuk mendapatkan logo berdasarkan nama wilayah
def get_logo_url(nama):
    """Mengembalikan URL logo untuk nama wilayah yang diberikan"""
    nama_clean = nama.replace("Kabupaten ", "").replace("Kota ", "")
    if nama.startswith("Kota "):
        return LOGO_KOTA.get(nama_clean, None)
    else:
        return LOGO_KABUPATEN.get(nama_clean, None)

# ==================== FUNGSI CLUE UNTUK QUIZ ====================

def get_wilayah_clue(wilayah_name):
    clues = {
        "Kota Surabaya": "🌊 Kota ini dikenal dengan sebutan Kota Pahlawan dan memiliki ikon Jembatan Suramadu.",
        "Kota Malang": "🍎 Kota ini dijuluki Kota Apel dan Kota Pendidikan dengan udara sejuk di pegunungan.",
        "Kota Batu": "🍎 Kota wisata pegunungan ini terkenal dengan wisata Jatim Park dan apelnya.",
        "Kota Kediri": "🚬 Kota ini dikenal sebagai Kota Tahu dan pusat industri rokok Gudang Garam.",
        "Kota Madiun": "🍽️ Kota ini terkenal dengan kuliner Nasi Pecel dan Brem.",
        "Kota Blitar": "🇮🇩 Kota ini terdapat tempat-tempat mengenai Presiden Indonesia Pertama, berupa: Makam Bung Karno, Istana Gebang, dan pusat peringatan Proklamator",
        "Kota Mojokerto": "🍡 Kota ini dikenal dengan onde-onde dan dekat dengan situs Kerajaan Majapahit di Trowulan.",
        "Kota Pasuruan": "🦐 Kota transit ini terkenal dengan udang dan kerupuknya.",
        "Kota Probolinggo": "🥭 Kota ini dilintasi Jalur Pantura Pulau Jawa.",
        "Banyuwangi": "🔥 Kabupaten di ujung timur Jawa Timur ini terkenal dengan Kawah Ijen yang memiliki fenomena api biru.",
        "Malang": "🏔️ Kabupaten yang mengelilingi Kota Pendidikan ini memiliki wisata Bromo, Coban Rondo, dan pantai selatan.",
        "Jember": "👗 Kabupaten ini terkenal dengan Fashion Carnival yang mendunia.",
        "Sidoarjo": "🦐 Kabupaten ini terkenal dengan lumpur Lapindo, kerupuk udang, dan Bandara Juanda.",
        "Kediri": "🌋 Kabupaten ini memiliki Gunung Kelud yang terkenal aktif dan pabrik rokok Gudang Garam.",
        "Mojokerto": "🏯 Kabupaten ini merupakan lokasi bekas ibu kota Kerajaan Majapahit di Trowulan.",
        "Pasuruan": "🌋 Kabupaten ini memiliki akses ke Gunung Bromo dari sisi Wonokitri.",
        "Probolinggo": "🌋 Kabupaten ini memiliki akses ke Gunung Bromo dari sisi Cemorolawang.",
        "Blitar": "🇮🇩 Kabupaten ini memiliki Budaya Jawa Arekan dengan tradisi Larung Sesaji ke Gunung Kelud.",
        "Tulungagung": "🪨 Kabupaten ini terkenal sebagai penghasil marmer terbesar di Indonesia.",
        "Trenggalek": "🏖️ Kabupaten ini memiliki pantai-pantai indah seperti Pantai Prigi dan Pantai Pasir Putih.",
        "Ponorogo": "🎭 Kabupaten ini terkenal dengan kesenian Reog yang mendunia.",
        "Pacitan": "🕳️ Kabupaten ini dijuluki Kota 1001 Goa, terkenal dengan Goa Gong.",
        "Ngawi": "🏰 Kabupaten ini memiliki Benteng Van den Bosch peninggalan Belanda.",
        "Magetan": "🌊 Kabupaten ini terkenal dengan Telaga Sarangan di kaki Gunung Lawu.",
        "Nganjuk": "🥬 Kabupaten ini terdapat Candi Lor dan Candi Ngetos.",
        "Jombang": "🕌 Kabupaten ini dikenal sebagai Kota Santri dengan pesantren besar seperti Tebuireng.",
        "Bojonegoro": "🛢️ Kabupaten ini terkenal sebagai kota minyak dengan sumur minyak tradisional.",
        "Tuban": "🕌 Kabupaten ini memiliki Makam Sunan Bonang, salah satu Wali Songo.",
        "Lamongan": "🍲 Kabupaten ini terkenal dengan kuliner Soto dan Makam Sunan Drajat.",
        "Gresik": "🏭 Kabupaten industri ini memiliki Makam Sunan Giri dan Smelter PT. Freeport.",
        "Bangkalan": "🌉 Kabupaten di Madura ini merupakan pintu masuk dari Surabaya melalui Jembatan Suramadu.",
        "Sampang": "🐃 Kabupaten di Madura ini terkenal dengan tradisi Karapan Sapi.",
        "Pamekasan": "🐃 Kabupaten di Madura ini terkenal dengan Festival Karapan Sapi dan Kerajinan batik tulis.",
        "Sumenep": "🏝️ Kabupaten di ujung timur Madura ini memiliki Keraton dan Kepulauan Kangean.",
        "Bondowoso": "🍯 Kabupaten ini dikenal sebagai Daerah Penghasil Tape dan Kopi.",
        "Situbondo": "🦏 Kabupaten ini memiliki Taman Nasional Baluran yang dijuluki Africa van Java.",
        "Lumajang": "🏔️ Kabupaten di kaki Gunung Semeru ini terkenal dengan pisang agung.",
    }
    if wilayah_name in clues:
        return f"💡 {clues[wilayah_name]}"
    else:
        return f"💡 {wilayah_name} memiliki potensi wisata dan budaya yang khas di Jawa Timur."

# ==================== FUNGSI EFEK BALON ====================

def get_perfect_score_markdown_effect():
    return """
    <style>
    @keyframes drift {
        0%   { transform: translateY(0) rotate(0deg) scale(1); opacity:1; }
        100% { transform: translateY(-110vh) rotate(720deg) scale(0.5); opacity:0; }
    }
    @keyframes sway {
        0%,100% { margin-left: 0; }
        25%     { margin-left: 40px; }
        75%     { margin-left: -40px; }
    }
    @keyframes popIn {
        0%   { transform: scale(0) rotate(-10deg); opacity:0; }
        100% { transform: scale(1) rotate(0deg); opacity:1; }
    }
    .perfect-banner {
        animation: popIn 0.7s cubic-bezier(0.175,0.885,0.32,1.275) forwards;
        text-align: center;
        padding: 24px 20px;
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
        border-radius: 20px;
        border: 3px solid #ffd700;
        margin: 10px 0 18px 0;
        position: relative;
        overflow: hidden;
    }
    .perfect-title {
        font-size: 2.4em;
        font-weight: 900;
        color: #ffd700;
        letter-spacing: 3px;
        margin: 0 0 6px 0;
    }
    .perfect-sub {
        font-size: 1.05em;
        color: #fff;
        margin: 6px 0;
    }
    .balloon-float {
        display: inline-block;
        font-size: 2.1em;
        animation: drift 3s ease-in infinite, sway 1.5s ease-in-out infinite;
        margin: 0 5px;
    }
    .balloon-float:nth-child(1)  { animation-delay: 0.0s, 0.0s; color: #ff6b6b; }
    .balloon-float:nth-child(2)  { animation-delay: 0.3s, 0.3s; color: #ffd93d; }
    .balloon-float:nth-child(3)  { animation-delay: 0.6s, 0.6s; color: #6bcb77; }
    .balloon-float:nth-child(4)  { animation-delay: 0.9s, 0.9s; color: #4d96ff; }
    .balloon-float:nth-child(5)  { animation-delay: 1.2s, 1.2s; color: #c77dff; }
    .balloon-float:nth-child(6)  { animation-delay: 1.5s, 1.5s; color: #ff6bd6; }
    .balloon-float:nth-child(7)  { animation-delay: 0.15s, 0.15s; color: #ff8e53; }
    .balloon-float:nth-child(8)  { animation-delay: 0.45s, 0.45s; color: #00c9a7; }
    .balloon-float:nth-child(9)  { animation-delay: 0.75s, 0.75s; color: #ffb703; }
    .balloon-float:nth-child(10) { animation-delay: 1.05s, 1.05s; color: #f72585; }
    </style>
    <div class="perfect-banner">
        <div style="margin-bottom:14px;">
            <span class="balloon-float">🎈</span><span class="balloon-float">🎈</span>
            <span class="balloon-float">🎈</span><span class="balloon-float">🎈</span>
            <span class="balloon-float">🎈</span><span class="balloon-float">🎈</span>
            <span class="balloon-float">🎈</span><span class="balloon-float">🎈</span>
            <span class="balloon-float">🎈</span><span class="balloon-float">🎈</span>
        </div>
        <p class="perfect-title">🏆 NILAI SEMPURNA! 🏆</p>
        <p class="perfect-sub">Luar biasa! Semua soal dijawab dengan benar! 🌟</p>
        <div class="emoji-row">🎉 🎊 🥳 🎁 🎀 🎶 💖 🎊 🎉</div>
    </div>
    """

def get_balloon_effect_html():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      body { background: transparent; overflow: hidden; width: 100%; height: 320px; position: relative; }
      #congrats-text { position: absolute; top: 18px; left: 50%; transform: translateX(-50%); z-index: 999; text-align: center; }
      #congrats-text h1 { font-family: 'Arial Rounded MT Bold', Arial, sans-serif; font-size: 30px; color: #fff; text-shadow: 0 3px 12px rgba(0,0,0,0.5); }
      .balloon { position: absolute; bottom: -120px; border-radius: 50%; animation: floatUp linear infinite; }
      @keyframes floatUp { 0% { bottom: -130px; opacity: 0; } 100% { bottom: 110%; opacity: 0; } }
    </style>
    </head>
    <body>
    <div id="congrats-text"><h1>🏆 NILAI SEMPURNA! 🏆</h1></div>
    <div id="balloon-container"></div>
    <script>
    (function() {
      var colors = ['#FF6B6B','#FF8E53','#FFD93D','#6BCB77','#4D96FF','#C77DFF','#FF6BD6','#00C9A7'];
      var bc = document.getElementById('balloon-container');
      for (var i = 0; i < 24; i++) {
        var b = document.createElement('div');
        b.className = 'balloon';
        b.style.background = colors[i % colors.length];
        b.style.width = (42 + Math.random() * 22) + 'px';
        b.style.height = Math.round(b.style.width.slice(0,-2) * 1.22) + 'px';
        b.style.left = (2 + (i / 24) * 96) + '%';
        b.style.animationDuration = (4.2 + Math.random() * 5).toFixed(2) + 's';
        b.style.animationDelay = (Math.random() * 3.8).toFixed(2) + 's';
        bc.appendChild(b);
      }
    })();
    </script>
    </body>
    </html>
    """

# ==================== FUNGSI BACKSOUND ====================

def get_backsound_html(volume=30):
    return f"""
    <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ background: transparent; overflow: hidden; display: flex; align-items: center; justify-content: center; height: 54px; }}
    #backsound-btn {{
        display: inline-flex; align-items: center; gap: 10px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 50px; padding: 10px 20px;
        cursor: pointer; color: white; font-size: 13px; font-weight: bold;
    }}
    #yt-iframe-hidden {{ display: none; width: 0; height: 0; position: absolute; pointer-events: none; }}
    #music-visualizer {{ display: flex; align-items: flex-end; gap: 2px; height: 18px; }}
    .music-bar {{ width: 3px; background: linear-gradient(to top, #ffd700, #fff); border-radius: 2px; animation: musicBounce 0.7s ease-in-out infinite alternate; }}
    .music-bar:nth-child(1) {{ animation-delay: 0.00s; height: 6px; }}
    .music-bar:nth-child(2) {{ animation-delay: 0.15s; height: 14px; }}
    .music-bar:nth-child(3) {{ animation-delay: 0.05s; height: 9px; }}
    .music-bar:nth-child(4) {{ animation-delay: 0.20s; height: 16px; }}
    .music-bar:nth-child(5) {{ animation-delay: 0.10s; height: 7px; }}
    @keyframes musicBounce {{
        from {{ transform: scaleY(0.35); opacity: 0.55; }}
        to   {{ transform: scaleY(1.15); opacity: 1.0; }}
    }}
    .music-bar.paused {{ animation: none !important; height: 3px !important; opacity: 0.4; }}
    </style>
    <iframe id="yt-iframe-hidden" src="https://www.youtube.com/embed/{MUSIC_VIDEO_ID}?autoplay=1&loop=1&playlist={MUSIC_VIDEO_ID}&enablejsapi=1&controls=0" allow="autoplay"></iframe>
    <div id="backsound-btn" onclick="toggleMusic()">
        <div id="music-visualizer"><div class="music-bar"></div><div class="music-bar"></div><div class="music-bar"></div><div class="music-bar"></div><div class="music-bar"></div></div>
        <span id="music-label">🎵 Musik On</span>
    </div>
    <script>
    (function() {{
        var isMusicPlaying = true, ytPlayer = null, initVolume = {volume};
        if (!window._ytApiLoaded) {{
            window._ytApiLoaded = true;
            var tag = document.createElement('script');
            tag.src = "https://www.youtube.com/iframe_api";
            document.head.appendChild(tag);
        }}
        window.onYouTubeIframeAPIReady = function() {{
            ytPlayer = new YT.Player('yt-iframe-hidden', {{
                events: {{
                    'onReady': function(event) {{ event.target.setVolume(initVolume); event.target.playVideo(); }},
                    'onStateChange': function(event) {{ if (event.data === YT.PlayerState.ENDED) event.target.playVideo(); }}
                }}
            }});
        }};
        window.toggleMusic = function() {{
            var bars = document.querySelectorAll('.music-bar'), label = document.getElementById('music-label');
            if (isMusicPlaying) {{
                if (ytPlayer && ytPlayer.pauseVideo) ytPlayer.pauseVideo();
                bars.forEach(b => b.classList.add('paused'));
                label.textContent = '🎵 Musik Off';
                isMusicPlaying = false;
            }} else {{
                if (ytPlayer && ytPlayer.playVideo) ytPlayer.playVideo();
                bars.forEach(b => b.classList.remove('paused'));
                label.textContent = '🎵 Musik On';
                isMusicPlaying = true;
            }}
        }};
    }})();
    </script>
    """


# ==================== PAPAN SKOR ====================

def load_scoreboard():
    if "scoreboard_data" not in st.session_state:
        st.session_state.scoreboard_data = []
    return list(st.session_state.scoreboard_data)

def save_scoreboard(scoreboard):
    try:
        if not isinstance(scoreboard, list):
            scoreboard = []
        scoreboard.sort(key=lambda x: (-x.get("skor", 0), -x.get("timestamp", 0)))
        scoreboard = scoreboard[:10]
        st.session_state.scoreboard_data = scoreboard
        return True
    except Exception as e:
        st.error(f"Error menyimpan skor: {str(e)}")
        return False

def add_score(nama, skor, level, total_soal, waktu_mulai=None, waktu_selesai=None):
    try:
        if not nama or not isinstance(skor, (int, float)) or not isinstance(total_soal, (int, float)):
            return False
        scoreboard = load_scoreboard()
        durasi = None
        if waktu_mulai and waktu_selesai:
            durasi_detik = waktu_selesai - waktu_mulai
            durasi = {"detik": round(durasi_detik, 1), "format": f"{int(durasi_detik // 60)} menit {int(durasi_detik % 60)} detik"}
        now = now_wib()
        new_entry = {
            "nama": str(nama), "skor": int(skor), "level": str(level), "total_soal": int(total_soal),
            "persentase": round((int(skor) / int(total_soal)) * 100, 1),
            "tanggal": now.strftime("%Y-%m-%d %H:%M:%S"), "tanggal_only": now.strftime("%Y-%m-%d"),
            "tahun": now.year, "bulan": now.month, "timestamp": time.time(),
            "durasi": durasi, "waktu_mulai": waktu_mulai, "waktu_selesai": waktu_selesai
        }
        scoreboard.append(new_entry)
        return save_scoreboard(scoreboard)
    except Exception as e:
        st.error(f"Error menambah skor: {str(e)}")
        return False

def get_filtered_scoreboard(level_filter="Semua Level", time_filter="Semua Waktu"):
    scoreboard = load_scoreboard()
    if level_filter != "Semua Level" and scoreboard:
        scoreboard = [s for s in scoreboard if s.get("level") == level_filter]
    if time_filter != "Semua Waktu" and scoreboard:
        now = now_wib()
        if time_filter == "Hari Ini":
            today_str = now.strftime("%Y-%m-%d")
            scoreboard = [s for s in scoreboard if s.get("tanggal_only") == today_str]
        elif time_filter == "7 Hari Terakhir":
            cutoff = now.timestamp() - (7 * 24 * 3600)
            scoreboard = [s for s in scoreboard if s.get("timestamp", 0) >= cutoff]
        elif time_filter == "30 Hari Terakhir":
            cutoff = now.timestamp() - (30 * 24 * 3600)
            scoreboard = [s for s in scoreboard if s.get("timestamp", 0) >= cutoff]
        elif time_filter == "Bulan Ini":
            scoreboard = [s for s in scoreboard if s.get("tahun") == now.year and s.get("bulan") == now.month]
    scoreboard.sort(key=lambda x: (-x.get("skor", 0), x.get("durasi", {}).get("detik", float('inf')), -x.get("timestamp", 0)))
    return scoreboard

def get_scoreboard_stats(scoreboard):
    if not scoreboard:
        return {"total_pemain": 0, "skor_tertinggi": 0, "rata_rata": 0, "level_populer": "-", "waktu_tercepat": None}
    total_pemain = len(scoreboard)
    skor_tertinggi = max(s.get("skor", 0) for s in scoreboard)
    rata_rata = sum(s.get("skor", 0) for s in scoreboard) / total_pemain
    level_counts = {}
    for s in scoreboard:
        lv = s.get("level", "Unknown")
        level_counts[lv] = level_counts.get(lv, 0) + 1
    level_populer = max(level_counts, key=level_counts.get) if level_counts else "-"
    waktu_tercepat = None
    for s in scoreboard:
        if s.get("durasi") and s["durasi"].get("detik") and s.get("skor") == s.get("total_soal"):
            if not waktu_tercepat or s["durasi"]["detik"] < waktu_tercepat["detik"]:
                waktu_tercepat = {"nama": s.get("nama"), "detik": s["durasi"]["detik"], "format": s["durasi"]["format"]}
    return {"total_pemain": total_pemain, "skor_tertinggi": skor_tertinggi, "rata_rata": round(rata_rata, 1), "level_populer": level_populer, "waktu_tercepat": waktu_tercepat}

# ==================== PAPAN SKOR PUZZLE ====================

def load_puzzle_scoreboard():
    if "puzzle_scoreboard_data" not in st.session_state:
        st.session_state.puzzle_scoreboard_data = []
    return list(st.session_state.puzzle_scoreboard_data)

def save_puzzle_scoreboard(scoreboard):
    try:
        if not isinstance(scoreboard, list):
            scoreboard = []
        scoreboard.sort(key=lambda x: (x.get("poin_penalti", float("inf")), -x.get("timestamp", 0)))
        scoreboard = scoreboard[:10]
        st.session_state.puzzle_scoreboard_data = scoreboard
        return True
    except Exception as e:
        st.error(f"Error menyimpan skor puzzle: {str(e)}")
        return False

def add_puzzle_score(nama, waktu_detik, kesalahan):
    try:
        if not nama or waktu_detik is None:
            return False
        scoreboard = load_puzzle_scoreboard()
        now = now_wib()
        menit = int(waktu_detik // 60)
        detik = int(waktu_detik % 60)
        poin_penalti = round(waktu_detik + kesalahan * 10, 1)
        new_entry = {
            "nama": str(nama), "waktu_detik": round(float(waktu_detik), 1),
            "waktu_format": f"{menit:02d}:{detik:02d}", "kesalahan": int(kesalahan),
            "poin_penalti": poin_penalti, "tanggal": now.strftime("%Y-%m-%d %H:%M:%S"),
            "tanggal_only": now.strftime("%Y-%m-%d"), "tahun": now.year, "bulan": now.month,
            "timestamp": time.time()
        }
        scoreboard.append(new_entry)
        return save_puzzle_scoreboard(scoreboard)
    except Exception as e:
        st.error(f"Error menambah skor puzzle: {str(e)}")
        return False

def get_puzzle_scoreboard_stats(scoreboard):
    if not scoreboard:
        return {"total_entri": 0, "waktu_tercepat": None, "rata_waktu": None}
    total = len(scoreboard)
    tercepat = min(scoreboard, key=lambda x: x.get("waktu_detik", float("inf")))
    rata_w = sum(s.get("waktu_detik", 0) for s in scoreboard) / total
    return {"total_entri": total, "waktu_tercepat": tercepat, "rata_waktu": round(rata_w, 1)}


# ==================== LOAD & PROSES GEOJSON ====================

@st.cache_data(show_spinner="Memuat data wilayah...")
def load_and_process_geojson(filepath):
    if not os.path.exists(filepath):
        return None, f"File GeoJSON tidak ditemukan: {filepath}"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception as e:
        return None, f"Gagal membaca file GeoJSON: {e}"
    if raw.get("type") != "FeatureCollection":
        return None, "Format GeoJSON tidak valid"
    features = raw.get("features", [])
    wilayah_dict = {}
    for feat in features:
        props = feat.get("properties", {})
        if props.get("WADMPR") != "Jawa Timur":
            continue
        nama = props.get("WADMKK", "").strip()
        if not nama:
            continue
        geom = feat.get("geometry")
        if not geom or not geom.get("coordinates"):
            continue
        if nama not in wilayah_dict:
            wilayah_dict[nama] = {"properties": props, "features": []}
        wilayah_dict[nama]["features"].append(feat)
    result_features = []
    for nama, data in wilayah_dict.items():
        merged = _merge_geometries(data["features"])
        if not merged:
            merged = data["features"][0].get("geometry")
        if not merged:
            continue
        result_features.append({
            "type": "Feature",
            "properties": {"name": nama, "WADMKK": nama, "WADMPR": "Jawa Timur"},
            "geometry": merged
        })
    geojson = {"type": "FeatureCollection", "features": result_features}
    wilayah_list = sorted({f["properties"]["name"] for f in result_features})
    return (geojson, wilayah_list), None

def _merge_geometries(features):
    all_coords = []
    for feat in features:
        geom = feat.get("geometry", {})
        coords = geom.get("coordinates")
        if not coords:
            continue
        if geom.get("type") == "Polygon":
            all_coords.append(coords)
        elif geom.get("type") == "MultiPolygon":
            all_coords.extend(coords)
    if all_coords:
        return {"type": "MultiPolygon", "coordinates": all_coords}
    return None

# ==================== LOAD DATA ====================

result, error = load_and_process_geojson(GEOJSON_FILE)
if error or result is None:
    st.error(f"❌ Gagal memuat data GeoJSON: {error}")
    st.stop()

jatim_geojson, wilayah_list = result
kota_list = [w for w in wilayah_list if w.startswith("Kota ")]
kab_list = [w for w in wilayah_list if not w.startswith("Kota ")]


# ==================== FUNGSI WAKTU ====================

def get_current_time_info():
    now = now_wib()
    return {"tanggal": now.strftime("%Y-%m-%d"), "jam": now.strftime("%H:%M:%S"), "hari": now.strftime("%A")}

def format_duration(seconds):
    if seconds is None:
        return "00:00"
    return f"{int(seconds // 60):02d}:{int(seconds % 60):02d}"

def get_session_duration():
    if st.session_state.get("session_start_time"):
        return time.time() - st.session_state.session_start_time
    return 0


# ==================== INISIALISASI SESSION STATE ====================

_defaults = {
    "user_name": "", "name_submitted": False, "score": 0, "total_questions": 0, "max_questions": 10,
    "current_region": None, "options": [], "feedback": "", "answered": False, "correct_answer": "",
    "game_over": False, "questions_asked": [], "game_started": False, "difficulty": "Normal",
    "selected_wilayah_info": None, "score_saved": False, "game_start_time": None, "game_end_time": None,
    "question_start_time": None, "total_game_duration": 0, "question_times": [], "average_answer_time": 0,
    "session_start_time": time.time(), "footer_brightness": 0.7, "scoreboard_data": [],
    "music_volume": 30, "balloon_shown": False,  # KUNCI: untuk melacak apakah balon sudah ditampilkan
    "puzzle_started": False, "puzzle_start_time": None, "puzzle_completed": False,
    "puzzle_scoreboard_data": [], "puzzle_result_time_sec": None, "puzzle_result_errors": None,
    "puzzle_score_saved": False, "pending_navigation": None, "puzzle_js_waktu": None, "puzzle_js_errors": None,
}
for key, val in _defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ==================== FUNGSI TIMER ====================

def start_question_timer():
    st.session_state.question_start_time = time.time()

def end_question_timer(is_correct=False):
    if st.session_state.question_start_time:
        duration = time.time() - st.session_state.question_start_time
        st.session_state.question_times.append({
            "question_number": st.session_state.total_questions + 1, "duration": duration, "correct": is_correct
        })
        total = sum(q["duration"] for q in st.session_state.question_times)
        st.session_state.average_answer_time = total / len(st.session_state.question_times)
        return duration
    return 0

def end_game_timer():
    if st.session_state.game_start_time:
        if not st.session_state.game_end_time:
            st.session_state.game_end_time = time.time()
        st.session_state.total_game_duration = st.session_state.game_end_time - st.session_state.game_start_time
        return st.session_state.total_game_duration
    return st.session_state.total_game_duration if st.session_state.total_game_duration > 0 else 0


# ==================== FUNGSI GAME ====================

def pilih_wilayah():
    if st.session_state.total_questions >= st.session_state.max_questions:
        st.session_state.game_over = True
        return
    available = [w for w in wilayah_list if w not in st.session_state.questions_asked]
    if not available:
        st.session_state.questions_asked = []
        available = list(wilayah_list)
    target = random.choice(available)
    st.session_state.questions_asked.append(target)
    st.session_state.correct_answer = target
    num_opts = {"Mudah": 2, "Normal": 4, "Sulit": 6}.get(st.session_state.difficulty, 4)
    others = [w for w in wilayah_list if w != target]
    num_opts = min(num_opts, len(others))
    options = random.sample(others, num_opts) + [target]
    random.shuffle(options)
    st.session_state.options = options
    st.session_state.current_region = target
    st.session_state.answered = False
    st.session_state.feedback = ""
    st.session_state.game_started = True
    start_question_timer()

def reset_game():
    _new_start = time.time()
    st.session_state.score = 0
    st.session_state.total_questions = 0
    st.session_state.game_over = False
    st.session_state.questions_asked = []
    st.session_state.current_region = None
    st.session_state.feedback = ""
    st.session_state.answered = False
    st.session_state.game_started = False
    st.session_state.score_saved = False
    st.session_state.game_start_time = _new_start
    st.session_state.game_end_time = None
    st.session_state.total_game_duration = 0
    st.session_state.question_times = []
    st.session_state.average_answer_time = 0
    st.session_state.balloon_shown = False  # Reset flag balon
    pilih_wilayah()


# ==================== DATABASE INFO WILAYAH ====================

def get_wilayah_info(nama):
    db_kota = {
        "Kota Malang": {"geografis": "Kota Malang terletak di dataran tinggi dengan ketinggian 440-667 mdpl.", "demografi": "Penduduk: ±900.000 jiwa.", "budaya": "Budaya Arek yang dinamis.", "keunikan": "Arsitektur kolonial Belanda masih terjaga.", "oleh_oleh": "Keripik buah, bakso Malang, wingko babat."},
        "Kota Surabaya": {"geografis": "Kota pesisir utara Pulau Jawa, ibu kota Provinsi Jawa Timur.", "demografi": "Penduduk: ±3 juta jiwa.", "budaya": "Budaya Arek Surabaya yang blak-blakan.", "keunikan": "Kota Pahlawan dengan Tugu Pahlawan.", "oleh_oleh": "Kerupuk udang, terasi, wingko babat."},
        "Kota Batu": {"geografis": "Kota wisata pegunungan dengan ketinggian 700-1.700 mdpl.", "demografi": "Penduduk: ±210.000 jiwa.", "budaya": "Budaya Jawa Timuran dengan sentuhan modern.", "keunikan": "Jatim Park, Batu Night Spectacular.", "oleh_oleh": "Apel Batu, keripik apel, susu murni."},
    }
    db_kabupaten = {
        "Kabupaten Banyuwangi": {"geografis": "Kabupaten di ujung timur Pulau Jawa.", "demografi": "Penduduk: ±1,7 juta jiwa.", "budaya": "Kesenian Gandrung Banyuwangi.", "keunikan": "Kawah Ijen dengan fenomena api biru.", "oleh_oleh": "Pisang agung, kopi khas Banyuwangi."},
        "Kabupaten Malang": {"geografis": "Kabupaten terluas kedua di Jawa Timur.", "demografi": "Penduduk: ±2,7 juta jiwa.", "budaya": "Budaya Jawa Arekan dan Tengger.", "keunikan": "Pantai Balekambang, Coban Rondo.", "oleh_oleh": "Keripik buah apel, keripik tempe."},
        "Kabupaten Jember": {"geografis": "Kabupaten di kawasan Tapal Kuda.", "demografi": "Penduduk: ±2,5 juta jiwa.", "budaya": "Jember Fashion Carnival.", "keunikan": "Pantai Papuma, Watu Ulo.", "oleh_oleh": "Suwar-suwir, proll tape."},
    }
    if nama.startswith("Kabupaten "):
        if nama in db_kabupaten:
            return db_kabupaten[nama]
    elif nama.startswith("Kota "):
        if nama in db_kota:
            return db_kota[nama]
    tipe = "Kota" if nama.startswith("Kota ") else "Kabupaten"
    return {"geografis": f"{tipe} di Provinsi Jawa Timur.", "demografi": "Penduduk dengan keragaman budaya.", "budaya": "Memiliki kesenian tradisional.", "keunikan": "Destinasi wisata menarik.", "oleh_oleh": "Produk makanan khas."}


# ==================== CSS SIDEBAR & FOOTER ====================

def get_background_image_html(image_url):
    return f"""
    <style>
    [data-testid="stSidebar"] {{ background-image: url("{image_url}"); background-size: cover; background-position: center; }}
    [data-testid="stSidebar"]::before {{ content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); z-index: 0; }}
    [data-testid="stSidebar"] > div:first-child {{ position: relative; z-index: 1; background-color: transparent !important; }}
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] .stButton > button {{ color: white !important; text-shadow: 1px 1px 3px rgba(0,0,0,0.8); }}
    </style>
    """

def create_footer(footer_text, image_url, brightness=0.7):
    current_time = now_wib().strftime("%H:%M:%S")
    return f"""
    <div style="margin-top: 30px; padding: 20px 0; background-image: url('{image_url}'); background-size: cover; background-position: center; border-radius: 15px 15px 0 0; filter: brightness({brightness});">
        <div style="text-align: center; color: white; padding: 15px; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);">
            <div style="font-size: 16px; font-weight: bold; color: #ffd700;">🧩 Sepiro Jawa Timur, Sampeyan</div>
            <p>{footer_text}</p>
            <p>⏰ {current_time} WIB | © 2026 Lab. EIIS - Universitas Brawijaya</p>
        </div>
    </div>
    """


# ==================== PUZZLE DRAG & DROP ====================

def get_puzzle_html(geojson_data, start_time_ms):
    all_features = geojson_data.get("features", [])
    if not all_features:
        return "<p>❌ Data wilayah tidak ditemukan.</p>"
    geojson_str = json.dumps(geojson_data)
    SNAP_DIST = 60
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family: Arial, sans-serif; background: linear-gradient(135deg, #0f0c29, #302b63); min-height: 100vh; color: white; padding: 10px; }}
  #puzzle-header {{ text-align:center; padding:6px 0; }}
  #stats-bar {{ display:flex; justify-content:center; gap:16px; margin:6px 0; flex-wrap:wrap; }}
  .stat-pill {{ background:rgba(255,255,255,0.12); border-radius:30px; padding:5px 14px; font-size:0.80em; }}
  #main-layout {{ display:flex; gap:10px; flex-wrap:wrap; }}
  #canvas-wrapper {{ position:relative; flex:1 1 560px; max-width:700px; border:2px solid rgba(255,255,255,0.15); border-radius:14px; overflow:hidden; }}
  #puzzle-canvas {{ display:block; width:100%; cursor:grab; }}
  #pieces-panel {{ background:rgba(255,255,255,0.06); border-radius:14px; padding:10px; flex:0 0 190px; max-height:640px; overflow-y:auto; }}
  #pieces-container {{ display:flex; flex-wrap:wrap; gap:5px; justify-content:center; }}
  .piece-thumb {{ background:rgba(255,255,255,0.08); border:1.5px solid rgba(255,255,255,0.2); border-radius:7px; cursor:grab; width:90px; height:80px; position:relative; }}
  .piece-thumb.placed {{ opacity:0.28; cursor:default; pointer-events:none; }}
  .piece-label {{ position:absolute; bottom:1px; left:0; right:0; font-size:7px; text-align:center; }}
  .puzzle-btn {{ background:linear-gradient(135deg,#667eea,#764ba2); color:white; border:none; border-radius:18px; padding:7px 18px; cursor:pointer; margin:5px; }}
  #win-overlay {{ display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.88); z-index:999; justify-content:center; align-items:center; }}
  #win-overlay.show {{ display:flex; }}
  #win-box {{ background:linear-gradient(135deg,#1a1a2e,#16213e); border:3px solid #ffd700; border-radius:22px; padding:32px; text-align:center; }}
</style>
</head>
<body>
<div id="puzzle-header"><h2>🧩 PUZZLE PETA JAWA TIMUR</h2><div class="subtitle">{len(all_features)} Kepingan</div></div>
<div id="stats-bar"><div class="stat-pill">⏱️ Waktu <span id="timer-display">00:00</span></div><div class="stat-pill">🧩 Terpasang <span id="placed-count">0</span>/{len(all_features)}</div></div>
<div id="btn-row"><button class="puzzle-btn" onclick="shufflePieces()">🔀 Acak</button><button class="puzzle-btn" onclick="resetPuzzle()">🔄 Reset</button></div>
<div id="main-layout"><div id="canvas-wrapper"><canvas id="puzzle-canvas"></canvas></div><div id="pieces-panel"><div id="pieces-container"></div></div></div>
<div id="win-overlay"><div id="win-box"><h1>🎉 PUZZLE SELESAI! 🎉</h1><p>Waktu: <span id="win-time">00:00</span></p><p>Kesalahan: <span id="win-moves">0</span></p><button class="puzzle-btn" onclick="location.reload()">Main Lagi</button></div></div>
<script>
(function() {{
  const GEOJSON = {geojson_str};
  const SNAP_DIST = {SNAP_DIST};
  const START_TIME = Date.now();
  const canvas = document.getElementById('puzzle-canvas');
  const ctx = canvas.getContext('2d');
  const W = 680, H = 560;
  canvas.width = W; canvas.height = H;
  let minLon=180, maxLon=-180, minLat=90, maxLat=-90;
  function iterGeom(geom, cb) {{ function rec(c) {{ if (typeof c[0] === 'number') {{ cb(c[0], c[1]); return; }} c.forEach(rec); }} rec(geom.coordinates); }}
  GEOJSON.features.forEach(f => iterGeom(f.geometry, (lon,lat) => {{ if(lon<minLon) minLon=lon; if(lon>maxLon) maxLon=lon; if(lat<minLat) minLat=lat; if(lat>maxLat) maxLat=lat; }}));
  const PAD = 38;
  const SCALE = Math.min((W-PAD*2)/(maxLon-minLon), (H-PAD*2)/(maxLat-minLat));
  function project(lon, lat) {{ return [PAD + (lon-minLon)*SCALE, H-PAD - (lat-minLat)*SCALE]; }}
  function buildPath(geometry) {{
    const p = new Path2D();
    function addRing(ring) {{ ring.forEach((c,i) => {{ const [x,y]=project(c[0],c[1]); if(i===0) p.moveTo(x,y); else p.lineTo(x,y); }}); p.closePath(); }}
    if(geometry.type === 'Polygon') geometry.coordinates.forEach(addRing);
    else if(geometry.type === 'MultiPolygon') geometry.coordinates.forEach(poly => poly.forEach(addRing));
    return p;
  }}
  function geomCentroid(geom) {{ let sx=0,sy=0,n=0; iterGeom(geom, (lon,lat) => {{ const [x,y]=project(lon,lat); sx+=x; sy+=y; n++; }}); return [sx/n, sy/n]; }}
  function geomBBox(geom) {{ let x1=W,x2=0,y1=H,y2=0; iterGeom(geom, (lon,lat) => {{ const [x,y]=project(lon,lat); if(x<x1) x1=x; if(x>x2) x2=x; if(y<y1) y1=y; if(y>y2) y2=y; }}); return {{ x1,x2,y1,y2, w:x2-x1, h:y2-y1 }}; }}
  const pieces = GEOJSON.features.map((feat,i) => {{
    const name = feat.properties.name;
    return {{ id:i, name:name, geometry:feat.geometry, path:buildPath(feat.geometry), centroid:geomCentroid(feat.geometry), bbox:geomBBox(feat.geometry), dx:0, dy:0, placed:false, inPanel:true, hue:(i*31+120)%360 }};
  }});
  const totalPieces = pieces.length;
  const THUMB_W = 90, THUMB_H = 80;
  const piecesContainer = document.getElementById('pieces-container');
  function drawThumb(piece, tctx) {{
    tctx.clearRect(0,0,THUMB_W,THUMB_H);
    const bb = piece.bbox;
    if(bb.w<0.5 || bb.h<0.5) return;
    const ts = Math.min((THUMB_W-10)/bb.w, (THUMB_H-10)/bb.h);
    const offX = 5 + (THUMB_W-10 - bb.w*ts)/2 - bb.x1*ts;
    const offY = 5 + (THUMB_H-10 - bb.h*ts)/2 - bb.y1*ts;
    tctx.save();
    tctx.setTransform(ts,0,0,ts,offX,offY);
    tctx.fillStyle = `hsla(${{piece.hue}},68%,56%,0.92)`;
    tctx.fill(piece.path);
    tctx.strokeStyle = 'rgba(255,255,255,0.8)';
    tctx.stroke(piece.path);
    tctx.restore();
  }}
  function buildThumbnails() {{
    piecesContainer.innerHTML = '';
    pieces.forEach(p => {{
      const div = document.createElement('div');
      div.className = 'piece-thumb' + (p.placed ? ' placed' : '');
      div.id = 'thumb-'+p.id;
      const tc = document.createElement('canvas');
      tc.width = THUMB_W; tc.height = THUMB_H;
      drawThumb(p, tc.getContext('2d'));
      div.appendChild(tc);
      const lbl = document.createElement('div');
      lbl.className = 'piece-label';
      lbl.textContent = p.name.replace('Kabupaten ','').replace('Kota ','');
      div.appendChild(lbl);
      div.addEventListener('mousedown', e => startDragPanel(e, p));
      piecesContainer.appendChild(div);
    }});
  }}
  buildThumbnails();
  let dragging = null, mouseX=0, mouseY=0, mistakes=0;
  function canvasPos(e) {{ const rect = canvas.getBoundingClientRect(); const cx = e.clientX; const cy = e.clientY; return [(cx-rect.left)*(W/rect.width), (cy-rect.top)*(H/rect.height)]; }}
  function startDragPanel(e, piece) {{ if(piece.placed) return; e.preventDefault(); dragging = piece; piece.inPanel = false; const [mx,my] = canvasPos(e); piece.dx = mx - piece.centroid[0]; piece.dy = my - piece.centroid[1]; render(); }}
  canvas.addEventListener('mousedown', e => {{
    const [mx,my] = canvasPos(e);
    for(let i=pieces.length-1; i>=0; i--) {{
      const p = pieces[i];
      if(p.placed || p.inPanel) continue;
      const bb = p.bbox;
      if(mx >= bb.x1+p.dx-4 && mx <= bb.x2+p.dx+4 && my >= bb.y1+p.dy-4 && my <= bb.y2+p.dy+4) {{
        dragging = p; mouseX=mx; mouseY=my; render(); break;
      }}
    }}
  }});
  document.addEventListener('mousemove', e => {{
    if(!dragging) return;
    const [mx,my] = canvasPos(e);
    mouseX=mx; mouseY=my;
    dragging.dx = mx - dragging.centroid[0];
    dragging.dy = my - dragging.centroid[1];
    render();
  }});
  document.addEventListener('mouseup', () => {{
    if(dragging) trySnap(dragging, mouseX, mouseY);
    dragging = null;
    render();
  }});
  function trySnap(piece, dropX, dropY) {{
    const tx = piece.centroid[0], ty = piece.centroid[1];
    const dist = Math.hypot(dropX-tx, dropY-ty);
    const bb = piece.bbox;
    const thr = Math.max(SNAP_DIST, Math.min(Math.sqrt(bb.w*bb.h)*0.45, 72));
    if(dist <= thr) {{
      piece.dx = 0; piece.dy = 0; piece.placed = true; piece.inPanel = false;
      const el = document.getElementById('thumb-'+piece.id);
      if(el) el.classList.add('placed');
      updateProgress();
      checkWin();
    }} else {{
      mistakes++;
      updateAccuracy();
    }}
  }}
  function updateProgress() {{
    const pl = pieces.filter(p=>p.placed).length;
    document.getElementById('placed-count').textContent = pl;
    if(pl===totalPieces) document.getElementById('progress-text').textContent = '🎉 Selesai!';
  }}
  function updateAccuracy() {{
    const pl = pieces.filter(p=>p.placed).length;
    const tot = pl + mistakes;
    document.getElementById('accuracy-display').textContent = tot>0 ? Math.round((pl/tot)*100)+'%' : '100%';
  }}
  function checkWin() {{
    if(pieces.filter(p=>p.placed).length >= totalPieces) {{
      const e = Math.floor((Date.now()-START_TIME)/1000);
      const m = Math.floor(e/60), s = e%60;
      document.getElementById('win-time').textContent = `${m.toString().padStart(2,'0')}:${s.toString().padStart(2,'0')}`;
      document.getElementById('win-moves').textContent = mistakes;
      setTimeout(() => document.getElementById('win-overlay').classList.add('show'), 600);
    }}
  }}
  setInterval(() => {{
    const e = Math.floor((Date.now()-START_TIME)/1000);
    document.getElementById('timer-display').textContent = `${Math.floor(e/60).toString().padStart(2,'0')}:${(e%60).toString().padStart(2,'0')}`;
  }}, 1000);
  function drawPiece(piece, dx, dy, isDrag) {{
    ctx.save();
    ctx.translate(dx, dy);
    ctx.fillStyle = `hsla(${{piece.hue}},66%,54%,0.82)`;
    ctx.fill(piece.path);
    ctx.strokeStyle = isDrag ? '#ffd700' : 'rgba(255,255,255,0.65)';
    ctx.lineWidth = isDrag ? 2.5 : 1.2;
    ctx.stroke(piece.path);
    ctx.restore();
  }}
  function render() {{
    ctx.clearRect(0,0,W,H);
    pieces.forEach(p => {{ if(!p.placed) {{ ctx.save(); ctx.strokeStyle = 'rgba(255,215,0,0.18)'; ctx.stroke(p.path); ctx.fillStyle = 'rgba(255,255,255,0.03)'; ctx.fill(p.path); ctx.restore(); }} }});
    pieces.forEach(p => {{ if(p.placed) drawPiece(p,0,0,false); }});
    pieces.forEach(p => {{ if(!p.placed && !p.inPanel && p!==dragging) drawPiece(p,p.dx,p.dy,false); }});
    if(dragging && !dragging.placed) drawPiece(dragging, dragging.dx, dragging.dy, true);
  }}
  render();
  window.shufflePieces = function() {{
    const margin = 30;
    pieces.forEach(p => {{ if(p.placed) return; p.inPanel = false; const bb = p.bbox; p.dx = (Math.random()*(W-margin*2-bb.w)+margin) - bb.x1; p.dy = (Math.random()*(H-margin*2-bb.h)+margin) - bb.y1; }});
    render();
  }};
  window.resetPuzzle = function() {{ mistakes=0; pieces.forEach(p => {{ p.placed=false; p.inPanel=true; p.dx=0; p.dy=0; }}); buildThumbnails(); updateProgress(); render(); }};
  shufflePieces();
}})();
</script>
</body>
</html>"""
    return html


# ==================== CSS RENDER ====================

st.markdown(get_background_image_html(SIDEBAR_BACKGROUND_URL), unsafe_allow_html=True)


# ==================== HALAMAN LOGIN NAMA ====================

if not st.session_state.name_submitted:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://img.freepik.com/vektor-premium/peta-yang-digambar-tangan-dari-provinsi-jawa-timur-indonesia-desain-kartun-garis-sederhana-modern_242622-498.jpg", width=150)
        time_info = get_current_time_info()
        st.markdown(f"<div style='text-align:center;color:#666;'>{time_info['hari']}, {time_info['tanggal']} | {time_info['jam']}</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;'><h1>🧩 Sepiro Jawa Timur, Sampeyan?</h1></div>", unsafe_allow_html=True)
        with st.form("name_form"):
            st.markdown("### 👤 Silahkan Masukkan Nama")
            name = st.text_input("Nama", placeholder="Contoh: Adi", max_chars=30)
            if st.form_submit_button("🚀 Mulai Bermain", use_container_width=True, type="primary"):
                if name.strip():
                    st.session_state.user_name = name.strip()
                    st.session_state.name_submitted = True
                    st.rerun()
                else:
                    st.error("❌ Nama tidak boleh kosong!")
    st.stop()


# ==================== SIDEBAR ====================

with st.sidebar:
    st.image("https://img.freepik.com/vektor-premium/peta-yang-digambar-tangan-dari-provinsi-jawa-timur-indonesia-desain-kartun-garis-sederhana-modern_242622-498.jpg", width=100)
    st.title("🧩 Ensiklopedia Jatim")
    time_info = get_current_time_info()
    st.markdown(f"<div style='background:linear-gradient(135deg,#667eea,#764ba2);padding:8px;border-radius:10px;text-align:center;'><p style='color:white;'>{time_info['hari']}, {time_info['tanggal']} | {time_info['jam']}</p></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background:linear-gradient(135deg,#667eea,#764ba2);padding:10px;border-radius:10px;text-align:center;'><p style='color:white;'>👋 Halo <strong>{st.session_state.user_name}</strong>!</p></div>", unsafe_allow_html=True)
    st.components.v1.html(get_backsound_html(st.session_state.music_volume), height=58, scrolling=False)
    st.markdown("---")
    
    menu_options = ["📚 Info Wilayah", "🎮 Quiz", "🧩 Puzzle", "🌋 Bromo 3D", "🏛️ Balaikota 3D", "🏆 Papan Skor", "⏱️ Statistik Waktu", "⚙️ Pengaturan", "ℹ️ Tentang"]
    _nav_index = 0
    if st.session_state.get("pending_navigation"):
        _target = st.session_state.pending_navigation
        st.session_state.pending_navigation = None
        if _target in menu_options:
            _nav_index = menu_options.index(_target)
    elif st.session_state.get("main_navigation") in menu_options:
        _nav_index = menu_options.index(st.session_state["main_navigation"])
    selected_menu = st.radio("Menu", menu_options, index=_nav_index, label_visibility="collapsed", key="main_navigation")
    PAGE = selected_menu.split(" ", 1)[1] if " " in selected_menu else selected_menu
    st.markdown("---")
    if st.button("🔄 Ganti Nama", use_container_width=True):
        st.session_state.name_submitted = False
        st.rerun()
    st.markdown("---")
    
    if PAGE == "Quiz":
        st.header("🎮 Kontrol Quiz")
        if not st.session_state.game_started or st.session_state.game_over:
            if st.button("🎲 Mulai Quiz Baru", use_container_width=True, type="primary"):
                reset_game()
                st.rerun()
        else:
            if st.button("🔄 Reset Quiz", use_container_width=True):
                reset_game()
                st.rerun()
        st.markdown("### 📊 Statistik")
        c1, c2 = st.columns(2)
        with c1: st.metric("Skor", st.session_state.score)
        with c2: st.metric("Soal", f"{st.session_state.total_questions}/{st.session_state.max_questions}")
        if st.session_state.game_started and not st.session_state.game_over:
            if st.session_state.game_start_time:
                st.metric("⏱️ Waktu", format_duration(time.time() - st.session_state.game_start_time))
        with st.expander("⚙️ Kesulitan"):
            diff = st.selectbox("Tingkat Kesulitan", ["Mudah", "Normal", "Sulit"], index=["Mudah", "Normal", "Sulit"].index(st.session_state.difficulty))
            if diff != st.session_state.difficulty:
                st.session_state.difficulty = diff
                st.rerun()
    elif PAGE == "Puzzle":
        st.header("🧩 Puzzle Kontrol")
        total_kab = len(jatim_geojson.get("features", []))
        st.info(f"🗺️ Susun **{total_kab} kepingan** kabupaten/kota menjadi peta Jawa Timur yang utuh!")
        if st.button("▶️ Mulai Puzzle", use_container_width=True, type="primary"):
            st.session_state.puzzle_started = True
            st.session_state.puzzle_start_time = time.time()
            st.session_state.puzzle_score_saved = False
            st.rerun()
        if st.session_state.puzzle_started:
            if st.button("⛔ Keluar Puzzle", use_container_width=True):
                st.session_state.puzzle_started = False
                st.rerun()


# ==================== KONTEN UTAMA ====================

# --- HALAMAN QUIZ ---
if PAGE == "Quiz":
    st.title("🧩 Tebak Bentuk Kota & Kabupaten di Jawa Timur")
    
    # Peta Quiz
    m = folium.Map(location=[-7.5, 112.3], zoom_start=8, tiles=None, control_scale=True)
    folium.TileLayer(tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", attr="Esri", name="Satellite", overlay=False, control=False).add_to(m)
    def style_function(feature):
        name = feature["properties"]["name"]
        if st.session_state.game_started and not st.session_state.game_over and name == st.session_state.current_region:
            return {"fillColor": "#ff0000", "color": "#ff0000", "weight": 3, "fillOpacity": 0.7}
        return {"fillColor": "#3388ff" if st.session_state.game_started else "#cccccc", "color": "#ffffff", "weight": 1.5, "fillOpacity": 0.3 if st.session_state.game_started else 0.1}
    folium.GeoJson(jatim_geojson, name="Wilayah Jatim", style_function=style_function).add_to(m)
    st_folium(m, width=None, height=500, use_container_width=True, key="game_map")
    
    if not st.session_state.game_started and not st.session_state.game_over:
        if st.button("🎮 Mulai Quiz", use_container_width=True, type="primary"):
            reset_game()
            st.rerun()
    
    if st.session_state.game_started and not st.session_state.game_over:
        st.markdown(f"**Kesulitan:** {st.session_state.difficulty} | **Soal:** {st.session_state.total_questions + 1}/{st.session_state.max_questions}")
        if st.session_state.game_start_time:
            st.info(f"⏱️ **Total:** {format_duration(time.time() - st.session_state.game_start_time)}")
        
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 📝 Pertanyaan")
            st.markdown("**Wilayah manakah yang disorot MERAH pada peta?**")
            if st.session_state.current_region:
                st.markdown(f"<div style='background:#fef9e6;border-left:5px solid #ff9800;padding:12px;border-radius:10px;'><span style='font-weight:bold;'>💡 Petunjuk:</span> {get_wilayah_clue(st.session_state.current_region)}</div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"### Soal {st.session_state.total_questions + 1}/{st.session_state.max_questions}")
        if st.session_state.question_start_time:
            qtime = time.time() - st.session_state.question_start_time
            st.progress(min(qtime/60, 1.0), text=f"⏱️ Waktu: {qtime:.1f} dtk")
        
        st.markdown("### Pilih Jawaban:")
        options = st.session_state.options
        half = len(options)//2 + len(options)%2
        ca1, ca2 = st.columns(2)
        answer_selected = None
        with ca1:
            for i, opt in enumerate(options[:half]):
                if st.button(opt, key=f"opt_{i}", use_container_width=True, disabled=st.session_state.answered):
                    answer_selected = opt
        with ca2:
            for i, opt in enumerate(options[half:]):
                if st.button(opt, key=f"opt_{i+half}", use_container_width=True, disabled=st.session_state.answered):
                    answer_selected = opt
        
        if answer_selected and not st.session_state.answered:
            is_correct = (answer_selected == st.session_state.correct_answer)
            q_time = end_question_timer(is_correct)
            st.session_state.total_questions += 1
            if is_correct:
                st.session_state.score += 1
                st.session_state.feedback = f"✅ **Benar! (Waktu: {q_time:.1f} dtk)**"
            else:
                st.session_state.feedback = f"❌ **Jawaban benar: {st.session_state.correct_answer} (Waktu: {q_time:.1f} dtk)**"
            st.session_state.answered = True
            if st.session_state.total_questions >= st.session_state.max_questions:
                st.session_state.game_over = True
                st.session_state.game_end_time = time.time()
                st.session_state.total_game_duration = st.session_state.game_end_time - st.session_state.game_start_time if st.session_state.game_start_time else 0
            st.rerun()
        
        if st.session_state.feedback:
            st.markdown("---")
            st.markdown(f"### {st.session_state.feedback}")
            if st.session_state.answered and st.session_state.total_questions < st.session_state.max_questions:
                if st.button("➡️ Soal Berikutnya", use_container_width=True, type="primary"):
                    pilih_wilayah()
                    st.rerun()
    
    # GAME OVER - HANYA TAMPIL DI HALAMAN QUIZ
    if st.session_state.game_over:
        end_game_timer()
        is_perfect = (st.session_state.score == st.session_state.max_questions)
        
        # Efek balon hanya sekali, dan berhenti setelah simpan skor
        if is_perfect and not st.session_state.balloon_shown:
            st.balloons()
            st.markdown(get_perfect_score_markdown_effect(), unsafe_allow_html=True)
            st.components.v1.html(get_balloon_effect_html(), height=340, scrolling=False)
            st.session_state.balloon_shown = True
        
        st.markdown("## 🎮 Quiz Selesai!")
        st.markdown(f"### Skor Akhir: **{st.session_state.score}/{st.session_state.max_questions}**")
        if st.session_state.total_game_duration > 0:
            st.info(f"⏱️ **Total Waktu:** {format_duration(st.session_state.total_game_duration)}")
        if st.session_state.average_answer_time > 0:
            st.info(f"⚡ **Rata-rata Jawab:** {st.session_state.average_answer_time:.1f} dtk")
        
        if is_perfect:
            st.markdown("### 🏆 Selamat! Nilai Sempurna!")
        
        if not st.session_state.score_saved and st.session_state.score > 0:
            st.markdown("---")
            st.markdown("### 💾 Simpan Skor")
            with st.form("save_score_form"):
                st.markdown(f"Nama: **{st.session_state.user_name}**")
                st.markdown(f"Skor: **{st.session_state.score}/{st.session_state.max_questions}** (Level: {st.session_state.difficulty})")
                if st.session_state.total_game_duration > 0:
                    st.markdown(f"Waktu: **{format_duration(st.session_state.total_game_duration)}**")
                if st.form_submit_button("💾 Simpan Skor", use_container_width=True, type="primary"):
                    if add_score(st.session_state.user_name, st.session_state.score, st.session_state.difficulty, st.session_state.max_questions, st.session_state.game_start_time, st.session_state.game_end_time):
                        st.session_state.score_saved = True
                        st.success("✅ Skor disimpan!")
                        st.rerun()
                    else:
                        st.error("❌ Gagal menyimpan skor.")
        elif st.session_state.score_saved:
            st.success("✅ Skor sudah disimpan!")
        
        if st.button("🔄 Main Lagi", use_container_width=True, type="primary"):
            reset_game()
            st.rerun()
    
    # Progress bar
    if st.session_state.game_started and not st.session_state.game_over:
        st.markdown("---")
        progress = st.session_state.total_questions / st.session_state.max_questions
        st.progress(progress, text=f"Progress: {st.session_state.total_questions}/{st.session_state.max_questions}")
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"### ⭐ Skor: {st.session_state.score}")
        with c2: st.markdown(f"### 🎯 Target: {st.session_state.max_questions}")
        with c3:
            if st.session_state.game_start_time:
                st.markdown(f"### ⏱️ {format_duration(time.time() - st.session_state.game_start_time)}")


# --- HALAMAN PUZZLE ---
elif PAGE == "Puzzle":
    st.title("🧩 Puzzle Peta Jawa Timur")
    total_kab = len(jatim_geojson.get("features", []))
    st.markdown(f"<div style='background:linear-gradient(135deg,#FF9800,#f57c00);border-radius:14px;padding:16px;margin-bottom:16px;color:white;text-align:center;'><div style='font-size:1.5em;font-weight:900;'>⚡ Level Normal — {total_kab} Kepingan</div></div>", unsafe_allow_html=True)
    
    if not st.session_state.puzzle_started and not st.session_state.puzzle_completed and not st.session_state.puzzle_score_saved:
        col_prev, col_info = st.columns([3, 1])
        with col_prev:
            m_prev = folium.Map(location=[-7.5, 112.3], zoom_start=7, tiles=None)
            folium.TileLayer(tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", attr="Esri").add_to(m_prev)
            folium.GeoJson(jatim_geojson, style_function=lambda f: {"fillColor": "#FF9800", "color": "#ffffff", "weight": 1.5, "fillOpacity": 0.55}, tooltip=folium.GeoJsonTooltip(fields=["name"])).add_to(m_prev)
            st_folium(m_prev, width=None, height=380, use_container_width=True, key="puzzle_preview")
        with col_info:
            if st.button("▶️ MULAI PUZZLE!", use_container_width=True, type="primary"):
                st.session_state.puzzle_started = True
                st.session_state.puzzle_start_time = time.time()
                st.session_state.puzzle_score_saved = False
                st.rerun()
        st.info("💡 Seret kepingan dari panel kanan ke posisi yang tepat di peta!")
    
    elif st.session_state.puzzle_started:
        if st.button("⛔ Keluar Puzzle", use_container_width=True):
            st.session_state.puzzle_started = False
            st.rerun()
        puzzle_html = get_puzzle_html(jatim_geojson, int(st.session_state.puzzle_start_time * 1000) if st.session_state.puzzle_start_time else 0)
        st.components.v1.html(puzzle_html, height=750, scrolling=True)
        
        st.markdown("---")
        st.markdown("#### ⏱️ Masukkan Waktu & Kesalahan dari Layar Puzzle")
        col_wm, col_ws = st.columns(2)
        with col_wm: input_menit = st.number_input("Menit", min_value=0, max_value=99, step=1, key="_puzzle_menit")
        with col_ws: input_detik = st.number_input("Detik", min_value=0, max_value=59, step=1, key="_puzzle_detik")
        input_errors = st.number_input("❌ Jumlah Kesalahan", min_value=0, max_value=999, step=1, key="_puzzle_errors")
        
        if st.button("✅ Selesai & Lanjut Simpan Skor", use_container_width=True, type="primary"):
            waktu_detik_js = int(input_menit) * 60 + int(input_detik)
            st.session_state.puzzle_js_waktu = waktu_detik_js if waktu_detik_js > 0 else 1
            st.session_state.puzzle_js_errors = int(input_errors)
            st.session_state.puzzle_completed = True
            st.session_state.puzzle_started = False
            st.rerun()
    
    if st.session_state.puzzle_completed or st.session_state.puzzle_score_saved:
        _js_wkt = st.session_state.get("puzzle_js_waktu")
        _js_err = st.session_state.get("puzzle_js_errors", 0)
        
        if st.session_state.puzzle_score_saved:
            wt = st.session_state.puzzle_result_time_sec or 0
            err = st.session_state.puzzle_result_errors or 0
            wm, ws = divmod(int(wt), 60)
            st.success(f"✅ Skor tersimpan! ⏱️ {wm:02d}:{ws:02d} | ❌ {err} kesalahan")
            cola, colb = st.columns(2)
            with cola:
                if st.button("🔄 Main Puzzle Lagi", use_container_width=True, type="primary"):
                    for key in ["puzzle_started", "puzzle_start_time", "puzzle_completed", "puzzle_score_saved", "puzzle_result_time_sec", "puzzle_result_errors", "puzzle_js_waktu", "puzzle_js_errors"]:
                        st.session_state[key] = False if key in ["puzzle_started", "puzzle_completed", "puzzle_score_saved"] else None
                    st.rerun()
            with colb:
                if st.button("🚪 Keluar", use_container_width=True):
                    for key in ["puzzle_started", "puzzle_start_time", "puzzle_completed", "puzzle_score_saved", "puzzle_result_time_sec", "puzzle_result_errors", "puzzle_js_waktu", "puzzle_js_errors"]:
                        st.session_state[key] = False if key in ["puzzle_started", "puzzle_completed", "puzzle_score_saved"] else None
                    st.session_state.pending_navigation = "📚 Info Wilayah"
                    st.rerun()
        elif _js_wkt:
            wm, ws = divmod(int(_js_wkt), 60)
            st.markdown(f"### 🏆 Puzzle Selesai! ⏱️ {wm:02d}:{ws:02d} | ❌ {_js_err} kesalahan")
            c_save, c_skip, c_exit = st.columns(3)
            with c_save:
                if st.button("💾 Simpan Skor", use_container_width=True, type="primary"):
                    if add_puzzle_score(st.session_state.user_name, _js_wkt, _js_err):
                        st.session_state.puzzle_score_saved = True
                        st.session_state.puzzle_completed = False
                        st.session_state.puzzle_result_time_sec = _js_wkt
                        st.session_state.puzzle_result_errors = _js_err
                        st.rerun()
            with c_skip:
                if st.button("🔄 Main Lagi", use_container_width=True):
                    st.session_state.puzzle_started = False
                    st.session_state.puzzle_completed = False
                    st.session_state.puzzle_js_waktu = None
                    st.rerun()
            with c_exit:
                if st.button("🚪 Keluar", use_container_width=True):
                    for key in ["puzzle_started", "puzzle_completed", "puzzle_js_waktu", "puzzle_js_errors"]:
                        st.session_state[key] = False if key in ["puzzle_started", "puzzle_completed"] else None
                    st.session_state.pending_navigation = "📚 Info Wilayah"
                    st.rerun()


# --- HALAMAN INFO WILAYAH ---
elif PAGE == "Info Wilayah":
    st.title("📚 Info Wilayah Jawa Timur")
    st.markdown("**Klik wilayah pada peta** untuk melihat informasi lengkap!")
    col_map, col_info = st.columns([2, 1])
    with col_map:
        m = folium.Map(location=[-7.5, 112.3], zoom_start=8, tiles=None, control_scale=True)
        folium.TileLayer(tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", attr="Esri").add_to(m)
        folium.GeoJson(jatim_geojson, style_function=lambda f: {"fillColor": "#33cc33", "color": "#ffffff", "weight": 1.5, "fillOpacity": 0.5}, tooltip=folium.GeoJsonTooltip(fields=["name"]), highlight_function=lambda x: {"fillColor": "#ffaa00", "weight": 3}).add_to(m)
        map_data = st_folium(m, width=None, height=500, use_container_width=True, key="info_map")
        if map_data and map_data.get("last_active_drawing") and "properties" in map_data["last_active_drawing"]:
            clicked_name = map_data["last_active_drawing"]["properties"]["name"]
            if clicked_name != st.session_state.selected_wilayah_info:
                st.session_state.selected_wilayah_info = clicked_name
                st.rerun()
    with col_info:
        st.markdown("## 📋 Info Wilayah")
        if st.session_state.selected_wilayah_info:
            wil = st.session_state.selected_wilayah_info
            logo_url = get_logo_url(wil)
            if logo_url:
                col_logo, col_title = st.columns([1, 3])
                with col_logo: st.image(logo_url, width=80)
                with col_title: st.markdown(f"<h3 style='color:#ffd700;'>📍 {wil}</h3>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h3 style='color:#ffd700;text-align:center;'>📍 {wil}</h3>", unsafe_allow_html=True)
            info = get_wilayah_info(wil)
            with st.expander("🗺️ Geografis", expanded=True): st.write(info["geografis"])
            with st.expander("👥 Demografi", expanded=True): st.write(info["demografi"])
            with st.expander("🎭 Budaya", expanded=True): st.write(info["budaya"])
            with st.expander("✨ Keunikan", expanded=True): st.write(info["keunikan"])
            with st.expander("🛍️ Oleh-oleh", expanded=True): st.write(info["oleh_oleh"])
            if st.button("🔄 Klik wilayah lain", use_container_width=True):
                st.session_state.selected_wilayah_info = None
                st.rerun()
        else:
            st.info("👆 Klik wilayah pada peta untuk melihat informasi detail!")


# --- HALAMAN BROMO 3D ---
elif PAGE == "Bromo 3D":
    st.title("🌋 Gunung Bromo - Visualisasi 3D Interaktif")
    st.components.v1.html("""
    <div style="width:100%;height:600px;border-radius:10px;overflow:hidden;">
        <iframe frameborder="0" allowfullscreen src="https://sketchfab.com/models/72f1c983ba4040eab89d75eb2b0d3e32/embed" style="width:100%;height:100%;"></iframe>
    </div>
    """, height=620)
    col1, col2 = st.columns(2)
    with col1: st.metric("Ketinggian", "2.329 m")
    with col2: st.metric("Status", "Aktif")
    with st.expander("📖 Info"): st.markdown("Gunung Bromo terkenal dengan lautan pasir dan kawahnya yang ikonik.")


# --- HALAMAN BALAIKOTA 3D ---
elif PAGE == "Balaikota 3D":
    st.title("🏛️ Balaikota Malang - Visualisasi 3D")
    st.components.v1.html("""
    <div style="width:100%;height:600px;border-radius:10px;overflow:hidden;">
        <iframe src="https://sandcastle.cesium.com/standalone.html#c=jZJvb9owEMa/ipUXVZA2p4G2KhqtxmCjQRBEyWiDIk3GMWBi7NQ2lGTqd5/zh62dtmmvLPt+99zdc3YcMJCIa9Ajiu53wxlAGBOlgBYgE3sJqOAAKUW0injFQE9wGJMV2jPdLeFAJISDGxBZJBtulgNMJ3Tofc0916ee8vj9Je55V16SPs57wzY00FM8SAzkNcMgOZ8Ec7qYnTfD5mIzCqbu4iHUk76f+JnL/P70Ypzj3M9jNg4wHfWG6cKIjYOw6ffHRtzfLlufGM68qwdTHLe8guFhNowLNnyc0sn2s+vn3Qt/uz5OAtaGyZfD/bzVPzbDRM7zULa/Pb5funfr6+l8sF0trikdNf0gu7sLRWR9iDgWXGlwoOSZSDMmJ8+1XXBevtmRhct7T3CNKCcyshomL+JaZuB7xAGoJDRlxFhpNNAzoifTYXW0+kEVhispdsbkbmG7F9vNS/eyfVEIgroJqDDhBKaS7qimB6IgimO7Vq/AqkCN50LsAvEaKBDHAd00ZRnQGwLqhQKlM0YAXQGTTY5UFXs/tU+OWiJluq+FYPkxYPVcVjV5dnGC02hG1vgR2xXTAGdn/whD89n+Azl9vlnRaqOAG5XJ4Gdj1RRvVvXa5DLzr4rlJC8RfwEYabwBNpFSyMavRQpGIBPr+t3gBrbeWZ2y6m1BfaS7VEgN9pLZEDqa7FKGNFHOco8T0x9WqsjrOKeUTkwPgMY3f/hJADPjs4ms9ozNaE4i67bjGP5NGhMopnw9ORDJUGaQoo3Oxr0dVQEIYccx16Lo77laCLZE8pXuDw" style="width:100%;height:100%;border:none;"></iframe>
    </div>
    """, height=620)
    col1, col2 = st.columns(2)
    with col1: st.metric("Kota", "Malang")
    with col2: st.metric("Gaya", "Kolonial")


# --- HALAMAN PAPAN SKOR ---
elif PAGE == "Papan Skor":
    st.title("🏆 Papan Skor Pemain")
    tab_options = ["🎮 Quiz Tebak Wilayah", "🧩 Puzzle Peta Jawa Timur"]
    selected_tab = st.radio("Pilih Tipe Skor", tab_options, horizontal=True, label_visibility="collapsed")
    
    if selected_tab == "🎮 Quiz Tebak Wilayah":
        st.markdown("### 🎮 Papan Skor Quiz")
        col_f1, col_f2 = st.columns(2)
        with col_f1: lf = st.selectbox("Filter level:", ["Semua Level", "Mudah", "Normal", "Sulit"], key="sb_level")
        with col_f2: tf = st.selectbox("Filter waktu:", ["Semua Waktu", "Hari Ini", "7 Hari Terakhir", "30 Hari Terakhir"], key="sb_time")
        scoreboard = get_filtered_scoreboard(lf, tf)
        if scoreboard:
            rows = []
            for i, p in enumerate(scoreboard[:10], 1):
                icon = {1: "👑", 2: "🥈", 3: "🥉"}.get(i, f"{i}.")
                nm = p.get("nama", "Unknown")
                if nm == st.session_state.user_name: nm = f"⭐ {nm} (Kamu)"
                rows.append({"Peringkat": icon, "Nama": nm, "Skor": f"{p.get('skor',0)}/{p.get('total_soal',0)}", "Persentase": f"{p.get('persentase',0)}%", "Level": p.get("level", "-")})
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        else:
            st.info("Belum ada skor Quiz. Mainkan Quiz dulu!")
        
        st.markdown("---")
        st.markdown(f"### 📝 Skor Quiz Kakak: **{st.session_state.user_name}**")
        st.markdown(f"**Skor:** {st.session_state.score}/{st.session_state.max_questions} (Level: {st.session_state.difficulty})")
        if st.session_state.score > 0 and not st.session_state.score_saved:
            if st.button("💾 Simpan Skor Quiz", use_container_width=True, type="primary"):
                if not st.session_state.game_end_time:
                    st.session_state.game_end_time = time.time()
                end_game_timer()
                if add_score(st.session_state.user_name, st.session_state.score, st.session_state.difficulty, st.session_state.max_questions, st.session_state.game_start_time, st.session_state.game_end_time):
                    st.session_state.score_saved = True
                    st.success("✅ Skor tersimpan!")
                    st.rerun()
        elif st.session_state.score_saved:
            st.success("✅ Skor sudah disimpan!")
    
    else:
        st.markdown("### 🧩 Papan Skor Puzzle")
        puzzle_sb = load_puzzle_scoreboard()
        if puzzle_sb:
            rows_p = []
            for i, p in enumerate(puzzle_sb, 1):
                icon = {1: "👑", 2: "🥈", 3: "🥉"}.get(i, f"{i}.")
                nm = p.get("nama", "Unknown")
                if nm == st.session_state.user_name: nm = f"⭐ {nm} (Kamu)"
                rows_p.append({"Peringkat": icon, "Nama": nm, "⏱️ Waktu": p.get("waktu_format", "--:--")})
            st.dataframe(pd.DataFrame(rows_p), hide_index=True, use_container_width=True)
        else:
            st.info("Belum ada skor Puzzle. Mainkan Puzzle dulu!")


# --- HALAMAN STATISTIK WAKTU ---
elif PAGE == "Statistik Waktu":
    st.title("⏱️ Statistik Waktu")
    st.metric("Durasi Sesi", format_duration(get_session_duration()))
    if st.session_state.question_times:
        st.metric("Total Soal", len(st.session_state.question_times))
        st.metric("Rata-rata Jawab", f"{st.session_state.average_answer_time:.1f} dtk")
        df_t = pd.DataFrame(st.session_state.question_times)
        st.dataframe(df_t[["question_number", "duration"]].rename(columns={"question_number": "Soal", "duration": "Waktu (dtk)"}), hide_index=True, use_container_width=True)


# --- HALAMAN PENGATURAN ---
elif PAGE == "Pengaturan":
    st.title("⚙️ Pengaturan")
    new_max = st.slider("Jumlah Soal", 5, 20, st.session_state.max_questions, 5)
    if new_max != st.session_state.max_questions:
        st.session_state.max_questions = new_max
    new_br = st.slider("Brightness Footer", 0.3, 1.0, st.session_state.footer_brightness, 0.05)
    if new_br != st.session_state.footer_brightness:
        st.session_state.footer_brightness = new_br
        st.rerun()
    new_vol = st.slider("Volume Musik (%)", 0, 100, st.session_state.music_volume, 5)
    if new_vol != st.session_state.music_volume:
        st.session_state.music_volume = new_vol
        st.rerun()


# --- HALAMAN TENTANG ---
elif PAGE == "Tentang":
    st.title("ℹ️ Tentang Aplikasi")
    st.markdown("""
    **Sepiro Jawa Timur, Sampeyan** v2.9.0
    
    Aplikasi interaktif untuk mempelajari bentuk kota dan kabupaten di Jawa Timur.
    
    **Fitur:**
    - 🧩 Quiz Tebak Wilayah
    - 📚 Info Wilayah + Logo Kabupaten/Kota
    - 🧩 Puzzle Drag & Drop
    - 🌋 Visualisasi 3D Gunung Bromo
    - 🏛️ Visualisasi 3D Balaikota Malang
    - 🏆 Papan Skor
    - ⏱️ Statistik Waktu
    - 🎵 Musik Latar
    """)


# ==================== FOOTER ====================
footer_texts = {
    "Quiz": f"🗺️ Quiz {len(wilayah_list)} Wilayah | Kesulitan: {st.session_state.difficulty}",
    "Info Wilayah": f"📚 Info Wilayah: {len(wilayah_list)} wilayah + Logo",
    "Puzzle": f"🧩 Puzzle Peta Jawa Timur",
    "Bromo 3D": "🌋 Gunung Bromo 3D",
    "Balaikota 3D": "🏛️ Balaikota Malang 3D",
    "Papan Skor": "🏆 Papan Skor",
    "Statistik Waktu": "⏱️ Statistik Waktu",
    "Pengaturan": "⚙️ Pengaturan",
    "Tentang": "ℹ️ Tentang"
}
footer_text = footer_texts.get(PAGE, "🧩 Sepiro Jawa Timur, Sampeyan")
st.markdown(create_footer(footer_text, FOOTER_BACKGROUND_URL, st.session_state.footer_brightness), unsafe_allow_html=True)
