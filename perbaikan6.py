import streamlit as st
import pandas as pd
from datetime import datetime, date

# ==========================================
# 🎨 STYLE CUTE PASTEL & INSTAGRAM UI
# ==========================================
def apply_cute_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300..700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], .main {
        background: linear-gradient(180deg, #FFF0F2 0%, #F3EAF8 100%) !important;
        font-family: 'Fredoka', 'Segoe UI', sans-serif;
        color: #5D5464;
    }
    
    /* Custom Sidebar Pastel */
    [data-testid="stSidebar"] {
        background-color: #FBF4FF !important;
        border-right: 3px dashed #E1D2EC;
    }
    
    .main-title {
        color: #FF8E9E;
        font-size: 38px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
        text-shadow: 2px 2px #FFE3E8;
    }
    
    /* Kartu Menu Grid */
    .menu-card {
        background: white;
        padding: 15px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0px 6px 12px rgba(255, 182, 193, 0.15);
        border: 2px solid #FFE6EA;
        transition: transform 0.2s;
        cursor: pointer;
        margin-bottom: 15px;
    }
    .menu-card:hover {
        transform: scale(1.05);
        border-color: #FFB7C5;
    }
    
    /* Cute Data Card */
    .cute-box {
        background: white;
        padding: 20px;
        border-radius: 20px;
        border: 2px solid #FFEAEF;
        box-shadow: 0px 8px 16px rgba(0,0,0,0.02);
        margin-bottom: 20px;
    }
    
    /* Tombol Lembut */
    .stButton>button {
        background-color: #FFB7C5 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 20px !important;
        border: none !important;
        padding: 8px 20px !important;
        box-shadow: 0px 4px 8px rgba(255, 183, 197, 0.3) !important;
    }
    .stButton>button:hover {
        background-color: #FF8E9E !important;
    }
    
    div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="calendar"] {
        border-radius: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Denara Grand Hotel", layout="wide", page_icon="✨")
apply_cute_theme()

# ==========================================
# 📊 STRUKTUR DATA ARRAY DINAMIS (SESSION STATE)
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

# 1. Array Master Kamar (Dinamis)
if "kamar_data" not in st.session_state:
    st.session_state.kamar_data = []
    # Generate otomatis kamar lantai 1 sampai 3
    for lt in range(1, 4):
        for no in range(1, 5):
            tipe = "🧸 Standard Room" if no <= 2 else ("👑 Deluxe Room" if no == 3 else "🏰 Suite Family Room")
            st.session_state.kamar_data.append({
                "No Kamar": f"{lt}0{no}", "Tipe": tipe, "Harga": TARIF_KAMAR[tipe], "Status": "🟩 Tersedia"
            })

# 2. Array Log Transaksi & Reservasi Aktif
if "reservasi_log" not in st.session_state: st.session_state.reservasi_log = []
if "histori_transaksi" not in st.session_state: st.session_state.histori_transaksi = []
if "makanan_log" not in st.session_state: st.session_state.makanan_log = []
if "ulasan_log" not in st.session_state: st.session_state.ulasan_log = []

# ==========================================
# 🗺️ SISTEM NAVIGASI SUB-MENU
# ==========================================
st.sidebar.markdown("<h2 style='text-align: center; color: #FF8E9E;'>🏨 Denara Hotel</h2>", unsafe_allow_html=True)

# State untuk menyimpan menu aktif secara global
if "current_menu" not in st.session_state:
    st.session_state.current_menu = "🏠 Dashboard"

# Sidebar selector sebagai backup navigasi gampang
menu_sidebar = st.sidebar.selectbox("Lompat Ke Menu:", [
    "🏠 Dashboard", "➕ Reservasi Baru", "🛏️ Manajemen Kamar", "🏨 Katalog Kamar", "🗺️ Denah Kamar",
    "📅 Transaksi", "📋 Riwayat Reservasi", "📊 Statistik Hotel", "🛎️ Room Service", "⭐ Penilaian Hotel", "❓ Bantuan"
])

# Singkronisasi navigasi
if menu_sidebar != st.session_state.current_menu:
    if st.sidebar.button("Konfirmasi Pindah Menu 🔄"):
        st.session_state.current_menu = menu_sidebar
        st.rerun()

pilihan = st.session_state.current_menu

# ==========================================
# LOGIKA OPERASIONAL SUB-MENU
# ==========================================

# --- MENU 1: DASHBOARD ---
if pilihan == "🏠 Dashboard":
    st.markdown('<div class="main-title">🏠 Denara Grand Dashboard</div>', unsafe_allow_html=True)
    
    # Grid Menu Utama berupa Tombol Shortcut Interaktif
    st.write("### 🌸 Akses Pintar Fitur")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("➕ Reservasi Baru", use_container_width=True): 
            st.session_state.current_menu = "➕ Reservasi Baru"; st.rerun()
    with col2:
        if st.button("🛏️ Manajemen Kamar", use_container_width=True): 
            st.session_state.current_menu = "🛏️ Manajemen Kamar"; st.rerun()
    with col3:
        if st.button("🗺️ Denah Kamar", use_container_width=True): 
            st.session_state.current_menu = "🗺️ Denah Kamar"; st.rerun()
    with col4:
        if st.button("🔍 Cek Reservasi Anda", use_container_width=True): 
            st.session_state.current_menu = "📋 Riwayat Reservasi"; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Ringkasan Live Stat Array
    c_kosong = len([k for k in st.session_state.kamar_data if k["Status"] == "🟩 Tersedia"])
    c_isi = len([k for k in st.session_state.kamar_data if k["Status"] == "🟥 Check-In"])
    c_book = len([k for k in st.session_state.kamar_data if k["Status"] == "🟨 Direservasi"])
    
    m1, m2, m3 = st.columns(3)
    m1.metric("🟩 Kamar Ready", f"{c_kosong} Kamar")
    m2.metric("🟨 Terbooking", f"{c_book} Kamar")
    m3.metric("🟥 Aktif Terisi", f"{c_isi} Tamu")

# --- MENU 2: RESERVASI BARU ---
elif pilihan == "➕ Reservasi Baru":
    st.markdown('<div class="main-title">➕ Form Reservasi Baru</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="cute-box">', unsafe_allow_html=True)
        nama = st.text_input("Nama Tamu (Sesuai KTP)")
        hp = st.text_input("No. WhatsApp")
        tipe_pilih = st.selectbox("Tipe Kamar", list(TARIF_KAMAR.keys()))
        
        # Cari alokasi kamar kosong dari array secara dinamis
        kamar_tersedia = [k for k in st.session_state.kamar_data if k["Tipe"] == tipe_pilih and k["Status"] == "🟩 Tersedia"]
        
        if not kamar_tersedia:
            st.error("⚠️ Maaf, Kamar tipe ini sedang penuh!")
            st.stop()
            
        no_kamar_dipilih = st.selectbox("Pilih Nomor Kamar Tersedia", [k["No Kamar"] for k in kamar_tersedia])
        
        tgl_in = st.date_input("Tanggal Check-In", date.today())
        tgl_out = st.date_input("Tanggal Check-Out", date.today() + pd.Timedelta(days=1))
        
        if st.button("Simpan Reservasi & Ambil Kode Invoice ➡️", type="primary"):
            if nama and hp:
                inv_id = f"RSV-{datetime.now().strftime('%m%d%H%M')}"
                durasi = max(1, (tgl_out - tgl_in).days)
                total = TARIF_KAMAR[tipe_pilih] * durasi
                
                # Masukkan ke array log reservasi aktif
                st.session_state.reservasi_log.append({
                    "id": inv_id, "nama": nama, "hp": hp, "kamar": no_kamar_dipilih, "tipe": tipe_pilih,
                    "check_in": str(tgl_in), "check_out": str(tgl_out), "total": total, "status": "🟨 Direservasi"
                })
                
                # Update status di array master kamar
                for kmr in st.session_state.kamar_data:
                    if kmr["No Kamar"] == no_kamar_dipilih:
                        kmr["Status"] = "🟨 Direservasi"
                
                st.success(f"🎉 Kamar Berhasil Dikunci! KODE RESERVASI: {inv_id} (Total: Rp {total:,})")
            else:
                st.warning("Mohon isi Nama dan Nomor WhatsApp terlebih dahulu!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- MENU 3: MANAJEMEN KAMAR (ADMIN KENDALISTATUS) ---
elif pilihan == "🛏️ Manajemen Kamar":
    st.markdown('<div class="main-title">🛏️ Manajemen Kontrol Kamar</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔄 Update Check-In / Out", "➕ Tambah Master Kamar Baru"])
    
    with tab1:
        if not st.session_state.reservasi_log:
            st.info("Tidak ada data reservasi aktif saat ini.")
        else:
            for rsv in list(st.session_state.reservasi_log):
                col_x, col_y = st.columns([3, 1])
                with col_x:
                    st.write(f"👤 **{rsv['nama']}** — Kamar {rsv['kamar']} ({rsv['tipe']}) | Status: **{rsv['status']}**")
                with col_y:
                    if rsv["status"] == "🟨 Direservasi":
                        if st.button(f"Proses Masuk (CI) {rsv['kamar']}", key=f"ci_{rsv['id']}"):
                            rsv["status"] = "🟥 Check-In"
                            for k in st.session_state.kamar_data:
                                if k["No Kamar"] == rsv["kamar"]: k["Status"] = "🟥 Check-In"
                            st.rerun()
                    elif rsv["status"] == "🟥 Check-In":
                        if st.button(f"Proses Keluar (CO) {rsv['kamar']}", key=f"co_{rsv['id']}"):
                            rsv["status"] = "🟩 Selesai"
                            st.session_state.histori_transaksi.append(rsv)
                            for k in st.session_state.kamar_data:
                                if k["No Kamar"] == rsv["kamar"]: k["Status"] = "🟩 Tersedia"
                            st.session_state.reservasi_log.remove(rsv)
                            st.success("Tamu Berhasil Check-Out!")
                            st.rerun()
                            
    with tab2:
        st.write("### Menambah Kamar Baru Ke Array Sistem")
        add_no = st.text_input("Nomor Kamar Baru (Contoh: 401)")
        add_tipe = st.selectbox("Tipe Kamar Baru", list(TARIF_KAMAR.keys()), key="add_tp")
        if st.button("Suntik Kamar Baru 🚀"):
            if add_no and not any(k["No Kamar"] == add_no for k in st.session_state.kamar_data):
                st.session_state.kamar_data.append({
                    "No Kamar": add_no, "Tipe": add_tipe, "Harga": TARIF_KAMAR[add_tipe], "Status": "🟩 Tersedia"
                })
                st.success(f"Kamar {add_no} berhasil didaftarkan secara dinamis!")
            else:
                st.error("Nomor kamar kosong atau sudah ada di database!")

# --- MENU 4: KATALOG KAMAR ---
elif pilihan == "🏨 Katalog Kamar":
    st.markdown('<div class="main-title">🏨 Katalog Kamar & Spesifikasi</div>', unsafe_allow_html=True)
    for t, h in TARIF_KAMAR.items():
        with st.expander(f"✨ {t} — Rp {h:,} / Malam"):
            st.write("Dilengkapi dekorasi pastel estetik, Smart TV, AC, Wifi 100Mbps, Kamar Mandi premium, dan gratis breakfast seru.")

# --- MENU 5: DENAH KAMAR ---
elif pilihan == "🗺️ Denah Kamar":
    st.markdown('<div class="main-title">🗺️ Denah Posisi Kamar</div>', unsafe_allow_html=True)
    for lt in ["1", "2", "3"]:
        st.subheader(f"🏢 Lantai Tingkat {lt}")
        k_lantai = [k for k in st.session_state.kamar_data if k["No Kamar"].startswith(lt)]
        cols = st.columns(4)
        for idx, kmr in enumerate(k_lantai):
            with cols[idx % 4]:
                if kmr["Status"] == "🟩 Tersedia": st.success(f"🚪 No. {kmr['No Kamar']}\n\nReady")
                elif kmr["Status"] == "🟨 Direservasi": st.warning(f"🟨 No. {kmr['No Kamar']}\n\nBooked")
                else: st.error(f"🟥 No. {kmr['No Kamar']}\n\nIn-Stay")

# --- MENU 6: TRANSAKSI (KASIR UTAMA) ---
elif pilihan == "📅 Transaksi":
    st.markdown('<div class="main-title">📅 Data Keuangan Transaksi Aktif</div>', unsafe_allow_html=True)
    if st.session_state.reservasi_log:
        df_transaksi = pd.DataFrame(st.session_state.reservasi_log)
        st.dataframe(df_transaksi[["id", "nama", "kamar", "total", "status"]], use_container_width=True)
    else:
        st.info("Belum ada omset transaksi aktif hari ini.")

# --- MENU 7: RIWAYAT RESERVASI (CEK MANDIRI PEMBELI / TAMU) ---
elif pilihan == "📋 Riwayat Reservasi":
    st.markdown('<div class="main-title">📋 Cek Status Reservasi Anda</div>', unsafe_allow_html=True)
    st.write("<p style='text-align:center;'>Fitur khusus pembeli untuk melacak status booking kamar</p>", unsafe_allow_html=True)
    
    cari_invoice = st.text_input("Ketik Nomor Kode Reservasimu (Contoh: RSV-...)").strip()
    
    if cari_invoice:
        # Cari di data aktif
        hasil_tamu = next((r for r in st.session_state.reservasi_log if r["id"].lower() == cari_invoice.lower()), None)
        
        if hasil_tamu:
            st.markdown(f"""
            <div class="cute-box" style="border-left: 6px solid #FFB7C5;">
                <h4>🧾 Reservasi Ditemukan! (Status: {hasil_tamu['status']})</h4>
                <p><b>Nama Pemesan:</b> {hasil_tamu['nama']}</p>
                <p><b>Nomor Kamar:</b> Kamar {hasil_tamu['kamar']} ({hasil_tamu['tipe']})</p>
                <p><b>Check-In / Out:</b> {hasil_tamu['check_in']} s/d {hasil_tamu['check_out']}</p>
                <p><b>Total Biaya Inap:</b> Rp {hasil_tamu['total']:,}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Cari di histori masa lalu
            hasil_lama = next((h for h in st.session_state.histori_transaksi if h["id"].lower() == cari_invoice.lower()), None)
            if hasil_lama:
                st.info(f"ℹ️ Reservasi Atas Nama {hasil_lama['nama']} tercatat **Sudah Selesai / Check-Out**.")
            else:
                st.error("❌ Kode Reservasi tidak valid atau tidak terdaftar.")

# --- MENU 8: STATISTIK HOTEL ---
elif pilihan == "📊 Statistik Hotel":
    st.markdown('<div class="main-title">📊 Analisis Grafik Pendapatan & Statistik</div>', unsafe_allow_html=True)
    
    total_pendapatan = sum([r["total"] for r in st.session_state.histori_transaksi]) + sum([r["total"] for r in st.session_state.reservasi_log])
    st.metric("Total Akumulasi Pendapatan (Gross Income)", f"Rp {total_pendapatan:,}")
    
    # Chart Sederhana Menggunakan Dataframe
    st.write("### Grafik Volume Kamar Menurut Tipe")
    df_kamars = pd.DataFrame(st.session_state.kamar_data)
    if not df_kamars.empty:
        st.bar_chart(df_kamars["Tipe"].value_counts())

# --- MENU 9: ROOM SERVICE ---
elif pilihan == "🛎️ Room Service":
    st.markdown('<div class="main-title">🛎️ Layanan Kamar / Room Service</div>', unsafe_allow_html=True)
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        st.subheader("🛒 Pesan Kuliner Kamar")
        p_kamar = st.text_input("Nomor Kamarmu", value="101")
        p_menu = st.selectbox("Pilih Menu Makanan", list(MENU_MAKANAN.keys()))
        if st.button("Kirim Pesanan Makanan"):
            st.session_state.makanan_log.append({"kamar": p_kamar, "menu": p_menu, "harga": MENU_MAKANAN[p_menu], "status": "Diproses"})
            st.success("Pesanan dikirim ke koki dapur!")
            
    with col_f2:
        st.subheader("📋 Log Antrian Dapur")
        if st.session_state.makanan_log:
            st.dataframe(pd.DataFrame(st.session_state.makanan_log), use_container_width=True)
        else:
            st.info("Belum ada antrian jajan kuliner saat ini.")

# --- MENU 10: PENILAIAN HOTEL ---
elif pilihan == "⭐ Penilaian Hotel":
    st.markdown('<div class="main-title">⭐ Review & Kepuasan Tamu</div>', unsafe_allow_html=True)
    with st.form("f_review"):
        n = st.text_input("Nama Anda")
        s = st.slider("Rating Bintang", 1, 5, 5)
        k = st.text_area("Tulis Review")
        if st.form_submit_button("Kirim"):
            if n and k:
                st.session_state.ulasan_log.append({"nama": n, "skor": s, "komen": k})
                st.rerun()
                
    st.write("### Ulasan Terbaru:")
    for u in st.session_state.ulasan_log[::-1]:
        st.markdown(f"**{u['nama']}** (⭐ {u['skor']}): *\"{u['komen']}\"*")

# --- MENU 11: BANTUAN ---
elif pilihan == "❓ Bantuan":
    st.markdown('<div class="main-title">❓ Pusat Bantuan & FAQ</div>', unsafe_allow_html=True)
    with st.expander("Apakah data kamar bersifat permanen jika browser direfresh?"):
        st.write("Karena menggunakan Array `st.session_state`, data akan tersimpan selama server Streamlit berjalan. Jika halaman di-hard-reload total, data kembali ke kondisi default.")
    st.info("📞 Hubungi Call Center Layanan Darurat Internal Hotel: **Tekan Ekstensi 0 dari Telepon Kamar**.")
