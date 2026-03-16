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
    page_title="Pengetahuan Tentang Kota & Kabupaten di Jawa Timur",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== KONSTANTA ====================
GEOJSON_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kabkotjatim_ok.geojson")

SIDEBAR_BACKGROUND_URL = "https://rayadventure.com/wp-content/uploads/2018/06/tempat-wisata-di-jawa-timur.jpg"
FOOTER_BACKGROUND_URL = "https://static.promediateknologi.id/crop/0x0:0x0/0x0/webp/photo/p2/231/2024/09/11/Bisa-melihat-sunrise-yang-menakjubkan-di-Gunung-Bromo-Gambar-dari-Elizaveta-G-Shutterstock-213080307.png"
MUSIC_VIDEO_ID = "H1tWb3axAdA"


# ==================== FUNGSI EFEK BALON 3 LAPISAN ====================

def get_perfect_score_markdown_effect():
    return """
    <style>
    @keyframes drift {
        0%   { transform: translateY(0)   rotate(0deg)   scale(1);   opacity:1; }
        80%  { opacity: 1; }
        100% { transform: translateY(-110vh) rotate(720deg) scale(0.5); opacity:0; }
    }
    @keyframes sway {
        0%,100% { margin-left: 0; }
        25%     { margin-left: 40px; }
        75%     { margin-left: -40px; }
    }
    @keyframes popIn {
        0%   { transform: scale(0) rotate(-10deg); opacity:0; }
        60%  { transform: scale(1.15) rotate(3deg); opacity:1; }
        100% { transform: scale(1) rotate(0deg); opacity:1; }
    }
    @keyframes shimmer {
        0%,100% { text-shadow: 0 0 10px #ffd700, 0 0 20px #ff6b35, 0 0 40px #ffd700; }
        50%     { text-shadow: 0 0 20px #ff6b35, 0 0 40px #ffd700, 0 0 80px #ff6b35; }
    }
    @keyframes starPop {
        0%   { transform: scale(0) rotate(0deg);   opacity:0; }
        50%  { transform: scale(1.3) rotate(180deg); opacity:1; }
        100% { transform: scale(1) rotate(360deg);  opacity:1; }
    }
    @keyframes bgPulse {
        0%,100% { box-shadow: 0 0 30px rgba(255,215,0,0.5), inset 0 0 30px rgba(255,215,0,0.05); }
        50%     { box-shadow: 0 0 60px rgba(255,107,53,0.7), inset 0 0 60px rgba(255,215,0,0.1); }
    }
    .perfect-banner {
        animation: popIn 0.7s cubic-bezier(0.175,0.885,0.32,1.275) forwards,
                   bgPulse 2s ease-in-out infinite 0.7s;
        text-align: center;
        padding: 24px 20px;
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
        border-radius: 20px;
        border: 3px solid #ffd700;
        margin: 10px 0 18px 0;
        position: relative;
        overflow: hidden;
    }
    .perfect-banner::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: conic-gradient(
            transparent 0deg, rgba(255,215,0,0.03) 60deg,
            transparent 120deg, rgba(255,107,53,0.03) 180deg,
            transparent 240deg, rgba(255,215,0,0.03) 300deg, transparent 360deg
        );
        animation: drift 8s linear infinite;
        pointer-events: none;
    }
    .perfect-title {
        font-size: 2.4em;
        font-weight: 900;
        color: #ffd700;
        animation: shimmer 1.5s ease-in-out infinite;
        letter-spacing: 3px;
        margin: 0 0 6px 0;
        position: relative;
        z-index: 1;
    }
    .perfect-sub {
        font-size: 1.05em;
        color: #fff;
        margin: 6px 0;
        opacity: 0.92;
        position: relative;
        z-index: 1;
    }
    .balloon-float {
        display: inline-block;
        font-size: 2.1em;
        animation: drift 3s ease-in infinite, sway 1.5s ease-in-out infinite;
        margin: 0 5px;
        position: relative;
        z-index: 1;
    }
    .balloon-float:nth-child(1)  { animation-delay: 0.0s,  0.0s;  color: #ff6b6b; }
    .balloon-float:nth-child(2)  { animation-delay: 0.3s,  0.3s;  color: #ffd93d; }
    .balloon-float:nth-child(3)  { animation-delay: 0.6s,  0.6s;  color: #6bcb77; }
    .balloon-float:nth-child(4)  { animation-delay: 0.9s,  0.9s;  color: #4d96ff; }
    .balloon-float:nth-child(5)  { animation-delay: 1.2s,  1.2s;  color: #c77dff; }
    .balloon-float:nth-child(6)  { animation-delay: 1.5s,  1.5s;  color: #ff6bd6; }
    .balloon-float:nth-child(7)  { animation-delay: 0.15s, 0.15s; color: #ff8e53; }
    .balloon-float:nth-child(8)  { animation-delay: 0.45s, 0.45s; color: #00c9a7; }
    .balloon-float:nth-child(9)  { animation-delay: 0.75s, 0.75s; color: #ffb703; }
    .balloon-float:nth-child(10) { animation-delay: 1.05s, 1.05s; color: #f72585; }
    .star-float {
        display: inline-block;
        font-size: 1.4em;
        animation: drift 2.5s ease-in infinite, starPop 0.5s ease-out forwards;
        margin: 0 4px;
        position: relative;
        z-index: 1;
    }
    .star-float:nth-child(1) { animation-delay: 0.1s, 0.1s; }
    .star-float:nth-child(2) { animation-delay: 0.4s, 0.4s; }
    .star-float:nth-child(3) { animation-delay: 0.7s, 0.7s; }
    .star-float:nth-child(4) { animation-delay: 1.0s, 1.0s; }
    .star-float:nth-child(5) { animation-delay: 1.3s, 1.3s; }
    .star-float:nth-child(6) { animation-delay: 1.6s, 1.6s; }
    .emoji-row {
        font-size: 1.9em;
        margin-top: 14px;
        letter-spacing: 4px;
        position: relative;
        z-index: 1;
        animation: popIn 1s ease-out 0.5s both;
    }
    </style>

    <div class="perfect-banner">
        <div style="margin-bottom:14px;">
            <span class="balloon-float">🎈</span>
            <span class="balloon-float">🎈</span>
            <span class="balloon-float">🎈</span>
            <span class="balloon-float">🎈</span>
            <span class="balloon-float">🎈</span>
            <span class="balloon-float">🎈</span>
            <span class="balloon-float">🎈</span>
            <span class="balloon-float">🎈</span>
            <span class="balloon-float">🎈</span>
            <span class="balloon-float">🎈</span>
        </div>
        <p class="perfect-title">🏆 NILAI SEMPURNA! 🏆</p>
        <p class="perfect-sub">
            Luar biasa! Semua soal dijawab dengan benar! 🌟
        </p>
        <div style="margin-top:8px;">
            <span class="star-float">⭐</span>
            <span class="star-float">✨</span>
            <span class="star-float">💫</span>
            <span class="star-float">🌟</span>
            <span class="star-float">⭐</span>
            <span class="star-float">✨</span>
        </div>
        <div class="emoji-row">
            🎉 &nbsp; 🎊 &nbsp; 🥳 &nbsp; 🎁 &nbsp; 🎀 &nbsp; 🎶 &nbsp; 💖 &nbsp; 🎊 &nbsp; 🎉
        </div>
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
      body {
        background: transparent;
        overflow: hidden;
        width: 100%;
        height: 320px;
        position: relative;
      }
      #congrats-text {
        position: absolute;
        top: 18px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 999;
        text-align: center;
        animation: popIn 0.6s cubic-bezier(0.175,0.885,0.32,1.275) forwards;
        white-space: nowrap;
      }
      #congrats-text h1 {
        font-family: 'Arial Rounded MT Bold', Arial, sans-serif;
        font-size: 30px;
        color: #fff;
        text-shadow: 0 3px 12px rgba(0,0,0,0.5), 0 0 30px #ffd700;
        letter-spacing: 2px;
      }
      #congrats-text p {
        font-size: 14px;
        color: #ffe066;
        text-shadow: 0 2px 6px rgba(0,0,0,0.5);
        margin-top: 5px;
      }
      @keyframes popIn {
        0%   { opacity:0; transform: translateX(-50%) scale(0.4); }
        100% { opacity:1; transform: translateX(-50%) scale(1); }
      }
      .balloon {
        position: absolute;
        bottom: -120px;
        border-radius: 50%;
        animation: floatUp linear infinite;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
      }
      .balloon::after {
        content: '';
        position: absolute;
        bottom: -18px;
        left: 50%;
        transform: translateX(-50%);
        width: 1.5px;
        height: 20px;
        background: rgba(0,0,0,0.2);
      }
      .balloon::before {
        content: '';
        position: absolute;
        top: 10px;
        left: 12px;
        width: 11px;
        height: 7px;
        background: rgba(255,255,255,0.45);
        border-radius: 50%;
        transform: rotate(-30deg);
      }
      @keyframes floatUp {
        0%   { bottom: -130px; opacity: 0; transform: translateX(0) rotate(-2deg); }
        6%   { opacity: 1; }
        48%  { transform: translateX(20px) rotate(2deg); }
        90%  { opacity: 0.85; }
        100% { bottom: 110%; opacity: 0; transform: translateX(-10px) rotate(-2deg); }
      }
      .confetti {
        position: absolute;
        font-size: 18px;
        animation: confettiFloat linear infinite;
        opacity: 0;
        pointer-events: none;
      }
      @keyframes confettiFloat {
        0%   { bottom: -30px; opacity: 0; transform: rotate(0deg) scale(0.5); }
        10%  { opacity: 1; }
        85%  { opacity: 0.9; }
        100% { bottom: 108%; opacity: 0; transform: rotate(360deg) scale(1.2); }
      }
    </style>
    </head>
    <body>
    <div id="congrats-text">
      <h1>🏆 NILAI SEMPURNA! 🏆</h1>
      <p>Luar biasa! Semua soal dijawab dengan benar! 🎉🌟</p>
    </div>
    <div id="balloon-container"></div>
    <div id="confetti-container"></div>
    <script>
    (function() {
      var colors = [
        '#FF6B6B','#FF8E53','#FFD93D','#6BCB77',
        '#4D96FF','#C77DFF','#FF6BD6','#00C9A7',
        '#F72585','#7209B7','#3A86FF','#FFBE0B',
        '#06D6A0','#EF476F','#118AB2','#FFB703'
      ];
      var emojis = ['⭐','🌟','✨','💫','🎊','🎈','🌈','🎀','🎁','🎶','💖','🥳'];
      var bc = document.getElementById('balloon-container');
      var cc = document.getElementById('confetti-container');

      for (var i = 0; i < 24; i++) {
        (function(idx) {
          var b = document.createElement('div');
          b.className = 'balloon';
          var col = colors[idx % colors.length];
          b.style.background =
            'radial-gradient(circle at 35% 32%, ' + lighten(col,0.4) +
            ', ' + col + ' 58%, ' + darken(col,0.25) + ')';
          var sz  = 42 + Math.floor(Math.random() * 22);
          b.style.width    = sz + 'px';
          b.style.height   = Math.round(sz * 1.22) + 'px';
          b.style.left     = (2 + (idx / 24) * 96) + '%';
          b.style.animationDuration = (4.2 + Math.random() * 5).toFixed(2) + 's';
          b.style.animationDelay   = (Math.random() * 3.8).toFixed(2) + 's';
          bc.appendChild(b);
        })(i);
      }

      for (var j = 0; j < 20; j++) {
        (function(idx) {
          var s = document.createElement('div');
          s.className   = 'confetti';
          s.textContent = emojis[idx % emojis.length];
          s.style.left  = (1 + Math.random() * 98) + '%';
          s.style.fontSize = (12 + Math.random() * 16) + 'px';
          s.style.animationDuration = (3.5 + Math.random() * 4).toFixed(2) + 's';
          s.style.animationDelay   = (Math.random() * 4.5).toFixed(2) + 's';
          cc.appendChild(s);
        })(j);
      }

      function lighten(hex, t) { return blend(hex, '#ffffff', t); }
      function darken(hex, t)  { return blend(hex, '#000000', t); }
      function blend(h1, h2, t) {
        var a = ph(h1), b = ph(h2);
        return 'rgb(' +
          Math.round(a[0]+(b[0]-a[0])*t) + ',' +
          Math.round(a[1]+(b[1]-a[1])*t) + ',' +
          Math.round(a[2]+(b[2]-a[2])*t) + ')';
      }
      function ph(hex) {
        hex = hex.replace('#','');
        return [parseInt(hex.slice(0,2),16), parseInt(hex.slice(2,4),16), parseInt(hex.slice(4,6),16)];
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
    body {{
        background: transparent;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 54px;
    }}

    #backsound-btn {{
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 50px;
        padding: 10px 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.35);
        cursor: pointer;
        color: white;
        font-size: 13px;
        font-weight: bold;
        font-family: Arial, sans-serif;
        transition: all 0.3s ease;
        border: 1.5px solid rgba(255,255,255,0.25);
        user-select: none;
        white-space: nowrap;
    }}
    #backsound-btn:hover {{
        transform: scale(1.05);
        box-shadow: 0 8px 24px rgba(102,126,234,0.5);
    }}
    #backsound-btn:active {{
        transform: scale(0.97);
    }}

    #yt-iframe-hidden {{
        display: none;
        width: 0;
        height: 0;
        position: absolute;
        pointer-events: none;
    }}

    #music-visualizer {{
        display: flex;
        align-items: flex-end;
        gap: 2px;
        height: 18px;
    }}
    .music-bar {{
        width: 3px;
        background: linear-gradient(to top, #ffd700, #fff);
        border-radius: 2px;
        animation: musicBounce 0.7s ease-in-out infinite alternate;
    }}
    .music-bar:nth-child(1) {{ animation-delay: 0.00s; height: 6px; }}
    .music-bar:nth-child(2) {{ animation-delay: 0.15s; height: 14px; }}
    .music-bar:nth-child(3) {{ animation-delay: 0.05s; height: 9px; }}
    .music-bar:nth-child(4) {{ animation-delay: 0.20s; height: 16px; }}
    .music-bar:nth-child(5) {{ animation-delay: 0.10s; height: 7px; }}
    @keyframes musicBounce {{
        from {{ transform: scaleY(0.35); opacity: 0.55; }}
        to   {{ transform: scaleY(1.15); opacity: 1.0; }}
    }}
    .music-bar.paused {{
        animation: none !important;
        height: 3px !important;
        opacity: 0.4;
    }}
    </style>

    <iframe
        id="yt-iframe-hidden"
        src="https://www.youtube.com/embed/{MUSIC_VIDEO_ID}?autoplay=1&loop=1&playlist={MUSIC_VIDEO_ID}&enablejsapi=1&controls=0&rel=0&modestbranding=1"
        allow="autoplay; encrypted-media"
        allowfullscreen
    ></iframe>

    <div id="backsound-btn" onclick="toggleMusic()" title="Klik untuk play / pause musik latar">
        <div id="music-visualizer">
            <div class="music-bar"></div>
            <div class="music-bar"></div>
            <div class="music-bar"></div>
            <div class="music-bar"></div>
            <div class="music-bar"></div>
        </div>
        <span id="music-label">🎵 Musik On</span>
    </div>

    <script>
    (function() {{
        var isMusicPlaying = true;
        var ytPlayer = null;
        var initVolume = {volume};

        if (!window._ytApiLoaded) {{
            window._ytApiLoaded = true;
            var tag = document.createElement('script');
            tag.src = "https://www.youtube.com/iframe_api";
            document.head.appendChild(tag);
        }}

        window.onYouTubeIframeAPIReady = function() {{
            ytPlayer = new YT.Player('yt-iframe-hidden', {{
                events: {{
                    'onReady': function(event) {{
                        event.target.setVolume(initVolume);
                        event.target.playVideo();
                    }},
                    'onStateChange': function(event) {{
                        if (event.data === YT.PlayerState.ENDED) {{
                            event.target.playVideo();
                        }}
                    }}
                }}
            }});
        }};

        window.toggleMusic = function() {{
            var bars  = document.querySelectorAll('.music-bar');
            var label = document.getElementById('music-label');

            if (isMusicPlaying) {{
                if (ytPlayer && ytPlayer.pauseVideo) {{ ytPlayer.pauseVideo(); }}
                bars.forEach(function(b) {{ b.classList.add('paused'); }});
                label.textContent = '🎵 Musik Off';
                isMusicPlaying = false;
            }} else {{
                if (ytPlayer && ytPlayer.playVideo) {{ ytPlayer.playVideo(); }}
                bars.forEach(function(b) {{ b.classList.remove('paused'); }});
                label.textContent = '🎵 Musik On';
                isMusicPlaying = true;
            }}
        }};
    }})();
    </script>
    """


