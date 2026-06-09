import streamlit as st
import pandas as pd
from datetime import datetime, date

# ==========================================
# 🎨 INSTAGRAM STORY & PASTEL GRID CUSTOM CSS
# ==========================================
def apply_instagram_story_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300..700&display=swap');
    
    /* Latar belakang utama menyerupai gradasi soft IG Story */
    html, body, [data-testid="stAppViewContainer"], .main {
        background: linear-gradient(180deg, #FAD0C4 0%, #FFD1FF 100%) !important;
        font-family: 'Fredoka', 'Segoe UI', sans-serif;
        color: #4A4A4A;
    }
    
    /* Sembunyikan sidebar dan header bawaan Streamlit agar bersih */
    [data-testid="stSidebar"] {display: none !important;}
    [data-testid="stHeader"] {background: transparent !important;}
    
    /* Wadah utama menyerupai Mockup Layar HP */
    .phone-container {
        max-width: 500px;
        margin: 0 auto;
        background-color: #FFF9FA;
        border-radius: 40px;
        padding: 25px;
        box-shadow: 0px 20px 40px rgba(0,0,0,0.2);
        border: 8px solid #333;
        position: relative;
    }
    
    /* Header Akun IG Story di bagian atas */
    .story-header {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }
    .story-avatar {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        border: 2px solid #FF8E9E;
        background: #FFE3E8;
        display: inline-block;
        margin-right: 12px;
    }
    .story-username {
        font-weight: bold;
        color: #333;
        font-size: 16px;
    }
    .story-time {
        color: #888;
        font-size: 14px;
        margin-left: 8px;
    }
    
    /* Judul Dashboard internal */
    .dashboard-title {
        font-size: 32px;
        font-weight: 700;
        color: #FF8E9E;
        text-shadow: 1px 1px #FFE3E8;
        margin-bottom: 5px;
    }
    
    /* Baris Indikator Angka / Metrics Kecil Atas */
    .mini-metrics-container {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
    }
    .mini-metric-box {
        flex: 1;
        padding: 10px;
        border-radius: 12px;
        text-align: center;
        font-size: 13px;
        font-weight: bold;
    }
    
    /* Gaya Kartu Grid Pastel */
    .pastel-card {
        border-radius: 20px;
        padding: 18px;
        margin-bottom: 18px;
        box-shadow: 0px 5px 10px rgba(0,0,0,0.03);
    }
    
    /* Penyesuaian form bawaan streamlit biar rounded imut */
    div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="calendar"] {
        border-radius: 12px !important;
    }
    
    /* Tombol Pink Pastel di dalam story */
    .stButton>button {
        background-color: #FFB7C5 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 20px !important;
        border: none !important;
        width: 100% !important;
        padding: 8px 0px !important;
        box-shadow: 0px 4px 6px rgba(255, 183, 197, 0.3) !important;
    }
    
    /* Bubble chat komentar tiruan */
    .comment-bubble {
        background: #F3EAF8;
        padding: 10px 14px;
        border-radius: 15px;
        margin-bottom: 8px;
        font-size: 14px;
    }
    
    /* Teks overlay bawah mirip caption IG */
    .bottom-caption {
        background: rgba(0, 0, 0, 0.6);
        color: white;
        padding: 8px 15px;
        border-radius: 10px;
        font-size: 13px;
        text-align: center;
        margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Denara Story App", layout="centered", page_icon="✨")
apply_instagram_story_theme()

# ==========================================
# 📊 LOCAL STATE DATA STORE (DATA ARRAYS)
# ==========================================
TARIF_KAMAR = {
    "🧸 Standard Room": 350000,
    "👑 Deluxe Room": 750000,
    "🏰 Suite Family Room": 1200000
}

MENU_MAKANAN = {
    "🥞 Pancake Strawberry": 25000,
    "🧋 Bubble Milk Tea": 18000,
    "🍱 Bento Box Imut": 45000
}

if "kamar_data" not in st.session_state:
    st.session_state.kamar_data = []
    for no in ["101", "102", "201", "202", "301", "302"]:
        st.session_state.kamar_data.append({"No Kamar": no, "Tipe Kamar": "👑 Deluxe Room", "Status": "🟩 Tersedia"})

if "reservasi_log" not in st.session_state: st.session_state.reservasi_log = []
if "histori_transaksi" not in st.session_state: st.session_state.histori_transaksi = []
if "makanan_log" not in st.session_state: st.session_state.makanan_log = []
if "ulasan_log" not in st.session_state: 
    st.session_state.ulasan_log = [{"nama": "Caca ✨", "rating": 5, "komentar": "Kamarnya wangi stroberi!"}]

# ==========================================
# 📱 WADAH FRAME TELEPHON / MOCKUP SCREEN
# ==========================================
st.markdown("""
<div class="phone-container">
    <div class="story-header">
        <div class="story-avatar"></div>
        <div>
            <span class="story-username">vanescence_</span>
            <span class="story-time">14 jam</span>
        </div>
    </div>
    <div class="dashboard-title">Dashboard</div>
    <div style="color: #8FA0CA; font-size:14px; margin-bottom:15px;">✨ Live Preview Aplikasi Reservasi Denara ✨</div>
</div>
""", unsafe_allow_html=True)

# Membuka ruang container Streamlit di dalam phone container menggunakan kolom tunggal
with st.container():
    
    # 1. BARIS INDIKATOR METRICS (MINI BOXES)
    kamar_kosong = len([k for k in st.session_state.kamar_data if k["Status"] == "🟩 Tersedia"])
    
    st.markdown(f"""
    <div class="mini-metrics-container">
        <div class="mini-metric-box" style="background-color: #E2F0D9; color: #385723;">Kamar Kosong<br><span style="font-size:18px;">{kamar_kosong}</span></div>
        <div class="mini-metric-box" style="background-color: #F2EBF7; color: #622599;">Tamu Inap<br><span style="font-size:18px;">{len(st.session_state.reservasi_log)}</span></div>
        <div class="mini-metric-box" style="background-color: #FFF2CC; color: #7F6000;">Histori<br><span style="font-size:18px;">{len(st.session_state.histori_transaksi)}</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 2. GRID UTAMA: MODUL BOOKING KAMAR BARU (KARTU PINK)
    st.markdown('<div class="pastel-card" style="background-color: #FFEAEF; border: 1px solid #FFC0CB;">', unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#CC4B61;'>🛍️ Booking Kamar Baru</h4>", unsafe_allow_html=True)
    
    in_nama = st.text_input("Nama Lengkap", key="rsv_nama", placeholder="Sesuai KTP")
    in_tipe = st.selectbox("Pilih Jenis Kamar", list(TARIF_KAMAR.keys()), key="rsv_tipe")
    
    col_tgl1, col_tgl2 = st.columns(2)
    with col_tgl1: in_in = st.date_input("Check-In", date.today(), key="rsv_in")
    with col_tgl2: in_out = st.date_input("Check-Out", date.today() + pd.Timedelta(days=1), key="rsv_out")
    
    kamar_ready = next((k for k in st.session_state.kamar_data if k["Status"] == "🟩 Tersedia"), None)
    
    if st.button("Pesan & Kunci Kamar ➡️", key="btn_booking"):
        if in_nama and kamar_ready:
            invoice_id = f"RSV-{datetime.now().strftime('%d%M%S')}"
            st.session_state.reservasi_log.append({
                "id": invoice_id, "nama": in_nama, "kamar": kamar_ready["No Kamar"], "tipe": in_tipe,
                "check_in": str(in_in), "check_out": str(in_out), "total_biaya": TARIF_KAMAR[in_tipe],
                "metode": "Gopay/Dana Pastel", "status_bayar": "PAID", "status": "🟨 Direservasi"
            })
            kamar_ready["Status"] = "🟨 Direservasi"
            st.success(f"Sukses! ID Reservasimu: {invoice_id}")
        else:
            st.error("Isi nama atau pastikan kamar tersedia ya!")
    st.markdown('</div>', unsafe_allow_html=True)


    # 3. GRID UTAMA: MODUL KATALOG KAMAR (KARTU HIJAU MINT)
    st.markdown('<div class="pastel-card" style="background-color: #E6F7F4; border: 1px solid #B4E7DD;">', unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#1ABC9C;'>🏨 Katalog Kamar Denara</h4>", unsafe_allow_html=True)
    for k, h in TARIF_KAMAR.items():
        st.markdown(f"• **{k}** — <span style='color:#16A085; font-weight:bold;'>Rp {h:,}/malam</span>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


    # 4. GRID UTAMA: MODUL CEK RESERVASI PEMBELI (KARTU UNGU LAVENDER)
    st.markdown('<div class="pastel-card" style="background-color: #F4EFFF; border: 1px solid #D1C4E9;">', unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#673AB7;'>🔍 Cek Data Reservasimu</h4>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:12px; margin-bottom:5px;'>Data khusus milik pembeli. Masukkan nomor faktur (Invoice ID):</p>", unsafe_allow_html=True)
    
    cari_id = st.text_input("Masukkan No. Reservasi (Contoh: RSV-...)", key="search_invoice_id").strip()
    
    if cari_id:
        match = next((r for r in st.session_state.reservasi_log if r["id"].lower() == cari_id.lower()), None)
        if match:
            st.markdown(f"""
            <div style="background: white; padding: 12px; border-radius: 12px; border: 1px solid #D1C4E9;">
                <b>👤 Pemesan:</b> {match['nama']}<br>
                <b>🚪 Kamar:</b> {match['kamar']} ({match['tipe']})<br>
                <b>📅 Tanggal:</b> {match['check_in']} s/d {match['check_out']}<br>
                <b>🔔 Status Kamar:</b> <span style="color:#673AB7; font-weight:bold;">{match['status']}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Nomor kode reservasi tidak ditemukan.")
    st.markdown('</div>', unsafe_allow_html=True)


    # 5. GRID UTAMA: ROOM SERVICE (KARTU ORANGE PASTEL)
    st.markdown('<div class="pastel-card" style="background-color: #FFF0E6; border: 1px solid #FFD1B3;">', unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#E67E22;'>🍽️ Room Service Camilan</h4>", unsafe_allow_html=True)
    pilih_makanan = st.selectbox("Pilih Menu Lezat", list(MENU_MAKANAN.keys()))
    if st.button("Kirim Pesanan ke Kamar 🛒", key="btn_food"):
        st.success(f"Pesanan {pilih_makanan} berhasil dikirim ke dapur!")
    st.markdown('</div>', unsafe_allow_html=True)


    # 6. GRID UTAMA: PENILAIAN HOTEL (KARTU BIRU PASTEL)
    st.markdown('<div class="pastel-card" style="background-color: #EBF5FB; border: 1px solid #AED6F1;">', unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#2980B9;'>⭐ Surat Cinta dari Tamu</h4>", unsafe_allow_html=True)
    
    with st.form("form_review_mini"):
        u_nama = st.text_input("Nama Kamu", placeholder="Nama samaran boleh")
        u_teks = st.text_area("Tulis komentar singkat", max_chars=100)
        if st.form_submit_button("Kirim Ulasan 💌"):
            if u_nama and u_teks:
                st.session_state.ulasan_log.append({"nama": u_nama, "rating": 5, "komentar": u_teks})
                st.rerun()
                
    for log in st.session_state.ulasan_log[-2:]:
        st.markdown(f'<div class="comment-bubble"><b>{log["nama"]}</b>: {log["komentar"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Teks Overlay penutup di paling bawah menyerupai caption teks IG Story asli
    st.markdown("""
    <div class="bottom-caption">
        💬 heywiilll: jgn dulu diangkat nes blm mateng
    </div>
    """, unsafe_allow_html=True)
