import streamlit as st
import sys
import io
import time
from datetime import datetime

st.set_page_config(
    page_title="NeuroCode Studio - Platform Coding STEM & Socratic AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Plotly Import with Graceful Fallback
try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

# ---------------------------------------------------------
# GLOBAL MULTI-USER DATABASE IN SESSION STATE
# ---------------------------------------------------------
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "rizky": {
            "name": "Rizky Pratama",
            "school": "SMPN 1 Surabaya (Kelas VIII-A)",
            "avatar": "👨‍💻",
            "password": "123",
            "exp": 450,
            "streak": 7,
            "level": "Master Algoritma",
            "solved_missions": {"🌾 Irigasi Sawah Cerdas IoT", "🌋 Seismograf & EWS Tsunami"},
            "journals": [
                {
                    "date": "15-10-2026 14:30",
                    "concept": "Percabangan Logika If-Elif-Else untuk Membaca Kelembapan Tanah",
                    "impact": "Bisa diterapkan di sawah kakek untuk otomatisasi pompa air saat kemarau."
                }
            ],
            "chat_history": [
                {"role": "bot", "text": "Halo Rizky! Saya NeuroBot, asisten koding kamu. Ada kendala dalam logika program atau ingin berdiskusi tentang algoritma STEM?"}
            ]
        },
        "siti": {
            "name": "Siti Rahmawati",
            "school": "SMPN 2 Malang (Kelas VII-B)",
            "avatar": "👩‍💻",
            "password": "123",
            "exp": 300,
            "streak": 5,
            "level": "Coder Inovatif",
            "solved_missions": {"🚦 Lampu Lalu Lintas Adaptif"},
            "journals": [],
            "chat_history": [
                {"role": "bot", "text": "Halo Siti! Selamat datang kembali di NeuroCode Studio!"}
            ]
        },
        "budi": {
            "name": "Budi Santoso",
            "school": "SMPN 3 Kediri (Kelas IX-C)",
            "avatar": "🧑‍💻",
            "password": "123",
            "exp": 600,
            "streak": 12,
            "level": "CT Strategist",
            "solved_missions": {"🌾 Irigasi Sawah Cerdas IoT", "🌋 Seismograf & EWS Tsunami", "🥗 Kalkulator BMI & Nutrisi"},
            "journals": [],
            "chat_history": [
                {"role": "bot", "text": "Halo Budi! Siap menyelesaikan tantangan koding berikutnya?"}
            ]
        },
        "guru": {
            "name": "Ibu Fatma Syifa, S.Pd.",
            "school": "Guru Pendamping / Admin Informatika",
            "avatar": "👩‍🏫",
            "password": "admin",
            "exp": 1000,
            "streak": 30,
            "level": "Guru PRIMA Inovator",
            "solved_missions": {"🌾 Irigasi Sawah Cerdas IoT", "🌋 Seismograf & EWS Tsunami", "🚦 Lampu Lalu Lintas Adaptif", "🥗 Kalkulator BMI & Nutrisi", "♻️ Pemilah Sampah Otomatis"},
            "journals": [],
            "chat_history": [
                {"role": "bot", "text": "Selamat datang Ibu Fatma Syifa, S.Pd.! Dashboard Guru siap digunakan."}
            ]
        }
    }

if 'active_user' not in st.session_state:
    st.session_state.active_user = "rizky"

user_data = st.session_state.users_db[st.session_state.active_user]