# ==================== PAPAN SKOR (SESSION STATE - CLOUD SAFE) ====================

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
            durasi = {
                "detik": round(durasi_detik, 1),
                "menit": round(durasi_detik / 60, 1),
                "format": f"{int(durasi_detik // 60)} menit {int(durasi_detik % 60)} detik"
            }

        now = now_wib()
        new_entry = {
            "nama": str(nama),
            "skor": int(skor),
            "level": str(level),
            "total_soal": int(total_soal),
            "persentase": round((int(skor) / int(total_soal)) * 100, 1),
            "tanggal": now.strftime("%Y-%m-%d %H:%M:%S"),
            "tanggal_lengkap": now.strftime("%Y-%m-%d %H:%M:%S"),
            "hari": now.strftime("%A"),
            "tanggal_only": now.strftime("%Y-%m-%d"),
            "jam": now.strftime("%H:%M:%S"),
            "tahun": now.year,
            "bulan": now.month,
            "timestamp": time.time(),
            "durasi": durasi,
            "waktu_mulai": waktu_mulai,
            "waktu_selesai": waktu_selesai
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
            scoreboard = [s for s in scoreboard if
                          s.get("tahun") == now.year and s.get("bulan") == now.month]

    scoreboard.sort(key=lambda x: (
        -x.get("skor", 0),
        x.get("durasi", {}).get("detik", float('inf')) if x.get("durasi") else float('inf'),
        -x.get("timestamp", 0)
    ))
    return scoreboard


def get_scoreboard_stats(scoreboard):
    if not scoreboard:
        return {
            "total_pemain": 0, "skor_tertinggi": 0, "rata_rata": 0,
            "level_populer": "-", "waktu_tercepat": None, "rata_rata_waktu": None
        }

    total_pemain = len(scoreboard)
    skor_tertinggi = max(s.get("skor", 0) for s in scoreboard)
    rata_rata = sum(s.get("skor", 0) for s in scoreboard) / total_pemain

    level_counts = {}
    for s in scoreboard:
        lv = s.get("level", "Unknown")
        level_counts[lv] = level_counts.get(lv, 0) + 1
    level_populer = max(level_counts, key=level_counts.get) if level_counts else "-"

    waktu_tercepat = None
    total_waktu = 0
    waktu_count = 0
    for s in scoreboard:
        if s.get("durasi") and s["durasi"].get("detik"):
            total_waktu += s["durasi"]["detik"]
            waktu_count += 1
            if s.get("skor") == s.get("total_soal"):
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
        return None, "Format GeoJSON tidak valid (bukan FeatureCollection)"

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
            "properties": {
                "name": nama,
                "WADMKK": nama,
                "WADMPR": "Jawa Timur",
                "LUAS": data["properties"].get("LUAS", 0),
            },
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
    st.info("Pastikan file `kabkotjatim_ok.geojson` sudah di-upload ke repositori GitHub bersama `app.py`.")
    st.stop()

jatim_geojson, wilayah_list = result
kota_list = [w for w in wilayah_list if w.startswith("Kota ")]
kab_list  = [w for w in wilayah_list if not w.startswith("Kota ")]


# ==================== FUNGSI WAKTU ====================

def get_current_time_info():
    now = now_wib()
    return {
        "tanggal": now.strftime("%Y-%m-%d"),
        "jam": now.strftime("%H:%M:%S"),
        "hari": now.strftime("%A"),
        "tahun": now.year,
        "timestamp": time.time()
    }


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
    "game_start_time": None,
    "game_end_time": None,
    "question_start_time": None,
    "total_game_duration": 0,
    "question_times": [],
    "average_answer_time": 0,
    "session_start_time": time.time(),
    "footer_brightness": 0.7,
    "scoreboard_data": [],
    "music_volume": 30,
    "music_enabled": True,
    "show_perfect_balloon": False,
    # Puzzle state
    "puzzle_difficulty": "Normal",
    "puzzle_started": False,
    "puzzle_target_region": None,
    "puzzle_start_time": None,
    "puzzle_completed": False,
    "puzzle_best_times": {},
}
for key, val in _defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ==================== FUNGSI TIMER ====================

def start_game_timer():
    st.session_state.game_start_time = time.time()
    st.session_state.game_end_time = None
    st.session_state.total_game_duration = 0
    st.session_state.question_times = []
    st.session_state.average_answer_time = 0


def start_question_timer():
    st.session_state.question_start_time = time.time()


def end_question_timer(is_correct=False):
    if st.session_state.question_start_time:
        duration = time.time() - st.session_state.question_start_time
        st.session_state.question_times.append({
            "question_number": st.session_state.total_questions + 1,
            "duration": duration,
            "correct": is_correct
        })
        total = sum(q["duration"] for q in st.session_state.question_times)
        st.session_state.average_answer_time = total / len(st.session_state.question_times)
        return duration
    return 0


def end_game_timer():
    if st.session_state.game_start_time is not None:
        if not st.session_state.game_end_time:
            st.session_state.game_end_time = time.time()
        if st.session_state.game_end_time is not None:
            st.session_state.total_game_duration = (
                st.session_state.game_end_time - st.session_state.game_start_time
            )
        return st.session_state.total_game_duration
    elif st.session_state.total_game_duration > 0:
        return st.session_state.total_game_duration
    return 0


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
    st.session_state.show_perfect_balloon = False
    pilih_wilayah()


# ==================== DATABASE INFO WILAYAH ====================

def get_wilayah_info(nama):
    db = {
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
        },
        "Kota Mojokerto": {
            "geografis": "Kota kecil di antara Surabaya dan Malang, dilintasi Sungai Brantas. Sejarah pusat Kerajaan Majapahit.",
            "demografi": "Penduduk: ±140 ribu jiwa. Masyarakat dengan budaya Jawa Timuran yang kental.",
            "budaya": "Budaya Jawa dengan pengaruh sejarah Majapahit yang kuat.",
            "keunikan": "Dikenal sebagai 'Kota Onde-onde'. Dekat situs bersejarah Trowulan.",
            "oleh_oleh": "Onde-onde Mojokerto, kerupuk rambak, dan berbagai makanan ringan khas."
        },
        "Kota Kediri": {
            "geografis": "Kota yang terbelah oleh Sungai Brantas, dikenal sebagai Kota Tahu.",
            "demografi": "Penduduk: ±300 ribu jiwa.",
            "budaya": "Budaya Jawa Arekan.",
            "keunikan": "Pusat industri rokok terbesar di Indonesia (Gudang Garam).",
            "oleh_oleh": "Tahu takwa, tahu kuning, dan getuk pisang."
        },
        "Kota Madiun": {
            "geografis": "Kota di jalur utama Surabaya-Yogyakarta, dikenal sebagai Kota Gadis.",
            "demografi": "Penduduk: ±200 ribu jiwa. Masyarakat dengan budaya Jawa yang kental.",
            "budaya": "Budaya Jawa dengan pengaruh arek dan mataraman.",
            "keunikan": "Dikenal dengan kuliner pecel Madiun dan Brem.",
            "oleh_oleh": "Pecel Madiun, brem, dan keripik pecel."
        },
        "Kota Blitar": {
            "geografis": "Kota kecil di kaki Gunung Kelud, terkenal sebagai tempat kelahiran Soekarno.",
            "demografi": "Penduduk: ±150 ribu jiwa.",
            "budaya": "Budaya Jawa Arekan.",
            "keunikan": "Makam Bung Karno, Istana Gebang, dan pusat peringatan Proklamator.",
            "oleh_oleh": "Rujak cingur khas Blitar, keripik tempe, dan pecel."
        },
        "Kota Pasuruan": {
            "geografis": "Kota kecil di pesisir utara, antara Surabaya dan Probolinggo.",
            "demografi": "Penduduk: ±200 ribu jiwa.",
            "budaya": "Budaya Jawa Arekan.",
            "keunikan": "Kota transit dengan industri kecil dan menengah.",
            "oleh_oleh": "Kerupuk udang, ikan asin, dan manisan buah."
        },
        "Kota Probolinggo": {
            "geografis": "Kota pesisir utara, jalur utama Surabaya-Banyuwangi-Bali.",
            "demografi": "Penduduk: ±240 ribu jiwa.",
            "budaya": "Budaya Jawa Arekan dengan pengaruh Madura.",
            "keunikan": "Kota transit menuju Bali, dikenal dengan mangga dan udang.",
            "oleh_oleh": "Mangga Probolinggo, kerupuk udang, dan ikan asin."
        },
        "Kabupaten Banyuwangi": {
            "geografis": "Ujung timur Pulau Jawa, berbatasan dengan Selat Bali. Wilayah terluas di Jawa Timur.",
            "demografi": "Penduduk: ±1,7 juta jiwa. Mayoritas suku Osing, Jawa, Madura, dan Bali.",
            "budaya": "Kesenian Gandrung Banyuwangi, Seblang, dan tari Jejer Jaran Dawuk.",
            "keunikan": "Kawah Ijen dengan api biru, Taman Nasional Alas Purwo, dan Pantai Plengkung (G-Land).",
            "oleh_oleh": "Pisang agung, sale pisang, kopi khas Banyuwangi, dan keripik tempe."
        },
        "Kabupaten Malang": {
            "geografis": "Kabupaten terluas kedua di Jawa Timur, mengelilingi Kota Malang dengan pegunungan dan pantai selatan.",
            "demografi": "Penduduk: ±2,7 juta jiwa.",
            "budaya": "Budaya Jawa Arekan.",
            "keunikan": "Pantai Balekambang, Coban Rondo, dan kawasan Bromo dari sisi Malang.",
            "oleh_oleh": "Keripik buah, keripik tempe, dan apel Malang."
        },
        "Kabupaten Jember": {
            "geografis": "Kabupaten di kawasan Tapal Kuda, dikenal sebagai Kota Tembakau.",
            "demografi": "Penduduk: ±2,5 juta jiwa. Masyarakat heterogen.",
            "budaya": "Budaya campuran Jawa, Madura, dan Pandhalungan.",
            "keunikan": "Karnaval Jember Fashion Carnival yang mendunia.",
            "oleh_oleh": "Suwar-suwir, proll tape, dan kopi Jember."
        },
        "Kabupaten Sidoarjo": {
            "geografis": "Kabupaten di selatan Surabaya, terkenal dengan industri dan lumpur Lapindo.",
            "demografi": "Penduduk: ±2,2 juta jiwa. Masyarakat heterogen.",
            "budaya": "Budaya Jawa Arekan.",
            "keunikan": "Pusat industri, bandara Juanda, dan kerajinan tas kulit.",
            "oleh_oleh": "Kerupuk udang, terasi, dan kerajinan kulit."
        },
        "Kabupaten Kediri": {
            "geografis": "Kabupaten yang mengelilingi Kota Kediri, wilayah subur di sekitar Sungai Brantas.",
            "demografi": "Penduduk: ±1,7 juta jiwa.",
            "budaya": "Budaya Jawa Arekan.",
            "keunikan": "Gunung Kelud, pabrik rokok terbesar, dan situs sejarah Kerajaan Kediri.",
            "oleh_oleh": "Tahu takwa, tahu kuning, dan getuk pisang."
        },
        "Kabupaten Mojokerto": {
            "geografis": "Kabupaten lokasi pusat Kerajaan Majapahit di Trowulan.",
            "demografi": "Penduduk: ±1,2 juta jiwa.",
            "budaya": "Budaya Jawa dengan pengaruh sejarah Majapahit.",
            "keunikan": "Situs Trowulan, bekas ibu kota Kerajaan Majapahit.",
            "oleh_oleh": "Onde-onde, kerupuk rambak, dan bandeng asap."
        },
        "Kabupaten Pasuruan": {
            "geografis": "Kabupaten dengan wilayah pegunungan di selatan dan pesisir utara.",
            "demografi": "Penduduk: ±1,6 juta jiwa.",
            "budaya": "Budaya Jawa Arekan.",
            "keunikan": "Kawasan Taman Nasional Bromo Tengger Semeru dari sisi Pasuruan.",
            "oleh_oleh": "Manisan buah, keripik apel, dan susu murni."
        },
        "Kabupaten Probolinggo": {
            "geografis": "Kabupaten dengan wilayah pegunungan dan pantai utara.",
            "demografi": "Penduduk: ±1,2 juta jiwa.",
            "budaya": "Budaya Jawa Arekan dengan pengaruh Madura.",
            "keunikan": "Kawasan Gunung Bromo dari sisi Probolinggo, penghasil mangga.",
            "oleh_oleh": "Mangga, kerupuk udang, dan keripik pisang."
        },
        "Kabupaten Blitar": {
            "geografis": "Kabupaten di kaki Gunung Kelud, memiliki wilayah pegunungan dan pantai selatan.",
            "demografi": "Penduduk: ±1,2 juta jiwa.",
            "budaya": "Budaya Jawa Arekan.",
            "keunikan": "Tempat kelahiran Presiden Soekarno, memiliki Makam Bung Karno.",
            "oleh_oleh": "Rujak cingur, sate blater, dan keripik tempe."
        },
        "Kabupaten Tulungagung": {
            "geografis": "Kabupaten di selatan Jawa Timur, terkenal dengan industri marmer.",
            "demografi": "Penduduk: ±1,1 juta jiwa.",
            "budaya": "Budaya Jawa Mataraman.",
            "keunikan": "Penghasil marmer terbesar di Indonesia, Pantai Popoh.",
            "oleh_oleh": "Kerajinan marmer, keripik tempe, dan jenang."
        },
        "Kabupaten Trenggalek": {
            "geografis": "Kabupaten di pesisir selatan Jawa Timur dengan pantai-pantai indah.",
            "demografi": "Penduduk: ±750 ribu jiwa. Mayoritas suku Jawa.",
            "budaya": "Budaya Jawa dengan tradisi pesisiran.",
            "keunikan": "Memiliki Pantai Prigi dan Pantai Karanggongso yang indah.",
            "oleh_oleh": "Alen-alen, keripik tempe, dan ikan asap."
        },
        "Kabupaten Ponorogo": {
            "geografis": "Kabupaten yang terkenal dengan kesenian Reog.",
            "demografi": "Penduduk: ±950 ribu jiwa.",
            "budaya": "Budaya Jawa Mataraman, pusat kesenian Reog.",
            "keunikan": "Kota Reog, Festival Reog Nasional, dan Telaga Ngebel.",
            "oleh_oleh": "Dawet Jabung, sambal pecel, dan keripik tempe."
        },
        "Kabupaten Pacitan": {
            "geografis": "Kabupaten di pesisir selatan dengan pantai-pantai indah, dijuluki '1001 Goa'.",
            "demografi": "Penduduk: ±550 ribu jiwa.",
            "budaya": "Budaya Jawa Mataraman.",
            "keunikan": "Goa Gong, Goa Tabuhan, dan pantai-pantai indah di selatan.",
            "oleh_oleh": "Sale pisang, keripik tempe, dan ikan asap."
        },
        "Kabupaten Ngawi": {
            "geografis": "Kabupaten di perbatasan Jawa Timur dan Jawa Tengah, dilintasi Bengawan Solo.",
            "demografi": "Penduduk: ±900 ribu jiwa.",
            "budaya": "Budaya Jawa Mataraman.",
            "keunikan": "Benteng Van den Bosch, gerbang masuk dari arah Solo.",
            "oleh_oleh": "Keripik tempe, pecel, dan jenang."
        },
        "Kabupaten Magetan": {
            "geografis": "Kabupaten di perbatasan Jawa Timur dan Jawa Tengah, di lereng Gunung Lawu.",
            "demografi": "Penduduk: ±650 ribu jiwa.",
            "budaya": "Budaya Jawa Mataraman (perbatasan dengan Solo/Yogyakarta).",
            "keunikan": "Telaga Sarangan, gerbang masuk Jawa Timur dari arah barat.",
            "oleh_oleh": "Keripik buah, brem, dan oleh-oleh khas Lawu."
        },
        "Kabupaten Madiun": {
            "geografis": "Kabupaten di sekitar Kota Madiun, wilayah agraris dengan persawahan luas.",
            "demografi": "Penduduk: ±750 ribu jiwa.",
            "budaya": "Budaya Jawa Mataraman.",
            "keunikan": "Penghasil beras dan jahe, jalur utama Surabaya-Yogyakarta.",
            "oleh_oleh": "Pecel Madiun, brem, dan jahe instan."
        },
        "Kabupaten Nganjuk": {
            "geografis": "Kabupaten di lembah Gunung Wilis, dilintasi Sungai Brantas.",
            "demografi": "Penduduk: ±1,1 juta jiwa. Masyarakat agraris.",
            "budaya": "Budaya Jawa Mataraman.",
            "keunikan": "Dikenal sebagai kota bayam dan penghasil beras berkualitas.",
            "oleh_oleh": "Bayam Nganjuk, keripik bayam, dan getuk pisang."
        },
        "Kabupaten Jombang": {
            "geografis": "Kabupaten yang dikenal sebagai 'Kota Santri' karena banyak pesantren.",
            "demografi": "Penduduk: ±1,3 juta jiwa.",
            "budaya": "Budaya Jawa dengan pengaruh pesantren.",
            "keunikan": "Pusat pendidikan Islam dengan pesantren-pesantren besar.",
            "oleh_oleh": "Jenang, keripik tempe, dan sambal pecel."
        },
        "Kabupaten Bojonegoro": {
            "geografis": "Kabupaten di Bengawan Solo, wilayah penghasil minyak dan gas.",
            "demografi": "Penduduk: ±1,3 juta jiwa.",
            "budaya": "Budaya Jawa dengan pengaruh Jawa Tengah.",
            "keunikan": "Kota minyak, Waduk Pacal, dan jembatan tua Bengawan Solo.",
            "oleh_oleh": "Ledre (makanan khas), sambal pecel, dan keripik pisang."
        },
        "Kabupaten Tuban": {
            "geografis": "Kabupaten pesisir utara, perbatasan Jawa Timur dan Jawa Tengah.",
            "demografi": "Penduduk: ±1,2 juta jiwa.",
            "budaya": "Budaya pesisir dengan pengaruh Jawa dan Madura.",
            "keunikan": "Makam Sunan Bonang, kota tua dengan sejarah penyebaran Islam.",
            "oleh_oleh": "Kopi Tuban, bandeng asap, dan kerupuk ikan."
        },
        "Kabupaten Lamongan": {
            "geografis": "Kabupaten pesisir utara, berbatasan dengan Laut Jawa.",
            "demografi": "Penduduk: ±1,4 juta jiwa.",
            "budaya": "Budaya pesisir dengan pengaruh Jawa dan Madura.",
            "keunikan": "Makam Sunan Drajat, wisata Bahari Lamongan, dan kuliner terkenal.",
            "oleh_oleh": "Soto Lamongan, wingko babat, dan kerupuk ikan."
        },
        "Kabupaten Gresik": {
            "geografis": "Kabupaten pesisir utara, berbatasan dengan Surabaya, memiliki banyak industri.",
            "demografi": "Penduduk: ±1,3 juta jiwa. Masyarakat heterogen.",
            "budaya": "Budaya pesisir dengan pengaruh Jawa dan Madura.",
            "keunikan": "Kota Industri, makam Sunan Giri, dan bandar udara internasional.",
            "oleh_oleh": "Bandeng presto, udang, dan kerupuk ikan."
        },
        "Kabupaten Bangkalan": {
            "geografis": "Kabupaten di Pulau Madura, pintu masuk dari Surabaya melalui Jembatan Suramadu.",
            "demografi": "Penduduk: ±1 juta jiwa. Mayoritas suku Madura.",
            "budaya": "Budaya Madura yang kental.",
            "keunikan": "Pintu gerbang Madura, Universitas Trunojoyo, dan makam para ulama.",
            "oleh_oleh": "Keripik pedas, batik Madura, dan olahan ikan."
        },
        "Kabupaten Sampang": {
            "geografis": "Kabupaten di Pulau Madura bagian selatan.",
            "demografi": "Penduduk: ±950 ribu jiwa. Mayoritas suku Madura.",
            "budaya": "Budaya Madura yang kental.",
            "keunikan": "Dikenal dengan tradisi karapan sapi dan batik khas Madura.",
            "oleh_oleh": "Batik Madura, keripik pedas, dan ikan asap."
        },
        "Kabupaten Pamekasan": {
            "geografis": "Kabupaten di Pulau Madura, berbatasan dengan Laut Jawa di utara dan Selat Madura di selatan.",
            "demografi": "Penduduk: ±850 ribu jiwa. Mayoritas suku Madura.",
            "budaya": "Budaya Madura yang kuat, tradisi karapan sapi, dan musik tong-tong.",
            "keunikan": "Dikenal sebagai pusat pendidikan agama di Madura dengan banyak pesantren.",
            "oleh_oleh": "Keripik pedas, batik Madura, dan olahan ikan."
        },
        "Kabupaten Sumenep": {
            "geografis": "Kabupaten di ujung timur Pulau Madura, terdiri dari Pulau Madura dan gugusan kepulauan.",
            "demografi": "Penduduk: ±1,1 juta jiwa. Suku Madura dengan budaya bahari.",
            "budaya": "Budaya Madura dengan pengaruh dari berbagai kerajaan.",
            "keunikan": "Keraton Sumenep, batik tulis Sumenep, dan kepulauan Kangean.",
            "oleh_oleh": "Batik Sumenep, keripik pedas, dan ikan asap."
        },
        "Kabupaten Bondowoso": {
            "geografis": "Kabupaten di kawasan Tapal Kuda, Jawa Timur bagian timur.",
            "demografi": "Penduduk: ±800 ribu jiwa. Campuran Jawa dan Madura.",
            "budaya": "Budaya campuran Jawa-Madura yang unik.",
            "keunikan": "Dikenal dengan tape Bondowoso dan kawasan perkebunan kopi.",
            "oleh_oleh": "Tape Bondowoso, kopi Bondowoso, dan kue nastar tape."
        },
        "Kabupaten Situbondo": {
            "geografis": "Kabupaten di kawasan Tapal Kuda, jalur pantai utara menuju Banyuwangi.",
            "demografi": "Penduduk: ±700 ribu jiwa. Campuran Jawa dan Madura.",
            "budaya": "Budaya campuran Jawa-Madura.",
            "keunikan": "Kawasan perbukitan dengan perkebunan, Pantai Pasir Putih.",
            "oleh_oleh": "Ikan asap, kerupuk ikan, dan manisan buah."
        },
        "Kabupaten Lumajang": {
            "geografis": "Kabupaten di kaki Gunung Semeru, memiliki pantai selatan yang indah.",
            "demografi": "Penduduk: ±1,1 juta jiwa.",
            "budaya": "Budaya Jawa Tengger dan Jawa umumnya.",
            "keunikan": "Kawasan Ranu Pane dan Ranu Kumbolo di jalur pendakian Semeru.",
            "oleh_oleh": "Pisang agung, keripik pisang, dan sale pisang."
        },
    }

    if nama in db:
        return db[nama]

    tipe = "Kota" if nama.startswith("Kota ") else "Kabupaten"
    return {
        "geografis": f"{tipe} di Provinsi Jawa Timur dengan berbagai potensi sumber daya alam.",
        "demografi": f"Penduduk dengan keragaman budaya dan tradisi khas {tipe} di Jawa Timur.",
        "budaya": f"Memiliki kesenian tradisional dan adat istiadat yang masih dilestarikan.",
        "keunikan": f"Berbagai destinasi wisata dan potensi ekonomi yang menjadi ciri khas wilayah.",
        "oleh_oleh": f"Berbagai produk makanan khas dan kerajinan tangan dari {nama}."
    }


