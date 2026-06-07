import streamlit as st
import pandas as pd
from datetime import datetime, date 

st.set_page_config(page_title="Denara Hotel", layout="wide", page_icon="🏨")

# ==========================================
# STYLING BIAR TAMPILANNYA CAKEP (PINK EMANG GA PERNAH SALAH)
# ==========================================
st.markdown("""
<style>
    .main { background-color: #FFF6F9; }
    section[data-testid="stSidebar"] { background-color: #FFE3EC; }
    .card { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0px 4px 15px rgba(0,0,0,0.05); margin-bottom: 15px; }
    .title { font-size: 28px; font-weight: bold; color: #E91E63; }
    .promo { background-color: #E3F0FF; padding: 15px; border-radius: 12px; margin-bottom: 15px; }
    .stButton>button { background-color: #FF4D8D; color: white; border-radius: 10px; width: 100%; }
    .review-box { background-color: #FFF; padding: 12px; border-radius: 12px; margin-bottom: 10px; border: 1px solid #eee; }
    .facility-tag { background-color: #F0F2F5; padding: 4px 10px; border-radius: 20px; font-size: 12px; margin-right: 5px; display: inline-block; margin-bottom: 5px;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA MASTER & FASILITAS KAMAR (BED TYPE NYA UDAH DIHAPUS YAA)
# ==========================================
TARIF_KAMAR = {
    "Standard Room": 650000, 
    "Superior Room": 1000000, 
    "Deluxe Room": 5000000, 
    "Suite Room": 9500000
}

# Di sini tipe bed/kasur udah ilang, diganti fasilitas pelengkap lainnya
FASILITAS_KAMAR = {
    "Standard Room": ["Free Wi-Fi", "AC Dingin", "Smart TV 32\"", "Shower", "Air Mineral Gratis"],
    "Superior Room": ["Free Wi-Fi", "AC Dingin", "Smart TV 43\"", "Water Heater", "Kulkas Mini", "Coffee & Tea Maker"],
    "Deluxe Room": ["Free Wi-Fi", "AC Dingin", "Smart TV 55\"", "Bathtub Mewah", "Mini Bar", "Safety Box", "Balkon Nyantai"],
    "Suite Room": ["Free Wi-Fi", "AC Dingin", "Smart TV 65\"", "Jacuzzi Pribadi", "Premium Mini Bar", "Ruang Tamu Terpisah", "Butler Service 24 Jam", "Kolam Renang Pribadi"]
}

MENU_MAKANAN = {
    "Nasi Goreng Kampung": 35000, 
    "Mie Goreng Cabe Ijo": 30000, 
    "Ayam Goreng Serundeng": 40000, 
    "Es Teh Manis Premium": 12000, 
    "Kopi Susu Aren": 20000
}

# Tempat nyimpen status data kamar lantai 1 sampe 5
if "kamar_data" not in st.session_state:
    st.session_state.kamar_data = [
        # LANTAI 1
        {"No Kamar": "101", "Tipe Kamar": "Standard Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "102", "Tipe Kamar": "Standard Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "103", "Tipe Kamar": "Standard Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "104", "Tipe Kamar": "Standard Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "105", "Tipe Kamar": "Standard Room", "Status": "🟩 Tersedia"},
        # LANTAI 2
        {"No Kamar": "201", "Tipe Kamar": "Superior Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "202", "Tipe Kamar": "Superior Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "203", "Tipe Kamar": "Superior Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "204", "Tipe Kamar": "Deluxe Room", "Status": "🟩 Tersedia"},
        # LANTAI 3
        {"No Kamar": "301", "Tipe Kamar": "Deluxe Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "302", "Tipe Kamar": "Deluxe Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "303", "Tipe Kamar": "Suite Room", "Status": "🟩 Tersedia"},
        # LANTAI 4
        {"No Kamar": "401", "Tipe Kamar": "Suite Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "402", "Tipe Kamar": "Suite Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "403", "Tipe Kamar": "Deluxe Room", "Status": "🟩 Tersedia"},
        # LANTAI 5
        {"No Kamar": "501", "Tipe Kamar": "Deluxe Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "502", "Tipe Kamar": "Suite Room", "Status": "🟩 Tersedia"},
        {"No Kamar": "503", "Tipe Kamar": "Suite Room", "Status": "🟩 Tersedia"},
    ]

# Wadah array dinamis buat nampung log aktivitas hotel
if "reservasi_log" not in st.session_state: st.session_state.reservasi_log = []
if "histori_transaksi" not in st.session_state: st.session_state.histori_transaksi = []
if "log_pembatalan" not in st.session_state: st.session_state.log_pembatalan = []
if "makanan_log" not in st.session_state: st.session_state.makanan_log = []
if "voucher_terpilih" not in st.session_state: st.session_state.voucher_terpilih = "Tanpa Voucher"
if "ulasan_log" not in st.session_state: 
    st.session_state.ulasan_log = [
        {"nama": "Andi Pratama", "rating": 5, "komentar": "Keren bgt, jacuzzi di lantai 5 mantap betul!"}
    ]

# ==========================================
# NAVIGASI MENU UTAMA & SUB-MENU DI SIDEBAR
# ==========================================
st.sidebar.title("🏨 Denara Hotel")
menu_utama = st.sidebar.radio("Menu Utama", [
    "🏠 Dashboard", 
    "🏨 Manajemen Kamar", 
    "💳 Transaksi", 
    "🍽️ Room Service", 
    "⭐ Penilaian Hotel", 
    "🛟 Bantuan"
])

if menu_utama == "🏠 Dashboard": pilihan_menu = "🏠 Dashboard"
elif menu_utama == "🏨 Manajemen Kamar":
    pilihan_menu = st.sidebar.radio("Sub-Menu Kamar", ["📝 Reservasi Baru", "🏨 Katalog Kamar", "🗺️ Denah Kamar"])
elif menu_utama == "💳 Transaksi":
    pilihan_menu = st.sidebar.radio("Sub-Menu Transaksi", ["💳 Pembayaran", "🔍 Cari & Data Reservasi", "📜 Histori & Pembatalan"])
elif menu_utama == "🍽️ Room Service":
    pilihan_menu = st.sidebar.radio("Sub-Menu Room Service", ["🍽️ Pesan Makanan", "💳 Bayar Room Service"])
elif menu_utama == "⭐ Penilaian Hotel": pilihan_menu = "⭐ Ulasan Kepuasan"
elif menu_utama == "🛟 Bantuan":
    pilihan_menu = st.sidebar.radio("Sub-Menu Bantuan", ["❓ Pusat Bantuan", "📞 Kontak Layanan Service"])

# ==========================================
# LOGIKA PROSES TIAP MENU
# ==========================================

# --- 1. DASHBOARD ---
if pilihan_menu == "🏠 Dashboard":
    st.markdown('<div class="title">🏠 Selamat Datang di Denara Hotel</div>', unsafe_allow_html=True)
    kamar_kosong = len([k for k in st.session_state.kamar_data if k["Status"] == "🟩 Tersedia"])
    st.metric("Kamar Kosong Yang Siap Dipesan (Lantai 1-5)", f"{kamar_kosong} Kamar")
    
    st.markdown("""
    <div class="promo">
    <h4>📢 Info Promo Buat Kamu</h4>
    <p>Jangan lupa pake tombol voucher pas bayar ntar biar dapet potongan harga gede!</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h3>👑 Kamar Paling Laris</h3>', unsafe_allow_html=True)
        st.write("**Suite Room (Lantai 5 VIP)**")
        st.caption("Fasilitas Andalan: Jacuzzi Pribadi & Kolam Renang Sendiri")
        st.progress(0.95)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><h3>⭐ Kata Tamu Yang Udah Nginep</h3>', unsafe_allow_html=True)
        for u in st.session_state.ulasan_log[-2:]:
            st.markdown(f'<div class="review-box"><b>{u["nama"]}</b> (⭐ {u["rating"]})<br><small>"{u["komentar"]}"</small></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 2. RESERVASI BARU ---
elif pilihan_menu == "📝 Reservasi Baru":
    st.title("📝 Form Reservasi Hotel (Gak Pake Ribet)")
    col_kiri, col_kanan = st.columns([1.5, 1])

    with col_kiri:
        st.subheader("Isi Data Diri Dulu Yuk")
        nama = st.text_input("Nama Lengkap (Sesuai KTP ya)")
        hp = st.text_input("Nomor WA Sing Aktif")
        email = st.text_input("Email Kamu")
        pilihan_tipe = st.selectbox("Mau Kamar Tipe Apa?", list(TARIF_KAMAR.keys()))
        
        # Nampilin daftar fasilitas kamar secara real-time pas diklik
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
        
        # Nyari kamar kosong di array master pake trik looping traversal
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
                # Ngiket data sementara ke session state biar bisa dibayar ntar
                st.session_state.proses_checkout = {
                    "id_invoice": f"RSV-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "nama": nama, "hp": hp, "email": email, "kamar": kamar_cocok,
                    "tipe": pilihan_tipe, "check_in": str(tgl_in), "check_out": str(tgl_out),
                    "add_on": addons, "late_checkout": pilihan_late
                }
                st.session_state.voucher_terpilih = "Tanpa Voucher" # reset voucher biar fair
                st.success("Sip! Data udah kesimpen, gass ke sub-menu 'Pembayaran' buat ngelunasin.")

# --- 3. KATALOG KAMAR ---
elif pilihan_menu == "🏨 Katalog Kamar":
    st.title("🏨 List Spesifikasi & Detail Kamar")
    for tipe, harga in TARIF_KAMAR.items():
        with st.expander(f"✨ {tipe} — Rp {harga:,} / Malam"):
            st.write("#### Fasilitas Kamar:")
            for fas in FASILITAS_KAMAR[tipe]:
                st.markdown(f'<span class="facility-tag">✨ {fas}</span>', unsafe_allow_html=True)

# --- 4. DENAH KAMAR ---
elif pilihan_menu == "🗺️ Denah Kamar":
    st.title("🗺️ Map Letak Kamar Hotel Lantai 1 s/d 5")
    for lt in range(1, 6):
        st.subheader(f"🏢 Lantai {lt}")
        kamar_lantai = [k for k in st.session_state.kamar_data if k["No Kamar"].startswith(str(lt))]
        cols = st.columns(6)
        for idx, detail in enumerate(kamar_lantai):
            with cols[idx % 6]:
                if detail["Status"] == "🟩 Tersedia": 
                    st.success(f"🚪 {detail['No Kamar']}\n({detail['Tipe Kamar'][:4]})")
                else: 
                    st.error(f"🟨 {detail['No Kamar']}\n(Booked)")

# --- 5. PEMBAYARAN RESERVASI (BUTTON VOUCHER TIMBUL) ---
elif pilihan_menu == "💳 Pembayaran":
    st.title("💳 Menu Pembayaran Billing Kamar")
    if "proses_checkout" not in st.session_state:
        st.warning("Belum ada antrian kamar yang mau dibayar nih.")
        st.stop()

    dt = st.session_state.proses_checkout
    malam = max(1, (datetime.strptime(dt["check_out"], "%Y-%m-%d") - datetime.strptime(dt["check_in"], "%Y-%m-%d")).days)
    
    harga_pokok = TARIF_KAMAR.get(dt["tipe"], 0) * malam
    biaya_extra = (50000 if "Late" in dt["late_checkout"] else 0) + (50000 if "Breakfast" in dt["add_on"] else 0) + (150000 if "Airport Pickup" in dt["add_on"] else 0)
    subtotal = harga_pokok + biaya_extra

    # Tombol voucher interaktif yang menonjol pas dipencet
    st.subheader("🎟️ Klik Tombol Di Bawah Buat Pasang Voucher")
    v_col1, v_col2, v_col3 = st.columns(3)
    
    with v_col1:
        is_active = st.session_state.voucher_terpilih == "Tanpa Voucher"
        if st.button("Gak Pake Voucher", key="btn_v1", type="secondary" if not is_active else "primary"):
            st.session_state.voucher_terpilih = "Tanpa Voucher"
            st.rerun()
            
    with v_col2:
        is_active = st.session_state.voucher_terpilih == "DENARADEAL"
        if st.button("🎁 Voucher DENARADEAL (-Rp100k)", key="btn_v2", type="primary" if is_active else "secondary"):
            st.session_state.voucher_terpilih = "DENARADEAL"
            st.rerun()
            
    with v_col3:
        is_active = st.session_state.voucher_terpilih == "DISC10%"
        if st.button("🔥 Voucher DISC10% (Diskon 10%)", key="btn_v3", type="primary" if is_active else "secondary"):
            st.session_state.voucher_terpilih = "DISC10%"
            st.rerun()

    # Logika ngitung diskon dari state voucher yang lagi aktif
    if st.session_state.voucher_terpilih == "DENARADEAL":
        diskon = 100000
    elif st.session_state.voucher_terpilih == "DISC10%":
        diskon = subtotal * 0.1
    else:
        diskon = 0

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

    metode = st.selectbox("Mau Bayar Lewat Mana?", ["Transfer BCA", "Mandiri Virtual Account", "Ovo / Dana / Gopay"])
    status_bayar = st.selectbox("Opsi Bayar", ["PAID (Langsung Lunas)", "DP Dulu 30%"])

    if st.button("Konfirmasi Bayar & Cetak Kunci Kamar ✔️", type="primary"):
        # Masukin data ke array list log utama hotel
        st.session_state.reservasi_log.append({
            "id": dt["id_invoice"], "nama": dt["nama"], "hp": dt["hp"], "email": dt["email"],
            "kamar": dt["kamar"]["No Kamar"], "tipe": dt["tipe"], "check_in": dt["check_in"],
            "check_out": dt["check_out"], "total_biaya": total_tagihan, "status_bayar": status_bayar,
            "metode": metode, "status": "🟨 Direservasi"
        })
        
        # Ngerubah status kamarnya di array biar jadi ke-booking
        for kamar in st.session_state.kamar_data:
            if kamar["No Kamar"] == dt["kamar"]["No Kamar"]:
                kamar["Status"] = "🟨 Direservasi"

        del st.session_state.proses_checkout
        st.success("Pembayaran Berhasil! Kamar udah sah jadi milikmu.")
        st.rerun()

# --- 6. CARI & DATA RESERVASI ---
elif pilihan_menu == "🔍 Cari & Data Reservasi":
    st.title("📋 Data Pencarian Buku Tamu Hotel Aktif")
    data = st.session_state.reservasi_log

    if not data:
        st.warning("Belum ada tamu yang check-in hari ini.")
        st.stop()

    keyword = st.text_input("🔍 Ketik Nama Tamu / ID Booking / No Kamar Buat Nyari:")
    
    # Algoritma searching nyari string yang mirip di dalem array
    hasil = [d for d in data if keyword.lower() in d["nama"].lower() or keyword.lower() in d["id"].lower() or keyword.lower() in d["kamar"].lower()] if keyword else data

    st.subheader("Data Tamu Yang Ketemu")
    st.dataframe(pd.DataFrame(hasil), use_container_width=True)

    for i, d in enumerate(hasil):
        with st.container():
            st.markdown(f'<div class="card"><h4>🧾 Kode Transaksi: {d["id"]}</h4>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            c1.write(f"👤 **Nama:** {d['nama']} | 🚪 **Kamar:** {d['kamar']} ({d['tipe']})<br>📱 **HP:** {d['hp']} | 📧 **Email:** {d['email']}", unsafe_allow_html=True)
            c2.write(f"📅 **Jadwal:** {d['check_in']} s/d {d['check_out']}<br>💰 **Total:** Rp {int(d['total_biaya']):,} — *{d['status_bayar']}*", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# --- 7. HISTORI & PEMBATALAN ---
elif pilihan_menu == "📜 Histori & Pembatalan":
    st.title("📜 Menu Riwayat Selesai & Pembatalan Kamar")
    tab_riwayat, tab_batal = st.tabs(["Arsip Kamar Selesai", "Ajukan Pembatalan Kamar"])
    
    with tab_riwayat:
        if not st.session_state.histori_transaksi:
            st.info("Belum ada history tamu yang checkout.")
        else:
            st.dataframe(pd.DataFrame(st.session_state.histori_transaksi), use_container_width=True)
            
    with tab_batal:
        if not st.session_state.reservasi_log:
            st.info("Gak ada jadwal booking aktif yang bisa dibatalin.")
        else:
            for idx, rsv in enumerate(st.session_state.reservasi_log):
                st.write(f"🔹 **{rsv['id']}** — Tamu: {rsv['nama']} | Kamar: {rsv['kamar']}")
                if st.button(f"Cancel Kamar {rsv['kamar']}", key=f"btl_{idx}"):
                    # Balikin status kamar di master data jadi kosong lagi
                    for k in st.session_state.kamar_data:
                        if k["No Kamar"] == rsv["kamar"]: k["Status"] = "🟩 Tersedia"
                    
                    # Pindahin datanya ke array list pembatalan
                    st.session_state.log_pembatalan.append({
                        "id": rsv["id"], "nama": rsv["nama"], "kamar": rsv["kamar"], "waktu_batal": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.session_state.reservasi_log.remove(rsv)
                    st.success("Sukses dibatalin! Kamar otomatis dilepas biar bisa dipesan orang lain.")
                    st.rerun()
            
            if st.session_state.log_pembatalan:
                st.subheader("📋 Daftar Kamar Yang Pernah Dibatalin")
                st.dataframe(pd.DataFrame(st.session_state.log_pembatalan), use_container_width=True)

# --- 8. ROOM SERVICE: PESAN MAKANAN (AKUMULASI QUANTITY JIKA MENU SAMA) ---
elif pilihan_menu == "🍽️ Pesan Makanan":
    st.title("🍽️ Room Service Kuliner - Kirim Ke Kamar")
    
    no_kmr = st.selectbox("Kamu Nyari Kamar Nomor Berapa?", [k["No Kamar"] for k in st.session_state.kamar_data])
    st.write("### Pilih Menu Makanan Di Bawah:")
    
    total_order = 0
    items_dipesan = []
    
    # Looping buat nampilin list menu makanan tanpa takut datanya ilang pas diinput
    for menu, harga in MENU_MAKANAN.items():
        qty = st.number_input(f"{menu} (Rp {harga:,})", min_value=0, step=1, key=f"food_{menu}")
        if qty > 0:
            total_order += (qty * harga)
            items_dipesan.append({"item": menu, "qty": qty, "subtotal": qty * harga})
            
    st.markdown(f"### Total Belanjaan Kuliner Baru: **Rp {total_order:,}**")
    
    if st.button("Pesan Sekarang & Kirim Ke Dapur 🛒"):
        if total_order > 0:
            # Algoritma nyari tau apakah nomor kamar ini udah pernah mesen makanan tapi belum bayar
            kamar_exist = next((m for m in st.session_state.makanan_log if m["kamar"] == no_kmr and m["status"] == "Belum Bayar"), None)
            
            if kamar_exist:
                # Kalau kamarnya udah ada di antrian dapur, kita akumulasiin aja itemnya
                for item_baru in items_dipesan:
                    # Cari tau menu makanannya udah ada di list pesanan kamar itu apa belum
                    idx_makanan = -1
                    for idx, s in enumerate(kamar_exist["pesanan_detail"]):
                        if s["item"] == item_baru["item"]:
                            idx_makanan = idx
                            break
                    
                    if idx_makanan != -1:
                        # Kalau menunya sama, tambahin qty ama subtotalnya (Gak bikin baris baru)
                        kamar_exist["pesanan_detail"][idx_makanan]["qty"] += item_baru["qty"]
                        kamar_exist["pesanan_detail"][idx_makanan]["subtotal"] += item_baru["subtotal"]
                    else:
                        # Kalau mesen menu yang bener-bener baru, insert aja ke array sub-list nya
                        kamar_exist["pesanan_detail"].append(item_baru)
                
                # Hitung ulang total harga kumulatif semuanya
                kamar_exist["total"] = sum(x["subtotal"] for x in kamar_exist["pesanan_detail"])
                st.success(f"Pesanan tambahan masuk buat Kamar {no_kmr}! Jumlah porsi otomatis nambah.")
            else:
                # Kalau kamar ini bener-bener baru pertama kali mesen makanan
                st.session_state.makanan_log.append({
                    "kamar": no_kmr, 
                    "pesanan_detail": items_dipesan, 
                    "total": total_order, 
                    "status": "Belum Bayar"
                })
                st.success("Pesanan dikirim! Chef kami bakal langsung masak pesananmu.")
        else:
            st.warning("Pilih dulu makanannya, masa mesen angin doang.")

# --- 9. ROOM SERVICE: BAYAR ROOM SERVICE ---
elif pilihan_menu == "💳 Bayar Room Service":
    st.title("💳 Kasir Tagihan Room Service Kuliner")
    antrian_kuliner = [m for m in st.session_state.makanan_log if m["status"] == "Belum Bayar"]
    
    if not antrian_kuliner:
        st.info("Mantap! Semua tagihan makanan udah beres lunas semua.")
    else:
        for idx, order in enumerate(antrian_kuliner):
            with st.container():
                st.markdown(f'<div class="card"><h4>🛎️ Total Bill Makan Kamar: {order["kamar"]}</h4>', unsafe_allow_html=True)
                
                st.write("**Rincian Pesanan Kuliner Yang Diakumulasi:**")
                for item in order["pesanan_detail"]:
                    st.write(f"- {item['item']} sebanyak ({item['qty']} Porsi) — total: Rp {item['subtotal']:,}")
                    
                st.markdown(f"Total Yang Harus Dibayar: **Rp {order['total']:,}**")
                
                if st.button(f"Lunasi Makanan Kamar {order['kamar']}", key=f"pay_food_{idx}"):
                    order["status"] = "Selesai PAID"
                    st.success(f"Tagihan makan Kamar {order['kamar']} sukses dibayar lunas!")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

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
