# ==========================================
# IMPORT
# ==========================================
import streamlit as st
from datetime import datetime

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

# ==========================================
# SIDEBAR MENU
# ==========================================
st.sidebar.title("🏨 Denara Hotel")

menu = st.sidebar.radio("Menu", [
    "🏠 Dashboard",
    "Reservasi Baru",
    "Katalog Kamar",
    "Denah Kamar",
    "Transaksi",
    "Room Service",
    "Voucher",
    "Penilaian",
    "Bantuan"
])

# ==========================================
# DASHBOARD
# ==========================================
if menu == "🏠 Dashboard":

    st.markdown('<div class="title">Dashboard</div>', unsafe_allow_html=True)

    # ================= PROMO =================
    st.markdown("""
    <div class="promo">
    <h4>📢 Promo Event Hari Ini</h4>
    <p>Info kupon aktif: Ketik kode <b>DENARADEAL</b> pas kasir buat potong harga <b>Rp 100.000!</b></p>
    <p>Info kupon aktif: Ketik kode <b>DENARADEAL</b> pas kasir buat potong harga <b>Rp 100.000!</b></p>
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
            ("Family Room", 9),
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

# ==========================================
# FOOTER
# ==========================================
st.write("")
st.markdown("""
<center>© 2025 Denara Hotel❤️</center>
""", unsafe_allow_html=True)

#INISIALISASI DATA (ARRAY)
# semua data menggunakan array
# ==========================================
# INISIALISASI DATA SIMULASI (SESSION STATE)
# ==========================================

# Penampung data master seluruh kamar dari lantai 1 sampai 5 (di RAM)
if "kamar_data" not in st.session_state:
    st.session_state.kamar_data = [
        #LANTAI 1
        {"No Kamar": "101", "Tipe Kamar": "Standard Room", "Harga": "350000", "Status": "🟩 Tersedia"},
        {"No Kamar": "102", "Tipe Kamar": "Standard Room", "Harga": "350000", "Status": "🟩 Tersedia"},
        {"No Kamar": "103", "Tipe Kamar": "Standard Room", "Harga": "350000", "Status": "🟩 Tersedia"},
        {"No Kamar": "104", "Tipe Kamar": "Standard Room", "Harga": "350000", "Status": "🟩 Tersedia"},
        {"No Kamar": "105", "Tipe Kamar": "Standard Room", "Harga": "350000", "Status": "🟩 Tersedia"},
        {"No Kamar": "106", "Tipe Kamar": "Superior Room", "Harga": "420000", "Status": "🟩 Tersedia"},
        #LANTAI 2
        {"No Kamar": "201", "Tipe Kamar": "Superior Room", "Harga": "420000", "Status": "🟩 Tersedia"},
        {"No Kamar": "202", "Tipe Kamar": "Superior Room", "Harga": "420000", "Status": "🟩 Tersedia"},
        {"No Kamar": "203", "Tipe Kamar": "Superior Room", "Harga": "420000", "Status": "🟩 Tersedia"},
        {"No Kamar": "204", "Tipe Kamar": "Deluxe Room", "Harga": "500000", "Status": "🟩 Tersedia"},
        {"No Kamar": "205", "Tipe Kamar": "Deluxe Room", "Harga": "500000", "Status": "🟩 Tersedia"},
        {"No Kamar": "206", "Tipe Kamar": "Deluxe Room", "Harga": "500000", "Status": "🟩 Tersedia"},
        #LANTAI 3
        {"No Kamar": "301", "Tipe Kamar": "Deluxe Room", "Harga": "500000", "Status": "🟩 Tersedia"},
        {"No Kamar": "302", "Tipe Kamar": "Deluxe Room", "Harga": "500000", "Status": "🟩 Tersedia"},
        {"No Kamar": "303", "Tipe Kamar": "Deluxe Room", "Harga": "500000", "Status": "🟩 Tersedia"},
        {"No Kamar": "304", "Tipe Kamar": "Suite Room", "Harga": "1200000", "Status": "🟩 Tersedia"},
        {"No Kamar": "305", "Tipe Kamar": "Suite Room", "Harga": "1200000", "Status": "🟩 Tersedia"},
        #LANTAI 4
        {"No Kamar": "401", "Tipe Kamar": "Suite Room", "Harga": "1200000", "Status": "🟩 Tersedia"},
        {"No Kamar": "402", "Tipe Kamar": "Suite Room", "Harga": "1200000", "Status": "🟩 Tersedia"},
        {"No Kamar": "403", "Tipe Kamar": "Suite Room", "Harga": "1200000", "Status": "🟩 Tersedia"},
        {"No Kamar": "404", "Tipe Kamar": "Deluxe Room", "Harga": "500000", "Status": "🟩 Tersedia"},
        {"No Kamar": "405", "Tipe Kamar": "Superior Room", "Harga": "420000", "Status": "🟩 Tersedia"},
        #LANTAI 5
        {"No Kamar": "501", "Tipe Kamar": "Deluxe Room", "Harga": "500000", "Status": "🟩 Tersedia"},
        {"No Kamar": "502", "Tipe Kamar": "Suite Room", "Harga": "1200000", "Status": "🟩 Tersedia"},
        {"No Kamar": "503", "Tipe Kamar": "Suite Room", "Harga": "1200000", "Status": "🟩 Tersedia"},
    ]

#Array untuk menyimpan riwayat booking hotel
if "reservasi_log" not in st.session_state:
    st.session_state.reservasi_log = []

#Array untuk menyimpan histori 
if "history_log" not in st.session_state:
    st.session_state.history_log = []

#Array untuk antrian pesan makanan pada room service
if "makanan_log" not in st.session_state:
    st.session_state.makanan_log = []

if "voucher_data" not in st.session_state:
    st.session_state.voucher_data = [
        {"kode": "DISC10", "diskon": 10},
        {"kode": "DENARADEAL", "diskon": 10},
    ]

#
