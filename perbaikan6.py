import streamlit as st
import pandas as pd
from datetime import datetime, date 

st.set_page_config(page_title="Denara Hotel", layout="wide", page_icon="🏨")

# ==========================================
# GAYA-GAYAAN INTERFACE (BIAR PINK ESTETIK)
# ==========================================
st.markdown("""
<style>
    .main { background-color: #FFF6F9; }
    section[data-testid="stSidebar"] { background-color: #FFE3EC; }
    .card { background-color: white; padding: 25px; border-radius: 15px; box-shadow: 0px 4px 15px rgba(0,0,0,0.04); margin-bottom: 20px; border: 1px solid #FFE3EC; }
    .title { font-size: 32px; font-weight: bold; color: #E91E63; margin-bottom: 10px; }
    .promo { background-color: #E3F0FF; padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 5px solid #2196F3; }
    .stButton>button { background-color: #FF4D8D; color: white; border-radius: 10px; width: 100%; font-weight: bold; }
    .stButton>button:hover { background-color: #E91E63; color: white; }
    .review-box { background-color: #FFF6F9; padding: 12px; border-radius: 12px; margin-bottom: 10px; border: 1px solid #FFE3EC; }
    .facility-tag { background-color: #FFE3EC; color: #E91E63; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 500; margin-right: 5px; display: inline-block; margin-bottom: 5px;}
    .price-text { font-size: 22px; font-weight: bold; color: #E91E63; }
    .promo-box { border: 2px dashed #FF4D8D; padding: 10px; border-radius: 8px; background-color: #FFF0F5; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA MASTER & KONDISI AWAL DATABASE
# ==========================================
TARIF_KAMAR = {
    "Standard Room": 650000, 
    "Superior Room": 1000000, 
    "Deluxe Room": 5000000, 
    "Suite Room": 9500000
}

FASILITAS_KAMAR = {
    "Standard Room": ["Free Wi-Fi", "Air Conditioning", "Smart TV 32\"", "Shower Bathroom", "Complimentary Water"],
    "Superior Room": ["Free Wi-Fi", "Air Conditioning", "Smart TV 43\"", "Water Heater", "Mini Refrigerator", "Coffee & Tea Maker"],
    "Deluxe Room": ["Free Wi-Fi", "Air Conditioning", "Smart TV 55\"", "Luxury Bathtub", "Mini Bar", "Safety Deposit Box", "Private Balcony"],
    "Suite Room": ["Free Wi-Fi", "Air Conditioning", "Smart TV 65\"", "Private Jacuzzi", "Premium Mini Bar", "Separate Living Room", "24/7 Butler Service", "Private Swimming Pool"]
}

MENU_MAKANAN = {
    "Nasi Goreng Kampung": 35000, 
    "Mie Goreng Cabe Ijo": 30000, 
    "Ayam Goreng Serundeng": 40000, 
    "Es Teh Manis Premium": 12000, 
    "Kopi Susu Aren": 20000
}

# Ramuan denah kamar (Lantai 1-4 disesuaikan dengan tipe kamar masing-masing lantai)
if "kamar_data" not in st.session_state:
    st.session_state.kamar_data = [
        {"No Kamar": "101", "Tipe Kamar": "Standard Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "102", "Tipe Kamar": "Standard Room", "Status": "🟨 Direservasi"}, 
        {"No Kamar": "103", "Tipe Kamar": "Standard Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "104", "Tipe Kamar": "Standard Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "105", "Tipe Kamar": "Standard Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "201", "Tipe Kamar": "Superior Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "202", "Tipe Kamar": "Superior Room", "Status": "🟨 Direservasi"}, 
        {"No Kamar": "203", "Tipe Kamar": "Superior Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "204", "Tipe Kamar": "Superior Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "301", "Tipe Kamar": "Deluxe Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "302", "Tipe Kamar": "Deluxe Room", "Status": "🟨 Direservasi"}, 
        {"No Kamar": "303", "Tipe Kamar": "Deluxe Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "401", "Tipe Kamar": "Suite Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "402", "Tipe Kamar": "Suite Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "403", "Tipe Kamar": "Suite Room", "Status": "🟨 Direservasi"}, 
    ]

# Data tamu-tamu aktif awal
if "reservasi_log" not in st.session_state: 
    st.session_state.reservasi_log = [
        {"id": "RSV-102202", "nama": "Budi Santoso", "hp": "08123444", "email": "budi@gmail.com", "kamar": "102", "tipe": "Standard Room", "check_in": "2026-06-01", "check_out": "2026-06-05", "total_biaya": 2600000, "status_bayar": "PAID (Langsung Lunas)", "metode": "Transfer BCA", "status": "🟨 Direservasi", "food_charge": 0},
        {"id": "RSV-202202", "nama": "Siti Rahma", "hp": "08125555", "email": "siti@gmail.com", "kamar": "202", "tipe": "Superior Room", "check_in": "2026-06-03", "check_out": "2026-06-07", "total_biaya": 4000000, "status_bayar": "PAID (Langsung Lunas)", "metode": "Mandiri Virtual Account", "status": "🟨 Direservasi", "food_charge": 65000},
        {"id": "RSV-403202", "nama": "Rayyanza", "hp": "08129999", "email": "rayyanza@gmail.com", "kamar": "403", "tipe": "Suite Room", "check_in": "2026-06-05", "check_out": "2026-06-12", "total_biaya": 66500000, "status_bayar": "DP Dulu 30%", "metode": "Dana", "status": "🟨 Direservasi", "food_charge": 0},
    ]

if "histori_transaksi" not in st.session_state: 
    st.session_state.histori_transaksi = [
        {"id": "RSV-101000", "nama": "Joko Widodo", "kamar": "101", "tipe": "Standard Room", "grand_total": 1300000, "status": "✅ Selesai (Check-Out)"}
    ]
if "log_pembatalan" not in st.session_state: st.session_state.log_pembatalan = []
if "makanan_log" not in st.session_state: st.session_state.makanan_log = []
if "kode_voucher_input" not in st.session_state: st.session_state.kode_voucher_input = ""
if "voucher_terpasang" not in st.session_state: st.session_state.voucher_terpasang = ""
if "ulasan_log" not in st.session_state: 
    st.session_state.ulasan_log = [{"nama": "Andi Pratama", "rating": 5, "komentar": "Keren bgt, nginep di lantai 4 berasa eksklusif!"}]

# ==========================================
# SIDEBAR MENUS
# ==========================================
st.sidebar.title("🏨 Denara Hotel")
menu_utama = st.sidebar.radio("Menu Utama", [
    "🏠 Dashboard", 
    "🏨 Manajemen Kamar", 
    "💳 Area Transaksi Tamu", 
    "🍽️ Room Service", 
    "⭐ Penilaian Hotel", 
    "🛟 Bantuan"
])

if menu_utama == "🏠 Dashboard": pilihan_menu = "🏠 Dashboard"
elif menu_utama == "🏨 Manajemen Kamar":
    pilihan_menu = st.sidebar.radio("Sub-Menu Kamar", ["📝 Reservasi Baru", "🏨 Katalog Kamar", "🗺️ Denah Kamar"])
elif menu_utama == "💳 Area Transaksi Tamu":
    pilihan_menu = st.sidebar.radio("Sub-Menu Transaksi", ["💳 Pembayaran Tiket", "🔍 Cek Detail & Check-Out", "📜 Histori & Pembatalan"])
elif menu_utama == "🍽️ Room Service":
    pilihan_menu = st.sidebar.radio("Sub-Menu Room Service", ["🍽️ Pesan Makanan", "💳 Bayar Room Service"])
elif menu_utama == "⭐ Penilaian Hotel": pilihan_menu = "⭐ Ulasan Kepuasan"
elif menu_utama == "🛟 Bantuan":
    pilihan_menu = st.sidebar.radio("Sub-Menu Bantuan", ["❓ Pusat Bantuan", "📞 Kontak Layanan Service"])

# ==========================================
# PROSES LOGIKA TIAP SUB-MENU
# ==========================================

# --- 1. DASHBOARD ---
if pilihan_menu == "🏠 Dashboard":
    st.markdown('<div class="title">🏠 Selamat Datang di Denara Hotel</div>', unsafe_allow_html=True)
    kamar_kosong = len([k for k in st.session_state.kamar_data if k["Status"] == "🟩 Tersedia"])
    st.metric("Kamar Kosong Yang Siap Dipesan (Lantai 1-4)", f"{kamar_kosong} Kamar")
    
    st.markdown("""
    <div class="promo">
    <h4>📢 Info Promo Buat Kamu</h4>
    <p>Gunakan Kode Voucher spesial <b>DISC10%</b> pada menu pembayaran tiket untuk diskon maksimal!</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h3>👑 Kamar Paling Laris</h3>', unsafe_allow_html=True)
        st.write("**Suite Room (Lantai 4 VIP)**")
        st.caption("Fasilitas Andalan: Private Jacuzzi & Premium Services")
        st.progress(0.95)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><h3>⭐ Kata Tamu Yang Udah Nginep</h3>', unsafe_allow_html=True)
        for u in st.session_state.ulasan_log[-2:]:
            st.markdown(f'<div class="review-box"><b>{u["nama"]}</b> (⭐ {u["rating"]})<br><small>"{u["komentar"]}"</small></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 2. RESERVASI BARU ---
elif pilihan_menu == "📝 Reservasi Baru":
    st.title("📝 Form Reservasi Hotel")
    col_kiri, col_kanan = st.columns([1.5, 1])

    with col_kiri:
        st.subheader("Isi Data Diri Dulu Yuk")
        nama = st.text_input("Nama Lengkap (Sesuai KTP)")
        hp = st.text_input("Nomor WhatsApp Aktif")
        
        # Penambahan karakter @ secara otomatis pada field email
        email = st.text_input("Alamat Email", value="@gmail.com")
        pilihan_tipe = st.selectbox("Mau Kamar Tipe Apa?", list(TARIF_KAMAR.keys()))
        
        st.markdown("**Fasilitas Yang Bakal Kamu Dapet:**")
        for fas in FASILITAS_KAMAR[pilihan_tipe]:
            st.markdown(f'<span class="facility-tag">✔️ {fas}</span>', unsafe_allow_html=True)
            
        jml_tamu = st.number_input("Buat Berapa Orang?", min_value=1, max_value=8, value=2)
        tgl_in = st.date_input("Tanggal Check-In", date.today())
        tgl_out = st.date_input("Tanggal Check-Out", date.today() + pd.Timedelta(days=1))
        pilihan_late = st.selectbox("Mau Keluar Jam Berapa?", ["Normal Check-Out", "Late Check-Out (+Rp 50.000)"])

    with col_kanan:
        st.subheader("🤖 Saran Kamar Dari Bot")
        saran = "Standard Room" if jml_tamu <= 2 else ("Superior Room" if jml_tamu <= 4 else "Suite Room")
        st.info(f"Karena kamu bawa {jml_tamu} orang, cocoknya pilih **{saran}**.")
        
        # Pemetaan tipe kamar ke nomor lantai yang benar agar nomor kamar yang didapat sinkron
        pemetaan_lantai = {
            "Standard Room": "1",
            "Superior Room": "2",
            "Deluxe Room": "3",
            "Suite Room": "4"
        }
        
        # --- PERBAIKAN LOGIKA BOT KEDUA ---
        # Memastikan lantai target mengikuti 'pilihan_tipe' kamar yang benar-benar dipilih/disesuaikan oleh user
        lantai_target = pemetaan_lantai[pilihan_tipe]
        
        # Bot mencari kamar kosong yang tipenya sesuai DAN berada di lantai yang tepat
        kamar_cocok = next((k for k in st.session_state.kamar_data if k["Tipe Kamar"] == pilihan_tipe and k["Status"] == "🟩 Tersedia" and k["No Kamar"].startswith(lantai_target)), None)
        
        if kamar_cocok:
            st.success(f"Kamar Ready! Kamu mendapatkan tipe **{pilihan_tipe}** dengan **No. {kamar_cocok['No Kamar']}** di Lantai {lantai_target}.")
        else:
            st.error(f"Waduh, tipe kamar {pilihan_tipe} di Lantai {lantai_target} saat ini sedang penuh.")

        st.markdown("---")
        st.subheader("🎁 Mau Tambah Fasilitas Ekstra?")
        addons = []
        if st.checkbox("Sarapan Pagi Sepuasnya (+Rp 50.000)"): addons.append("Breakfast")
        if st.checkbox("Antar Jemput Bandara (+Rp 150.000)"): addons.append("Airport Pickup")

        if st.button("Booking & Lanjut Ke Pembayaran ➡️", type="primary"):
            if not nama or not kamar_cocok or tgl_out <= tgl_in or email == "@gmail.com":
                st.error("Isi formnya yang bener dong, pastikan email sudah diisi lengkap dan kamar tersedia.")
            else:
                st.session_state.proses_checkout = {
                    "id_invoice": f"RSV-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "nama": nama, "hp": hp, "email": email, "kamar": kamar_cocok,
                    "tipe": pilihan_tipe, "check_in": str(tgl_in), "check_out": str(tgl_out),
                    "add_on": addons, "late_checkout": pilihan_late
                }
                st.session_state.voucher_terpasang = "" 
                st.success("Sip! Data udah kesimpen, gass ke sub-menu 'Pembayaran Tiket' buat ngelunasin.")

# --- 3. KATALOG KAMAR ---
elif pilihan_menu == "🏨 Katalog Kamar":
    st.title("🏨 Katalog Pilihan & Spesifikasi Eksklusif Kamar")
    st.write("Temukan kenyamanan terbaik selama menginap di Denara Hotel:")
    
    for tipe, harga in TARIF_KAMAR.items():
        with st.container():
            st.markdown(f"""
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <span style="font-size: 24px; font-weight: bold; color: #E91E63;">✨ {tipe}</span>
                    <span class="price-text">Rp {harga:,} <small style="color: #777; font-size: 14px; font-weight: normal;">/ Malam</small></span>
                </div>
                <hr style="border: 0; border-top: 1px solid #FFE3EC; margin: 12px 0;">
                <p style="margin-bottom: 8px; font-weight: bold; color: #555;">Fasilitas Unggulan Kamar:</p>
            """, unsafe_allow_html=True)
            
            for fas in FASILITAS_KAMAR[tipe]:
                st.markdown(f'<span class="facility-tag">⭐ {fas}</span>', unsafe_allow_html=True)
                
            st.markdown('</div>', unsafe_allow_html=True)

# --- 4. DENAH KAMAR ---
elif pilihan_menu == "🗺️ Denah Kamar":
    st.title("🗺️ Map Letak Kamar Hotel Lantai 1 s/d 4")
    
    for lt in range(1, 5):
        if lt == 1:
            st.subheader("🏢 Lantai 1 — ROOM STANDARD")
        elif lt == 2:
            st.subheader("🏢 Lantai 2 — SUPERIOR ROOM")
        elif lt == 3:
            st.subheader("🏢 Lantai 3 — DELUXE ROOM")
        elif lt == 4:
            st.subheader("🏢 Lantai 4 — SUITE ROOM")
            
        kamar_lantai = [k for k in st.session_state.kamar_data if k["No Kamar"].startswith(str(lt))]
        cols = st.columns(6)
        for idx, detail in enumerate(kamar_lantai):
            with cols[idx % 6]:
                if detail["Status"] == "🟩 Tersedia": 
                    st.success(f"🚪 {detail['No Kamar']}\n(Masih tersedia)")
                else: 
                    st.error(f"🟨 {detail['No Kamar']}\n(Ada yang booking)")

# --- 5. PEMBAYARAN TIKET RESERVASI ---
elif pilihan_menu == "💳 Pembayaran Tiket":
    st.title("💳 Menu Pembayaran Billing Kamar")
    if "proses_checkout" not in st.session_state:
        st.warning("Belum ada antrian kamar yang mau dibayar nih. Buka menu 'Reservasi Baru' dulu ya.")
        st.stop()

    dt = st.session_state.proses_checkout
    malam = max(1, (datetime.strptime(dt["check_out"], "%Y-%m-%d") - datetime.strptime(dt["check_in"], "%Y-%m-%d")).days)
    
    harga_pokok = TARIF_KAMAR.get(dt["tipe"], 0) * malam
    biaya_extra = (50000 if "Late" in dt["late_checkout"] else 0) + (50000 if "Breakfast" in dt["add_on"] else 0) + (150000 if "Airport Pickup" in dt["add_on"] else 0)
    subtotal = harga_pokok + biaya_extra

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎟️ Kupon Promo & Diskon")
    st.caption("Punya kode kupon? Masukkan kodenya di bawah untuk mendapatkan potongan harga spesial!")
    
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.markdown('<div class="promo-box"><b>🔥 DISC10%</b><br><small>Diskon potongan 10% dari total transaksi kamu!</small></div>', unsafe_allow_html=True)
    with p_col2:
        st.markdown('<div class="promo-box"><b>🎁 DENARADEAL</b><br><small>Potongan langsung Rp 100.000 tanpa minimum transaksi.</small></div>', unsafe_allow_html=True)
        
    vc_input_col, vc_btn_col = st.columns([3, 1])
    with vc_input_col:
        kode_input = st.text_input("Masukkan kode voucher di sini:", value=st.session_state.voucher_terpasang, placeholder="Contoh: DISC10%").strip()
    with vc_btn_col:
        st.write("##") 
        if st.button("Terapkan Kupon"):
            if kode_input.upper() in ["DISC10%", "DENARADEAL"]:
                st.session_state.voucher_terpasang = kode_input.upper()
                st.toast(f"🎉 Voucher {st.session_state.voucher_terpasang} berhasil dipasang!", icon="✅")
            elif kode_input == "":
                st.session_state.voucher_terpasang = ""
                st.toast("Voucher dihapus.", icon="ℹ️")
            else:
                st.error("Kode kupon salah atau kedaluwarsa.")
                st.session_state.voucher_terpasang = ""
                
    if st.session_state.voucher_terpasang:
        st.success(f"🟢 **Kupon Diterapkan:** Anda menghemat menggunakan kode **{st.session_state.voucher_terpasang}**")
    st.markdown('</div>', unsafe_allow_html=True)

    diskon = 100000 if st.session_state.voucher_terpasang == "DENARADEAL" else (subtotal * 0.1 if st.session_state.voucher_terpasang == "DISC10%" else 0)
    pajak = subtotal * 0.11
    total_tagihan = (subtotal + pajak) - diskon

    st.code(f"""
    ================================================
               DENARA HOTEL - NOTA BOOKING
    ================================================
    ID Booking   : {dt['id_invoice']}
    Nama Tamu    : {dt['nama']}
    Nomor Kamar  : Kamar No. {dt['kamar']['No Kamar']} ({dt['tipe']})
    Durasi       : {malam} Malam ({dt['check_in']} s/d {dt['check_out']})
    ------------------------------------------------
    Harga Kamar  : Rp {harga_pokok:,}
    Biaya Ekstra : Rp {biaya_extra:,}
    Pajak PPN 11%: Rp {int(pajak):,}
    Potongan     : -Rp {int(diskon):,} ({st.session_state.voucher_terpasang if st.session_state.voucher_terpasang else 'Tanpa Kupon'})
    ------------------------------------------------
    TOTAL BILL   : Rp {int(total_tagihan):,}
    ================================================
    """, language="text")

    metode = st.selectbox("Mau Bayar Lewat Mana?", ["Transfer BCA", "Mandiri Virtual Account", "GoPay", "OVO", "Dana"])
    status_bayar = st.selectbox("Opsi Bayar", ["PAID (Langsung Lunas)", "DP Dulu 30%"])

    if st.button("Konfirmasi Bayar & Ambil Kode Kamar ✔️", type="primary"):
        st.session_state.reservasi_log.append({
            "id": dt["id_invoice"], "nama": dt["nama"], "hp": dt["hp"], "email": dt["email"],
            "kamar": dt["kamar"]["No Kamar"], "tipe": dt["tipe"], "check_in": dt["check_in"],
            "check_out": dt["check_out"], "total_biaya": total_tagihan, "status_bayar": status_bayar,
            "metode": metode, "status": "🟨 Direservasi", "food_charge": 0
        })
        for kamar in st.session_state.kamar_data:
            if kamar["No Kamar"] == dt["kamar"]["No Kamar"]:
                kamar["Status"] = "🟨 Direservasi"
        del st.session_state.proses_checkout
        st.success("Pembayaran Berhasil! Kamar udah sah jadi milikmu. Catat ID Booking-mu untuk akses Room Service.")
        st.rerun()

# --- 6. CEK DETAIL & CHECK-OUT MANDIRI ---
elif pilihan_menu == "🔍 Cek Detail & Check-Out":
    st.title("🔍 Menu Cek Data & Check-Out Mandiri (Akses Tamu)")
    st.write("Silakan masukkan salah satu data identitas booking Anda untuk memuat rincian billing kamar.")
    
    input_pencarian = st.text_input("Masukkan Nomor Kamar / Nama Tamu / ID Booking Anda:", placeholder="Contoh: 102 atau Budi Santoso atau RSV-102202").strip()
    
    if input_pencarian:
        tamu = next((d for d in st.session_state.reservasi_log if 
                     d["kamar"] == input_pencarian or 
                     input_pencarian.lower() in d["nama"].lower() or 
                     d["id"] == input_pencarian), None)
        
        if tamu:
            st.markdown(f"""
            <div class="card">
                <h4>🧾 ID Booking: {tamu['id']}</h4>
                <p>👤 <b>Nama Tamu:</b> {tamu['nama']}<br>
                🚪 <b>Nomor Kamar:</b> {tamu['kamar']} ({tamu['tipe']})<br>
                📅 <b>Periode Menginap:</b> {tamu['check_in']} s/d {tamu['check_out']}<br>
                💰 <b>Biaya Kamar Awal:</b> Rp {int(tamu['total_biaya']):,}<br>
                🍽️ <b>Akumulasi Tagihan Kuliner (Room Service):</b> Rp {int(tamu['food_charge']):,}</p>
                <hr style="border-top:1px dashed #ccc;">
                <h4><b>Grand Total Tagihan: Rp {int(tamu['total_biaya'] + tamu['food_charge']):,}</b></h4>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Saya Selesai Menginap & Ajukan Check-Out", type="primary"):
                for k in st.session_state.kamar_data:
                    if k["No Kamar"] == tamu["kamar"]:
                        k["Status"] = "🟩 Tersedia"
                
                st.session_state.histori_transaksi.append({
                    "id": tamu["id"], 
                    "nama": tamu["nama"], 
                    "kamar": tamu["kamar"], 
                    "tipe": tamu["tipe"],
                    "grand_total": tamu["total_biaya"] + tamu["food_charge"], 
                    "status": "✅ Selesai (Check-Out)"
                })
                
                st.session_state.reservasi_log.remove(tamu)
                st.success("Proses Check-Out Berhasil! Kamar Anda sudah tersedia kembali untuk tamu lain dan data tersimpan di arsip histori.")
                st.rerun()
        else:
            st.error("Data reservasi aktif dengan keyword tersebut tidak ditemukan di sistem kami.")

# --- 7. HISTORI & PEMBATALAN SAYA ---
elif pilihan_menu == "📜 Histori & Pembatalan":
    st.title("📜 Menu Riwayat & Pembatalan Mandiri Tamu")
    tab_riwayat, tab_batal = st.tabs(["Arsip Histori Menginap", "Ajukan Pembatalan Kamar"])
    
    with tab_riwayat:
        st.subheader("📋 Buku Riwayat Selesai")
        cari_nama = st.text_input("Ketik nama Anda / No Kamar / ID Booking untuk mencari riwayat arsip pesanan lama:")
        if cari_nama:
            df_histori = pd.DataFrame(st.session_state.histori_transaksi)
            if not df_histori.empty:
                hasil_cari = df_histori[
                    df_histori['nama'].str.lower().str.contains(cari_nama.lower()) | 
                    df_histori['kamar'].astype(str).str.contains(cari_nama) | 
                    df_histori['id'].str.lower().str.contains(cari_nama.lower())
                ]
                if not hasil_cari.empty:
                    st.dataframe(hasil_cari, use_container_width=True)
                else:
                    st.info("Tidak ada riwayat menginap yang cocok dengan kata kunci tersebut.")
            else:
                st.info("Tidak ada riwayat menginap atas nama tersebut.")
        else:
            if st.session_state.histori_transaksi:
                st.dataframe(pd.DataFrame(st.session_state.histori_transaksi), use_container_width=True)

    with tab_batal:
        st.subheader("❌ Ajukan Pembatalan Kamar Mandiri")
        input_batal = st.text_input("Masukkan ID Booking / Nama Tamu / No Kamar Kamu untuk Mengajukan Pembatalan:", placeholder="Contoh: RSV-102202 atau Budi atau 102")
        
        if input_batal:
            rsv = next((d for d in st.session_state.reservasi_log if 
                         d["id"] == input_batal or 
                         input_batal.lower() in d["nama"].lower() or 
                         d["kamar"] == input_batal), None)
                         
            if rsv:
                st.warning(f"Apakah Anda benar-benar yakin ingin membatalkan pesanan Kamar No. {rsv['kamar']} atas nama {rsv['nama']}?")
                if st.button("Ya, Batalkan Pesanan Saja"):
                    for k in st.session_state.kamar_data:
                        if k["No Kamar"] == rsv["kamar"]: 
                            k["Status"] = "🟩 Tersedia"
                    
                    st.session_state.log_pembatalan.append({
                        "id": rsv["id"], "nama": rsv["nama"], "kamar": rsv["kamar"], "waktu_batal": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.session_state.reservasi_log.remove(rsv)
                    st.success("Pembatalan Sukses! Kamar otomatis dilepas kembali agar bisa dipesan tamu lain.")
                    st.rerun()
            else:
                st.error("Data booking aktif tidak ditemukan atau statusnya sudah tidak aktif.")

# --- 8. ROOM SERVICE: PESAN MAKANAN (FLEXIBLE MULTI-INPUT CONFRIMATION) ---
elif pilihan_menu == "🍽️ Pesan Makanan":
    st.title("🍽️ Room Service Kuliner - Kirim Ke Kamar")
    
    st.subheader("Verifikasi Hunian Kamar")
    # PERBAIKAN: Input sekarang fleksibel untuk nomor kamar, nama tamu, atau kode reservasi
    input_verifikasi = st.text_input("Konfirmasi Nomor Kamar / Nama Tamu / ID Booking Anda Saat Ini:", placeholder="Contoh: 102 atau Budi Santoso atau RSV-102202")
    
    if not input_verifikasi:
        st.info("Silakan konfirmasi identitas menginap kamu dulu di atas untuk memesan makanan.")
        st.stop()
        
    tamu_menginap = next((t for t in st.session_state.reservasi_log if 
                          t["kamar"] == input_verifikasi or 
                          input_verifikasi.lower() in t["nama"].lower() or 
                          t["id"] == input_verifikasi), None)
    
    if not tamu_menginap:
        st.error("Data hunian kamar tidak ditemukan atau tidak aktif. Pastikan data yang dimasukkan benar.")
        st.stop()
        
    no_kmr = tamu_menginap["kamar"] # Kunci nomor kamar asli hasil pencarian data
    st.success(f"Terverifikasi! Kamar No. {no_kmr} atas nama Kak **{tamu_menginap['nama']}** siap memesan hidangan.")
    st.write("### Pilih Menu Makanan Di Bawah:")
    
    total_order = 0
    items_dipesan = []
    
    for menu, harga in MENU_MAKANAN.items():
        qty = st.number_input(f"{menu} (Rp {harga:,})", min_value=0, step=1, key=f"food_{menu}")
        if qty > 0:
            total_order += (qty * harga)
            items_dipesan.append({"item": menu, "qty": qty, "subtotal": qty * harga})
            
    st.markdown(f"### Total Belanjaan Kuliner Baru: **Rp {total_order:,}**")
    
    if st.button("Pesan Sekarang & Kirim Ke Dapur 🛒"):
        if total_order > 0:
            kamar_exist = next((m for m in st.session_state.makanan_log if m["kamar"] == no_kmr and m["status"] == "Belum Bayar"), None)
            
            if kamar_exist:
                for item_baru in items_dipesan:
                    idx_makanan = next((idx for idx, s in enumerate(kamar_exist["pesanan_detail"]) if s["item"] == item_baru["item"]), -1)
                    if idx_makanan != -1:
                        kamar_exist["pesanan_detail"][idx_makanan]["qty"] += item_baru["qty"]
                        kamar_exist["pesanan_detail"][idx_makanan]["subtotal"] += item_baru["subtotal"]
                    else:
                        kamar_exist["pesanan_detail"].append(item_baru)
                kamar_exist["total"] = sum(x["subtotal"] for x in kamar_exist["pesanan_detail"])
                st.success(f"Pesanan tambahan berhasil masuk ke list Kamar {no_kmr}!")
            else:
                st.session_state.makanan_log.append({
                    "id_order": f"FS-{datetime.now().strftime('%M%S')}",
                    "kamar": no_kmr, 
                    "pesanan_detail": items_dipesan, 
                    "total": total_order, 
                    "status": "Belum Bayar"
                })
                st.success("Pesanan dikirim! Chef kami bakal langsung masak pesananmu.")
        else:
            st.warning("Pilih dulu makanannya dong, porsi tidak boleh kosong.")

# --- 9. ROOM SERVICE: BAYAR FOOD SERVICE (FLEXIBLE MULTI-INPUT CONFRIMATION) ---
elif pilihan_menu == "💳 Bayar Room Service":
    st.title("💳 Kasir Tagihan Room Service Kuliner Mandiri")
    
    # PERBAIKAN: Input kasir makanan juga dibuat fleksibel agar mempermudah tamu
    input_kasir = st.text_input("Input Nomor Kamar / Nama Tamu / ID Booking Kamu untuk Mengecek Bill Makanan:", placeholder="Contoh: 102, Budi, atau RSV-102202")
    if not input_kasir:
        st.info("Masukkan identitas Anda untuk memuat tagihan hidangan makanan.")
        st.stop()
        
    # Cari tahu nomor kamar aslinya terlebih dahulu dari manifes tamu aktif
    tamu_terkait = next((t for t in st.session_state.reservasi_log if 
                         t["kamar"] == input_kasir or 
                         input_kasir.lower() in t["nama"].lower() or 
                         t["id"] == input_kasir), None)
                         
    kamar_tamu_input = tamu_terkait["kamar"] if tamu_terkait else input_kasir
    
    order = next((m for m in st.session_state.makanan_log if m["kamar"] == kamar_tamu_input and m["status"] == "Belum Bayar"), None)
    
    if not order:
        st.success("Mantap! Semua tagihan makanan untuk kamar ini sudah bersih / lunas semua.")
    else:
        with st.container():
            st.markdown(f'<div class="card"><h4>🛎️ Bill Room Service Kamar No: {order["kamar"]}</h4>', unsafe_allow_html=True)
            st.write("**Rincian Pesanan Kuliner:**")
            for item in order["pesanan_detail"]:
                st.write(f"- {item['item']} ({item['qty']} Porsi) — Rp {item['subtotal']:,}")
                
            st.markdown(f"Total Yang Harus Dibayar: **Rp {order['total']:,}**")
            
            pilihan_metode = st.selectbox("Pilih Jenis Pembayaran Kuliner", ["Room Charge (Masuk Bill Kamar Utama)", "GoPay", "OVO", "Dana", "Debit Card"])
            
            if st.button(f"Proses & Cetak Struk Kamar {order['kamar']}"):
                # INTEGRASI: Jika memilih Room Charge, tagihan makanan digabungkan ke bill kamar utama
                if pilihan_metode == "Room Charge (Masuk Bill Kamar Utama)":
                    tamu_aktif = next((d for d in st.session_state.reservasi_log if d["kamar"] == order["kamar"]), None)
                    if tamu_aktif:
                        tamu_aktif["food_charge"] += order["total"] # Masuk ke sub-total food charge bill kamar utama
                        order["status"] = "Selesai PAID (Masuk Bill Kamar)"
                        st.success("Sukses! Biaya makanan dimasukkan ke billing kamar. Pembayaran dilakukan sekalian saat Check-Out nanti.")
                    else:
                        st.error("Gagal menyambungkan ke billing kamar utama karena status hunian kamar tidak terdeteksi.")
                else:
                    order["status"] = "Selesai PAID"
                    st.success(f"Pembayaran kuliner kamar {order['kamar']} via {pilihan_metode} sukses terverifikasi!")
                
                st.code(f"""
                ================================================
                     DENARA HOTEL - ROOM SERVICE RECEIPT
                ================================================
                ID Order     : {order['id_order']}
                Nomor Kamar  : Kamar No. {order['kamar']}
                Waktu Bayar  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                Jenis Bayar  : {pilihan_metode}
                ------------------------------------------------
                TOTAL BILL   : Rp {order['total']:,}
                STATUS       : LUNAS / PAID
                ================================================
                """, language="text")
                st.rerun()

# --- 10. PENILAIAN HOTEL ---
elif pilihan_menu == "⭐ Ulasan Kepuasan":
    st.title("⭐ Kotak Kepuasan & Review Tamu")
    with st.form("form_ulasan"):
        nama_tamu = st.text_input("Nama Kamu / No Kamar")
        skor_rating = st.slider("Kasih Rating Bintang Berapa? (1 - 5)", 1, 5, 5)
        komentar_tamu = st.text_area("Tulis Kesan Pesan Selama Liburan Di Sini")
        
        if st.form_submit_button("Kirim Review"):
            if nama_tamu and komentar_tamu:
                st.session_state.ulasan_log.append({
                    "nama": nama_tamu, "rating": skor_rating, "komentar": komentar_tamu
                })
                st.success("Makasih banyak ya ulasannya! Berharga bgt buat tim hotel.")
                st.rerun()
            else:
                st.error("Isi dulu review-nya, jangan dikosongin.")
                
    st.subheader("Semua Kumpulan Review Tamu")
    st.dataframe(pd.DataFrame(st.session_state.ulasan_log), use_container_width=True)

# --- 11. PUSAT BANTUAN ---
elif pilihan_menu == "❓ Pusat Bantuan":
    st.title("🛟 FAQ - Pusat Bantuan Informasi")
    with st.expander("⏱️ Jam Berapa Batas Waktu Check-In & Check-Out Standard?"):
        st.write("Masuk kamar jam 14:00 WIB yaa, kalau keluar maksimal jam 12:00 WIB biar kamar bisa diberesin dulu.")
    with st.expander("💳 Bisa Bayar Pake QRIS Atau E-Wallet Gak?"):
        st.write("Bisa bgt! Kita nerima Dana, Gopay, Ovo, ShopeePay, sama Transfer VA Bank kok.")

# --- 12. KONTAK LAYANAN SERVICE ---
elif pilihan_menu == "📞 Kontak Layanan Service":
    st.title("📞 Kontak Hubung & Layanan Fast Respon")
    st.markdown("""
    <div class="card">
        <h3>Layanan Operator Resepsionis (24 Jam Nonstop)</h3>
        <p>Hubungi kontak di bawah kalau ada masalah darurat di kamar atau butuh bantuan teknisi.</p>
        <ul>
            <li><b>Telpon Kamar:</b> Pencet angka 0 langsung ke resepsionis</li>
            <li><b>WhatsApp Chat:</b> 0812-3456-7890</li>
            <li><b>Email Support:</b> care@denarahotel.com</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
