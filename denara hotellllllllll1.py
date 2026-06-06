# ==========================================
# IMPORT LIBRARY UTAMA
# ==========================================
import streamlit as st
import pandas as pd
from datetime import datetime, date

# Setingan awal layout browser biar melebar
st.set_page_config(
    page_title="Denara Hotel System",
    layout="wide",
    page_icon="🏨"
)
# ==========================================
# UI STYLE (SOFT PINK)
# ==========================================
st.markdown("""
<style>
.main {background-color: #FFF1F2;}
section[data-testid="stSidebar"] {background-color: #FFE4E6;}
h1, h2, h3 {color:#BE185D;}
.stButton>button {
    background-color:#F472B6;
    color:white;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# INISIALISASI DATA SIMULASI (SESSION STATE)
# ==========================================

#LOGIN
if "login" not in st.session_state:
    st.session_state.login = False
if not st.session_state.login:
    st.title("🔐 Login Hotel")

    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pw == "123":
            st.session_state.login = True
            st.session_state.role = "admin"
        else:
            st.error("Login gagal")

    st.stop()
    
# Penampung data master seluruh kamar dari lantai 1 sampai 5
if "kamar_data" not in st.session_state:
    st.session_state.kamar_data = {
        # Lantai 1
        "101": {"tipe": "Standard Room", "harga": 300000, "status": "🟩 Tersedia", "view": "No View"},
        "102": {"tipe": "Standard Room", "harga": 300000, "status": "🟥 Terisi", "view": "Garden View"},
        "103": {"tipe": "Standard Room", "harga": 300000, "status": "🟩 Tersedia", "view": "Garden View"},
        "104": {"tipe": "Standard Room", "harga": 300000, "status": "🟩 Tersedia", "view": "No View"},
        "105": {"tipe": "Deluxe Room", "harga": 500000, "status": "🟨 Booking", "view": "City View"},
        "106": {"tipe": "Deluxe Room", "harga": 500000, "status": "🟩 Tersedia", "view": "City View"},
        # Lantai 2
        "201": {"tipe": "Deluxe Room", "harga": 500000, "status": "🟩 Tersedia", "view": "Pool View"},
        "202": {"tipe": "Deluxe Room", "harga": 500000, "status": "🟩 Tersedia", "view": "Pool View"},
        "203": {"tipe": "Deluxe Room", "harga": 500000, "status": "🟩 Tersedia", "view": "Garden View"},
        "204": {"tipe": "Family Room", "harga": 800000, "status": "🟥 Terisi", "view": "City View"},
        "205": {"tipe": "Family Room", "harga": 800000, "status": "🟩 Tersedia", "view": "Pool View"},
        "206": {"tipe": "Family Room", "harga": 800000, "status": "🟩 Tersedia", "view": "Garden View"},
        # Lantai 3
        "301": {"tipe": "Family Room", "harga": 800000, "status": "🟩 Tersedia", "view": "City View"},
        "302": {"tipe": "Family Room", "harga": 800000, "status": "🟩 Tersedia", "view": "Pool View"},
        "303": {"tipe": "Suite Room", "harga": 1200000, "status": "🟩 Tersedia", "view": "Ocean View"},
        "304": {"tipe": "Suite Room", "harga": 1200000, "status": "🟩 Tersedia", "view": "Ocean View"},
        "305": {"tipe": "Suite Room", "harga": 1200000, "status": "🟩 Tersedia", "view": "City View"},
        # Lantai 4
        "401": {"tipe": "Standard Room", "harga": 300000, "status": "🟩 Tersedia", "view": "No View"},
        "402": {"tipe": "Standard Room", "harga": 300000, "status": "🟩 Tersedia", "view": "Garden View"},
        "403": {"tipe": "Deluxe Room", "harga": 500000, "status": "🟩 Tersedia", "view": "City View"},
        "404": {"tipe": "Deluxe Room", "harga": 500000, "status": "🟩 Tersedia", "view": "Pool View"},
        "405": {"tipe": "Family Room", "harga": 800000, "status": "🟩 Tersedia", "view": "Garden View"},
        # Lantai 5
        "501": {"tipe": "Suite Room", "harga": 1200000, "status": "🟩 Tersedia", "view": "Skyline View"},
        "502": {"tipe": "Suite Room", "harga": 1200000, "status": "🟩 Tersedia", "view": "Skyline View"},
        "503": {"tipe": "Suite Room", "harga": 1200000, "status": "🟩 Tersedia", "view": "Ocean View"}
    }

# Array dinamis untuk nyimpan riwayat bookingan transaksi tamu
if "reservasi_log" not in st.session_state:
    st.session_state.reservasi_log = [
        {
            "id": "INV2026001", "nama": "Andi", "hp": "0812345678", "email": "andi@mail.com",
            "kamar": "102", "tipe": "Standard Room", "bed_type": "Double Bed",
            "check_in": "2026-06-01", "check_out": "2026-06-03", "status": "Check-In", 
            "total_biaya": 600000, "status_bayar": "PAID", "metode": "Transfer BCA", 
            "late_checkout": "Normal Check-Out", "poin_earned": 60
        }
    ]

# Array dinamis untuk antrean pesanan makanan room service
if "makanan_log" not in st.session_state:
    st.session_state.makanan_log = [
        {"kamar": "102", "pesanan": "Nasi Goreng Spesial + Es Teh Manis", "total": 65000, "status": "Diproses"}
    ]

if "keranjang" not in st.session_state: st.session_state.keranjang = []

# Array dinamis untuk nampung review atau rating dari tamu
if "ulasan_log" not in st.session_state:
    st.session_state.ulasan_log = [
        {"nama": "Andi", "rating": 5, "komentar": "Kamarnya bersih, pelayanan mantap!", "tanggal": "2026-06-03"}
    ]

# Kamus harga sewa per malam masing-masing tipe kamar
TARIF_KAMAR = {
    "Standard Room": 300000, 
    "Deluxe Room": 500000, 
    "Family Room": 800000, 
    "Suite Room": 1200000
}

# ==========================================
# SIDEBAR MENU NAVIGATION
# ==========================================
st.sidebar.markdown("# 🏨 Denara Hotel System")
st.sidebar.caption("Sistem Log Internal Kontrol")
st.sidebar.markdown("---")

menu_utama = st.sidebar.radio("📂 Pilih Kategori", [
    "🏠 Dashboard",
    "🏨 Manajemen Kamar",
    "🍽️ Layanan Hotel",
    "💳 Transaksi & Data",
    "⭐ Customer Experience",
    "📊 Laporan & Bantuan"
])

# Sub menu dinamis
if menu_utama == "🏠 Dashboard":
    pilihan_menu = "Dashboard"

elif menu_utama == "🏨 Manajemen Kamar":
    pilihan_menu = st.sidebar.radio("Menu Kamar", [
        "📝 Reservasi Baru",
        "🏨 Daftar Katalog Kamar",
        "🗺️ Room Map Denah"
    ])

elif menu_utama == "🍽️ Layanan Hotel":
    pilihan_menu = "🍽️ Room Service (DenaraEats)"

elif menu_utama == "💳 Transaksi & Data":
    pilihan_menu = st.sidebar.radio("Menu Transaksi", [
        "💳 Kasir & Pembayaran",
        "🔍 Cari Reservasi",
        "📋 Data Master Log",
        "📜 Histori Transaksi"
    ])

elif menu_utama == "⭐ Customer Experience":
    pilihan_menu = st.sidebar.radio("Menu Customer", [
        "⭐ Ulasan Kepuasan",
        "👤 Poin Loyalitas VIP",
        "🏷️ Info Voucher Promo"
    ])

elif menu_utama == "📊 Laporan & Bantuan":
    pilihan_menu = st.sidebar.radio("Menu Laporan", [
        "📊 Analisis Keuangan",
        "🛟 Pusat Bantuan"
    ])

# ==========================================
# LOGIKA OPERASIONAL PER HALAMAN MENU
# ==========================================

# --- MENU 1: DASHBOARD SUMMARY ---
if pilihan_menu == "Dashboard":
    st.title("🏠 Dashboard Summary")
    
    # Hitung jumlah kondisi kamar saat ini secara realtime dari memori
    total_kmr = len(st.session_state.kamar_data)
    isi = sum(1 for d in st.session_state.kamar_data.values() if d["status"] == "🟥 Terisi")
    book = sum(1 for d in st.session_state.kamar_data.values() if d["status"] == "🟨 Booking")
    kosong = total_kmr - isi - book
    
    # Render tampilan info angka kotak-kotak di atas dashboard
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Kamar Kosong Ready 🟩", kosong)
    c2.metric("Kamar Aktif Terisi 🟥", isi)
    c3.metric("Total Data Transaksi", len(st.session_state.reservasi_log))
    c4.metric("Antrean Dapur 🍽️", len(st.session_state.makanan_log))
    
    st.markdown("---")
    st.subheader("📢 Promo Event Hari Ini")
    st.info("Info kupon aktif: Ketik kode **DENARADEAL** pas kasir buat potong harga Rp 100.000!")

# --- MENU 2: INPUT RESERVASI BARU ---
elif pilihan_menu == "📝 Reservasi Baru":
    st.title("📝 Input Reservasi Tamu Baru")
    # Bagi layar jadi kolom kiri (form) dan kolom kanan (rekomendasi & alokasi)
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
        pilihan_bed = st.selectbox("Jenis Bed Kasur", ["Single Bed", "Double Bed", "Twin Bed"])
        jml_tamu = st.number_input("Jumlah Orang Menginap", min_value=1, max_value=10, value=1)
        tgl_in = st.date_input("Tanggal Check-In", date.today())
        tgl_out = st.date_input("Tanggal Check-Out", date.today() + pd.Timedelta(days=1))
        pilihan_late = st.selectbox("Request Jam Check-Out", ["Normal Check-Out", "Late Check-Out (+Rp 50.000)"])
        
    with col_kanan:
        # Bagian pengecekan aturan otomatis kelayakan kamar
        st.subheader("🤖 Smart Room Recommendation")
        
        valid_rekomendasi = True
        pesan_saran = ""
        
        # Aturan 1: Cek kapasitas orang untuk tipe kamar standard
        if pilihan_tipe_kamar == "Standard Room" and jml_tamu > 2:
            valid_rekomendasi = False
            pesan_saran = "⚠️ Kapasitas Standard Room maks. 2 orang. Disarankan pindah ke Deluxe/Family."
            
        # Aturan 2: Cek ketersediaan tipe kasur twin bed di kamar standard
        elif pilihan_tipe_kamar == "Standard Room" and pilihan_bed == "Twin Bed":
            valid_rekomendasi = False
            pesan_saran = "⚠️ Slot Twin Bed untuk tipe Standard terbatas saat ini. Disarankan memakai Double Bed atau pilih tipe Deluxe."
            
        # Aturan 3: Cek rombongan besar biar ga sumpek di kamar kecil
        elif jml_tamu > 4 and pilihan_tipe_kamar in ["Standard Room", "Deluxe Room"]:
            valid_rekomendasi = False
            pesan_saran = "💡 Jumlah tamu banyak (>4 orang). Direkomendasikan ganti ke Family atau Suite Room."

        # Munculin status notifikasi hasil filter validasi ke layar
        if not valid_rekomendasi:
            st.warning(pesan_saran)
        else:
            st.success("✨ Pilihan kombinasi tipe kamar, kasur, dan kapasitas tamu sudah sesuai standar manufaktur hotel.")

        st.markdown("---")
        st.subheader("⚙️ Alokasi Kamar Fisik (Auto)")
        
        # Proses looping mencari nomor kamar kosong terendah yang tipenya sesuai request
        kamar_cocok = None
        for no, detail in st.session_state.kamar_data.items():
            if detail["tipe"] == pilihan_tipe_kamar and detail["status"] == "🟩 Tersedia":
                kamar_cocok = no
                break
                
        # Kasih feedback status pencarian nomor kamar otomatisnya
        if kamar_cocok:
            st.success(f"Kamar Terkunci Otomatis: **Nomor {kamar_cocok}** ({st.session_state.kamar_data[kamar_cocok]['view']})")
        else:
            st.error("Kamar tipe ini penuh!")
            kamar_cocok = st.text_input("Ketik Manual Nomor Kamar Cadangan:")
            
        st.markdown("---")
        st.subheader("🎁 Layanan Tambahan")
        addons = []
        if st.checkbox("Sarapan Pagi Buffet (+Rp 50.000)"): addons.append("Breakfast")
        if st.checkbox("Jemputan Bandara (+Rp 150.000)"): addons.append("Airport Pickup")

    # Tombol klik buat nge-lock data form bookingan dan dioper ke kasir
    if st.button("Kunci Pemesanan & Lanjut Bayar ➡️", type="primary"):
        if not nama:
            st.error("Nama tamu wajib diisi!")
        elif not email or "@" not in email:
            st.error("Email tidak valid!")
        elif not kamar_cocok:
            st.error("Nomor kamar tidak ditemukan!")
        elif tgl_out <= tgl_in:
            st.error("Tanggal Check-Out harus lebih besar dari Check-In!")
        else:
            st.session_state.proses_checkout = {
                "nama": nama,
                "hp": hp,
                "email": email,
                "kamar": kamar_cocok,
                "tipe": pilihan_tipe_kamar,
                "bed_type": pilihan_bed,
                "check_in": str(tgl_in),
                "check_out": str(tgl_out),
                "add_ons": addons,
                "late_checkout": pilihan_late
            }
            
            st.success("Data masuk antrean kasir.Silakan klik menu '💳 Kasir & Pembayaran' ")
# --- MENU 3: KATALOG INFO KAMAR ---
elif pilihan_menu == "🏨 Daftar Katalog Kamar":
    st.title("🏨 Katalog Info Kamar")
    # Looping tampilin harga dan deskripsi sewa kamar hotel
    for tipe, harga in TARIF_KAMAR.items():
        with st.expander(f"Kategori: {tipe} — Rp {harga:,} / Malam"):
            st.write("Fasilitas standar: AC, Smart TV, Free Wifi, air mineral, serta daily cleaning service.")

# --- MENU 4: DENAH VISUAL KAMAR PER LANTAI ---
elif pilihan_menu == "🗺️ Room Map Denah":
    st.title("🗺️ Denah Status Blok Kamar")
    
    # Looping rapi membagi blok visual kotak per lantai (Lantai 1-5)
    for lt in range(1, 6):
        st.subheader(f"🏢 Lantai {lt}")
        # Nyaring nomor kamar yang angka depannya sama dengan tingkat lantai
        kamar_lantai = {no: det for no, det in st.session_state.kamar_data.items() if no.startswith(str(lt))}
        
        cols = st.columns(6)
        for idx, (nomor, detail) in enumerate(kamar_lantai.items()):
            with cols[idx % 6]:
                # Warnai kotak sesuai indikator status kamarnya saat ini
                if "Tersedia" in detail["status"]: 
                    st.success(f"**{nomor}**\n🟩 Ready\n*{detail['view']}*")
                elif "Terisi" in detail["status"]: 
                    st.error(f"**{nomor}**\n🟥 Terisi\n*{detail['tipe']}*")
                else: 
                    st.warning(f"**{nomor}**\n🟨 Booked\n*{detail['tipe']}*")
        st.markdown("---")

# --- MENU 5: ROOM SERVICE FOOD ORDER ---
# ==========================================
# SESSION STATE UNTUK MENYIMPAN PILIHAN
# ==========================================
elif pilihan_menu == "🍽️ Room Service (DenaraEats)":
    st.title("🍽️ Room Service Order")

    no_kmr = st.selectbox("Nomor Kamar:", list(st.session_state.kamar_data.keys()))

    if "keranjang" not in st.session_state:
        st.session_state.keranjang = []

    menu_makanan = {
        "Nasi Goreng": 25000,
        "Mie Goreng": 20000,
        "Ayam Bakar": 30000
    }

    pilih = st.selectbox("Pilih Menu", list(menu_makanan.keys()))

    qty = st.number_input(
    "Jumlah",
    min_value=1,
    value=1
    )

    if st.button("Tambah ke Keranjang"):
        st.session_state.keranjang.append({
            "menu": pilih,
            "qty": qty
        })

    st.markdown("### 🛒 Keranjang")
    total = 0
    
    for item in st.session_state.keranjang:
        harga = menu_makanan[item["menu"]]
        subtotal = harga * item["qty"]
        
        st.write(
            f'{item["menu"]} x {item["qty"]} = Rp {subtotal:,}'
        )
        total += subtotal
        
    st.write(f"**Total: Rp {total:,}**")

    if st.button("Kirim Orderan ke Dapur 🍳"):
        if st.session_state.keranjang:
            st.session_state.makanan_log.append({
                "kamar": no_kmr,
                "pesanan": ", ".join(
                    [f"{x['menu']} x{x['qty']}" for x in st.session_state.keranjang]
                ),
                "total": total,
                "status": "Diproses"
            })
            st.session_state.keranjang = []
            st.success("Pesanan dikirim!")
        else:
            st.warning("Keranjang kosong!")

# --- MENU 6: PENCARIAN DATA TAMU ---
elif pilihan_menu == "🔍 Cari Reservasi":
    st.title("🔍 Cari Data Booking Tamu")
    cari = st.text_input("Ketik Nama Tamu atau Nomor Kamar:")
    if cari:
        # Melakukan scan / pencarian manual mencocokan kata kunci di dalam list array
        ketemu = [r for r in st.session_state.reservasi_log if cari.lower() in r["nama"].lower() or cari == r["kamar"]]
        if ketemu: 
            st.table(pd.DataFrame(ketemu)[["id", "nama", "kamar", "tipe", "check_in", "status"]])
        else: 
            st.warning("Data tidak ketemu!")

# --- MENU 7: KENDALI DATA MASTER LOG (CRUD OPERASIONAL) ---
elif pilihan_menu == "📋 Data Master Log":
    st.title("📋 Log Kendali Master Data")
    if st.session_state.reservasi_log:
        df_log = pd.DataFrame(st.session_state.reservasi_log)
        st.dataframe(df_log[["id", "nama", "kamar", "tipe", "check_in", "check_out", "status"]], use_container_width=True)
        
        st.markdown("---")
        st.subheader("Ubah Status Tamu")
        id_target = st.selectbox("Pilih ID Invoice:", df_log["id"].tolist())
        # Nyari posisi baris index data di dalam array list berdasarkan ID nota invoice
        idx = next((i for i, item in enumerate(st.session_state.reservasi_log) if item["id"] == id_target), None)
        
        b1, b2 = st.columns(2)
        if b1.button("Set CHECK-IN 🟥") and idx is not None:
            # Ubah log reservasi jadi check-in dan ubah warna fisik kamar jadi merah terisi
            st.session_state.reservasi_log[idx]["status"] = "Check-In"
            st.session_state.kamar_data[st.session_state.reservasi_log[idx]["kamar"]]["status"] = "🟥 Terisi"
            st.rerun()
            
        if b2.button("Set CHECK-OUT 🟩") and idx is not None:
            # Ubah log reservasi jadi check-out dan balikkan warna fisik kamar jadi hijau ready kosong
            st.session_state.reservasi_log[idx]["status"] = "Check-Out"
            st.session_state.kamar_data[st.session_state.reservasi_log[idx]["kamar"]]["status"] = "🟩 Tersedia"
            st.rerun()

# --- MENU 8: BILLING STRUK & HITUNGAN KASIR ---
elif pilihan_menu == "💳 Kasir & Pembayaran":
    st.title("💳 Billing Kasir Pembayaran")
    # Cek ketersediaan antrean form booking
    if "proses_checkout" not in st.session_state:
        st.info("Antrean kasir kosong. Silakan isi dulu form di menu '📝 Reservasi Baru'.")
    else:
        dt = st.session_state.proses_checkout
        # Ambil objek datetime buat kalkulasi jumlah selisih hari menginap
        in_dt = datetime.strptime(dt["check_in"], "%Y-%m-%d")
        out_dt = datetime.strptime(dt["check_out"], "%Y-%m-%d")
        malam = max(1, (out_dt - in_dt).days)

        #untuk memilih promo
        promo = st.session_state.get(
            "promo_aktif",
            "Belum ada promo"
        )
        
        st.info(f"Promo aktif saat ini: {promo}")
        
        # Hitung kalkulasi perkalian tarif total biaya rincian
        harga_pokok = TARIF_KAMAR.get(dt["tipe"], 300000) * malam
        biaya_late = 50000 if "Late" in dt["late_checkout"] else 0
        biaya_addon = 0
        for addon in dt["add_ons"]:
            if addon == "Breakfast":
                biaya_addon += 50000
            elif addon == "Airport Pickup":
                biaya_addon += 150000
        
        subtotal = harga_pokok + biaya_late + biaya_addon
        # =========================
        # PROMO (FIX)
        # =========================
        diskon = 0
        promo = st.session_state.get("promo_aktif", None)
        
        if promo == "DENARADEAL":
            diskon = 100000
        elif promo == "SMART10":
            diskon = subtotal * 0.1
        
        # =========================
        # TOTAL
        # =========================
        ppn = subtotal * 0.11
        total_tagihan = subtotal + ppn - diskon
      
       
        poin = int(total_tagihan / 10000) # Kasih bonus loyalty reward poin per kelipatan transaksi 10 ribu
        
        # Cetak tampilan teks nota kuitansi manual
        st.code(f"""
        ================================================
                      DENARA HOTEL SYSTEM               
                        E-RECEIPT STRUK                 
        ================================================
        Nama Tamu       : {dt['nama']}
        Kamar           : No. {dt['kamar']} ({dt['tipe']})
        Durasi          : {malam} Malam
        ------------------------------------------------
        Biaya Kamar     : Rp {harga_pokok:,}
        Biaya Addons    : Rp {biaya_late + biaya_addon:,}
        PPN 11%         : Rp {ppn:,}
        Diskon Voucher  : -Rp {diskon:,} 
        Promo           : {promo}
        ------------------------------------------------
        TOTAL BAYAR     : Rp {total_tagihan:,}
        Bonus Poin      : +{poin} DenaraPoints
        ================================================
        """, language="text")
        
        cara_bayar = st.selectbox(
            "Pilih Metode Bank Transaksi:",
            ["BCA Transfer Direct", "Mandiri Virtual Account", "DenaraPay"]
        )

        status_bayar = st.selectbox(
            "Status Pembayaran",
            ["PAID (Lunas)", "DP 30%"]
        )

        if st.button("Finalisasi Transaksi & Cetak 📑", type="primary"):

            id_invoice = f"INV{datetime.now().strftime('%Y%m%d%H%M%S')}"

            st.session_state.reservasi_log.append({
                "id": id_invoice,
                "nama": dt["nama"],
                "hp": dt["hp"],
                "email": dt["email"],
                "kamar": dt["kamar"],
                "tipe": dt["tipe"],
                "bed_type": dt["bed_type"],
                "check_in": dt["check_in"],
                "check_out": dt["check_out"],
                "status": "Booking",
                "total_biaya": total_tagihan,
                "status_bayar": status_bayar,
                "metode": cara_bayar,
                "add_ons": dt["add_ons"],
                "late_checkout": dt["late_checkout"],
                "poin_earned": poin
            })

            st.session_state.kamar_data[dt["kamar"]]["status"] = "🟨 Booking"

            del st.session_state.proses_checkout

            st.success("Pembayaran berhasil disimpan!")
            st.rerun()

# --- MENU 9: HISTORI TRANSAKSI SELESAI ---
elif pilihan_menu == "📜 Histori Transaksi":
    st.title("📜 Riwayat Cetak Invoice Pembayaran")
    if st.session_state.reservasi_log:
        st.table(pd.DataFrame(st.session_state.reservasi_log)[["id", "nama", "metode", "total_biaya", "status_bayar"]])
# --- MENU 10: REPORT POIN REWARD LOYALITAS VIP ---
elif pilihan_menu == "👤 Poin Loyalitas VIP":
    st.subheader("👤 Program Loyalitas Customer")
    st.info("Poin otomatis didapat dari transaksi pembayaran")
    
    nama = st.text_input("Nama Customer")
    
    poin = 0
    nama_asli = ""

    if nama:
        for data in st.session_state.reservasi_log:
            if data["nama"].lower() == nama.lower():
                nama_asli = data["nama"]
                poin += data.get("poin_earned", 0)

        if poin > 0:
            level = "Regular"
            if poin >= 1000:
                level = "Platinum"
            elif poin >= 500:
                level = "Gold"

            st.success(f"Customer : {nama_asli}")
            st.write(f"Total Poin : {poin}")
            st.write(f"Level Member : **{level}**")

            if st.button("Tukar Poin"):
                if poin >= 100:
                    st.success("🎁 Poin berhasil ditukar dengan voucher!")
                else:
                    st.warning("⚠️ Poin belum cukup")

        else:
            st.warning("Customer tidak ditemukan")

# --- MENU 11: INFO KODE PROMO AKTIF ---
elif pilihan_menu == "🏷️ Info Voucher Promo":
    st.title("🏷️ Kode Promo Aktif")
    st.markdown("---")

    st.success("Pilih promo yang ingin digunakan")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎟️ DENARADEAL"):
            st.session_state.promo_aktif = "DENARADEAL"
            st.success("✅ Promo 100K aktif!")

    with col2:
        if st.button("💳 SMART10"):
            st.session_state.promo_aktif = "SMART10"
            st.success("✅ Diskon 10% aktif!")

    st.markdown("---")
    promo = st.session_state.get(
        "promo_aktif",
        "Belum ada promo"
    )
    st.info(f"Promo aktif saat ini: {promo}")
    
# --- MENU12: DASHBOARD FEEDBACK PELANGGAN ---
elif pilihan_menu == "⭐ Ulasan Kepuasan":
    st.title("📊 Dashboard Feedback Pelanggan")

    # Jika belum ada data
    if not st.session_state.ulasan_log:
        st.info("Belum ada data ulasan pelanggan.")
    else:
        data = st.session_state.ulasan_log

        # ==========================================
        # METRIC RINGKASAN
        # ==========================================
        total_ulasan = len(data)
        rata_rating = sum([u["rating"] for u in data]) / total_ulasan
        rating_tertinggi = max([u["rating"] for u in data])
        rating_terendah = min([u["rating"] for u in data])

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Ulasan", total_ulasan)
        col2.metric("Rata-rata Rating", f"{rata_rating:.2f} ⭐")
        col3.metric("Tertinggi", f"{rating_tertinggi} ⭐")
        col4.metric("Terendah", f"{rating_terendah} ⭐")

        st.markdown("---")

        # ==========================================
        # DISTRIBUSI RATING (GRAFIK)
        # ==========================================
        import pandas as pd

        df = pd.DataFrame(data)
        rating_count = df["rating"].value_counts().sort_index()

        st.subheader("📈 Distribusi Rating")
        st.bar_chart(rating_count)

        st.markdown("---")

        # ==========================================
        # ULASAN TERBARU
        # ==========================================
        st.subheader("📝 Ulasan Terbaru")

        for r in reversed(data[-5:]):  # tampilkan 5 terbaru
            st.markdown(f"""
            <div style="background:#1E293B; padding:10px; border-radius:10px; margin-bottom:10px;">
                <b>{r['nama']}</b> — {'⭐'*r['rating']} <br>
                <small>{r['tanggal']}</small><br>
                <i>"{r['komentar']}"</i>
            </div>
            """, unsafe_allow_html=True)

# --- MENU 13: GRAFIK FINANSIAL OMSET ---
elif pilihan_menu == "📊 Analisis Keuangan":
    st.title("📊 Grafik Omset Finansial")
    if st.session_state.reservasi_log:
        df_an = pd.DataFrame(st.session_state.reservasi_log)
        total_omset = df_an["total_biaya"].sum()
        st.metric("Total Omset Masuk RAM", f"Rp {total_omset:,}")
        st.metric("Target Omset Estimasi Next Month (+20%)", f"Rp {int(total_omset * 1.20):,}")
        # Gambar grafik batang pendapatan dari pembagian kategori tipe sewaan kamar
        st.bar_chart(df_an.groupby("tipe")["total_biaya"].sum())

# --- MENU 14: FAQ PUSAT BANTUAN ---
elif pilihan_menu == "🛟 Pusat Bantuan":
    st.title("🛟 FAQ Layanan")
    with st.expander("Bagaimana cara cancel status kamar?"):
        st.write("Akses menu '📋 Data Master Log', pilih ID Invoice target, lalu lakukan update perubahan status check-out.")
    with st.expander("Apakah data hilang kalau browser ditutup?"):
        st.write("Iya, karena program ini murni berjalan di memori lokal runtime RAM web (session state) tanpa database eksternal.") . 
