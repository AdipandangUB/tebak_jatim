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
    "Probolinggo": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Flag_of_Probolinggo_Regency.png",
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
    # Hapus prefix "Kabupaten " atau "Kota " untuk pencarian
    nama_clean = nama.replace("Kabupaten ", "").replace("Kota ", "")
    
    # Cek apakah ini kota (dimulai dengan "Kota ")
    if nama.startswith("Kota "):
        return LOGO_KOTA.get(nama_clean, None)
    else:
        return LOGO_KABUPATEN.get(nama_clean, None)


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


# ==================== PAPAN SKOR PUZZLE ====================

def load_puzzle_scoreboard():
    if "puzzle_scoreboard_data" not in st.session_state:
        st.session_state.puzzle_scoreboard_data = []
    return list(st.session_state.puzzle_scoreboard_data)


def save_puzzle_scoreboard(scoreboard):
    """Simpan SEMUA entri (semua percobaan semua pemain),
    urutkan penalti terkecil = peringkat tertinggi, simpan top 10."""
    try:
        if not isinstance(scoreboard, list):
            scoreboard = []
        # Sort: penalti terkecil dulu, jika sama ambil yang terbaru
        scoreboard.sort(key=lambda x: (
            x.get("poin_penalti", float("inf")),
            -x.get("timestamp", 0)
        ))
        scoreboard = scoreboard[:10]  # simpan top 10 entri terbaik
        st.session_state.puzzle_scoreboard_data = scoreboard
        return True
    except Exception as e:
        st.error(f"Error menyimpan skor puzzle: {str(e)}")
        return False




