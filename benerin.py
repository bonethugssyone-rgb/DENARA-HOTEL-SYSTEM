import streamlit as st
import pandas as pd
from datetime import datetime, date 

st.set_page_config(page_title="Denara Hotel System", layout="wide", page_icon="🏨")

# ==========================================
# STYLE & CSS (SOFT PINK PREMIUM)
# ==========================================
st.markdown("""
<style>
    .main { background-color: #FFF6F9; }
    section[data-testid="stSidebar"] { background-color: #FFE3EC; }
    .card { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0px 4px 15px rgba(0,0,0,0.05); margin-bottom: 15px; }
    .title { font-size: 28px; font-weight: bold; color: #E91E63; }
    .promo { background-color: #E3F0FF; padding: 15px; border-radius: 12px; }
    .stButton>button { background-color: #FF4D8D; color: white; border-radius: 10px; }
    .review { background-color: #FFF; padding: 12px; border-radius: 12px; margin-bottom: 10px; border: 1px solid #eee; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# INISIALISASI DATA MASTER & SESSION STATE
# ==========================================
TARIF_KAMAR = {"Standard Room": 650000, "Superior Room": 1000000, "Deluxe Room": 5000000, "Suite Room": 9500000}

if "kamar_data" not in st.session_state:
    st.session_state.kamar_data = [
        {"No Kamar": "101", "Tipe Kamar": "Standard Room", "Harga": 650000, "Status": "🟩 Tersedia"},
        {"No Kamar": "102", "Tipe Kamar": "Standard Room", "Harga": 650000, "Status": "🟩 Tersedia"},
        {"No Kamar": "103", "Tipe Kamar": "Standard Room", "Harga": 650000, "Status": "🟩 Tersedia"},
        {"No Kamar": "106", "Tipe Kamar": "Superior Room", "Harga": 1000000, "Status": "🟩 Tersedia"},
        {"No Kamar": "201", "Tipe Kamar": "Superior Room", "Harga": 1000000, "Status": "🟩 Tersedia"},
        {"No Kamar": "204", "Tipe Kamar": "Deluxe Room", "Harga": 5000000, "Status": "🟩 Tersedia"},
        {"No Kamar": "301", "Tipe Kamar": "Deluxe Room", "Harga": 5000000, "Status": "🟩 Tersedia"},
        {"No Kamar": "304", "Tipe Kamar": "Suite Room", "Harga": 9500000, "Status": "🟩 Tersedia"},
        {"No Kamar": "401", "Tipe Kamar": "Suite Room", "Harga": 9500000, "Status": "🟩 Tersedia"},
        {"No Kamar": "501", "Tipe Kamar": "Deluxe Room", "Harga": 5000000, "Status": "🟩 Tersedia"},
    ] # Diringkas sampelnya agar kode tidak terlalu panjang, Anda bisa menambahkannya kembali

if "reservasi_log" not in st.session_state: st.session_state.reservasi_log = []
if "histori_transaksi" not in st.session_state: st.session_state.histori_transaksi = []
if "log_pembatalan" not in st.session_state: st.session_state.log_pembatalan = []

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("🏨 Denara Hotel")
menu_utama = st.sidebar.radio("Navigasi Utama", ["🏠 Dashboard", "🏨 Manajemen Kamar", "💳 Transaksi"])

if menu_utama == "🏠 Dashboard":
    pilihan_menu = "🏠 Dashboard"
elif menu_utama == "🏨 Manajemen Kamar":
    pilihan_menu = st.sidebar.radio("Sub-Menu Kamar", ["📝 Reservasi Baru", "🏨 Katalog Kamar", "🗺️ Denah Kamar"])
elif menu_utama == "💳 Transaksi":
    pilihan_menu = st.sidebar.radio("Sub-Menu Transaksi", ["💳 Pembayaran", "🔍 Cari & Data Reservasi", "📜 Histori & Pembatalan"])

# ==========================================
# LOGIKA OPERASIONAL PER MENU
# ==========================================

# --- 1. DASHBOARD ---
if pilihan_menu == "🏠 Dashboard":
    st.markdown('<div class="title">🏠 Dashboard Sistem Hotel</div>', unsafe_allow_html=True)
    
    # Statistik Singkat Berbasis Array Traversal
    kamar_tersedia = len([k for k in st.session_state.kamar_data if k["Status"] == "🟩 Tersedia"])
    total_rsv = len(st.session_state.reservasi_log)
    
    c1, c2 = st.columns(2)
    c1.metric("Kamar Tersedia saat Ini", f"{kamar_tersedia} Kamar")
    c2.metric("Total Aktif Reservasi", f"{total_rsv} Transaksi")
    
    st.markdown("""
    <div class="promo">
    <h4>📢 Kupon Aktif Hari Ini</h4>
    <p>Gunakan <b>DENARADEAL</b> (Potongan Rp 100.000) atau <b>DISC10%</b> (Diskon 10%) saat pembayaran.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h3>👑 Tipe Terpopuler</h3>', unsafe_allow_html=True)
        for name, progress in [("Deluxe Room", 0.9), ("Superior Room", 0.7), ("Suite Room", 0.5)]:
            st.write(f"**{name}**")
            st.progress(progress)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="card"><h3>⭐ Review Terbaru</h3>', unsafe_allow_html=True)
        st.markdown('<div class="review"><b>Andi P.</b> ⭐ 5.0<br><small>Pelayanan mantap dan bersih!</small></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 2. RESERVASI BARU ---
elif pilihan_menu == "📝 Reservasi Baru":
    st.title("📝 Form Reservasi Kamar Baru")
    col_kiri, col_kanan = st.columns([1.5, 1])

    with col_kiri:
        st.subheader("Biodata Tamu")
        nama = st.text_input("Nama Lengkap")
        hp = st.text_input("No HP / WhatsApp")
        email = st.text_input("Email Tamu")
        pilihan_tipe_kamar = st.selectbox("Pipe Kamar", list(TARIF_KAMAR.keys()))
        jml_tamu = st.number_input("Jumlah Orang", min_value=1, max_value=10, value=1)
        tgl_in = st.date_input("Tanggal Check-In", date.today())
        tgl_out = st.date_input("Tanggal Check-Out", date.today() + pd.Timedelta(days=1))
        pilihan_late = st.selectbox("Opsi Check-Out", ["Normal Check-Out", "Late Check-Out (+Rp 50.000)"])

    with col_kanan:
        st.subheader("🤖 Smart Recommendation & Alokasi")
        
        # Validasi Kapasitas Singkat
        rekomendasi = "Standard Room" if jml_tamu <= 2 else ("Superior/Deluxe" if jml_tamu <= 4 else "Suite Room")
        st.info(f"💡 Saran Sistem untuk {jml_tamu} orang: **{rekomendasi}**")
        
        # Cari Kamar Kosong Berdasarkan Tipe (Searching & Traversal Array)
        kamar_cocok = next((k for k in st.session_state.kamar_data if k["Tipe Kamar"] == pilihan_tipe_kamar and k["Status"] == "🟩 Tersedia"), None)
        
        if kamar_cocok:
            st.success(f"✅ Kamar Tersedia: **No. {kamar_cocok['No Kamar']}**")
        else:
            st.error("❌ Kamar tipe ini sudah penuh!")

        st.markdown("---")
        st.subheader("🎁 Layanan Tambahan")
        addons = []
        if st.checkbox("Sarapan Buffet (+Rp 50.000)"): addons.append("Breakfast")
        if st.checkbox("Jemputan Bandara (+Rp 150.000)"): addons.append("Airport Pickup")

        if st.button("Kunci Pemesanan & Lanjut ke Kasir ➡️", type="primary"):
            if not nama or not kamar_cocok or tgl_out <= tgl_in:
                st.error("Mohon periksa kembali kelengkapan data form dan ketersediaan kamar!")
            else:
                st.session_state.proses_checkout = {
                    "id_invoice": f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "nama": nama, "hp": hp, "email": email, "kamar": kamar_cocok,
                    "tipe": pilihan_tipe_kamar, "check_in": str(tgl_in), "check_out": str(tgl_out),
                    "add_on": addons, "late_checkout": pilihan_late
                }
                st.success("Data berhasil dikunci! Silahkan buka menu 💳 Pembayaran untuk cetak struk.")

# --- 3. KATALOG KAMAR ---
elif pilihan_menu == "🏨 Katalog Kamar":
    st.title("🏨 Katalog & Fasilitas Kamar")
    for tipe, harga in TARIF_KAMAR.items():
        with st.expander(f"Kategori: {tipe} — Rp {harga:,} / Malam"):
            st.write(f"Fasilitas premium untuk tipe {tipe} mencakup Smart TV, Wi-Fi 5G, Kamar Mandi Dalam, AC, dan Breakfast.")

# --- 4. DENAH KAMAR ---
elif pilihan_menu == "🗺️ Denah Kamar":
    st.title("🗺️ Peta Visual Denah Kamar")
    for lt in range(1, 6):
        st.subheader(f"🏢 Lantai {lt}")
        kamar_lantai = [k for k in st.session_state.kamar_data if k["No Kamar"].startswith(str(lt))]
        cols = st.columns(6)
        for idx, detail in enumerate(kamar_lantai):
            with cols[idx % 6]:
                if detail["Status"] == "🟩 Tersedia": st.success(f"🚪 {detail['No Kamar']}")
                elif detail["Status"] == "🟨 Direservasi": st.warning(f"🟨 {detail['No Kamar']}")
                else: st.error(f"🟥 {detail['No Kamar']}")

# --- 5. PEMBAYARAN KASIR ---
elif pilihan_menu == "💳 Pembayaran":
    st.title("💳 Billing Kasir & Pembayaran")
    if "proses_checkout" not in st.session_state:
        st.warning("Tidak ada antrian data reservasi yang perlu dibayar.")
        st.stop()

    dt = st.session_state.proses_checkout
    malam = max(1, (datetime.strptime(dt["check_out"], "%Y-%m-%d") - datetime.strptime(dt["check_in"], "%Y-%m-%d")).days)
    
    harga_pokok = TARIF_KAMAR.get(dt["tipe"], 0) * malam
    biaya_late = 50000 if "Late" in dt["late_checkout"] else 0
    biaya_addon = (50000 if "Breakfast" in dt["add_on"] else 0) + (150000 if "Airport Pickup" in dt["add_on"] else 0)
    subtotal = harga_pokok + biaya_late + biaya_addon

    # Fitur Voucher
    st.subheader("🎟️ Pilihan Voucher Promo")
    v_opsi = st.radio("Pilih Voucher:", ["Tanpa Voucher", "DENARADEAL (Potongan Rp100k)", "DISC10% (Potongan 10%)"])
    diskon = 100000 if v_opsi == "DENARADEAL (Potongan Rp100k)" else (subtotal * 0.1 if v_opsi == "DISC10% (Potongan 10%)" else 0)
    
    total_tagihan = (subtotal + (subtotal * 0.11)) - diskon
    poin = int(total_tagihan / 10000)

    st.code(f"""
    ================================================
                  DENARA HOTEL RECEIPT Struk        
    ================================================
    ID Invoice   : {dt['id_invoice']}
    Nama Tamu    : {dt['nama']}
    Nomor Kamar  : No. {dt['kamar']['No Kamar']} ({dt['tipe']})
    Durasi       : {malam} Malam ({dt['check_in']} s/d {dt['check_out']})
    ------------------------------------------------
    Biaya Kamar  : Rp {harga_pokok:,}
    Biaya Extra  : Rp {biaya_late + biaya_addon:,}
    PPN (11%)    : Rp {int(subtotal * 0.11):,}
    Pot. Diskon  : -Rp {int(diskon):,}
    ------------------------------------------------
    TOTAL BAYAR  : Rp {int(total_tagihan):,}
    Reward Poin  : +{poin} Poin
    ================================================
    """, language="text")

    metode = st.selectbox("Metode Pembayaran", ["BCA Transfer", "E-Wallet Gopay/Dana", "Mandiri VA"])
    status_bayar = st.selectbox("Status Tagihan", ["PAID (Lunas)", "DP 30%"])

    if st.button("Finalisasi Transaksi & Cetak 📑", type="primary"):
        # Insert Data Baru ke Array Log Dinamis
        st.session_state.reservasi_log.append({
            "id": dt["id_invoice"], "nama": dt["nama"], "hp": dt["hp"], "email": dt["email"],
            "kamar": dt["kamar"]["No Kamar"], "tipe": dt["tipe"], "check_in": dt["check_in"],
            "check_out": dt["check_out"], "total_biaya": total_tagihan, "status_bayar": status_bayar,
            "metode": metode, "status": "🟨 Direservasi"
        })
        
        # Update Status Kamar di Data Master (Array Update)
        for kamar in st.session_state.kamar_data:
            if kamar["No Kamar"] == dt["kamar"]["No Kamar"]:
                kamar["Status"] = "🟨 Direservasi"

        del st.session_state.proses_checkout
        st.success("Transaksi Sukses dimasukkan ke Log Sistem!")
        st.rerun()

# --- 6. CARI & DATA RESERVASI ---
elif pilihan_menu == "🔍 Cari & Data Reservasi":
    st.title("📋 Database Log Reservasi Aktif")
    data = st.session_state.reservasi_log

    if not data:
        st.warning("Belum ada data reservasi aktif dalam sistem.")
        st.stop()

    keyword = st.text_input("🔍 Pencarian Cepat (Masukkan Nama / ID Invoice / No Kamar):")
    hasil = [d for d in data if keyword.lower() in d["nama"].lower() or keyword.lower() in d["id"].lower() or keyword.lower() in d["kamar"].lower()] if keyword else data

    st.subheader("Tabel Data Reservasi")
    st.dataframe(pd.DataFrame(hasil), use_container_width=True)

    for i, d in enumerate(hasil):
        with st.container():
            st.markdown(f'<div class="card"><h4>🧾 Invoice: {d["id"]}</h4>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            col1.write(f"👤 **Nama:** {d['nama']} | 📱 **HP:** {d['hp']}<br>🚪 **Kamar:** {d['kamar']} ({d['tipe']})", unsafe_allow_html=True)
            col2.write(f"📅 **Periode:** {d['check_in']} s/d {d['check_out']}<br>💰 **Total:** Rp {int(d['total_biaya']):,} ({d['status_bayar']})", unsafe_allow_html=True)
            
            if st.button(f"🗑️ Selesaikan / Hapus Log {d['id']}", key=f"del_{i}"):
                # Simpan ke Histori Permanen Sebelum Dihapus
                st.session_state.histori_transaksi.append({
                    "id": d["id"], "nama": d["nama"], "kamar": d["kamar"], "tipe": d["tipe"],
                    "total": d["total_biaya"], "metode": d["metode"], "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"), "keterangan": "Selesai"
                })
                # Ubah Kamar kembali Menjadi Tersedia
                for kamar in st.session_state.kamar_data:
                    if kamar["No Kamar"] == d["kamar"]: kamar["Status"] = "🟩 Tersedia"
                st.session_state.reservasi_log.remove(d)
                st.success("Transaksi diselesaikan dan diarsipkan.")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# --- 7. HISTORI & PEMBATALAN ---
elif pilihan_menu == "📜 Histori & Pembatalan":
    st.title("📜 Histori Arsip & Pembatalan Transaksi")
    
    t1, t2 = st.tabs(["📜 Histori Selesai", "❌ Ajukan Pembatalan (Cancel)"])
    
    with t1:
        if not st.session_state.histori_transaksi:
            st.info("Arsip histori transaksi kosong.")
        else:
            st.dataframe(pd.DataFrame(st.session_state.histori_transaksi), use_container_width=True)
            
    with t2:
        if not st.session_state.reservasi_log:
            st.warning("Tidak ada transaksi aktif yang bisa dibatalkan.")
        else:
            for idx, rsv in enumerate(st.session_state.reservasi_log):
                st.write(f"🧾 **{rsv['id']}** — {rsv['nama']} (Kamar {rsv['kamar']})")
                if st.button(f"🔴 Batalkan Transaksi {rsv['id']}", key=f"btn_btl_{idx}"):
                    # Update status kamar master
                    for k in st.session_state.kamar_data:
                        if k["No Kamar"] == rsv["kamar"]: k["Status"] = "🟩 Tersedia"
                    
                    # Tambah ke log batal
                    st.session_state.log_pembatalan.append({
                        "id": rsv["id"], "nama": rsv["nama"], "kamar": rsv["kamar"], "tanggal_batal": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.session_state.reservasi_log.remove(rsv)
                    st.success(f"Invoice {rsv['id']} Berhasil Dibatalkan!")
                    st.rerun()
            
            if st.session_state.log_pembatalan:
                st.subheader("📋 Log Riwayat Pembatalan")
                st.dataframe(pd.DataFrame(st.session_state.log_pembatalan), use_container_width=True)