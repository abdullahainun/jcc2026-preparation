# LAB 02: NEEDLE IN A HAYSTACK
### Filter Lanjutan, DNS Tracking, & Ekstraksi File di Wireshark

**Program Pembinaan Tim CTF SMK Maskumambang 1**
Persiapan **Jatim Cybersecurity Competition (JCC) 2026**, kategori SMA/SMK Sederajat
Kelas Sasaran: X (usia 15-16 tahun) | Level: Pemula Lanjutan
Prasyarat: **LAB 01 - The Wire Sniffer** sudah tuntas
Versi Modul: 1.0 | Tanggal: 05 September 2026

***

## DAFTAR ISI

1. [Informasi Modul & Target Capaian](#bagian-1-informasi-modul-target-capaian)
2. [Briefing Misi: Kasus Kebocoran Dokumen](#bagian-2-briefing-misi-kasus-kebocoran-dokumen)
3. [Konsep Inti](#bagian-3-konsep-inti)
4. [Panduan Praktik Step-by-Step](#bagian-4-panduan-praktik-step-by-step-hands-on-lab)
5. [Prompt Drill: Latihan Bertanya ke AI](#bagian-5-prompt-drill-latihan-bertanya-ke-ai)
6. [Lembar Jawaban Siswa & Template Write-Up](#bagian-6-lembar-jawaban-siswa-template-write-up)
7. [Lampiran Instruktur](#lampiran-c-panduan-instruktur)

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# BAGIAN 1: INFORMASI MODUL & TARGET CAPAIAN

## 1.1 Identitas Modul

| Item | Keterangan |
|---|---|
| **Kode Modul** | LAB-02 / FORENSICS-NET-ADV |
| **Judul** | Needle in a Haystack: Filter Lanjutan, DNS Tracking, & Ekstraksi File |
| **Kategori CTF** | Forensics / Network Traffic Analysis |
| **Tingkat Kesulitan** | ★★☆☆☆ (Easy-Medium, soal nomor 4-8 di babak penyisihan) |
| **Metode** | Praktik berpasangan, 1 laptop per siswa |
| **File Latihan** | `lab02/lab02_export_object.pcapng` (59 paket, 19.480 byte) |
| **Modul Prasyarat** | LAB 01 - The Wire Sniffer |

## 1.2 Alokasi Waktu (Total 60 Menit)

| Sesi | Kegiatan | Durasi |
|---|---|---|
| **Sesi 0** | Persiapan alat, salin file `.pcapng`, tes buka di Wireshark | 5 menit |
| **Sesi 1** | Briefing misi + konsep DNS dan rekonstruksi file | 10 menit |
| **Sesi 2** | Bagian A: DNS Hunting | 12 menit |
| **Sesi 3** | Bagian B: Filter bertingkat dengan operator logika | 12 menit |
| **Sesi 4** | Bagian C: Ekstraksi file lewat Export Objects | 13 menit |
| **Sesi 5** | Prompt drill AI + isi lembar jawaban | 5 menit |
| **Sesi 6** | Diskusi, koreksi, tanya jawab | 3 menit |

> **Catatan pembina:** Sesi 3 paling sering molor. Siswa cenderung menulis filter panjang sekaligus lalu bingung ketika kotaknya merah. Latih mereka membangun filter bertahap: uji satu syarat dulu, baru sambung dengan `&&`.

## 1.3 Prasyarat

| Prasyarat | Cara memastikan |
|---|---|
| **LAB 01 tuntas** | Siswa bisa menyebut fungsi `http`, `ip.addr`, dan Follow TCP Stream tanpa membuka catatan |
| **Wireshark 4.0+** | Buka aplikasi, menu **File → Export Objects** tersedia dan tidak kelabu |
| **Browser** | Bisa membuka file gambar lokal lewat `Ctrl+O` |
| **Folder kerja kosong** | Buat folder `Ekstraksi-LAB02` di Desktop sebagai tempat menyimpan hasil |
| **File latihan** | `lab02_export_object.pcapng`, ukuran 19.480 byte |

> **Pengaturan Wireshark yang wajib menyala.** Buka **Edit → Preferences → Protocols → TCP**, pastikan **Allow subdissector to reassemble TCP streams** tercentang. Tanpa itu, Wireshark tidak menyatukan potongan file dan menu Export Objects akan tampil kosong. Pengaturan ini menyala secara bawaan, tetapi tetap periksa sebelum lab mulai.

## 1.4 Capaian Pembelajaran (Learning Outcomes)

| Kode | Rumusan Capaian (terukur) | Bukti Ketercapaian |
|---|---|---|
| **LO-1** | Menyusun display filter bertingkat menggunakan operator `==`, `contains`, `&&`, dan `\|\|` yang menghasilkan tepat kumpulan paket yang dituju, minimal 4 filter berbeda. | Kolom "Filter yang dipakai" pada Tabel Temuan terisi dan hasilnya cocok |
| **LO-2** | Menjelaskan fungsi DNS sebagai penerjemah nama domain ke alamat IP, lalu menunjukkan letak nama domain pada panel Packet Details. | Jawaban Pertanyaan Refleksi nomor 1 |
| **LO-3** | Mengidentifikasi minimal 2 ciri domain mencurigakan dari lalu lintas DNS dalam waktu kurang dari 6 menit. | Domain janggal tercatat benar beserta nomor paketnya |
| **LO-4** | Menjelaskan bagaimana satu file utuh terpecah menjadi banyak segmen TCP dan disatukan kembali oleh Wireshark. | Jawaban Pertanyaan Refleksi nomor 2 |
| **LO-5** | Mengekstrak file gambar dari lalu lintas HTTP menggunakan **File → Export Objects → HTTP**, menyimpannya ke disk, lalu membukanya. | File hasil ekstraksi ada di folder kerja, nilai MD5 cocok |
| **LO-6** | Membaca flag berformat `JCC{...}` dari dalam berkas hasil ekstraksi dan menyalinnya tanpa satu pun karakter salah. | Flag tercatat benar di lembar jawaban |
| **LO-7** | Menyusun write-up sesuai juknis JCC 2026 lengkap dengan log prompt AI. | Dokumen write-up 7 bagian terisi |

## 1.5 Aturan Main

> ### ⚠️ ETIKA DAN BATASAN
>
> 1. **Semua data buatan.** Domain, IP, dan file di lab ini dibuat khusus untuk latihan. Domain `free-hosting-murah.tk` tidak nyata, jangan dikunjungi.
> 2. **Jangan pernah menyadap jaringan sekolah atau publik.** UU ITE Pasal 31 mengancam pidana untuk intersepsi tanpa hak.
> 3. **Automated scanner tetap dilarang di JCC 2026.** Modul ini murni memakai fitur bawaan Wireshark dan mata kalian sendiri.
> 4. **AI boleh dipakai**, dengan syarat setiap prompt dicatat dan dilampirkan di write-up.
> 5. **File hasil ekstraksi di lab ini aman.** Di dunia nyata, file yang kalian tarik dari lalu lintas malware bisa berisi program berbahaya. Buka file semacam itu hanya di mesin virtual yang terisolasi, tidak pernah di laptop pribadi.

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# BAGIAN 2: BRIEFING MISI: KASUS KEBOCORAN DOKUMEN

## 2.1 Situasi

```
=====================================================================
  LAPORAN INSIDEN #2026-0225-02           KLASIFIKASI: SANGAT RAHASIA
  Unit Teknologi Informasi, SMK Maskumambang 1
  Waktu kejadian : Rabu, 25 Februari 2026, 13:40 WIB
  Pelapor        : Sistem monitoring perimeter (otomatis)
  Status         : ESKALASI ke tim forensik siswa
=====================================================================
```

Empat jam setelah kalian menutup kasus Portal Nilai, alarm kedua berbunyi.

Sistem monitoring di gateway sekolah menandai satu workstation di **Lab Multimedia**, alamatnya `192.168.10.44`. Mesin itu tiba-tiba menghubungi server yang tidak pernah dikenal, di luar jaringan sekolah, lewat HTTP polos.

Anehnya bukan cuma itu. Beberapa detik sebelum koneksi terjadi, workstation itu menanyakan sebuah nama domain yang tidak masuk akal ke server DNS sekolah. Nama domainnya panjang, berakhiran `.tk`, dan salah satu bagiannya berupa deretan huruf acak yang jelas bukan bahasa manusia.

Kepala Program Keahlian curiga ada orang menyalin dokumen ujian ke luar sekolah. Rekaman lalu lintas 20 detik terakhir sudah diamankan sebagai `lab02_export_object.pcapng`, berisi **59 paket**.

Kalian punya 60 menit. Berkas bukti itu jerami, dan di dalamnya ada satu jarum.

## 2.2 Misi Kalian

| # | Pertanyaan Investigasi | Nilai |
|---|---|---|
| **M1** | Workstation mana yang melakukan query DNS, dan ke server DNS mana? | 10 poin |
| **M2** | Sebutkan **nama domain janggal** yang di-query, plus dua alasan kenapa kalian menilainya janggal. | 20 poin |
| **M3** | Alamat IP mana yang menjadi jawaban atas query domain janggal itu? | 10 poin |
| **M4** | Ada berapa berkas yang diunduh dari server itu, dan apa saja namanya? | 15 poin |
| **M5** | Ekstrak berkas gambar yang bocor, lalu catat nama, ukuran, dan nilai MD5-nya. | 20 poin |
| **M6** | Buka gambar hasil ekstraksi, temukan **FLAG** di dalamnya. | 25 poin |

**Bonus (15 poin):** salah satu label pada domain janggal itu ter-encode. Bongkar isinya dan jelaskan apa artinya bagi investigasi kalian.

## 2.3 Format Flag

```
JCC{TEKS_HURUF_BESAR_PAKAI_GARIS_BAWAH}
```

Flag di lab ini tertulis dengan **huruf besar semua**. Salin persis apa yang kalian lihat.

> 💡 **Peringatan salin-tempel.** Flag di lab ini berada di dalam gambar, jadi kalian tidak bisa mem-blok dan menekan `Ctrl+C`. Kalian harus mengetiknya ulang. Perbesar gambar sampai 200% sebelum mengetik, lalu bacakan keras-keras ke pasangan tim kalian untuk verifikasi. Angka `0` di gambar ini digambar dengan garis miring di tengah supaya tidak tertukar dengan huruf `O`.

## 2.4 Peta Jaringan TKP

```
        SMK MASKUMAMBANG 1                    |         INTERNET
                                              |
   [Workstation Lab Multimedia]               |
        192.168.10.44                         |
        MAC 08:00:27:9f:8e:21                 |
              |                               |
              | (1) tanya nama domain         |
              v                               |
        [DNS Server]                          |
        192.168.10.1  -------------------------------> ???
              |                               |
              | (2) jawab: 185.220.101.47     |
              v                               |
        [Gateway] ------------------------------> [Server Asing]
                                              |    185.220.101.47
                                              |    port 80, HTTP polos
                                              |    arsip-nilai.free-hosting-murah.tk
```

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# BAGIAN 3: KONSEP INTI

## 3.1 DNS: Buku Kontak Telepon Internet

Bayangkan kalian mau menelepon teman bernama **Nabila**. Kalian tidak menghafal nomornya, `0812-3456-7890`. Kalian buka kontak di HP, ketik "Nabila", dan HP kalian yang mencarikan nomornya.

Komputer punya masalah yang sama. Manusia hafal `www.smkmaska.sch.id`, sedangkan jaringan hanya paham angka `103.28.14.92`. **DNS (Domain Name System)** adalah buku kontak yang menjembatani keduanya.

### Urutan kejadiannya

```
   Kalian ketik "www.smkmaska.sch.id" di browser
                    |
                    v
   [1] Komputer bertanya ke server DNS:
       "Berapa nomor si www.smkmaska.sch.id?"     <-- ini disebut QUERY
                    |
                    v
   [2] Server DNS menjawab:
       "Nomornya 103.28.14.92"                     <-- ini disebut RESPONSE
                    |
                    v
   [3] Baru setelah itu komputer menghubungi 103.28.14.92
```

### Kenapa investigator sangat menyukai DNS

Tiga alasan, dan ketiganya berguna untuk kalian:

1. **DNS terjadi lebih dulu.** Sebelum satu byte data pun dikirim, komputer sudah mengumumkan tujuannya. Query DNS ibarat pengumuman rencana.
2. **DNS hampir selalu polos.** Sebagian besar DNS tetap berjalan tanpa enkripsi. Meski situs tujuannya HTTPS, nama domainnya tetap terbaca di query DNS.
3. **DNS sulit disembunyikan.** Program apa pun yang ingin menghubungi server lewat nama domain harus bertanya dulu. Ia meninggalkan jejak.

Dengan kata lain: **HTTPS menutup isi surat, tetapi DNS tetap membocorkan alamat tujuannya.** Kalimat ini melanjutkan pelajaran Lab 01 dan penting untuk write-up kalian.

### Ciri domain mencurigakan

| Ciri | Contoh | Kenapa mencurigakan |
|---|---|---|
| **TLD murah atau gratis** | `.tk`, `.ml`, `.ga`, `.cf`, `.gq` | Bisa didaftarkan gratis dan anonim, favorit penyerang |
| **Nama meniru instansi** | `arsip-nilai.free-hosting-murah.tk` | Memakai kata "arsip-nilai" supaya terlihat resmi |
| **Label acak dan panjang** | `ZG9rdW1lbi1yYWhhc2lh.exfil.` | Deretan huruf tanpa makna, sering hasil encoding data |
| **Subdomain bertumpuk** | `a.b.c.d.domain.tk` | Pola khas DNS tunneling untuk menyelundupkan data |
| **Query berulang cepat** | puluhan query berbeda per detik | Ciri exfiltration lewat DNS |

> ### 🔍 Petunjuk untuk misi kalian
> Salah satu label domain di file latihan ini berisi teks ber-encoding. Kalau kalian menemukan deretan huruf yang panjangnya kelipatan 4 dan hanya memakai A-Z, a-z, 0-9, itu tanda kuat **Base64**. Bongkar isinya dan kalian akan paham apa yang sedang dicuri.

## 3.2 Bagaimana Satu File Bisa Disatukan Kembali

Kembali ke analogi Lab 01: data besar dipotong menjadi banyak amplop kecil. Sekarang kita lihat detailnya.

Sebuah gambar berukuran 6.476 byte tidak muat dalam satu paket. Batas isi satu paket di jaringan Ethernet biasanya **1.460 byte**, disebut **MSS (Maximum Segment Size)**. Jadi gambar itu dipotong menjadi lima potongan.

```
   FILE ASLI DI SERVER: bocoran-soal-un-2026.png  (6.476 byte)

   +---------------------------------------------------------------+
   |  PNG header |  data gambar .............................. akhir |
   +---------------------------------------------------------------+
              |
              |  dipotong sesuai MSS 1.460 byte
              v
   +--------+ +--------+ +--------+ +--------+ +------+
   | seq 1  | | seq 2  | | seq 3  | | seq 4  | | seq 5|
   | 1460 B | | 1460 B | | 1460 B | | 1460 B | | 851 B|
   +--------+ +--------+ +--------+ +--------+ +------+
     frame 25   frame 26   frame 28   frame 29   frame 31

   (segmen pertama juga membawa 215 byte header HTTP,
    jadi totalnya 215 + 6.476 = 6.691 byte)
              |
              |  Wireshark membaca nomor urut (sequence number)
              |  dan menyusunnya kembali
              v
   +---------------------------------------------------------------+
   |          FILE UTUH, siap disimpan lewat Export Objects         |
   +---------------------------------------------------------------+
```

**Kunci yang membuat ini mungkin: setiap segmen TCP membawa nomor urut.** Persis seperti nomor halaman di buku yang dipotong. Meski paket tiba tidak berurutan, Wireshark tetap bisa menyusunnya benar.

### Kenapa Wireshark tahu itu file gambar

Server memberi tahu jenis berkas lewat header HTTP:

```
Content-Type: image/png          <-- jenis berkas
Content-Length: 6476             <-- panjangnya, dipakai untuk tahu kapan berhenti
```

Wireshark membaca `Content-Length`, mengumpulkan segmen sampai jumlahnya pas 6.476 byte, lalu berkata "berkas ini lengkap". Setelah itu berkas muncul di daftar **Export Objects**.

> ### 🎯 Inti yang harus nempel di kepala
> Apa pun yang lewat HTTP polos, entah gambar, PDF, video, atau installer, bisa direkonstruksi utuh oleh siapa pun yang merekam jalurnya. Enkripsi bukan sekadar melindungi password, tetapi juga melindungi berkas.

## 3.3 Cheatsheet Operator Filter Wireshark

### Operator perbandingan

| Operator | Bentuk lain | Arti | Contoh |
|---|---|---|---|
| `==` | `eq` | sama dengan | `ip.addr == 185.220.101.47` |
| `!=` | `ne` | tidak sama dengan | `ip.src != 192.168.10.44` |
| `>` `<` | `gt` `lt` | lebih besar / kecil | `frame.len > 1000` |
| `>=` `<=` | `ge` `le` | lebih besar / kecil atau sama | `http.response.code >= 400` |
| `contains` | | memuat teks atau byte tertentu | `frame contains "PNG"` |
| `matches` | `~` | cocok dengan pola regex | `dns.qry.name matches "(?i)\\.tk$"` |

### Operator logika

| Operator | Bentuk lain | Arti | Cara membacanya |
|---|---|---|---|
| `&&` | `and` | **DAN** | kedua syarat harus benar |
| `\|\|` | `or` | **ATAU** | cukup salah satu benar |
| `!` | `not` | **BUKAN** | kebalikan dari syarat |

### Cara membaca operator logika

```
   ip.addr == 185.220.101.47  &&  http.request.method == "GET"
   \________________________/      \___________________________/
        syarat pertama                    syarat kedua
                        \      /
                         \    /
                       KEDUANYA harus benar
   Hasil: hanya request GET yang berhubungan dengan IP itu


   http.response.code == 200  ||  http.response.code == 404
   \______________________/       \______________________/
        syarat pertama                 syarat kedua
                        \      /
                         \    /
                    CUKUP SALAH SATU benar
   Hasil: respons sukses maupun respons gagal, keduanya tampil
```

### Empat filter wajib hafal untuk lab ini

| Filter | Fungsi |
|---|---|
| `ip.addr == 185.220.101.47` | semua paket yang berhubungan dengan satu IP |
| `http.request.method == "GET"` | semua permintaan pengambilan berkas |
| `frame contains "PNG"` | paket yang memuat teks atau byte tertentu |
| `dns` | seluruh lalu lintas penerjemahan nama domain |

### Cara membangun filter bertingkat tanpa pusing

Jangan menulis filter panjang sekaligus. Bangun bertahap, uji tiap tahap:

```
Tahap 1:  dns                                      -> 10 paket, terlalu banyak
Tahap 2:  dns && dns.flags.response == 0           -> 5 paket, tinggal query saja
Tahap 3:  dns.qry.name contains "tk"               -> 4 paket, mengerucut
Tahap 4:  dns.flags.response == 0 && dns.qry.name contains "free-hosting"
                                                   -> 2 paket, ketemu
```

> ### ⚠️ Tiga kesalahan sintaks yang paling sering terjadi
> | Salah | Benar | Sebabnya |
> |---|---|---|
> | `http.request.method == GET` | `http.request.method == "GET"` | teks harus diapit tanda kutip |
> | `ip.addr = 185.220.101.47` | `ip.addr == 185.220.101.47` | perbandingan pakai dua tanda sama dengan |
> | `dns AND http` | `dns && http` atau `dns and http` | huruf besar tidak dikenali |

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# BAGIAN 4: PANDUAN PRAKTIK STEP-BY-STEP (HANDS-ON LAB)

> **Cara membaca bagian ini.** Setiap langkah punya kotak ✅ **CEK KEBERHASILAN**. Jangan lanjut sebelum layar kalian cocok. Kalau tidak cocok, baca 🔧 **KALAU MACET** di bawahnya.

## LANGKAH 0: Membuka Berkas Bukti

1. Buka **Wireshark**.
2. **File → Open** (`Ctrl + O`), pilih `lab02_export_object.pcapng`, klik **Open**.
3. Rapikan tampilan waktu: **View → Time Display Format → Seconds Since Beginning of Capture**.

> ✅ **CEK KEBERHASILAN**
> Panel atas berisi **59 baris**. Baris 1 berprotokol **DNS**, kolom `Info` bertuliskan `Standard query 0x2c41 A www.smkmaska.sch.id`. Status bar paling bawah menulis `Packets: 59 · Displayed: 59 (100.0%)`.

> 🔧 **KALAU MACET**
> - Jumlah baris bukan 59: ada filter tersisa. Kosongkan kotak filter, tekan `Enter`.
> - Kolom `Info` kosong melompong: berkas mungkin rusak saat disalin. Cek ukurannya harus 19.480 byte.

***

## BAGIAN A: DNS HUNTING

### LANGKAH A1: Melihat Semua Lalu Lintas DNS

1. Klik kotak filter di bagian atas (`Ctrl + /` untuk melompat ke sana).
2. Ketik `dns`, tekan `Enter`.

> ✅ **CEK KEBERHASILAN**
> Tersisa **10 baris**, semuanya berprotokol `DNS`, status bar menulis `Displayed: 10 (16.9%)`. Isinya berpasangan: satu query diikuti satu response.
>
> | No. | Info |
> |---|---|
> | 1 | `Standard query 0x2c41 A www.smkmaska.sch.id` |
> | 2 | `Standard query response 0x2c41 A www.smkmaska.sch.id A 103.28.14.92` |
> | 3 | `Standard query 0x2c42 A portal-nilai.smkmaska.local` |
> | 4 | `Standard query response 0x2c42 A portal-nilai.smkmaska.local A 192.168.10.10` |
> | 5 | `Standard query 0x2c43 A fonts.gstatic.com` |
> | 6 | `Standard query response 0x2c43 A fonts.gstatic.com A 142.250.199.67` |
> | 7 | `Standard query 0x2c44 A arsip-nilai.free-hosting-murah.tk` |
> | 8 | `Standard query response 0x2c44 ... A 185.220.101.47` |
> | 9 | `Standard query 0x2c45 A ZG9rdW1lbi1yYWhhc2lh.exfil.free-hosting-murah.tk` |
> | 10 | `Standard query response 0x2c45 ... A 185.220.101.47` |

**🔍 Berhenti dan amati.** Tiga domain pertama wajar: situs sekolah, portal internal, dan server font. Dua domain terakhir berbeda sendiri. Tulis di lembar jawaban sekarang, sebelum lupa.

### LANGKAH A2: Menyaring Query Saja

Response DNS hanya mengulang isi query, jadi separuh daftar tadi sebenarnya duplikat. Buang saja.

1. Ganti filter menjadi:
   ```
   dns.flags.response == 0
   ```
2. Tekan `Enter`.

> ✅ **CEK KEBERHASILAN**
> Tersisa **5 baris**: paket 1, 3, 5, 7, dan 9. Semuanya berjalan dari `192.168.10.44` menuju `192.168.10.1`.

**Catat dua fakta ini untuk M1:** workstation `192.168.10.44` bertanya ke server DNS `192.168.10.1`.

### LANGKAH A3: Membaca Nama Domain di Packet Details

Kolom `Info` sudah menampilkan nama domain, tetapi kalian perlu tahu letak persisnya di struktur paket. Juri JCC sering meminta bukti sampai level field.

1. Klik baris paket **nomor 9**.
2. Lihat **panel tengah (Packet Details)**.
3. Klik tanda panah untuk membuka lipatan berikut, satu per satu:

```
Domain Name System (query)
 └─ Transaction ID: 0x2c45
 └─ Flags: 0x0100 Standard query
 └─ Questions: 1
 └─ Queries
     └─ ZG9rdW1lbi1yYWhhc2lh.exfil.free-hosting-murah.tk: type A, class IN
         └─ Name: ZG9rdW1lbi1yYWhhc2lh.exfil.free-hosting-murah.tk
         └─ [Name Length: 47]
         └─ Type: A (Host Address) (1)
         └─ Class: IN (0x0001)
```

> ✅ **CEK KEBERHASILAN**
> Kalian menemukan baris **Name:** berisi nama domain lengkap. Klik baris itu satu kali, lalu perhatikan **panel bawah**: byte yang bersangkutan langsung tersorot. Wireshark selalu menghubungkan tampilan terjemahan dengan byte aslinya.

> 💡 **Trik cepat.** Klik kanan pada baris **Name:** → **Apply as Filter** → **Selected**. Wireshark menuliskan sendiri filter `dns.qry.name == "..."` ke kotak filter. Pakai cara ini setiap kali kalian malas mengetik nama field yang panjang.

### LANGKAH A4: Memburu Domain Janggal dengan `contains`

Di kompetisi, daftar DNS bisa berisi ratusan baris. Kalian butuh cara menyaring berdasarkan ciri, bukan membaca satu per satu.

1. Ketik filter:
   ```
   dns.qry.name contains "free-hosting"
   ```
2. Tekan `Enter`.

> ✅ **CEK KEBERHASILAN**
> Tersisa **4 baris**: paket 7, 8, 9, dan 10. Dua query dan dua response, semuanya menuju domain yang sama-sama mencurigakan.

Coba juga variasi berikut dan amati bedanya:

| Filter | Hasil | Gunanya |
|---|---|---|
| `dns.qry.name contains ".tk"` | 4 baris | menyaring berdasarkan TLD gratis |
| `dns.qry.name contains "exfil"` | 2 baris | menyaring berdasarkan kata kunci mencurigakan |
| `dns && frame.len > 90` | beberapa baris | query bernama panjang cenderung berukuran besar |

### LANGKAH A5: Membongkar Label Ber-encoding (Bonus)

Perhatikan label pertama pada domain paket 9: `ZG9rdW1lbi1yYWhhc2lh`.

Ciri-cirinya: panjang 20 karakter, hanya huruf dan angka, tidak ada makna dalam bahasa mana pun, dan panjangnya kelipatan 4. Itu pola **Base64**.

**Bongkar di terminal Linux:**
```bash
echo 'ZG9rdW1lbi1yYWhhc2lh' | base64 -d
```

**Bongkar tanpa terminal:** buka `gchq.github.io/CyberChef`, tarik operasi **From Base64** ke panel Recipe, tempel teksnya di kotak Input.

> ✅ **CEK KEBERHASILAN**
> Hasilnya sebuah kata berbahasa Indonesia yang langsung menjelaskan apa yang sedang dikirim keluar. Catat hasilnya di lembar jawaban bagian Bonus, plus satu kalimat penjelasan kenapa temuan itu penting.

> 🔧 **KALAU MACET**
> Perintah `base64 -d` mengeluarkan sampah: kemungkinan kalian ikut menyalin titik di ujung label. Salin **hanya** bagian sebelum titik pertama.

***
<div class="page-break"></div>

```{=latex}
\newpage
```

## BAGIAN B: FILTER BERTINGKAT

### LANGKAH B1: Melihat Seluruh Lalu Lintas Web

1. Ketik filter `http`, tekan `Enter`.

> ✅ **CEK KEBERHASILAN**
> Tersisa **10 baris**: 5 permintaan dan 5 jawaban.
>
> | No. | Source | Info |
> |---|---|---|
> | 14 | 192.168.10.44 | `GET /arsip/ HTTP/1.1` |
> | 15 | 185.220.101.47 | `HTTP/1.1 200 OK (text/html)` |
> | 17 | 192.168.10.44 | `GET /assets/logo-sekolah.png HTTP/1.1` |
> | 19 | 185.220.101.47 | `HTTP/1.1 200 OK (PNG)` |
> | 21 | 192.168.10.44 | `GET /arsip/daftar-hadir-rapat.pdf HTTP/1.1` |
> | 22 | 185.220.101.47 | `HTTP/1.1 200 OK (PDF)` |
> | 24 | 192.168.10.44 | `GET /arsip/bocoran-soal-un-2026.png HTTP/1.1` |
> | 31 | 185.220.101.47 | `HTTP/1.1 200 OK (PNG)` |
> | 40 | 192.168.10.44 | `GET /arsip/kunci-jawaban.zip HTTP/1.1` |
> | 41 | 185.220.101.47 | `HTTP/1.1 404 Not Found (text/html)` |

**🔍 Perhatikan keanehan nomor paket.** Permintaan gambar bocor ada di paket **24**, tetapi jawabannya baru muncul di paket **31**. Ke mana perginya paket 25 sampai 30?

Jawabannya: paket 25, 26, 28, dan 29 berisi potongan-potongan gambar itu, sedangkan paket 27 dan 30 adalah tanda terima (ACK) dari workstation. Wireshark menahan tampilan barisnya sampai potongan terakhir tiba di paket 31, baru menuliskan satu baris HTTP utuh. Itulah **reassembly** dari Bagian 3.2, terlihat langsung di layar.

Buktikan sendiri: klik paket **31**, buka panel tengah, dan cari baris:

```
[5 Reassembled TCP Segments (6691 bytes): #25(1460), #26(1460), #28(1460),
 #29(1460), #31(851)]
```

Klik baris itu, dan Wireshark menyorot semua paket penyusunnya.

### LANGKAH B2: Menggabungkan Dua Syarat dengan `&&`

Sekarang persempit: hanya permintaan pengambilan berkas, dan hanya yang berhubungan dengan server asing.

1. Ketik filter:
   ```
   ip.addr == 185.220.101.47 && http.request.method == "GET"
   ```
2. Tekan `Enter`.

> ✅ **CEK KEBERHASILAN**
> Tersisa **5 baris**: paket 14, 17, 21, 24, dan 40. Semuanya `GET`, semuanya menuju `185.220.101.47`. Tidak ada satu pun baris jawaban server yang ikut, karena syarat kedua hanya meloloskan permintaan.

**Inilah jawaban M4.** Lima permintaan, tetapi hanya empat berkas yang benar-benar terkirim. Satu permintaan gagal, dan kalian akan membuktikannya di Langkah B3.

### LANGKAH B3: Menggabungkan dengan `||` dan Membaca Kode Status

1. Ketik filter:
   ```
   http.response.code == 200 || http.response.code == 404
   ```
2. Tekan `Enter`.

> ✅ **CEK KEBERHASILAN**
> Tersisa **5 baris** jawaban server: empat berkode `200 OK` dan satu berkode `404 Not Found` di paket 41.

| Kode | Arti | Kesimpulan investigasi |
|---|---|---|
| **200 OK** | berkas ada dan terkirim | data benar-benar keluar dari sekolah |
| **404 Not Found** | berkas tidak ada di server | percobaan mengambil `kunci-jawaban.zip` gagal |

Catatan penting untuk write-up: paket 40 membuktikan pelaku **mencoba** mengambil `kunci-jawaban.zip`. Niatnya terekam meski usahanya gagal. Bukti percobaan tetap bernilai dalam laporan insiden.

### LANGKAH B4: Latihan Mandiri Operator Logika

Kerjakan lima soal berikut sendiri. Tulis filter dan jumlah hasilnya di lembar jawaban.

| # | Yang dicari | Filter kalian | Jumlah baris |
|---|---|---|---|
| 1 | Semua paket dari workstation, kecuali DNS | | |
| 2 | Semua permintaan GET untuk berkas berakhiran `.png` | | |
| 3 | Semua paket yang memuat teks `PNG` di isinya | | |
| 4 | Semua lalu lintas ke server asing, selain HTTP | | |
| 5 | Query DNS yang namanya lebih dari 30 karakter | | |

<details>
<summary><b>Petunjuk (buka hanya kalau sudah mentok 5 menit)</b></summary>

| # | Filter yang bekerja |
|---|---|
| 1 | `ip.src == 192.168.10.44 && !dns` |
| 2 | `http.request.uri contains ".png"` |
| 3 | `frame contains "PNG"` |
| 4 | `ip.addr == 185.220.101.47 && !http` |
| 5 | `dns.qry.name.len > 30` |

</details>

***
<div class="page-break"></div>

```{=latex}
\newpage
```

## BAGIAN C: EKSTRAKSI FILE

Bagian inilah alasan modul ini bernama Needle in a Haystack. Kalian akan menarik keluar berkas utuh dari tumpukan paket, lalu membukanya seperti berkas biasa.

### LANGKAH C1: Membuka Daftar Objek HTTP

1. Kosongkan kotak filter lebih dulu, tekan `Enter`. (Export Objects membaca seluruh berkas, jadi filter tidak berpengaruh, tetapi layar yang bersih memudahkan kalian.)
2. Pada menu bar, klik **File**.
3. Arahkan ke **Export Objects**. Sebuah submenu terbuka ke samping berisi pilihan: `DICOM…`, `HTTP…`, `IMF…`, `SMB…`, `TFTP…`.
4. Klik **HTTP…**

Sebuah jendela baru terbuka berjudul **Wireshark · Export · HTTP object list**.

> ✅ **CEK KEBERHASILAN**
> Jendela itu berisi tabel **5 baris** dengan kolom `Packet`, `Hostname`, `Content Type`, `Size`, dan `Filename`:
>
> | Packet | Hostname | Content Type | Size | Filename |
> |---|---|---|---|---|
> | 15 | arsip-nilai.free-hosting-murah.tk | text/html; charset=UTF-8 | 475 bytes | `\` |
> | 19 | arsip-nilai.free-hosting-murah.tk | image/png | 1.405 bytes | `logo-sekolah.png` |
> | 22 | arsip-nilai.free-hosting-murah.tk | application/pdf | 817 bytes | `daftar-hadir-rapat.pdf` |
> | 31 | arsip-nilai.free-hosting-murah.tk | image/png | 6.476 bytes | `bocoran-soal-un-2026.png` |
> | 41 | arsip-nilai.free-hosting-murah.tk | text/html | 39 bytes | `kunci-jawaban.zip` |
>
> Di bagian bawah jendela ada kotak **Text Filter**, lalu tombol **Preview**, **Save**, **Save All**, dan **Close**.

> 🔧 **KALAU MACET**
> - **Daftar kosong sama sekali:** buka **Edit → Preferences → Protocols → TCP**, centang **Allow subdissector to reassemble TCP streams**, klik OK, lalu ulangi.
> - **Menu Export Objects kelabu:** kalian belum membuka berkas `.pcapng` apa pun.
> - **Hanya muncul 2-3 baris:** kalian mungkin membuka berkas yang salah. Cek judul jendela Wireshark, harus tertulis `lab02_export_object.pcapng`.

**🔍 Baca tabel itu seperti detektif.** Baris terakhir menarik: nama berkasnya `kunci-jawaban.zip`, tetapi `Content Type`-nya `text/html` dan ukurannya cuma 39 byte. Itu bukan file zip, melainkan halaman error 404. Nama berkas tidak pernah menjamin isinya.

### LANGKAH C2: Memilih dan Menyimpan Berkas yang Bocor

1. Klik satu kali pada baris **`bocoran-soal-un-2026.png`** (baris packet 31) sampai tersorot biru.
2. Klik tombol **Save** di bagian bawah jendela.
3. Muncul dialog **Save Object As…**. Arahkan ke folder `Ekstraksi-LAB02` yang kalian siapkan di Desktop.
4. Biarkan nama berkasnya apa adanya, klik **Save**.

> ✅ **CEK KEBERHASILAN**
> Berkas `bocoran-soal-un-2026.png` muncul di folder `Ekstraksi-LAB02`. Klik kanan berkas itu → **Properties** (Windows) atau **Properties** (Linux). Ukurannya harus tertulis **6.476 byte**, bukan 6 KB yang dibulatkan. Kalau ukurannya berbeda, ekstraksi kalian gagal.

> 💡 **Tombol Preview.** Sebelum menyimpan, kalian bisa menekan **Preview** untuk mengintip isi berkas di dalam Wireshark. Berguna ketika daftar berisi puluhan berkas dan kalian belum tahu mana yang penting.

**Ambil juga dua berkas pengecoh** dengan cara yang sama, karena write-up kalian perlu menyebut semuanya:
- `logo-sekolah.png` (1.405 byte)
- `daftar-hadir-rapat.pdf` (817 byte)

Atau tekan **Save All** sekaligus, lalu pilih folder tujuan.

### LANGKAH C3: Memverifikasi Keaslian dengan MD5

Dalam forensik digital, kalian wajib membuktikan berkas hasil ekstraksi tidak berubah. Caranya menghitung **sidik jari digital** bernama hash. Satu byte berubah, seluruh sidik jarinya berubah.

**Linux / macOS:**
```bash
md5sum bocoran-soal-un-2026.png
```

**Windows PowerShell:**
```powershell
Get-FileHash -Algorithm MD5 .\bocoran-soal-un-2026.png
```

**Windows Command Prompt:**
```
certutil -hashfile bocoran-soal-un-2026.png MD5
```

> ✅ **CEK KEBERHASILAN**
> Hasilnya deretan 32 karakter heksadesimal. Catat di lembar jawaban. Pembina kalian memegang nilai pembandingnya. Kalau cocok, ekstraksi kalian sempurna.

### LANGKAH C4: Membuka Berkas dan Membaca Flag

1. Buka folder `Ekstraksi-LAB02`.
2. Klik dua kali berkas `bocoran-soal-un-2026.png`.
3. Kalau aplikasi gambar bawaan menolak membukanya, buka lewat browser: tekan `Ctrl + O` di Chrome atau Firefox, lalu pilih berkas itu.

> ✅ **CEK KEBERHASILAN**
> Muncul gambar berlatar biru navy dengan bingkai emas. Isinya:
> - Kop hijau: `SMK MASKUMAMBANG 1 - PONDOK PESANTREN MASKUMAMBANG`
> - Tulisan emas besar: `DOKUMEN INTERNAL - RAHASIA`
> - Baris: `KODE VERIFIKASI PANITIA JCC 2026 :`
> - Di dalam kotak gelap, dengan huruf emas: **flag kalian**

**Perbesar gambar sampai 200% sebelum menyalin.** Perhatikan tiga hal:
- Angka `0` digambar dengan garis miring di tengahnya, huruf `O` tidak.
- Angka `1` punya kaki di bawah, huruf `I` berbentuk palang atas-bawah.
- Kurung kurawal `{` dan `}` berbeda jelas dari tanda kurung biasa.

Ketik ulang flag itu di lembar jawaban, lalu minta pasangan tim kalian membacakannya ulang dari gambar sambil kalian mencocokkan huruf demi huruf. Dua mata lebih baik dari satu.

### LANGKAH C5: Memeriksa Metadata Tersembunyi (Pengayaan)

Berkas PNG bisa menyimpan catatan teks yang tidak tampil di gambar.

**Linux:**
```bash
strings bocoran-soal-un-2026.png | head -20
```

> ✅ **CEK KEBERHASILAN**
> Di antara karakter acak, muncul satu kalimat berbahasa Indonesia yang ditulis pembuat berkas. Kalimat itu tidak terlihat sama sekali saat gambar dibuka. Catat di write-up sebagai bukti tambahan.

Pelajaran yang dibawa pulang: **berkas menyimpan lebih banyak hal daripada yang terlihat.** Di soal CTF kategori Forensics, `strings` dan pemeriksaan metadata sering menjadi langkah pertama, bukan terakhir.

## 4.6 Ringkasan Perintah Bagian A sampai C

| Bagian | Tujuan | Filter atau menu |
|---|---|---|
| A1 | Lihat semua DNS | `dns` |
| A2 | Query saja | `dns.flags.response == 0` |
| A3 | Baca field nama domain | panel Packet Details → Queries → Name |
| A4 | Buru domain janggal | `dns.qry.name contains "free-hosting"` |
| A5 | Bongkar label ber-encoding | `base64 -d` atau CyberChef |
| B1 | Lihat lalu lintas web | `http` |
| B2 | GET ke server asing | `ip.addr == 185.220.101.47 && http.request.method == "GET"` |
| B3 | Sukses dan gagal | `http.response.code == 200 \|\| http.response.code == 404` |
| C1 | Daftar berkas | **File → Export Objects → HTTP…** |
| C2 | Simpan berkas | pilih baris → tombol **Save** |
| C3 | Verifikasi | `md5sum` atau `Get-FileHash` |
| C5 | Metadata tersembunyi | `strings` |

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# BAGIAN 5: PROMPT DRILL: LATIHAN BERTANYA KE AI

## 5.1 Pengingat Aturan JCC 2026

Chatbot AI boleh dipakai. Syaratnya satu, dan panitia menegakkannya:

> **Seluruh riwayat prompt dan alur penalaran tim wajib dilampirkan dalam write-up resmi.**

Juri membaca cara kalian berpikir. Tim yang menempel soal mentah lalu menyalin jawaban akan langsung terlihat di lampiran, dan nilai analisisnya jatuh.

## 5.2 Aturan Emas: AI Tidak Memegang Berkas Kalian

Chatbot tidak bisa melihat `lab02_export_object.pcapng`. Ia tidak tahu isi paket 31. Bertanya "apa flagnya?" sama saja meminta orang menebak isi kotak tertutup.

Pakai AI untuk empat hal ini, dan hasilnya akan bagus:

| Pakai AI untuk | Contoh |
|---|---|
| Memperbaiki sintaks filter yang error | "kenapa filter saya ditolak Wireshark?" |
| Menjelaskan arti field atau kode status | "apa beda 302 dan 404?" |
| Mengenali pola encoding | "ciri apa yang menandakan string ini Base64?" |
| Merapikan kalimat write-up | "rapikan paragraf ini tanpa mengubah temuan" |

Rumus prompt yang efektif:

```
[PERAN yang AI mainkan] + [KONTEKS situasi kalian] + [DATA spesifik, bukan seluruh soal]
+ [PERTANYAAN yang jelas] + [FORMAT jawaban yang diinginkan]
```

## 5.3 Template Prompt #1: Filter Wireshark yang Rumit

Pakai ini di Langkah B4 ketika filter kalian ditolak atau hasilnya meleset.

```text
Kamu adalah instruktur Wireshark untuk siswa SMK kelas 10 yang baru belajar
analisis paket.

KONTEKS:
Saya menganalisis file .pcapng berisi 59 paket dari jaringan lab sekolah.
Sebuah workstation 192.168.10.44 mengunduh beberapa berkas dari server asing
185.220.101.47 lewat HTTP polos. Saya ingin menampilkan HANYA permintaan
pengambilan berkas gambar berformat .png yang ditujukan ke server itu.

FILTER YANG SUDAH SAYA COBA:
    ip.addr == 185.220.101.47 and http.request.uri = ".png"
Hasilnya: kotak filter berwarna merah, tidak ada paket yang tampil.

PERTANYAAN:
1. Ada berapa kesalahan sintaks di filter saya, dan di bagian mana persisnya?
2. Tulis versi yang benar, lalu satu versi alternatif yang memakai operator
   "matches" supaya hanya cocok pada akhiran .png, bukan .png di tengah URL.
3. Jelaskan beda "contains" dan "matches" dalam 3 kalimat sederhana.

FORMAT JAWABAN:
Tabel dua kolom berjudul "Filter" dan "Penjelasan".
Bahasa Indonesia. Jangan pakai istilah teknis tanpa menjelaskannya.
Jangan berikan jawaban akhir saja, tunjukkan juga alasannya.
```

**Kenapa prompt ini bekerja:**
- Kalian melaporkan **apa yang sudah dicoba** beserta gejalanya, jadi AI mendiagnosis, bukan menebak.
- Kalian menyebut konteks jaringan tanpa membocorkan flag.
- Kalian minta format tabel, sehingga jawabannya bisa langsung ditempel ke write-up.
- Pertanyaan nomor 3 membuat kalian belajar konsep, bukan sekadar menyalin.

## 5.4 Template Prompt #2: Menganalisis Kode Status dan Jenis Berkas

Pakai ini di Langkah C1 ketika kalian menemukan baris ganjil di daftar Export Objects.

```text
Kamu adalah mentor CTF kategori Forensics untuk pemula.

KONTEKS:
Saya mengekstrak daftar objek HTTP dari sebuah file .pcapng menggunakan menu
File > Export Objects > HTTP di Wireshark. Salah satu barisnya seperti ini:

    Packet       : 41
    Content Type : text/html
    Size         : 39 bytes
    Filename     : kunci-jawaban.zip

Respons servernya berkode HTTP 404 Not Found.

PERTANYAAN:
1. Kenapa sebuah berkas bernama .zip bisa punya Content Type text/html?
2. Apa yang sebenarnya tersimpan di 39 byte itu?
3. Dalam laporan insiden keamanan, apakah permintaan yang gagal seperti ini
   tetap layak dilaporkan? Beri alasannya.
4. Sebutkan 2 cara manual memastikan jenis asli sebuah berkas hasil ekstraksi,
   tanpa memakai automated scanner.

FORMAT JAWABAN:
Poin bernomor, maksimal 3 kalimat per poin.
Bahasa Indonesia yang mudah dipahami siswa kelas 10.
```

**Kenapa prompt ini bekerja:**
- Kalian mengirim **satu potongan data konkret**, bukan seluruh tantangan.
- Pertanyaan nomor 3 mengarahkan AI membantu bagian analisis write-up, bagian yang paling bernilai di mata juri.
- Pertanyaan nomor 4 sengaja menyebut batasan lomba, jadi AI tidak menyarankan alat terlarang.

## 5.5 Disiplin Mencatat Prompt

Buka `prompt-log.md` di text editor **sebelum** lab dimulai. Setiap kali mengirim prompt, catat lima hal:

```markdown
### Prompt #1
- Waktu       : 14:07 WIB
- Chatbot     : Claude
- Prompt      : (salin persis yang kalian ketik, jangan diringkas)
- Inti jawaban: (1-2 kalimat)
- Keputusan   : (apa yang tim lakukan setelah membaca jawaban itu)
```

Mencatat sambil jalan makan waktu 20 detik. Menyusun ulang dari ingatan setelah lomba selesai makan 20 menit, dan hasilnya tetap meleset.

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# BAGIAN 6: LEMBAR JAWABAN SISWA & TEMPLATE WRITE-UP

## 6.1 Identitas Tim

| Field | Isian |
|---|---|
| Nama Tim | ................................................. |
| Anggota 1 | ................................................. |
| Anggota 2 | ................................................. |
| Tanggal Praktikum | ....... / ....... / 2026 |
| Waktu mulai | ....... : ....... WIB |
| Waktu selesai | ....... : ....... WIB |

## 6.2 Tabel Temuan Bukti

Kolom **Nomor Paket** wajib diisi. Juri memakai kolom itu untuk memverifikasi temuan kalian.

| Kode | Item Bukti | Temuan Kalian | Nomor Paket | Filter yang Dipakai |
|---|---|---|---|---|
| **B1** | IP workstation yang diselidiki | | | |
| **B2** | IP server DNS sekolah | | | |
| **B3** | Jumlah query DNS seluruhnya | | | |
| **B4** | 🚩 **Domain DNS mencurigakan (utama)** | | | |
| **B5** | Alasan pertama domain itu janggal | | | |
| **B6** | Alasan kedua domain itu janggal | | | |
| **B7** | Domain kedua yang mengandung label ter-encoding | | | |
| **B8** | Hasil decode label tersebut | | | |
| **B9** | IP jawaban DNS untuk domain janggal | | | |
| **B10** | Jumlah permintaan `GET` ke server asing | | | |
| **B11** | Nama berkas ke-1 yang diunduh | | | |
| **B12** | Nama berkas ke-2 yang diunduh | | | |
| **B13** | 🚩 **Nama berkas yang bocor (berisi flag)** | | | |
| **B14** | Ukuran berkas bocor (byte) | | | |
| **B15** | **MD5 berkas bocor** | | | |
| **B16** | Nama berkas yang gagal diambil | | | |
| **B17** | Kode status untuk permintaan gagal itu | | | |
| **B18** | Jumlah segmen TCP penyusun berkas bocor | | | |
| **B19** | Isi metadata tersembunyi di dalam PNG | | | |
| **B20** | 🚩 **FLAG** | `JCC{` ................................ `}` | | |

**Skor mandiri:** ...... dari 100 poin (+ 15 poin bonus)

## 6.3 Lembar Latihan Filter (dari Langkah B4)

| # | Yang dicari | Filter yang kalian tulis | Jumlah baris |
|---|---|---|---|
| 1 | Paket dari workstation, kecuali DNS | | |
| 2 | Permintaan GET berkas `.png` | | |
| 3 | Paket yang memuat teks `PNG` | | |
| 4 | Lalu lintas ke server asing, selain HTTP | | |
| 5 | Query DNS bernama lebih dari 30 karakter | | |

## 6.4 Pertanyaan Refleksi & Analisis Logika Keamanan

Jawab dengan kalimat kalian sendiri. Menyalin dari modul tidak mendapat nilai.

***

**PERTANYAAN 1 (Bobot 50): Tentang DNS**

Di Lab 01 kalian menyimpulkan bahwa HTTPS menyembunyikan isi percakapan. Di Lab 02 kalian melihat query DNS berjalan polos meski situs tujuannya nanti memakai HTTPS.

a. Andaikan pelaku mengunduh berkas itu lewat **HTTPS**, bukan HTTP. Bukti mana yang masih bisa kalian kumpulkan, dan bukti mana yang hilang?

b. Kenapa administrator jaringan sekolah lebih suka memantau log DNS dibanding memantau isi setiap paket? Sebutkan dua alasan praktis.

c. Sebutkan satu cara sekolah mencegah workstation menghubungi domain seperti `free-hosting-murah.tk`, lalu jelaskan kelemahan cara itu.

```
Jawaban:
_________________________________________________________________________

_________________________________________________________________________

_________________________________________________________________________

_________________________________________________________________________

_________________________________________________________________________
```

***

**PERTANYAAN 2 (Bobot 50): Tentang Rekonstruksi Berkas**

Berkas `bocoran-soal-un-2026.png` berukuran 6.476 byte dan terpecah menjadi beberapa segmen TCP sebelum sampai ke workstation.

a. Kenapa berkas itu harus dipecah? Sebutkan angka batas yang menyebabkannya.

b. Wireshark bisa menyusunnya kembali dengan urutan benar. Informasi apa di dalam paket yang memungkinkan hal itu?

c. Andaikan tiga dari segmen itu hilang dari rekaman karena perekam sempat mati sesaat. Apa yang akan terjadi pada daftar **Export Objects**, dan apa yang bisa kalian lakukan sebagai investigator?

d. Kaitkan dengan keamanan: kenapa mengirim dokumen sekolah lewat HTTP polos jauh lebih berbahaya daripada sekadar bocornya satu password?

```
Jawaban:
_________________________________________________________________________

_________________________________________________________________________

_________________________________________________________________________

_________________________________________________________________________

_________________________________________________________________________
```

***
<div class="page-break"></div>

```{=latex}
\newpage
```

## 6.5 Template Write-Up Resmi JCC 2026

> **Cara pakai:** salin seluruh blok di bawah ke text editor, simpan sebagai `writeup-lab02-[namatim].md`, isi setiap bagian, lalu ekspor ke PDF sebelum mengunggah. Jangan menghapus judul bagian mana pun.

````markdown
# WRITE-UP JCC 2026
## Nama Soal   : LAB 02 - Needle in a Haystack
## Kategori    : Forensics / Network Analysis
## Nama Tim    : ______________________
## Anggota     : 1. ______________________  2. ______________________
## Asal Sekolah: SMK Maskumambang 1
## Tanggal     : ____ / ____ / 2026
## Status      : [ ] Solved   [ ] Unsolved

# 1. DESKRIPSI SOAL
(Tulis ulang deskripsi dari panitia. Sebutkan nama berkas yang diberikan
beserta ukuran dan jumlah paketnya.)

# 2. ALAT YANG DIGUNAKAN
| Alat | Versi | Fungsi dalam penyelesaian |
|---|---|---|
| Wireshark | | |
| CyberChef / base64 | | |
| md5sum / Get-FileHash | | |
| Chatbot AI | | |

Pernyataan kepatuhan:
Tim menyatakan tidak menggunakan automated scanner (sqlmap, Burp Scanner,
dirb, nikto, atau sejenisnya). Seluruh analisis dilakukan manual memakai
fitur bawaan Wireshark.

Tanda tangan ketua tim: ______________________

# 3. ALUR PENALARAN (REASONING FLOW)
(Tulis urut sesuai kejadian, termasuk langkah yang gagal. Juri menilai proses
berpikir, jadi jangan menyembunyikan jalan buntu.)

## 3.1 Pengamatan awal
- Jumlah paket total: ____
- Protokol yang muncul (Statistics > Protocol Hierarchy): ____
- Hipotesis awal tim: ____

## 3.2 Pelacakan DNS
- Filter yang dipakai: ____
- Domain wajar yang ditemukan: ____
- Domain janggal yang ditemukan: ____
- Ciri yang membuat tim curiga: ____

## 3.3 Penyempitan lalu lintas HTTP
- Filter bertingkat yang dipakai: ____
- Alasan memilih operator && atau ||: ____
- Daftar berkas yang teridentifikasi: ____

## 3.4 Jalan buntu yang sempat ditemui
- Apa yang dicoba: ____
- Kenapa gagal: ____
- Pelajaran yang diambil: ____

## 3.5 Ekstraksi berkas
- Menu yang dipakai: ____
- Berkas yang dipilih dan alasannya: ____
- Cara tim memverifikasi berkas utuh: ____

## 3.6 Konfirmasi flag
- Cara tim memastikan flag terbaca benar: ____

# 4. LANGKAH TEKNIS (STEP-BY-STEP REPRODUCTION)
(Tulis sedetail mungkin sampai orang lain bisa mengulanginya tanpa bertanya.)

**Langkah 1:** ____
> Filter / menu: `____`
> Hasil: ____
> [Tangkapan layar 1]

**Langkah 2:** ____
> Filter / menu: `____`
> Hasil: ____
> [Tangkapan layar 2]

**Langkah 3:** ____
> Filter / menu: `____`
> Hasil: ____
> [Tangkapan layar 3]

**Langkah 4:** ____
> Filter / menu: `____`
> Hasil: ____
> [Tangkapan layar 4 - jendela Export Objects]

# 5. BUKTI TEMUAN
| Item | Nilai | Nomor Paket |
|---|---|---|
| IP workstation | | |
| Domain mencurigakan | | |
| IP server asing | | |
| Berkas bocor | | |
| Ukuran berkas | | |
| MD5 berkas | | |
| Label ter-encoding | | |
| Hasil decode | | |

**FLAG:**

    JCC{________________________________}

# 6. LAMPIRAN RIWAYAT PROMPT AI (WAJIB)
(Salin persis prompt yang tim kirimkan. Jangan dirapikan, jangan diringkas.
Kalau tim tidak memakai AI, tulis "Tidak menggunakan AI" dan kosongkan tabel.)

| No | Waktu | Chatbot | Prompt yang dikirim (lengkap) | Ringkasan jawaban AI | Keputusan tim setelah membaca |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

## Refleksi penggunaan AI
- Bagian yang dikerjakan tim sendiri tanpa AI: ____
- Bagian yang terbantu AI, dan seberapa besar bantuannya: ____
- Apakah ada jawaban AI yang keliru? Bagaimana tim mengetahuinya? ____

# 7. PELAJARAN & MITIGASI
## 7.1 Akar masalah
(Kenapa insiden ini bisa terjadi?)
____

## 7.2 Rekomendasi perbaikan untuk admin jaringan sekolah
1. ____
2. ____
3. ____

## 7.3 Refleksi tim
(Apa yang akan tim lakukan berbeda kalau mengerjakan soal serupa besok?)
____

Ditulis oleh: ______________________
Diperiksa oleh: ______________________
````

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# LAMPIRAN A: KARTU CONTEKAN (CHEAT SHEET)

> **Cetak halaman ini terpisah, tempel di meja latihan.**

## A.1 Filter DNS

| Filter | Fungsi |
|---|---|
| `dns` | seluruh lalu lintas DNS |
| `dns.flags.response == 0` | query saja |
| `dns.flags.response == 1` | jawaban saja |
| `dns.qry.name == "contoh.com"` | satu domain persis |
| `dns.qry.name contains "tk"` | domain yang memuat potongan teks |
| `dns.qry.name.len > 30` | nama domain yang panjangnya mencurigakan |
| `dns.flags.rcode != 0` | query yang gagal, misal NXDOMAIN |
| `dns.a == 185.220.101.47` | jawaban yang menunjuk ke IP tertentu |

## A.2 Filter HTTP

| Filter | Fungsi |
|---|---|
| `http` | seluruh lalu lintas HTTP |
| `http.request.method == "GET"` | pengambilan berkas |
| `http.request.method == "POST"` | pengiriman form |
| `http.request.uri contains ".png"` | permintaan berkas gambar |
| `http.response.code == 200` | berkas berhasil terkirim |
| `http.response.code >= 400` | seluruh permintaan yang gagal |
| `http.content_type contains "image"` | jawaban berupa gambar |
| `http.host contains "free-hosting"` | permintaan ke host tertentu |
| `http.file_data` | paket yang membawa isi berkas |

## A.3 Operator

| Operator | Arti | Contoh |
|---|---|---|
| `&&` atau `and` | dan | `dns && ip.src == 192.168.10.44` |
| `\|\|` atau `or` | atau | `http \|\| dns` |
| `!` atau `not` | bukan | `!(tls)` |
| `==` | sama dengan | `tcp.port == 80` |
| `!=` | tidak sama dengan | `ip.dst != 192.168.10.1` |
| `contains` | memuat teks/byte | `frame contains "PNG"` |
| `matches` | cocok pola regex | `dns.qry.name matches "\\.tk$"` |
| `in` | termasuk dalam daftar | `tcp.port in {80 443 8080}` |

## A.4 Menu Penting

| Menu | Kegunaan |
|---|---|
| **File → Export Objects → HTTP…** | menarik keluar berkas dari lalu lintas HTTP |
| **File → Export Packet Bytes** (`Ctrl+Shift+X`) | menyimpan potongan byte terpilih |
| **Statistics → Protocol Hierarchy** | komposisi protokol dalam satu layar |
| **Statistics → Conversations** | daftar pasangan IP yang saling bicara |
| **Statistics → DNS** | ringkasan seluruh aktivitas DNS |
| **Edit → Preferences → Protocols → TCP** | menyalakan reassembly |
| klik kanan → **Apply as Filter → Selected** | membuat filter otomatis dari field terpilih |
| klik kanan → **Follow → HTTP Stream** | membaca satu percakapan web utuh |

## A.5 Alur Kerja 90 Detik Pertama di Soal Forensics Jaringan

```
1. Buka berkas, catat jumlah paket
2. Statistics > Protocol Hierarchy   -> protokol apa saja yang ada?
3. Filter "dns"                      -> ke mana saja mesin ini bicara?
4. Cari domain aneh: TLD gratis, label acak, nama panjang
5. Filter "http"                     -> ada berkas yang lewat polos?
6. File > Export Objects > HTTP      -> ada berkas yang bisa ditarik?
7. Simpan semua berkas, buka satu per satu
8. Belum ketemu? jalankan "strings" pada tiap berkas
9. Masih belum? cek metadata, komentar, dan header non-standar
```

## A.6 Mengenali Jenis Berkas dari Byte Pertamanya

Byte pembuka sebuah berkas disebut **magic number**. Berguna ketika nama berkas berbohong.

| Byte pertama (hex) | Terbaca sebagai | Jenis berkas |
|---|---|---|
| `89 50 4E 47` | `.PNG` | PNG |
| `FF D8 FF` | | JPEG |
| `25 50 44 46` | `%PDF` | PDF |
| `50 4B 03 04` | `PK..` | ZIP, DOCX, XLSX, APK |
| `47 49 46 38` | `GIF8` | GIF |
| `52 61 72 21` | `Rar!` | RAR |
| `7F 45 4C 46` | `.ELF` | program Linux |
| `4D 5A` | `MZ` | program Windows (.exe) |

Cara memeriksanya di Linux:
```bash
xxd bocoran-soal-un-2026.png | head -2
file bocoran-soal-un-2026.png
```

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# LAMPIRAN B: KUNCI JAWABAN (KHUSUS PEMBINA)

> ## 🔒 HALAMAN INI JANGAN DIBAGIKAN KE SISWA
> Pisahkan atau hapus sebelum mencetak modul untuk latihan.

## B.1 Kunci Tabel Temuan

| Kode | Item | Jawaban Benar | Paket |
|---|---|---|---|
| B1 | IP workstation | `192.168.10.44` | 1 |
| B2 | IP server DNS | `192.168.10.1` | 1 |
| B3 | Jumlah query DNS | 5 query (10 paket DNS total) | 1-10 |
| B4 | Domain mencurigakan utama | `arsip-nilai.free-hosting-murah.tk` | 7 |
| B5 | Alasan pertama | TLD `.tk` gratis dan anonim | |
| B6 | Alasan kedua | nama meniru arsip sekolah, servernya di luar negeri | |
| B7 | Domain ber-encoding | `ZG9rdW1lbi1yYWhhc2lh.exfil.free-hosting-murah.tk` | 9 |
| B8 | Hasil decode | `dokumen-rahasia` | |
| B9 | IP jawaban DNS | `185.220.101.47` | 8 |
| B10 | Jumlah GET ke server asing | 5 permintaan | 14, 17, 21, 24, 40 |
| B11 | Berkas ke-1 | `logo-sekolah.png` (1.405 byte) | 19 |
| B12 | Berkas ke-2 | `daftar-hadir-rapat.pdf` (817 byte) | 22 |
| B13 | **Berkas bocor** | `bocoran-soal-un-2026.png` | 31 |
| B14 | Ukuran berkas bocor | 6.476 byte | |
| B15 | **MD5 berkas bocor** | `ea6262fd8f70204f0ff16b6de05ea1b9` | |
| B16 | Berkas gagal diambil | `kunci-jawaban.zip` | 40 |
| B17 | Kode status | `404 Not Found` | 41 |
| B18 | Jumlah segmen penyusun | 5 segmen data: frame 25, 26, 28, 29, 31 | |
| B19 | Metadata tersembunyi | `Arsip internal SMK Maskumambang 1. Distribusi terbatas.` | |
| B20 | **FLAG** | `JCC{DNS_B0C0R_G4MB4R_T3RB4C4}` | 31 |

**Nilai pembanding hash lainnya:**

| Berkas | Ukuran | MD5 |
|---|---|---|
| `logo-sekolah.png` | 1.405 byte | `79867e8f0d0d03e52ac3f21df5055e6b` |
| `daftar-hadir-rapat.pdf` | 817 byte | `0997eb1c7e5bd0a68f6079aa45779d45` |
| `bocoran-soal-un-2026.png` | 6.476 byte | `ea6262fd8f70204f0ff16b6de05ea1b9` |

## B.2 Kunci Lembar Latihan Filter

| # | Filter yang bekerja | Jumlah baris |
|---|---|---|
| 1 | `ip.src == 192.168.10.44 && !dns` | 28 |
| 2 | `http.request.uri contains ".png"` | 2 |
| 3 | `frame contains "PNG"` | 2 |
| 4 | `ip.addr == 185.220.101.47 && !http` | 26 |
| 5 | `dns.qry.name.len > 30` | 4 |

Filter alternatif tetap diterima selama hasilnya benar. Justru bagus kalau siswa menemukan jalan lain, misalnya `http.content_type == "image/png"` untuk soal nomor 2. Minta mereka menjelaskan bedanya.

## B.3 Rambu Jawaban Pertanyaan Refleksi

**Pertanyaan 1 (DNS).**

(a) Yang **tetap ada**: query DNS berisi nama domain, alamat IP tujuan, port, waktu, ukuran paket, dan SNI di TLS Client Hello. Yang **hilang**: nama berkas, isi berkas, dan menu Export Objects tidak berfungsi karena isi HTTP terenkripsi. Kesimpulan yang diharapkan: investigasi masih mungkin, tetapi kalian kehilangan barang buktinya sendiri.

(b) Dua alasan praktis yang diterima: log DNS jauh lebih kecil sehingga bisa disimpan berbulan-bulan, DNS terjadi lebih dulu sehingga bisa dipakai memblokir sebelum koneksi terjadi, DNS tetap terbaca meski lalu lintasnya HTTPS, dan memeriksa isi setiap paket melanggar privasi pengguna.

(c) Cara yang diterima: DNS filtering atau blokir kategori TLD gratis di resolver sekolah, firewall egress yang hanya mengizinkan port tertentu, atau proxy wajib. Kelemahan yang diharapkan siswa sebutkan: pelaku bisa memakai IP langsung tanpa DNS, memakai DNS over HTTPS yang tidak lewat resolver sekolah, atau memakai domain yang belum masuk daftar hitam. Beri nilai penuh kalau siswa menyebut satu kelemahan yang masuk akal.

**Pertanyaan 2 (Rekonstruksi).**

(a) Karena ukuran berkas melebihi batas isi satu paket. Angka yang dicari: **MSS 1.460 byte** (atau MTU 1.500 byte dikurangi header). Siswa yang menyebut MTU tetap benar selama menjelaskan hubungannya.

(b) **Sequence number** pada header TCP. Jawaban yang menyebut "nomor urut" tanpa istilah teknis tetap diterima di level kelas 10.

(c) Berkas akan tampil dengan ukuran tidak lengkap, atau hilang sama sekali dari daftar Export Objects karena `Content-Length` tidak pernah terpenuhi. Tindakan investigator yang diharapkan: menyimpan potongan yang ada lewat **File → Export Packet Bytes**, mencatat bahwa bukti tidak lengkap di write-up, dan mencari salinan berkas dari sumber lain seperti log server atau cache browser. Jawaban yang menekankan **kejujuran melaporkan bukti tidak lengkap** layak nilai penuh.

(d) Password bisa diganti dalam satu menit. Berkas yang sudah keluar tidak bisa ditarik kembali. Satu password bocor membuka satu akun, sedangkan satu berkas bocor bisa memuat data ratusan siswa sekaligus.

## B.4 Kesalahan yang Paling Sering Terjadi

| Gejala | Penyebab | Cara membimbing |
|---|---|---|
| Daftar Export Objects kosong | reassembly TCP dimatikan | tunjukkan Preferences → Protocols → TCP, jangan langsung perbaiki sendiri |
| Siswa mengambil `logo-sekolah.png` dan berhenti | tidak membaca kolom Size | tanyakan "berkas mana yang paling besar, dan kenapa ukurannya penting?" |
| Filter merah terus | tanda kutip melengkung hasil salin dari Word | minta mengetik ulang manual |
| Flag salah satu karakter | `0` dibaca `O`, atau `1` dibaca `I` | minta perbesar 200% dan bacakan berdua |
| Siswa menyerah di Base64 | tidak mengenali polanya | arahkan ke Lampiran A.6 dan template prompt AI nomor 1 |
| Bingung paket 24 lompat ke 31 | belum paham reassembly | buka panel Reassembled TCP Segments bersama-sama |

## B.5 Rubrik Penilaian Write-Up

| Komponen | Bobot | Kriteria nilai penuh |
|---|---|---|
| Kelengkapan temuan (Bagian 5) | 25% | 18 dari 20 item terisi benar beserta nomor paket |
| Alur penalaran (Bagian 3) | 30% | Runtut, memuat minimal satu jalan buntu yang dilaporkan jujur |
| Reproduksi langkah (Bagian 4) | 20% | Orang lain bisa mengulang tanpa bertanya, 4 tangkapan layar terbaca |
| Lampiran prompt AI (Bagian 6) | 15% | Prompt disalin utuh, refleksi terisi, tidak ada yang disembunyikan |
| Mitigasi & refleksi (Bagian 7) | 10% | Rekomendasi teknis spesifik, bukan slogan umum |

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# LAMPIRAN C: PANDUAN INSTRUKTUR

## C.1 Membuat Ulang Berkas Latihan

Berkas `lab02_export_object.pcapng` dibuat oleh skrip `lab02/generate_pcapng.py`. Skrip itu **tidak memerlukan scapy, Pillow, atau pustaka pihak ketiga mana pun**, hanya Python 3 bawaan. Alasannya sederhana: laptop pengajar di sekolah sering tidak punya akses internet saat jam praktik, dan instalasi paket justru memakan waktu lab.

```bash
cd lab02
python3 generate_pcapng.py
```

Keluarannya:

```
file          : .../lab02_export_object.pcapng
paket         : 59
ukuran        : 19480 byte
domain jahat  : arsip-nilai.free-hosting-murah.tk
domain exfil  : ZG9rdW1lbi1yYWhhc2lh.exfil.free-hosting-murah.tk
  label base64: ZG9rdW1lbi1yYWhhc2lh  ->  dokumen-rahasia
FLAG          : JCC{DNS_B0C0R_G4MB4R_T3RB4C4}

  logo-sekolah.png            1405 byte  md5=79867e8f...
  daftar-hadir-rapat.pdf       817 byte  md5=0997eb1c...
  bocoran-soal-un-2026.png    6476 byte  md5=ea6262fd...
```

Untuk melihat gambar berisi flag tanpa membuka Wireshark:

```bash
python3 generate_pcapng.py --preview
```

Perintah itu menulis `_preview-bocoran.png` di folder yang sama. **Hapus berkas itu sebelum folder dibagikan ke siswa.**

## C.2 Membuat Varian Soal Baru

Ubah baris di bagian atas skrip, lalu jalankan ulang. Skrip menghitung ulang `Content-Length`, seluruh checksum IP dan TCP, serta pemotongan segmen secara otomatis.

| Variabel | Baris | Efek perubahan |
|---|---|---|
| `FLAG` | ~30 | teks yang tergambar di dalam PNG |
| `BAD_HOST` | ~32 | nama domain mencurigakan |
| `EXFIL_LABEL` | ~33 | teks yang di-Base64 menjadi label domain |
| `IP_BAD` | ~38 | alamat server asing |
| `IP_CLIENT` | ~35 | alamat workstation tersangka |
| `MSS` | ~44 | ukuran potongan, kecilkan ke 512 agar segmennya lebih banyak |

> **Perhatian pada FLAG.** Skrip menggambar teks memakai font bitmap 5x7 buatan sendiri yang hanya memuat huruf besar, angka, dan simbol `{ } _ - . , : / ( ) ! #`. Huruf kecil otomatis digambar sebagai huruf besar. Kalau kalian membuat flag baru, tulis dengan huruf besar semua supaya gambar dan teks jawaban tetap konsisten.

Setelah membuat varian, verifikasi dengan membuka hasilnya di Wireshark dan memastikan menu Export Objects menampilkan lima baris.

## C.3 Alternatif 1: Membuat Berkas dengan Scapy

Kalau laptop pengajar sudah memiliki scapy (`pip install scapy`) dan kalian lebih nyaman dengan pustaka itu, potongan berikut membangun sesi HTTP berisi PNG. Pendekatannya sama, hanya penyusunan paketnya yang berbeda.

```python
#!/usr/bin/env python3
"""Alternatif ringkas memakai scapy. Butuh: pip install scapy"""
from scapy.all import Ether, IP, TCP, wrpcap

CLIENT, SERVER = "192.168.10.44", "185.220.101.47"
MAC_C, MAC_S = "08:00:27:9f:8e:21", "00:1c:42:a1:b2:c3"
SPORT, MSS = 51402, 1460

png = open("bocoran-soal-un-2026.png", "rb").read()
req = (f"GET /arsip/bocoran-soal-un-2026.png HTTP/1.1\r\n"
       f"Host: arsip-nilai.free-hosting-murah.tk\r\n"
       f"User-Agent: Mozilla/5.0\r\n\r\n").encode()
resp_head = (f"HTTP/1.1 200 OK\r\n"
             f"Content-Type: image/png\r\n"
             f"Content-Length: {len(png)}\r\n\r\n").encode()

pkts = []
cseq, sseq = 1000, 5000

def c2s(flags, payload=b""):
    global cseq
    p = (Ether(src=MAC_C, dst=MAC_S) / IP(src=CLIENT, dst=SERVER) /
         TCP(sport=SPORT, dport=80, flags=flags, seq=cseq, ack=sseq) / payload)
    cseq += len(payload) + (1 if "S" in flags or "F" in flags else 0)
    pkts.append(p)

def s2c(flags, payload=b""):
    global sseq
    p = (Ether(src=MAC_S, dst=MAC_C) / IP(src=SERVER, dst=CLIENT) /
         TCP(sport=80, dport=SPORT, flags=flags, seq=sseq, ack=cseq) / payload)
    sseq += len(payload) + (1 if "S" in flags or "F" in flags else 0)
    pkts.append(p)

c2s("S"); s2c("SA"); c2s("A")
c2s("PA", req)
body = resp_head + png
for i in range(0, len(body), MSS):
    chunk = body[i:i + MSS]
    s2c("PA" if i + MSS >= len(body) else "A", chunk)
    c2s("A")
c2s("FA"); s2c("A"); s2c("FA"); c2s("A")

wrpcap("lab02_scapy.pcap", pkts)
print(f"selesai, {len(pkts)} paket")
```

Scapy menghitung ulang checksum sendiri saat menulis berkas, jadi kalian tidak perlu mengurusnya. Kekurangannya: scapy harus terpasang, dan versi lama kadang bermasalah dengan pcapng.

## C.4 Alternatif 2: Menangkap Sendiri dari Server Lokal

Cara ini paling mendekati kenyataan dan bagus dipakai kalau kalian ingin siswa melihat proses penangkapan paket secara langsung, bukan sekadar membuka berkas jadi.

**Langkah 1.** Siapkan folder berisi berkas yang akan diunduh:

```bash
mkdir -p /tmp/lab02-server/arsip
cd lab02 && python3 generate_pcapng.py --preview
cp _preview-bocoran.png /tmp/lab02-server/arsip/bocoran-soal-un-2026.png
```

**Langkah 2.** Jalankan server HTTP bawaan Python di satu terminal:

```bash
cd /tmp/lab02-server && python3 -m http.server 8080
```

**Langkah 3.** Mulai menangkap paket di terminal lain, pada interface loopback:

```bash
sudo tcpdump -i lo -w lab02-live.pcap 'tcp port 8080'
```

**Langkah 4.** Unduh berkasnya dari terminal ketiga:

```bash
curl -s http://127.0.0.1:8080/arsip/bocoran-soal-un-2026.png -o /dev/null
```

**Langkah 5.** Hentikan tcpdump dengan `Ctrl+C`, lalu buka `lab02-live.pcap` di Wireshark.

> **Catatan penting untuk cara ini.** Interface loopback memakai MTU besar (65.536 byte), jadi berkas kalian mungkin terkirim dalam satu segmen raksasa dan pelajaran tentang reassembly justru hilang. Kalau ingin memaksa pemotongan, turunkan MTU sementara:
> ```bash
> sudo ip link set dev lo mtu 1500     # kembalikan ke 65536 setelah selesai
> ```
> Cara ini juga tidak menghasilkan lalu lintas DNS, sehingga Bagian A tidak bisa dilatih. Gunakan skrip generator untuk lab utama, dan cara ini sebagai demonstrasi tambahan kalau waktu masih tersisa.

## C.5 Daftar Periksa Sebelum Lab Dimulai

```
[ ] Wireshark 4.0+ terpasang di kedua laptop siswa
[ ] Edit > Preferences > Protocols > TCP > reassembly tercentang
[ ] lab02_export_object.pcapng tersalin, ukuran 19.480 byte
[ ] Folder Ekstraksi-LAB02 sudah dibuat di Desktop masing-masing
[ ] Berkas _preview-bocoran.png SUDAH DIHAPUS dari folder siswa
[ ] Lampiran B (kunci jawaban) tidak ikut tercetak di modul siswa
[ ] prompt-log.md sudah dibuka di text editor sebelum lab mulai
[ ] Akses ke CyberChef atau terminal untuk decoding Base64 tersedia
[ ] Stopwatch atau timer disiapkan untuk menjaga alokasi 60 menit
```

## C.6 Rencana Lanjutan

| Modul | Judul | Fokus |
|---|---|---|
| LAB 01 ✅ | The Wire Sniffer | Sniffing HTTP, Follow TCP Stream |
| LAB 02 ✅ | Needle in a Haystack | Filter lanjutan, DNS tracking, Export Objects |
| LAB 03 | The Hidden Layer | Steganografi, metadata EXIF, berkas dalam berkas |
| LAB 04 | Broken Login | Logika autentikasi web, manipulasi cookie dan JWT |
| LAB 05 | Cipher Playground | Sandi klasik, Base-family, XOR sederhana |
| LAB 06 | Simulasi Penyisihan | 15 soal, 3 jam, write-up wajib |

***

**Selamat berburu. Jarum itu ada di sana, dan kalian sekarang punya magnet.**

*Modul ini disusun untuk pembinaan internal Tim CTF SMK Maskumambang 1, Pondok Pesantren Maskumambang.*