def add_puzzle_score(nama, waktu_detik, kesalahan):
    """Tambahkan hasil puzzle ke papan skor puzzle."""
    try:
        if not nama or waktu_detik is None:
            return False
        scoreboard = load_puzzle_scoreboard()
        now = now_wib()
        menit = int(waktu_detik // 60)
        detik = int(waktu_detik % 60)
        # Hitung skor poin: waktu × 1 + kesalahan × 10 (makin kecil makin baik)
        poin_penalti = round(waktu_detik + kesalahan * 10, 1)
        new_entry = {
            "nama": str(nama),
            "waktu_detik": round(float(waktu_detik), 1),
            "waktu_format": f"{menit:02d}:{detik:02d}",
            "waktu_teks": f"{menit} menit {detik} detik" if menit > 0 else f"{detik} detik",
            "kesalahan": int(kesalahan),
            "poin_penalti": poin_penalti,
            "tanggal": now.strftime("%Y-%m-%d %H:%M:%S"),
            "tanggal_only": now.strftime("%Y-%m-%d"),
            "jam": now.strftime("%H:%M:%S"),
            "tahun": now.year,
            "bulan": now.month,
            "timestamp": time.time(),
        }
        scoreboard.append(new_entry)
        return save_puzzle_scoreboard(scoreboard)
    except Exception as e:
        st.error(f"Error menambah skor puzzle: {str(e)}")
        return False


def get_puzzle_scoreboard_stats(scoreboard):
    """Stats dihitung langsung dari semua entri di papan skor."""
    if not scoreboard:
        return {"total_entri": 0, "waktu_tercepat": None, "kesalahan_minimal": None,
                "rata_waktu": None, "rata_kesalahan": None}
    total       = len(scoreboard)
    tercepat    = min(scoreboard, key=lambda x: x.get("waktu_detik",  float("inf")))
    minimal_err = min(scoreboard, key=lambda x: x.get("kesalahan",    float("inf")))
    rata_w      = sum(s.get("waktu_detik", 0) for s in scoreboard) / total
    rata_e      = sum(s.get("kesalahan",   0) for s in scoreboard) / total
    return {
        "total_entri":      total,
        "waktu_tercepat":   tercepat,
        "kesalahan_minimal": minimal_err,
        "rata_waktu":       round(rata_w, 1),
        "rata_kesalahan":   round(rata_e, 1),
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
    "current_page": "Quiz",
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
    "puzzle_started": False,
    "puzzle_start_time": None,
    "puzzle_completed": False,
    # Puzzle scoreboard & hasil
    "puzzle_scoreboard_data": [],
    "puzzle_result_time_sec": None,
    "puzzle_result_errors": None,
    "puzzle_score_saved": False,
    "puzzle_pending_save": False,
    "pending_navigation": None,
    "puzzle_js_waktu": None,
    "puzzle_js_errors": None,
    "puzzle_auto_save_pending": False,
}
for key, val in _defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


# (query_params puzzle tidak digunakan — komunikasi JS→Python tidak bisa via iframe)


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


# ==================== DATABASE INFO WILAYAH LENGKAP (DIPERBAIKI DENGAN PENGECEKAN KETAT) ====================

def get_wilayah_info(nama):
    """
    Fungsi untuk mendapatkan informasi wilayah berdasarkan nama
    dengan pengecekan yang sangat ketat antara Kabupaten dan Kota
    """
    
    # Database untuk KOTA (hanya kota)
    db_kota = {
        "Kota Malang": {
            "geografis": "Kota Malang terletak di dataran tinggi dengan ketinggian 440-667 mdpl. Suhu udara rata-rata 24°C, dikelilingi pegunungan (Arjuno, Semeru, Welirang) dan terkenal dengan julukan Kota Pendidikan.",
            "demografi": "Penduduk: ±900.000 jiwa. Mayoritas suku Jawa, dengan komunitas Tionghoa, Arab, dan Madura. Kepadatan tinggi dengan banyak pendatang untuk pendidikan.",
            "budaya": "Budaya Arek yang dinamis dengan pengaruh Mataraman. Seni tradisional: Tari Topeng Malangan, Wayang Topeng Malangan. Banyak seni musik modern dan tempat nongkrong artistik.",
            "keunikan": "Arsitektur kolonial Belanda masih terjaga (Gedung Balaikota, Ijen Boulevard). Dijuluki Kota Bunga dan Kota Pendidikan dengan lebih dari 50 perguruan tinggi.",
            "oleh_oleh": "Keripik buah (apel, salak), keripik tempe, bakso Malang, wingko babat, kripik singkong, coklat Singosari, dan kue lumpur."
        },
        "Kota Surabaya": {
            "geografis": "Kota pesisir utara Pulau Jawa, ibu kota Provinsi Jawa Timur. Berbatasan dengan Selat Madura di utara dan timur. Memiliki pelabuhan Tanjung Perak dan kawasan industri.",
            "demografi": "Penduduk: ±3 juta jiwa (kota terbesar kedua di Indonesia). Masyarakat multietnis: Jawa, Madura, Tionghoa, Arab, dengan budaya urban yang dinamis.",
            "budaya": "Budaya Arek Surabaya yang blak-blakan dan egaliter. Kesenian: Tari Remo, Ludruk, Wayang Kulit, dan tradisi 'arek Suroboyo'. Festival tahunan: Surabaya Cross Culture.",
            "keunikan": "Kota Pahlawan dengan sejarah pertempuran 10 November 1945. Ikon: Tugu Pahlawan, Jembatan Suramadu, House of Sampoerna, dan Patung Suro dan Boyo.",
            "oleh_oleh": "Kerupuk udang, terasi, sambal bu Rudy, wingko babat, spikok Surabaya, onde-onde, roti Semir, dan bika ambon."
        },
        "Kota Batu": {
            "geografis": "Kota wisata pegunungan dengan ketinggian 700-1.700 mdpl. Udara sejuk (17-24°C), dikelilingi Gunung Panderman, Arjuno, dan Anjasmoro. Dijuluki 'Kota Apel'.",
            "demografi": "Penduduk: ±210.000 jiwa. Masyarakat dengan budaya agraris dan pariwisata. Banyak pendatang untuk bekerja di sektor pariwisata.",
            "budaya": "Budaya Jawa Timuran dengan sentuhan modern karena pariwisata. Tradisi: Bersih Desa, Grebeg Suro, dan Festival Apel.",
            "keunikan": "Kota wisata terbesar di Jawa Timur dengan destinasi: Jatim Park 1,2,3, Batu Night Spectacular, Selecta, Songgoriti, petik apel, dan agro wisata.",
            "oleh_oleh": "Apel Batu (Manalagi, Rome Beauty), keripik apel, sari apel, sayuran organik, susu murni, kripik jamur, dan madu."
        },
        "Kota Mojokerto": {
            "geografis": "Kota kecil seluas 16,47 km², terletak di antara Surabaya (50 km) dan Malang. Dilintasi Sungai Brantas. Pusat sejarah Kerajaan Majapahit.",
            "demografi": "Penduduk: ±140.000 jiwa. Masyarakat dengan budaya Jawa Timuran yang kental, mayoritas bekerja di sektor jasa dan perdagangan.",
            "budaya": "Budaya Jawa dengan pengaruh sejarah Majapahit yang kuat. Tradisi Grebeg Majapahit dan ruwatan agung.",
            "keunikan": "Dikenal sebagai 'Kota Onde-onde' dan 'Kota Tahu'. Dekat situs bersejarah Trowulan (ibu kota Majapahit).",
            "oleh_oleh": "Onde-onde Mojokerto, tahu pong, kerupuk rambak, bandeng asap, dan berbagai makanan ringan khas."
        },
        "Kota Kediri": {
            "geografis": "Kota yang terbelah oleh Sungai Brantas menjadi Kota Barat dan Timur. Luas 63,4 km², dikenal sebagai Kota Tahu dan Kota Stasiun.",
            "demografi": "Penduduk: ±320.000 jiwa. Mayoritas suku Jawa, dengan budaya yang religius dan pekerja keras.",
            "budaya": "Budaya Jawa Arekan dengan pengaruh Mataraman. Kesenian: Tari Gambyong, Wayang Kulit, dan tradisi larung sesaji di Sungai Brantas.",
            "keunikan": "Pusat industri rokok terbesar di Indonesia (Gudang Garam). Terdapat Stasiun Kediri peninggalan Belanda dan kuliner khas yang legendaris.",
            "oleh_oleh": "Tahu takwa, tahu kuning, getuk pisang, sambal pecel, keripik tempe, dan rokok kretek."
        },
        "Kota Madiun": {
            "geografis": "Kota di jalur utama Surabaya-Yogyakarta, luas 33,23 km². Berada di dataran rendah dengan suhu 20-31°C, dikenal sebagai Kota Gadis (Perdagangan, Pendidikan, Industri).",
            "demografi": "Penduduk: ±210.000 jiwa. Masyarakat dengan budaya Jawa yang kental, banyak pekerja industri dan pedagang.",
            "budaya": "Budaya Jawa dengan pengaruh arek dan mataraman (perbatasan). Kesenian: Wayang Kulit, Tari Tayub, dan tradisi Grebeg Suro.",
            "keunikan": "Dikenal dengan kuliner pecel Madiun dan Brem. Terdapat Pura Agung Taman Sari dan Monumen Kresek.",
            "oleh_oleh": "Pecel Madiun (bumbu pecel khas), brem padat dan cair, keripik pecel, tahu khas, dan jenang."
        },
        "Kota Blitar": {
            "geografis": "Kota kecil di kaki Gunung Kelud (masih berstatus waspada). Luas 32,58 km², terkenal sebagai tempat kelahiran Soekarno.",
            "demografi": "Penduduk: ±155.000 jiwa. Masyarakat dengan budaya Jawa Arekan yang religius dan nasionalis.",
            "budaya": "Budaya Jawa Arekan dengan pengaruh Mataraman. Tradisi: larung sesaji ke Gunung Kelud dan peringatan hari lahir Bung Karno.",
            "keunikan": "Makam Bung Karno, Istana Gebang (rumah masa kecil Soekarno), Perpustakaan Bung Karno, dan pusat peringatan Proklamator.",
            "oleh_oleh": "Rujak cingur khas Blitar, sate blater, keripik tempe, pecel, dan jenang."
        },
        "Kota Pasuruan": {
            "geografis": "Kota kecil di pesisir utara Jawa Timur, antara Surabaya (65 km) dan Probolinggo. Luas 35,29 km², dilintasi jalur pantura.",
            "demografi": "Penduduk: ±210.000 jiwa. Mayoritas bekerja di sektor perdagangan, jasa, dan industri kecil.",
            "budaya": "Budaya Jawa Arekan dengan pengaruh Madura di pesisir. Kesenian: Tari Remo, Ludruk, dan tradisi petik laut.",
            "keunikan": "Kota transit dengan industri kecil dan menengah. Terdapat Stasiun Pasuruan tua dan bangunan kolonial.",
            "oleh_oleh": "Kerupuk udang, ikan asin, manisan buah, bandeng asap, dan terasi."
        },
        "Kota Probolinggo": {
            "geografis": "Kota pesisir utara di jalur utama Surabaya-Banyuwangi-Bali. Luas 56,67 km², dikenal sebagai Kota Anggur dan Kota Udang.",
            "demografi": "Penduduk: ±245.000 jiwa. Campuran Jawa dan Madura, banyak bekerja di sektor perikanan dan perdagangan.",
            "budaya": "Budaya Jawa Arekan dengan pengaruh Madura yang kuat. Tradisi: petik laut, karapan sapi, dan kesenian Tong-tong.",
            "keunikan": "Kota transit menuju Bali, dikenal dengan mangga dan udang. Terdapat Pelabuhan Tanjung Tembaga dan Gunung Bromo dari sisi Probolinggo.",
            "oleh_oleh": "Mangga Probolinggo (Mangga Manalagi), kerupuk udang, ikan asin, bandeng asap, dan keripik pisang."
        },
    }

    # Database untuk KABUPATEN (hanya kabupaten)
    db_kabupaten = {
        "Kabupaten Banyuwangi": {
            "geografis": "Terletak di ujung timur Pulau Jawa, berbatasan dengan Selat Bali. Wilayah terluas di Jawa Timur (5.782 km²). Memiliki pantai, pegunungan, dan hutan tropis.",
            "demografi": "Penduduk: ±1,7 juta jiwa. Mayoritas suku Osing (asli Banyuwangi), Jawa, Madura, dan Bali. Masyarakat multikultural dengan toleransi tinggi.",
            "budaya": "Kesenian khas: Gandrung Banyuwangi (tari penyambutan), Seblang (tari sakral), dan tari Jejer Jaran Dawuk. Tradisi: Kebo-keboan, Barong Ider Bumi.",
            "keunikan": "Kawah Ijen dengan fenomena api biru (blue fire), Taman Nasional Alas Purwo, Pantai Plengkung (G-Land) surga surfing, dan De Djawatan Forest.",
            "oleh_oleh": "Pisang agung, sale pisang, kopi khas Banyuwangi (Kopi Osing, Kopi Ijen), keripik tempe, dan kue kering khas Osing."
        },
        "Kabupaten Malang": {
            "geografis": "Kabupaten terluas kedua di Jawa Timur (3.530 km²). Mengelilingi Kota Malang dan Kota Batu. Memiliki pegunungan (Bromo, Semeru) dan pantai selatan.",
            "demografi": "Penduduk: ±2,7 juta jiwa (terbanyak di Jatim). Mayoritas suku Jawa Tengger di pegunungan dan Jawa Arekan di perkotaan.",
            "budaya": "Budaya Jawa Arekan dan Tengger (di wilayah Bromo). Tradisi: Yadnya Kasada (suku Tengger), bersih desa, dan wayang topeng Malangan.",
            "keunikan": "Pantai Balekambang (dengan pura di tengah laut), Coban Rondo (air terjun), kawasan Bromo dari sisi Malang, dan wisata petik apel di Poncokusumo.",
            "oleh_oleh": "Keripik buah (apel, salak), keripik tempe, apel Malang, susu murni, dan kerajinan kayu."
        },
        "Kabupaten Jember": {
            "geografis": "Kabupaten di kawasan Tapal Kuda, luas 3.293 km². Dikenal sebagai Kota Tembakau dan Kota Seribu Gumuk (bukit kecil).",
            "demografi": "Penduduk: ±2,5 juta jiwa. Masyarakat heterogen: Jawa, Madura, Osing, dengan budaya Pandhalungan (campuran).",
            "budaya": "Budaya campuran Jawa, Madura, dan Osing (Pandhalungan). Tradisi: Jember Fashion Carnival (mendunia), Petik Laut, dan Larung Sesaji.",
            "keunikan": "Karnaval Jember Fashion Carnival yang mendunia (terinspirasi dari Carnaval de Nice). Terdapat Pantai Papuma, Watu Ulo, dan perkebunan teh.",
            "oleh_oleh": "Suwar-suwir (kue tradisional), proll tape (kue tape), kopi Jember (Kopi Argopuro), dan olahan tembakau."
        },
        "Kabupaten Sidoarjo": {
            "geografis": "Kabupaten di selatan Surabaya, luas 714 km². Terkenal dengan industri dan lumpur Lapindo. Berbatasan dengan Selat Madura.",
            "demografi": "Penduduk: ±2,2 juta jiwa. Masyarakat heterogen dengan banyak pekerja industri dan pengrajin.",
            "budaya": "Budaya Jawa Arekan dengan pengaruh Madura di pesisir. Tradisi: kupatan, petik laut, dan kesenian ludruk.",
            "keunikan": "Pusat industri, Bandara Juanda, dan kerajinan tas kulit. Fenomena Lumpur Lapindo yang masih aktif. Penghasil udang dan bandeng.",
            "oleh_oleh": "Kerupuk udang, terasi, kerajinan kulit (tas, sepatu), bandeng presto, dan otak-otak bandeng."
        },
        "Kabupaten Kediri": {
            "geografis": "Kabupaten yang mengelilingi Kota Kediri, luas 1.386 km². Wilayah subur di sekitar Sungai Brantas dengan Gunung Kelud di selatan.",
            "demografi": "Penduduk: ±1,7 juta jiwa. Mayoritas petani dan buruh pabrik rokok.",
            "budaya": "Budaya Jawa Arekan dengan tradisi: Bersih Desa, Wayang Kulit, dan Tari Gambyong. Pengaruh Kerajaan Kediri (Kadiri) masih kuat.",
            "keunikan": "Gunung Kelud (salah satu gunung teraktif di Indonesia), pabrik rokok terbesar (Gudang Garam), dan situs sejarah Kerajaan Kediri (Candi Tondowongso).",
            "oleh_oleh": "Tahu takwa, tahu kuning, getuk pisang, sambal pecel, dan keripik tempe."
        },
        "Kabupaten Mojokerto": {
            "geografis": "Kabupaten yang menjadi lokasi pusat Kerajaan Majapahit di Trowulan. Luas 969 km², dilintasi Sungai Brantas.",
            "demografi": "Penduduk: ±1,2 juta jiwa. Banyak bekerja di sektor pertanian, industri, dan pariwisata sejarah.",
            "budaya": "Budaya Jawa dengan pengaruh sejarah Majapahit. Tradisi: Grebeg Majapahit, wayang kulit, dan pertunjukan sejarah.",
            "keunikan": "Situs Trowulan, bekas ibu kota Kerajaan Majapahit dengan museum dan candi (Candi Tikus, Candi Brahu, Kolam Segaran).",
            "oleh_oleh": "Onde-onde Mojokerto, kerupuk rambak, bandeng asap, dan makanan ringan khas Majapahitan."
        },
        "Kabupaten Pasuruan": {
            "geografis": "Kabupaten dengan wilayah pegunungan di selatan (Gunung Arjuno, Welirang) dan pesisir utara. Luas 1.474 km².",
            "demografi": "Penduduk: ±1,6 juta jiwa. Masyarakat agraris di pegunungan dan nelayan di pesisir.",
            "budaya": "Budaya Jawa Arekan dengan tradisi: Yadnya Kasada (Tengger), petik laut, dan wayang kulit.",
            "keunikan": "Kawasan Taman Nasional Bromo Tengger Semeru dari sisi Pasuruan (Desa Wonokitri). Air terjun dan pemandian air panas.",
            "oleh_oleh": "Manisan buah, keripik apel, susu murni, sayuran organik, dan madu."
        },
        "Kabupaten Probolinggo": {
            "geografis": "Kabupaten dengan wilayah pegunungan (Bromo) di selatan dan pantai utara. Luas 1.696 km².",
            "demografi": "Penduduk: ±1,2 juta jiwa. Mayoritas suku Jawa Tengger di pegunungan dan Jawa-Madura di pesisir.",
            "budaya": "Budaya Jawa Arekan dengan pengaruh Madura. Tradisi: Yadnya Kasada (Tengger), karapan sapi, dan petik laut.",
            "keunikan": "Kawasan Gunung Bromo dari sisi Probolinggo (Cemorolawang), penghasil mangga terbesar di Jatim, dan Pantai Bentar.",
            "oleh_oleh": "Mangga Probolinggo, kerupuk udang, keripik pisang, dan manisan mangga."
        },
        "Kabupaten Blitar": {
            "geografis": "Kabupaten di kaki Gunung Kelud, memiliki wilayah pegunungan di utara dan pantai selatan (Samudra Hindia). Luas 1.588 km².",
            "demografi": "Penduduk: ±1,2 juta jiwa. Mayoritas petani dan nelayan dengan budaya yang religius.",
            "budaya": "Budaya Jawa Arekan dengan tradisi: Larung Sesaji ke Gunung Kelud, petik laut, dan wayang kulit.",
            "keunikan": "Tempat kelahiran Presiden Soekarno, memiliki Makam Bung Karno, Istana Gebang, dan Pantai Tambakrejo.",
            "oleh_oleh": "Rujak cingur khas Blitar, sate blater, keripik tempe, pecel, dan jenang."
        },
        "Kabupaten Tulungagung": {
            "geografis": "Kabupaten di selatan Jawa Timur, luas 1.055 km². Terkenal dengan industri marmer. Berbatasan dengan Samudra Hindia.",
            "demografi": "Penduduk: ±1,1 juta jiwa. Banyak bekerja sebagai perajin marmer, petani, dan nelayan.",
            "budaya": "Budaya Jawa Mataraman dengan pengaruh pesisir selatan. Tradisi: Larung Sesaji ke Pantai Popoh, wayang kulit, dan jaranan.",
            "keunikan": "Penghasil marmer terbesar di Indonesia (marmer Tulungagung), Pantai Popoh, Pantai Gemah, dan Goa Pasir.",
            "oleh_oleh": "Kerajinan marmer (patung, asbak, meja), keripik tempe, jenang, dan bandeng asap."
        },
        "Kabupaten Trenggalek": {
            "geografis": "Kabupaten di pesisir selatan Jawa Timur, luas 1.261 km². Memiliki pantai-pantai indah di sepanjang Samudra Hindia.",
            "demografi": "Penduduk: ±750 ribu jiwa. Mayoritas suku Jawa dengan budaya pesisiran dan agraris.",
            "budaya": "Budaya Jawa dengan tradisi pesisiran. Kesenian: Jaranan, Wayang Kulit, dan tradisi larung sesaji.",
            "keunikan": "Memiliki Pantai Prigi, Pantai Karanggongso, dan Pantai Pasir Putih yang indah. Dikenal dengan kuliner alen-alen.",
            "oleh_oleh": "Alen-alen (makanan ringan dari singkong), keripik tempe, ikan asap, dan terasi."
        },
        "Kabupaten Ponorogo": {
            "geografis": "Kabupaten yang terkenal dengan kesenian Reog, luas 1.371 km². Berada di wilayah barat Jawa Timur.",
            "demografi": "Penduduk: ±950 ribu jiwa. Mayoritas suku Jawa Mataraman dengan budaya yang kental.",
            "budaya": "Budaya Jawa Mataraman, pusat kesenian Reog Ponorogo (warisan budaya tak benda). Tradisi: Grebeg Suro, Festival Reog Nasional.",
            "keunikan": "Kota Reog dengan Patung Reog raksasa, Telaga Ngebel (danau alami), dan Goa Lowo (goa kelelawar).",
            "oleh_oleh": "Dawet Jabung (minuman khas), sambal pecel, keripik tempe, dan jenang."
        },
        "Kabupaten Pacitan": {
            "geografis": "Kabupaten di pesisir selatan, berbatasan dengan Jawa Tengah. Luas 1.389 km², dijuluki 'Kota 1001 Goa'.",
            "demografi": "Penduduk: ±550 ribu jiwa. Mayoritas suku Jawa Mataraman dengan budaya pesisir.",
            "budaya": "Budaya Jawa Mataraman dengan pengaruh pesisir selatan. Tradisi: larung sesaji, wayang kulit, dan jaranan.",
            "keunikan": "Goa Gong (goa paling indah se-Asia Tenggara), Goa Tabuhan, Pantai Klayar, dan Pantai Soge.",
            "oleh_oleh": "Sale pisang, keripik tempe, ikan asap, terasi, dan batik Pacitan."
        },
        "Kabupaten Ngawi": {
            "geografis": "Kabupaten di perbatasan Jawa Timur dan Jawa Tengah, dilintasi Bengawan Solo (sungai terpanjang di Jawa). Luas 1.295 km².",
            "demografi": "Penduduk: ±900 ribu jiwa. Mayoritas suku Jawa Mataraman dengan budaya agraris.",
            "budaya": "Budaya Jawa Mataraman dengan pengaruh Jawa Tengah. Kesenian: Wayang Kulit, Jaranan, dan tradisi bersih desa.",
            "keunikan": "Benteng Van den Bosch (benteng peninggalan Belanda), gerbang masuk dari arah Solo, dan Hutan Klitih.",
            "oleh_oleh": "Keripik tempe, pecel, jenang, dan sale pisang."
        },
        "Kabupaten Magetan": {
            "geografis": "Kabupaten di perbatasan Jawa Timur dan Jawa Tengah, di lereng Gunung Lawu. Luas 688 km², dikenal sebagai 'Kota Kaki Gunung Lawu'.",
            "demografi": "Penduduk: ±650 ribu jiwa. Mayoritas suku Jawa Mataraman dengan budaya agraris.",
            "budaya": "Budaya Jawa Mataraman (perbatasan dengan Solo/Yogyakarta). Tradisi: Grebeg Suro, wayang kulit, dan jaranan.",
            "keunikan": "Telaga Sarangan (danau alami di kaki Gunung Lawu), gerbang masuk Jawa Timur dari arah barat, dan kawasan wisata lereng Lawu.",
            "oleh_oleh": "Keripik buah, brem, oleh-oleh khas Lawu, dan sayuran organik."
        },
        "Kabupaten Madiun": {
            "geografis": "Kabupaten yang mengelilingi Kota Madiun, luas 1.010 km². Wilayah agraris dengan persawahan luas di lembah Gunung Wilis.",
            "demografi": "Penduduk: ±750 ribu jiwa. Mayoritas petani dengan budaya Jawa Mataraman.",
            "budaya": "Budaya Jawa Mataraman dengan tradisi: Grebeg Suro, wayang kulit, dan jaranan.",
            "keunikan": "Penghasil beras dan jahe, jalur utama Surabaya-Yogyakarta. Terdapat Waduk Bening dan Waduk Widas.",
            "oleh_oleh": "Pecel Madiun, brem, jahe instan, dan keripik tempe."
        },
        "Kabupaten Nganjuk": {
            "geografis": "Kabupaten di lembah Gunung Wilis, dilintasi Sungai Brantas. Luas 1.224 km², dikenal sebagai 'Kota Bayam'.",
            "demografi": "Penduduk: ±1,1 juta jiwa. Masyarakat agraris dengan mayoritas petani.",
            "budaya": "Budaya Jawa Mataraman dengan tradisi: Wayang Kulit, Jaranan, dan bersih desa.",
            "keunikan": "Dikenal sebagai kota bayam dan penghasil beras berkualitas. Terdapat Candi Lor dan Candi Ngetos.",
            "oleh_oleh": "Bayam Nganjuk, keripik bayam, getuk pisang, dan jenang."
        },
        "Kabupaten Jombang": {
            "geografis": "Kabupaten yang dikenal sebagai 'Kota Santri' karena banyak pesantren. Luas 1.159 km², dilintasi Sungai Brantas.",
            "demografi": "Penduduk: ±1,3 juta jiwa. Masyarakat religius dengan banyak santri dan ulama.",
            "budaya": "Budaya Jawa dengan pengaruh pesantren yang kuat. Tradisi: haul kyai, manaqiban, dan kesenian rebana.",
            "keunikan": "Pusat pendidikan Islam dengan pesantren-pesantren besar (Tebuireng, Denanyar). Makam pendiri NU (KH Hasyim Asy'ari).",
            "oleh_oleh": "Jenang, keripik tempe, sambal pecel, dan oleh-oleh khas pesantren."
        },
        "Kabupaten Bojonegoro": {
            "geografis": "Kabupaten di tepi Bengawan Solo, luas 2.307 km². Wilayah penghasil minyak dan gas terbesar di Jawa Timur.",
            "demografi": "Penduduk: ±1,3 juta jiwa. Mayoritas petani dan pekerja migas.",
            "budaya": "Budaya Jawa dengan pengaruh Jawa Tengah (perbatasan). Tradisi: sedekah bumi, wayang kulit, dan jaranan.",
            "keunikan": "Kota minyak dengan sumur minyak tradisional (mbah Liyung), Waduk Pacal, dan Jembatan tua Bengawan Solo.",
            "oleh_oleh": "Ledre (makanan khas dari pisang), sambal pecel, keripik pisang, dan olahan jagung."
        },
        "Kabupaten Tuban": {
            "geografis": "Kabupaten pesisir utara, perbatasan Jawa Timur dan Jawa Tengah. Luas 1.834 km², berbatasan dengan Laut Jawa.",
            "demografi": "Penduduk: ±1,2 juta jiwa. Mayoritas suku Jawa pesisir dengan pengaruh Madura.",
            "budaya": "Budaya pesisir dengan pengaruh Jawa dan Madura. Tradisi: petik laut, haul wali, dan kesenian sandur.",
            "keunikan": "Makam Sunan Bonang (salah satu Wali Songo), kota tua dengan sejarah penyebaran Islam, dan Pantai Boom.",
            "oleh_oleh": "Kopi Tuban, bandeng asap, kerupuk ikan, terasi, dan batik Tuban (batik gedog)."
        },
        "Kabupaten Lamongan": {
            "geografis": "Kabupaten pesisir utara, berbatasan dengan Laut Jawa. Luas 1.812 km², dikenal sebagai 'Kota Soto'.",
            "demografi": "Penduduk: ±1,4 juta jiwa. Campuran Jawa pesisir dan Madura.",
            "budaya": "Budaya pesisir dengan pengaruh Jawa dan Madura. Tradisi: petik laut, wayang kulit, dan kesenian tong-tong.",
            "keunikan": "Makam Sunan Drajat (Wali Songo), Wisata Bahari Lamongan (WBL), dan kuliner soto legendaris.",
            "oleh_oleh": "Soto Lamongan (bumbu soto), wingko babat, kerupuk ikan, bandeng asap, dan terasi."
        },
        "Kabupaten Gresik": {
            "geografis": "Kabupaten pesisir utara, berbatasan dengan Surabaya, luas 1.191 km². Memiliki banyak industri besar (Kawasan Industri Gresik).",
            "demografi": "Penduduk: ±1,3 juta jiwa. Masyarakat heterogen dengan banyak pekerja industri.",
            "budaya": "Budaya pesisir dengan pengaruh Jawa dan Madura. Tradisi: haul Sunan Giri, petik laut, dan kesenian hadrah.",
            "keunikan": "Kota Industri, makam Sunan Giri (Wali Songo), Bandara Internasional Juanda, dan Pelabuhan Gresik.",
            "oleh_oleh": "Bandeng presto, udang, kerupuk ikan, terasi, dan kerajinan batik Gresik."
        },
        "Kabupaten Bangkalan": {
            "geografis": "Kabupaten di Pulau Madura, pintu masuk dari Surabaya melalui Jembatan Suramadu. Luas 1.260 km².",
            "demografi": "Penduduk: ±1 juta jiwa. Mayoritas suku Madura dengan budaya yang kental.",
            "budaya": "Budaya Madura yang kental: Karapan Sapi, musik Tong-tong, Tari Muang Sangkal.",
            "keunikan": "Pintu gerbang Madura melalui Suramadu, Universitas Trunojoyo, dan makam para ulama (Syaikhona Kholil).",
            "oleh_oleh": "Keripik pedas (cilok), batik Madura, olahan ikan, dan terasi."
        },
        "Kabupaten Sampang": {
            "geografis": "Kabupaten di Pulau Madura bagian selatan, luas 1.233 km². Berbatasan dengan Selat Madura.",
            "demografi": "Penduduk: ±950 ribu jiwa. Mayoritas suku Madura dengan budaya bahari.",
            "budaya": "Budaya Madura yang kental: Karapan Sapi, musik Tong-tong, Tari Topeng Madura.",
            "keunikan": "Dikenal dengan tradisi karapan sapi dan batik khas Madura. Terdapat Pantai Nepa dan Camplong.",
            "oleh_oleh": "Batik Madura, keripik pedas, ikan asap, dan terasi."
        },
        "Kabupaten Pamekasan": {
            "geografis": "Kabupaten di Pulau Madura, berbatasan dengan Laut Jawa di utara dan Selat Madura di selatan. Luas 792 km².",
            "demografi": "Penduduk: ±850 ribu jiwa. Mayoritas suku Madura dengan budaya yang kuat.",
            "budaya": "Budaya Madura yang kuat, tradisi karapan sapi, musik tong-tong, dan Tari Rokat Tase'.",
            "keunikan": "Dikenal sebagai pusat pendidikan agama di Madura dengan banyak pesantren. Pusat kerajinan batik tulis.",
            "oleh_oleh": "Keripik pedas, batik Madura (batik tulis Pamekasan), olahan ikan, dan terasi."
        },
        "Kabupaten Sumenep": {
            "geografis": "Kabupaten di ujung timur Pulau Madura, terdiri dari Pulau Madura dan gugusan kepulauan (Kangean, Masalembu). Luas 2.093 km².",
            "demografi": "Penduduk: ±1,1 juta jiwa. Suku Madura dengan budaya bahari di kepulauan.",
            "budaya": "Budaya Madura dengan pengaruh dari berbagai kerajaan (Majapahit, Demak). Tradisi: Karapan Sapi, Tari Moang Sangkal.",
            "keunikan": "Keraton Sumenep (peninggalan kesultanan), batik tulis Sumenep, kepulauan Kangean dengan keindahan bawah laut.",
            "oleh_oleh": "Batik Sumenep, keripik pedas, ikan asap, kerajinan perak, dan terasi."
        },
        "Kabupaten Bondowoso": {
            "geografis": "Kabupaten di kawasan Tapal Kuda, luas 1.560 km². Dikenal sebagai 'Kota Tape' dan 'Kota Kopi'.",
            "demografi": "Penduduk: ±800 ribu jiwa. Campuran Jawa dan Madura (Pandhalungan).",
            "budaya": "Budaya campuran Jawa-Madura yang unik (Pandhalungan). Tradisi: petik kopi, ruwatan, dan kesenian jaranan.",
            "keunikan": "Dikenal dengan tape Bondowoso dan kawasan perkebunan kopi di dataran tinggi Ijen. Kawah Wurung, Puncak Maha.",
            "oleh_oleh": "Tape Bondowoso (tape singkong), kopi Bondowoso (Kopi Ijen Raung), kue nastar tape, dan keripik tape."
        },
        "Kabupaten Situbondo": {
            "geografis": "Kabupaten di kawasan Tapal Kuda, jalur pantai utara menuju Banyuwangi. Luas 1.638 km².",
            "demografi": "Penduduk: ±700 ribu jiwa. Campuran Jawa dan Madura (Pandhalungan) dengan budaya pesisir.",
            "budaya": "Budaya campuran Jawa-Madura. Tradisi: petik laut, karapan sapi, dan kesenian jaranan.",
            "keunikan": "Kawasan perbukitan dengan perkebunan, Pantai Pasir Putih, Taman Nasional Baluran (African van Java).",
            "oleh_oleh": "Ikan asap, kerupuk ikan, manisan buah, dan batik Situbondo."
        },
        "Kabupaten Lumajang": {
            "geografis": "Kabupaten di kaki Gunung Semeru (tertinggi di Jawa), luas 1.790 km². Memiliki pantai selatan yang indah.",
            "demografi": "Penduduk: ±1,1 juta jiwa. Mayoritas suku Jawa Tengger di pegunungan dan Jawa Arekan di perkotaan.",
            "budaya": "Budaya Jawa Tengger dan Jawa umumnya. Tradisi: Yadnya Kasada (Tengger), bersih desa, dan wayang kulit.",
            "keunikan": "Kawasan Ranu Pane dan Ranu Kumbolo di jalur pendakian Semeru. Pantai Bambang, Pantai Watu Pecak, dan Selokambang.",
            "oleh_oleh": "Pisang agung, keripik pisang, sale pisang, dan kopi khas Lumajang."
        }
    }

    # PENCARIAN DENGAN PRIORITAS SANGAT KETAT
    
    # 1. CEK PREFIX TERLEBIH DAHULU
    if nama.startswith("Kabupaten "):
        # Cari di database kabupaten
        if nama in db_kabupaten:
            return db_kabupaten[nama]
        # Case insensitive di kabupaten
        for key in db_kabupaten.keys():
            if key.lower() == nama.lower():
                return db_kabupaten[key]
    
    elif nama.startswith("Kota "):
        # Cari di database kota
        if nama in db_kota:
            return db_kota[nama]
        # Case insensitive di kota
        for key in db_kota.keys():
            if key.lower() == nama.lower():
                return db_kota[key]
    
    # 2. JIKA TIDAK ADA PREFIX, COBA COCOKKAN DENGAN KOTA ATAU KABUPATEN YANG SESUAI
    else:
        # Coba cari di database kabupaten dulu (default untuk tanpa prefix)
        for key in db_kabupaten.keys():
            # Ambil nama tanpa "Kabupaten "
            nama_tanpa_prefix = key.replace("Kabupaten ", "")
            if nama_tanpa_prefix.lower() == nama.lower():
                return db_kabupaten[key]
        
        # Coba cari di database kota
        for key in db_kota.keys():
            # Ambil nama tanpa "Kota "
            nama_tanpa_prefix = key.replace("Kota ", "")
            if nama_tanpa_prefix.lower() == nama.lower():
                return db_kota[key]
    
    # 3. FALLBACK: Gabungkan kedua database dan cari
    db = {**db_kota, **db_kabupaten}
    
    # Exact match
    if nama in db:
        return db[nama]
    
    # Case insensitive
    for key in db.keys():
        if key.lower() == nama.lower():
            return db[key]
    
    # Cari tanpa prefix (dari semua database)
    nama_without_prefix = nama.lower().replace("kabupaten ", "").replace("kota ", "")
    for key in db.keys():
        key_without_prefix = key.lower().replace("kabupaten ", "").replace("kota ", "")
        if key_without_prefix == nama_without_prefix:
            return db[key]

    # 4. DEFAULT jika tidak ditemukan
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
            <div class="footer-title">🧩 Sepiro Jawa Timur, Sampeyan</div>
            <p>{footer_text}</p>
            <p>⏰ {current_time} WIB | © 2026 Program Pengabdian Masyarakat - Penguatan Literasi Geospasial Jawa Timur Bagi Gen Z Melalui Edukasi Berbasis Gamifikasi Menggunakan Platform "Sepiro Jatim, Sampeyan" - Lab. Environmental, Infrastructure, and Information System (EIIS), Dept. Perencanaan Wilayah & Kota, Fak. Teknik, Universitas Brawijaya | Versi 2.9.0</p>
            <p>Quiz Tebak Wilayah | Info Wilayah | Puzzle Drag & Drop | Bromo 3D | Balaikota 3D | Papan Skor | Statistik Waktu | 🎵 Musik</p>
        </div>
    </div>
    """


# ==================== PUZZLE DRAG & DROP FEATURE (v3.0 — JAWA TIMUR UTUH) ====================

def get_puzzle_html(geojson_data, start_time_ms):
    """
    Puzzle peta JAWA TIMUR UTUH:
    - 1 wilayah provinsi (seluruh Jawa Timur)
    - Setiap kepingan = 1 kabupaten/kota (bentuk polygon asli GeoJSON)
    - Level Normal saja (semua kab/kota = kepingan)
    - Drag & drop ke posisi geografis yang tepat
    """
    all_features = geojson_data.get("features", [])
    if not all_features:
        return "<p>❌ Data wilayah tidak ditemukan.</p>"

    geojson_str = json.dumps(geojson_data)
    SNAP_DIST   = 60   # piksel toleransi snap (level Normal)

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
  #puzzle-header {{ text-align:center; padding:6px 0 10px 0; }}
  #puzzle-header h2 {{
    font-size:1.4em; font-weight:900;
    background: linear-gradient(90deg,#ffd700,#ff6b35,#ffd700);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    letter-spacing:1px;
  }}
  #puzzle-header .subtitle {{ font-size:0.82em; color:rgba(255,255,255,0.7); margin-top:2px; }}
  #stats-bar {{
    display:flex; justify-content:center; gap:16px; margin:6px 0; flex-wrap:wrap;
  }}
  .stat-pill {{
    background:rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.2);
    border-radius:30px; padding:5px 14px; font-size:0.80em; font-weight:700;
    display:flex; align-items:center; gap:5px;
  }}
  .stat-pill span {{ color:#ffd700; }}
  #main-layout {{
    display:flex; gap:10px; align-items:flex-start; justify-content:center; flex-wrap:wrap;
  }}
  #canvas-wrapper {{
    position:relative; background:rgba(255,255,255,0.04);
    border:2px solid rgba(255,255,255,0.15); border-radius:14px;
    overflow:hidden; flex:1 1 560px; max-width:700px;
  }}
  #canvas-label {{
    position:absolute; top:7px; left:10px; font-size:0.68em;
    color:rgba(255,255,255,0.45); font-weight:700; letter-spacing:1px;
    text-transform:uppercase; pointer-events:none; z-index:10;
  }}
  #puzzle-canvas {{
    display:block; width:100%; touch-action:none; user-select:none; cursor:grab;
  }}
  #puzzle-canvas:active {{ cursor:grabbing; }}
  #pieces-panel {{
    background:rgba(255,255,255,0.06); border:2px dashed rgba(255,255,255,0.2);
    border-radius:14px; padding:10px; flex:0 0 190px;
    max-height:640px; overflow-y:auto; min-width:155px;
  }}
  #pieces-panel h4 {{
    font-size:0.78em; color:rgba(255,255,255,0.6); text-transform:uppercase;
    letter-spacing:1px; margin-bottom:6px; text-align:center;
  }}
  #pieces-container {{ display:flex; flex-wrap:wrap; gap:5px; justify-content:center; }}
  .piece-thumb {{
    background:rgba(255,255,255,0.08); border:1.5px solid rgba(255,255,255,0.2);
    border-radius:7px; cursor:grab; transition:all 0.2s; overflow:hidden;
    display:flex; align-items:center; justify-content:center;
    position:relative;
  }}
  .piece-thumb:hover {{
    background:rgba(255,215,0,0.15); border-color:#ffd700;
    transform:scale(1.07); box-shadow:0 3px 12px rgba(255,215,0,0.3);
  }}
  .piece-thumb.placed {{
    opacity:0.28; cursor:default; pointer-events:none;
    border-color:#4CAF50; background:rgba(76,175,80,0.08);
  }}
  .piece-label {{
    position:absolute; bottom:1px; left:0; right:0;
    font-size:7px; text-align:center; color:rgba(255,255,255,0.7);
    line-height:1.1; padding:0 2px;
    pointer-events:none;
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
  }}
  #progress-bar-wrap {{
    margin:8px 0 4px 0; background:rgba(255,255,255,0.1);
    border-radius:10px; height:9px; overflow:hidden;
  }}
  #progress-bar-fill {{
    height:100%; background:linear-gradient(90deg,#4CAF50,#8BC34A);
    border-radius:10px; transition:width 0.4s ease; width:0%;
  }}
  #progress-text {{ text-align:center; font-size:0.76em; color:rgba(255,255,255,0.6); margin-bottom:6px; }}
  #btn-row {{
    display:flex; gap:7px; justify-content:center; margin:8px 0 5px 0; flex-wrap:wrap;
  }}
  .puzzle-btn {{
    background:linear-gradient(135deg,#667eea,#764ba2); color:white; border:none;
    border-radius:18px; padding:7px 18px; font-size:0.82em; font-weight:700;
    font-family:'Nunito',sans-serif; cursor:pointer; transition:all 0.2s;
    box-shadow:0 3px 10px rgba(102,126,234,0.4);
  }}
  .puzzle-btn:hover {{ transform:translateY(-2px); box-shadow:0 5px 16px rgba(102,126,234,0.6); }}
  .puzzle-btn.danger {{ background:linear-gradient(135deg,#f44336,#c62828); }}
  .puzzle-btn.success {{ background:linear-gradient(135deg,#4CAF50,#2E7D32); }}
  #win-overlay {{
    display:none; position:fixed; top:0; left:0; width:100%; height:100%;
    background:rgba(0,0,0,0.88); z-index:999; justify-content:center;
    align-items:center; flex-direction:column; text-align:center; padding:20px;
  }}
  #win-overlay.show {{ display:flex; }}
  #win-box {{
    background:linear-gradient(135deg,#1a1a2e,#16213e);
    border:3px solid #ffd700; border-radius:22px; padding:32px 36px; max-width:420px;
    box-shadow:0 0 60px rgba(255,215,0,0.4);
    animation:popIn 0.6s cubic-bezier(0.175,0.885,0.32,1.275) forwards;
  }}
  @keyframes popIn {{
    from {{ transform:scale(0.4); opacity:0; }}
    to   {{ transform:scale(1);   opacity:1; }}
  }}
  #win-box h1 {{
    font-size:2em; font-weight:900;
    background:linear-gradient(90deg,#ffd700,#ff6b35);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:8px;
  }}
  #win-box p {{ color:rgba(255,255,255,0.85); font-size:1em; margin:6px 0; }}
  #win-time {{ font-size:1.7em; font-weight:900; color:#ffd700; margin:10px 0; }}
  #snap-feedback {{
    position:absolute; pointer-events:none; font-size:1.7em;
    z-index:200; display:none;
  }}
  @keyframes floatUp {{
    0%   {{ opacity:1; transform:translateY(0) scale(1); }}
    100% {{ opacity:0; transform:translateY(-55px) scale(1.4); }}
  }}
  #tooltip {{
    position:absolute; background:rgba(0,0,0,0.88); color:#ffd700;
    padding:4px 10px; border-radius:8px; font-size:0.74em; font-weight:700;
    pointer-events:none; display:none; white-space:nowrap; z-index:100;
    border:1px solid rgba(255,215,0,0.3);
  }}
</style>
</head>
<body>

<div id="puzzle-header">
  <div style="display:inline-block;background:#FF9800;color:white;padding:3px 14px;
    border-radius:20px;font-weight:700;font-size:0.80em;margin-bottom:5px;">
    ⚡ Normal — {len(all_features)} Kepingan
  </div>
  <h2>🧩 PUZZLE PETA JAWA TIMUR</h2>
  <div class="subtitle">Susun {len(all_features)} kepingan kabupaten/kota menjadi peta Jawa Timur yang utuh!</div>
</div>

<div id="stats-bar">
  <div class="stat-pill">⏱️ Waktu <span id="timer-display">00:00</span></div>
  <div class="stat-pill">🧩 Terpasang <span id="placed-count">0</span>/<span id="total-count">{len(all_features)}</span></div>
  <div class="stat-pill">🎯 Akurasi <span id="accuracy-display">100%</span></div>
</div>

<div id="progress-bar-wrap"><div id="progress-bar-fill"></div></div>
<div id="progress-text">Seret kepingan kab/kota ke posisi yang tepat di peta!</div>

<div id="btn-row">
  <button class="puzzle-btn" onclick="shufflePieces()">🔀 Acak Ulang</button>
  <button class="puzzle-btn" onclick="showHint()">💡 Petunjuk</button>
  <button class="puzzle-btn danger" onclick="resetPuzzle()">🔄 Reset</button>
  <button class="puzzle-btn success" onclick="autoSolve()">✨ Selesaikan</button>
</div>

<div id="main-layout">
  <div id="canvas-wrapper">
    <div id="canvas-label">PETA JAWA TIMUR — DRAG KEPINGAN KE SINI</div>
    <canvas id="puzzle-canvas"></canvas>
    <div id="tooltip"></div>
    <div id="snap-feedback">✅</div>
  </div>
  <div id="pieces-panel">
    <h4 id="panel-title">📦 Kepingan ({len(all_features)})</h4>
    <div id="progress-bar-wrap" style="margin:4px 0 8px 0;">
      <div id="progress-bar-fill2"
        style="height:7px;background:linear-gradient(90deg,#4CAF50,#8BC34A);
               border-radius:10px;width:0%;transition:width 0.4s;">
      </div>
    </div>
    <div id="pieces-container"></div>
  </div>
</div>

<div id="win-overlay">
  <div id="win-box">
    <div style="font-size:3em;margin-bottom:6px;">🏆</div>
    <h1>PUZZLE SELESAI!</h1>
    <p>Peta <strong>Jawa Timur</strong> berhasil disusun!</p>
    <p>Semua <strong>{len(all_features)} kabupaten/kota</strong> terpasang!</p>
    <div id="win-time">00:00</div>
    <p id="win-moves">0 kesalahan</p>
    <p style="color:#ffd700;font-size:0.88em;margin-top:8px;">
      🎉 Luar biasa! Kamu mengenal semua wilayah Jawa Timur!
    </p>
    <p style="color:#4ade80;font-size:0.85em;margin-top:10px;">
      📜 Scroll ke bawah untuk menyimpan skor!
    </p>
    <button class="puzzle-btn success"
      style="margin-top:10px;font-size:1em;padding:10px 30px;"
      onclick="location.reload()">🔄 Main Lagi</button>
  </div>
</div>

<script>
(function() {{
  const GEOJSON    = {geojson_str};
  const SNAP_DIST  = {SNAP_DIST};
  const START_TIME = Date.now();

  // ===== CANVAS =====
  const canvas = document.getElementById('puzzle-canvas');
  const ctx    = canvas.getContext('2d');
  const W = 680, H = 560;
  canvas.width = W; canvas.height = H;

  // ===== PROYEKSI — fit seluruh Jawa Timur =====
  let minLon=180, maxLon=-180, minLat=90, maxLat=-90;

  function iterGeom(geom, cb) {{
    function rec(c) {{
      if (typeof c[0] === 'number') {{ cb(c[0], c[1]); return; }}
      c.forEach(rec);
    }}
    rec(geom.coordinates);
  }}

  GEOJSON.features.forEach(f => iterGeom(f.geometry, (lon,lat) => {{
    if(lon<minLon) minLon=lon; if(lon>maxLon) maxLon=lon;
    if(lat<minLat) minLat=lat; if(lat>maxLat) maxLat=lat;
  }}));

  const PAD    = 38;
  const scaleX = (W - PAD*2) / (maxLon - minLon);
  const scaleY = (H - PAD*2) / (maxLat - minLat);
  const SCALE  = Math.min(scaleX, scaleY);

  function project(lon, lat) {{
    return [
      PAD + (lon - minLon) * SCALE,
      H - PAD - (lat - minLat) * SCALE
    ];
  }}

  // ===== BUILD Path2D =====
  function buildPath(geometry) {{
    const p = new Path2D();
    function addRing(ring) {{
      ring.forEach((c, i) => {{
        const [x,y] = project(c[0],c[1]);
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

  // Hitung luas poligon (dalam satuan proyeksi)
  function polyArea(ring) {{
    let area = 0;
    const pts = ring.map(c => project(c[0], c[1]));
    for(let i=0, j=pts.length-1; i<pts.length; j=i++) {{
      area += (pts[j][0]+pts[i][0]) * (pts[j][1]-pts[i][1]);
    }}
    return Math.abs(area / 2);
  }}

  // Centroid proyeksi: untuk MultiPolygon pakai polygon TERBESAR
  // sehingga kepulauan kecil tidak menarik centroid ke tengah laut
  function geomCentroid(geom) {{
    if(geom.type === 'MultiPolygon') {{
      // Cari polygon terbesar berdasarkan luas ring luar
      let bestRing = null, bestArea = 0;
      geom.coordinates.forEach(poly => {{
        const area = polyArea(poly[0]);
        if(area > bestArea) {{ bestArea = area; bestRing = poly[0]; }}
      }});
      if(bestRing) {{
        let sx=0, sy=0;
        bestRing.forEach(c => {{ const [x,y]=project(c[0],c[1]); sx+=x; sy+=y; }});
        return [sx/bestRing.length, sy/bestRing.length];
      }}
    }}
    // Polygon biasa atau fallback: rata-rata semua titik
    let sx=0, sy=0, n=0;
    iterGeom(geom, (lon,lat) => {{
      const [x,y] = project(lon,lat);
      sx+=x; sy+=y; n++;
    }});
    return [sx/n, sy/n];
  }}

  // Bounding box proyeksi
  function geomBBox(geom) {{
    let x1=W, x2=0, y1=H, y2=0;
    iterGeom(geom, (lon,lat) => {{
      const [x,y] = project(lon,lat);
      if(x<x1) x1=x; if(x>x2) x2=x;
      if(y<y1) y1=y; if(y>y2) y2=y;
    }});
    return {{ x1,x2,y1,y2, w:x2-x1, h:y2-y1 }};
  }}

  // ===== BUILD PIECES — setiap feature = 1 kepingan =====
  const pieces = GEOJSON.features.map((feat, i) => {{
    const name     = feat.properties.name;
    const centroid = geomCentroid(feat.geometry);
    const bbox     = geomBBox(feat.geometry);
    const path     = buildPath(feat.geometry);
    return {{
      id:       i,
      name:     name,
      geometry: feat.geometry,
      path:     path,
      centroid: centroid,   // posisi target di canvas (dx=0 = terpasang)
      bbox:     bbox,
      dx:       0,          // offset drag dari posisi target
      dy:       0,
      placed:   false,
      inPanel:  true,
      dragOffX: 0,
      dragOffY: 0,
      hue:      (i * 31 + 120) % 360,
    }};
  }});

  const totalPieces = pieces.length;

  // ===== THUMBNAIL DI PANEL =====
  const THUMB_W = 90, THUMB_H = 80;
  const piecesContainer = document.getElementById('pieces-container');

  function buildThumbnails() {{
    piecesContainer.innerHTML = '';
    pieces.forEach(p => {{
      const div = document.createElement('div');
      div.className = 'piece-thumb' + (p.placed ? ' placed' : '');
      div.id  = 'thumb-' + p.id;
      div.style.width  = THUMB_W + 'px';
      div.style.height = THUMB_H + 'px';
      div.title = p.name;

      const tc  = document.createElement('canvas');
      tc.width  = THUMB_W;
      tc.height = THUMB_H;
      drawThumb(p, tc.getContext('2d'));
      div.appendChild(tc);

      // Label nama singkat
      const lbl = document.createElement('div');
      lbl.className = 'piece-label';
      // Singkat: hapus "Kabupaten " / "Kota "
      lbl.textContent = p.name.replace('Kabupaten ','').replace('Kota ','');
      div.appendChild(lbl);

      div.addEventListener('mousedown', e => startDragPanel(e, p));
      div.addEventListener('touchstart', e => startDragPanelTouch(e, p), {{passive:false}});
      piecesContainer.appendChild(div);
    }});
  }}

  function drawThumb(piece, tctx) {{
    tctx.clearRect(0, 0, THUMB_W, THUMB_H);
    const bb = piece.bbox;
    if(bb.w < 0.5 || bb.h < 0.5) return;
    const tpad = 5;
    const ts   = Math.min((THUMB_W-tpad*2)/bb.w, (THUMB_H-tpad*2-10)/bb.h);
    const offX = tpad + (THUMB_W-tpad*2 - bb.w*ts)/2 - bb.x1*ts;
    const offY = tpad + (THUMB_H-tpad*2-10 - bb.h*ts)/2 - bb.y1*ts;

    tctx.save();
    tctx.setTransform(ts, 0, 0, ts, offX, offY);

    const lp = new Path2D();
    function addRingLocal(ring) {{
      ring.forEach((c,i) => {{
        const [x,y] = project(c[0],c[1]);
        if(i===0) lp.moveTo(x,y); else lp.lineTo(x,y);
      }});
      lp.closePath();
    }}
    piece.geometry.coordinates.forEach ? 
      (piece.geometry.type === 'MultiPolygon' 
        ? piece.geometry.coordinates.forEach(poly => poly.forEach(addRingLocal))
        : piece.geometry.coordinates.forEach(addRingLocal))
      : null;

    tctx.shadowColor = 'rgba(0,0,0,0.5)';
    tctx.shadowBlur  = 4/ts;
    tctx.fillStyle   = `hsla(${{piece.hue}},68%,56%,0.92)`;
    tctx.fill(lp);
    tctx.shadowBlur  = 0;
    tctx.strokeStyle = 'rgba(255,255,255,0.8)';
    tctx.lineWidth   = 1.5/ts;
    tctx.stroke(lp);
    tctx.restore();
  }}

  buildThumbnails();

  // ===== DRAG STATE =====
  let dragging = null;
  let mouseX = 0, mouseY = 0;
  let mistakes = 0;

  function canvasPos(e) {{
    const rect = canvas.getBoundingClientRect();
    const cx   = e.touches ? e.touches[0].clientX : e.clientX;
    const cy   = e.touches ? e.touches[0].clientY : e.clientY;
    return [
      (cx - rect.left) * (W / rect.width),
      (cy - rect.top)  * (H / rect.height)
    ];
  }}

  function startDragPanel(e, piece) {{
    e.preventDefault();
    if(piece.placed) return;
    dragging = piece;
    piece.inPanel = false;
    const [mx,my] = canvasPos(e);
    piece.dx = mx - piece.centroid[0];
    piece.dy = my - piece.centroid[1];
    piece.dragOffX = 0; piece.dragOffY = 0;
    mouseX=mx; mouseY=my;
    render();
  }}

  function startDragPanelTouch(e, piece) {{
    e.preventDefault();
    if(piece.placed) return;
    dragging = piece;
    piece.inPanel = false;
    const touch = e.touches[0];
    const rect  = canvas.getBoundingClientRect();
    const mx = (touch.clientX-rect.left)*(W/rect.width);
    const my = (touch.clientY-rect.top)*(H/rect.height);
    piece.dx = mx - piece.centroid[0];
    piece.dy = my - piece.centroid[1];
    piece.dragOffX = 0; piece.dragOffY = 0;
    mouseX=mx; mouseY=my;
    render();
  }}

  canvas.addEventListener('mousedown', e => {{
    const [mx,my] = canvasPos(e);
    for(let i=pieces.length-1; i>=0; i--) {{
      const p = pieces[i];
      if(p.placed || p.inPanel) continue;
      const bb = p.bbox;
      if(mx >= bb.x1+p.dx-4 && mx <= bb.x2+p.dx+4 &&
         my >= bb.y1+p.dy-4 && my <= bb.y2+p.dy+4) {{
        dragging = p;
        const pcx = p.centroid[0] + p.dx;
        const pcy = p.centroid[1] + p.dy;
        p.dragOffX = mx - pcx;
        p.dragOffY = my - pcy;
        mouseX=mx; mouseY=my;
        render();
        break;
      }}
    }}
  }});

  document.addEventListener('mousemove', e => {{
    if(!dragging) return;
    const [mx,my] = canvasPos(e);
    mouseX=mx; mouseY=my;
    dragging.dx = mx - dragging.centroid[0] - dragging.dragOffX;
    dragging.dy = my - dragging.centroid[1] - dragging.dragOffY;
    render();

    // Tooltip: tunjukkan nama wilayah yang sedang di-drag
    const tt = document.getElementById('tooltip');
    tt.textContent = dragging.name;
    tt.style.left  = Math.min(mx+12, W-120) + 'px';
    tt.style.top   = Math.max(my-28, 5) + 'px';
    tt.style.display = 'block';
  }});

  document.addEventListener('mouseup', () => {{
    document.getElementById('tooltip').style.display = 'none';
    if(dragging) {{
      trySnap(dragging, mouseX, mouseY);
      dragging = null;
      render();
    }}
  }});

  canvas.addEventListener('touchmove', e => {{
    e.preventDefault();
    if(!dragging) return;
    const [mx,my] = canvasPos(e);
    mouseX=mx; mouseY=my;
    dragging.dx = mx - dragging.centroid[0] - dragging.dragOffX;
    dragging.dy = my - dragging.centroid[1] - dragging.dragOffY;
    render();
  }}, {{passive:false}});

  document.addEventListener('touchend', () => {{
    if(dragging) {{
      trySnap(dragging, mouseX, mouseY);
      dragging = null;
      render();
    }}
  }});

  // ===== SNAP =====
  // Wilayah kepulauan: centroid bisa bergeser, beri toleransi ekstra
  const KEPULAUAN_BONUS = {{
    'Kabupaten Sumenep': 2.2,   // kepulauan sangat tersebar (Kangean, Masalembu)
    'Kabupaten Bangkalan': 1.4,
    'Kabupaten Sampang':  1.4,
    'Kabupaten Pamekasan':1.4,
    'Kabupaten Gresik':   1.3,  // ada Pulau Bawean
  }};

  function trySnap(piece, dropX, dropY) {{
    const tx   = piece.centroid[0];
    const ty   = piece.centroid[1];
    const dist = Math.hypot(dropX - tx, dropY - ty);

    // Threshold dasar: akar luas bbox (lebih representatif dari min dimension)
    const bb     = piece.bbox;
    const sqrtArea = Math.sqrt(bb.w * bb.h);
    const baseThr  = Math.max(SNAP_DIST, Math.min(sqrtArea * 0.45, 72));

    // Bonus threshold untuk wilayah kepulauan
    const bonus  = KEPULAUAN_BONUS[piece.name] || 1.0;
    const thr    = baseThr * bonus * (W / 680);

    if(dist <= thr) {{
      piece.dx = 0; piece.dy = 0;
      piece.placed = true; piece.inPanel = false;
      showFB(dropX, dropY, true);
      const el = document.getElementById('thumb-'+piece.id);
      if(el) el.classList.add('placed');
      updateProgress();
      checkWin();
    }} else {{
      mistakes++;
      showFB(dropX, dropY, false);
      updateAccuracy();
      // Kepingan tetap mengambang di posisi drop
    }}
  }}

  function showFB(x, y, ok) {{
    const fb = document.getElementById('snap-feedback');
    fb.textContent = ok ? '✅' : '❌';
    fb.style.left = Math.min(x, W-50)+'px';
    fb.style.top  = Math.max(y-35, 5)+'px';
    fb.style.display = 'block';
    fb.style.animation = 'none';
    fb.offsetHeight;
    fb.style.animation = 'floatUp 0.8s ease-out forwards';
    setTimeout(() => {{ fb.style.display='none'; }}, 800);
  }}

  function updateProgress() {{
    const pl  = pieces.filter(p=>p.placed).length;
    const pct = Math.round((pl/totalPieces)*100);
    document.getElementById('placed-count').textContent        = pl;
    document.getElementById('progress-bar-fill').style.width  = pct+'%';
    document.getElementById('progress-bar-fill2').style.width = pct+'%';
    document.getElementById('progress-text').textContent =
      pl===totalPieces ? '🎉 Peta Jawa Timur lengkap!' : pl+'/'+totalPieces+' kepingan terpasang';
  }}

  function updateAccuracy() {{
    const pl  = pieces.filter(p=>p.placed).length;
    const tot = pl + mistakes;
    document.getElementById('accuracy-display').textContent =
      tot > 0 ? Math.round((pl/tot)*100)+'%' : '100%';
  }}

  function checkWin() {{
    if(pieces.filter(p=>p.placed).length >= totalPieces) {{
      const e = Math.floor((Date.now()-START_TIME)/1000);
      const m = Math.floor(e/60);
      const s = e % 60;
      document.getElementById('win-time').textContent =
        String(m).padStart(2,'0')+':'+String(s).padStart(2,'0');
      document.getElementById('win-moves').textContent = mistakes+' kesalahan';
      // Tampilkan overlay — user scroll ke bawah untuk simpan skor via tombol Streamlit
      setTimeout(() => document.getElementById('win-overlay').classList.add('show'), 600);
    }}
  }}

  // ===== TIMER =====
  setInterval(() => {{
    const e = Math.floor((Date.now()-START_TIME)/1000);
    document.getElementById('timer-display').textContent =
      String(Math.floor(e/60)).padStart(2,'0')+':'+String(e%60).padStart(2,'0');
  }}, 1000);

  // ===== RENDER =====
  function drawPiece(piece, dx, dy, isDrag) {{
    ctx.save();
    ctx.translate(dx, dy);

    ctx.shadowColor = isDrag ? 'rgba(255,215,0,0.9)' : 'rgba(0,0,0,0.5)';
    ctx.shadowBlur  = isDrag ? 22 : 8;
    ctx.fillStyle   = `hsla(${{piece.hue}}, ${{isDrag?82:66}}%, ${{isDrag?66:54}}%, ${{isDrag?0.96:0.82}})`;
    ctx.fill(piece.path);

    ctx.shadowBlur  = 0;
    ctx.strokeStyle = isDrag ? '#ffd700' : 'rgba(255,255,255,0.65)';
    ctx.lineWidth   = isDrag ? 2.5 : 1.2;
    ctx.stroke(piece.path);

    // Label nama wilayah di peta (hanya jika tidak di-drag & wilayah cukup besar)
    if(!isDrag) {{
      const bb = piece.bbox;
      if(bb.w > 18 && bb.h > 10) {{
        const cx_ = (bb.x1+bb.x2)/2;
        const cy_ = (bb.y1+bb.y2)/2;
        ctx.fillStyle    = 'rgba(255,255,255,0.92)';
        ctx.font         = 'bold 7.5px Nunito,sans-serif';
        ctx.textAlign    = 'center';
        ctx.textBaseline = 'middle';
        ctx.shadowColor  = 'rgba(0,0,0,0.9)';
        ctx.shadowBlur   = 3;
        // Singkat nama
        const short = piece.name.replace('Kabupaten ','').replace('Kota ','★');
        ctx.fillText(short, cx_, cy_);
        ctx.shadowBlur = 0;
      }}
    }}
    ctx.restore();
  }}

  function render() {{
    ctx.clearRect(0, 0, W, H);

    // 1. Ghost outline semua wilayah (panduan posisi)
    pieces.forEach(p => {{
      if(p.placed) return;
      ctx.save();
      ctx.setLineDash([4,3]);
      ctx.strokeStyle = 'rgba(255,215,0,0.18)';
      ctx.lineWidth   = 1;
      ctx.stroke(p.path);
      ctx.setLineDash([]);
      ctx.fillStyle = 'rgba(255,255,255,0.03)';
      ctx.fill(p.path);
      ctx.restore();
    }});

    // 2. Kepingan terpasang
    pieces.forEach(p => {{
      if(!p.placed) return;
      drawPiece(p, 0, 0, false);
    }});

    // 3. Kepingan mengambang (tidak di panel, bukan yang di-drag)
    pieces.forEach(p => {{
      if(p.placed || p.inPanel || p === dragging) return;
      drawPiece(p, p.dx, p.dy, false);
    }});

    // 4. Kepingan sedang di-drag (paling atas)
    if(dragging && !dragging.placed) {{
      drawPiece(dragging, dragging.dx, dragging.dy, true);
    }}
  }}

  render();

  // ===== KONTROL =====
  window.shufflePieces = function() {{
    const margin = 30;
    pieces.forEach(p => {{
      if(p.placed) return;
      p.inPanel = false;
      // Scatter acak di seluruh area canvas
      const bb = p.bbox;
      p.dx = (Math.random() * (W - margin*2 - bb.w) + margin) - bb.x1;
      p.dy = (Math.random() * (H - margin*2 - bb.h) + margin) - bb.y1;
    }});
    render();
  }};

  window.showHint = function() {{
    // Flash outline seluruh Jawa Timur
    let n=0;
    const iv = setInterval(() => {{
      if(++n > 8) {{ clearInterval(iv); render(); return; }}
      ctx.save();
      pieces.forEach(p => {{
        ctx.strokeStyle = n%2===0 ? `hsla(${{p.hue}},80%,60%,0.8)` : 'rgba(255,255,255,0.05)';
        ctx.lineWidth   = 2.5;
        ctx.stroke(p.path);
      }});
      ctx.restore();
    }}, 200);
  }};

  window.resetPuzzle = function() {{
    mistakes = 0;
    pieces.forEach(p => {{
      p.placed=false; p.inPanel=true; p.dx=0; p.dy=0;
    }});
    document.getElementById('accuracy-display').textContent = '100%';
    buildThumbnails();
    updateProgress();
    render();
  }};

  window.autoSolve = function() {{
    const unplaced = pieces.filter(p=>!p.placed);
    let i=0;
    const iv = setInterval(() => {{
      if(i>=unplaced.length) {{ clearInterval(iv); checkWin(); return; }}
      const p = unplaced[i++];
      p.dx=0; p.dy=0; p.placed=true; p.inPanel=false;
      const el = document.getElementById('thumb-'+p.id);
      if(el) el.classList.add('placed');
      updateProgress(); render();
    }}, 80);
  }};

  // Scatter awal
  shufflePieces();

}})();
</script>
</body>
</html>"""

    return html


# ==================== BACA HASIL PUZZLE DARI JS (query_params) ====================
# JS tutupOverlayDanSimpan() menulis ?puzzle_waktu=X&puzzle_salah=Y ke URL lalu reload
# Python cukup menyimpan ke session state — penyimpanan ke papan skor lewat tombol


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
            "<p>✨ Fitur: 🎮 Quiz | 📚 Info Wilayah | 🧩 Puzzle | 🌋 Bromo 3D | 🏛️ Balaikota 3D | 🏆 Papan Skor | 🎵 Musik Latar</p></div>",
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
                    © 2026 <strong>Program Pengabdian Masyarakat</strong> — Penguatan Literasi Geospasial Jawa Timur Bagi Gen Z Melalui Edukasi Berbasis Gamifikasi Menggunakan Platform" <em>"Sepiro Jatim, Sampeyan"</em><br>
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
    st.title("🧩 Ensiklopedia Jatim")

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

    # ==================== PERUBAHAN: "Belajar" -> "Info Wilayah", "Game" -> "Quiz" ====================
    menu_options = ["📚 Info Wilayah", "🎮 Quiz", "🧩 Puzzle", "🌋 Bromo 3D", "🏛️ Balaikota 3D",
                    "🏆 Papan Skor", "⏱️ Statistik Waktu", "⚙️ Pengaturan", "ℹ️ Tentang"]
    # Terapkan pending navigation sebelum widget radio dirender
    if st.session_state.get("pending_navigation"):
        _target = st.session_state.pending_navigation
        st.session_state.pending_navigation = None
        if _target in menu_options:
            st.session_state["main_navigation"] = _target
    selected_menu = st.radio("Menu", menu_options,
                             index=menu_options.index(st.session_state.get("main_navigation", menu_options[0]))
                                   if st.session_state.get("main_navigation") in menu_options else 0,
                             label_visibility="collapsed", key="main_navigation")

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
        total_kab = len(jatim_geojson.get("features", []))
        st.markdown(
            f"<div style='background:linear-gradient(135deg,#FF9800,#f57c00);"
            f"padding:12px;border-radius:10px;text-align:center;color:white;margin-bottom:10px;'>"
            f"<div style='font-size:1.6em;'>⚡</div>"
            f"<div style='font-weight:900;font-size:1.1em;'>Level Normal</div>"
            f"<div style='font-size:0.85em;opacity:0.9;'>{total_kab} kepingan kab/kota</div>"
            f"</div>",
            unsafe_allow_html=True
        )
        st.info(
            f"🗺️ **Puzzle Peta Jawa Timur**\n\n"
            f"Susun **{total_kab} kepingan** kabupaten/kota\n"
            f"menjadi peta Jawa Timur yang utuh!"
        )
        st.markdown("---")
        if st.button("▶️ Mulai Puzzle", use_container_width=True, type="primary"):
            st.session_state.puzzle_started     = True
            st.session_state.puzzle_start_time  = time.time()
            st.session_state.puzzle_score_saved = False
            st.session_state.puzzle_result_time_sec = None
            st.session_state.puzzle_result_errors   = None
            st.rerun()
        if st.session_state.puzzle_started:
            if st.button("⛔ Keluar Puzzle", use_container_width=True):
                st.session_state.puzzle_started = False
                st.rerun()

    elif PAGE == "Info Wilayah":
        st.header("📚 Info Wilayah")
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
        # --- Quiz summary ---
        st.markdown("**🎮 Quiz**")
        sb    = get_filtered_scoreboard(
            st.session_state.get("scoreboard_level_filter", "Semua Level"),
            st.session_state.get("scoreboard_time_filter", "Semua Waktu")
        )
        stats = get_scoreboard_stats(sb)
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Pemain Quiz", stats["total_pemain"])
        with c2:
            if sb:
                st.metric("Skor Tertinggi", f"{stats['skor_tertinggi']}/{sb[0]['total_soal']}")
        st.markdown("---")
        # --- Puzzle summary ---
        st.markdown("**🧩 Puzzle**")
        psb   = load_puzzle_scoreboard()
        pstats = get_puzzle_scoreboard_stats(psb)
        cp1, cp2 = st.columns(2)
        with cp1:
            st.metric("Entri Puzzle", pstats.get("total_entri", 0))
        with cp2:
            wt = pstats["waktu_tercepat"]
            st.metric("⚡ Tercepat", wt.get("waktu_format", "-") if wt else "-")
        if psb:
            st.success(f"👑 Juara: {psb[0].get('nama','-')}")

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
        st.markdown("**Sepiro Jawa Timur, Sampeyan** v2.9.0\n\nAplikasi interaktif Pembelajaran Geospasial Jawa Timur.")

# Expose PAGE for main content area
PAGE = st.session_state.get("main_navigation", "📚 Info Wilayah")
PAGE = PAGE.split(" ", 1)[1] if " " in PAGE else PAGE


# ==================== KONTEN UTAMA ====================

# --- HALAMAN QUIZ ---
if PAGE == "Quiz":
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
    st.title("🧩 Puzzle Peta Jawa Timur")

    total_kab = len(jatim_geojson.get("features", []))

    # Info banner
    st.markdown(
        f"""
        <div style='background:linear-gradient(135deg,#FF9800,#f57c00);
            border-radius:14px;padding:16px 20px;margin-bottom:16px;
            display:flex;align-items:center;gap:16px;flex-wrap:wrap;'>
          <div style='font-size:2.5em;'>🧩</div>
          <div>
            <div style='color:white;font-size:1.2em;font-weight:900;'>
              Puzzle Peta Jawa Timur — Level Normal
            </div>
            <div style='color:rgba(255,255,255,0.9);font-size:0.9em;margin-top:3px;'>
              Susun <strong>{total_kab} kepingan</strong> kabupaten/kota
              menjadi peta Jawa Timur yang utuh!
            </div>
          </div>
          <div style='margin-left:auto;background:rgba(255,255,255,0.2);
            border-radius:10px;padding:8px 14px;text-align:center;color:white;'>
            <div style='font-size:1.5em;font-weight:900;'>{total_kab}</div>
            <div style='font-size:0.75em;'>Kab/Kota</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.puzzle_started and not st.session_state.puzzle_completed and not st.session_state.puzzle_score_saved:
        # Pratinjau peta + tombol mulai
        st.markdown("### 🗺️ Pratinjau Peta Jawa Timur")

        col_prev, col_info = st.columns([3, 1])
        with col_prev:
            m_prev = folium.Map(location=[-7.5, 112.3], zoom_start=7, tiles=None)
            folium.TileLayer(
                tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                attr="Esri", name="Satellite"
            ).add_to(m_prev)
            folium.GeoJson(
                jatim_geojson,
                style_function=lambda f: {
                    "fillColor": "#FF9800", "color": "#ffffff",
                    "weight": 1.5, "fillOpacity": 0.55
                },
                tooltip=folium.GeoJsonTooltip(fields=["name"], aliases=["Wilayah:"]),
            ).add_to(m_prev)
            st_folium(m_prev, width=None, height=380, use_container_width=True, key="puzzle_preview_map")

        with col_info:
            st.markdown(
                f"""
                <div style='background:linear-gradient(135deg,#1a1a2e,#16213e);
                    border:2px solid #FF9800;border-radius:14px;padding:18px;
                    text-align:center;color:white;'>
                  <div style='font-size:2.2em;margin-bottom:8px;'>⚡</div>
                  <div style='font-size:1em;font-weight:900;color:#FF9800;margin-bottom:6px;'>
                    Level Normal
                  </div>
                  <div style='font-size:2em;font-weight:900;color:#ffd700;'>{total_kab}</div>
                  <div style='font-size:0.82em;color:rgba(255,255,255,0.7);'>kepingan kab/kota</div>
                  <hr style='border-color:rgba(255,255,255,0.15);margin:12px 0;'>
                  <div style='font-size:0.78em;color:rgba(255,255,255,0.65);line-height:1.5;'>
                    Setiap kepingan adalah<br>bentuk asli wilayah<br>administrasi GeoJSON
                  </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown("")
            if st.button("▶️ MULAI PUZZLE!", use_container_width=True, type="primary"):
                st.session_state.puzzle_started     = True
                st.session_state.puzzle_start_time  = time.time()
                st.session_state.puzzle_score_saved = False
                st.session_state.puzzle_result_time_sec = None
                st.session_state.puzzle_result_errors   = None
                st.rerun()

        st.markdown("---")
        st.info(
            "💡 **Cara Bermain:**\n"
            "1. Klik **MULAI PUZZLE!** untuk memulai\n"
            "2. Seret kepingan dari panel kanan ke area peta\n"
            "3. Setiap kepingan adalah bentuk asli kabupaten/kota\n"
            "4. Kepingan akan *snap* otomatis jika ditempatkan di posisi yang benar\n"
            "5. Susun semua kepingan untuk melengkapi peta Jawa Timur!"
        )

    elif st.session_state.puzzle_started:
        # PUZZLE AKTIF
        h1, h2 = st.columns([3, 1])
        with h1:
            st.markdown(
                f"<div style='background:linear-gradient(135deg,#FF9800,#f57c00);"
                f"padding:10px 16px;border-radius:10px;color:white;'>"
                f"<strong>⚡ Puzzle Peta Jawa Timur — {total_kab} kepingan kab/kota</strong></div>",
                unsafe_allow_html=True
            )
        with h2:
            if st.button("⛔ Keluar Puzzle", use_container_width=True):
                st.session_state.puzzle_started = False
                st.rerun()

        st.markdown("")

        puzzle_html = get_puzzle_html(
            jatim_geojson,
            int(st.session_state.puzzle_start_time * 1000) if st.session_state.puzzle_start_time else 0
        )
        st.components.v1.html(puzzle_html, height=820, scrolling=True)

        st.markdown("---")
        st.info(
            "💡 Seret kepingan dari panel kanan → lepas di posisi yang tepat → "
            "kepingan *snap* otomatis jika benar. "
            "Klik **💡 Petunjuk** untuk melihat outline panduan."
        )

        # Tombol Streamlit "Saya Sudah Selesai" — tidak bergantung iframe JS
        st.markdown("---")
        st.markdown(
            "<div style='background:linear-gradient(135deg,#1a1a2e,#16213e);"
            "border:2px solid #ffd700;border-radius:12px;padding:14px 18px;"
            "margin-bottom:8px;text-align:center;'>"
            "<div style='color:#ffd700;font-weight:900;font-size:1.05em;'>🏆 Puzzle Selesai?</div>"
            "<div style='color:rgba(255,255,255,0.7);font-size:0.85em;margin-top:4px;'>"
            "Klik tombol di bawah setelah semua kepingan terpasang untuk menyimpan skor</div>"
            "</div>",
            unsafe_allow_html=True
        )
        if st.button(
            "✅ Saya Sudah Selesai — Catat Waktu & Simpan Skor",
            use_container_width=True,
            type="primary",
            key="btn_puzzle_selesai"
        ):
            waktu_selesai = int(time.time() - st.session_state.puzzle_start_time)                             if st.session_state.puzzle_start_time else 0
            st.session_state.puzzle_js_waktu  = waktu_selesai
            st.session_state.puzzle_js_errors = 0   # user isi sendiri di form
            st.session_state.puzzle_completed = True
            st.session_state.puzzle_started   = False
            st.rerun()

    # ===== HASIL PUZZLE & FORM SIMPAN SKOR =====
    # Ditampilkan ketika puzzle_completed = True (dari JS) atau puzzle_score_saved = True
    if st.session_state.puzzle_completed or st.session_state.puzzle_score_saved:
        _js_wkt = st.session_state.get("puzzle_js_waktu")
        _js_err = st.session_state.get("puzzle_js_errors", 0)

        if st.session_state.puzzle_score_saved:
            # Skor sudah disimpan
            wt  = st.session_state.puzzle_result_time_sec or 0
            err = st.session_state.puzzle_result_errors   or 0
            wm, ws  = divmod(int(wt), 60)
            penalti = int(wt) + err * 10
            st.markdown("### 🏆 Puzzle Selesai!")
            st.success(
                f"✅ **Skor berhasil disimpan ke Papan Skor!** — "
                f"⏱️ {wm:02d}:{ws:02d} | ❌ {err} kesalahan | 📊 Penalti: {penalti}"
            )
            cola, colb = st.columns(2)
            with cola:
                if st.button("🔄 Main Puzzle Lagi", use_container_width=True,
                             type="primary", key="btn_puzzle_ulang"):
                    st.session_state.puzzle_started         = False
                    st.session_state.puzzle_start_time      = None
                    st.session_state.puzzle_completed       = False
                    st.session_state.puzzle_score_saved     = False
                    st.session_state.puzzle_result_time_sec = None
                    st.session_state.puzzle_result_errors   = None
                    st.session_state.puzzle_js_waktu        = None
                    st.session_state.puzzle_js_errors       = None
                    st.rerun()
            with colb:
                if st.button("🏆 Lihat Papan Skor Puzzle", use_container_width=True,
                             key="btn_lihat_papan"):
                    st.session_state.pending_navigation = "🏆 Papan Skor"
                    st.rerun()

        elif _js_wkt:
            # Puzzle selesai, belum disimpan — tampilkan form simpan bergaya Quiz
            wm, ws = divmod(int(_js_wkt), 60)

            st.markdown("### 🏆 Puzzle Selesai!")
            st.markdown(
                f"""
                <div style='background:linear-gradient(135deg,#1a1a2e,#16213e);
                    border:2px solid #ffd700;border-radius:14px;padding:18px 22px;
                    margin-bottom:14px;'>
                  <div style='display:flex;flex-wrap:wrap;gap:24px;align-items:center;'>
                    <div style='text-align:center;'>
                      <div style='color:rgba(255,255,255,0.55);font-size:0.78em;'>⏱️ WAKTU TERCATAT</div>
                      <div style='color:#ffd700;font-size:2em;font-weight:900;'>{wm:02d}:{ws:02d}</div>
                    </div>
                    <div style='margin-left:auto;'>
                      <div style='color:rgba(255,255,255,0.55);font-size:0.78em;'>👤 PEMAIN</div>
                      <div style='color:#ffd700;font-weight:bold;'>⭐ {st.session_state.user_name}</div>
                    </div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Inisialisasi nilai kesalahan di session state agar tersimpan antar render
            if "puzzle_input_kesalahan" not in st.session_state:
                st.session_state.puzzle_input_kesalahan = 0

            with st.form("puzzle_save_form"):
                st.markdown(f"**Nama:** {st.session_state.user_name}")
                st.markdown(f"**Waktu:** `{wm:02d}:{ws:02d}`")
                st.number_input(
                    "❌ Jumlah Kesalahan (lihat angka di layar puzzle)",
                    min_value=0, max_value=999, step=1,
                    key="puzzle_input_kesalahan"
                )
                st.caption("💡 Penalti = Waktu (detik) + Kesalahan × 10 — makin kecil makin baik")
                c_save, c_skip = st.columns(2)
                with c_save:
                    simpan = st.form_submit_button(
                        "💾 Simpan Skor ke Papan Skor",
                        use_container_width=True,
                        type="primary"
                    )
                with c_skip:
                    skip = st.form_submit_button(
                        "🔄 Main Lagi (tanpa simpan)",
                        use_container_width=True
                    )

            # Baca nilai dari session_state (bukan dari variabel lokal)
            # agar nilai yang diinput user benar-benar tersimpan saat submit
            if simpan:
                _kesalahan = int(st.session_state.get("puzzle_input_kesalahan", 0))
                if add_puzzle_score(st.session_state.user_name, _js_wkt, _kesalahan):
                    st.session_state.puzzle_score_saved          = True
                    st.session_state.puzzle_completed            = False
                    st.session_state.puzzle_result_time_sec      = _js_wkt
                    st.session_state.puzzle_result_errors        = _kesalahan
                    st.session_state.puzzle_js_waktu             = None
                    st.session_state.puzzle_js_errors            = None
                    st.session_state.puzzle_input_kesalahan      = 0
                    st.rerun()
                else:
                    st.error("❌ Gagal menyimpan skor.")

            if skip:
                st.session_state.puzzle_started          = False
                st.session_state.puzzle_start_time       = None
                st.session_state.puzzle_completed        = False
                st.session_state.puzzle_js_waktu         = None
                st.session_state.puzzle_js_errors        = None
                st.session_state.puzzle_input_kesalahan  = 0
                st.rerun()

        else:
            # puzzle_completed = True tapi js_waktu kosong (edge case)
            st.info("💡 Data hasil puzzle tidak ditemukan. Silakan main puzzle lagi.")
            if st.button("🔄 Main Puzzle Lagi", key="btn_puzzle_retry"):
                st.session_state.puzzle_completed = False
                st.session_state.puzzle_started   = False
                st.rerun()


# ==================== HALAMAN INFO WILAYAH (dengan logo) ====================
elif PAGE == "Info Wilayah":
    st.title("📚 Info Wilayah Jawa Timur")
    st.markdown("**Klik wilayah pada peta** untuk melihat informasi lengkap!")
    
    # Buat layout 2 kolom untuk peta dan info
    col_map, col_info = st.columns([2, 1])
    
    with col_map:
        m = folium.Map(location=[-7.5, 112.3], zoom_start=8,
                       tiles=None, control_scale=True, prefer_canvas=True)
        folium.TileLayer(
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Esri", name="Satellite", overlay=False, control=False
        ).add_to(m)

        def style_function(feature):
            return {"fillColor": "#33cc33", "color": "#ffffff",
                    "weight": 1.5, "fillOpacity": 0.5}

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

        map_data = st_folium(m, width=None, height=500, use_container_width=True,
                             key="belajar_map")

        if map_data:
            clicked = map_data.get("last_active_drawing")
            if clicked and "properties" in clicked and "name" in clicked["properties"]:
                clicked_name = clicked["properties"]["name"]
                if clicked_name != st.session_state.selected_wilayah_info:
                    st.session_state.selected_wilayah_info = clicked_name
                    st.rerun()
    
    with col_info:
        st.markdown("## 📋 Info Wilayah")
        
        if st.session_state.selected_wilayah_info:
            wil = st.session_state.selected_wilayah_info
            
            # Ambil logo URL
            logo_url = get_logo_url(wil)
            
            # Tampilkan header dengan logo dan nama wilayah
            if logo_url:
                col_logo, col_title = st.columns([1, 3])
                with col_logo:
                    st.image(logo_url, width=80)
                with col_title:
                    st.markdown(
                        f"<div style='background:linear-gradient(135deg,#667eea,#764ba2);"
                        f"padding:15px;border-radius:10px;height:100%;display:flex;align-items:center;'>"
                        f"<h3 style='color:#ffd700;margin:0;'>📍 {wil}</h3>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
            else:
                st.markdown(
                    f"<div style='background:linear-gradient(135deg,#667eea,#764ba2);"
                    f"padding:15px;border-radius:10px;margin-bottom:15px;'>"
                    f"<h3 style='color:#ffd700;margin:0;text-align:center;'>📍 {wil}</h3>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            
            # Ambil info wilayah
            info = get_wilayah_info(wil)
            
            with st.expander("🗺️ Geografis", expanded=True):
                st.write(info["geografis"])
            
            with st.expander("👥 Demografi", expanded=True):
                st.write(info["demografi"])
            
            with st.expander("🎭 Budaya", expanded=True):
                st.write(info["budaya"])
            
            with st.expander("✨ Keunikan", expanded=True):
                st.write(info["keunikan"])
            
            with st.expander("🛍️ Oleh-oleh", expanded=True):
                st.write(info["oleh_oleh"])
            
            if st.button("🔄 Klik wilayah lain", use_container_width=True):
                st.session_state.selected_wilayah_info = None
                st.rerun()
        else:
            st.markdown(
                "<div style='background:linear-gradient(135deg,#f8f9fa,#e9ecef);"
                "padding:30px 20px;border-radius:10px;text-align:center;"
                "border:3px dashed #667eea;'>"
                "<h4 style='color:#667eea;margin-bottom:15px;'>👆 Klik Wilayah di Peta</h4>"
                "<p style='color:#666;font-size:16px;'>Klik wilayah pada peta untuk melihat:</p>"
                "<div style='display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin-top:15px;'>"
                "<span style='background:#667eea;color:white;padding:5px 15px;border-radius:20px;'>🗺️ Geografis</span>"
                "<span style='background:#764ba2;color:white;padding:5px 15px;border-radius:20px;'>👥 Demografi</span>"
                "<span style='background:#43b89c;color:white;padding:5px 15px;border-radius:20px;'>🎭 Budaya</span>"
                "<span style='background:#ff9800;color:white;padding:5px 15px;border-radius:20px;'>✨ Keunikan</span>"
                "<span style='background:#e05c8a;color:white;padding:5px 15px;border-radius:20px;'>🛍️ Oleh-oleh</span>"
                "</div></div>",
                unsafe_allow_html=True
            )
            
            with st.expander("📌 Atau pilih dari daftar"):
                popular_regions = [
                    "Kabupaten Banyuwangi", "Kabupaten Malang", "Kota Surabaya",
                    "Kota Batu", "Kabupaten Jember", "Kota Malang",
                    "Kabupaten Sidoarjo", "Kabupaten Ponorogo", "Kabupaten Pacitan",
                    "Kabupaten Bondowoso", "Kabupaten Lumajang", "Kota Kediri",
                    "Kabupaten Kediri", "Kabupaten Madiun", "Kota Madiun",
                    "Kabupaten Blitar", "Kota Blitar", "Kabupaten Pasuruan",
                    "Kota Pasuruan", "Kabupaten Probolinggo", "Kota Probolinggo",
                    "Kabupaten Mojokerto", "Kota Mojokerto"
                ]
                
                col_reg1, col_reg2 = st.columns(2)
                half = len(popular_regions) // 2 + len(popular_regions) % 2
                
                for i, region in enumerate(popular_regions[:half]):
                    with col_reg1:
                        logo_preview = get_logo_url(region)
                        if logo_preview:
                            col_btn_logo, col_btn_text = st.columns([1, 3])
                            with col_btn_logo:
                                st.image(logo_preview, width=25)
                            with col_btn_text:
                                if st.button(region, key=f"quick_{region}", use_container_width=True):
                                    st.session_state.selected_wilayah_info = region
                                    st.rerun()
                        else:
                            if st.button(region, key=f"quick_{region}", use_container_width=True):
                                st.session_state.selected_wilayah_info = region
                                st.rerun()
                
                for i, region in enumerate(popular_regions[half:]):
                    with col_reg2:
                        logo_preview = get_logo_url(region)
                        if logo_preview:
                            col_btn_logo, col_btn_text = st.columns([1, 3])
                            with col_btn_logo:
                                st.image(logo_preview, width=25)
                            with col_btn_text:
                                if st.button(region, key=f"quick_{region}_{i}", use_container_width=True):
                                    st.session_state.selected_wilayah_info = region
                                    st.rerun()
                        else:
                            if st.button(region, key=f"quick_{region}_{i}", use_container_width=True):
                                st.session_state.selected_wilayah_info = region
                                st.rerun()


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

    tab_quiz, tab_puzzle = st.tabs(["🎮 Quiz Tebak Wilayah", "🧩 Puzzle Peta Jawa Timur"])

    # =========================================================
    # TAB 1 — QUIZ
    # =========================================================
    with tab_quiz:
        st.markdown("### 🎮 Papan Skor Quiz")
        st.caption("Peringkat: Skor tertinggi → Waktu tercepat → Terbaru")

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            lf = st.selectbox(
                "Filter level:",
                ["Semua Level", "Mudah", "Normal", "Sulit"],
                key="scoreboard_level_filter"
            )
        with col_f2:
            tf = st.selectbox(
                "Filter waktu:",
                ["Semua Waktu", "Hari Ini", "7 Hari Terakhir", "30 Hari Terakhir", "Bulan Ini"],
                key="scoreboard_time_filter"
            )

        scoreboard = get_filtered_scoreboard(lf, tf)
        stats      = get_scoreboard_stats(scoreboard)

        if scoreboard:
            rows = []
            for i, p in enumerate(scoreboard[:10], 1):
                icon = {1: "👑", 2: "🥈", 3: "🥉"}.get(i, f"{i}.")
                nm   = p.get("nama", "Unknown")
                if nm == st.session_state.user_name:
                    nm = f"⭐ {nm} (Kamu)"
                dur  = p.get("durasi", {}).get("format", "-") if p.get("durasi") else "-"
                rows.append({
                    "Peringkat": icon,
                    "Nama":      nm,
                    "Skor":      f"{p.get('skor',0)}/{p.get('total_soal',0)}",
                    "Persentase":f"{p.get('persentase',0)}%",
                    "Level":     p.get("level", "-"),
                    "Durasi":    dur,
                    "Tanggal":   (p.get("tanggal", "")[:10] if p.get("tanggal") else "")
                })
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("🏆 Juara 1", scoreboard[0].get("nama", "-"))
            with c2:
                st.metric("⭐ Skor Tertinggi", f"{stats['skor_tertinggi']}/{scoreboard[0].get('total_soal',0)}")
            with c3:
                st.metric("📊 Rata-rata Skor", str(stats["rata_rata"]))
            with c4:
                st.metric("🎯 Level Populer", stats["level_populer"])
            if stats["waktu_tercepat"]:
                st.success(
                    f"⚡ Waktu Tercepat (Perfect Score): "
                    f"{stats['waktu_tercepat']['format']} oleh {stats['waktu_tercepat']['nama']}"
                )
        else:
            st.info("Belum ada skor Quiz. Mainkan Quiz dulu!")

        st.markdown("---")
        st.markdown(f"### 📝 Skor Quiz Kakak: **{st.session_state.user_name}**")
        st.markdown(
            f"**Skor:** {st.session_state.score}/{st.session_state.max_questions} "
            f"(Level: {st.session_state.difficulty})"
        )
        if st.session_state.total_game_duration > 0:
            st.markdown(f"**Waktu:** {format_duration(st.session_state.total_game_duration)}")

        if st.session_state.score > 0 and not st.session_state.score_saved:
            if st.button("💾 Simpan Skor Quiz ke Papan Skor", use_container_width=True,
                         type="primary", key="btn_simpan_quiz_papan"):
                if not st.session_state.game_end_time:
                    st.session_state.game_end_time = time.time()
                end_game_timer()
                if add_score(
                    st.session_state.user_name, st.session_state.score,
                    st.session_state.difficulty, st.session_state.max_questions,
                    st.session_state.game_start_time, st.session_state.game_end_time
                ):
                    st.session_state.score_saved = True
                    st.success("✅ Skor Quiz berhasil disimpan!")
                    st.rerun()
                else:
                    st.error("❌ Gagal menyimpan skor.")
        elif st.session_state.score_saved:
            st.success("✅ Skor Quiz sudah disimpan!")

        with st.expander("🛠️ Reset Papan Skor Quiz (Admin)"):
            st.warning("⚠️ Akan menghapus semua data skor Quiz sesi ini!")
            if st.button("🗑️ Reset Skor Quiz", use_container_width=True, key="btn_reset_quiz"):
                st.session_state.scoreboard_data = []
                st.success("✅ Papan skor Quiz direset!")
                st.rerun()

    # =========================================================
    # TAB 2 — PUZZLE
    # =========================================================
    with tab_puzzle:
        st.markdown("### 🧩 Papan Skor Puzzle Peta Jawa Timur")
        st.caption("Peringkat: ⏱️ Waktu tercepat → ❌ Kesalahan paling sedikit → Terbaru")

        st.markdown(
            """
            <div style='background:linear-gradient(135deg,#0f3443,#1a1a2e);
                border:1px solid rgba(255,215,0,0.3);border-radius:12px;
                padding:12px 16px;margin-bottom:14px;'>
              <span style='color:#ffd700;font-weight:bold;'>📐 Sistem Penilaian Puzzle:</span>
              <span style='color:rgba(255,255,255,0.8);font-size:0.9em;'>
                &nbsp; Skor Penalti = Waktu (detik) + Kesalahan × 10 &nbsp;|&nbsp;
                Makin kecil skor penalti = Peringkat makin tinggi
              </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        puzzle_sb      = load_puzzle_scoreboard()
        puzzle_stats = get_puzzle_scoreboard_stats(puzzle_sb)   # stats dari semua entri

        if puzzle_sb:
            rows_p = []
            for i, p in enumerate(puzzle_sb, 1):
                icon = {1: "👑", 2: "🥈", 3: "🥉"}.get(i, f"{i}.")
                nm   = p.get("nama", "Unknown")
                if nm == st.session_state.user_name:
                    nm = f"⭐ {nm} (Kamu)"
                waktu_fmt = p.get("waktu_format", "--:--")
                kesalahan = p.get("kesalahan", 0)
                penalti   = p.get("poin_penalti", "-")
                tgl       = (p.get("tanggal", "")[:16] if p.get("tanggal") else "")
                rows_p.append({
                    "Peringkat":    icon,
                    "Nama":         nm,
                    "⏱️ Waktu":     waktu_fmt,
                    "❌ Kesalahan": kesalahan,
                    "📊 Penalti":   penalti,
                    "🗓️ Tanggal":   tgl,
                })
            st.dataframe(pd.DataFrame(rows_p), hide_index=True, use_container_width=True)

            # Statistik ringkas
            pc1, pc2, pc3, pc4 = st.columns(4)
            with pc1:
                juara = puzzle_sb[0]
                st.metric("👑 Juara 1", juara.get("nama", "-"))
            with pc2:
                wt = puzzle_stats["waktu_tercepat"]
                st.metric(
                    "⚡ Waktu Tercepat",
                    wt.get("waktu_format", "-") if wt else "-"
                )
            with pc3:
                me = puzzle_stats["kesalahan_minimal"]
                st.metric(
                    "🎯 Min. Kesalahan",
                    f"{me.get('kesalahan','-')} oleh {me.get('nama','-')[:8]}" if me else "-"
                )
            with pc4:
                st.metric("📋 Total Entri", puzzle_stats["total_entri"])

            if puzzle_stats["rata_waktu"]:
                rw = int(puzzle_stats["rata_waktu"])
                rm, rs = divmod(rw, 60)
                st.info(
                    f"📊 Rata-rata waktu: **{rm:02d}:{rs:02d}** | "
                    f"Rata-rata kesalahan: **{puzzle_stats['rata_kesalahan']}**"
                )

            # Highlight podium top 3
            st.markdown("#### 🏅 Podium Juara Puzzle")
            podium_cols = st.columns(min(3, len(puzzle_sb)))
            podium_styles = [
                ("👑", "#ffd700", "linear-gradient(135deg,#2d2010,#3d2e0a)"),
                ("🥈", "#c0c0c0", "linear-gradient(135deg,#1a1a1a,#2a2a2a)"),
                ("🥉", "#cd7f32", "linear-gradient(135deg,#1a0e05,#2a1a0a)"),
            ]
            for idx, (col, (medal, color, bg)) in enumerate(zip(podium_cols, podium_styles)):
                p = puzzle_sb[idx]
                nm = p.get("nama", "?")
                if nm == st.session_state.user_name:
                    nm = f"⭐ {nm}"
                wm_p, ws_p = divmod(int(p.get("waktu_detik", 0)), 60)
                with col:
                    st.markdown(
                        f"""
                        <div style='background:{bg};border:2px solid {color};
                            border-radius:14px;padding:16px 12px;text-align:center;'>
                          <div style='font-size:2em;'>{medal}</div>
                          <div style='color:{color};font-weight:900;font-size:1.05em;
                              margin:4px 0;word-break:break-all;'>{nm}</div>
                          <div style='color:rgba(255,255,255,0.9);font-size:1.2em;
                              font-weight:bold;'>⏱️ {wm_p:02d}:{ws_p:02d}</div>
                          <div style='color:rgba(255,255,255,0.7);font-size:0.85em;'>
                            ❌ {p.get("kesalahan",0)} kesalahan
                          </div>
                          <div style='color:{color};font-size:0.8em;margin-top:4px;'>
                            Penalti: {p.get("poin_penalti","-")}
                          </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            st.info("Belum ada skor Puzzle. Mainkan Puzzle dan simpan hasilnya ke Papan Skor!")

        # Skor puzzle user saat ini (jika belum disimpan dari halaman puzzle)
        st.markdown("---")
        if st.session_state.puzzle_result_time_sec and not st.session_state.puzzle_score_saved:
            wt = st.session_state.puzzle_result_time_sec
            err = st.session_state.puzzle_result_errors or 0
            wm2, ws2 = divmod(int(wt), 60)
            st.markdown(
                f"### 📝 Hasil Puzzle Kakak: **{st.session_state.user_name}**\n\n"
                f"**Waktu:** {wm2:02d}:{ws2:02d} | **Kesalahan:** {err} | "
                f"**Penalti:** {int(wt) + err * 10}"
            )
            if st.button("💾 Simpan Skor Puzzle dari Sini", use_container_width=True,
                         type="primary", key="btn_simpan_puzzle_dari_papan"):
                if add_puzzle_score(st.session_state.user_name, wt, err):
                    st.session_state.puzzle_score_saved = True
                    st.success("✅ Skor Puzzle berhasil disimpan!")
                    st.rerun()
                else:
                    st.error("❌ Gagal menyimpan.")
        elif st.session_state.puzzle_score_saved:
            wt  = st.session_state.puzzle_result_time_sec or 0
            err = st.session_state.puzzle_result_errors or 0
            wm2, ws2 = divmod(int(wt), 60)
            st.success(
                f"✅ Skor Puzzle sudah tersimpan! — "
                f"⏱️ {wm2:02d}:{ws2:02d} | ❌ {err} kesalahan"
            )

        with st.expander("🛠️ Reset Papan Skor Puzzle (Admin)"):
            st.warning("⚠️ Akan menghapus semua data skor Puzzle sesi ini!")
            if st.button("🗑️ Reset Skor Puzzle", use_container_width=True,
                         key="btn_reset_puzzle_sb"):
                st.session_state.puzzle_scoreboard_data = []
                st.success("✅ Papan skor Puzzle direset!")
                st.rerun()


# --- HALAMAN STATISTIK WAKTU ---
elif PAGE == "Statistik Waktu":
    st.title("⏱️ Statistik Waktu")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Durasi Sesi", format_duration(get_session_duration()))
    with c2:
        if st.session_state.total_game_duration > 0:
            st.metric("Durasi Quiz", format_duration(st.session_state.total_game_duration))
        elif st.session_state.game_start_time and not st.session_state.game_end_time:
            dur = time.time() - st.session_state.game_start_time
            st.metric("Durasi Quiz", format_duration(dur))
        else:
            st.metric("Durasi Quiz", "-")
    with c3:
        st.metric("Total Soal", st.session_state.total_questions)

    if st.session_state.question_times:
        df_t = pd.DataFrame(st.session_state.question_times)
        df_t["waktu"]  = df_t["duration"].apply(lambda x: f"{x:.1f} dtk")
        df_t["status"] = df_t["correct"].apply(lambda x: "✅ Benar" if x else "❌ Salah")
        st.dataframe(df_t[["question_number", "waktu", "status"]],
                     column_config={"question_number": "Soal", "waktu": "Waktu", "status": "Hasil"},
                     hide_index=True, use_container_width=True)
        st.markdown("### 📈 Grafik Waktu Menjawab")
        st.line_chart(pd.DataFrame({"Soal": df_t["question_number"],
                                    "Waktu (dtk)": df_t["duration"]}).set_index("Soal"))
    else:
        st.info("Belum ada data. Mulai quiz untuk melihat statistik waktu.")

# --- HALAMAN PENGATURAN ---
elif PAGE == "Pengaturan":
    st.title("⚙️ Pengaturan Aplikasi")
    t1, t2, t3 = st.tabs(["🎮 Quiz", "🎨 Tampilan & Musik", "⏱️ Waktu"])
    with t1:
        c1, c2 = st.columns(2)
        with c1:
            new_max = st.number_input("Maksimum Soal", min_value=5, max_value=30,
                                      value=st.session_state.max_questions, key="s_max")
        with c2:
            new_diff = st.selectbox("Kesulitan", ["Mudah", "Normal", "Sulit"],
                                    index=["Mudah", "Normal", "Sulit"].index(st.session_state.difficulty),
                                    key="s_diff")
        if st.button("💾 Simpan Pengaturan Quiz", use_container_width=True):
            st.session_state.max_questions = new_max
            st.session_state.difficulty = new_diff
            st.success("✅ Pengaturan quiz disimpan!")

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
            "untuk pause/play musik kapan saja.</p></div>",
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
        st.checkbox("Tampilkan timer di quiz", value=True, key="s_timer")
        st.info("Pengaturan waktu aktif secara default.")

# --- HALAMAN TENTANG ---
elif PAGE == "Tentang":
    st.title("ℹ️ Tentang Aplikasi")

    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("""
        ### Sepiro Jawa Timur, Sampeyan

        Aplikasi interaktif untuk mempelajari bentuk kota dan kabupaten di Jawa Timur.

        **Fitur:**
        - 🧩 Quiz Tebak bentuk kota & wilayah dari peta
        - 📚 Info Wilayah dengan informasi lengkap + Logo Kabupaten/Kota
        - 🧩 **Puzzle Drag & Drop** — Kepingan berbentuk POLYGON ASLI wilayah administrasi
        - 🌋 Visualisasi 3D Gunung Bromo
        - 🏛️ Visualisasi 3D Balaikota Malang (Cesium)
        - 🏆 Papan skor sesi
        - ⏱️ Statistik waktu bermain
        - 🎵 Musik latar otomatis
        - 🎈 Efek balon kejutan untuk nilai sempurna!

        **Teknologi:**
        - Streamlit, Folium, streamlit-folium
        - GeoJSON data wilayah administrasi
        - HTML5 Canvas Puzzle Engine (bentuk polygon asli)
        - Sketchfab embed 3D (Bromo)
        - CesiumJS 3D Geospatial (Balaikota)
        - YouTube IFrame API (backsound)
        """)
    with c2:
        st.image("https://img.freepik.com/vektor-premium/peta-yang-digambar-tangan-dari-provinsi-jawa-timur-indonesia-desain-kartun-garis-sederhana-modern_242622-498.jpg")
        st.markdown("**Versi:** 2.9.0")
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
        "<div style='text-align:center;margin-bottom:16px;'>"
        "<span style='background:linear-gradient(135deg,#FF9800,#f57c00);color:white;"
        "padding:4px 20px;border-radius:20px;font-weight:bold;font-size:13px;'>🔬 RESEARCH ASSISTANTS</span>"
        "</div>",
        unsafe_allow_html=True
    )

    ra1, ra2, ra3 = st.columns(3)
    
    with ra1:
        st.markdown(
            """
            <div style='background:linear-gradient(135deg,#FF9800,#f57c00);
                        border-radius:16px;padding:22px;text-align:center;
                        box-shadow:0 6px 20px rgba(255,152,0,0.3);
                        height:100%;'>
              <img src='https://adipandang.wordpress.com/wp-content/uploads/2026/03/nabila-zahra.jpeg'
                   style='width:110px;height:110px;border-radius:50%;
                          object-fit:cover;object-position:top;
                          border:4px solid rgba(255,255,255,0.6);
                          box-shadow:0 4px 12px rgba(0,0,0,0.25);
                          margin-bottom:12px;'>
              <h4 style='color:white;margin:0 0 4px 0;font-size:15px;line-height:1.3;'>
                Nabila Zahra
              </h4>
              <p style='color:rgba(255,255,255,0.8);margin:0 0 12px 0;
                        font-size:12px;font-style:italic;'>Research Assistant</p>
              <span style='background:rgba(255,255,255,0.2);color:white;
                           padding:4px 12px;border-radius:12px;font-size:11px;
                           border:1px solid rgba(255,255,255,0.3);'>
                🔬 Data & Research
              </span>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with ra2:
        st.markdown(
            """
            <div style='background:linear-gradient(135deg,#FF9800,#f57c00);
                        border-radius:16px;padding:22px;text-align:center;
                        box-shadow:0 6px 20px rgba(255,152,0,0.3);
                        height:100%;'>
              <img src='https://media.licdn.com/dms/image/v2/D4E03AQGqTT63jvv2Fg/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1723509953345?e=2147483647&v=beta&t=oSubn-UP7bawIpCNv7qCQ3w3ykUdTu-3hkzUE4YQO5w'
                   style='width:110px;height:110px;border-radius:50%;
                          object-fit:cover;object-position:top;
                          border:4px solid rgba(255,255,255,0.6);
                          box-shadow:0 4px 12px rgba(0,0,0,0.25);
                          margin-bottom:12px;'>
              <h4 style='color:white;margin:0 0 4px 0;font-size:15px;line-height:1.3;'>
                Riska Dwi Thalita Putri
              </h4>
              <p style='color:rgba(255,255,255,0.8);margin:0 0 12px 0;
                        font-size:12px;font-style:italic;'>Research Assistant</p>
              <span style='background:rgba(255,255,255,0.2);color:white;
                           padding:4px 12px;border-radius:12px;font-size:11px;
                           border:1px solid rgba(255,255,255,0.3);'>
                📊 Data Analyst
              </span>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with ra3:
        st.markdown(
            """
            <div style='background:linear-gradient(135deg,#FF9800,#f57c00);
                        border-radius:16px;padding:22px;text-align:center;
                        box-shadow:0 6px 20px rgba(255,152,0,0.3);
                        height:100%;'>
              <img src='https://img.freepik.com/vektor-premium/gambar-profil-avatar-pria-diisolasi-pada-gambar-profil-avatar-latar-belakang-untuk-pria_1293239-4842.jpg'
                   style='width:110px;height:110px;border-radius:50%;
                          object-fit:cover;object-position:top;
                          border:4px solid rgba(255,255,255,0.6);
                          box-shadow:0 4px 12px rgba(0,0,0,0.25);
                          margin-bottom:12px;'>
              <h4 style='color:white;margin:0 0 4px 0;font-size:15px;line-height:1.3;'>
                Muhammad Fulan Hidayatullah
              </h4>
              <p style='color:rgba(255,255,255,0.8);margin:0 0 12px 0;
                        font-size:12px;font-style:italic;'>Research Assistant</p>
              <span style='background:rgba(255,255,255,0.2);color:white;
                           padding:4px 12px;border-radius:12px;font-size:11px;
                           border:1px solid rgba(255,255,255,0.3);'>
                💻 Developer
              </span>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    ra4, ra5, _ = st.columns(3)
    
    with ra4:
        st.markdown(
            """
            <div style='background:linear-gradient(135deg,#FF9800,#f57c00);
                        border-radius:16px;padding:22px;text-align:center;
                        box-shadow:0 6px 20px rgba(255,152,0,0.3);
                        height:100%;'>
              <img src='https://img.freepik.com/vektor-premium/ilustrasi-vektor-profil-avatar-wanita-imut_1058532-14546.jpg'
                   style='width:110px;height:110px;border-radius:50%;
                          object-fit:cover;object-position:top;
                          border:4px solid rgba(255,255,255,0.6);
                          box-shadow:0 4px 12px rgba(0,0,0,0.25);
                          margin-bottom:12px;'>
              <h4 style='color:white;margin:0 0 4px 0;font-size:15px;line-height:1.3;'>
                Daniella Nathalie Makalew
              </h4>
              <p style='color:rgba(255,255,255,0.8);margin:0 0 12px 0;
                        font-size:12px;font-style:italic;'>Research Assistant</p>
              <span style='background:rgba(255,255,255,0.2);color:white;
                           padding:4px 12px;border-radius:12px;font-size:11px;
                           border:1px solid rgba(255,255,255,0.3);'>
                🎨 UI/UX Design
              </span>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with ra5:
        st.markdown(
            """
            <div style='background:linear-gradient(135deg,#FF9800,#f57c00);
                        border-radius:16px;padding:22px;text-align:center;
                        box-shadow:0 6px 20px rgba(255,152,0,0.3);
                        height:100%;'>
              <img src='https://png.pngtree.com/png-clipart/20240416/original/pngtree-hijab-girl-cartoon-avatar-png-image_14848857.png'
                   style='width:110px;height:110px;border-radius:50%;
                          object-fit:cover;object-position:top;
                          border:4px solid rgba(255,255,255,0.6);
                          box-shadow:0 4px 12px rgba(0,0,0,0.25);
                          margin-bottom:12px;'>
              <h4 style='color:white;margin:0 0 4px 0;font-size:15px;line-height:1.3;'>
                Naraya Helga Amelia
              </h4>
              <p style='color:rgba(255,255,255,0.8);margin:0 0 12px 0;
                        font-size:12px;font-style:italic;'>Research Assistant</p>
              <span style='background:rgba(255,255,255,0.2);color:white;
                           padding:4px 12px;border-radius:12px;font-size:11px;
                           border:1px solid rgba(255,255,255,0.3);'>
                📝 Content Writer
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


# ==================== PETA QUIZ ====================

if PAGE == "Quiz":
    # Quiz map
    m = folium.Map(location=[-7.5, 112.3], zoom_start=8,
                   tiles=None, control_scale=True, prefer_canvas=True)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri", name="Satellite", overlay=False, control=False
    ).add_to(m)

    def style_function(feature):
        name = feature["properties"]["name"]
        if st.session_state.game_started and not st.session_state.game_over and name == st.session_state.current_region:
            return {"fillColor": "#ff0000", "color": "#ff0000",
                    "weight": 3, "fillOpacity": 0.7}
        return {
            "fillColor": "#3388ff" if st.session_state.game_started else "#cccccc",
            "color": "#ffffff", "weight": 1.5,
            "fillOpacity": 0.3 if st.session_state.game_started else 0.1
        }

    folium.GeoJson(
        jatim_geojson,
        name="Wilayah Jatim",
        style_function=style_function,
    ).add_to(m)

    st_folium(m, width=None, height=500, use_container_width=True, key="game_map")

    if not st.session_state.game_started and not st.session_state.game_over:
        if st.button("🎮 Mulai Quiz", use_container_width=True, type="primary"):
            reset_game()
            st.rerun()

    # ==================== AREA QUIZ ====================
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

            st.markdown("## 🎮 Quiz Selesai!")
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
        half    = len(options) // 2 + len(options) % 2
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
                st.session_state.game_over      = True
                st.session_state.game_end_time  = time.time()
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

    # Progress bar quiz
    if st.session_state.game_started and not st.session_state.game_over:
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
    "Quiz":             f"🗺️ Quiz {len(wilayah_list)} Wilayah Jawa Timur | Kesulitan: {st.session_state.difficulty}",
    "Info Wilayah":          f"📚 Info Wilayah: {len(wilayah_list)} wilayah tersedia + Logo",
    "Puzzle":           f"🧩 Puzzle Peta Jawa Timur — {len(jatim_geojson.get('features', []))} Kepingan Kab/Kota | Level Normal",
    "Bromo 3D":         "🌋 Gunung Bromo 3D - Jelajahi keindahan gunung berapi aktif",
    "Balaikota 3D":     "🏛️ Balaikota Malang 3D - Visualisasi bangunan bersejarah Kota Malang",
    "Papan Skor":       "🏆 Papan Skor Tebak Jawa Timur",
    "Statistik Waktu":  "⏱️ Statistik Waktu Bermain",
    "Pengaturan":       "⚙️ Sesuaikan pengalaman bermain Anda",
    "Tentang":          "ℹ️ Sepiro Jawa Timur, Sampeyan - Aplikasi Interaktif Pembelajaran Geospasial Jawa Timur"
}
footer_text = footer_texts.get(menu_key, "🧩 Sepiro Jawa Timur, Sampeyan")
st.markdown(create_footer(footer_text, FOOTER_BACKGROUND_URL, st.session_state.footer_brightness),
            unsafe_allow_html=True)
