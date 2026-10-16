import streamlit as st
import sys
import io

st.set_page_config(
    page_title="NeuroCode Studio - Learning App",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Plotly Import with Graceful Fallback
try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

# Custom Modern Mobile/Web App Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Fira+Code:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background: #0f172a;
        color: #f8fafc;
    }
    
    /* Top App Header */
    .app-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%);
        padding: 1.5rem 2rem;
        border-radius: 20px;
        color: white;
        box-shadow: 0 10px 25px rgba(67, 56, 202, 0.25);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
    }
    
    .user-profile {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .avatar {
        width: 52px;
        height: 52px;
        border-radius: 50%;
        background: linear-gradient(135deg, #a855f7, #ec4899);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(168, 85, 247, 0.4);
    }
    
    .app-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    
    .stat-badge {
        background: rgba(255, 255, 255, 0.1);
        padding: 0.4rem 0.9rem;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 700;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    .chat-bubble-user {
        background: #312e81;
        border-radius: 16px 16px 2px 16px;
        padding: 1rem;
        margin: 0.5rem 0 0.5rem auto;
        max-width: 80%;
        color: #e0e7ff;
    }
    
    .chat-bubble-bot {
        background: #1e293b;
        border: 1px solid #6366f1;
        border-radius: 16px 16px 16px 2px;
        padding: 1rem;
        margin: 0.5rem auto 0.5rem 0;
        max-width: 85%;
        color: #f8fafc;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Session State
if 'user_exp' not in st.session_state:
    st.session_state.user_exp = 520
if 'user_level' not in st.session_state:
    st.session_state.user_level = "Level 3 - Coder Handal"
if 'streak' not in st.session_state:
    st.session_state.streak = 7
if 'solved_missions' not in st.session_state:
    st.session_state.solved_missions = set()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "bot", "text": "Halo! Saya NeuroBot, asisten koding kamu. Ada kendala dalam logika program atau ingin berdiskusi tentang algoritma STEM?"}
    ]

# Top Navigation Bar / User Status
st.markdown(f"""
<div class="app-header">
    <div class="user-profile">
        <div class="avatar">👨‍💻</div>
        <div>
            <h2 style="margin:0; font-size: 1.4rem; font-weight: 800;">NeuroCode Studio</h2>
            <p style="margin:0; font-size: 0.85rem; opacity: 0.85;">Siswa: <b>Rizky Pratama</b> (SMP Kelas VIII)</p>
        </div>
    </div>
    <div style="display: flex; gap: 0.6rem; flex-wrap: wrap; margin-top: 0.5rem;">
        <span class="stat-badge">🔥 Streak: {st.session_state.streak} Hari</span>
        <span class="stat-badge">💎 {st.session_state.user_exp} XP</span>
        <span class="stat-badge">🎖️ {st.session_state.user_level}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Main App Navigation Tabs
tab_home, tab_lab, tab_bot, tab_progress = st.tabs([
    "🏠 Beranda", 
    "🧪 Lab STEM & Coding", 
    "🤖 NeuroBot AI", 
    "📈 Progres & Jurnal"
])

# ---------------------------------------------------------
# TAB 1: BERANDA (DASHBOARD)
# ---------------------------------------------------------
with tab_home:
    st.subheader("👋 Selamat Datang Kembali!")
    
    col_h1, col_h2 = st.columns([1.2, 0.8])
    
    with col_h1:
        st.markdown("""
        <div class="app-card">
            <h3 style="margin-top:0; color: #818cf8;">🚀 Misi Koding Mingguan</h3>
            <p style="color: #cbd5e1; font-size: 0.95rem;">
                Selesaikan simulasi logika pemrograman berbasis kasus dunia nyata (STEM) di bawah ini untuk menaikkan skor XP dan membuka lencana baru!
            </p>
            <hr style="border-color: #334155;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <b>Target Minggu Ini:</b> 4 Misi STEM<br>
                    <small style="color: #94a3b8;">Terintegrasi dengan Pemikiran Komputasional</small>
                </div>
                <span style="background: #22c55e; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">
                    Aktif
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("📚 Alur Pembelajaran Aktif")
        st.markdown("""
        - 1️⃣ **Eksplorasi Parameter:** Geser nilai sensor di Lab STEM.
        - 2️⃣ **Uji Kode Python:** Amati bagaimana logika `if-else` dan perulangan memproses data.
        - 3️⃣ **Diskusi dengan NeuroBot:** Tanyakan alasan di balik error atau optimasi program.
        - 4️⃣ **Isi Jurnal:** Catat pemahaman reflektif kamu di menu Progres.
        """)
        
    with col_h2:
        st.markdown("""
        <div class="app-card">
            <h3 style="margin-top:0; color: #f43f5e;">🏆 Statistik Kamu</h3>
            <div style="font-size: 1.1rem; margin-bottom: 0.5rem;">
                • Misi Tuntas: <b>{} / 4</b>
            </div>
            <div style="font-size: 1.1rem; margin-bottom: 0.5rem;">
                • Total XP: <b>{} PTS</b>
            </div>
            <div style="font-size: 1.1rem; margin-bottom: 0.5rem;">
                • Lencana Utama: <b>Master Algoritma</b>
            </div>
            <hr style="border-color: #334155;">
            <p style="font-size: 0.85rem; color: #94a3b8;">
                Terus tingkatkan pemahaman logika koding setiap hari untuk menjaga streak belajar kamu!
            </p>
        </div>
        """.format(len(st.session_state.solved_missions), st.session_state.user_exp), unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2: LAB STEM & CODING
# ---------------------------------------------------------
MISS_DATA = {
    "🌾 Irigasi Sawah Cerdas IoT": {
        "tag": "STEM Biologi & Lingkungan",
        "desc": "Simulasi kontrol otomatis pompa air berdasarkan sensor kelembapan tanah.",
        "param": "Kelembapan Tanah (%)",
        "min": 0, "max": 100, "default": 25, "unit": "%",
        "template": lambda v: f"""# Program Irigasi Otomatis
sensor_kelembapan = {v}

if sensor_kelembapan < 30:
    print("STATUS: TANAH KERING")
    print("AKSI: POMPA AIR NYALA (ON)")
elif sensor_kelembapan <= 70:
    print("STATUS: KONDISI OPTIMAL")
    print("AKSI: POMPA AIR STANDBY")
else:
    print("STATUS: TANAH SANGAT BASAH")
    print("AKSI: DRAINASE DIBUKA")
""",
        "type": "irrigation"
    },
    "🌋 Seismograf & EWS Tsunami": {
        "tag": "STEM Geofisika & Fisika",
        "desc": "Deteksi dini gempa bumi dan aktivasi sirine keselamatan masyarakat.",
        "param": "Magnitudo Gempa (SR)",
        "min": 1.0, "max": 9.0, "default": 7.2, "unit": " SR",
        "template": lambda v: f"""# Program EWS Gempa & Tsunami
magnitudo = {v}

if magnitudo < 5.0:
    print("STATUS: AMAN - Gempa Kecil")
elif magnitudo < 7.0:
    print("STATUS: WASPADA - Gempa Sedang")
else:
    print("🚨 STATUS: BAHAYA TSUNAMI! 🚨")
    for i in range(1, 4):
        print(f"SIRINE KOTA-{i}: BEEP! BEEP!")
""",
        "type": "earthquake"
    },
    "🚦 Lampu Lalu Lintas Adaptif": {
        "tag": "STEM Robotika & Transportasi",
        "desc": "Penyesuaian durasi lampu hijau secara adaptif berdasarkan kepadatan mobil.",
        "param": "Jumlah Mobil (Kendaraan)",
        "min": 0, "max": 50, "default": 28, "unit": " Mobil",
        "template": lambda v: f"""# Lampu Lalu Lintas Pintar
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
print(f"Durasi Hijau: {{durasi}} Detik")
""",
        "type": "traffic"
    },
    "🥗 Kalkulator BMI & Gizi": {
        "tag": "STEM Kesehatan & Nutrisi",
        "desc": "Analisis indeks massa tubuh dan rekomendasi pola makan remaja.",
        "param": "Berat Badan (kg)",
        "min": 30, "max": 90, "default": 50, "unit": " kg",
        "template": lambda v: f"""# Analisis BMI Remaja
berat = {v}
tinggi_m = 1.58

bmi = berat / (tinggi_m ** 2)
print(f"Nilai BMI Anda: {{round(bmi, 1)}}")

if bmi < 18.5:
    print("Kategori: Kurang Berat -> Protein Tambahan")
elif bmi <= 25.0:
    print("Kategori: SEHAT & IDEAL!")
else:
    print("Kategori: Kelebihan Berat -> Kurangi Gula")
""",
        "type": "health"
    }
}

with tab_lab:
    st.subheader("🧪 Lab Simulasi STEM & Coding")
    
    col_select, col_ctrl = st.columns([1.2, 0.8])
    with col_select:
        selected_miss_name = st.selectbox("Pilih Modul STEM:", list(MISS_DATA.keys()))
        miss = MISS_DATA[selected_miss_name]
    
    with col_ctrl:
        slider_input = st.slider(f"Atur Input {miss['param']}:", min_value=miss['min'], max_value=miss['max'], value=miss['default'])

    col_editor, col_visual = st.columns([1.1, 0.9])
    
    with col_editor:
        st.markdown(f"""
        <div class="app-card">
            <span style="background: #6366f1; color: white; padding: 2px 10px; border-radius: 10px; font-size: 0.8rem; font-weight: bold;">
                {miss['tag']}
            </span>
            <p style="margin-top: 8px; margin-bottom: 0; color: #cbd5e1;">{miss['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        code_input = st.text_area(
            "Editor Kode Python:",
            value=miss["template"](slider_input),
            height=250
        )
        
        btn_run = st.button("▶️ JALANKAN PROGRAM", use_container_width=True, type="primary")

    # Code Execution Engine
    out_buf = io.StringIO()
    sys.stdout = out_buf
    err_msg = None
    try:
        exec(code_input, {})
        exec_out = out_buf.getvalue()
        if btn_run and selected_miss_name not in st.session_state.solved_missions:
            st.session_state.solved_missions.add(selected_miss_name)
            st.session_state.user_exp += 100
            st.toast("🎉 Misi Berhasil Tuntas! (+100 XP)", icon="✨")
    except Exception as ex:
        err_msg = str(ex)
    finally:
        sys.stdout = sys.__stdout__

    with col_visual:
        st.markdown("**🖥️ Output Terminal:**")
        st.markdown("""<div style="background: #020617; padding: 0.8rem; border-radius: 10px; border: 1px solid #1e293b; font-family: monospace;">""", unsafe_allow_html=True)
        if err_msg:
            st.error(f"Error: {err_msg}")
        else:
            st.code(exec_out, language="text")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br><b>📊 Visualisasi Sensor Real-Time:</b>", unsafe_allow_html=True)
        st.markdown("""<div class="app-card" style="text-align: center;">""", unsafe_allow_html=True)
        
        if HAS_PLOTLY:
            fig = go.Figure()
            if miss["type"] == "irrigation":
                c = "#ef4444" if slider_input < 30 else ("#22c55e" if slider_input <= 70 else "#3b82f6")
                fig.add_trace(go.Indicator(mode="gauge+number", value=slider_input, title={'text': "Kelembapan %"}, gauge={'axis': {'range': [0, 100]}, 'bar': {'color': c}}))
            elif miss["type"] == "earthquake":
                c = "#22c55e" if slider_input < 5.0 else ("#eab308" if slider_input < 7.0 else "#ef4444")
                fig.add_trace(go.Indicator(mode="gauge+number", value=slider_input, title={'text': "Skala SR"}, gauge={'axis': {'range': [1.0, 9.0]}, 'bar': {'color': c}}))
            elif miss["type"] == "traffic":
                c = "#22c55e" if slider_input < 10 else ("#eab308" if slider_input <= 20 else "#ef4444")
                fig.add_trace(go.Indicator(mode="gauge+number", value=slider_input, title={'text': "Mobil"}, gauge={'axis': {'range': [0, 50]}, 'bar': {'color': c}}))
            elif miss["type"] == "health":
                bmi_calc = round(slider_input / (1.58**2), 1)
                c = "#eab308" if bmi_calc < 18.5 else ("#22c55e" if bmi_calc <= 25.0 else "#ef4444")
                fig.add_trace(go.Indicator(mode="gauge+number", value=bmi_calc, title={'text': "BMI"}, gauge={'axis': {'range': [10, 35]}, 'bar': {'color': c}}))
                
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': 'white'}, height=200, margin=dict(l=20,r=20,t=30,b=20))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.metric("Nilai Sensor", f"{slider_input} {miss['unit']}")
            st.progress(min(int(slider_input / miss['max'] * 100), 100))
            
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 3: NEUROBOT AI
# ---------------------------------------------------------
with tab_bot:
    st.subheader("🤖 NeuroBot - Asisten Koding Sokratik")
    st.caption("NeuroBot membantu kamu menganalisis kesalahan kode dan memahami logika tanpa membocorkan jawaban langsung.")
    
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""<div class="chat-bubble-user"><b>Kamu:</b><br>{msg['text']}</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="chat-bubble-bot"><b>🤖 NeuroBot:</b><br>{msg['text']}</div>""", unsafe_allow_html=True)
            
    user_q = st.text_input("Ketik pertanyaan atau masalah koding kamu di sini:", key="chat_input")
    if st.button("Kirim Pertanyaan", type="primary"):
        if user_q.strip():
            st.session_state.chat_history.append({"role": "user", "text": user_q})
            
            # Smart Socratic Response
            if "error" in user_q.lower() or "salah" in user_q.lower():
                bot_ans = "Mari kita amati pesan error-nya bersama! Apakah kamu sudah memeriksa tanda titik dua (`:`) di akhir baris `if`/`else` dan spasi indentasi di bawahnya?"
            elif "if" in user_q.lower() or "logika" in user_q.lower():
                bot_ans = "Logika percabangan `if-elif-else` bekerja seperti persimpangan jalan. Urutan kondisi sangat menentukan! Manakah kondisi yang menurutmu dieksekusi lebih dulu saat input bernilai ekstrem?"
            else:
                bot_ans = f"Pertanyaan menarik tentang '{user_q}'! Coba analisis kembali bagaimana variabel dalam program kamu menyimpan dan memperbarui nilainya."
                
            st.session_state.chat_history.append({"role": "bot", "text": bot_ans})
            st.rerun()

# ---------------------------------------------------------
# TAB 4: PROGRES & JURNAL
# ---------------------------------------------------------
with tab_progress:
    st.subheader("📈 Jurnal Refleksi & Catatan Belajar")
    
    with st.form("form_jurnal"):
        st.markdown("<b>1. Apa konsep koding paling berharga yang kamu kuasai hari ini?</b>", unsafe_allow_html=True)
        q1 = st.text_input("", placeholder="Misal: Saya memahami cara kerja pengkondisian percabangan untuk sensor...")
        
        st.markdown("<b>2. Bagaimana ide teknologi ini bisa membantu masyarakat di sekitar tempat tinggalmu?</b>", unsafe_allow_html=True)
        q2 = st.text_area("", placeholder="Misal: Sistem irigasi otomatis bisa dipakai oleh petani di desa saya...")
        
        submitted = st.form_submit_button("💾 Simpan Jurnal Refleksi")
        if submitted:
            st.success("Jurnal refleksi kamu berhasil tersimpan di dalam profil NeuroCode Studio!")
            
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🏅 Koleksi Lencana Belajar")
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        st.markdown("""<div class="app-card" style="text-align: center;">🔥<br><b>Streak 7 Hari</b><br><small style="color:#22c55e;">Terbuka</small></div>""", unsafe_allow_html=True)
    with col_b2:
        st.markdown("""<div class="app-card" style="text-align: center;">🌾<br><b>Master IoT Sawah</b><br><small style="color:#22c55e;">Terbuka</small></div>""", unsafe_allow_html=True)
    with col_b3:
        st.markdown("""<div class="app-card" style="text-align: center;">🤖<br><b>Socratic Thinker</b><br><small style="color:#22c55e;">Terbuka</small></div>""", unsafe_allow_html=True)
