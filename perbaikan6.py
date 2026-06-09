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

# Ramuan denah kamar (beberapa kamar sengaja dibikin penuh biar kelihatan simulasi jalannya)
if "kamar_data" not in st.session_state:
    st.session_state.kamar_data = [
        {"No Kamar": "101", "Tipe Kamar": "Standard Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "102", "Tipe Kamar": "Standard Room", "Status": "🟨 Direservasi"}, # Udah ada yang nempatin dari awal gess
        {"No Kamar": "103", "Tipe Kamar": "Standard Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "104", "Tipe Kamar": "Standard Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "105", "Tipe Kamar": "Standard Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "201", "Tipe Kamar": "Superior Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "202", "Tipe Kamar": "Superior Room", "Status": "🟨 Direservasi"}, # Kamar ini juga ngeboking dari awal
        {"No Kamar": "203", "Tipe Kamar": "Superior Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "204", "Tipe Kamar": "Deluxe Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "301", "Tipe Kamar": "Deluxe Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "302", "Tipe Kamar": "Deluxe Room", "Status": "🟨 Direservasi"}, # Isinya anak sultan nih pas baru buka
        {"No Kamar": "303", "Tipe Kamar": "Suite Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "401", "Tipe Kamar": "Suite Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "402", "Tipe Kamar": "Suite Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "403", "Tipe Kamar": "Deluxe Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "501", "Tipe Kamar": "Deluxe Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "502", "Tipe Kamar": "Suite Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "503", "Tipe Kamar": "Suite Room", "Status": "🟨 Direservasi"}, # Kamar VIP full booked duluan
    ]

# Data mentah tamu-tamu yang lagi mager di kamar yang keisi tadi
if "reservasi_log" not in st.session_state: 
    st.session_state.reservasi_log = [
        {"id": "RSV-102202", "nama": "Budi Santoso", "hp": "08123444", "email": "budi@gmail.com", "kamar": "102", "tipe": "Standard Room", "check_in": "2026-06-01", "check_out": "2026-06-05", "total_biaya": 2600000, "status_bayar": "PAID (Langsung Lunas)", "metode": "Transfer BCA", "status": "🟨 Direservasi", "food_charge": 0},
        {"id": "RSV-202202", "nama": "Siti Rahma", "hp": "08125555", "email": "siti@gmail.com", "kamar": "202", "tipe": "Superior Room", "check_in": "2026-06-03", "check_out": "2026-06-07", "total_biaya": 4000000, "status_bayar": "PAID (Langsung Lunas)", "metode": "Mandiri Virtual Account", "status": "🟨 Direservasi", "food_charge": 65000}, # Doi sempet jajan nih, ada bill makanan nempel
        {"id": "RSV-503202", "nama": "Rayyanza", "hp": "08129999", "email": "rayyanza@gmail.com", "kamar": "503", "tipe": "Suite Room", "check_in": "2026-06-05", "check_out": "2026-06-12", "total_biaya": 66500000, "status_bayar": "DP Dulu 30%", "metode": "Dana", "status": "🟨 Direservasi", "food_charge": 0},
    ]

# Wadah penampung data kosong biar gak error pas dipanggil di halaman lain
if "histori_transaksi" not in st.session_state: st.session_state.histori_transaksi = []
if "log_pembatalan" not in st.session_state: st.session_state.log_pembatalan = []
if "makanan_log" not in st.session_state: st.session_state.makanan_log = []
if "voucher_terpilih" not in st.session_state: st.session_state.voucher_terpilih = "Tanpa Voucher"
if "ulasan_log" not in st.session_state: 
    st.session_state.ulasan_log = [{"nama": "Andi Pratama", "rating": 5, "komentar": "Keren bgt, jacuzzi di lantai 5 mantap betul!"}]

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

# Buat misahin mana sub-menu yang diklik sama si user
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
    st.metric("Kamar Kosong Yang Siap Dipesan (Lantai 1-5)", f"{kamar_kosong} Kamar")
    
    st.markdown("""
    <div class="promo">
    <h4>📢 Info Promo Buat Kamu</h4>
    <p>Gunakan Kode Voucher spesial <b>DISC10%</b> pada menu pembayaran tiket untuk diskon maksimal!</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h3>👑 Kamar Paling Laris</h3>', unsafe_allow_html=True)
        st.write("**Suite Room (Lantai 5 VIP)**")
        st.caption("Fasilitas Andalan: Private Jacuzzi & Private Swimming Pool")
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
        email = st.text_input("Alamat Email")
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
        saran = "Standard Room" if jml_tamu <= 2 else ("Superior/Deluxe" if jml_tamu <= 4 else "Suite Room")
        st.info(f"Karena kamu bawa {jml_tamu} orang, cocoknya pilih **{saran}**.")
        
        # Cari kamar kosong di master data yang emang masih ijo alias ready
        kamar_cocok = next((k for k in st.session_state.kamar_data if k["Tipe Kamar"] == pilihan_tipe and k["Status"] == "🟩 Tersedia"), None)
        
        if kamar_cocok:
            st.success(f"Kamar Ready! Kamu dapet **No. {kamar_cocok['No Kamar']}**")
        else:
            st.error("Waduh, kamar tipe ini lagi full booked di semua lantai.")

        st.markdown("---")
        st.subheader("🎁 Mau Tambah Fasilitas Ekstra?")
        addons = []
        if st.checkbox("Sarapan Pagi Sepuasnya (+Rp 50.000)"): addons.append("Breakfast")
        if st.checkbox("Antar Jemput Bandara (+Rp 150.000)"): addons.append("Airport Pickup")

        if st.button("Booking & Lanjut Ke Pembayaran ➡️", type="primary"):
            if not nama or not kamar_cocok or tgl_out <= tgl_in:
                st.error("Isi formnya yang bener dong, atau cek lagi tanggal check-out nya.")
            else:
                # Titip data reservasi sementara ke session state sebelum dibayar di kasir
                st.session_state.proses_checkout = {
                    "id_invoice": f"RSV-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "nama": nama, "hp": hp, "email": email, "kamar": kamar_cocok,
                    "tipe": pilihan_tipe, "check_in": str(tgl_in), "check_out": str(tgl_out),
                    "add_on": addons, "late_checkout": pilihan_late
                }
                st.session_state.voucher_terpilih = "Tanpa Voucher" 
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
    st.title("🗺️ Map Letak Kamar Hotel Lantai 1 s/d 5")
    
    for lt in range(1, 6):
        # Nyocokin teks nama lantai khusus buat tipe kamar lantai 1-4 sesuai request user
        if lt == 1:
            st.subheader("🏢 Lantai 1 — ROOM STANDARD")
        elif lt == 2:
            st.subheader("🏢 Lantai 2 — SUPERIOR ROOM")
        elif lt == 3:
            st.subheader("🏢 Lantai 3 — DELUXE ROOM")
        elif lt == 4:
            st.subheader("🏢 Lantai 4 — SUITE ROOM")
        else:
            st.subheader(f"🏢 Lantai {lt}") # Biar lantai 5 tetap aman terkendali
            
        kamar_lantai = [k for k in st.session_state.kamar_data if k["No Kamar"].startswith(str(lt))]
        cols = st.columns(6)
        for idx, detail in enumerate(kamar_lantai):
            with cols[idx % 6]:
                if detail["Status"] == "🟩 Tersedia": 
                    st.success(f"🚪 {detail['No Kamar']}\n({detail['Tipe Kamar'][:4]})")
                else: 
                    st.error(f"🟨 {detail['No Kamar']}\n(TERISI)")

# --- 5. PEMBAYARAN TIKET RESERVASI ---
elif pilihan_menu == "💳 Pembayaran Tiket":
    st.title("💳 Menu Pembayaran Billing Kamar")
    if "proses_checkout" not in st.session_state:
        st.warning("Belum ada antrian kamar yang mau dibayar nih. Buka menu 'Reservasi Baru' dulu ya.")
        st.stop()

    dt = st.session_state.proses_checkout
    # Hitung selisih hari buat dikaliin tarif kamar (minimal semalam)
    malam = max(1, (datetime.strptime(dt["check_out"], "%Y-%m-%d") - datetime.strptime(dt["check_in"], "%Y-%m-%d")).days)
    
    harga_pokok = TARIF_KAMAR.get(dt["tipe"], 0) * malam
    biaya_extra = (50000 if "Late" in dt["late_checkout"] else 0) + (50000 if "Breakfast" in dt["add_on"] else 0) + (150000 if "Airport Pickup" in dt["add_on"] else 0)
    subtotal = harga_pokok + biaya_extra

    st.subheader("🎟️ Klik Tombol Di Bawah Buat Pasang Voucher")
    v_col1, v_col2, v_col3 = st.columns(3)
    with v_col1:
        if st.button("Gak Pake Voucher", type="secondary" if st.session_state.voucher_terpilih != "Tanpa Voucher" else "primary"):
            st.session_state.voucher_terpilih = "Tanpa Voucher"; st.rerun()
    with v_col2:
        if st.button("🎁 Voucher DENARADEAL (-Rp100k)", type="primary" if st.session_state.voucher_terpilih == "DENARADEAL" else "secondary"):
            st.session_state.voucher_terpilih = "DENARADEAL"; st.rerun()
    with v_col3:
        if st.button("🔥 Voucher DISC10% (Diskon 10%)", type="primary" if st.session_state.voucher_terpilih == "DISC10%" else "secondary"):
            st.session_state.voucher_terpilih = "DISC10%"; st.rerun()

    diskon = 100000 if st.session_state.voucher_terpilih == "DENARADEAL" else (subtotal * 0.1 if st.session_state.voucher_terpilih == "DISC10%" else 0)
    total_tagihan = (subtotal + (subtotal * 0.11)) - diskon
    st.info(f"Voucher Yang Kamu Pasang: **{st.session_state.voucher_terpilih}**")

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
    Pajak PPN 11%: Rp {int(subtotal * 0.11):,}
    Potongan     : -Rp {int(diskon):,} ({st.session_state.voucher_terpilih})
    ------------------------------------------------
    TOTAL BILL   : Rp {int(total_tagihan):,}
    ================================================
    """, language="text")

    metode = st.selectbox("Mau Bayar Lewat Mana?", ["Transfer BCA", "Mandiri Virtual Account", "GoPay", "OVO", "Dana"])
    status_bayar = st.selectbox("Opsi Bayar", ["PAID (Langsung Lunas)", "DP Dulu 30%"])

    if st.button("Konfirmasi Bayar & Ambil Kode Kamar ✔️", type="primary"):
        # Masukin datanya ke log database utama biar kecatat aktif menginap
        st.session_state.reservasi_log.append({
            "id": dt["id_invoice"], "nama": dt["nama"], "hp": dt["hp"], "email": dt["email"],
            "kamar": dt["kamar"]["No Kamar"], "tipe": dt["tipe"], "check_in": dt["check_in"],
            "check_out": dt["check_out"], "total_biaya": total_tagihan, "status_bayar": status_bayar,
            "metode": metode, "status": "🟨 Direservasi", "food_charge": 0
        })
        # Ubah status kamarnya biar berubah jadi kuning (terisi) di denah layout
        for kamar in st.session_state.kamar_data:
            if kamar["No Kamar"] == dt["kamar"]["No Kamar"]:
                kamar["Status"] = "🟨 Direservasi"
        del st.session_state.proses_checkout # Hapus antrian transaksi biar bersih
        st.success("Pembayaran Berhasil! Kamar udah sah jadi milikmu. Catat ID Booking-mu untuk akses Room Service.")
        st.rerun()

# --- 6. CEK DETAIL & CHECK-OUT MANDIRI ---
elif pilihan_menu == "🔍 Cek Detail & Check-Out":
    st.title("🔍 Menu Cek Data & Check-Out Mandiri (Akses Tamu)")
    st.write("Silakan masukkan Nomor Kamar Anda untuk memverifikasi data dan melakukan check-out.")
    
    input_kamar = st.text_input("Konfirmasi Nomor Kamar Anda (Contoh: 102 / 202):")
    
    if input_kamar:
        # Ngintip nyari data reservasi aktif berdasarkan nomor kamarnya
        tamu = next((d for d in st.session_state.reservasi_log if d["kamar"] == input_kamar), None)
        
        if tamu:
            st.markdown(f"""
            <div class="card">
                <h4>🧾 ID Booking: {tamu['id']}</h4>
                <p>👤 <b>Nama Tamu:</b> {tamu['nama']}<br>
                📅 <b>Periode Menginap:</b> {tamu['check_in']} s/d {tamu['check_out']}<br>
                💰 <b>Biaya Kamar Awal:</b> Rp {int(tamu['total_biaya']):,}<br>
                🍽️ <b>Akumulasi Tagihan Kuliner (Room Service):</b> Rp {int(tamu['food_charge']):,}</p>
                <hr style="border-top:1px dashed #ccc;">
                <h4><b>Grand Total Tagihan: Rp {int(tamu['total_biaya'] + tamu['food_charge']):,}</b></h4>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Saya Selesai Menginap & Ajukan Check-Out", type="primary"):
                # Balikin status nomor kamar jadi ijo (kosong) lagi
                for k in st.session_state.kamar_data:
                    if k["No Kamar"] == tamu["kamar"]:
                        k["Status"] = "🟩 Tersedia"
                
                # Masukin data transaksinya ke kotak arsip sejarah lama
                st.session_state.histori_transaksi.append({
                    "id": tamu["id"], "nama": tamu["nama"], "kamar": tamu["kamar"], "tipe": tamu["tipe"],
                    "grand_total": tamu["total_biaya"] + tamu["food_charge"], "status": "✅ Selesai (Check-Out)"
                })
                st.session_state.reservasi_log.remove(tamu) # Kick dari log hunian aktif
                st.success("Proses Check-Out Berhasil! Terima kasih banyak telah mempercayai Denara Hotel.")
                st.rerun()
        else:
            st.error("Data reservasi aktif untuk nomor kamar tersebut tidak ditemukan di sistem kami.")

# --- 7. HISTORI & PEMBATALAN SAYA ---
elif pilihan_menu == "📜 Histori & Pembatalan":
    st.title("📜 Menu Riwayat & Pembatalan Mandiri Tamu")
    tab_riwayat, tab_batal = st.tabs(["Arsip Histori Menginap", "Ajukan Pembatalan Kamar"])
    
    with tab_riwayat:
        st.subheader("📋 Buku Riwayat Selesai")
        cari_nama = st.text_input("Ketik nama Anda untuk mencari riwayat arsip pesanan lama:")
        if cari_nama:
            df_histori = pd.DataFrame(st.session_state.histori_transaksi)
            if not df_histori.empty:
                # Filter nyari string nama yang mirip-mirip ketikan user
                hasil_cari = df_histori[df_histori['nama'].str.lower().str.contains(cari_nama.lower())]
                st.dataframe(hasil_cari, use_container_width=True)
            else:
                st.info("Tidak ada riwayat menginap atas nama tersebut.")

    with tab_batal:
        st.subheader("❌ Ajukan Pembatalan Kamar Mandiri")
        input_id = st.text_input("Masukkan ID Booking Kamu untuk Mengajukan Pembatalan (Contoh: RSV-102202):")
        
        if input_id:
            rsv = next((d for d in st.session_state.reservasi_log if d["id"] == input_id), None)
            if rsv:
                st.warning(f"Apakah Anda benar-benar yakin ingin membatalkan pesanan Kamar No. {rsv['kamar']} atas nama {rsv['nama']}?")
                if st.button("Ya, Batalkan Pesanan Saja"):
                    # Kosongin lagi kamar hotelnya biar bisa dicaplok orang lain
                    for k in st.session_state.kamar_data:
                        if k["No Kamar"] == rsv["kamar"]: 
                            k["Status"] = "🟩 Tersedia"
                    
                    st.session_state.log_pembatalan.append({
                        "id": rsv["id"], "nama": rsv["nama"], "kamar": rsv["kamar"], "waktu_batal": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.session_state.reservasi_log.remove(rsv) # Hapus dari daftar hunian
                    st.success("Pembatalan Sukses! Kamar otomatis dilepas kembali agar bisa dipesan tamu lain.")
                    st.rerun()
            else:
                st.error("ID Booking tidak ditemukan atau statusnya sudah tidak aktif.")

# --- 8. ROOM SERVICE: PESAN MAKANAN ---
elif pilihan_menu == "🍽️ Pesan Makanan":
    st.title("🍽️ Room Service Kuliner - Kirim Ke Kamar")
    
    st.subheader("Verifikasi Hunian Kamar")
    no_kmr = st.text_input("Konfirmasi Nomor Kamar Kamu Saat Ini (Contoh: 102 atau 202):")
    
    if not no_kmr:
        st.info("Silakan input nomor kamar kamu dulu di atas untuk memesan makanan.")
        st.stop()
        
    # Validasi dulu, kamar yang mesen beneran berpenghuni gak nih, biar gak fiktif
    tamu_menginap = next((t for t in st.session_state.reservasi_log if t["kamar"] == no_kmr), None)
    
    if not tamu_menginap:
        st.error("Nomor kamar tidak aktif/kosong. Pastikan kamu menginput kamar yang sudah kamu booking.")
        st.stop()
        
    st.success(f"Terverifikasi! Selamat memesan hidangan favorit Anda, Kak **{tamu_menginap['nama']}**.")
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
            # Cari tau dulu kamar bersangkutan udah punya nota pesanan makan nyangkut apa gak
            kamar_exist = next((m for m in st.session_state.makanan_log if m["kamar"] == no_kmr and m["status"] == "Belum Bayar"), None)
            
            if kamar_exist:
                # Kalo ada bill makanan gantung lama, tinggal kita tambahin isinya biar gak bikin baris baru
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
                # Kalo bersih, kita buatin nota pesanan food service perdana
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

# --- 9. ROOM SERVICE: BAYAR FOOD SERVICE (KASIR MANDIRI TAMU) ---
elif pilihan_menu == "💳 Bayar Room Service":
    st.title("💳 Kasir Tagihan Room Service Kuliner Mandiri")
    
    kamar_tamu_input = st.text_input("Input Nomor Kamar Kamu untuk Mengecek Bill Makanan:")
    if not kamar_tamu_input:
        st.info("Masukkan nomor kamar Anda untuk memuat tagihan hidangan makanan.")
        st.stop()
        
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
            
            # Pilihan pembayaran kuliner sesuai request (Tanpa Cash, e-wallet dipecah riil)
            pilihan_metode = st.selectbox("Pilih Jenis Pembayaran Kuliner", ["Room Charge (Masuk Bill Kamar Utama)", "GoPay", "OVO", "Dana", "Debit Card"])
            
            if st.button(f"Proses & Cetak Struk Kamar {order['kamar']}"):
                if pilihan_metode == "Room Charge (Masuk Bill Kamar Utama)":
                    # Lempar totalan makanannya biar ditimbun ke tagihan check-out hotel nanti
                    tamu_aktif = next((d for d in st.session_state.reservasi_log if d["kamar"] == kamar_tamu_input), None)
                    if tamu_aktif:
                        tamu_aktif["food_charge"] += order["total"]
                        order["status"] = "Selesai PAID (Masuk Bill Kamar)"
                        st.success("Sukses! Biaya makanan dimasukkan ke billing kamar. Pembayaran dilakukan sekalian saat Check-Out nanti.")
                    else:
                        st.error("Gagal menyambungkan ke billing kamar utama.")
                else:
                    order["status"] = "Selesai PAID" # Langsung lunas via e-wallet dkk
                    st.success(f"Pembayaran kuliner kamar {order['kamar']} via {pilihan_metode} sukses terverifikasi!")
                
                # Tampilkan Struk Kasir Cetak
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
