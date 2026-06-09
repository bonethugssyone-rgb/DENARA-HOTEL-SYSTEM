import streamlit as st
import pandas as pd
from datetime import datetime, date

# ==========================================
# 🎨 CLEAN PASTEL THEME (MODERN & MINIMALIS)
# ==========================================
def apply_clean_pastel_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #F8F9FA; 
        font-family: 'Inter', sans-serif;
        color: #495057;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E9ECEF;
    }
    
    /* Header & Title */
    .header-container {
        text-align: center;
        padding: 20px 0;
        margin-bottom: 30px;
        background-color: #FFFFFF;
        border-radius: 16px;
        border: 1px solid #E9ECEF;
    }
    .main-title {
        color: #212529;
        font-size: 32px;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .subtitle {
        color: #6C757D;
        font-size: 14px;
        margin-top: 5px;
    }
    
    /* Card Layout System */
    .pastel-card {
        background: #FFFFFF;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #E9ECEF;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.02);
        margin-bottom: 20px;
    }
    .card-title {
        font-size: 18px;
        font-weight: 600;
        color: #343A40;
        margin-bottom: 15px;
        border-bottom: 2px solid #F1F3F5;
        padding-bottom: 8px;
    }
    
    /* Custom Button Style (Soft Pink Pastel Accent) */
    .stButton>button {
        background-color: #F8D7DA !important;
        color: #842029 !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        border: 1px solid #F5C2C7 !important;
        padding: 10px 20px !important;
        width: 100%;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #F5C2C7 !important;
        border-color: #F1AEB5 !important;
    }
    
    /* Input Elements rounded corners */
    div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="calendar"] {
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Denara Hotel Management", layout="wide", page_icon="🏢")
apply_clean_pastel_theme()

# ==========================================
# 📊 STRUKTUR DATA ARRAY DINAMIS
# ==========================================
TARIF_KAMAR = {
    "Standard Room": 350000,
    "Deluxe Room": 750000,
    "Suite Family Room": 1200000,
    "Presidential Luxury Suite": 2500000
}

MENU_MAKANAN = {
    "Pancake Strawberry": 25000,
    "Bubble Milk Tea": 18000,
    "Bento Box": 45000
}

# Array Master Kamar
if "kamar_data" not in st.session_state:
    st.session_state.kamar_data = []
    for lt in range(1, 4):
        for no in range(1, 5):
            if no == 1:
                tipe = "Standard Room"
            elif no == 2:
                tipe = "Deluxe Room"
            elif no == 3:
                tipe = "Suite Family Room"
            else:
                tipe = "Presidential Luxury Suite"
                
            st.session_state.kamar_data.append({
                "No Kamar": f"{lt}0{no}", "Tipe": tipe, "Harga": TARIF_KAMAR[tipe], "Status": "Tersedia"
            })

# Array Logs
if "reservasi_log" not in st.session_state: st.session_state.reservasi_log = []
if "histori_transaksi" not in st.session_state: st.session_state.histori_transaksi = []
if "makanan_log" not in st.session_state: st.session_state.makanan_log = []
if "ulasan_log" not in st.session_state: st.session_state.ulasan_log = []

# ==========================================
# 🗺️ SISTEM NAVIGASI (SIDEBAR & DASHBOARD INTEGRATED)
# ==========================================
st.sidebar.markdown("<h3 style='text-align: center; color: #212529;'>Denara System</h3>", unsafe_allow_html=True)

if "current_menu" not in st.session_state:
    st.session_state.current_menu = "Dashboard"

menu_pilihan = st.sidebar.radio("Menu Utama", [
    "Dashboard", "Reservasi Baru", "Manajemen Kamar", "Katalog Kamar", "Denah Kamar",
    "Transaksi", "Riwayat Reservasi", "Statistik Hotel", "Room Service", "Penilaian Hotel", "Bantuan"
])

# Singkronisasi Menu dari Klik Sidebar
if menu_pilihan != st.session_state.current_menu:
    st.session_state.current_menu = menu_pilihan

pilihan = st.session_state.current_menu

# ==========================================
# LOGIKA OPERASIONAL PER MENU
# ==========================================

# --- 1. DASHBOARD ---
if pilihan == "Dashboard":
    st.markdown("""
    <div class="header-container">
        <div class="main-title">Denara Hotel Platform</div>
        <div class="subtitle">Sistem Manajemen dan Pusat Informasi Terintegrasi</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Ringkasan Stat
    c_kosong = len([k for k in st.session_state.kamar_data if k["Status"] == "Tersedia"])
    c_isi = len([k for k in st.session_state.kamar_data if k["Status"] == "Check-In"])
    c_book = len([k for k in st.session_state.kamar_data if k["Status"] == "Direservasi"])
    
    st.write("### Status Operasional Hari Ini")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="pastel-card" style="background-color: #E8F5E9; border-color: #C8E6C9;"><p style="color: #2E7D32; margin:0;">Kamar Tersedia</p><h2 style="color: #1B5E20; margin:0;">{c_kosong}</h2></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="pastel-card" style="background-color: #FFF3E0; border-color: #FFE0B2;"><p style="color: #E65100; margin:0;">Direservasi</p><h2 style="color: #E65100; margin:0;">{c_book}</h2></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="pastel-card" style="background-color: #FFEBEE; border-color: #FFCDD2;"><p style="color: #C62828; margin:0;">Aktif Terisi</p><h2 style="color: #B71C1C; margin:0;">{c_isi}</h2></div>', unsafe_allow_html=True)

    # Grid Akses Cepat (Shortcut)
    st.write("### Akses Cepat Menu")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Reservasi Baru"): st.session_state.current_menu = "Reservasi Baru"; st.rerun()
    with col2:
        if st.button("Manajemen Kamar"): st.session_state.current_menu = "Manajemen Kamar"; st.rerun()
    with col3:
        if st.button("Denah Kamar"): st.session_state.current_menu = "Denah Kamar"; st.rerun()
    with col4:
        if st.button("Cek Riwayat"): st.session_state.current_menu = "Riwayat Reservasi"; st.rerun()

# --- 2. RESERVASI BARU ---
elif pilihan == "Reservasi Baru":
    st.write("## Input Reservasi Kamar")
    col_form, col_info = st.columns([2, 1])
    
    with col_form:
        st.markdown('<div class="pastel-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Formulir Data Diri</div>', unsafe_allow_html=True)
        nama = st.text_input("Nama Lengkap Tamu")
        hp = st.text_input("Nomor Kontak (WhatsApp)")
        tipe_pilih = st.selectbox("Pilih Klasifikasi Kamar", list(TARIF_KAMAR.keys()))
        
        kamar_tersedia = [k for k in st.session_state.kamar_data if k["Tipe"] == tipe_pilih and k["Status"] == "Tersedia"]
        
        if not kamar_tersedia:
            st.error("Kamar tipe ini sedang tidak tersedia.")
        else:
            no_kamar_dipilih = st.selectbox("Pilih Nomor Kamar", [k["No Kamar"] for k in kamar_tersedia])
            tgl_in = st.date_input("Tanggal Check-In", date.today())
            tgl_out = st.date_input("Tanggal Check-Out", date.today() + pd.Timedelta(days=1))
            
            if st.button("Konfirmasi Booking"):
                if nama and hp:
                    inv_id = f"RSV-{datetime.now().strftime('%d%M%S')}"
                    durasi = max(1, (tgl_out - tgl_in).days)
                    total = TARIF_KAMAR[tipe_pilih] * durasi
                    
                    st.session_state.reservasi_log.append({
                        "id": inv_id, "nama": nama, "hp": hp, "kamar": no_kamar_dipilih, "tipe": tipe_pilih,
                        "check_in": str(tgl_in), "check_out": str(tgl_out), "total": total, "status": "Direservasi"
                    })
                    
                    for kmr in st.session_state.kamar_data:
                        if kmr["No Kamar"] == no_kamar_dipilih: kmr["Status"] = "Direservasi"
                        
                    st.success(f"Reservasi Berhasil Disimpan. ID Faktur: {inv_id}")
                else:
                    st.warning("Silakan lengkapi formulir terlebih dahulu.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 3. MANAJEMEN KAMAR ---
elif pilihan == "Manajemen Kamar":
    st.write("## Kontrol Operasional Kamar")
    tab1, tab2 = st.tabs(["Check-In / Out Billing", "Registrasi Kamar Baru"])
    
    with tab1:
        if not st.session_state.reservasi_log:
            st.info("Tidak ada data pemesanan yang aktif.")
        else:
            for rsv in list(st.session_state.reservasi_log):
                col_x, col_y = st.columns([3, 1])
                with col_x:
                    st.write(f"Tamu: **{rsv['nama']}** | Kamar {rsv['kamar']} ({rsv['tipe']}) | Status: `{rsv['status']}`")
                with col_y:
                    if rsv["status"] == "Direservasi":
                        if st.button(f"Check-In {rsv['kamar']}", key=f"ci_{rsv['id']}"):
                            rsv["status"] = "Check-In"
                            for k in st.session_state.kamar_data:
                                if k["No Kamar"] == rsv["kamar"]: k["Status"] = "Check-In"
                            st.rerun()
                    elif rsv["status"] == "Check-In":
                        if st.button(f"Check-Out {rsv['kamar']}", key=f"co_{rsv['id']}"):
                            rsv["status"] = "Selesai"
                            st.session_state.histori_transaksi.append(rsv)
                            for k in st.session_state.kamar_data:
                                if k["No Kamar"] == rsv["kamar"]: k["Status"] = "Tersedia"
                            st.session_state.reservasi_log.remove(rsv)
                            st.success("Proses Check-Out Berhasil.")
                            st.rerun()
                            
    with tab2:
        st.markdown('<div class="pastel-card" style="max-width:500px;">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Tambah Slot Kamar</div>', unsafe_allow_html=True)
        add_no = st.text_input("Input Nomor Kamar")
        add_tipe = st.selectbox("Pilih Kategori", list(TARIF_KAMAR.keys()), key="add_tp")
        if st.button("Tambahkan Master Kamar"):
            if add_no and not any(k["No Kamar"] == add_no for k in st.session_state.kamar_data):
                st.session_state.kamar_data.append({
                    "No Kamar": add_no, "Tipe": add_tipe, "Harga": TARIF_KAMAR[add_tipe], "Status": "Tersedia"
                })
                st.success(f"Kamar {add_no} telah ditambahkan ke dalam sistem database.")
            else:
                st.error("Gagal menambahkan. Nomor kamar sudah terdaftar.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 4. KATALOG KAMAR ---
elif pilihan == "Katalog Kamar":
    st.write("## Kategori dan Spesifikasi Kamar")
    col1, col2, col3, col4 = st.columns(4)
    for idx, (tipe, harga) in enumerate(TARIF_KAMAR.items()):
        with [col1, col2, col3, col4][idx % 4]:
            st.markdown(f"""
            <div class="pastel-card">
                <div class="card-title">{tipe}</div>
                <p style="font-size:20px; font-weight:700; color:#212529;">Rp {harga:,} <span style="font-size:12px; font-weight:400; color:#6C757D;">/ Malam</span></p>
                <p style="font-size:13px; color:#6C757D;">Termasuk fasilitas AC, Wi-Fi berkecepatan tinggi, Smart TV, perlengkapan mandi lengkap, dan sarapan pagi gratis.</p>
            </div>
            """, unsafe_allow_html=True)

# --- 5. DENAH KAMAR ---
elif pilihan == "Denah Kamar":
    st.write("## Pemetaan Status Tata Letak Kamar")
    for lt in ["1", "2", "3"]:
        st.write(f"### Lantai {lt}")
        k_lantai = [k for k in st.session_state.kamar_data if k["No Kamar"].startswith(lt)]
        cols = st.columns(4)
        for idx, kmr in enumerate(k_lantai):
            with cols[idx % 4]:
                if kmr["Status"] == "Tersedia": 
                    st.success(f"Kamar {kmr['No Kamar']} (Tersedia)")
                elif kmr["Status"] == "Direservasi": 
                    st.warning(f"Kamar {kmr['No Kamar']} (Booking)")
                else: 
                    st.error(f"Kamar {kmr['No Kamar']} (Terisi)")

# --- 6. TRANSAKSI ---
elif pilihan == "Transaksi":
    st.write("## Monitor Transaksi Keuangan")
    if st.session_state.reservasi_log:
        df_transaksi = pd.DataFrame(st.session_state.reservasi_log)
        st.dataframe(df_transaksi[["id", "nama", "kamar", "total", "status"]], use_container_width=True)
    else:
        st.info("Belum ada pencatatan transaksi aktif.")

# --- 7. RIWAYAT RESERVASI ---
elif pilihan == "Riwayat Reservasi":
    st.write("## Pelacakan Status Reservasi Mandiri")
    cari_invoice = st.text_input("Masukkan Nomor Invoice Anda").strip()
    
    if cari_invoice:
        hasil_tamu = next((r for r in st.session_state.reservasi_log if r["id"].lower() == cari_invoice.lower()), None)
        if hasil_tamu:
            st.markdown(f"""
            <div class="pastel-card" style="border-left: 4px solid #0D6EFD;">
                <div class="card-title">Informasi Reservasi Aktif</div>
                <p><b>Nama Tamu:</b> {hasil_tamu['nama']}</p>
                <p><b>Alokasi Unit:</b> Kamar {hasil_tamu['kamar']} ({hasil_tamu['tipe']})</p>
                <p><b>Periode Inap:</b> {hasil_tamu['check_in']} s/d {hasil_tamu['check_out']}</p>
                <p><b>Total Biaya:</b> Rp {hasil_tamu['total']:,}</p>
                <p><b>Status Kamar:</b> {hasil_tamu['status']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Nomor invoice tidak ditemukan dalam sistem.")

# --- 8. STATISTIK HOTEL ---
elif pilihan == "Statistik Hotel":
    st.write("## Statistik dan Analitik Pendapatan")
    total_pendapatan = sum([r["total"] for r in st.session_state.histori_transaksi]) + sum([r["total"] for r in st.session_state.reservasi_log])
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("Total Akumulasi Pendapatan", f"Rp {total_pendapatan:,}")
    with col_s2:
        df_kamars = pd.DataFrame(st.session_state.kamar_data)
        if not df_kamars.empty:
            st.write("Distribusi Kategori Kamar")
            st.bar_chart(df_kamars["Tipe"].value_counts())

# --- 9. ROOM SERVICE ---
elif pilihan == "Room Service":
    st.write("## Jasa Pelayanan Kamar")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.subheader("Pemesanan Makanan")
        p_kamar = st.text_input("Nomor Kamar", value="101")
        p_menu = st.selectbox("Pilih Menu Makanan", list(MENU_MAKANAN.keys()))
        if st.button("Kirim Pesanan"):
            st.session_state.makanan_log.append({"Kamar": p_kamar, "Menu": p_menu, "Harga": MENU_MAKANAN[p_menu], "Status": "Diproses"})
            st.success("Pesanan dikirim ke dapur.")
    with col_f2:
        st.subheader("Daftar Antrian Layanan")
        if st.session_state.makanan_log:
            st.dataframe(pd.DataFrame(st.session_state.makanan_log), use_container_width=True)
        else:
            st.info("Tidak ada antrian pesanan.")

# --- 10. PENILAIAN HOTEL ---
elif pilihan == "Penilaian Hotel":
    st.write("## Evaluasi Tingkat Kepuasan Pelanggan")
    with st.form("f_review"):
        n = st.text_input("Nama Pelanggan")
        s = st.slider("Skor Penilaian (1-5)", 1, 5, 5)
        k = st.text_area("Deskripsi Ulasan")
        if st.form_submit_button("Kirimkan Feedback"):
            if n and k:
                st.session_state.ulasan_log.append({"nama": n, "skor": s, "komen": k})
                st.rerun()
                
    st.write("### Rekapitulasi Ulasan Tamu")
    for u in st.session_state.ulasan_log[::-1]:
        st.write(f"**{u['nama']}** (Skor: {u['skor']}/5) — *\"{u['komen']}\"*")

# --- 11. BANTUAN ---
elif pilihan == "Bantuan":
    st.write("## Pusat Bantuan Terpusat")
    with st.expander("Metode Penyimpanan Data Aplikasi"):
        st.write("Seluruh data operasional diletakkan di dalam memori cache array lokal Streamlit Session State.")
    st.info("Layanan Bantuan Teknis Pusat Hubungi Saluran Internal: Ext. 0")
