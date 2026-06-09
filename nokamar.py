# ==========================================
# IMPORT
# ==========================================
import streamlit as st
import pandas as pd
from datetime import datetime, date 

st.set_page_config(
    page_title="Denara Hotel System",
    layout="wide",
    page_icon="🏨"
)

# ==========================================
# STYLE (SOFT PINK PREMIUM)
# ==========================================
st.markdown("""
<style>

.main {
    background-color: #FFF6F9;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #FFE3EC;
}

/* CARD */
.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
}

/* TITLE */
.title {
    font-size: 28px;
    font-weight: bold;
    color: #E91E63;
}

/* PROMO BOX */
.promo {
    background-color: #E3F0FF;
    padding: 20px;
    border-radius: 12px;
}

/* BUTTON */
.stButton>button {
    background-color: #FF4D8D;
    color: white;
    border-radius: 10px;
}

/* REVIEW CARD */
.review {
    background-color: #FFF;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
    border: 1px solid #eee;
}

</style>
""", unsafe_allow_html=True)

# =========================
# INISIALISASI DATA (ARRAY)
# =========================

# semua data menggunakan array

# Penampung data master seluruh kamar dari lantai 1 sampai 5 (di RAM)
if "kamar_data" not in st.session_state:
    st.session_state.kamar_data = [
        #LANTAI 1
        {"No Kamar": "101", "Tipe Kamar": "Standard Room", "Harga": "650000", "Status": "🟩 Tersedia"},
        {"No Kamar": "102", "Tipe Kamar": "Standard Room", "Harga": "650000", "Status": "🟩 Tersedia"},
        {"No Kamar": "103", "Tipe Kamar": "Standard Room", "Harga": "650000", "Status": "🟩 Tersedia"},
        {"No Kamar": "104", "Tipe Kamar": "Standard Room", "Harga": "650000", "Status": "🟩 Tersedia"},
        {"No Kamar": "105", "Tipe Kamar": "Standard Room", "Harga": "650000", "Status": "🟩 Tersedia"},
        {"No Kamar": "106", "Tipe Kamar": "Superior Room", "Harga": "1000000", "Status": "🟩 Tersedia"},
        #LANTAI 2
        {"No Kamar": "201", "Tipe Kamar": "Superior Room", "Harga": "1000000", "Status": "🟩 Tersedia"},
        {"No Kamar": "202", "Tipe Kamar": "Superior Room", "Harga": "1000000", "Status": "🟩 Tersedia"},
        {"No Kamar": "203", "Tipe Kamar": "Superior Room", "Harga": "1000000", "Status": "🟩 Tersedia"},
        {"No Kamar": "204", "Tipe Kamar": "Deluxe Room", "Harga": "5000000", "Status": "🟩 Tersedia"},
        {"No Kamar": "205", "Tipe Kamar": "Deluxe Room", "Harga": "5000000", "Status": "🟩 Tersedia"},
        {"No Kamar": "206", "Tipe Kamar": "Deluxe Room", "Harga": "5000000", "Status": "🟩 Tersedia"},
        #LANTAI 3
        {"No Kamar": "301", "Tipe Kamar": "Deluxe Room", "Harga": "5000000", "Status": "🟩 Tersedia"},
        {"No Kamar": "302", "Tipe Kamar": "Deluxe Room", "Harga": "5000000", "Status": "🟩 Tersedia"},
        {"No Kamar": "303", "Tipe Kamar": "Deluxe Room", "Harga": "5000000", "Status": "🟩 Tersedia"},
        {"No Kamar": "304", "Tipe Kamar": "Suite Room", "Harga": "9500000", "Status": "🟩 Tersedia"},
        {"No Kamar": "305", "Tipe Kamar": "Suite Room", "Harga": "9500000", "Status": "🟩 Tersedia"},
        #LANTAI 4
        {"No Kamar": "401", "Tipe Kamar": "Suite Room", "Harga": "9500000", "Status": "🟩 Tersedia"},
        {"No Kamar": "402", "Tipe Kamar": "Suite Room", "Harga": "9500000", "Status": "🟩 Tersedia"},
        {"No Kamar": "403", "Tipe Kamar": "Suite Room", "Harga": "9500000", "Status": "🟩 Tersedia"},
        {"No Kamar": "404", "Tipe Kamar": "Deluxe Room", "Harga": "5000000", "Status": "🟩 Tersedia"},
        {"No Kamar": "405", "Tipe Kamar": "Superior Room", "Harga": "1000000", "Status": "🟩 Tersedia"},
        #LANTAI 5
        {"No Kamar": "501", "Tipe Kamar": "Deluxe Room", "Harga": "5000000", "Status": "🟩 Tersedia"},
        {"No Kamar": "502", "Tipe Kamar": "Suite Room", "Harga": "9500000", "Status": "🟩 Tersedia"},
        {"No Kamar": "503", "Tipe Kamar": "Suite Room", "Harga": "9500000", "Status": "🟩 Tersedia"},
    ]