# ---------------------------------------------------------
# STYLING: BRIGHT, FULL COLOR, EYE-CATCHING UI
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Fira+Code:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 30%, #f3e8ff 70%, #fce7f3 100%);
        color: #0f172a;
    }
    
    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #ec4899 100%);
        color: white;
        border-radius: 24px;
        padding: 1.75rem 2rem;
        box-shadow: 0 15px 35px rgba(124, 58, 237, 0.25);
        margin-bottom: 1.5rem;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.15);
    }
    
    .hero-subtitle {
        font-size: 1.05rem;
        opacity: 0.95;
        margin-top: 0.4rem;
        margin-bottom: 1rem;
    }
    
    /* Stat Pills */
    .stat-pill {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(12px);
        padding: 0.5rem 1.1rem;
        border-radius: 50px;
        font-weight: 800;
        font-size: 0.9rem;
        border: 1px solid rgba(255, 255, 255, 0.4);
        color: white;
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    /* Bright White App Cards */
    .bright-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.08), 0 8px 10px -6px rgba(99, 102, 241, 0.04);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .bright-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 30px -5px rgba(99, 102, 241, 0.12);
    }
    
    .card-gradient-header {
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 16px;
        margin-bottom: 1rem;
    }
    
    /* Colorful Chat Bubbles */
    .chat-bubble-user {
        background: linear-gradient(135deg, #4f46e5, #6366f1);
        color: white;
        border-radius: 18px 18px 2px 18px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0 0.5rem auto;
        max-width: 82%;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.2);
        font-weight: 500;
    }
    
    .chat-bubble-bot {
        background: #ffffff;
        border: 2px solid #818cf8;
        color: #1e293b;
        border-radius: 18px 18px 18px 2px;
        padding: 1rem 1.2rem;
        margin: 0.5rem auto 0.5rem 0;
        max-width: 85%;
        box-shadow: 0 4px 15px rgba(129, 140, 248, 0.12);
    }
    
    .badge-tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 700;
        color: white;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR: MULTI-USER LOGIN & ACCOUNT MANAGEMENT
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 👤 Akun & Pengguna")
    
    # User Profile Card in Sidebar
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #3b82f6, #8b5cf6); padding: 1rem; border-radius: 16px; color: white; margin-bottom: 1rem; text-align: center;">
        <div style="font-size: 2.5rem;">{user_data['avatar']}</div>
        <h3 style="margin: 4px 0 0 0; font-size: 1.15rem;">{user_data['name']}</h3>
        <p style="margin: 0; font-size: 0.8rem; opacity: 0.9;">{user_data['school']}</p>
        <hr style="border-color: rgba(255,255,255,0.2); margin: 8px 0;">
        <div style="display: flex; justify-content: space-around; font-size: 0.85rem; font-weight: bold;">
            <span>💎 {user_data['exp']} XP</span>
            <span>🔥 {user_data['streak']} Hari</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Account Switcher Dropdown
    with st.expander("🔄 Ganti Akun / Log In"):
        selected_user_key = st.selectbox(
            "Pilih Akun Terdaftar:",
            options=list(st.session_state.users_db.keys()),
            format_func=lambda k: f"{st.session_state.users_db[k]['avatar']} {st.session_state.users_db[k]['name']}",
            index=list(st.session_state.users_db.keys()).index(st.session_state.active_user)
        )
        if st.button("Masuk dengan Akun Ini", use_container_width=True, type="primary"):
            st.session_state.active_user = selected_user_key
            st.toast(f"Berhasil masuk sebagai {st.session_state.users_db[selected_user_key]['name']}!", icon="🔑")
            time.sleep(0.3)
            st.rerun()

    # Register New Account Form
    with st.expander("✨ Daftar Akun Siswa Baru"):
        new_username = st.text_input("Username (Tanpa Spasi):", key="new_u")
        new_name = st.text_input("Nama Lengkap Siswa:", key="new_n")
        new_school = st.text_input("Asal Sekolah & Kelas:", key="new_s")
        new_avatar = st.selectbox("Pilih Avatar:", ["👨‍💻", "👩‍💻", "🧑‍💻", "🚀", "🌟"], key="new_a")
        
        if st.button("Daftar Sekarang", use_container_width=True):
            if new_username and new_name and new_school:
                clean_u = new_username.strip().lower()
                if clean_u in st.session_state.users_db:
                    st.error("Username sudah digunakan!")
                else:
                    st.session_state.users_db[clean_u] = {
                        "name": new_name,
                        "school": new_school,
                        "avatar": new_avatar,
                        "password": "123",
                        "exp": 100,
                        "streak": 1,
                        "level": "Siswa Coder Pemula",
                        "solved_missions": set(),
                        "journals": [],
                        "chat_history": [
                            {"role": "bot", "text": f"Selamat datang {new_name}! Saya NeuroBot, asisten koding kamu. Mari mulai eksplorasi STEM!"}
                        ]
                    }
                    st.session_state.active_user = clean_u
                    st.success("Akun baru berhasil dibuat!")
                    st.rerun()
            else:
                st.warning("Mohon lengkapi semua data pendaftaran.")

    st.markdown("---")
    st.markdown("### 🎛️ Pengaturan Kelas")
    st.caption("Platform Pembelajaran Coding STEM & Socratic AI - Terintegrasi Kurikulum Merdeka SMP")

# Re-fetch user data after potential account switch
user_data = st.session_state.users_db[st.session_state.active_user]

