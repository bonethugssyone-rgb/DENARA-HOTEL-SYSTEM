import streamlit as st
import pandas as pd
from datetime import datetime, date

# ==========================================
# 🎨 STYLE PASTEL & LUCU (TAMPILAN KUSTOM)
# ==========================================
def apply_cute_pastel_theme():
    st.markdown("""
    <style>
    /* Mengubah font global dan latar belakang seluruh aplikasi */
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300..700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #FFF9FA; /* Pink pastel super soft */
        font-family: 'Fredoka', 'Segoe UI', sans-serif;
        color: #5D5464;
    }
    
    /* Mengubah gaya sidebar menjadi ungu lavender pastel */
    [data-testid="stSidebar"] {
        background-color: #F3EAF8 !important;
        border-right: 3px dashed #E1D2EC;
    }
    
    /* Gaya Judul Utama */
    .main-title {
        color: #FF8E9E; /* Pink cerah lucu */
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
        text-shadow: 2px 2px #FFE3E8;
    }
    
    .subtitle {
        color: #8FA0CA; /* Biru pastel soft */
        font-size: 18px;
        text-align: center;
        margin-bottom: 25px;
    }
    
    /* Kartu bergaya Bubble / Pop-up Lucu */
    .cute-card {
        background: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0px 8px 16px rgba(255, 182, 193, 0.2);
        border: 2px solid #FFE6EA;
        margin-bottom: 20px;
    }
    
    /* Kotak Promo Kuning Pastel */
    .promo-box {
        background: #FFF9E6;
        border: 2px dashed #FFD966;
        padding: 15px;
        border-radius: 15px;
        color: #7D6608;
        margin-bottom: 20px;
    }
    
    /* Mengubah warna semua tombol menjadi pink pastel gemas */
    .stButton>button {
        background-color: #FFB7C5 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 10px 25px !important;
        box-shadow: 0px 4px 10px rgba(255, 183, 197, 0.4) !important;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #FF8E9E !important;
        transform: scale(1.05);
    }
    
    /* Kustomisasi input, selectbox, dan date_input agar membulat imut */
    div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="calendar"] {
        border-radius: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Panggil fungsi tema pastel di awal halaman
st.set_page_config(page_title="Denara Cute Hotel", layout="wide", page_icon="✨")
apply_cute_pastel_theme()

# ==========================================
# 📊 LOCAL DATABASE BACKUP (PENGGANTI DATA_STORE)
# ==========================================
TARIF_KAMAR = {
    "🧸 Standard Room": 350000,
    "🎀 Superior Room": 500000,
    "👑 Deluxe Room": 750000,
    "🏰 Suite Family Room": 1200000
}

MENU_MAKANAN = {
    "🥞 Pancake Strawberry Seru": 25000,
    "🧋 Bubble Milk Tea Pastel": 18000,
    "🍱 Bento Box Imut": 45000,
    "🍟 Kentang Goreng Senyum": 20000
}

# Inisialisasi Session State (Sistem Array) jika belum ada
if "kamar_data" not in st.session_state:
    st.session_state.kamar_data = []
    # Membuat 24 kamar otomatis (Lantai 1-4)
    for lt in range(1, 5):
        for no in range(1, 7):
            tipe = list(TARIF_KAMAR.keys())[(no-1) % len(TARIF_KAMAR)]
            st.session_state.kamar_data.append({"No Kamar": f"{lt}0{no}", "Tipe Kamar": tipe, "Status": "🟩 Tersedia"})

if "reservasi_log" not in st.session_state: st.session_state.reservasi_log = []
if "histori_transaksi" not in st.session_state: st.session_state.histori_transaksi = []
if "log_pembatalan" not in st.session_state: st.session_state.log_pembatalan = []
if "makanan_log" not in st.session_state: st.session_state.makanan_log = []
if "ulasan_log" not in st.session_state: st.session_state.ulasan_log = [{"nama": "Caca ✨", "rating": 5, "komentar": "Kamarnya wangi stroberi dan estetik banget fotogenik!"}]

# Fungsi lokal pembantu operasional
def lokal_update_status_kamar(no_kamar, status_baru):
    for k in st.session_state.kamar_data:
        if k["No Kamar"] == no_kamar:
            k["Status"] = status_baru
            break

def lokal_update_status_reservasi(id_invoice, status_baru):
    for r in st.session_state.reservasi_log:
        if r["id"] == id_invoice:
            r["status"] = status_baru
            break

# ==========================================
# 🦄 SIDEBAR NAVIGATION (PASTEL STYLE)
# ==========================================
st.sidebar.markdown("<h2 style='text-align: center; color: #AA8BDB;'>🦄 Denara Hotel</h2>", unsafe_allow_html=True)
menu_utama = st.sidebar.radio("Menu Utama", [
    "🏠 Dashboard", 
    "🏨 Manajemen Kamar", 
    "💳 Transaksi", 
    "🍽️ Room Service", 
    "⭐ Penilaian Hotel", 
    "🛟 Bantuan"
])

pilihan_menu = "🏠 Dashboard"
if menu_utama == "🏠 Dashboard": 
    pilihan_menu = "🏠 Dashboard"
elif menu_utama == "🏨 Manajemen Kamar":
    pilihan_menu = st.sidebar.radio("Sub-Menu Kamar", ["📝 Reservasi Baru", "🏨 Katalog Kamar", "🗺️ Denah Kamar"], key="sub_kamar")
elif menu_utama == "💳 Transaksi":
    pilihan_menu = st.sidebar.radio("Sub-Menu Transaksi", ["💳 Pembayaran", "🔍 Cari & Data Reservasi", "⚙️ Update Status & Histori"], key="sub_transaksi")
elif menu_utama == "🍽️ Room Service":
    pilihan_menu = st.sidebar.radio("Sub-Menu Room Service", ["🍽️ Pesan Makanan", "💳 Bayar Room Service"], key="sub_room")
elif menu_utama == "⭐ Penilaian Hotel": 
    pilihan_menu = "⭐ Ulasan Kepuasan"
elif menu_utama == "🛟 Bantuan":
    pilihan_menu = st.sidebar.radio("Sub-Menu Bantuan", ["❓ Pusat Bantuan", "📞 Kontak Layanan Service"], key="sub_bantuan")


# ==========================================
# 🎪 LOGIKA OPERASIONAL PER MENU
# ==========================================

# --- 1. DASHBOARD ---
if pilihan_menu == "🏠 Dashboard":
    st.markdown('<div class="main-title">🏠 Denara Dreamy Hotel</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">✨ Rasakan Sensasi Menginap di Kamar Pastel yang Penuh Keajaiban ✨</div>', unsafe_allow_html=True)
    
    kamar_kosong = len([k for k in st.session_state.kamar_data if k["Status"] == "🟩 Tersedia"])
    st.metric("Kamar Kosong Imut Tersedia", f"{kamar_kosong} Kamar")
    
    st.markdown("""
    <div class="promo-box">
    <h4>💖 Promo Spesial Minggu Ini Hari Ini 💖</h4>
    <p>Gunakan kode voucher <b>DENARADEAL</b> untuk potongan Rp100.000 atau <b>DISC10%</b> untuk diskon ekstra 10%!</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="cute-card"><h3>👑 Kamar Paling Rebutan</h3>', unsafe_allow_html=True)
        st.write("1. **👑 Deluxe Room** (Pilihan Utama Selebgram)")
        st.progress(0.95)
        st.write("2. **🏰 Suite Family Room** (Kasur Besar & Luas)")
        st.progress(0.75)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="cute-card"><h3>⭐ Surat Cinta dari Tamu</h3>', unsafe_allow_html=True)
        for u in st.session_state.ulasan_log[-2:]:
            st.markdown(f"<div style='background:#FBF4FF; padding:10px; border-radius:10px; margin-bottom:10px;'><b>{u['nama']}</b> (⭐ {u['rating']})<br><small>\"{u['komentar']}\"</small></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 2. RESERVASI BARU (CREATE) ---
elif pilihan_menu == "📝 Reservasi Baru":
    st.markdown('<div class="main-title">📝 Booking Kamar Impianmu</div>', unsafe_allow_html=True)
    col_kiri, col_kanan = st.columns([1.5, 1])

    with col_kiri:
        st.subheader("🧸 Data Diri Pemesan")
        nama = st.text_input("Nama Lengkap (Sesuai KTP)")
        hp = st.text_input("Nomor WhatsApp (Aktif)")
        email = st.text_input("Alamat Email Kamu")
        pilihan_tipe = st.selectbox("Pilih Tipe Kamar Impian", list(TARIF_KAMAR.keys()))
        jml_tamu = st.number_input("Berapa Orang yang Ikut Menginap?", min_value=1, max_value=8, value=2)
        tgl_in = st.date_input("Kapan Mau Check-In?", date.today())
        tgl_out = st.date_input("Kapan Mau Check-Out?", date.today() + pd.Timedelta(days=1))
        pilihan_late = st.selectbox("Ada Request Tambahan Waktu Keluar?", ["Normal Check-Out", "Late Check-Out (+Rp 50.000)"])

    with col_kanan:
        st.subheader("🤖 Saran Robot Imut")
        saran = "🧸 Standard Room" if jml_tamu <= 2 else ("👑 Deluxe Room" if jml_tamu <= 4 else "🏰 Suite Family Room")
        st.info(f"Halo! Kamar yang paling cocok untuk {jml_tamu} orang yaitu: **{saran}**")
        
        kamar_cocok = next((k for k in st.session_state.kamar_data if k["Tipe Kamar"] == pilihan_tipe and k["Status"] == "🟩 Tersedia"), None)
        
        if kamar_cocok:
            st.success(f"Yey! Kamar kosong siap dipesan: **Kamar {kamar_cocok['No Kamar']}**")
        else:
            st.error("Yah, tipe kamar pilihanmu kebetulan lagi penuh terisi nih..")

        st.markdown("---")
        st.subheader("🎁 Paket Seru Ekstra")
        addons = []
        if st.checkbox("Paket Sarapan Pagi Sepuasnya (+Rp 50.000)"): addons.append("Breakfast")
        if st.checkbox("Jemput Aku di Bandara (+Rp 150.000)"): addons.append("Airport Pickup")

        if st.button("Kunci Kamar Imutku Sekarang! ➡️", type="primary"):
            if not nama or not kamar_cocok or tgl_out < tgl_in:
                st.error("Oops! Tolong isi formulir dengan lengkap dan benar ya!")
            else:
                st.session_state.proses_checkout = {
                    "id_invoice": f"RSV-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "nama": nama, "hp": hp, "email": email, "kamar": kamar_cocok,
                    "tipe": pilihan_tipe, "check_in": str(tgl_in), "check_out": str(tgl_out),
                    "add_on": addons, "late_checkout": pilihan_late
                }
                st.success("Pesanan berhasil dikunci! Lanjutkan ke menu '💳 Pembayaran' ya!")

# --- 3. KATALOG KAMAR ---
elif pilihan_menu == "🏨 Katalog Kamar":
    st.markdown('<div class="main-title">🏨 Mengintip Isi Kamar</div>', unsafe_allow_html=True)
    for tipe, harga in TARIF_KAMAR.items():
        with st.expander(f"✨ {tipe} — Rp {harga:,} / Malam"):
            st.write("Fasilitas kamar lengkap bernuansa estetis, kasur empuk empuk, Smart TV, Wi-Fi kencang, AC dingin, perlengkapan mandi wangi bunga, serta akses gratis berenang!")

# --- 4. DENAH KAMAR ---
elif pilihan_menu == "🗺️ Denah Kamar":
    st.markdown('<div class="main-title">🗺️ Peta Denah Kamar Hotel</div>', unsafe_allow_html=True)
    for lt in range(1, 5):
        st.subheader(f"🏢 Lantai {lt}")
        kamar_lantai = [k for k in st.session_state.kamar_data if k["No Kamar"].startswith(str(lt))]
        cols = st.columns(6)
        for idx, detail in enumerate(kamar_lantai):
            with cols[idx % 6]:
                if detail["Status"] == "🟩 Tersedia": 
                    st.success(f"🚪 No. {detail['No Kamar']}")
                elif detail["Status"] == "🟨 Direservasi":
                    st.warning(f"🟨 No. {detail['No Kamar']}")
                else: 
                    st.error(f"🟥 No. {detail['No Kamar']}")

# --- 5. PEMBAYARAN RESERVASI ---
elif pilihan_menu == "💳 Pembayaran":
    st.markdown('<div class="main-title">💳 Kasir Pembayaran Lucu</div>', unsafe_allow_html=True)
    if "proses_checkout" not in st.session_state:
        st.warning("Belum ada antrian pembayaran kamar baru saat ini.")
        st.stop()

    dt = st.session_state.proses_checkout
    malam = max(1, (datetime.strptime(dt["check_out"], "%Y-%m-%d") - datetime.strptime(dt["check_in"], "%Y-%m-%d")).days)
    
    harga_pokok = TARIF_KAMAR.get(dt["tipe"], 0) * malam
    biaya_extra = (50000 if "Late" in dt["late_checkout"] else 0) + (50000 if "Breakfast" in dt["add_on"] else 0) + (150000 if "Airport Pickup" in dt["add_on"] else 0)
    subtotal = harga_pokok + biaya_extra

    st.subheader("🎟️ Masukkan Kode Promo")
    v_opsi = st.radio("Pilih Diskonmu:", ["Tanpa Voucher", "DENARADEAL (Potongan Rp100k)", "DISC10% (Potongan 10%)"])
    diskon = 100000 if v_opsi == "DENARADEAL (Potongan Rp100k)" else (subtotal * 0.1 if v_opsi == "DISC10% (Potongan 10%)" else 0)
    
    total_tagihan = (subtotal + (subtotal * 0.11)) - diskon

    st.code(f"""
    ================================================
                🎀 NOTA STRUK DENARA CUTE HOTEL 🎀
    ================================================
    Kode Transaksi : {dt['id_invoice']}
    Nama Pelanggan : {dt['nama']}
    Nomor Kamar    : Kamar {dt['kamar']['No Kamar']} ({dt['tipe']})
    Masa Staycation: {malam} Malam ({dt['check_in']} s/d {dt['check_out']})
    ------------------------------------------------
    Sewa Kamar     : Rp {harga_pokok:,}
    Layanan Ekstra : Rp {biaya_extra:,}
    PPN Lucu (11%) : Rp {int(subtotal * 0.11):,}
    Potongan Kupon : -Rp {int(diskon):,}
    ------------------------------------------------
    TOTAL BAYAR    : Rp {int(total_tagihan):,}
    ================================================
    """, language="text")

    metode = st.selectbox("Pilih Cara Bayar", ["BCA Transfer Direct", "Mandiri Virtual Account", "Gopay/Dana Pastel"])
    status_bayar = st.selectbox("Status Uang", ["PAID (Lunas 100%)", "DP Jaminan Dulu"])

    if st.button("Selesaikan Transaksi & Bayar Sekarang! ✔️", type="primary"):
        st.session_state.reservasi_log.append({
            "id": dt["id_invoice"], "nama": dt["nama"], "hp": dt["hp"], "email": dt["email"],
            "kamar": dt["kamar"]["No Kamar"], "tipe": dt["tipe"], "check_in": dt["check_in"],
            "check_out": dt["check_out"], "total_biaya": total_tagihan, "status_bayar": status_bayar,
            "metode": metode, "status": "🟨 Direservasi"
        })
        
        lokal_update_status_kamar(dt["kamar"]["No Kamar"], "🟨 Direservasi")

        del st.session_state.proses_checkout
        st.success("Yey! Pembayaran berhasil diterima. Kamarmu sudah resmi terkunci aman!")
        st.rerun()

# --- 6. CARI DATA RESERVASI (VERSI PEMBELI / TAMU) ---
elif pilihan_menu == "🔍 Cari & Data Reservasi":
    # // PERBAIKAN: Halaman cek mandiri khusus pembeli menggunakan gaya CSS pastel imut
    st.markdown('<div class="main-title">🔍 Cek Status Reservasimu</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Masukkan <b>Nomor Reservasi (ID Invoice)</b> kamu yang berawal 'RSV-...' untuk melihat data tiket inapmu.</p>", unsafe_allow_html=True)

    input_invoice = st.text_input("Ketikkan Nomor Reservasimu di sini...").strip()

    if input_invoice:
        reservasi_tamu = next((d for d in st.session_state.reservasi_log if d["id"].lower() == input_invoice.lower()), None)

        if reservasi_tamu:
            st.success("🎯 Data Reservasimu Ditemukan!")
            st.markdown(f"""
            <div class="cute-card" style='border-left: 8px solid #FFB7C5;'>
                <h3 style='color: #FF8E9E; margin-top:0;'>🧾 E-Invoice Staycation: {reservasi_tamu['id']}</h3>
                <hr style='border: 1px dashed #FFE6EA;'>
                <p>👤 <b>Nama Tamu Pemesan:</b> {reservasi_tamu['nama']}</p>
                <p>🚪 <b>Nomor Kamar Kamu:</b> <span style='background-color: #FFF0F2; padding: 4px 10px; border-radius: 10px; font-weight: bold; color:#FF8E9E;'>Kamar {reservasi_tamu['kamar']}</span> ({reservasi_tamu['tipe']})</p>
                <p>📅 <b>Tanggal Menginap:</b> {reservasi_tamu['check_in']} s/d {reservasi_tamu['check_out']}</p>
                <p>💰 <b>Total Biaya Lunas:</b> Rp {int(reservasi_tamu['total_biaya']):,}</p>
                <p>💳 <b>Opsi Bayar:</b> {reservasi_tamu['metode']} ({reservasi_tamu['status_bayar']})</p>
                <p>🔔 <b>Kondisi Kamar Saat Ini:</b> <span style='color:#AA8BDB; font-weight:bold;'>{reservasi_tamu['status']}</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            if reservasi_tamu['status'] == "🟨 Direservasi":
                st.info("💡 **Catatan Imut:** Kamarmu sudah aman dipersiapkan. Tunjukkan halaman ini ke kakak resepsionis hotel pas kamu datang ya!")
            elif reservasi_tamu['status'] == "🟥 Check-In":
                st.warning("🏠 **Catatan Imut:** Kamu sedang berada di dalam kamar. Selamat menikmati liburan staycation seru!")
        else:
            histori_tamu = next((h for h in st.session_state.histori_transaksi if h["id"].lower() == input_invoice.lower()), None)
            if histori_tamu:
                st.info("ℹ️ Kabar Hotel: Nomor reservasi ini tercatat telah selesai menginap (**Sudah Check-Out**). Sampai jumpa di liburan berikutnya!")
            else:
                st.error("❌ Yah, nomor reservasi itu tidak bisa ditemukan. Coba cek lagi spasi atau huruf besarnya ya!")
    else:
        st.info("💡 Menunggu input kode... Silakan ketik ID tiket reservasi di atas.")

# --- 7. UPDATE STATUS & HISTORI (ADMIN MANAJEMEN) ---
elif pilihan_menu == "⚙️ Update Status & Histori":
    st.markdown('<div class="main-title">⚙️ Kendali Operasional Hotel</div>', unsafe_allow_html=True)
    tab_update, tab_riwayat, tab_batal = st.tabs(["🔄 Kamar Check-In/Out", "Arsip Tamu Selesai", "Daftar Batal"])
    
    with tab_update:
        if not st.session_state.reservasi_log:
            st.info("Saat ini seluruh kamar dalam keadaan tenang, tidak ada antrian status.")
        else:
            for rsv in list(st.session_state.reservasi_log):
                col_a, col_b = st.columns([2, 1])
                with col_a:
                    st.write(f"👤 **{rsv['nama']}** (Room {rsv['kamar']}) — Status: `{rsv['status']}`")
                with col_b:
                    if rsv["status"] == "🟨 Direservasi":
                        if st.button(f"Masuk Kamar {rsv['kamar']}", key=f"ci_{rsv['id']}"):
                            lokal_update_status_reservasi(rsv["id"], "🟥 Check-In")
                            lokal_update_status_kamar(rsv["kamar"], "🟥 Check-In")
                            st.success("Tamu berhasil Check-In!")
                            st.rerun()
                    elif rsv["status"] == "🟥 Check-In":
                        if st.button(f"Selesai & Keluar {rsv['kamar']}", key=f"co_{rsv['id']}"):
                            st.session_state.histori_transaksi.append(rsv)
                            lokal_update_status_kamar(rsv["kamar"], "🟩 Tersedia")
                            st.session_state.reservasi_log.remove(rsv)
                            st.success("Tamu berhasil Check-Out. Kamar bersih kembali!")
                            st.rerun()

    with tab_riwayat:
        if not st.session_state.histori_transaksi:
            st.info("Belum ada riwayat arsip transaksi.")
        else:
            st.dataframe(pd.DataFrame(st.session_state.histori_transaksi), use_container_width=True)
            
    with tab_batal:
        if not st.session_state.reservasi_log:
            st.info("Tidak ada transaksi aktif yang bisa dibatalkan.")
        else:
            for rsv in list(st.session_state.reservasi_log):
                st.write(f"🔹 **{rsv['id']}** — {rsv['nama']}")
                if st.button(f"Batalkan Room {rsv['kamar']}", key=f"btl_{rsv['id']}"):
                    lokal_update_status_kamar(rsv["kamar"], "🟩 Tersedia")
                    st.session_state.log_pembatalan.append({
                        "id": rsv["id"], "nama": rsv["nama"], "kamar": rsv["kamar"], "waktu_batal": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.session_state.reservasi_log.remove(rsv)
                    st.success("Pesanan berhasil hangus dibatalkan.")
                    st.rerun()

# --- 8. ROOM SERVICE: PESAN MAKANAN ---
elif pilihan_menu == "🍽️ Pesan Makanan":
    st.markdown('<div class="main-title">🍽️ Jasa Pengantaran Kuliner Kamar</div>', unsafe_allow_html=True)
    no_kmr = st.selectbox("Kamu Menempati Nomor Kamar Berapa?", [k["No Kamar"] for k in st.session_state.kamar_data])
    
    total_order = 0
    items_dipesan = []
    
    for menu, harga in MENU_MAKANAN.items():
        qty = st.number_input(f"{menu} — Rp {harga:,}", min_value=0, step=1, key=f"food_{menu}")
        if qty > 0:
            total_order += (qty * harga)
            items_dipesan.append(f"{menu} (x{qty})")
            
    st.markdown(f"### Total Belanja Camilan: **Rp {total_order:,}**")
    if st.button("Kirim Camilan ke Kamarku 🛒"):
        if total_order > 0:
            st.session_state.makanan_log.append({
                "kamar": no_kmr, "pesanan": items_dipesan, "total": total_order, "status": "Belum Bayar"
            })
            st.success("Pesanan sukses dikirim ke dapur! Mohon ditunggu ya kaka!")
        else:
            st.warning("Pilih dulu menu camilan lezat kesukaanmu ya!")

# --- 9. ROOM SERVICE: BAYAR ROOM SERVICE ---
elif pilihan_menu == "💳 Bayar Room Service":
    st.markdown('<div class="main-title">💳 Tagihan Jajan Kuliner</div>', unsafe_allow_html=True)
    antrian_kuliner = [m for m in st.session_state.makanan_log if m["status"] == "Belum Bayar"]
    
    if not antrian_kuliner:
        st.info("Hore! Tidak ada tunggakan pembayaran jajanan saat ini.")
    else:
        for idx, order in enumerate(antrian_kuliner):
            with st.container():
                st.markdown(f'<div class="cute-card"><h4>🛎️ Pesanan Kamar {order["kamar"]}</h4>', unsafe_allow_html=True)
                st.write(f"**Menu Dipesan:** {', '.join(order['pesanan'])}")
                st.write(f"Total Biaya Makan: **Rp {order['total']:,}**")
                
                if st.button(f"Lunasi Makanan Kamar {order['kamar']}", key=f"pay_food_{idx}"):
                    order["status"] = "Selesai PAID"
                    st.success(f"Jajanan Kamar {order['kamar']} Lunas! Terima kasih banyak!")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# --- 10. PENILAIAN HOTEL ---
elif pilihan_menu == "⭐ Ulasan Kepuasan":
    st.markdown('<div class="main-title">⭐ Kotak Komentar Bintang Tamu</div>', unsafe_allow_html=True)
    with st.form("form_ulasan"):
        nama_tamu = st.text_input("Siapa Nama Panggilanmu?")
        skor_rating = st.slider("Beri Nilai Kepuasan (1-5 Bintang)", 1, 5, 5)
        komentar_tamu = st.text_area("Ceritakan Pengalaman Serumu Menginap Disini")
        
        if st.form_submit_button("Kirim Surat Review 💌"):
            if nama_tamu and komentar_tamu:
                st.session_state.ulasan_log.append({
                    "nama": nama_tamu, "rating": skor_rating, "komentar": komentar_tamu
                })
                st.success("Terima kasih banyak atas feedback ulasan manisnya!")
                st.rerun()

    st.subheader("Buku Cerita Seluruh Tamu")
    st.dataframe(pd.DataFrame(st.session_state.ulasan_log), use_container_width=True)

# --- 11. PUSAT BANTUAN ---
elif pilihan_menu == "❓ Pusat Bantuan":
    st.markdown('<div class="main-title">🛟 Informasi & FAQ</div>', unsafe_allow_html=True)
    with st.expander("⏱️ Jam Berapa Waktu Standar Masuk & Keluar Kamar?"):
        st.write("Check-In bisa dimulai jam 14:00 siang WIB, dan batas maksimal keluar kamar (Check-Out) jam 12:00 siang WIB ya!")
    with st.expander("💳 Apakah Bisa Bayar Pakai Aplikasi E-Wallet Digital?"):
        st.write("Bisa dong! Hotel kami menerima QRIS, OVO, Dana, LinkAja, ShopeePay, serta transfer bank konvensional.")

# --- 12. KONTAK LAYANAN SERVICE ---
elif pilihan_menu == "📞 Kontak Layanan Service":
    st.markdown('<div class="main-title">📞 Hubungi Kakak Penjaga</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="cute-card" style='text-align: center;'>
        <h3>Layanan Resepsionis Peri Hotel (24 Jam Aktif)</h3>
        <p>Jangan sungkan menghubungi kami jika butuh bantuan selimut tebal atau keluhan darurat.</p>
        <p>☎️ <b>Telepon Kamar:</b> Hubungi nomor internal 0</p>
        <p>💬 <b>WhatsApp Peri Resmi:</b> 0812-3456-7890</p>
        <p>📧 <b>Email Layanan Ramah:</b> care@denarahotel.com</p>
    </div>
    """, unsafe_allow_html=True)