# harga sewa per malam masing-masing tipe kamar
TARIF_KAMAR = {
    "Standard Room": 650000, 
    "Superior Room": 1000000, 
    "Deluxe Room": 5000000, 
    "Suite Room": 9500000
}

#Array dinamis untuk menyimpan riwayat booking hotel
if "reservasi_log" not in st.session_state:
    st.session_state.reservasi_log = []

#Array dinamis untuk menyimpan histori 
if "history_log" not in st.session_state:
    st.session_state.history_log = []

#Array dinamis untuk antrian pesan makanan pada room service
if "makanan_log" not in st.session_state:
    st.session_state.makanan_log = []

# array untuk riwayat pemesanan makanan
if "riwayat_makanan" not in st.session_state:
    st.session_state.riwayat_makanan = []

#Array agar 
# Keranjang baru (pakai qty + kamar)
if "keranjang" not in st.session_state:
    st.session_state.keranjang = {
        "nama": "",
        "kamar": "",
        "items": []
    }

#Histori Transaksi
if "histori_transaksi" not in st.session_state:
    st.session_state.histori_transaksi = []

#Pemabataln
if "log_pembatalan" not in st.session_state:
    st.session_state.log_pembatalan = []

if "voucher_data" not in st.session_state:
    st.session_state.voucher_data = [
        {"kode": "DISC10", "diskon": 10},
        {"kode": "DENARADEAL", "diskon": 100000},
    ]

#SUBMENU DENARA HOTEL

# ==========================================
# SIDEBAR MENU
# ==========================================
st.sidebar.title("🏨 Denara Hotel")
colA, colB = st.columns([6,2])

with colA:
    st.markdown("<h2 style='color:#E91E63;'>Dashboard</h2>", unsafe_allow_html=True)

with colB:
    st.markdown("""
    <div style='text-align:right'>
    📅 Rabu, 4 Juni 2025 <br>
    👤 Admin
    </div>
    """, unsafe_allow_html=True)

menu_utama = st.sidebar.radio("Menu Utama", [
    "🏠 Dashboard",
    "🏨 Manajemen Kamar",
    "💳 Transaksi",
    "🍽️ Room Service",
    "⭐ Penilaian Hotel",
    "🛟 Bantuan"
])

# Sub menu dinamis
if menu_utama == "🏠 Dashboard":
    pilihan_menu = "🏠 Dashboard"

elif menu_utama == "🏨 Manajemen Kamar":
    pilihan_menu = st.sidebar.radio("Menu Kamar", [
        "📝 Reservasi Baru",
        "🏨 Katalog Kamar",
        "🗺️ Denah Kamar"
    ])

elif menu_utama == "💳 Transaksi":
    pilihan_menu = st.sidebar.radio("Menu Transaksi", [
        "💳 Pembayaran",
        "🔍 Cari Reservasi",
        "📋 Data Reservasi",
        "📜 Histori Transaksi",
        "❌ Pembatalan Reservasi"
    ])

elif menu_utama == "🍽️ Room Service":
    pilihan_menu = st.sidebar.radio("Menu PesanMakanan", [
        "🍽️ Pesan Makanan (DenaraEats)",
        "💳 Pembayaran Makanan", 
])

elif menu_utama == "⭐ Penilaian Hotel":
    pilihan_menu = st.sidebar.radio("Menu Customer", [
        "⭐ Ulasan Kepuasan"
    ])

elif menu_utama == "🛟 Bantuan":
    pilihan_menu = st.sidebar.radio("Menu Laporan", [
        "🛟 Pusat Bantuan",
        "📞 Kontak Layanan Service"
    ])

# ================================
# LOGIKA OPERASIONAL PER MENU
# ==========================================