# ---------------------------------------------------------
# TOP HERO HEADER BANNER
# ---------------------------------------------------------
st.markdown(f"""
<div class="hero-banner">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
        <div>
            <div style="background: rgba(255,255,255,0.25); padding: 4px 14px; border-radius: 20px; display: inline-block; font-size: 0.85rem; font-weight: 800; margin-bottom: 8px;">
                ⚡ NEUROCODE STUDIO v8 - FULL INTERACTIVE
            </div>
            <h1 class="hero-title">🚀 Platform Simulator Coding STEM & Socratic AI</h1>
            <p class="hero-subtitle">Meningkatkan Computational Thinking & Deep Learning Siswa SMP</p>
        </div>
        <div style="display: flex; gap: 0.6rem; flex-wrap: wrap;">
            <div class="stat-pill">👨‍🎓 {user_data['name']}</div>
            <div class="stat-pill">💎 {user_data['exp']} XP</div>
            <div class="stat-pill">🔥 {user_data['streak']} Hari Streak</div>
            <div class="stat-pill">🎖️ {user_data['level']}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tab_home, tab_lab, tab_bot, tab_progress = st.tabs([
    "🏠 Beranda & Papan Peringkat", 
    "🧪 Lab STEM & Coding", 
    "🤖 NeuroBot AI Sokratik", 
    "📈 Progres & Jurnal Refleksi"
])

# ---------------------------------------------------------
# TAB 1: BERANDA & PAPAN PERINGKAT
# ---------------------------------------------------------
with tab_home:
    col_dash1, col_dash2 = st.columns([1.2, 0.8])
    
    with col_dash1:
        st.markdown(f"""
        <div class="bright-card" style="border-left: 6px solid #4f46e5;">
            <h3 style="margin-top:0; color: #4f46e5;">👋 Selamat Datang, {user_data['name']}!</h3>
            <p style="color: #475569; font-size: 0.95rem; line-height: 1.6;">
                Siap mengasah logika <b>Computational Thinking</b> hari ini? Pilih Misi STEM kontekstual di Lab Coding, operasikan sensor fisik secara real-time, dan konsultasikan logika program kamu bersama <b>NeuroBot AI</b>!
            </p>
            <div style="background: #f1f5f9; padding: 0.8rem 1.2rem; border-radius: 12px; display: flex; justify-content: space-between; align-items: center;">
                <span>🎯 Target Minggu Ini: <b>4 Misi Tuntas</b></span>
                <span class="badge-tag" style="background: #10b981;">{len(user_data['solved_missions'])} / 5 Selesai</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("🎯 Capaian Pembelajaran (CP) Informatika SMP")
        
        cp_class = st.radio("Pilih Tingkat Kelas:", ["Kelas VII", "Kelas VIII", "Kelas IX"], horizontal=True)
        
        CP_DATA = {
            "Kelas VII": [
                ("BK-K7", "Berpikir Komputasional: Algoritma dan Dekomposisi Kasus Sehari-hari"),
                ("AP-K7", "Algoritma & Pemrograman: Pengenalan Variabel dan Kondisional Sederhana")
            ],
            "Kelas VIII": [
                ("BK-K8", "Berpikir Komputasional: Pengenalan Pola & Abstraksi Sensor IoT"),
                ("AP-K8", "Algoritma & Pemrograman: Percabangan Bertingkat (If-Elif-Else) & Perulangan")
            ],
            "Kelas IX": [
                ("BK-K9", "Berpikir Komputasional: Simulasi Sistem Kompleks & Geofisika"),
                ("AP-K9", "Algoritma & Pemrograman: Integrasi Struktur Data & Otomasi Robotik")
            ]
        }
        
        for code, title in CP_DATA[cp_class]:
            st.markdown(f"""
            <div class="bright-card" style="padding: 1rem; border-left: 4px solid #06b6d4;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span class="badge-tag" style="background: #0284c7; font-size: 0.75rem;">{code}</span>
                        <h4 style="margin: 4px 0 0 0; color: #0f172a;">{title}</h4>
                    </div>
                    <span style="color: #059669; font-weight: bold; font-size: 0.85rem;">✅ Terintegrasi</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_dash2:
        st.markdown("""
        <div class="bright-card" style="border-top: 5px solid #f59e0b;">
            <h3 style="margin-top:0; color: #d97706;">🏆 Papan Peringkat Siswa (Leaderboard)</h3>
            <p style="font-size: 0.85rem; color: #64748b;">Peringkat real-time berdasarkan total perolehan XP koding:</p>
        """, unsafe_allow_html=True)
        
        # Sort users by EXP
        sorted_users = sorted(
            st.session_state.users_db.items(),
            key=lambda item: item[1]['exp'],
            reverse=True
        )
        
        for idx, (ukey, uinfo) in enumerate(sorted_users, start=1):
            rank_icon = "🥇" if idx == 1 else ("🥈" if idx == 2 else ("🥉" if idx == 3 else f"#{idx}"))
            bg_color = "#fef3c7" if idx == 1 else ("#f1f5f9" if ukey == st.session_state.active_user else "#ffffff")
            border_color = "#f59e0b" if idx == 1 else "#e2e8f0"
            
            st.markdown(f"""
            <div style="background: {bg_color}; border: 1px solid {border_color}; padding: 0.75rem 1rem; border-radius: 12px; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 0.8rem;">
                    <span style="font-size: 1.2rem; font-weight: bold;">{rank_icon}</span>
                    <div>
                        <b style="color: #0f172a;">{uinfo['avatar']} {uinfo['name']}</b><br>
                        <small style="color: #64748b;">{uinfo['school'].split('(')[0]}</small>
                    </div>
                </div>
                <span class="badge-tag" style="background: #7c3aed;">{uinfo['exp']} XP</span>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2: LAB STEM & CODING SIMULATOR
# ---------------------------------------------------------
MISS_DATA = {
    "🌾 Irigasi Sawah Cerdas IoT": {
        "tag": "STEM Biologi & Pertanian",
        "bg_tag": "#059669",
        "desc": "Simulasi kontrol otomatis pompa air berdasarkan sensor kelembapan tanah.",
        "param": "Kelembapan Tanah (%)",
        "min": 0, "max": 100, "default": 25, "unit": "%",
        "template": lambda v: f"""# Misi 1: Irigasi Sawah Cerdas IoT
sensor_kelembapan = {v}  # Nilai dari sensor tanah

if sensor_kelembapan < 30:
    print("STATUS: TANAH KERING!")
    print("AKSI: POMPA AIR NYALA (ON)")
elif sensor_kelembapan <= 70:
    print("STATUS: KONDISI OPTIMAL")
    print("AKSI: POMPA AIR STANDBY")
else:
    print("STATUS: TANAH SANGAT BASAH!")
    print("AKSI: DRAINASE DIBUKA & POMPA OFF")
""",
        "type": "irrigation"
    },
    "🌋 Seismograf & EWS Tsunami": {
        "tag": "STEM Geofisika & Kebencanaan",
        "bg_tag": "#dc2626",
        "desc": "Deteksi dini getaran gempa bumi (Skala Richter) dan sirine keselamatan BMKG.",
        "param": "Magnitudo Gempa (SR)",
        "min": 1.0, "max": 9.0, "default": 7.2, "unit": " SR",
        "template": lambda v: f"""# Misi 2: EWS Gempa & Tsunami
magnitudo = {v}  # Nilai dari Seismograf

if magnitudo < 5.0:
    print("STATUS: AMAN - Gempa Skala Kecil")
elif magnitudo < 7.0:
    print("STATUS: WASPADA - Gempa Sedang")
else:
    print("🚨 STATUS: BAHAYA TSUNAMI! 🚨")
    for i in range(1, 4):
        print(f"BUNYI SIRINE KOTA KE-{{i}}: BEEP! BEEP! BEEP!")
""",
        "type": "earthquake"
    },
    "🚦 Lampu Lalu Lintas Adaptif": {
        "tag": "STEM Robotika & Sipil",
        "bg_tag": "#d97706",
        "desc": "Penyesuaian durasi lampu hijau secara otomatis berdasarkan jumlah kendaraan.",
        "param": "Jumlah Kendaraan (Mobil)",
        "min": 0, "max": 50, "default": 28, "unit": " Mobil",
        "template": lambda v: f"""# Misi 3: Lampu Lalu Lintas Pintar
jumlah_mobil = {v}

if jumlah_mobil > 20:
    durasi = 45
    status = "SANGAT PADAT"
elif jumlah_mobil >= 10:
    durasi = 25
    status = "NORMAL"
else:
    durasi = 10
    status = "LENGANG"

print(f"Kepadatan Jalan: {{status}} ({{jumlah_mobil}} Mobil)")
print(f"Durasi Hijau Diset: {{durasi}} Detik")
""",
        "type": "traffic"
    },
    "🥗 Kalkulator BMI & Nutrisi": {
        "tag": "STEM Kesehatan & WHO",
        "bg_tag": "#2563eb",
        "desc": "Analisis indeks massa tubuh (BMI) dan saran nutrisi gizi seimbang remaja.",
        "param": "Berat Badan (kg)",
        "min": 30, "max": 90, "default": 50, "unit": " kg",
        "template": lambda v: f"""# Misi 4: Analisis BMI & Gizi Remaja
berat_kg = {v}
tinggi_m = 1.58

bmi = berat_kg / (tinggi_m ** 2)
print(f"Nilai BMI Anda: {{round(bmi, 2)}}")

if bmi < 18.5:
    print("Kategori: Kurang Berat -> Perbanyak Protein!")
elif bmi <= 25.0:
    print("Kategori: SEHAT & IDEAL! -> Pertahankan Pola Makan")
else:
    print("Kategori: Kelebihan Berat -> Kurangi Konsumsi Gula")
""",
        "type": "health"
    },
    "♻️ Pemilah Sampah Otomatis": {
        "tag": "STEM Lingkungan & Kimia",
        "bg_tag": "#7c3aed",
        "desc": "Klasifikasi otomatis jenis sampah organik vs anorganik berbasis list Python.",
        "param": "Jumlah Botol Plastik",
        "min": 1, "max": 20, "default": 8, "unit": " Botol",
        "template": lambda v: f"""# Misi 5: Pemilah Sampah Robotik
botol_count = {v}
daftar_sampah = ["Botol Plastik", "Sisa Apel", "Kaleng Bekas", "Daun Kering"]

print(f"Jumlah Botol Terdeteksi Sensor: {{botol_count}} buah")
for item in daftar_sampah:
    if "Botol" in item or "Kaleng" in item:
        print(f"[RECYCLE] {{item}} -> Boks ANORGANIK")
    else:
        print(f"[COMPOST] {{item}} -> Boks ORGANIK")
""",
        "type": "trash"
    }
}

with tab_lab:
    st.subheader("🧪 Lab Simulasi STEM & Editor Kode")
    
    col_s1, col_s2 = st.columns([1.2, 0.8])
    with col_s1:
        selected_miss_name = st.selectbox("📌 Pilih Modul STEM:", list(MISS_DATA.keys()))
        miss = MISS_DATA[selected_miss_name]
    
    with col_s2:
        slider_input = st.slider(
            f"🎛️ Atur Sensor {miss['param']}:",
            min_value=miss['min'],
            max_value=miss['max'],
            value=miss['default']
        )

    col_code_area, col_visual_area = st.columns([1.1, 0.9])
    
    with col_code_area:
        st.markdown(f"""
        <div class="bright-card" style="border-left: 6px solid {miss['bg_tag']};">
            <span class="badge-tag" style="background: {miss['bg_tag']};">{miss['tag']}</span>
            <h3 style="margin: 8px 0 4px 0; color: #0f172a;">{selected_miss_name}</h3>
            <p style="color: #475569; font-size: 0.9rem; margin: 0;">{miss['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        code_input = st.text_area(
            "💻 Editor Kode Python Siswa (Silakan Edit / Uji Logika Anda):",
            value=miss["template"](slider_input),
            height=260,
            key=f"editor_{selected_miss_name}_{slider_input}"
        )
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            btn_run = st.button("▶️ JALANKAN PROGRAM", use_container_width=True, type="primary")
        with col_btn2:
            btn_soc = st.button("🤖 MINTA BIMBINGAN AI", use_container_width=True)

    # Execution Engine
    out_buf = io.StringIO()
    sys.stdout = out_buf
    err_msg = None
    
    try:
        exec(code_input, {})
        exec_out = out_buf.getvalue()
        
        if btn_run:
            if selected_miss_name not in user_data['solved_missions']:
                user_data['solved_missions'].add(selected_miss_name)
                user_data['exp'] += 100
                st.toast("🎉 Misi Berhasil Tuntas! (+100 XP)", icon="🌟")
            else:
                st.toast("🚀 Kode berhasil dijalankan!", icon="✅")
    except Exception as ex:
        err_msg = str(ex)
    finally:
        sys.stdout = sys.__stdout__

    with col_visual_area:
        st.markdown("<b>🖥️ Output Terminal Execution:</b>", unsafe_allow_html=True)
        st.markdown("""<div style="background: #0f172a; color: #38bdf8; padding: 1rem; border-radius: 14px; border: 2px solid #1e293b; font-family: 'Fira Code', monospace;">""", unsafe_allow_html=True)
        if err_msg:
            st.error(f"⚠️ Error Terdeteksi:\n{err_msg}")
        elif exec_out:
            st.code(exec_out, language="text")
        else:
            st.info("Tekan tombol '▶️ JALANKAN PROGRAM' untuk melihat hasil terminal.")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br><b>📊 Visualisasi Meteran Sensor Real-Time (Plotly Gauge):</b>", unsafe_allow_html=True)
        st.markdown("""<div class="bright-card" style="text-align: center; padding: 1rem;">""", unsafe_allow_html=True)
        
        if HAS_PLOTLY:
            fig = go.Figure()
            if miss["type"] == "irrigation":
                c = "#ef4444" if slider_input < 30 else ("#10b981" if slider_input <= 70 else "#3b82f6")
                fig.add_trace(go.Indicator(mode="gauge+number", value=slider_input, title={'text': "Kelembapan Tanah (%)"}, gauge={'axis': {'range': [0, 100]}, 'bar': {'color': c}}))
            elif miss["type"] == "earthquake":
                c = "#10b981" if slider_input < 5.0 else ("#f59e0b" if slider_input < 7.0 else "#ef4444")
                fig.add_trace(go.Indicator(mode="gauge+number", value=slider_input, title={'text': "Skala Richter (SR)"}, gauge={'axis': {'range': [1.0, 9.0]}, 'bar': {'color': c}}))
            elif miss["type"] == "traffic":
                c = "#10b981" if slider_input < 10 else ("#f59e0b" if slider_input <= 20 else "#ef4444")
                fig.add_trace(go.Indicator(mode="gauge+number", value=slider_input, title={'text': "Jumlah Mobil"}, gauge={'axis': {'range': [0, 50]}, 'bar': {'color': c}}))
            elif miss["type"] == "health":
                bmi_calc = round(slider_input / (1.58**2), 1)
                c = "#f59e0b" if bmi_calc < 18.5 else ("#10b981" if bmi_calc <= 25.0 else "#ef4444")
                fig.add_trace(go.Indicator(mode="gauge+number", value=bmi_calc, title={'text': "Skor BMI Siswa"}, gauge={'axis': {'range': [10, 35]}, 'bar': {'color': c}}))
            elif miss["type"] == "trash":
                fig.add_trace(go.Indicator(mode="gauge+number", value=slider_input, title={'text': "Sensor Botol Plastik"}, gauge={'axis': {'range': [0, 20]}, 'bar': {'color': "#8b5cf6"}}))
                
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': '#0f172a', 'family': 'Plus Jakarta Sans'}, height=210, margin=dict(l=20,r=20,t=30,b=20))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.metric("Nilai Sensor Input", f"{slider_input} {miss['unit']}")
            st.progress(min(int(slider_input / miss['max'] * 100), 100))
            
        st.markdown("</div>", unsafe_allow_html=True)

    # Socratic Mentor Popup / Modal response
    if btn_soc or err_msg:
        st.markdown("---")
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e0e7ff, #f3e8ff); border: 2px solid #6366f1; border-radius: 20px; padding: 1.25rem;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                <span style="font-size: 1.8rem;">🤖</span>
                <b style="color: #4f46e5; font-size: 1.1rem;">NeuroBot AI Socratic Mentor:</b>
            </div>
        """, unsafe_allow_html=True)
        
        if err_msg:
            st.write("🧐 **Mari Analisis Kesalahan Kode Tersebut Bersama-Sama:**")
            st.write(f"Pesan error: `{err_msg}`.")
            st.write("**Pertanyaan Refleksi Debugging:** Apakah kamu lupa menuliskan tanda titik dua (`:`) di akhir baris `if`/`elif`, atau ada spasi indentasi yang belum sejajar?")
        else:
            st.write(f"💡 **Pertanyaan Refleksi Computational Thinking ({selected_miss_name}):**")
            st.write(f"Nilai input sensor saat ini adalah **{slider_input} {miss['unit']}**. *Coba perhatikan baris pengkondisian `if-elif-else` mana yang terpilih? Apa yang terjadi jika nilai sensor dinaikkan ke batas maksimal?*")
            
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 3: NEUROBOT AI SOKRATIK
# ---------------------------------------------------------
with tab_bot:
    st.subheader("🤖 NeuroBot AI - Asisten Koding Sokratik")
    st.caption("NeuroBot membantu kamu menganalisis kesalahan kode dan memahami logika tanpa membocorkan jawaban langsung.")
    
    # Quick Prompt Buttons
    q_col1, q_col2, q_col3 = st.columns(3)
    with q_col1:
        if st.button("💡 Kenapa Kode Saya Error?", use_container_width=True):
            user_data['chat_history'].append({"role": "user", "text": "NeuroBot, kenapa kode saya bisa error saat dijalankan?"})
            user_data['chat_history'].append({"role": "bot", "text": "Mari kita cek 3 penyebab umum error pada Python:\n1. **SyntaxError:** Apakah ada tanda kurung `()` atau titik dua `:` yang hilang?\n2. **IndentationError:** Apakah baris di dalam blok `if` sudah menjorok ke dalam (4 spasi)?\n3. **NameError:** Apakah nama variabel yang kamu panggil sudah persis sama huruf besar-kecilnya?"})
            st.rerun()
    with q_col2:
        if st.button("🔍 Cara Kerja Logika If-Else", use_container_width=True):
            user_data['chat_history'].append({"role": "user", "text": "Bagaimana cara kerja logika If-Else dalam percabangan?"})
            user_data['chat_history'].append({"role": "bot", "text": "Bayangkan logika `If-Else` seperti lampu lalu lintas:\n- `if` mencek kondisi pertama (misal: Apakah Kelembapan < 30%).\n- Jika **Benar**, komputer mengeksekusi perintah di bawahnya dan mengabaikan baris lain!\n- Jika **Salah**, komputer lanjut mengecek `elif` atau masuk ke `else`."})
            st.rerun()
    with q_col3:
        if st.button("🚀 Minta Tantangan HOTS", use_container_width=True):
            user_data['chat_history'].append({"role": "user", "text": "NeuroBot, beri saya tantangan penalaran koding tingkat tinggi (HOTS)!"})
            user_data['chat_history'].append({"role": "bot", "text": "🔥 **Tantangan HOTS:** Bisakah kamu mengubah kode Misi Irigasi Sawah agar memiliki kondisi tambahan: Jika kelembapan antara 40% dan 60%, nyalakan pompa selama 5 detik saja? *Operasi logika apa (`and` / `or`) yang kamu butuhkan?*"})
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Render Chat History
    for msg in user_data['chat_history']:
        if msg["role"] == "user":
            st.markdown(f"""<div class="chat-bubble-user"><b>👨‍🎓 {user_data['name']}:</b><br>{msg['text']}</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="chat-bubble-bot"><b>🤖 NeuroBot AI:</b><br>{msg['text']}</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Interactive Chat Input
    with st.form("chat_form", clear_on_submit=True):
        user_text_input = st.text_input("Ketik pertanyaan atau kendala koding kamu di sini:", placeholder="Misal: NeuroBot, apa fungsi dari variabel float pada magnitudo gempa?")
        submit_chat = st.form_submit_button("Kirim Pertanyaan 🚀", type="primary")
        
        if submit_chat and user_text_input.strip():
            user_data['chat_history'].append({"role": "user", "text": user_text_input})
            
            # Socratic AI Response Generator
            low_text = user_text_input.lower()
            if "error" in low_text or "salah" in low_text or "bug" in low_text:
                bot_ans = "Mari lakukan *debugging* mandiri! Coba salin baris kode tempat pesan error itu terjadi. Apakah struktur spasi atau tanda baca di baris tersebut sudah benar?"
            elif "loop" in low_text or "for" in low_text or "ulang" in low_text:
                bot_ans = "Perulangan (`for loop`) digunakan untuk mengulang perintah yang sama secara otomatis! Dalam Misi EWS Gempa, perulangan dipakai untuk membunyikan sirine kota sebanyak 3 kali tanpa perlu mengetik print 3 kali."
            elif "sensor" in low_text or "iot" in low_text or "stem" in low_text:
                bot_ans = "Di dunia nyata, sensor IoT membaca data fisik (seperti suhu atau kelembapan) menjadi angka digital. Angka inilah yang masuk ke variabel program Python kamu untuk diolah!"
            else:
                bot_ans = f"Pertanyaan yang bagus tentang '{user_text_input}'! Menurut analisis kamu, pilar Computational Thinking mana (Dekomposisi, Pengenalan Pola, Abstraksi, Algoritma) yang paling berperan dalam memecahkan masalah tersebut?"
                
            user_data['chat_history'].append({"role": "bot", "text": bot_ans})
            st.rerun()

# ---------------------------------------------------------
# TAB 4: PROGRES & JURNAL REFLEKSI
# ---------------------------------------------------------
with tab_progress:
    st.subheader("📈 Jurnal Refleksi Deep Learning & Portofolio")
    
    col_j1, col_j2 = st.columns([1.1, 0.9])
    
    with col_j1:
        st.markdown("""
        <div class="bright-card" style="border-top: 5px solid #10b981;">
            <h3 style="margin-top:0; color: #059669;">📝 Tambah Catatan Refleksi Baru</h3>
            <p style="font-size: 0.85rem; color: #64748b;">Refleksi 3 Tahap (Mindful, Meaningful, & Joyful Learning):</p>
        """, unsafe_allow_html=True)
        
        with st.form("form_jurnal_v8"):
            concept_input = st.text_input(
                "1. Konsep / Logika Koding Apa yang Kamu Kuasai Hari Ini?",
                placeholder="Misal: Saya memahami logika percabangan if-elif-else dan sensor kelembapan tanah."
            )
            impact_input = st.text_area(
                "2. Bagaimana Teknologi / Algoritma Ini Diterapkan untuk Masyarakat?",
                placeholder="Misal: Sistem ini bisa diterapkan di persimpangan jalan desa saya untuk mengurai kemacetan saat jam sekolah."
            )
            
            btn_save_journal = st.form_submit_button("💾 SIMPAN JURNAL REFLEKSI", type="primary", use_container_width=True)
            
            if btn_save_journal:
                if concept_input and impact_input:
                    now_str = datetime.now().strftime("%d-%m-%Y %H:%M")
                    user_data['journals'].append({
                        "date": now_str,
                        "concept": concept_input,
                        "impact": impact_input
                    })
                    user_data['exp'] += 50
                    st.success("Jurnal refleksi berhasil disimpan ke portofolio kamu! (+50 XP)")
                    st.rerun()
                else:
                    st.warning("Mohon isi kedua pertanyaan refleksi di atas.")
                    
        st.markdown("</div>", unsafe_allow_html=True)

    with col_j2:
        st.markdown("""
        <div class="bright-card" style="border-top: 5px solid #8b5cf6;">
            <h3 style="margin-top:0; color: #7c3aed;">🏅 Koleksi Lencana Belajar</h3>
        """, unsafe_allow_html=True)
        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.markdown("""
            <div style="background: #f8fafc; border: 2px solid #10b981; border-radius: 14px; padding: 0.8rem; text-align: center; margin-bottom: 0.5rem;">
                <span style="font-size: 2rem;">🌾</span><br>
                <b style="color: #0f172a;">Master IoT Sawah</b><br>
                <small style="color: #059669; font-weight: bold;">✅ Terbuka</small>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div style="background: #f8fafc; border: 2px solid #10b981; border-radius: 14px; padding: 0.8rem; text-align: center;">
                <span style="font-size: 2rem;">🤖</span><br>
                <b style="color: #0f172a;">Socratic Thinker</b><br>
                <small style="color: #059669; font-weight: bold;">✅ Terbuka</small>
            </div>
            """, unsafe_allow_html=True)
        with col_b2:
            st.markdown("""
            <div style="background: #f8fafc; border: 2px solid #10b981; border-radius: 14px; padding: 0.8rem; text-align: center; margin-bottom: 0.5rem;">
                <span style="font-size: 2rem;">🔥</span><br>
                <b style="color: #0f172a;">Streak Master</b><br>
                <small style="color: #059669; font-weight: bold;">✅ Terbuka</small>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div style="background: #f8fafc; border: 2px solid #f59e0b; border-radius: 14px; padding: 0.8rem; text-align: center;">
                <span style="font-size: 2rem;">👑</span><br>
                <b style="color: #0f172a;">Guru PRIMA Hero</b><br>
                <small style="color: #d97706; font-weight: bold;">🏆 Level Top</small>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

    # Saved Reflection Journals History
    st.markdown("### 📚 Riwayat Jurnal Refleksi Siswa")
    if user_data['journals']:
        for idx, j in enumerate(reversed(user_data['journals']), start=1):
            st.markdown(f"""
            <div class="bright-card" style="border-left: 5px solid #3b82f6;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <b style="color: #1d4ed8;">📌 Catatan Refleksi #{len(user_data['journals']) - idx + 1}</b>
                    <small style="color: #64748b;">📅 {j['date']}</small>
                </div>
                <p style="margin: 0 0 6px 0; color: #0f172a;"><b>Konsep Koding:</b> {j['concept']}</p>
                <p style="margin: 0; color: #475569;"><b>Dampak Masyarakat:</b> {j['impact']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Belum ada jurnal refleksi yang disimpan. Silakan isi formulir di atas!")

    st.markdown("---")
    
    # Download Certificate / Summary Feature
    cert_text = f"""==================================================
SER T I F I K A T   P O R T O F O L I O   S I S W A
NEUROCODE STUDIO - COMPUTATIONAL THINKING & STEM
==================================================

Nama Siswa    : {user_data['name']}
Asal Sekolah  : {user_data['school']}
Total Skor XP : {user_data['exp']} PTS
Level Coder   : {user_data['level']}
Streak Belajar: {user_data['streak']} Hari

MISI STEM YANG BERHASIL DISLESAIKAN:
{chr(10).join([f"- {m}" for m in user_data['solved_missions']]) if user_data['solved_missions'] else "- Belum ada misi tuntas"}

CATATAN JURNAL REFLEKSI:
Total Jurnal Tersimpan: {len(user_data['journals'])} Catatan

Diisukan oleh: NeuroCode Studio Platform
Anugerah Guru PRIMA Jawa Timur 2026
=================================================="""

    st.download_button(
        label="📄 UNDUH PORTOFOLIO & SERTIFIKAT SISWA (.TXT)",
        data=cert_text,
        file_name=f"Portofolio_NeuroCode_{user_data['name'].replace(' ', '_')}.txt",
        mime="text/plain",
        type="primary"
    )