# ==================== CSS SIDEBAR & FOOTER ====================

def get_background_image_html(image_url):
    return f"""
    <style>
    [data-testid="stSidebar"] {{
        background-image: url("{image_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    [data-testid="stSidebar"]::before {{
        content: "";
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: rgba(0,0,0,0.6);
        z-index: 0;
    }}
    [data-testid="stSidebar"] > div:first-child {{
        position: relative;
        z-index: 1;
        background-color: transparent !important;
    }}
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stButton > button {{
        color: white !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
    }}
    [data-testid="stSidebar"] .stRadio label {{ color: white !important; }}
    [data-testid="stSidebar"] .stButton > button {{
        background-color: rgba(102,126,234,0.8);
        border: 1px solid rgba(255,255,255,0.3);
    }}
    [data-testid="stSidebar"] [data-testid="stMetricValue"],
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {{
        color: white !important;
    }}
    [data-testid="stSidebar"] .stSlider label {{ color: white !important; }}
    [data-testid="stSidebar"] hr {{ border-color: rgba(255,255,255,0.3); }}
    [data-testid="stSidebar"] iframe {{
        display: block;
    }}
    </style>
    """


def get_footer_css(image_url, brightness=0.7):
    ov = 1 - brightness
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
        border-radius: 15px 15px 0 0;
        overflow: hidden;
        filter: brightness({brightness});
    }}
    .footer-container::before {{
        content: "";
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: rgba(0,0,0,{ov});
        z-index: 1;
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
    .footer-content p {{ margin: 5px 0; font-size: 14px; }}
    .footer-title {{ font-size: 16px; font-weight: bold; color: #ffd700; margin-bottom: 10px; }}
    .footer-link {{ color: #ffd700; text-decoration: none; font-weight: bold; }}
    .footer-divider {{
        height: 3px;
        background: linear-gradient(90deg, transparent, #ffd700, transparent);
        margin: 20px 0 10px 0;
    }}
    </style>
    """


def create_footer(footer_text, image_url, brightness=0.7):
    current_time = now_wib().strftime("%H:%M:%S")
    return f"""
    <div class="footer-divider"></div>
    <div class="footer-container">
        <div class="footer-content">
            <div class="footer-title">🧩 Pengetahuan Tentang Kota & Kabupaten Jawa Timur</div>
            <p>{footer_text}</p>
            <p>⏰ {current_time} WIB | © 2026 Program Pengabdian Masyarakat - Penguatan Geospasial Tentang Jawa Timur Sejak Usia Dini Melalui Edukasi Gamifikasi Menggunakan Platform "Pengetahuan Jatim" - Lab. Environmental, Infrastructure, and Information System (EIIS), Dept. Perencanaan Wilayah & Kota, Fak. Teknik, Universitas Brawijaya | Versi 2.8.0</p>
            <p>Game Tebak Wilayah | Mode Belajar | Puzzle Drag & Drop | Bromo 3D | Balaikota 3D | Papan Skor | Statistik Waktu | 🎵 Musik</p>
        </div>
    </div>
    """


# ==================== PUZZLE DRAG & DROP FEATURE ====================

def get_puzzle_html(geojson_data, target_region, difficulty, piece_count, start_time_ms):
    """
    Generate self-contained HTML puzzle game with drag-and-drop SVG pieces.
    The map is sliced into a grid; only the target region's polygon pieces are shown.
    """
    # Find the target feature
    target_feature = None
    all_features = geojson_data.get("features", [])
    for feat in all_features:
        if feat["properties"]["name"] == target_region:
            target_feature = feat
            break

    if not target_feature:
        return "<p>❌ Data wilayah tidak ditemukan.</p>"

    # Serialize only needed data - target + neighbors for context
    # Pass just enough GeoJSON for the puzzle
    context_features = []
    for feat in all_features:
        context_features.append({
            "type": "Feature",
            "properties": {"name": feat["properties"]["name"]},
            "geometry": feat["geometry"]
        })

    geojson_str = json.dumps({
        "type": "FeatureCollection",
        "features": context_features
    })

    target_str = json.dumps(target_feature)

    level_config = {
        "Pemula":  {"pieces": 5,  "color": "#4CAF50", "label": "🌱 Pemula",  "snap_dist": 40},
        "Mudah":   {"pieces": 10, "color": "#2196F3", "label": "😊 Mudah",   "snap_dist": 30},
        "Normal":  {"pieces": 25, "color": "#FF9800", "label": "⚡ Normal",  "snap_dist": 22},
        "Sulit":   {"pieces": 38, "color": "#f44336", "label": "🔥 Sulit",   "snap_dist": 15},
    }
    cfg = level_config.get(difficulty, level_config["Normal"])

    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap');
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    font-family: 'Nunito', sans-serif;
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
    color: white;
    padding: 10px;
  }}
  #puzzle-header {{
    text-align: center;
    padding: 8px 0 12px 0;
  }}
  #puzzle-header h2 {{
    font-size: 1.5em;
    font-weight: 900;
    background: linear-gradient(90deg, #ffd700, #ff6b35, #ffd700);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 1px;
  }}
  #puzzle-header .subtitle {{
    font-size: 0.85em;
    color: rgba(255,255,255,0.7);
    margin-top: 2px;
  }}
  #stats-bar {{
    display: flex;
    justify-content: center;
    gap: 20px;
    margin: 8px 0;
    flex-wrap: wrap;
  }}
  .stat-pill {{
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 30px;
    padding: 5px 16px;
    font-size: 0.82em;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .stat-pill span {{ color: #ffd700; font-size: 1.1em; }}
  #level-badge {{
    display: inline-block;
    background: {cfg['color']};
    color: white;
    padding: 3px 14px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.82em;
    margin-bottom: 6px;
  }}
  #main-layout {{
    display: flex;
    gap: 12px;
    align-items: flex-start;
    justify-content: center;
    flex-wrap: wrap;
  }}
  #canvas-wrapper {{
    position: relative;
    background: rgba(255,255,255,0.05);
    border: 2px solid rgba(255,255,255,0.15);
    border-radius: 16px;
    overflow: hidden;
    flex: 1 1 520px;
    max-width: 620px;
  }}
  #canvas-label {{
    position: absolute;
    top: 8px; left: 12px;
    font-size: 0.72em;
    color: rgba(255,255,255,0.5);
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
  }}
  #puzzle-canvas {{
    display: block;
    width: 100%;
    touch-action: none;
    user-select: none;
    cursor: grab;
  }}
  #puzzle-canvas:active {{ cursor: grabbing; }}
  #pieces-panel {{
    background: rgba(255,255,255,0.06);
    border: 2px dashed rgba(255,255,255,0.2);
    border-radius: 16px;
    padding: 12px;
    flex: 0 0 200px;
    max-height: 580px;
    overflow-y: auto;
    min-width: 160px;
  }}
  #pieces-panel h4 {{
    font-size: 0.8em;
    color: rgba(255,255,255,0.6);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
    text-align: center;
  }}
  #pieces-container {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    justify-content: center;
  }}
  .piece-thumb {{
    background: rgba(255,255,255,0.08);
    border: 1.5px solid rgba(255,255,255,0.2);
    border-radius: 8px;
    cursor: grab;
    transition: all 0.2s;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .piece-thumb:hover {{
    background: rgba(255,215,0,0.15);
    border-color: #ffd700;
    transform: scale(1.08);
    box-shadow: 0 4px 14px rgba(255,215,0,0.3);
  }}
  .piece-thumb.placed {{
    opacity: 0.35;
    cursor: default;
    pointer-events: none;
    border-color: #4CAF50;
    background: rgba(76,175,80,0.1);
  }}
  .piece-thumb svg {{
    pointer-events: none;
  }}
  #progress-bar-wrap {{
    margin: 10px 0 6px 0;
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
    height: 10px;
    overflow: hidden;
  }}
  #progress-bar-fill {{
    height: 100%;
    background: linear-gradient(90deg, #4CAF50, #8BC34A);
    border-radius: 10px;
    transition: width 0.4s ease;
    width: 0%;
  }}
  #progress-text {{
    text-align: center;
    font-size: 0.78em;
    color: rgba(255,255,255,0.6);
    margin-bottom: 8px;
  }}
  #btn-row {{
    display: flex;
    gap: 8px;
    justify-content: center;
    margin: 10px 0 6px 0;
    flex-wrap: wrap;
  }}
  .puzzle-btn {{
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    border-radius: 20px;
    padding: 8px 20px;
    font-size: 0.85em;
    font-weight: 700;
    font-family: 'Nunito', sans-serif;
    cursor: pointer;
    transition: all 0.2s;
    box-shadow: 0 4px 12px rgba(102,126,234,0.4);
  }}
  .puzzle-btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(102,126,234,0.6);
  }}
  .puzzle-btn.danger {{
    background: linear-gradient(135deg, #f44336, #c62828);
    box-shadow: 0 4px 12px rgba(244,67,54,0.4);
  }}
  .puzzle-btn.success {{
    background: linear-gradient(135deg, #4CAF50, #2E7D32);
    box-shadow: 0 4px 12px rgba(76,175,80,0.4);
  }}
  #win-overlay {{
    display: none;
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: rgba(0,0,0,0.85);
    z-index: 999;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    text-align: center;
    padding: 20px;
  }}
  #win-overlay.show {{ display: flex; }}
  #win-box {{
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border: 3px solid #ffd700;
    border-radius: 24px;
    padding: 36px 40px;
    max-width: 400px;
    box-shadow: 0 0 60px rgba(255,215,0,0.4);
    animation: popIn 0.6s cubic-bezier(0.175,0.885,0.32,1.275) forwards;
  }}
  @keyframes popIn {{
    from {{ transform: scale(0.4); opacity:0; }}
    to   {{ transform: scale(1);   opacity:1; }}
  }}
  #win-box h1 {{
    font-size: 2.2em;
    font-weight: 900;
    background: linear-gradient(90deg, #ffd700, #ff6b35);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
  }}
  #win-box p {{
    color: rgba(255,255,255,0.85);
    font-size: 1.05em;
    margin: 8px 0;
  }}
  #win-time {{
    font-size: 1.8em;
    font-weight: 900;
    color: #ffd700;
    margin: 12px 0;
  }}
  .hint-zone {{
    stroke-dasharray: 6,3;
    stroke: rgba(255,215,0,0.4);
    fill: rgba(255,215,0,0.05);
    stroke-width: 1.5;
    pointer-events: none;
  }}
  .placed-piece {{
    fill: rgba(76,175,80,0.5);
    stroke: #4CAF50;
    stroke-width: 2;
    pointer-events: none;
    filter: drop-shadow(0 0 6px rgba(76,175,80,0.8));
  }}
  .dragging-piece {{
    opacity: 0.9;
    filter: drop-shadow(0 8px 16px rgba(0,0,0,0.6));
  }}
  #tooltip {{
    position: absolute;
    background: rgba(0,0,0,0.8);
    color: #ffd700;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 0.75em;
    font-weight: 700;
    pointer-events: none;
    display: none;
    white-space: nowrap;
    z-index: 100;
  }}
  #snap-feedback {{
    position: absolute;
    pointer-events: none;
    font-size: 1.6em;
    animation: floatUp 0.8s ease-out forwards;
    z-index: 200;
    display: none;
  }}
  @keyframes floatUp {{
    0%   {{ opacity:1; transform: translateY(0) scale(1); }}
    100% {{ opacity:0; transform: translateY(-60px) scale(1.5); }}
  }}
</style>
</head>
<body>

<div id="puzzle-header">
  <div id="level-badge">{cfg['label']} — {cfg['pieces']} Keping</div>
  <h2>🧩 PUZZLE: {target_region.upper()}</h2>
  <div class="subtitle">Susun kepingan untuk membentuk peta wilayah!</div>
</div>

<div id="stats-bar">
  <div class="stat-pill">⏱️ Waktu <span id="timer-display">00:00</span></div>
  <div class="stat-pill">🧩 Keping <span id="placed-count">0</span>/<span id="total-count">0</span></div>
  <div class="stat-pill">🎯 Akurasi <span id="accuracy-display">100%</span></div>
</div>

<div id="progress-bar-wrap"><div id="progress-bar-fill"></div></div>
<div id="progress-text">Seret kepingan ke area peta yang benar!</div>

<div id="btn-row">
  <button class="puzzle-btn" onclick="shufflePieces()">🔀 Acak Ulang</button>
  <button class="puzzle-btn" onclick="showHint()">💡 Petunjuk</button>
  <button class="puzzle-btn danger" onclick="resetPuzzle()">🔄 Reset</button>
  <button class="puzzle-btn success" onclick="autoSolve()">✨ Selesaikan</button>
</div>

<div id="main-layout">
  <div id="canvas-wrapper">
    <div id="canvas-label">AREA PUZZLE</div>
    <canvas id="puzzle-canvas"></canvas>
    <div id="tooltip"></div>
    <div id="snap-feedback">✅</div>
  </div>
  <div id="pieces-panel">
    <h4>📦 Kepingan ({cfg['pieces']})</h4>
    <div id="progress-bar-wrap" style="margin:6px 0 10px 0;">
      <div id="progress-bar-fill2" style="height:8px;background:linear-gradient(90deg,#4CAF50,#8BC34A);border-radius:10px;width:0%;transition:width 0.4s;"></div>
    </div>
    <div id="pieces-container"></div>
  </div>
</div>

<div id="win-overlay">
  <div id="win-box">
    <div style="font-size:3em;margin-bottom:8px;">🏆</div>
    <h1>PUZZLE SELESAI!</h1>
    <p>Wilayah: <strong>{target_region}</strong></p>
    <p>Tingkat: <strong>{cfg['label']}</strong></p>
    <div id="win-time">00:00</div>
    <p id="win-moves">0 kesalahan</p>
    <p style="color:#ffd700;font-size:0.9em;margin-top:10px;">🎉 Luar biasa! Kamu berhasil!</p>
    <button class="puzzle-btn success" style="margin-top:18px;font-size:1em;padding:12px 32px;" onclick="location.reload()">🔄 Main Lagi</button>
  </div>
</div>

<script>
(function() {{
  // ===== CONSTANTS =====
  const GEOJSON = {geojson_str};
  const TARGET_FEATURE = {target_str};
  const TARGET_NAME = "{target_region}";
  const PIECE_COUNT = {cfg['pieces']};
  const SNAP_DIST = {cfg['snap_dist']};
  const LEVEL_COLOR = "{cfg['color']}";
  const START_TIME = Date.now();

  // ===== CANVAS SETUP =====
  const canvas = document.getElementById('puzzle-canvas');
  const ctx = canvas.getContext('2d');
  const wrapper = document.getElementById('canvas-wrapper');

  let W = 600, H = 520;
  canvas.width = W; canvas.height = H;

  // ===== PROJECTION =====
  // Compute bounding box of ALL Jawa Timur features
  let minLon=180, maxLon=-180, minLat=90, maxLat=-90;
  GEOJSON.features.forEach(f => {{
    iterCoords(f.geometry, (lon, lat) => {{
      if(lon<minLon) minLon=lon; if(lon>maxLon) maxLon=lon;
      if(lat<minLat) minLat=lat; if(lat>maxLat) maxLat=lat;
    }});
  }});

  // Add padding
  const pad = 30;
  const lonRange = maxLon - minLon;
  const latRange = maxLat - minLat;
  const scaleX = (W - pad*2) / lonRange;
  const scaleY = (H - pad*2) / latRange;
  const scale = Math.min(scaleX, scaleY);

  function project(lon, lat) {{
    const x = pad + (lon - minLon) * scale;
    const y = H - pad - (lat - minLat) * scale;
    return [x, y];
  }}

  function iterCoords(geometry, cb) {{
    function rec(coords, depth) {{
      if(typeof coords[0] === 'number') {{ cb(coords[0], coords[1]); return; }}
      coords.forEach(c => rec(c, depth+1));
    }}
    rec(geometry.coordinates, 0);
  }}

  function buildPath(geometry) {{
    const p = new Path2D();
    function addRing(ring) {{
      ring.forEach((coord, i) => {{
        const [x,y] = project(coord[0], coord[1]);
        if(i===0) p.moveTo(x,y); else p.lineTo(x,y);
      }});
      p.closePath();
    }}
    if(geometry.type === 'Polygon') {{
      geometry.coordinates.forEach(addRing);
    }} else if(geometry.type === 'MultiPolygon') {{
      geometry.coordinates.forEach(poly => poly.forEach(addRing));
    }}
    return p;
  }}

  // Build path for target
  const targetPath = buildPath(TARGET_FEATURE.geometry);

  // Compute bounding box of target
  let tMinX=W, tMaxX=0, tMinY=H, tMaxY=0;
  iterCoords(TARGET_FEATURE.geometry, (lon, lat) => {{
    const [x,y] = project(lon,lat);
    if(x<tMinX) tMinX=x; if(x>tMaxX) tMaxX=x;
    if(y<tMinY) tMinY=y; if(y>tMaxY) tMaxY=y;
  }});
  const targetCX = (tMinX+tMaxX)/2;
  const targetCY = (tMinY+tMaxY)/2;

  // ===== PUZZLE PIECES GENERATION =====
  // Slice the target region into a grid of pieces
  // Grid dims based on piece count
  let gridCols, gridRows;
  if(PIECE_COUNT <= 5)       {{ gridCols=2; gridRows=3; }}
  else if(PIECE_COUNT <= 10) {{ gridCols=3; gridRows=4; }}
  else if(PIECE_COUNT <= 25) {{ gridCols=5; gridRows=5; }}
  else                       {{ gridCols=6; gridRows=7; }}

  const tW = tMaxX - tMinX;
  const tH = tMaxY - tMinY;
  const cellW = tW / gridCols;
  const cellH = tH / gridRows;

  // Generate pieces by intersecting grid cells with target polygon
  // We approximate this visually: each piece is a clipped rectangle
  let pieces = [];
  let pieceId = 0;

  for(let row=0; row<gridRows; row++) {{
    for(let col=0; col<gridCols; col++) {{
      const cx1 = tMinX + col*cellW;
      const cy1 = tMinY + row*cellH;
      const cx2 = cx1 + cellW;
      const cy2 = cy1 + cellH;
      const centerX = (cx1+cx2)/2;
      const centerY = (cy1+cy2)/2;

      // Check if this cell center is inside the target polygon
      // Use canvas hit test
      const testCanvas = document.createElement('canvas');
      testCanvas.width = W; testCanvas.height = H;
      const testCtx = testCanvas.getContext('2d');
      testCtx.fill(targetPath);
      const isInside = testCtx.isPointInPath(targetPath, centerX, centerY);
      if(!isInside) continue;

      pieces.push({{
        id: pieceId++,
        col, row,
        targetX: cx1, targetY: cy1,
        targetW: cellW, targetH: cellH,
        // Current position (scattered in puzzle panel)
        currentX: 0, currentY: 0,
        placed: false,
        dragging: false,
        dragOffX: 0, dragOffY: 0,
        // Thumb offset in panel
        panelX: 0, panelY: 0,
        inPanel: true,
      }});
    }}
  }}

  // Limit to PIECE_COUNT
  if(pieces.length > PIECE_COUNT) {{
    pieces = pieces.slice(0, PIECE_COUNT);
  }}

  const totalPieces = pieces.length;
  document.getElementById('total-count').textContent = totalPieces;

  // ===== RENDER THUMBNAILS IN PANEL =====
  const piecesContainer = document.getElementById('pieces-container');
  const thumbCanvases = {{}};

  function buildThumbnails() {{
    piecesContainer.innerHTML = '';
    pieces.forEach(p => {{
      if(p.placed) return;
      const thumbW = 70, thumbH = 60;
      const div = document.createElement('div');
      div.className = 'piece-thumb' + (p.placed ? ' placed' : '');
      div.id = 'thumb-' + p.id;
      div.style.width = thumbW+'px';
      div.style.height = thumbH+'px';

      const tc = document.createElement('canvas');
      tc.width = thumbW; tc.height = thumbH;
      thumbCanvases[p.id] = tc;

      // Draw piece on thumbnail
      const tctx = tc.getContext('2d');
      // Scale to fit in thumb
      const sx = (thumbW-8) / p.targetW;
      const sy = (thumbH-8) / p.targetH;
      const ts = Math.min(sx, sy);

      tctx.save();
      tctx.translate(thumbW/2, thumbH/2);
      tctx.scale(ts, ts);
      tctx.translate(-(p.targetX + p.targetW/2), -(p.targetY + p.targetH/2));

      // Clip to target shape
      tctx.save();
      tctx.clip(targetPath);

      // Fill piece color
      const hue = (p.id * 37 + 180) % 360;
      tctx.fillStyle = `hsla(${{hue}}, 70%, 55%, 0.85)`;
      tctx.fillRect(p.targetX, p.targetY, p.targetW, p.targetH);
      tctx.strokeStyle = 'rgba(255,255,255,0.6)';
      tctx.lineWidth = 2/ts;
      tctx.strokeRect(p.targetX+1, p.targetY+1, p.targetW-2, p.targetH-2);

      tctx.restore();
      tctx.restore();

      div.appendChild(tc);

      // Drag events from panel
      div.addEventListener('mousedown', (e) => startDragFromPanel(e, p));
      div.addEventListener('touchstart', (e) => startDragFromPanelTouch(e, p), {{passive:false}});
      piecesContainer.appendChild(div);
    }});
  }}

  buildThumbnails();

  // ===== DRAG STATE =====
  let draggingPiece = null;
  let dragX = 0, dragY = 0;
  let mistakeCount = 0;

  function startDragFromPanel(e, piece) {{
    e.preventDefault();
    if(piece.placed) return;
    draggingPiece = piece;
    piece.inPanel = false;
    const rect = canvas.getBoundingClientRect();
    dragX = e.clientX - rect.left;
    dragY = e.clientY - rect.top;
    piece.currentX = dragX - piece.targetW/2;
    piece.currentY = dragY - piece.targetH/2;
    piece.dragOffX = piece.targetW/2;
    piece.dragOffY = piece.targetH/2;
    render();
  }}

  function startDragFromPanelTouch(e, piece) {{
    e.preventDefault();
    if(piece.placed) return;
    const touch = e.touches[0];
    draggingPiece = piece;
    piece.inPanel = false;
    const rect = canvas.getBoundingClientRect();
    dragX = touch.clientX - rect.left;
    dragY = touch.clientY - rect.top;
    piece.currentX = dragX - piece.targetW/2;
    piece.currentY = dragY - piece.targetH/2;
    piece.dragOffX = piece.targetW/2;
    piece.dragOffY = piece.targetH/2;
    render();
  }}

  canvas.addEventListener('mousedown', (e) => {{
    const rect = canvas.getBoundingClientRect();
    const mx = (e.clientX - rect.left) * (W / rect.width);
    const my = (e.clientY - rect.top) * (H / rect.height);
    // Check if clicking on a floating piece
    for(let i=pieces.length-1; i>=0; i--) {{
      const p = pieces[i];
      if(p.placed || p.inPanel) continue;
      if(mx >= p.currentX && mx <= p.currentX+p.targetW &&
         my >= p.currentY && my <= p.currentY+p.targetH) {{
        draggingPiece = p;
        p.dragOffX = mx - p.currentX;
        p.dragOffY = my - p.currentY;
        dragX = mx; dragY = my;
        render();
        break;
      }}
    }}
  }});

  document.addEventListener('mousemove', (e) => {{
    if(!draggingPiece) return;
    const rect = canvas.getBoundingClientRect();
    dragX = (e.clientX - rect.left) * (W / rect.width);
    dragY = (e.clientY - rect.top) * (H / rect.height);
    draggingPiece.currentX = dragX - draggingPiece.dragOffX;
    draggingPiece.currentY = dragY - draggingPiece.dragOffY;
    render();
  }});

  document.addEventListener('mouseup', (e) => {{
    if(draggingPiece) {{
      trySnap(draggingPiece, dragX, dragY);
      draggingPiece = null;
      render();
    }}
  }});

  canvas.addEventListener('touchmove', (e) => {{
    e.preventDefault();
    if(!draggingPiece) return;
    const touch = e.touches[0];
    const rect = canvas.getBoundingClientRect();
    dragX = (touch.clientX - rect.left) * (W / rect.width);
    dragY = (touch.clientY - rect.top) * (H / rect.height);
    draggingPiece.currentX = dragX - draggingPiece.dragOffX;
    draggingPiece.currentY = dragY - draggingPiece.dragOffY;
    render();
  }}, {{passive: false}});

  document.addEventListener('touchend', (e) => {{
    if(draggingPiece) {{
      trySnap(draggingPiece, dragX, dragY);
      draggingPiece = null;
      render();
    }}
  }});

  // ===== SNAP LOGIC =====
  function trySnap(piece, dropX, dropY) {{
    const targetCenterX = piece.targetX + piece.targetW/2;
    const targetCenterY = piece.targetY + piece.targetH/2;
    const dist = Math.hypot(dropX - targetCenterX, dropY - targetCenterY);

    if(dist <= SNAP_DIST * (W/600)) {{
      // Snap!
      piece.currentX = piece.targetX;
      piece.currentY = piece.targetY;
      piece.placed = true;
      piece.inPanel = false;
      showSnapFeedback(dropX, dropY, true);
      updateThumb(piece.id);
      updateProgress();
      checkWin();
    }} else {{
      // Wrong placement
      mistakeCount++;
      showSnapFeedback(dropX, dropY, false);
      updateAccuracy();
      // Return to near center area (scattered)
      piece.currentX = tMinX + Math.random()*tW*0.6 + tW*0.1;
      piece.currentY = tMinY + Math.random()*tH*0.6 + tH*0.1;
      piece.inPanel = false;
    }}
  }}

  function showSnapFeedback(x, y, success) {{
    const fb = document.getElementById('snap-feedback');
    fb.textContent = success ? '✅' : '❌';
    fb.style.left = Math.min(x, W-40)+'px';
    fb.style.top = Math.max(y-30, 10)+'px';
    fb.style.display = 'block';
    fb.style.animation = 'none';
    fb.offsetHeight; // reflow
    fb.style.animation = 'floatUp 0.8s ease-out forwards';
    setTimeout(() => {{ fb.style.display = 'none'; }}, 800);
  }}

  function updateThumb(id) {{
    const el = document.getElementById('thumb-'+id);
    if(el) el.classList.add('placed');
  }}

  function updateProgress() {{
    const placed = pieces.filter(p => p.placed).length;
    document.getElementById('placed-count').textContent = placed;
    const pct = Math.round((placed / totalPieces) * 100);
    document.getElementById('progress-bar-fill').style.width = pct+'%';
    document.getElementById('progress-bar-fill2').style.width = pct+'%';
    document.getElementById('progress-text').textContent =
      placed === totalPieces ? '🎉 Selesai!' : `${{placed}}/${{totalPieces}} kepingan terpasang`;
  }}

  function updateAccuracy() {{
    const placed = pieces.filter(p => p.placed).length;
    const totalAttempts = placed + mistakeCount;
    const acc = totalAttempts > 0 ? Math.round((placed/totalAttempts)*100) : 100;
    document.getElementById('accuracy-display').textContent = acc+'%';
  }}

  function checkWin() {{
    const placed = pieces.filter(p => p.placed).length;
    if(placed >= totalPieces) {{
      const elapsed = Math.floor((Date.now() - START_TIME) / 1000);
      const m = Math.floor(elapsed/60).toString().padStart(2,'0');
      const s = (elapsed%60).toString().padStart(2,'0');
      document.getElementById('win-time').textContent = m+':'+s;
      document.getElementById('win-moves').textContent = mistakeCount + ' kesalahan';
      setTimeout(() => {{
        document.getElementById('win-overlay').classList.add('show');
      }}, 500);
    }}
  }}

  // ===== TIMER =====
  setInterval(() => {{
    const elapsed = Math.floor((Date.now() - START_TIME) / 1000);
    const m = Math.floor(elapsed/60).toString().padStart(2,'0');
    const s = (elapsed%60).toString().padStart(2,'0');
    document.getElementById('timer-display').textContent = m+':'+s;
  }}, 1000);

  // ===== RENDER =====
  function render() {{
    ctx.clearRect(0, 0, W, H);

    // 1. Draw background map (all regions faded)
    GEOJSON.features.forEach(f => {{
      if(f.properties.name === TARGET_NAME) return;
      const path = buildPath(f.geometry);
      ctx.fillStyle = 'rgba(80,100,140,0.25)';
      ctx.fill(path);
      ctx.strokeStyle = 'rgba(255,255,255,0.12)';
      ctx.lineWidth = 0.8;
      ctx.stroke(path);
    }});

    // 2. Draw target region outline (hint)
    ctx.save();
    ctx.setLineDash([6,3]);
    ctx.strokeStyle = 'rgba(255,215,0,0.5)';
    ctx.lineWidth = 2;
    ctx.stroke(targetPath);
    ctx.setLineDash([]);
    ctx.restore();

    // 3. Draw grid hints (ghost cells)
    for(let i=0; i<pieces.length; i++) {{
      const p = pieces[i];
      if(p.placed) continue;
      ctx.save();
      ctx.clip(targetPath);
      ctx.setLineDash([4,4]);
      ctx.strokeStyle = 'rgba(255,215,0,0.2)';
      ctx.lineWidth = 1;
      ctx.strokeRect(p.targetX, p.targetY, p.targetW, p.targetH);
      ctx.setLineDash([]);
      ctx.restore();
    }}

    // 4. Draw placed pieces
    pieces.forEach(p => {{
      if(!p.placed) return;
      ctx.save();
      ctx.clip(targetPath);
      const hue = (p.id * 37 + 180) % 360;
      ctx.fillStyle = `hsla(${{hue}}, 65%, 50%, 0.75)`;
      ctx.fillRect(p.targetX, p.targetY, p.targetW, p.targetH);
      ctx.strokeStyle = '#4CAF50';
      ctx.lineWidth = 2;
      ctx.strokeRect(p.targetX, p.targetY, p.targetW, p.targetH);
      ctx.restore();
    }});

    // 5. Draw floating (unplaced, not in panel) pieces
    pieces.forEach(p => {{
      if(p.placed || p.inPanel) return;
      ctx.save();
      // Clip the piece shape using offset
      const clipPath = new Path2D();
      // Create a shifted version of the target path for this cell
      ctx.beginPath();
      const dx = p.currentX - p.targetX;
      const dy = p.currentY - p.targetY;
      ctx.rect(p.currentX-1, p.currentY-1, p.targetW+2, p.targetH+2);
      ctx.clip();

      // Translate and draw target shape
      ctx.translate(dx, dy);
      ctx.clip(targetPath);

      const hue = (p.id * 37 + 180) % 360;
      const isDragging = (p === draggingPiece);
      ctx.fillStyle = `hsla(${{hue}}, 70%, ${{isDragging?65:55}}%, ${{isDragging?0.95:0.85}})`;
      ctx.fillRect(p.targetX, p.targetY, p.targetW, p.targetH);
      ctx.strokeStyle = isDragging ? '#ffd700' : 'rgba(255,255,255,0.7)';
      ctx.lineWidth = isDragging ? 3 : 1.5;
      ctx.strokeRect(p.targetX+1, p.targetY+1, p.targetW-2, p.targetH-2);
      ctx.restore();

      if(isDragging) {{
        // Glow
        ctx.save();
        ctx.shadowColor = '#ffd700';
        ctx.shadowBlur = 18;
        ctx.strokeStyle = 'rgba(255,215,0,0.7)';
        ctx.lineWidth = 2;
        ctx.strokeRect(p.currentX, p.currentY, p.targetW, p.targetH);
        ctx.restore();
      }}
    }});

    // 6. Draw target label
    ctx.fillStyle = 'rgba(255,215,0,0.9)';
    ctx.font = 'bold 11px Nunito, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(TARGET_NAME, targetCX, tMinY - 6);
  }}

  render();

  // ===== CONTROLS =====
  window.shufflePieces = function() {{
    pieces.forEach(p => {{
      if(p.placed) return;
      p.inPanel = false;
      p.currentX = tMinX + Math.random() * (tW * 0.7);
      p.currentY = tMinY + Math.random() * (tH * 0.7);
    }});
    render();
  }};

  window.showHint = function() {{
    // Flash target border
    let count = 0;
    const interval = setInterval(() => {{
      ctx.save();
      ctx.strokeStyle = count%2===0 ? '#ffd700' : 'transparent';
      ctx.lineWidth = 4;
      ctx.stroke(targetPath);
      ctx.restore();
      count++;
      if(count > 6) clearInterval(interval);
    }}, 200);
  }};

  window.resetPuzzle = function() {{
    pieces.forEach(p => {{
      p.placed = false;
      p.inPanel = true;
    }});
    mistakeCount = 0;
    document.getElementById('accuracy-display').textContent = '100%';
    buildThumbnails();
    updateProgress();
    render();
  }};

  window.autoSolve = function() {{
    let i = 0;
    const interval = setInterval(() => {{
      const unplaced = pieces.filter(p => !p.placed);
      if(unplaced.length === 0) {{
        clearInterval(interval);
        checkWin();
        return;
      }}
      const p = unplaced[0];
      p.placed = true;
      p.inPanel = false;
      p.currentX = p.targetX;
      p.currentY = p.targetY;
      updateThumb(p.id);
      updateProgress();
      render();
      i++;
    }}, 120);
  }};

  // Initial scatter of pieces
  shufflePieces();

}})();
</script>
</body>
</html>"""

    return html


# ==================== CSS RENDER ====================

st.markdown(get_background_image_html(SIDEBAR_BACKGROUND_URL), unsafe_allow_html=True)
st.markdown(get_footer_css(FOOTER_BACKGROUND_URL, st.session_state.footer_brightness), unsafe_allow_html=True)


# ==================== HALAMAN LOGIN NAMA ====================

if not st.session_state.name_submitted:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(
            "https://img.freepik.com/vektor-premium/peta-yang-digambar-tangan-dari-provinsi-jawa-timur-indonesia-desain-kartun-garis-sederhana-modern_242622-498.jpg",
            width=150
        )
        time_info = get_current_time_info()
        st.markdown(
            f"<div style='text-align:center;color:#666;font-size:14px;'>{time_info['hari']}, {time_info['tanggal']} | {time_info['jam']}</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<div style='text-align:center;margin:20px 0;'><h1>🧩 Sepiro Jawa Timur, Sampeyan? </h1>"
            "<p style='font-size:18px;color:#666;'>Game interaktif pembelajaran wilayah Jawa Timur!</p></div>",
            unsafe_allow_html=True
        )

        with st.form("name_form"):
            st.markdown("### 👤 Silahkan Masukkan Nama Kakak yaa...")
            name = st.text_input("Nama", placeholder="Contoh: Adi", max_chars=30)
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                submitted = st.form_submit_button("🚀 Mulai Bermain", use_container_width=True, type="primary")
            if submitted:
                if name.strip():
                    st.session_state.user_name = name.strip()
                    st.session_state.name_submitted = True
                    st.rerun()
                else:
                    st.error("❌ Nama tidak boleh kosong!")

        st.markdown("---")
        st.markdown(
            "<div style='text-align:center;color:#666;font-size:14px;'>"
            "<p>✨ Fitur: 🎮 Game | 📚 Belajar | 🧩 Puzzle | 🌋 Bromo 3D | 🏛️ Balaikota 3D | 🏆 Papan Skor | 🎵 Musik Latar</p></div>",
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <div style='
                text-align:center;
                margin-top:18px;
                padding:14px 18px;
                background: linear-gradient(135deg, #f8f9fa, #e9ecef);
                border-radius: 10px;
                border-top: 3px solid #667eea;
            '>
                <p style='
                    color:#555;
                    font-size:12px;
                    line-height:1.7;
                    margin:0;
                '>
                    © 2026 <strong>Program Pengabdian Masyarakat</strong> — Penguatan Geospasial Tentang Jawa Timur
                    Sejak Usia Dini Melalui Edukasi Gamifikasi Menggunakan Platform <em>"Pengetahuan Jatim"</em><br>
                    🏛️ Lab. <strong>Environmental, Infrastructure, and Information System (EIIS)</strong> ·
                    Dept. Perencanaan Wilayah &amp; Kota · Fak. Teknik · <strong>Universitas Brawijaya</strong>
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.stop()


# ==================== SIDEBAR ====================

with st.sidebar:
    st.image(
        "https://img.freepik.com/vektor-premium/peta-yang-digambar-tangan-dari-provinsi-jawa-timur-indonesia-desain-kartun-garis-sederhana-modern_242622-498.jpg",
        width=100
    )
    st.title("🧩 Pengetahuan Jatim")

    time_info = get_current_time_info()
    st.markdown(
        f"<div style='background:linear-gradient(135deg,#667eea,#764ba2);padding:8px;border-radius:10px;"
        f"margin-bottom:10px;text-align:center;'>"
        f"<p style='color:white;margin:0;font-size:12px;'>{time_info['hari']}, {time_info['tanggal']}</p>"
        f"<p style='color:white;margin:0;font-size:14px;font-weight:bold;'>⏰ {time_info['jam']}</p></div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='background:linear-gradient(135deg,#667eea,#764ba2);padding:10px;border-radius:10px;"
        f"margin-bottom:10px;text-align:center;'>"
        f"<p style='color:white;margin:0;'>👋 Halo Kak <strong>{st.session_state.user_name}</strong>!</p></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='color:rgba(255,255,255,0.7);font-size:11px;margin-bottom:2px;'>🎵 Kontrol Musik</p>",
        unsafe_allow_html=True
    )
    st.components.v1.html(
        get_backsound_html(st.session_state.music_volume),
        height=58,
        scrolling=False
    )

    st.markdown("---")

    menu_options = ["🎮 Game", "📚 Belajar", "🧩 Puzzle", "🌋 Bromo 3D", "🏛️ Balaikota 3D",
                    "🏆 Papan Skor", "⏱️ Statistik Waktu", "⚙️ Pengaturan", "ℹ️ Tentang"]
    selected_menu = st.radio("Menu", menu_options, index=0,
                             label_visibility="collapsed", key="main_navigation")

    # Derive clean page key for exact matching (strip emoji prefix)
    PAGE = selected_menu.split(" ", 1)[1] if " " in selected_menu else selected_menu

    st.markdown("---")
    if st.button("🔄 Ganti Nama", use_container_width=True):
        st.session_state.name_submitted = False
        st.rerun()
    st.markdown("---")

    if PAGE == "Game":
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
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Skor", st.session_state.score)
        with c2:
            st.metric("Soal", f"{st.session_state.total_questions}/{st.session_state.max_questions}")

        if st.session_state.game_started and not st.session_state.game_over:
            if st.session_state.game_start_time:
                dur = time.time() - st.session_state.game_start_time
                st.metric("⏱️ Waktu", format_duration(dur))
            if st.session_state.average_answer_time > 0:
                st.metric("⚡ Rata-rata", f"{st.session_state.average_answer_time:.1f} dtk")

        with st.expander("⚙️ Kesulitan"):
            diff = st.selectbox("Tingkat Kesulitan", ["Mudah", "Normal", "Sulit"],
                                index=["Mudah", "Normal", "Sulit"].index(st.session_state.difficulty),
                                key="game_difficulty")
            if diff != st.session_state.difficulty:
                st.session_state.difficulty = diff
                st.rerun()

    elif PAGE == "Puzzle":
        st.header("🧩 Puzzle Kontrol")
        st.markdown("**Pilih tingkat kesulitan:**")
        puzzle_diff = st.radio(
            "Kesulitan Puzzle",
            ["Pemula", "Mudah", "Normal", "Sulit"],
            index=["Pemula", "Mudah", "Normal", "Sulit"].index(st.session_state.puzzle_difficulty),
            key="puzzle_diff_radio",
            label_visibility="collapsed"
        )
        if puzzle_diff != st.session_state.puzzle_difficulty:
            st.session_state.puzzle_difficulty = puzzle_diff
            st.session_state.puzzle_started = False
            st.rerun()

        st.markdown("---")
        pieces_info = {"Pemula": "5 keping", "Mudah": "10 keping", "Normal": "25 keping", "Sulit": "38 keping"}
        desc_info = {
            "Pemula": "🌱 Cocok untuk pemula",
            "Mudah": "😊 Grid kecil, mudah disusun",
            "Normal": "⚡ Tantangan standar",
            "Sulit": "🔥 Banyak keping, butuh ketelitian"
        }
        st.info(f"**{puzzle_diff}** — {pieces_info[puzzle_diff]}\n\n{desc_info[puzzle_diff]}")

        st.markdown("---")
        st.markdown("**Pilih Wilayah:**")
        selected_region = st.selectbox(
            "Wilayah",
            wilayah_list,
            index=wilayah_list.index(st.session_state.puzzle_target_region) if st.session_state.puzzle_target_region in wilayah_list else 0,
            key="puzzle_region_select",
            label_visibility="collapsed"
        )
        st.session_state.puzzle_target_region = selected_region

        if st.button("🎲 Wilayah Acak", use_container_width=True):
            st.session_state.puzzle_target_region = random.choice(wilayah_list)
            st.session_state.puzzle_started = False
            st.rerun()

        if st.button("▶️ Mulai Puzzle", use_container_width=True, type="primary"):
            st.session_state.puzzle_started = True
            st.session_state.puzzle_start_time = time.time()
            st.rerun()

    elif PAGE == "Belajar":
        st.header("📚 Mode Belajar")
        st.markdown("Klik wilayah di peta untuk melihat informasi lengkap.")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total", len(wilayah_list))
        with c2:
            st.metric("Kab.", len(kab_list))
        with c3:
            st.metric("Kota", len(kota_list))

    elif PAGE == "Bromo 3D":
        st.header("🌋 Gunung Bromo 3D")
        st.markdown("Visualisasi interaktif Gunung Bromo.")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Ketinggian", "2.329 m")
        with c2:
            st.metric("Status", "Aktif")

    elif PAGE == "Balaikota 3D":
        st.header("🏛️ Balaikota Malang 3D")
        st.markdown("Visualisasi 3D interaktif Balaikota Malang.")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Kota", "Malang")
        with c2:
            st.metric("Teknologi", "Cesium 3D")

    elif PAGE == "Papan Skor":
        st.header("🏆 Papan Skor")
        st.selectbox("Filter level:", ["Semua Level", "Mudah", "Normal", "Sulit"],
                     key="scoreboard_level_filter")
        st.selectbox("Filter waktu:", ["Semua Waktu", "Hari Ini", "7 Hari Terakhir",
                                       "30 Hari Terakhir", "Bulan Ini"],
                     key="scoreboard_time_filter")
        sb = get_filtered_scoreboard(
            st.session_state.get("scoreboard_level_filter", "Semua Level"),
            st.session_state.get("scoreboard_time_filter", "Semua Waktu")
        )
        stats = get_scoreboard_stats(sb)
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Pemain", stats["total_pemain"])
        with c2:
            if sb:
                st.metric("Tertinggi", f"{stats['skor_tertinggi']}/{sb[0]['total_soal']}")

    elif PAGE == "Statistik Waktu":
        st.header("⏱️ Statistik Waktu")
        st.metric("Durasi Sesi", format_duration(get_session_duration()))
        if st.session_state.question_times:
            st.metric("Total Soal", len(st.session_state.question_times))
            st.metric("Rata-rata Jawab", f"{st.session_state.average_answer_time:.1f} dtk")
            fastest = min(st.session_state.question_times, key=lambda x: x["duration"])
            st.metric("⚡ Tercepat", f"{fastest['duration']:.1f} dtk (Soal {fastest['question_number']})")

    elif PAGE == "Pengaturan":
        st.header("⚙️ Pengaturan")
        new_max = st.slider("Jumlah Soal", min_value=5, max_value=20,
                            value=st.session_state.max_questions, step=5)
        if new_max != st.session_state.max_questions:
            st.session_state.max_questions = new_max
        st.markdown("---")
        st.markdown("### 🎨 Brightness Footer")
        new_br = st.slider("Brightness", min_value=0.3, max_value=1.0,
                           value=st.session_state.footer_brightness, step=0.05)
        if new_br != st.session_state.footer_brightness:
            st.session_state.footer_brightness = new_br
            st.rerun()
        st.markdown("---")
        st.markdown("### 🎵 Volume Musik")
        new_vol_sb = st.slider("Volume (%)", min_value=0, max_value=100,
                               value=st.session_state.music_volume, step=5,
                               key="sidebar_music_volume")
        if new_vol_sb != st.session_state.music_volume:
            st.session_state.music_volume = new_vol_sb
            st.rerun()
        st.caption("Gunakan tombol 🎵 di atas untuk play/pause musik")

    elif PAGE == "Tentang":
        st.header("ℹ️ Tentang")
        st.markdown("**Pengetahuan Tentang Kota & Kabupaten di Jawa Timur** v2.8.0\n\nAplikasi interaktif Pembelajaran Geospasial Jawa Timur.")

# Expose PAGE for main content area (re-derive outside sidebar scope)
PAGE = st.session_state.get("main_navigation", "🎮 Game")
PAGE = PAGE.split(" ", 1)[1] if " " in PAGE else PAGE


# ==================== KONTEN UTAMA ====================

# --- HALAMAN GAME ---
if PAGE == "Game":
    st.title("🧩 Tebak Bentuk Kota & Kabupaten di Jawa Timur")

    if st.session_state.game_started and not st.session_state.game_over:
        st.markdown(f"**Tingkat Kesulitan:** {st.session_state.difficulty} | "
                    f"**Soal:** {st.session_state.total_questions + 1}/{st.session_state.max_questions}")
        if st.session_state.game_start_time:
            dur = time.time() - st.session_state.game_start_time
            c1, c2, c3 = st.columns(3)
            with c1:
                st.info(f"⏱️ **Total:** {format_duration(dur)}")
            with c2:
                if st.session_state.question_start_time:
                    qd = time.time() - st.session_state.question_start_time
                    st.info(f"⚡ **Soal ini:** {qd:.1f} dtk")
            with c3:
                if st.session_state.average_answer_time > 0:
                    st.info(f"📊 **Rata-rata:** {st.session_state.average_answer_time:.1f} dtk")

# --- HALAMAN PUZZLE ---
elif PAGE == "Puzzle":
    st.title("🧩 Puzzle Peta Jawa Timur — Drag & Drop")

    # Info cards
    col_info1, col_info2, col_info3, col_info4 = st.columns(4)
    level_data = {
        "Pemula":  {"pieces": 5,  "color": "#4CAF50", "icon": "🌱"},
        "Mudah":   {"pieces": 10, "color": "#2196F3", "icon": "😊"},
        "Normal":  {"pieces": 25, "color": "#FF9800", "icon": "⚡"},
        "Sulit":   {"pieces": 38, "color": "#f44336", "icon": "🔥"},
    }
    for i, (lvl, info) in enumerate(level_data.items()):
        col = [col_info1, col_info2, col_info3, col_info4][i]
        with col:
            is_selected = (lvl == st.session_state.puzzle_difficulty)
            border = f"3px solid {info['color']}" if is_selected else "1px solid #ddd"
            bg = f"linear-gradient(135deg, {info['color']}22, {info['color']}11)" if is_selected else "#f8f9fa"
            st.markdown(
                f"""<div style='background:{bg};border:{border};border-radius:12px;
                padding:14px;text-align:center;'>
                <div style='font-size:1.8em;'>{info['icon']}</div>
                <div style='font-weight:900;font-size:1.1em;color:{"#333" if not is_selected else info["color"]};'>{lvl}</div>
                <div style='color:#666;font-size:0.85em;'>{info['pieces']} keping</div>
                {"<div style='color:"+info['color']+";font-size:0.75em;font-weight:700;'>▲ AKTIF</div>" if is_selected else ""}
                </div>""",
                unsafe_allow_html=True
            )

    st.markdown("---")

    if not st.session_state.puzzle_started:
        # Show selection UI
        st.markdown("### 🗺️ Pilih Wilayah & Mulai Puzzle")

        sel_col1, sel_col2 = st.columns([2, 1])
        with sel_col1:
            # Show mini map preview
            m_prev = folium.Map(location=[-7.5, 112.3], zoom_start=7, tiles=None)
            folium.TileLayer(
                tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                attr="Esri", name="Satellite"
            ).add_to(m_prev)

            target = st.session_state.puzzle_target_region or wilayah_list[0]

            def puzzle_style(feature):
                name = feature["properties"]["name"]
                if name == target:
                    return {"fillColor": "#FF6B35", "color": "#FF6B35", "weight": 3, "fillOpacity": 0.7}
                return {"fillColor": "#3388ff", "color": "#ffffff", "weight": 1, "fillOpacity": 0.2}

            folium.GeoJson(
                jatim_geojson,
                style_function=puzzle_style,
                tooltip=folium.GeoJsonTooltip(fields=["name"], aliases=["Wilayah:"]),
            ).add_to(m_prev)
            st_folium(m_prev, width=None, height=400, use_container_width=True, key="puzzle_preview_map")

        with sel_col2:
            st.markdown("#### ⚙️ Pengaturan Puzzle")

            new_diff = st.selectbox(
                "Tingkat Kesulitan",
                ["Pemula", "Mudah", "Normal", "Sulit"],
                index=["Pemula", "Mudah", "Normal", "Sulit"].index(st.session_state.puzzle_difficulty),
                key="puzzle_diff_main"
            )
            if new_diff != st.session_state.puzzle_difficulty:
                st.session_state.puzzle_difficulty = new_diff

            new_region = st.selectbox(
                "Pilih Wilayah",
                wilayah_list,
                index=wilayah_list.index(st.session_state.puzzle_target_region) if st.session_state.puzzle_target_region in wilayah_list else 0,
                key="puzzle_region_main"
            )
            st.session_state.puzzle_target_region = new_region

            cfg_sel = level_data[new_diff]
            st.markdown(
                f"""<div style='background:linear-gradient(135deg,{cfg_sel["color"]}33,{cfg_sel["color"]}11);
                border:2px solid {cfg_sel["color"]};border-radius:12px;padding:14px;margin:12px 0;text-align:center;'>
                <div style='font-size:2em;'>{cfg_sel["icon"]}</div>
                <div style='font-weight:900;font-size:1.2em;color:{cfg_sel["color"]};'>{new_diff}</div>
                <div style='color:#555;'>{cfg_sel["pieces"]} keping puzzle</div>
                </div>""",
                unsafe_allow_html=True
            )

            if st.button("▶️ MULAI PUZZLE!", use_container_width=True, type="primary"):
                st.session_state.puzzle_started = True
                st.session_state.puzzle_start_time = time.time()
                st.session_state.puzzle_target_region = new_region
                st.session_state.puzzle_difficulty = new_diff
                st.rerun()

            if st.button("🎲 Wilayah Acak", use_container_width=True):
                st.session_state.puzzle_target_region = random.choice(wilayah_list)
                st.rerun()

            # Info wilayah
            st.markdown("---")
            info = get_wilayah_info(new_region)
            with st.expander(f"ℹ️ Info {new_region}"):
                st.markdown(f"**📍 Geografis:** {info['geografis']}")
                st.markdown(f"**🛍️ Oleh-oleh:** {info['oleh_oleh']}")

    else:
        # PUZZLE IS ACTIVE
        target_region = st.session_state.puzzle_target_region or wilayah_list[0]
        difficulty = st.session_state.puzzle_difficulty
        piece_count = level_data[difficulty]["pieces"]

        # Header info
        h1, h2, h3 = st.columns(3)
        with h1:
            st.markdown(
                f"<div style='background:linear-gradient(135deg,#667eea,#764ba2);padding:10px;border-radius:10px;text-align:center;color:white;'>"
                f"<strong>🗺️ {target_region}</strong></div>",
                unsafe_allow_html=True
            )
        with h2:
            st.markdown(
                f"<div style='background:linear-gradient(135deg,{level_data[difficulty]['color']},{level_data[difficulty]['color']}bb);padding:10px;border-radius:10px;text-align:center;color:white;'>"
                f"<strong>{level_data[difficulty]['icon']} {difficulty} — {piece_count} keping</strong></div>",
                unsafe_allow_html=True
            )
        with h3:
            if st.button("⛔ Keluar Puzzle", use_container_width=True):
                st.session_state.puzzle_started = False
                st.rerun()

        st.markdown("")

        # Render the puzzle HTML component
        puzzle_html = get_puzzle_html(
            jatim_geojson,
            target_region,
            difficulty,
            piece_count,
            int(st.session_state.puzzle_start_time * 1000) if st.session_state.puzzle_start_time else 0
        )
        st.components.v1.html(puzzle_html, height=780, scrolling=True)

        st.markdown("---")
        tip_col1, tip_col2 = st.columns(2)
        with tip_col1:
            st.info(
                "💡 **Cara Bermain:**\n"
                "1. Seret kepingan dari panel kanan ke area peta\n"
                "2. Tempatkan di posisi yang tepat\n"
                "3. Kepingan akan 'snap' otomatis jika dekat posisi yang benar\n"
                "4. Susun semua kepingan untuk menyelesaikan puzzle!"
            )
        with tip_col2:
            info = get_wilayah_info(target_region)
            st.success(
                f"📖 **{target_region}**\n\n"
                f"{info['geografis'][:120]}..."
            )

# --- HALAMAN BELAJAR ---
elif PAGE == "Belajar":
    st.title("📚 Mode Belajar Wilayah Jawa Timur")
    st.markdown("**Klik wilayah pada peta** untuk melihat informasi lengkap!")

# --- HALAMAN BROMO ---
elif PAGE == "Bromo 3D":
    st.title("🌋 Gunung Bromo - Visualisasi 3D Interaktif")
    cl, cr = st.columns([2, 1])
    with cl:
        st.markdown("### Model 3D Gunung Bromo")
        st.components.v1.html("""
        <div style="width:100%;height:600px;position:relative;border-radius:10px;overflow:hidden;">
            <iframe
                title="Mount Bromo"
                frameborder="0" allowfullscreen
                mozallowfullscreen="true" webkitallowfullscreen="true"
                src="https://sketchfab.com/models/72f1c983ba4040eab89d75eb2b0d3e32/embed?autostart=1&ui_controls=1&ui_infos=1"
                style="width:100%;height:100%;position:absolute;top:0;left:0;">
            </iframe>
        </div>
        """, height=620)
    with cr:
        st.markdown("### 📍 Informasi Detail")
        st.markdown("""
        **Nama:** Gunung Bromo
        **Tinggi:** 2.329 meter
        **Koordinat:** 7°56′30″S 112°57′00″E
        **Jenis:** Stratovolcano
        **Status:** Aktif
        """)
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Ketinggian", "2.329 m")
        with c2:
            st.metric("Status", "Aktif")
        with st.expander("📖 Sejarah & Keunikan"):
            st.markdown("""
            Gunung Bromo terbentuk dari letusan gunung berapi purba.
            Nama "Bromo" berasal dari kata "Brahma" (dewa Hindu).

            - Kawah berdiameter ±800 meter
            - Lautan pasir seluas 5.250 hektar
            - Tempat upacara Kasada masyarakat Tengger
            """)
        with st.expander("🎫 Tips Kunjungan"):
            st.markdown("""
            **Waktu terbaik:** Mei – Oktober
            **Akses:** ±3-4 jam dari Surabaya
            **Tiket masuk:** Rp 29.000–34.000
            """)

# --- HALAMAN BALAIKOTA MALANG 3D ---
elif PAGE == "Balaikota 3D":
    st.title("🏛️ Balaikota Malang - Visualisasi 3D Interaktif")

    cl, cr = st.columns([2, 1])

    with cl:
        st.markdown("### 🗺️ Model 3D Balaikota Malang")
        st.markdown(
            "<div style='background:#e8f4fd;padding:10px;border-radius:8px;margin-bottom:10px;"
            "border-left:4px solid #0066cc;font-size:13px;color:#333;'>"
            "💡 <strong>Tips:</strong> Gunakan mouse untuk memutar, scroll untuk zoom, "
            "dan klik kanan + drag untuk geser tampilan 3D.</div>",
            unsafe_allow_html=True
        )
        SANDCASTLE_URL = "https://sandcastle.cesium.com/standalone.html#c=jZJvb9owEMa/ipUXVZA2p4G2KhqtxmCjQRBEyWiDIk3GMWBi7NQ2lGTqd5/zh62dtmmvLPt+99zdc3YcMJCIa9Ajiu53wxlAGBOlgBYgE3sJqOAAKUW0injFQE9wGJMV2jPdLeFAJISDGxBZJBtulgNMJ3Tofc0916ee8vj9Je55V16SPs57wzY00FM8SAzkNcMgOZ8Ec7qYnTfD5mIzCqbu4iHUk76f+JnL/P70Ypzj3M9jNg4wHfWG6cKIjYOw6ffHRtzfLlufGM68qwdTHLe8guFhNowLNnyc0sn2s+vn3Qt/uz5OAtaGyZfD/bzVPzbDRM7zULa/Pb5funfr6+l8sF0trikdNf0gu7sLRWR9iDgWXGlwoOSZSDMmJ8+1XXBevtmRhct7T3CNKCcyshomL+JaZuB7xAGoJDRlxFhpNNAzoifTYXW0+kEVhispdsbkbmG7F9vNS/eyfVEIgroJqDDhBKaS7qimB6IgimO7Vq/AqkCN50LsAvEaKBDHAd00ZRnQGwLqhQKlM0YAXQGTTY5UFXs/tU+OWiJluq+FYPkxYPVcVjV5dnGC02hG1vgR2xXTAGdn/whD89n+Azl9vlnRaqOAG5XJ4Gdj1RRvVvXa5DLzr4rlJC8RfwEYabwBNpFSyMavRQpGIBPr+t3gBrbeWZ2y6m1BfaS7VEgN9pLZEDqa7FKGNFHOco8T0x9WqsjrOKeUTkwPgMY3f/hJADPjs4ms9ozNaE4i67bjGP5NGhMopnw9ORDJUGaQoo3Oxr0dVQEIYccx16Lo77laCLZE8pXuDw"

        st.components.v1.html(
            f"""
            <!DOCTYPE html>
            <html>
            <head>
              <meta charset="utf-8">
              <style>
                html, body {{
                  margin: 0; padding: 0;
                  width: 100%; height: 100%;
                  overflow: hidden;
                  background: #000;
                }}
                iframe {{
                  width: 100%;
                  height: 640px;
                  border: none;
                  display: block;
                  border-radius: 10px;
                }}
              </style>
            </head>
            <body>
              <iframe
                src="{SANDCASTLE_URL}"
                allowfullscreen
                allow="fullscreen"
                sandbox="allow-scripts allow-same-origin allow-popups allow-forms"
              ></iframe>
            </body>
            </html>
            """,
            height=660,
            scrolling=False
        )

    with cr:
        st.markdown("### 📍 Informasi Balaikota")
        st.markdown(
            "<div style='background:linear-gradient(135deg,#667eea,#764ba2);"
            "padding:15px;border-radius:12px;color:white;margin-bottom:15px;'>"
            "<h4 style='margin:0 0 8px 0;color:#ffd700;'>🏛️ Balaikota Malang</h4>"
            "<p style='margin:3px 0;font-size:13px;'>📍 Jl. Tugu No.1, Klojen</p>"
            "<p style='margin:3px 0;font-size:13px;'>🏙️ Kota Malang, Jawa Timur</p>"
            "<p style='margin:3px 0;font-size:13px;'>🇮🇩 Indonesia</p>"
            "</div>",
            unsafe_allow_html=True
        )

        c1, c2 = st.columns(2)
        with c1:
            st.metric("Kota", "Malang")
            st.metric("Gaya", "Kolonial")
        with c2:
            st.metric("Dibangun", "1929")
            st.metric("Teknologi", "Cesium")

        with st.expander("📖 Sejarah & Arsitektur", expanded=True):
            st.markdown("""
            Balaikota Malang dibangun pada masa kolonial Belanda tahun **1929** dengan
            arsitektur bergaya **Art Deco** dan Neo-Klasik yang khas.

            **Ciri Arsitektur:**
            - Fasad simetris dengan pilar-pilar besar
            - Atap pelana tinggi khas bangunan kolonial
            - Ornamen detail khas era 1920-an
            - Taman depan yang tertata rapi

            **Fungsi Saat Ini:**
            - Kantor Walikota Malang
            - Pusat pemerintahan Kota Malang
            - Objek wisata sejarah dan arsitektur
            """)

        with st.expander("🎫 Info Kunjungan"):
            st.markdown("""
            **Lokasi:** Jl. Tugu No.1, Malang
            **Akses:** ±5 menit dari Alun-alun Kota Malang
            **Transportasi:** Angkot, ojek online, atau jalan kaki dari pusat kota
            **Jam Buka:** Senin–Jumat, 08.00–16.00 WIB
            **Tiket:** Gratis (area taman depan)
            """)

        with st.expander("🌐 Tentang Visualisasi Cesium"):
            st.markdown("""
            Visualisasi ini menggunakan **CesiumJS**, platform 3D geospatial
            berbasis WebGL untuk menampilkan model bangunan dalam lingkungan
            peta 3D yang interaktif.

            **Kontrol:**
            - 🖱️ **Klik kiri + drag** → Putar tampilan
            - 🖱️ **Scroll** → Zoom in/out
            - 🖱️ **Klik kanan + drag** → Geser peta
            - 🖱️ **Double klik** → Fokus ke titik
            """)

# --- HALAMAN PAPAN SKOR ---
elif PAGE == "Papan Skor":
    st.title("🏆 Papan Skor Pemain")
    st.info("ℹ️ Papan skor tersimpan selama sesi berlangsung. Refresh halaman akan mereset data.")

    lf = st.session_state.get("scoreboard_level_filter", "Semua Level")
    tf = st.session_state.get("scoreboard_time_filter", "Semua Waktu")
    scoreboard = get_filtered_scoreboard(lf, tf)
    stats = get_scoreboard_stats(scoreboard)

    st.info(f"📊 Menampilkan: **{lf}** | **{tf}**")

    if scoreboard:
        rows = []
        for i, p in enumerate(scoreboard[:10], 1):
            icon = {1: "👑", 2: "🥈", 3: "🥉"}.get(i, f"{i}.")
            nm = p.get("nama", "Unknown")
            if nm == st.session_state.user_name:
                nm = f"⭐ {nm} (Kamu)"
            dur = p.get("durasi", {}).get("format", "-") if p.get("durasi") else "-"
            rows.append({
                "Peringkat": icon, "Nama": nm,
                "Skor": f"{p.get('skor',0)}/{p.get('total_soal',0)}",
                "Persentase": f"{p.get('persentase',0)}%",
                "Level": p.get("level", "-"),
                "Durasi": dur,
                "Tanggal": (p.get("tanggal", "")[:10] if p.get("tanggal") else "")
            })
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("🏆 Juara 1", scoreboard[0].get("nama", "-"))
        with c2:
            st.metric("⭐ Tertinggi", f"{stats['skor_tertinggi']}/{scoreboard[0].get('total_soal',0)}")
        with c3:
            st.metric("📊 Rata-rata", str(stats["rata_rata"]))
        with c4:
            st.metric("🎯 Level Populer", stats["level_populer"])
        if stats["waktu_tercepat"]:
            st.success(f"⚡ Waktu Tercepat: {stats['waktu_tercepat']['format']} oleh {stats['waktu_tercepat']['nama']}")
    else:
        st.info("Belum ada skor. Mainkan game dulu!")

    st.markdown("---")
    st.markdown(f"### 📝 Skor Kakak: **{st.session_state.user_name}**")
    st.markdown(f"**Skor:** {st.session_state.score}/{st.session_state.max_questions} (Level: {st.session_state.difficulty})")
    if st.session_state.total_game_duration > 0:
        st.markdown(f"**Waktu:** {format_duration(st.session_state.total_game_duration)}")

    if st.session_state.score > 0 and not st.session_state.score_saved:
        if st.button("💾 Simpan Skor ke Papan Skor", use_container_width=True, type="primary"):
            if not st.session_state.game_end_time:
                st.session_state.game_end_time = time.time()
            end_game_timer()
            if add_score(st.session_state.user_name, st.session_state.score,
                         st.session_state.difficulty, st.session_state.max_questions,
                         st.session_state.game_start_time, st.session_state.game_end_time):
                st.session_state.score_saved = True
                st.success("✅ Skor berhasil disimpan!")
                st.rerun()
            else:
                st.error("❌ Gagal menyimpan skor.")
    elif st.session_state.score_saved:
        st.success("✅ Skor sudah disimpan!")

    with st.expander("🛠️ Reset Papan Skor (Admin)"):
        st.warning("⚠️ Akan menghapus semua data skor sesi ini!")
        if st.button("🗑️ Reset Semua Skor", use_container_width=True):
            st.session_state.scoreboard_data = []
            st.success("✅ Papan skor direset!")
            st.rerun()

# --- HALAMAN STATISTIK WAKTU ---
elif PAGE == "Statistik Waktu":
    st.title("⏱️ Statistik Waktu")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Durasi Sesi", format_duration(get_session_duration()))
    with c2:
        if st.session_state.total_game_duration > 0:
            st.metric("Durasi Game", format_duration(st.session_state.total_game_duration))
        elif st.session_state.game_start_time and not st.session_state.game_end_time:
            dur = time.time() - st.session_state.game_start_time
            st.metric("Durasi Game", format_duration(dur))
        else:
            st.metric("Durasi Game", "-")
    with c3:
        st.metric("Total Soal", st.session_state.total_questions)

    if st.session_state.question_times:
        df_t = pd.DataFrame(st.session_state.question_times)
        df_t["waktu"] = df_t["duration"].apply(lambda x: f"{x:.1f} dtk")
        df_t["status"] = df_t["correct"].apply(lambda x: "✅ Benar" if x else "❌ Salah")
        st.dataframe(df_t[["question_number", "waktu", "status"]],
                     column_config={"question_number": "Soal", "waktu": "Waktu", "status": "Hasil"},
                     hide_index=True, use_container_width=True)
        st.markdown("### 📈 Grafik Waktu Menjawab")
        st.line_chart(pd.DataFrame({"Soal": df_t["question_number"],
                                    "Waktu (dtk)": df_t["duration"]}).set_index("Soal"))
    else:
        st.info("Belum ada data. Mulai game untuk melihat statistik waktu.")

# --- HALAMAN PENGATURAN ---
elif PAGE == "Pengaturan":
    st.title("⚙️ Pengaturan Aplikasi")
    t1, t2, t3 = st.tabs(["🎮 Game", "🎨 Tampilan & Musik", "⏱️ Waktu"])
    with t1:
        c1, c2 = st.columns(2)
        with c1:
            new_max = st.number_input("Maksimum Soal", min_value=5, max_value=30,
                                      value=st.session_state.max_questions, key="s_max")
        with c2:
            new_diff = st.selectbox("Kesulitan", ["Mudah", "Normal", "Sulit"],
                                    index=["Mudah", "Normal", "Sulit"].index(st.session_state.difficulty),
                                    key="s_diff")
        if st.button("💾 Simpan Pengaturan Game", use_container_width=True):
            st.session_state.max_questions = new_max
            st.session_state.difficulty = new_diff
            st.success("✅ Pengaturan game disimpan!")

    with t2:
        st.markdown("### 🎨 Tampilan")
        br = st.slider("Brightness Footer", 0.3, 1.0, st.session_state.footer_brightness, 0.05,
                       key="settings_brightness")
        if br != st.session_state.footer_brightness:
            st.session_state.footer_brightness = br
            st.rerun()

        st.markdown("---")
        st.markdown("### 🎵 Pengaturan Musik Latar")
        st.markdown(
            "<div style='background:#f0f2f6;padding:15px;border-radius:10px;margin-bottom:10px;'>"
            "<p style='margin:0;font-size:14px;color:#555;'>🎵 Musik latar berjalan otomatis saat "
            "aplikasi dibuka. Gunakan tombol <strong>🎵 Musik On/Off</strong> di sidebar "
            "(bagian atas, bawah nama Anda) untuk pause/play musik kapan saja.</p></div>",
            unsafe_allow_html=True
        )

        new_vol = st.slider(
            "🔊 Volume Musik (%)",
            min_value=0, max_value=100,
            value=st.session_state.music_volume,
            step=5,
            key="settings_music_volume",
            help="Geser untuk mengatur volume musik latar."
        )
        if new_vol != st.session_state.music_volume:
            st.session_state.music_volume = new_vol
            st.info("⚠️ Klik 'Simpan & Terapkan Volume' untuk menerapkan perubahan.")

        vol_pct = st.session_state.music_volume
        if vol_pct == 0:
            vol_label = "🔇 Mute"
        elif vol_pct <= 30:
            vol_label = "🔈 Rendah"
        elif vol_pct <= 70:
            vol_label = "🔉 Sedang"
        else:
            vol_label = "🔊 Tinggi"

        st.markdown(
            f"<div style='background:linear-gradient(135deg,#667eea,#764ba2);padding:12px;"
            f"border-radius:8px;text-align:center;color:white;font-weight:bold;'>"
            f"{vol_label} — Volume: {vol_pct}%</div>",
            unsafe_allow_html=True
        )

        if st.button("💾 Simpan & Terapkan Volume", use_container_width=True, type="primary"):
            st.session_state.music_volume = new_vol
            st.success(f"✅ Volume disimpan: {new_vol}%. Musik akan reload otomatis.")
            st.rerun()

    with t3:
        st.checkbox("Tampilkan timer di game", value=True, key="s_timer")
        st.info("Pengaturan waktu aktif secara default.")

# --- HALAMAN TENTANG ---
elif PAGE == "Tentang":
    st.title("ℹ️ Tentang Aplikasi")

    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("""
        ### Pengetahuan Tentang Kota & Wilayah di Jawa Timur

        Aplikasi interaktif untuk mempelajari bentuk kota dan kabupaten di Jawa Timur.

        **Fitur:**
        - 🧩 Tebak bentuk kota & wilayah dari peta
        - 📚 Mode belajar dengan info wilayah
        - 🧩 **Puzzle Drag & Drop** — 4 tingkat kesulitan (Pemula/Mudah/Normal/Sulit)
        - 🌋 Visualisasi 3D Gunung Bromo
        - 🏛️ Visualisasi 3D Balaikota Malang (Cesium)
        - 🏆 Papan skor sesi
        - ⏱️ Statistik waktu bermain
        - 🎵 Musik latar otomatis (tombol play/pause di sidebar)
        - 🎈 Efek balon kejutan untuk nilai sempurna!

        **Teknologi:**
        - Streamlit, Folium, streamlit-folium
        - GeoJSON data wilayah
        - HTML5 Canvas Puzzle Engine
        - Sketchfab embed 3D (Bromo)
        - CesiumJS 3D Geospatial (Balaikota)
        - YouTube IFrame API (backsound)
        """)
    with c2:
        st.image("https://img.freepik.com/vektor-premium/peta-yang-digambar-tangan-dari-provinsi-jawa-timur-indonesia-desain-kartun-garis-sederhana-modern_242622-498.jpg")
        st.markdown("**Versi:** 2.8.0")
        st.markdown("**Musik:** 🎵 Aktif (YouTube)")

    st.markdown("---")

    st.markdown(
        "<h2 style='text-align:center;color:#0066cc;margin-bottom:6px;'>👨‍💻 Tim Pengembang Aplikasi</h2>"
        "<p style='text-align:center;color:#666;font-size:14px;margin-bottom:24px;'>"
        "Dikembangkan oleh tim Departemen Perencanaan Wilayah dan Kota, Universitas Brawijaya</p>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='text-align:center;margin-bottom:8px;'>"
        "<span style='background:linear-gradient(135deg,#ffd700,#ffaa00);color:#333;"
        "padding:4px 20px;border-radius:20px;font-weight:bold;font-size:13px;'>👑 KETUA</span>"
        "</div>",
        unsafe_allow_html=True
    )

    k1, k2, k3 = st.columns([1, 2, 1])
    with k2:
        st.markdown(
            """
            <div style='background:linear-gradient(135deg,#667eea,#764ba2);
                        border-radius:16px;padding:24px;text-align:center;
                        box-shadow:0 6px 24px rgba(102,126,234,0.35);
                        margin-bottom:20px;'>
              <img src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4q4OFNy-m3dc68a8SC7Nmo1UZn7N_p8QU7Q&s'
                   style='width:120px;height:120px;border-radius:50%;
                          object-fit:cover;border:4px solid #ffd700;
                          box-shadow:0 4px 12px rgba(0,0,0,0.3);
                          margin-bottom:14px;'>
              <h3 style='color:#ffd700;margin:0 0 4px 0;font-size:17px;'>
                Adipandang Yudono, S.Si., MURP., PhD
              </h3>
              <p style='color:rgba(255,255,255,0.85);margin:0 0 12px 0;font-size:13px;
                        font-style:italic;'>Ketua Tim Pengembang</p>
              <div style='display:flex;flex-wrap:wrap;justify-content:center;gap:6px;'>
                <span style='background:rgba(255,215,0,0.2);color:#ffd700;
                             padding:3px 10px;border-radius:12px;font-size:11px;
                             border:1px solid rgba(255,215,0,0.4);'>🖥️ Lead Developer</span>
                <span style='background:rgba(255,215,0,0.2);color:#ffd700;
                             padding:3px 10px;border-radius:12px;font-size:11px;
                             border:1px solid rgba(255,215,0,0.4);'>🏗️ Architecture System</span>
                <span style='background:rgba(255,215,0,0.2);color:#ffd700;
                             padding:3px 10px;border-radius:12px;font-size:11px;
                             border:1px solid rgba(255,215,0,0.4);'>🎨 UI/UX</span>
                <span style='background:rgba(255,215,0,0.2);color:#ffd700;
                             padding:3px 10px;border-radius:12px;font-size:11px;
                             border:1px solid rgba(255,215,0,0.4);'>📜 Script</span>
                <span style='background:rgba(255,215,0,0.2);color:#ffd700;
                             padding:3px 10px;border-radius:12px;font-size:11px;
                             border:1px solid rgba(255,215,0,0.4);'>🗺️ GIS Engineer</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        "<div style='text-align:center;margin-bottom:16px;'>"
        "<span style='background:linear-gradient(135deg,#43b89c,#1a8f6f);color:white;"
        "padding:4px 20px;border-radius:20px;font-weight:bold;font-size:13px;'>👥 ANGGOTA</span>"
        "</div>",
        unsafe_allow_html=True
    )

    a1, a2 = st.columns(2)

    with a1:
        st.markdown(
            """
            <div style='background:linear-gradient(135deg,#1a8f6f,#43b89c);
                        border-radius:16px;padding:22px;text-align:center;
                        box-shadow:0 6px 20px rgba(67,184,156,0.3);
                        height:100%;'>
              <img src='https://kanal24.co.id/wp-content/uploads/2024/06/WhatsApp-Image-2024-06-07-at-11.35.24-AM-1024x576.jpeg'
                   style='width:110px;height:110px;border-radius:50%;
                          object-fit:cover;object-position:top;
                          border:4px solid rgba(255,255,255,0.6);
                          box-shadow:0 4px 12px rgba(0,0,0,0.25);
                          margin-bottom:12px;'>
              <h4 style='color:white;margin:0 0 4px 0;font-size:15px;line-height:1.3;'>
                Fauzul Rizal Sutikno,<br>S.T., M.T., Ph.D
              </h4>
              <p style='color:rgba(255,255,255,0.8);margin:0 0 12px 0;
                        font-size:12px;font-style:italic;'>Anggota 1</p>
              <span style='background:rgba(255,255,255,0.2);color:white;
                           padding:4px 12px;border-radius:12px;font-size:11px;
                           border:1px solid rgba(255,255,255,0.3);'>
                🏙️ Participatory Planning
              </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with a2:
        st.markdown(
            """
            <div style='background:linear-gradient(135deg,#e05c8a,#c0396a);
                        border-radius:16px;padding:22px;text-align:center;
                        box-shadow:0 6px 20px rgba(192,57,106,0.3);
                        height:100%;'>
              <img src='https://0.academia-photos.com/12624073/3599023/4222310/s200_mustika.anggraeni.jpg'
                   style='width:110px;height:110px;border-radius:50%;
                          object-fit:cover;object-position:top;
                          border:4px solid rgba(255,255,255,0.6);
                          box-shadow:0 4px 12px rgba(0,0,0,0.25);
                          margin-bottom:12px;'>
              <h4 style='color:white;margin:0 0 4px 0;font-size:15px;line-height:1.3;'>
                Dr. (Cand.) Mustika Anggraeni,<br>S.T., M.Si.
              </h4>
              <p style='color:rgba(255,255,255,0.8);margin:0 0 12px 0;
                        font-size:12px;font-style:italic;'>Anggota 2</p>
              <span style='background:rgba(255,255,255,0.2);color:white;
                           padding:4px 12px;border-radius:12px;font-size:11px;
                           border:1px solid rgba(255,255,255,0.3);'>
                🌿 Environmental Planning
              </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<div style='text-align:center;background:#f8f9fa;padding:12px;border-radius:10px;"
        "border:1px solid #dee2e6;color:#666;font-size:13px;'>"
        "🏛️ <strong>Departemen Perencanaan Wilayah dan Kota</strong> · "
        "Fakultas Teknik · Universitas Brawijaya · Malang, Jawa Timur"
        "</div>",
        unsafe_allow_html=True
    )


# ==================== PETA (GAME & BELAJAR) ====================

if (PAGE == "Game") or PAGE == "Belajar":
    if PAGE == "Belajar":
        col_map, col_info = st.columns([2, 1])
    else:
        col_map = st.container()
        col_info = None

    map_container = col_map if PAGE == "Belajar" else st.container()

    with map_container:
        m = folium.Map(location=[-7.5, 112.3], zoom_start=8,
                       tiles=None, control_scale=True, prefer_canvas=True)
        folium.TileLayer(
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Esri", name="Satellite", overlay=False, control=False
        ).add_to(m)

        def style_function(feature):
            name = feature["properties"]["name"]
            if PAGE == "Belajar":
                return {"fillColor": "#33cc33", "color": "#ffffff",
                        "weight": 1.5, "fillOpacity": 0.5}
            if (st.session_state.game_started and not st.session_state.game_over
                    and name == st.session_state.current_region):
                return {"fillColor": "#ff0000", "color": "#ff0000",
                        "weight": 3, "fillOpacity": 0.7}
            return {
                "fillColor": "#3388ff" if st.session_state.game_started else "#cccccc",
                "color": "#ffffff", "weight": 1.5,
                "fillOpacity": 0.3 if st.session_state.game_started else 0.1
            }

        if PAGE == "Belajar":
            folium.GeoJson(
                jatim_geojson,
                name="Wilayah Jatim",
                style_function=style_function,
                tooltip=folium.GeoJsonTooltip(
                    fields=["name"], aliases=["Wilayah:"],
                    style="background-color:white;color:#333;font-weight:bold;padding:5px;"
                ),
                highlight_function=lambda x: {
                    "fillColor": "#ffaa00", "color": "#ffaa00",
                    "weight": 3, "fillOpacity": 0.7
                }
            ).add_to(m)
        else:
            folium.GeoJson(
                jatim_geojson,
                name="Wilayah Jatim",
                style_function=style_function,
            ).add_to(m)

        map_data = st_folium(m, width=None, height=500, use_container_width=True,
                             key="belajar_map" if PAGE == "Belajar" else "game_map")

        if PAGE == "Belajar" and map_data:
            clicked = map_data.get("last_active_drawing")
            if clicked and "properties" in clicked and "name" in clicked["properties"]:
                clicked_name = clicked["properties"]["name"]
                if clicked_name != st.session_state.selected_wilayah_info:
                    st.session_state.selected_wilayah_info = clicked_name
                    st.rerun()

        if PAGE == "Game" and not st.session_state.game_started and not st.session_state.game_over:
            if st.button("🎮 Mulai Game", use_container_width=True, type="primary"):
                reset_game()
                st.rerun()

    # Panel info wilayah (mode Belajar)
    if PAGE == "Belajar" and col_info is not None:
        with col_info:
            st.markdown("## 📋 Info Wilayah")
            if st.session_state.selected_wilayah_info:
                wil = st.session_state.selected_wilayah_info
                info = get_wilayah_info(wil)
                st.markdown(
                    f"<div style='background:#f0f2f6;padding:15px;border-radius:10px;margin-bottom:15px;'>"
                    f"<h3 style='color:#0066cc;margin-top:0;'>📍 {wil}</h3></div>",
                    unsafe_allow_html=True
                )
                tabs = st.tabs(["🗺️ Geografis", "👥 Demografi", "🎭 Budaya", "✨ Keunikan", "🛍️ Oleh-oleh"])
                with tabs[0]: st.markdown(info["geografis"])
                with tabs[1]: st.markdown(info["demografi"])
                with tabs[2]: st.markdown(info["budaya"])
                with tabs[3]: st.markdown(info["keunikan"])
                with tabs[4]: st.markdown(info["oleh_oleh"])
                if st.button("🔄 Klik wilayah lain", use_container_width=True):
                    st.session_state.selected_wilayah_info = None
                    st.rerun()
            else:
                st.markdown(
                    "<div style='background:#e8f4fd;padding:20px;border-radius:10px;text-align:center;"
                    "border:2px dashed #0066cc;'>"
                    "<h4 style='color:#0066cc;'>👆 Klik Wilayah di Peta</h4>"
                    "<p style='color:#666;'>Klik wilayah untuk melihat informasi lengkap!</p></div>",
                    unsafe_allow_html=True
                )
                with st.expander("📌 Atau pilih dari daftar"):
                    for region in ["Kabupaten Banyuwangi", "Kabupaten Malang", "Kota Surabaya",
                                   "Kota Batu", "Kota Mojokerto"]:
                        if st.button(region, key=f"quick_{region}"):
                            st.session_state.selected_wilayah_info = region
                            st.rerun()

    # ==================== AREA GAME ====================
    if PAGE == "Game":
        st.markdown("---")

        if st.session_state.game_over:
            end_game_timer()
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                is_perfect = (st.session_state.score == st.session_state.max_questions)

                if is_perfect or st.session_state.show_perfect_balloon:
                    st.balloons()
                    st.markdown(get_perfect_score_markdown_effect(), unsafe_allow_html=True)
                    st.components.v1.html(get_balloon_effect_html(), height=340, scrolling=False)
                    st.session_state.show_perfect_balloon = False

                st.markdown("## 🎮 Game Selesai!")
                st.markdown(f"### Skor Akhir: **{st.session_state.score}/{st.session_state.max_questions}**")
                if st.session_state.total_game_duration > 0:
                    st.info(f"⏱️ **Total Waktu:** {format_duration(st.session_state.total_game_duration)}")
                if st.session_state.average_answer_time > 0:
                    st.info(f"⚡ **Rata-rata Jawab:** {st.session_state.average_answer_time:.1f} dtk")

                if is_perfect:
                    st.markdown("### 🏆 Selamat! Nilai Sempurna!")
                    if st.session_state.question_times:
                        fastest = min(st.session_state.question_times, key=lambda x: x["duration"])
                        st.success(f"⚡ **Tercepat:** Soal {fastest['question_number']} dalam {fastest['duration']:.1f} dtk!")
                elif st.session_state.score >= 7:
                    st.markdown("### 👍 Bagus! Terus belajar!")
                elif st.session_state.score >= 5:
                    st.markdown("### 📚 Lumayan, coba lagi!")
                else:
                    st.markdown("### 💪 Ayo coba lagi!")

                if not st.session_state.score_saved and st.session_state.score > 0:
                    st.markdown("---")
                    st.markdown("### 💾 Simpan Skor")
                    with st.form("save_score_form"):
                        st.markdown(f"Nama: **{st.session_state.user_name}**")
                        st.markdown(f"Skor: **{st.session_state.score}/{st.session_state.max_questions}** (Level: {st.session_state.difficulty})")
                        if st.session_state.total_game_duration > 0:
                            st.markdown(f"Waktu: **{format_duration(st.session_state.total_game_duration)}**")
                        if st.form_submit_button("💾 Simpan Skor", use_container_width=True, type="primary"):
                            if add_score(st.session_state.user_name, st.session_state.score,
                                         st.session_state.difficulty, st.session_state.max_questions,
                                         st.session_state.game_start_time, st.session_state.game_end_time):
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

        elif st.session_state.game_started:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("### 📝 Pertanyaan")
                st.markdown("**Wilayah manakah yang disorot MERAH pada peta?**")
            with c2:
                st.markdown(f"### Soal {st.session_state.total_questions + 1}/{st.session_state.max_questions}")

            if st.session_state.question_start_time:
                qtime = time.time() - st.session_state.question_start_time
                st.progress(min(qtime / 60, 1.0), text=f"⏱️ Waktu: {qtime:.1f} dtk")

            st.markdown("### Pilih Jawaban:")
            options = st.session_state.options
            half = len(options) // 2 + len(options) % 2
            ca1, ca2 = st.columns(2)
            answer_selected = None

            with ca1:
                for i, opt in enumerate(options[:half]):
                    if st.button(opt, key=f"opt_{i}", use_container_width=True,
                                 disabled=st.session_state.answered):
                        answer_selected = opt
            with ca2:
                for i, opt in enumerate(options[half:]):
                    if st.button(opt, key=f"opt_{i+half}", use_container_width=True,
                                 disabled=st.session_state.answered):
                        answer_selected = opt

            if answer_selected and not st.session_state.answered:
                is_correct = (answer_selected == st.session_state.correct_answer)
                q_time = end_question_timer(is_correct)
                st.session_state.total_questions += 1
                if is_correct:
                    st.session_state.score += 1
                    st.session_state.feedback = f"✅ **Benar! Hebat! (Waktu: {q_time:.1f} dtk)**"
                else:
                    st.session_state.feedback = (
                        f"❌ **Jawaban benar: {st.session_state.correct_answer} "
                        f"(Waktu: {q_time:.1f} dtk)**"
                    )
                st.session_state.answered = True

                if st.session_state.total_questions >= st.session_state.max_questions:
                    st.session_state.game_over = True
                    st.session_state.game_end_time = time.time()
                    if st.session_state.game_start_time is not None:
                        st.session_state.total_game_duration = (
                            st.session_state.game_end_time - st.session_state.game_start_time
                        )
                    else:
                        st.session_state.total_game_duration = sum(
                            q["duration"] for q in st.session_state.question_times
                        )
                    if st.session_state.score == st.session_state.max_questions:
                        st.session_state.show_perfect_balloon = True

                st.rerun()

            if st.session_state.feedback:
                st.markdown("---")
                cf1, cf2, cf3 = st.columns([1, 2, 1])
                with cf2:
                    st.markdown(f"### {st.session_state.feedback}")
                    if st.session_state.answered and st.session_state.total_questions < st.session_state.max_questions:
                        if st.button("➡️ Soal Berikutnya", use_container_width=True, type="primary"):
                            pilih_wilayah()
                            st.rerun()

    # Progress bar
    if PAGE == "Game" and st.session_state.game_started and not st.session_state.game_over:
        st.markdown("---")
        cp1, cp2, cp3, cp4 = st.columns([2, 1, 1, 1])
        with cp1:
            progress = st.session_state.total_questions / st.session_state.max_questions
            st.progress(progress, text=f"Progress: {st.session_state.total_questions}/{st.session_state.max_questions}")
        with cp2:
            st.markdown(f"### ⭐ Skor: {st.session_state.score}")
        with cp3:
            st.markdown(f"### 🎯 Target: {st.session_state.max_questions}")
        with cp4:
            if st.session_state.game_start_time:
                dur = time.time() - st.session_state.game_start_time
                st.markdown(f"### ⏱️ {format_duration(dur)}")


# ==================== FOOTER ====================

menu_key = PAGE
footer_texts = {
    "Game": f"🗺️ Tebak {len(wilayah_list)} Wilayah Jawa Timur | Kesulitan: {st.session_state.difficulty}",
    "Belajar": f"📚 Mode Belajar: {len(wilayah_list)} wilayah tersedia",
    "Puzzle": f"🧩 Puzzle Drag & Drop | Tingkat: {st.session_state.puzzle_difficulty} | Wilayah: {st.session_state.puzzle_target_region or '-'}",
    "Bromo 3D": "🌋 Gunung Bromo 3D - Jelajahi keindahan gunung berapi aktif",
    "Balaikota 3D": "🏛️ Balaikota Malang 3D - Visualisasi bangunan bersejarah Kota Malang",
    "Papan Skor": "🏆 Papan Skor Tebak Jawa Timur",
    "Statistik Waktu": "⏱️ Statistik Waktu Bermain",
    "Pengaturan": "⚙️ Sesuaikan pengalaman bermain Anda",
    "Tentang": "ℹ️ Pengetahuan Jawa Timur - Aplikasi Interaktif Pembelajaran Geospasial Jawa Timur"
}
footer_text = footer_texts.get(menu_key, "🧩 Pengetahuan Tentang Kota & Kabupaten di Jawa Timur")
st.markdown(create_footer(footer_text, FOOTER_BACKGROUND_URL, st.session_state.footer_brightness),
            unsafe_allow_html=True)