# --- MENU 1. DASHBOARD ---
if menu_utama == "🏠 Dashboard":
    st.title("🏠 Dashboard")

    st.markdown('<div class="title">Dashboard</div>', unsafe_allow_html=True)
    # ==========================================
    # FOOTER
    # ==========================================
    st.write("")
    st.markdown("""
        <center>© 2025 Denara Hotel❤️</center>
        """, unsafe_allow_html=True)
    # ================= PROMO =================
    st.markdown("""
    <div class="promo">
    <h4>📢 Promo Event Hari Ini</h4>
    <p>Info kupon aktif: Ketik kode <b>DENARADEAL</b> untuk potongan harga <b>Rp 100.000!</b></p>
    <p>Info kupon aktif: Ketik kode <b>DISC10%</b> untuk mendapat diskon 10%</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2 = st.columns(2)

    # ================= KAMAR TERPOPULER =================
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("👑 Kamar Terpopuler")

        kamar = [
            ("Deluxe Room", 12),
            ("Superior Room", 9),
            ("Suite Room", 7),
            ("Standard Room", 6)
        ]

        for i, (nama, jumlah) in enumerate(kamar, start=1):
            st.write(f"{i}. **{nama}**")
            st.progress(jumlah / 12)
            st.caption(f"{jumlah} reservasi")

        st.button("Lihat Semua Kamar")
        st.markdown('</div>', unsafe_allow_html=True)

    # ================= REVIEW =================
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("⭐ Review Terbaru")

        review = [
            ("Andi Pratama", "Pelayanan sangat memuaskan, kamar bersih dan nyaman.", "5.0"),
            ("Siti Nurhaliza", "Lokasi strategis dan sarapan enak.", "4.0"),
            ("Budi Santoso", "Fasilitas lengkap, harga sesuai.", "5.0"),
            ("Rina Wulandari", "Pengalaman menyenangkan, wifi agak lambat.", "4.0")
        ]

        for nama, isi, rating in review:
            st.markdown(f"""
            <div class="review">
            <b>{nama}</b> ⭐ {rating} <br>
            <small>{isi}</small>
            </div>
            """, unsafe_allow_html=True)

        st.button("Lihat Semua Review")
        st.markdown('</div>', unsafe_allow_html=True)

# --- MENU 2: INPUT RESERVASI BARU ---
elif pilihan_menu == "📝 Reservasi Baru":
    st.title(" Reservasi Hotel")
    #Bagi layar jadi kolom kiri (form) dan kolom kanan (rekomendasi)
    col_kiri, col_kanan = st.columns([1.5, 1])

    with col_kiri:
        st.subheader("Biodata Isian Tamu")
        nama = st.text_input("Nama Lengkap")
        hp = st.text_input("No HP / WhatsApp")
        email = st.text_input("Email Tamu")
        #EMAIL
        if email and "@" not in email:
            st.warning("Format email tidak valid")
        pilihan_tipe_kamar = st.selectbox("Tipe Kamar", list(TARIF_KAMAR.keys()))
        jml_tamu = st.number_input("Jumlah Orang Menginap", min_value=1, max_value=10, value=1)
        tgl_in = st.date_input("Tanggal Check-In", date.today())
        tgl_out = st.date_input("Tanggal Check-Out", date.today() + pd.Timedelta(days=1))
        pilihan_late = st.selectbox("Request Jam Check-Out", ["Normal Check-Out", "Late Check-Out (+Rp 50.000)"])
        
        addons = []
        kamar_cocok = None

    with col_kanan:
        #Bagian pengecekan aturan otomatis kelayakan kamar
        st.subheader("🤖 Smart Room Recommendation")

        valid_rekomendasi = True
        pesan_saran= ""

        # ----- ATURAN VALIDASI BERDASARKAN KAPASITAS ------
        #ATURAN 1: Cek Kapasitas orang untuk tipe kamar standard
        if pilihan_tipe_kamar == "Standard Room" and jml_tamu > 2:
            valid_rekomendasi = False
            pesan_saran = "⚠️ Kapasitas Standard Room maksimal 2 orang."

        #Aturan 2: Cek Kapasitas orang untuk tipe kamar superior dan deluxe
        if pilihan_tipe_kamar in ["Superior Room", "Deluxe Room"] and (jml_tamu < 3 or jml_tamu > 4):
            valid_rekomendasi = False
            pesan_saran = ("⚠️ Superior/Deluxe cocok untuk 3-4 orang")

        #Aturan 3: Cek Kapasitas orang untuk tipe kamar suite 
        if pilihan_tipe_kamar == "Suite Room" and jml_tamu <= 4:
            valid_rekomendasi = False
            pesan_saran = ("⚠️ Suite digunakan untuk tamu lebih dari 4 orang.")

        # ----- REKOMENDASI AI -----
        if jml_tamu <= 2:
            rekomendasi = "Standard Room"
        elif jml_tamu <= 4:
            rekomendasi = "Superior Room / Deluxe Room"
        else:
            rekomendasi = "Suite Room"

        #Output Notifikasi
        if not valid_rekomendasi:
            st.warning(pesan_saran)
            #Tampilkan Rekomendai (AI)
            st.info(f"💡 Rekomendasi: **{rekomendasi}**")

            #Tombol pakai rekomendasi
            if st.button("Gunakan Rekomendasi "):
                pilihan_tipe_kamar = rekomendasi
        else:
            st.success(" ✨ Pilihan Kamar sesuai kapasitas hotel.")

            st.markdown("---")
            st.subheader(" ⚙️ Alokasi Kamar Otomatis")

            #pakai tipe final (AI atau user )
            tipe_final = pilihan_tipe_kamar
            kamar_cocok = None
            
            for kamar in st.session_state.kamar_data:
                if (
                    kamar["Tipe Kamar"] == tipe_final
                    and kamar["Status"] == "🟩 Tersedia"
                ):
                    
                    kamar_cocok = kamar
                    break
                
            if kamar_cocok:
                st.success(f"✅ Kamar otomatis: {kamar_cocok['No Kamar']}")
                else:
    st.error("❌ Kamar penuh")
            addons = []
            

            if kamar_cocok:
                st.success(f"✅ Kamar otomatis: {kamar_cocok}")
            else:
                st.error("❌ Kamar penuh")

                st.markdown("---")
                st.subheader(" 🎁 Layanan Tambahan")

                if st.checkbox("Sarapan Pagi Buffet (+Rp 50.000)"): addons.append("Breakfast")
                if st.checkbox("Jemputan Bandara (+Rp 150.000)"): addons.append("Airport Pickup")

        #Tombol Klik buat nge-lock data form bookingan dan dioper ke kasir
        if st.button("Kunci Pemesanan & Lanjut Pembayaran ➡️", type="primary"):
            if not nama:
                st.error("Nama tamu wajib diisi!")
            elif not email or "@" not in email:
                st.error("Email tidak valid!")
            elif not kamar_cocok:
                st.error("Nomor Kamar tidak ditemukan!")
            elif tgl_out <= tgl_in:
                st.error("Tanggal Check-Out harus lebih dari Check-In!")
            else:
                st.session_state.proses_checkout = {
                    "Id Invoice" : id_invoice,
                    "Nama": nama,
                    "Hp": hp,
                    "Email": email,
                    "Kamar": kamar_cocok,
                    "Tipe Kamar": pilihan_tipe_kamar,
                    "Tanggal Check-In": str(tgl_in),
                    "Tanggal Check-Out": str(tgl_out),
                    "Add on": addons,
                    "Late Checkout": pilihan_late
                }

                st.success("Data masuk antrian kasir. Silahkan pilih menu 💳 Pembayaran ")

# --- Menu 3: Katalog Info Kamar ---
elif pilihan_menu == "🏨 Katalog Kamar":
    st.title("🏨 Info Katalog Kamar")
    #looping tampilan harga dan deskripsi sewa kamar hotel
    for tipe, harga, in TARIF_KAMAR.items():
        with st.expander(f"Kategori: {tipe} - Rp {harga,} / Malam"):
            st.write("Failitas Standard Room: 1 Kasur Ukuran Double atau 2 Single Bed, AC, Smart TV, WI-FI, Lemari Pakaian, Teko Listrik, Air Mineral, Toiletries")
            st.write("Failitas Superior Room: Kasur Ukuran Twin Bed atau Double Bed, AC, Smart TV, WI-FI, MIni Fridge, Teko Listrik, Brankas, Air Mineral, Toiletries")
            st.write("Failitas Deluxe Room: Kasur Ukuran King Bed, Sofa, GYM Access, AC, Smart TV, WI-FI, Mini Fridge, Brankas, Mesin Kopi, Bathtub, Toiletries")
            st.write("Failitas Suite Room: Kasur Ukuran King Bed, Memiliki Ruang Tamu, Mini Pantry, Lounge Access, AC, Smart TV, WI-FI, Mini Fridge, Brankas, Mesin Kopi, Jacuzzi, Bathtub, Toiletries")

# --- Menu 4: Denah kamar per lantai
elif pilihan_menu == "🗺️ Denah Kamar":
    st.title("🗺️ Denah Kamar")

    #looping membagi blok visual kotak per lantai (lantai 1-5)
    for lt in range(1, 6):
        st.subheader(f"🏢 Lantai {lt}")
        #menyaring no kamar yang angka depannya sama dengan tingkat lantai
        kamar_lantai = [
            k for k in st.session_state.kamar_data
            if k["No Kamar"].startswith(str(lt))
        ]

        cols = st.columns(6)
        for idx, detail in enumerate(kamar_lantai):
            with cols[idx % 6]:
                st.success(detail["No Kamar"])

# --- Menu 5: Pembayaran ----
elif pilihan_menu == "💳 Pembayaran":
    st.title("💳 Billing Kasir Pembayaran")
    
    #cek data apakah ada atau tidak
    if "proses_checkout" not in st.session_state:
        st.warning("Belum ada data reservasi")
        st.stop()

    out_dt = st.session_state.proses_checkout
    id_invoice = f"INV{datetime.now().strftime('%Y%m%d%H%M%S')}"

    st.subheader("")
    
    # ambil objek datetime buat kalkulasi selisih hari menginap
    dt = st.session_state.proses_checkout
    in_dt = datetime.strptime(dt["check_in"], "%Y-%m-%d")
    out_dt = datetime.strptime(dt["check_out"], "%Y-%m-%d")
    malam = max(1, (out_dt - in_dt).days)

    # hitung kalkulasi tarif biaya rincian

    harga_pokok = TARIF_KAMAR.get(dt["tipe"], 0) * malam
    biaya_late = 50000 if "Late" in dt["late_checkout"] else 0
    biaya_addon = 0
    for addons in dt["add_ons"]:
        if addons == "Breakfast":
            biaya_addon += 500000
        elif addons == "Airport Pickup":
            biaya_addon += 150000


    subtotal = harga_pokok + biaya_late + biaya_addon 

    #VOUCHER DISKON
    st.subheader(" 🎟️ Pilih Voucher")
    if "voucher_pilih" not in st.session_state:
        st.session_state.voucher_pilih = None

    colV1, colV2 = st.columns(2)

    with colV1:
        if st.button("🎉 DENARADEAL\nDiskon Rp100.000"):
            st.session_state.voucher_pilih = ("Fix", 100000)

    with colV2:
        if st.button("🔥 DISC10%\nDiskon 10%"):
            st.session_state.voucher_pilih = ("persen", 10)

    #Hitung 
    total_awal = subtotal
    diskon = 0 

    if st.session_state.voucher_pilih:
        tipe, nilai = st.session_state.voucher_pilih

        if tipe == "Fix":
            diskon = nilai
        elif tipe == "persen":
            diskon = total_awal * (nilai / 100)

    #TOTAL 
    ppn = subtotal * 0.11
    total_tagihan = subtotal + ppn - diskon

    poin = int(total_tagihan / 10000) #kasih bonus loyalitas reward poin

    #Cetak Struk
    st.code(f"""
        ================================================
                      DENARA HOTEL SYSTEM               
                        E-RECEIPT STRUK                 
        ================================================
        Id Invoice      : {dt('id_invoice')}
        Nama Tamu       : {dt['nama']}
        Kamar           : No. {dt['kamar']} ({dt['tipe']})
        Durasi          : {malam} Malam
        ------------------------------------------------
        Biaya Kamar     : Rp {harga_pokok:,}
        Biaya Addons    : Rp {biaya_late + biaya_addon:,}
        PPN 11%         : Rp {ppn:,}
        Diskon Voucher  : -Rp {diskon:,}
        Promo           : {voucher_pilih:,}
        ------------------------------------------------
        TOTAL BAYAR     : Rp {total_tagihan:,}
        Bonus Poin      : +{poin} DenaraPoints
        ================================================
        """, language="text")
    
    cara_bayar = st.selectbox(
        "Pilih Metode Transaksi:",
        ["BCA Transfer Direct", "Mandiri Virtual Account", "Gopay", "Dana"]
    )

    status_bayar = st.selectbox(
        "Status_pembayaran",
        ["PAID (Lunas)", "DP 30%"]
    )

    if st.button("Finalisasi Transaksi & Cetak 📑", type="primary"):

            id_invoice = f"INV{datetime.now().strftime('%Y%m%d%H%M%S')}"

            st.session_state.reservasi_log.append({
                "id": id_invoice,
                "Nama": dt["nama"],
                "Hp": dt["hp"],
                "Email": dt["email"],
                "Kamar": kamar_cocok["No Kamar"],
                "Tipe": dt[pilihan_tipe_kamar],
                "Tanggal Check-In": datetime.strptime(dt["Tanggal Check-In"], "%Y-%m-%d"),
                "Tanggal Check-In": datetime.strptime(dt["Tanggal Check-Out"], "%Y-%m-%d"),
                "Add On": dt[add_ons],
                "Late Checkout": dt[late_checkout],
                "poin_earned": poin
            })

            for kamar in st.session_state.kamar_data:
                if kamar["No Kamar"] == dt["kamar"]:
                    kamar["Status"] = "🟨 Booking"

            del st.session_state.proses_checkout

            st.success("Pembayaran berhasil disimpan!")
            st.rerun()

# --- MENU 6: CARI RESERVASI ---
elif pilihan_menu == "🔍 Cari Reservasi":
    st.title("🔍 Cari Data Reservasi")

    if not st.session_state.reservasi_log:
        st.warning("Belum ada data reservasi")
        st.stop()

    # Input pencarian
    keyword = st.text_input("Masukkan Nama / ID Invoice / No Kamar")

    hasil = []

    if keyword:
        for data in st.session_state.reservasi_log:
            if (
                keyword.lower() in data["nama"].lower()
                or keyword.lower() in data["id"].lower()
                or keyword.lower() in data["kamar"].lower()
            ):
                hasil.append(data)

    # Tampilkan hasil
    if keyword:
        if hasil:
            st.success(f"Ditemukan {len(hasil)} data")
            
            for dt in hasil:
                with st.container():
                    st.markdown("""
                    <div class="card">
                    """, unsafe_allow_html=True)

                    st.subheader(f"🧾 {dt['id']}")
                    st.write(f"👤 Nama       : {dt['nama']}")
                    st.write(f"📱 HP         : {dt['hp']}")
                    st.write(f"📧 Email      : {dt['email']}")
                    st.write(f"🏨 Kamar      : {dt['kamar']} ({dt['tipe']})")
                    st.write(f"📅 Check-in   : {dt['check_in']}")
                    st.write(f"📅 Check-out  : {dt['check_out']}")
                    st.write(f"💰 Total      : Rp {int(dt['total_biaya']):,}")
                    st.write(f"💳 Status     : {dt['status_bayar']}")
                    st.write(f"📌 Metode     : {dt['metode']}")

                    # Badge status
                    if dt["status"] == "Booking":
                        st.info("🟨 Status: Booking")
                    elif dt["status"] == "Check-in":
                        st.success("🟩 Status: Check-in")
                    else:
                        st.error("🟥 Status: Selesai")

                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("❌ Data tidak ditemukan")


# data reservasi
elif pilihan_menu == "📋 Data Reservasi":
    st.title("📋 Data Reservasi Hotel")

    # Ambil dari reservasi_log (yang benar)
    data = st.session_state.reservasi_log

    if not data:
        st.warning("Belum ada data reservasi")
        st.stop()

    # =========================
    # 🔍 FITUR CARI
    # =========================
    st.subheader("🔍 Cari Reservasi")

    keyword = st.text_input("Masukkan Nama / ID / No Kamar")

    if keyword:
        hasil = []
        for d in data:
            if (
                keyword.lower() in d["nama"].lower()
                or keyword.lower() in d["id"].lower()
                or keyword.lower() in d["kamar"].lower()
            ):
                hasil.append(d)
    else:
        hasil = data

    # =========================
    # 📊 TABEL DATA (PRO LOOK)
    # =========================
    st.subheader("📊 Daftar Reservasi")

    df = pd.DataFrame(hasil)
    st.dataframe(df, use_container_width=True)

    st.markdown("---")

    # =========================
    # 📋 DETAIL CARD
    # =========================
    st.subheader("📄 Detail Reservasi")

    for i, d in enumerate(hasil):
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)

            col1, col2 = st.columns([3,2])

            with col1:
                st.write(f"🧾 ID        : {d['id']}")
                st.write(f"👤 Nama      : {d['nama']}")
                st.write(f"📱 HP        : {d['hp']}")
                st.write(f"🏨 Kamar     : {d['kamar']} ({d['tipe']})")
                st.write(f"📅 Check-in  : {d['check_in']}")
                st.write(f"📅 Check-out : {d['check_out']}")

            with col2:
                st.write(f"💰 Total     : Rp {int(d['total_biaya']):,}")
                st.write(f"💳 Status    : {d['status_bayar']}")
                st.write(f"📌 Metode    : {d['metode']}")

                # Status warna
                if d["status"] == "Booking":
                    st.warning("🟨 Booking")
                elif d["status"] == "Check-in":
                    st.success("🟩 Check-in")
                else:
                    st.error("🟥 Selesai")

                # Tombol hapus
                if st.button("❌ Hapus", key=f"hapus_{i}"):
                    st.session_state.reservasi_log.remove(d)
                    st.success("Data berhasil dihapus")
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

# --- Menu 8: Histori Reservasi ---
elif pilihan_menu == "📜 Histori Transaksi":
    st.title("📜 Histori Transaksi Reservasi Hotel")

    if "histori_transaksi" not in st.session_state or len(st.session_state.histori_transaksi) == 0:
        st.warning("Belum ada transaksi reservasi yang selesai")
        st.stop()

    data = st.session_state.histori_transaksi

    # =========================
    # 🔍 FILTER (KHUSUS HOTEL)
    # =========================
    st.subheader("🔍 Cari Histori")

    keyword = st.text_input("Cari Nama / ID / Kamar")

    if keyword:
        hasil = []
        for d in data:
            if (
                keyword.lower() in d["nama"].lower()
                or keyword.lower() in d["id"].lower()
                or keyword.lower() in d["kamar"].lower()
            ):
                hasil.append(d)
    else:
        hasil = data

    # =========================
    # 📊 TABEL HISTORI
    # =========================
    st.subheader("📊 Data Histori Reservasi")

    df = pd.DataFrame(hasil)
    st.dataframe(df, use_container_width=True)

    st.markdown("---")

    # =========================
    # 📄 DETAIL HISTORI HOTEL
    # =========================
    st.subheader("📄 Detail Transaksi Hotel")

    for i, d in enumerate(hasil):
        with st.container():
            col1, col2 = st.columns([3,2])

            with col1:
                st.write(f"🧾 ID        : {d['id']}")
                st.write(f"👤 Nama      : {d['nama']}")
                st.write(f"🏨 Kamar     : {d['kamar']} ({d['tipe']})")
                st.write(f"📅 Check-in  : {d['check_in']}")
                st.write(f"📅 Check-out : {d['check_out']}")
                st.write(f"📅 Transaksi : {d['tanggal']}")

            with col2:
                st.write(f"💰 Total     : Rp {int(d['total']):,}")
                st.write(f"💳 Metode    : {d['metode']}")
                st.success("✅ LUNAS")

                if st.button("🗑️ Hapus", key=f"hapus_histori_{i}"):
                    st.session_state.histori_transaksi.remove(d)
                    st.success("Histori dihapus")
                    st.rerun()

            st.markdown("---")

# --- Menu 9: Pembatalan Reservasi --- 
elif pilihan_menu == "❌ Pembatalan Reservasi":
    st.title("❌ Pembatalan Reservasi")

    if "reservasi_log" not in st.session_state or len(st.session_state.reservasi_log) == 0:
        st.warning("Belum ada data reservasi")
        st.stop()

    data = st.session_state.reservasi_log

    # =========================
    # 🔍 CARI RESERVASI
    # =========================
    st.subheader("🔍 Cari Reservasi")

    keyword = st.text_input("Masukkan Nama / ID / Kamar")

    if keyword:
        hasil = []
        for d in data:
            if (
                keyword.lower() in d["nama"].lower()
                or keyword.lower() in d["id"].lower()
                or keyword.lower() in d["kamar"].lower()
            ):
                hasil.append(d)
    else:
        hasil = data

    # =========================
    # 📋 LIST RESERVASI
    # =========================
    st.subheader("📋 Daftar Reservasi")

    for i, d in enumerate(hasil):
        with st.container():
            col1, col2 = st.columns([3,2])

            with col1:
                st.write(f"🧾 ID        : {d['id']}")
                st.write(f"👤 Nama      : {d['nama']}")
                st.write(f"🏨 Kamar     : {d['kamar']} ({d['tipe']})")
                st.write(f"📅 Check-in  : {d['check_in']}")
                st.write(f"📅 Check-out : {d['check_out']}")

            with col2:
                st.write(f"💰 Total     : Rp {int(d['total_biaya']):,}")
                st.write(f"📌 Status    : {d['status']}")
                st.write(f"💳 Bayar     : {d['status_bayar']}")

                # =========================
                # ❌ LOGIKA PEMBATALAN
                # =========================
                if d["status"] == "Booking" and d["status_bayar"] != "Lunas":

                    if st.button("❌ Batalkan", key=f"batal_{i}"):
                        d["status"] = "Dibatalkan"
                        st.error("Reservasi berhasil dibatalkan")
                        st.rerun()

                elif d["status"] == "Dibatalkan":
                    st.warning("⚠️ Sudah dibatalkan")

                else:
                    st.info("⛔ Tidak bisa dibatalkan")

            st.markdown("---")

            if "log_pembatalan" not in st.session_state:
                st.session_state.log_pembatalan = []

            st.session_state.log_pembatalan.append([
                    "id": d["id"],
                    "nama": d["nama"],
                    "kamar": d["kamar"],
                    "tanggal_batal": datetime.now().strftime("%Y-%m-%d %H:%M")
            ])

# menu 10
elif pilihan_menu == "🍽️ Pesan Makanan (DenaraEats)":
    st.title("🍽️ Pembayaran Makanan")

    menu_makanan = {
        "Nasi Goreng Gila": 35000,
        "Mie Goreng Kampung": 30000,
        "Mie Goreng Cabe Ijo": 30000,
        "Kwetiau Goreng Cabe Ijo": 30000,
        "Ayam Goreng": 30000,
        "Nasi Putih": 30000,
        "Sate Ayam": 30000,
        "Es Teh Manis": 10000,
        "Teh Panas Manis": 10000,
        "Teh Tarik": 10000,
        "Kopi Susu Aren": 20000
    }

    no_kmr = st.selectbox(
    "Nomor Kamar:",
    [k["No Kamar"] for k in st.session_state.kamar_data]
    )

    total = 0
    pesanan_detail = []

    st.write("### Pilih Jumlah")

    for menu, harga in menu_makanan.items():
        qty = st.number_input(f"{menu} (Rp {harga})", min_value=0, key=menu)

        if qty > 0:
            subtotal = qty * harga
            total += subtotal
            pesanan_detail.append(f"{menu} x{qty}")

    st.write("💰 Total:", total)

    if st.button("🛒 Pesan"):
        if total > 0:
            st.session_state.makanan_log.append({
                "kamar": no_kmr,
                "pesanan": pesanan_detail,
                "total": total,
                "status": "Belum Bayar"
            })

            st.success("Pesanan masuk ke kasir!")

            # reset qty
            for menu in menu_makanan:
                st.session_state[menu] = 0

            st.rerun()
        else:
            st.warning("Pesan dulu!")

 # menu 11
elif pilihan_menu == "🍽️ Pesan Makanan (DenaraEats)":
    st.title("💳 Pembayaran Makanan")

    for i, d in enumerate(st.session_state.makanan_log):

        if d["status"] == "Belum Bayar":

            st.subheader(f"Kamar {d['kamar']}")
            st.write("Pesanan:", ", ".join(d["pesanan"]))

            total_awal = d["total"]
            diskon = 0

            # 🔥 VOUCHER
            col1, col2 = st.columns(2)

            with col1:
                if st.button("🎟️ DENARADEAL", key=f"deal_{i}"):
                    diskon = 100000

            with col2:
                if st.button("🎟️ DISC10%", key=f"disc_{i}"):
                    diskon = int(total_awal * 0.1)

            total_bayar = max(0, total_awal - diskon)

            st.write(f"Total Awal: Rp {total_awal}")
            st.write(f"Diskon: Rp {diskon}")
            st.write(f"💰 Total Bayar: Rp {total_bayar}")

            if st.button("✅ Bayar", key=f"bayar_{i}"):

                waktu = datetime.now().strftime("%d-%m-%Y %H:%M")

                st.success("Pembayaran berhasil!")

                # 🧾 STRUK KHUSUS
                st.markdown(f"""
                <div style="
                    background-color:#000;
                    color:#00FF90;
                    padding:20px;
                    border-radius:10px;
                    font-family:monospace;
                ">
                <h3 style="text-align:center;">DENARA HOTEL</h3>
                <p style="text-align:center;">ROOM SERVICE RECEIPT</p>
                <hr>
                <p>Kamar : {d['kamar']}</p>
                <p>Waktu : {waktu}</p>
                <hr>
                <p>Pesanan:</p>
                <ul>
                    {''.join([f"<li>{item}</li>" for item in d["pesanan"]])}
                </ul>
                <hr>
                <p>Total Awal : Rp {total_awal}</p>
                <p>Diskon     : Rp {diskon}</p>
                <h4>Total Bayar: Rp {total_bayar}</h4>
                <hr>
                <p style="text-align:center;">Terima Kasih 🙏</p>
                </div>
                """, unsafe_allow_html=True)

                # 🔥 SIMPAN KE RIWAYAT
                st.session_state.riwayat_makanan.append({
                    "kamar": d["kamar"],
                    "pesanan": d["pesanan"],
                    "total": total_bayar,
                    "waktu": waktu
                })

                d["status"] = "Selesai"

                st.rerun()

# Menu 12 ulasan kepusan pelanggan
elif pilihan_menu == "⭐ Ulasan Kepuasan":
    st.title("⭐ Ulasan Kepuasan Pelanggan")

    if "ulasan" not in st.session_state:
        st.session_state.ulasan = []

    nama = st.text_input("Nama Anda")
    rating = st.slider("Rating", 1, 5)
    komentar = st.text_area("Komentar")

    if st.button("Kirim Ulasan"):
        st.session_state.ulasan.append({
            "nama": nama,
            "rating": rating,
            "komentar": komentar
        })
        st.success("Terima kasih atas ulasan Anda!")

    st.divider()
    st.subheader("📋 Daftar Ulasan")

    for u in st.session_state.ulasan:
        st.write(f"👤 {u['nama']} | ⭐ {u['rating']}")
        st.write(f"💬 {u['komentar']}")
        st.write("---")

# menu 13 pusat bantuan
elif pilihan_menu == "🛟 Pusat Bantuan":
    st.title("🛟 Pusat Bantuan")

    with st.expander("❓ Cara Reservasi"):
        st.write("Pilih menu reservasi, isi data, lalu lanjut ke pembayaran.")

    with st.expander("🍽️ Cara Pesan Room Service"):
        st.write("Masuk ke menu Room Service, pilih makanan, lalu kirim ke dapur.")

    with st.expander("💳 Cara Pembayaran"):
        st.write("Masuk ke kasir, cek total, lalu klik bayar.")

    with st.expander("📞 Kendala Sistem"):
        st.write("Hubungi admin jika terjadi error atau bug.")

# menu 14 kontak layanan service
elif pilihan_menu == "📞 Kontak Layanan Service":
    st.title("📞 Kontak Layanan Hotel")

    st.write("🏨 Denara Hotel")
    st.write("📍 Alamat: Jl. Mawar No. 123, Indonesia")
    st.write("📞 Telepon: 0812-3456-7890")
    st.write("📧 Email: denarahotel@gmail.com")

    st.divider()

    st.subheader("📩 Kirim Pesan")

    nama = st.text_input("Nama")
    pesan = st.text_area("Pesan Anda")

    if st.button("Kirim Pesan"):
        st.success("Pesan Anda telah dikirim ke customer service!")
