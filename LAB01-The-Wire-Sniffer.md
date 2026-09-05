# LAB 01: THE WIRE SNIFFER
### Dasar Analisis Paket dengan Wireshark

**Program Pembinaan Tim CTF SMK Maskumambang 1**
Persiapan **Jatim Cybersecurity Competition (JCC) 2026**, kategori SMA/SMK Sederajat
Kelas Sasaran: X (usia 15-16 tahun) | Level: Pemula (Beginner Friendly)
Versi Modul: 1.0 | Tanggal: 05 September 2026

***

## DAFTAR ISI

1. [Informasi Modul & Target Capaian](#bagian-1-informasi-modul-target-capaian)
2. [Briefing Misi & Skenario Dunia Nyata](#bagian-2-briefing-misi-skenario-dunia-nyata)
3. [Konsep Inti (Explain Like I'm 15)](#bagian-3-konsep-inti-explain-like-im-15)
4. [Panduan Praktik Step-by-Step](#bagian-4-panduan-praktik-step-by-step-hands-on-lab)
5. [Panduan Efektif Menggunakan AI & Menulis Prompt](#bagian-5-panduan-efektif-menggunakan-ai-menulis-prompt)
6. [Lembar Kerja Siswa & Template Write-Up](#bagian-6-lembar-kerja-siswa-template-write-up)
7. [Lampiran: Kartu Contekan & Kunci Jawaban Pembina](#lampiran-a-kartu-contekan-cheat-sheet)

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# BAGIAN 1: INFORMASI MODUL & TARGET CAPAIAN

## 1.1 Identitas Modul

| Item | Keterangan |
|---|---|
| **Kode Modul** | LAB-01 / FORENSICS-NET |
| **Judul** | The Wire Sniffer: Dasar Analisis Paket dengan Wireshark |
| **Kategori CTF** | Forensics / Network Traffic Analysis |
| **Tingkat Kesulitan** | ★☆☆☆☆ (Easy, soal pembuka babak penyisihan) |
| **Metode** | Praktik mandiri berpasangan, 1 laptop per siswa |
| **Jumlah Peserta** | 2 siswa (1 tim JCC) |
| **File Latihan** | `lab01/lab01-wire-sniffer.pcap` (44 paket, 9.202 byte) |

## 1.2 Alokasi Waktu (Total 45-60 Menit)

| Sesi | Kegiatan | Durasi | Penanggung Jawab |
|---|---|---|---|
| **Sesi 0** | Persiapan alat, salin file `.pcap` ke laptop | 5 menit | Siswa |
| **Sesi 1** | Briefing misi + konsep inti (Bagian 2 & 3) | 10 menit | Pembina |
| **Sesi 2** | Praktik hands-on lab (Bagian 4, Langkah 1-7) | 20-25 menit | Siswa |
| **Sesi 3** | Latihan prompt AI + decoding flag bonus (Bagian 5) | 8 menit | Siswa |
| **Sesi 4** | Mengisi lembar kerja + menyusun write-up (Bagian 6) | 8-10 menit | Siswa |
| **Sesi 5** | Diskusi, koreksi, tanya jawab | 5 menit | Pembina |

> **Catatan pembina:** kalau siswa baru pertama kali membuka Wireshark, tambahkan 10 menit di Sesi 2. Jangan potong Sesi 4. Kemampuan menulis write-up menyumbang nilai di JCC 2026.

## 1.3 Prasyarat Alat

Siapkan semuanya **sebelum** jam praktik dimulai. Instalasi di tengah lab membuang waktu.

| Alat | Versi Minimum | Sumber Unduh | Cek Kesiapan |
|---|---|---|---|
| **Wireshark** | 4.0 ke atas | wireshark.org/download | Buka aplikasi, muncul daftar interface jaringan |
| **Browser** | Chrome / Firefox terbaru | bawaan laptop | Bisa membuka situs apa pun |
| **Text Editor** | VS Code / Notepad++ / Notepad | code.visualstudio.com | Bisa membuat file `.md` atau `.txt` |
| **Akun Chatbot AI** | ChatGPT atau Claude | chat.openai.com / claude.ai | Bisa mengirim satu pesan uji |
| **File latihan** | `lab01-wire-sniffer.pcap` | folder `lab01/` | Ukuran file 9.202 byte |

**Catatan instalasi Wireshark:**
- **Windows:** saat instalasi, centang **Npcap** ketika installer menawarkannya. Tanpa Npcap, Wireshark tetap bisa membuka file `.pcap` (itu yang lab ini butuhkan), tetapi tidak bisa menangkap paket langsung.
- **Linux (Ubuntu/Debian):** `sudo apt install wireshark`, lalu jawab **Yes** pada pertanyaan "non-superusers capture packets".
- **macOS:** pasang lewat installer resmi, izinkan **ChmodBPF** saat diminta.

## 1.4 Tujuan Pembelajaran (Learning Outcomes)

Setelah menyelesaikan modul ini, siswa mampu:

| Kode | Rumusan Capaian (terukur) | Bukti Ketercapaian |
|---|---|---|
| **LO-1** | Menjelaskan perbedaan HTTP dan HTTPS beserta konsekuensi keamanannya menggunakan analogi kartu pos dan kotak surat terkunci, tanpa membuka catatan. | Jawaban benar pada Pertanyaan Konseptual nomor 1 |
| **LO-2** | Membuka file `.pcap` di Wireshark dan menerapkan minimal 3 display filter berbeda (`http`, `ip.addr`, `frame contains`) dengan hasil filter yang tepat. | Tangkapan layar 3 filter di lembar kerja |
| **LO-3** | Mengekstraksi kredensial plaintext (username dan password) dari lalu lintas HTTP menggunakan fitur Follow TCP Stream dalam waktu kurang dari 8 menit. | Kolom "Kredensial Bocor" pada Tabel Temuan terisi benar |
| **LO-4** | Menemukan flag berformat `JCC{...}` menggunakan fitur pencarian string (Ctrl+F) pada mode *Packet bytes*. | Flag utama tercatat lengkap dan benar |
| **LO-5** | Melakukan decoding string Base64 dan menjelaskan alasan data tersebut dicurigai sebagai Base64. | Flag bonus tercatat + alasan tertulis di write-up |
| **LO-6** | Menyusun write-up sesuai format panitia JCC 2026, termasuk lampiran riwayat prompt AI dan alur penalaran tim. | Dokumen write-up lengkap 6 bagian |

## 1.5 Aturan Main (Wajib Dibaca)

> ### ⚠️ ETIKA DAN BATASAN
>
> 1. **Semua data di file latihan ini buatan.** IP, nama server, dan kredensial dibuat khusus untuk latihan. Tidak ada sistem nyata yang tersentuh.
> 2. **Dilarang menyadap jaringan sekolah, warnet, atau WiFi publik.** Menangkap paket milik orang lain tanpa izin tertulis melanggar UU ITE Pasal 31. Ancamannya pidana, bukan sekadar teguran guru.
> 3. **Kalau ingin berlatih menangkap paket langsung**, pakai jaringan lab yang sudah diizinkan pembina, atau pakai laptop sendiri di hotspot pribadi.
> 4. **Aturan JCC 2026:** automated scanner (sqlmap, Burp Scanner, dirb, nikto, dan sejenisnya) **dilarang keras**. Modul ini sengaja melatih teknik manual, jadi kalian aman dan tetap tajam.
> 5. **Aturan AI di JCC 2026:** chatbot boleh dipakai, dengan syarat seluruh riwayat prompt dan alur penalaran dilampirkan di write-up resmi. Catat sejak prompt pertama, bukan setelah selesai.

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# BAGIAN 2: BRIEFING MISI & SKENARIO DUNIA NYATA

## 2.1 Situasi

```
=====================================================================
  LAPORAN INSIDEN #2026-0225-01            KLASIFIKASI: INTERNAL
  Unit Teknologi Informasi, SMK Maskumambang 1
  Waktu kejadian : Rabu, 25 Februari 2026, 13:13 WIB
  Pelapor        : Wali Kelas XII TKJ 2
=====================================================================
```

Rabu siang, ruang guru gaduh.

Nilai rapor sementara di **Portal Nilai** berubah sendiri. Tiga siswa yang seharusnya mendapat 70-an tiba-tiba tercatat 90-an. Wali kelas bersumpah tidak menyentuh angka itu sejak Senin. Kepala sekolah minta jawaban sebelum jam pulang.

Portal Nilai berjalan di server lab, alamatnya `portal-nilai.smkmaska.local`. Server itu dipasang tahun 2019 oleh alumni, dan sejak itu tidak pernah diperbarui. Portal masih melayani halaman lewat **HTTP polos** di port 80, tanpa gembok hijau di browser.

Beruntung, teknisi lab memasang perekam lalu lintas di switch utama sejak awal semester. Rekaman siang itu tersimpan sebagai `lab01-wire-sniffer.pcap`, berisi **44 paket** data mentah. Semua yang lewat kabel siang itu ada di dalamnya.

Kepala sekolah menunjuk kalian, tim CTF sekolah, sebagai investigator pertama.

## 2.2 Misi Kalian

Bongkar rekaman itu dan jawab lima pertanyaan berikut:

| # | Pertanyaan Investigasi | Nilai |
|---|---|---|
| **M1** | Alamat IP mana yang berhasil masuk ke halaman admin portal? | 15 poin |
| **M2** | Username dan password apa yang melintas di kabel dalam bentuk polos? | 25 poin |
| **M3** | Ada satu percobaan login yang gagal. Dari IP mana, dan apa buktinya gagal? | 15 poin |
| **M4** | Temukan **FLAG UTAMA** yang tertinggal di dalam halaman yang diakses penyusup. | 30 poin |
| **M5** | Temukan **FLAG BONUS** yang disamarkan di salah satu header respons server. | 15 poin |

## 2.3 Format Flag

Flag di JCC 2026 selalu berbentuk:

```
JCC{teks_tanpa_spasi_pakai_garis_bawah}
```

Aturan penulisan flag:
- Salin **persis** apa yang kalian lihat, termasuk huruf besar-kecil dan angka.
- Sertakan kurung kurawal `{` dan `}`.
- Jangan menambah spasi di depan atau belakang.
- Kalau flag berisi `1` dan `l`, `0` dan `O`, perbesar tampilan sebelum menyalin. Satu karakter salah berarti nol poin.

> 💡 **Trik tim juara:** jangan pernah mengetik ulang flag. Blok teksnya di Wireshark, tekan `Ctrl+C`, lalu tempel langsung ke kolom jawaban.

## 2.4 Peta Jaringan TKP

```
                     SMK MASKUMAMBANG 1 - LAB JARINGAN
                            192.168.10.0/24

   [Laptop A]                                            [Laptop B]
 192.168.10.37                                        192.168.10.52
 MAC 08:00:27:1a:2b:3c                          MAC 08:00:27:4d:5e:6f
       |                                                    |
       |                 +--------------+                   |
       +---------------->|   SWITCH     |<------------------+
                         |  (perekam    |
                         |   dipasang   |
                         |   di sini)   |
                         +------+-------+
                                |
                +---------------+---------------+
                |                               |
     [Server Portal Nilai]             [Gateway / Router]
        192.168.10.10                     192.168.10.1
        HTTP port 80                    (jalan ke internet)
   portal-nilai.smkmaska.local
```

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# BAGIAN 3: KONSEP INTI (EXPLAIN LIKE I'M 15)

## 3.1 Paket Data: Surat yang Dipotong-potong

Bayangkan kalian mengirim buku setebal 300 halaman lewat pos, tetapi kantor pos hanya menerima amplop tipis isi 3 halaman.

Solusinya: potong buku itu jadi 100 amplop, tulis nomor urut di tiap amplop, kirim semuanya, lalu penerima menyusun ulang sesuai nomor.

Jaringan komputer bekerja persis seperti itu. Data besar dipotong menjadi potongan kecil bernama **paket**. Setiap paket membawa tiga hal:

| Bagian Paket | Analogi Amplop | Isinya |
|---|---|---|
| **Header** | Tulisan di luar amplop | Alamat pengirim (IP asal), alamat tujuan (IP tujuan), nomor urut |
| **Payload** | Kertas di dalam amplop | Isi sebenarnya: teks, gambar, password, apa saja |
| **Trailer / Checksum** | Segel keaslian | Penanda supaya penerima tahu paket rusak di jalan atau tidak |

Sekarang bagian pentingnya. Di jaringan lokal, semua amplop itu **lewat satu jalan yang sama**: kabel dan switch. Siapa pun yang duduk di jalur itu dengan alat perekam bisa memfoto setiap amplop yang lewat.

Wireshark adalah alat perekam sekaligus kaca pembesarnya.

## 3.2 HTTP vs HTTPS: Kartu Pos vs Kotak Surat Terkunci

Ini konsep terpenting di modul ini. Baca pelan-pelan.

### 🟥 HTTP = KARTU POS

```
   +-----------------------------------------------+
   |  KARTU POS                        [ perangko ] |
   |                                                |
   |  Kepada: Portal Nilai (192.168.10.10)          |
   |  Dari  : Laptop A (192.168.10.37)              |
   |                                                |
   |  "Halo, username saya admin_nilai,             |
   |   password saya Sup3rR4h4s1a_2026,             |
   |   tolong bukakan halaman nilai ya."            |
   |                                                |
   +-----------------------------------------------+
        ^                    ^                  ^
        |                    |                  |
    tukang pos          petugas sortir      tetangga
    membacanya          membacanya          membacanya
```

Kartu pos tidak punya amplop. Tulisannya terbuka. **Setiap orang yang memegangnya bisa membaca isinya**, dan tidak ada yang tahu siapa saja sudah membaca.

Begitulah HTTP. Password yang kalian ketik melintas di kabel sebagai teks biasa, terbaca utuh oleh siapa pun yang merekam jalur itu.

### 🟩 HTTPS = KOTAK SURAT BAJA BERGEMBOK

```
   +-----------------------------------------------+
   |  [==] KOTAK BAJA TERKUNCI          [ gembok ]  |
   |                                                |
   |  Kepada: mail.smkmaska.sch.id                  |
   |  Dari  : Laptop A                              |
   |                                                |
   |  isi: 7f a3 91 0c bb 4e 22 d8 6a 1f 05 e9      |
   |       c4 77 30 8b 2d 19 f6 aa 51 3c 90 e2      |
   |       (acak total, tidak terbaca)              |
   |                                                |
   +-----------------------------------------------+
        ^
        |
   tukang pos hanya tahu KOTAKNYA dikirim ke mana,
   tetapi tidak bisa membuka isinya
```

HTTPS membungkus isi kartu pos ke dalam kotak baja, lalu menguncinya dengan gembok yang kuncinya cuma dimiliki pengirim dan penerima. Perekam di tengah jalur tetap melihat kotak itu lewat, tetapi isinya berupa karakter acak.

### Tabel Perbandingan

| Aspek | HTTP (port 80) | HTTPS (port 443) |
|---|---|---|
| Tampilan di browser | Tulisan "Not secure" | Gembok tertutup |
| Isi paket di Wireshark | Terbaca sebagai teks biasa | Tampil sebagai `Application Data` acak |
| Password saat dikirim | Terlihat utuh | Terenkripsi |
| Yang tetap terlihat penyadap | Semuanya | Alamat IP, nama domain, ukuran data |
| Protokol di kolom Protocol | `HTTP` | `TLSv1.2` / `TLSv1.3` |

> ### 🎯 Inti yang harus nempel di kepala
> HTTPS tidak menyembunyikan **ke mana** kalian pergi. HTTPS menyembunyikan **apa** yang kalian bawa.
> Penyadap tetap tahu kalian membuka `mail.smkmaska.sch.id`, tetapi tidak tahu isi email kalian.

Di file latihan nanti, kalian akan melihat kedua jenis lalu lintas ini berdampingan. Rasakan sendiri bedanya.

## 3.3 Tiga Filter Dasar Wireshark

File `.pcap` berisi 44 paket. File asli di kompetisi bisa berisi 40.000 paket. Membaca satu per satu mustahil. Filter adalah cara menyuruh Wireshark menyembunyikan yang tidak relevan.

Ketik filter di **kotak panjang paling atas** jendela Wireshark (bertuliskan `Apply a display filter … <Ctrl-/>`), lalu tekan `Enter`.

> **Penanda warna kotak filter:**
> 🟩 **hijau** = sintaks benar, siap dijalankan
> 🟨 **kuning** = jalan, tetapi hasilnya mungkin tidak seperti dugaan kalian
> 🟥 **merah** = sintaks salah, perbaiki dulu sebelum menekan Enter

### Filter #1: `http`

```
http
```

**Fungsi:** menampilkan hanya paket yang berisi permintaan dan jawaban HTTP.
**Analogi:** menyuruh petugas pos menyisihkan semua kartu pos, buang sisanya.
**Dipakai saat:** kalian mencari halaman web, form login, atau data yang dikirim tanpa enkripsi.

Variasi yang berguna:

| Filter | Artinya |
|---|---|
| `http.request` | hanya permintaan dari klien ke server |
| `http.response` | hanya jawaban dari server ke klien |
| `http.request.method == "POST"` | hanya pengiriman form, tempat password biasanya lewat |
| `http.response.code == 200` | hanya jawaban sukses |

### Filter #2: `ip.addr == 192.168.10.37`

```
ip.addr == 192.168.10.37
```

**Fungsi:** menampilkan semua paket yang melibatkan satu komputer, baik sebagai pengirim maupun penerima.
**Analogi:** menyuruh petugas pos mengeluarkan semua surat yang berhubungan dengan satu rumah.
**Dipakai saat:** kalian sudah mencurigai satu perangkat dan ingin melihat seluruh aktivitasnya.

Variasi yang berguna:

| Filter | Artinya |
|---|---|
| `ip.src == 192.168.10.37` | hanya paket yang **dikirim** komputer itu |
| `ip.dst == 192.168.10.10` | hanya paket yang **menuju** server itu |
| `tcp.port == 80` | hanya lalu lintas di port 80 (HTTP) |
| `ip.addr == 192.168.10.37 && http` | gabungan dua syarat, pakai `&&` untuk "dan" |

### Filter #3: `frame contains "JCC"`

```
frame contains "JCC"
```

**Fungsi:** menampilkan paket mana pun yang di dalamnya mengandung teks `JCC`, di bagian mana pun.
**Analogi:** menyuruh petugas pos membaca semua surat dan menyisihkan yang menyebut satu kata tertentu.
**Dipakai saat:** kalian berburu flag, kata kunci, nama file, atau potongan kalimat.

> ⚠️ **Peringatan huruf besar-kecil:** `frame contains` bersifat **case sensitive**. `frame contains "jcc"` tidak akan menemukan `JCC`. Kalau ragu, pakai versi tidak peduli huruf besar-kecil:
> ```
> frame matches "(?i)jcc"
> ```

### Ringkasan Tiga Filter

| Filter | Pertanyaan yang dijawab | Kapan dipakai |
|---|---|---|
| `http` | "Apa saja lalu lintas web polos di sini?" | Awal investigasi, memetakan kejadian |
| `ip.addr == x.x.x.x` | "Apa saja yang dilakukan komputer ini?" | Setelah punya tersangka |
| `frame contains "..."` | "Di paket mana kata ini muncul?" | Berburu flag atau kata kunci |

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# BAGIAN 4: PANDUAN PRAKTIK STEP-BY-STEP (HANDS-ON LAB)

> **Cara membaca bagian ini:** setiap langkah punya kotak ✅ **CEK KEBERHASILAN**. Jangan lanjut ke langkah berikutnya sebelum kotak itu cocok dengan layar kalian. Kalau tidak cocok, baca kotak 🔧 **KALAU MACET** di bawahnya.

***

## LANGKAH 1: Membuka File Rekaman

1. Buka aplikasi **Wireshark**.
2. Pada menu bar paling atas, klik **File** → **Open**. Pintasannya `Ctrl + O`.
3. Arahkan ke folder `lab01/`, pilih file **`lab01-wire-sniffer.pcap`**, klik **Open**.

> ✅ **CEK KEBERHASILAN**
> Layar kalian terbagi tiga panel bertumpuk:
> - **Panel atas (Packet List):** tabel berisi **44 baris**, berkolom `No.`, `Time`, `Source`, `Destination`, `Protocol`, `Length`, `Info`.
> - **Panel tengah (Packet Details):** pohon lipatan berisi `Frame`, `Ethernet II`, `Internet Protocol Version 4`, dan seterusnya.
> - **Panel bawah (Packet Bytes):** deretan angka heksadesimal di kiri, teks di kanan.
>
> Baris nomor 1 dan 2 berprotokol **DNS**. Di kolom `Info` baris 1 tertulis `Standard query ... A portal-nilai.smkmaska.local`.

> 🔧 **KALAU MACET**
> - Panel bawah tidak muncul: klik menu **View**, pastikan **Packet Bytes** tercentang.
> - Jumlah baris bukan 44: kemungkinan masih ada filter tersisa dari percobaan sebelumnya. Kosongkan kotak filter, tekan `Enter`.
> - File tidak bisa dibuka: cek ukuran file harus 9.202 byte. Kalau berbeda, salin ulang dari folder pembina.

**Sekilas isi paket 1 dan 2:** laptop bertanya ke server DNS `192.168.10.1`, "berapa alamat IP `portal-nilai.smkmaska.local`?", dan dijawab `192.168.10.10`. Catat alamat itu, karena server itulah TKP kalian.

***

## LANGKAH 2: Memfilter Lalu Lintas HTTP

1. Klik satu kali di **kotak filter** paling atas (tulisan abu-abu `Apply a display filter … <Ctrl-/>`).
2. Ketik:
   ```
   http
   ```
3. Perhatikan kotak berubah **hijau**, lalu tekan `Enter`.

> ✅ **CEK KEBERHASILAN**
> Daftar paket menyusut menjadi **10 baris**. Kolom `Protocol` semuanya bertuliskan `HTTP`. Di pojok kanan bawah jendela Wireshark muncul keterangan `Displayed: 10 (22.7%)`.
>
> Kolom `Info` menampilkan barisan seperti ini:
>
> | No. | Source | Destination | Info |
> |---|---|---|---|
> | 6 | 192.168.10.52 | 192.168.10.10 | `POST /login.php HTTP/1.1 (application/x-www-form-urlencoded)` |
> | 7 | 192.168.10.10 | 192.168.10.52 | `HTTP/1.1 401 Unauthorized (text/html)` |
> | 16 | 192.168.10.37 | 192.168.10.10 | `POST /login.php HTTP/1.1 (application/x-www-form-urlencoded)` |
> | 17 | 192.168.10.10 | 192.168.10.37 | `HTTP/1.1 302 Found` |
> | 19 | 192.168.10.37 | 192.168.10.10 | `GET /dashboard.php HTTP/1.1` |
> | 20 | 192.168.10.10 | 192.168.10.37 | `HTTP/1.1 200 OK (text/html)` |

> 🔧 **KALAU MACET**
> - Kotak filter merah: kalian mungkin mengetik `HTTP` huruf besar atau menambah spasi. Nama filter selalu huruf kecil.
> - Hasil 0 baris: hapus isi kotak, tekan `Enter`, lalu ketik ulang perlahan.

**🔍 Analisis cepat.** Dua komputer mencoba masuk ke `/login.php`. Server menjawab dengan kode berbeda:

| Kode | Arti | Kesimpulan |
|---|---|---|
| **401 Unauthorized** | server menolak | login dari `192.168.10.52` **gagal** |
| **302 Found** | server mengalihkan ke halaman lain | login dari `192.168.10.37` **berhasil** |

Tersangka utama kalian: **192.168.10.37**. Catat di lembar kerja sekarang juga.

***

## LANGKAH 3: Menyaring Percobaan Login Saja

Untuk memastikan tidak ada percobaan login lain yang terlewat, persempit filternya.

1. Kosongkan kotak filter, lalu ketik:
   ```
   http.request.method == "POST"
   ```
2. Tekan `Enter`.

> ✅ **CEK KEBERHASILAN**
> Tersisa **2 baris**: paket **6** (dari `192.168.10.52`) dan paket **16** (dari `192.168.10.37`). Hanya dua percobaan login sepanjang rekaman.

> 🔧 **KALAU MACET**
> Tanda kutip harus lurus (`"`), bukan kutip melengkung hasil salin-tempel dari Word. Ketik manual kalau ragu.

***

## LANGKAH 4: Follow TCP Stream, Membaca Kartu Pos Utuh

Satu percakapan HTTP sering terpecah ke banyak paket. **Follow TCP Stream** menyusun ulang potongan itu menjadi satu halaman percakapan yang enak dibaca.

1. Klik **satu kali** pada baris paket **nomor 16** (POST dari `192.168.10.37`) sampai barisnya tersorot.
2. **Klik kanan** pada baris itu.
3. Pilih **Follow** → **TCP Stream**.
   Pintasan keyboard: `Ctrl + Alt + Shift + T`.
   Lewat menu bar: **Analyze** → **Follow** → **TCP Stream**.

Sebuah jendela baru terbuka berjudul `Follow TCP Stream (tcp.stream eq 1)`.

> ✅ **CEK KEBERHASILAN**
> Isi jendela berwarna dua rupa:
> - **Teks merah** = dikirim laptop ke server (permintaan)
> - **Teks biru** = dikirim server ke laptop (jawaban)
>
> Di blok merah paling atas kalian membaca:
>
> ```
> POST /login.php HTTP/1.1
> Host: portal-nilai.smkmaska.local
> User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) ...
> Content-Type: application/x-www-form-urlencoded
> Content-Length: 59
> Origin: http://portal-nilai.smkmaska.local
> Referer: http://portal-nilai.smkmaska.local/login.php
> Connection: keep-alive
>
> username=admin_nilai&password=Sup3rR4h4s1a_2026&remember=on
> ```

**🚨 Di situlah kartu posnya terbaca.** Baris terakhir memuat kredensial lengkap, terkirim polos tanpa enkripsi:

| Field | Nilai |
|---|---|
| `username` | `admin_nilai` |
| `password` | `Sup3rR4h4s1a_2026` |

Password itu terlihat rumit dan panjang. Tetap saja bocor, karena kekuatan password tidak menolong sedikit pun ketika saluran pengirimannya polos. Tulis kalimat itu di write-up kalian, penguji suka analisis semacam ini.

**Gulir terus ke bawah** di jendela yang sama. Di blok biru berikutnya, server menjawab:

```
HTTP/1.1 302 Found
Date: Wed, 25 Feb 2026 06:13:20 GMT
Server: Apache/2.4.57 (Debian)
X-Powered-By: PHP/8.2.12
Set-Cookie: PHPSESSID=b7f4c02e9ad13c5e88a1; path=/
Location: /dashboard.php
X-Debug-Note: SkNDe2h0dHBfMXR1X2s0cnR1X3Awc30=
Cache-Control: no-store
```

Berhenti sejenak di baris **`X-Debug-Note`**. Header itu tidak ada di daftar header HTTP standar mana pun, dan isinya deretan huruf acak berakhiran `=`. Simpan string itu, kalian akan membongkarnya di Bagian 5.

> 🔧 **KALAU MACET**
> - Menu **Follow** tidak muncul: kalian mengklik kanan di panel tengah atau bawah. Klik kanan harus di **panel atas** (daftar paket).
> - Teks tampil sebagai simbol aneh: di jendela Follow, ubah dropdown `Show data as` di bagian bawah menjadi **ASCII**.
> - Ingin lompat ke stream lain: pakai kotak `Stream` di kanan bawah jendela Follow, ubah angkanya. Stream 0 = login gagal, stream 1 = login berhasil.

> ⚠️ **Penting sebelum lanjut**
> Menutup jendela Follow membuat Wireshark otomatis memasang filter `tcp.stream eq 1` di kotak filter. Kosongkan kotak itu dan tekan `Enter` sebelum langkah berikutnya, atau kalian akan bingung karena paket lain menghilang.

***

## LANGKAH 5: Membaca Halaman yang Diakses Penyusup

Setelah login berhasil, penyusup membuka `/dashboard.php`. Isi halaman itu ada di jawaban server, paket nomor 20.

1. Pastikan kotak filter **kosong**, atau ketik ulang `http`, lalu `Enter`.
2. Klik baris paket **nomor 20** (`HTTP/1.1 200 OK`).
3. Klik kanan → **Follow** → **HTTP Stream**.

> ✅ **CEK KEBERHASILAN**
> Muncul isi halaman HTML lengkap di blok biru, termasuk tabel nilai siswa:
>
> ```html
> <h1>Dasbor Wali Kelas</h1>
> <p>Selamat datang, <b>admin_nilai</b>. Terakhir masuk: 25/02/2026 13:13 WIB.</p>
> <table>
>   <tr><th>NIS</th><th>Nama</th><th>Rerata</th></tr>
>   <tr><td>10231</td><td>Nabila R.</td><td>88</td></tr>
>   ...
> ```

**Baca sampai baris paling bawah HTML.** Programmer sering meninggalkan catatan pribadi di komentar HTML (`<!-- ... -->`) dan lupa menghapusnya sebelum rilis. Komentar itu tidak tampil di browser, tetapi terbaca jelas di kode sumber dan di Wireshark.

Di sanalah **FLAG UTAMA** kalian menunggu. Blok teksnya, salin dengan `Ctrl + C`.

***

## LANGKAH 6: Berburu Flag dengan Ctrl+F

Cara di Langkah 5 berhasil karena kalian sudah tahu paket mana yang dicurigai. Di kompetisi, sering kali kalian belum tahu apa-apa. Teknik berikut menyapu seluruh file sekaligus.

1. Kosongkan kotak filter, tekan `Enter`.
2. Tekan `Ctrl + F`. Sebuah **toolbar pencarian** muncul tepat di bawah kotak filter.
3. Atur tiga kotak dropdown di toolbar itu, urut dari kiri:

| Posisi Dropdown | Nilai yang Harus Dipilih | Alasan |
|---|---|---|
| **Kotak 1** (kiri) | **Packet bytes** | menyuruh Wireshark mencari sampai ke isi mentah paket, bukan cuma ringkasan di layar |
| **Kotak 2** (tengah) | **String** | kalian mencari teks, bukan angka heksa atau filter |
| **Kotak 3** (kanan) | **Narrow & Wide** | mencakup teks format biasa maupun format lebar |

4. Kosongkan centang **Case sensitive** kalau kalian tidak yakin huruf besar-kecilnya.
5. Ketik di kolom pencarian:
   ```
   JCC{
   ```
6. Klik tombol **Find** di ujung kanan toolbar, atau tekan `Enter`.

> ✅ **CEK KEBERHASILAN**
> Wireshark melompat ke paket **nomor 20** dan menyorotnya. Di **panel bawah (Packet Bytes)**, potongan teks yang cocok tersorot dengan warna berbeda. Geser panel bawah sampai kalian membaca komentar HTML yang memuat `JCC{...}`.
>
> Tekan `Ctrl + F` lalu **Find** sekali lagi untuk mencari kecocokan berikutnya. Kalau Wireshark tidak menemukan yang lain, artinya hanya ada satu flag dalam bentuk polos.

> 🔧 **KALAU MACET**
> - Muncul pesan `No packet contained that string`: kemungkinan besar Kotak 1 masih di posisi **Packet list**. Ubah ke **Packet bytes**.
> - Toolbar pencarian tidak muncul: klik dulu satu baris paket di panel atas supaya fokus keyboard berada di daftar paket, lalu tekan `Ctrl + F` lagi.

**Cara alternatif (lebih cepat, biasakan juga):** ketik langsung di kotak filter

```
frame contains "JCC{"
```

Hasilnya paket nomor 20 langsung tersaring sendirian. Bandingkan kedua cara ini dan tulis di write-up mana yang kalian pilih beserta alasannya.

***

## LANGKAH 7: Membandingkan dengan Lalu Lintas Terenkripsi

Langkah terakhir ini membuktikan sendiri materi Bagian 3.2. Jangan dilewati.

1. Kosongkan kotak filter, ketik:
   ```
   tls
   ```
2. Tekan `Enter`.
3. Klik paket berprotokol `TLSv1.3` yang di kolom `Info` bertuliskan `Client Hello`.
4. Klik kanan → **Follow** → **TCP Stream**.

> ✅ **CEK KEBERHASILAN**
> Isi jendela Follow berupa **karakter sampah**: titik, simbol acak, huruf tak berpola. Tidak ada satu pun kalimat yang terbaca.
>
> Sekarang balik ke panel tengah (Packet Details) pada paket `Client Hello`, lalu buka lipatan berikut satu per satu dengan mengklik tanda panah:
> ```
> Transport Layer Security
>  └─ TLSv1.3 Record Layer: Handshake Protocol: Client Hello
>      └─ Handshake Protocol: Client Hello
>          └─ Extension: server_name
>              └─ Server Name Indication extension
>                  └─ Server Name: mail.smkmaska.sch.id
> ```

**Inilah pelajarannya.** Kalian tahu laptop `192.168.10.37` menghubungi `mail.smkmaska.sch.id`, tetapi isi percakapannya tertutup rapat. Bandingkan dengan `/login.php` tadi yang passwordnya terbaca telanjang.

Satu perbedaan huruf, `http` versus `https`, memisahkan kartu pos dari kotak baja.

***

## 4.8 Ringkasan Perintah Langkah 1-7

| Langkah | Aksi | Pintasan / Filter |
|---|---|---|
| 1 | Buka file `.pcap` | `Ctrl + O` |
| 2 | Saring lalu lintas web polos | `http` |
| 3 | Saring percobaan login | `http.request.method == "POST"` |
| 4 | Susun ulang percakapan | `Ctrl + Alt + Shift + T` |
| 5 | Baca isi halaman | klik kanan → Follow → HTTP Stream |
| 6 | Buru flag | `Ctrl + F` (mode *Packet bytes* + *String*) |
| 6b | Buru flag lewat filter | `frame contains "JCC{"` |
| 7 | Lihat pembanding terenkripsi | `tls` |

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# BAGIAN 5: PANDUAN EFEKTIF MENGGUNAKAN AI & MENULIS PROMPT

## 5.1 Aturan Panitia JCC 2026

Panitia mengizinkan ChatGPT dan Claude di babak penyisihan dengan satu syarat tegas:

> **Seluruh riwayat prompt dan alur penalaran tim wajib dilampirkan dalam write-up resmi.**

Artinya juri membaca cara kalian berpikir, bukan sekadar flag yang kalian setor. Tim yang menempelkan soal mentah lalu menyalin jawaban AI akan langsung terlihat di lampiran, dan nilai analisisnya jatuh.

## 5.2 Tiga Kesalahan Fatal

| ❌ Kesalahan | Kenapa merugikan kalian |
|---|---|
| **Menempel soal mentah-mentah** | AI tidak melihat file `.pcap` kalian, jadi jawabannya menebak. Riwayat prompt kalian juga memperlihatkan kalian tidak menganalisis apa pun. |
| **Menanyakan "apa flagnya?"** | AI tidak memegang file itu. Kalian membuang menit berharga menunggu jawaban yang mustahil benar. |
| **Menempelkan flag utuh ke chatbot** | Flag adalah jawaban akhir. Menyalinnya keluar sistem berisiko kena diskualifikasi dan tidak ada gunanya. Sensor jadi `JCC{XXXX}` kalau memang perlu dibahas. |

## 5.3 Cara Bertanya yang Benar

Pakai AI sebagai **asisten teori dan penerjemah teknis**, bukan sebagai mesin jawaban. Empat pekerjaan yang cocok dilempar ke AI:

1. Menjelaskan arti sebuah header, kode status, atau istilah asing.
2. Memeriksa apakah sintaks filter Wireshark buatan kalian sudah benar.
3. Menerangkan ciri-ciri sebuah encoding, misalnya Base64, hex, atau ROT13.
4. Merapikan kalimat write-up kalian tanpa mengubah temuan.

Rumus prompt yang bagus punya empat unsur:

```
[PERAN yang AI mainkan] + [KONTEKS situasi kalian] + [PERTANYAAN spesifik] + [FORMAT jawaban yang diinginkan]
```

## 5.4 Template Prompt #1: Menganalisis Header Mencurigakan

Pakai ini saat kalian menemukan header aneh seperti `X-Debug-Note` di Langkah 4.

```text
Kamu adalah mentor CTF untuk siswa SMK pemula.

KONTEKS:
Saya menganalisis file .pcap berisi lalu lintas HTTP di lab jaringan sekolah.
Pada respons server HTTP 302 Found, saya menemukan header non-standar berikut:

    X-Debug-Note: SkNDe2h0dHBfMXR1X2s0cnR1X3Awc30=

PERTANYAAN:
1. Ciri-ciri apa pada nilai header itu yang menandakan jenis encoding tertentu?
2. Encoding apa yang paling mungkin dipakai, dan apa alasan teknisnya?
3. Bagaimana cara mendecode-nya secara manual, baik lewat CyberChef maupun lewat
   perintah terminal Linux?

FORMAT JAWABAN:
Jelaskan langkah penalarannya dulu, baru berikan hasil akhirnya.
Jangan berikan jawaban tanpa penjelasan, saya perlu memahami logikanya untuk write-up.
```

**Kenapa prompt ini bagus:**
- Kalian memberi peran dan tingkat kesulitan, jadi jawaban AI menyesuaikan usia kalian.
- Kalian mengirim **satu potongan data spesifik**, bukan seluruh soal.
- Kalian meminta **penalaran lebih dulu**, dan penalaran itulah yang kalian salin ke kolom "Alur Penalaran" di write-up.
- Kalian minta cara manual, sesuai aturan JCC yang melarang automated tools.

**Yang kalian pelajari dari jawabannya:** string berakhiran `=`, panjangnya kelipatan 4, dan hanya memakai karakter A-Z, a-z, 0-9, `+`, `/`. Itu tanda kuat Base64.

**Decode manual di terminal Linux:**

```bash
echo 'SkNDe2h0dHBfMXR1X2s0cnR1X3Awc30=' | base64 -d
```

**Decode tanpa terminal:** buka `gchq.github.io/CyberChef`, tarik operasi **From Base64** ke panel Recipe, tempel string di kotak Input, hasilnya muncul di kotak Output.

Hasil decode itulah **FLAG BONUS** kalian.

## 5.5 Template Prompt #2: Memverifikasi Logika Filter

Pakai ini saat filter Wireshark kalian tidak memberi hasil sesuai harapan.

```text
Kamu adalah instruktur Wireshark untuk pemula.

KONTEKS:
Saya sedang menganalisis file .pcap latihan berisi 44 paket dari jaringan lokal
192.168.10.0/24. Tujuan saya: menemukan semua paket yang membawa data form login
yang dikirim ke server 192.168.10.10.

FILTER YANG SUDAH SAYA COBA:
    http.request.method == POST
Hasilnya: kotak filter berwarna merah dan tidak ada paket yang tampil.

PERTANYAAN:
1. Bagian mana dari sintaks filter saya yang salah, dan kenapa Wireshark menolaknya?
2. Tulis versi filter yang benar, plus satu versi alternatif yang sekaligus
   membatasi hasilnya hanya ke server tujuan 192.168.10.10.
3. Jelaskan perbedaan display filter dan capture filter dalam 3 kalimat.

FORMAT JAWABAN:
Tabel dua kolom: "Filter" dan "Penjelasan singkat".
Bahasa Indonesia, tanpa istilah teknis yang tidak kamu jelaskan.
```

**Kenapa prompt ini bagus:**
- Kalian melaporkan **apa yang sudah dicoba** dan **gejala errornya**, jadi AI mendiagnosis, bukan menebak.
- Kalian meminta format tabel, sehingga jawabannya bisa langsung masuk ke write-up.
- Kalian menyisipkan satu pertanyaan konsep (nomor 3), jadi sekali bertanya kalian sekaligus belajar.

## 5.6 Disiplin Mencatat Prompt

Buka satu file bernama `prompt-log.md` di text editor **sebelum** lab dimulai. Setiap kali mengirim prompt, catat lima hal ini:

```markdown
### Prompt #1
- Waktu       : 13:24 WIB
- Chatbot     : Claude
- Prompt      : (salin persis yang kalian ketik)
- Inti jawaban: (ringkas 1-2 kalimat)
- Keputusan   : (apa yang tim lakukan setelah membaca jawaban itu)
```

Mencatat sambil jalan memakan 20 detik. Menyusun ulang dari ingatan setelah lomba selesai memakan 20 menit dan hasilnya tetap tidak akurat.

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# BAGIAN 6: LEMBAR KERJA SISWA & TEMPLATE WRITE-UP

## 6.1 Identitas Tim

| Field | Isian |
|---|---|
| Nama Tim | ................................................. |
| Anggota 1 | ................................................. |
| Anggota 2 | ................................................. |
| Asal Sekolah | SMK Maskumambang 1 |
| Tanggal Praktikum | ....... / ....... / 2026 |
| Waktu mulai | ....... : ....... WIB |
| Waktu selesai | ....... : ....... WIB |

## 6.2 Tabel Temuan Bukti

Isi setiap baris berdasarkan pengamatan langsung. Kolom **Nomor Paket** wajib, karena juri memakai kolom itu untuk memverifikasi temuan kalian.

| Kode | Item Bukti | Temuan Kalian | Nomor Paket | Filter / Langkah yang Dipakai |
|---|---|---|---|---|
| **B1** | Nama domain server target | | | |
| **B2** | Alamat IP server target | | | |
| **B3** | IP penyerang (login **berhasil**) | | | |
| **B4** | IP percobaan **gagal** | | | |
| **B5** | Kode status respons untuk login gagal | | | |
| **B6** | Kode status respons untuk login berhasil | | | |
| **B7** | Username yang bocor | | | |
| **B8** | Password yang bocor | | | |
| **B9** | Nilai cookie sesi (`PHPSESSID`) | | | |
| **B10** | Halaman yang diakses setelah login | | | |
| **B11** | Nama header mencurigakan di respons | | | |
| **B12** | Nilai header tersebut (masih ter-encode) | | | |
| **B13** | Jenis encoding yang dipakai | | | |
| **B14** | 🚩 **FLAG UTAMA** | `JCC{` .................................... `}` | | |
| **B15** | 🚩 **FLAG BONUS** | `JCC{` .................................... `}` | | |
| **B16** | Nama domain pada sesi terenkripsi (TLS) | | | |

**Skor mandiri:** ...... dari 100 poin (lihat tabel nilai di bagian 2.2)

## 6.3 Pertanyaan Pemahaman Konseptual

Jawab dengan kalimat kalian sendiri. Menyalin dari modul tidak mendapat nilai.

***

**PERTANYAAN 1 (Bobot 30)**
Password `Sup3rR4h4s1a_2026` panjangnya 17 karakter, memuat huruf besar, huruf kecil, angka, dan simbol. Kriteria password kuat terpenuhi semua. Meski begitu, password itu tetap bocor dalam hitungan detik. Jelaskan penyebabnya menggunakan analogi kartu pos, lalu sebutkan **satu** perubahan di sisi server yang mencegah kebocoran seperti ini.

```
Jawaban:
_________________________________________________________________________

_________________________________________________________________________

_________________________________________________________________________

_________________________________________________________________________
```

***

**PERTANYAAN 2 (Bobot 35)**
Pada Langkah 7 kalian membuka Follow TCP Stream untuk sesi TLS dan hanya menemukan karakter acak. Meski begitu, kalian tetap berhasil membaca nama domain `mail.smkmaska.sch.id` di panel Packet Details.

a. Kenapa nama domain tetap terbaca padahal isi percakapannya terenkripsi?
b. Informasi apa lagi yang masih bisa dikumpulkan penyadap dari sesi HTTPS?
c. Menurut kalian, apakah HTTPS membuat pengguna sepenuhnya anonim? Beri alasan.

```
Jawaban:
_________________________________________________________________________

_________________________________________________________________________

_________________________________________________________________________

_________________________________________________________________________
```

***

**PERTANYAAN 3 (Bobot 35)**
Bandingkan dua cara menemukan flag yang kalian pakai di Langkah 6, yaitu `Ctrl + F` mode *Packet bytes* dan display filter `frame contains "JCC{"`.

a. Jelaskan perbedaan cara kerja keduanya.
b. Pada file berisi 40.000 paket, mana yang kalian pilih lebih dulu? Beri alasan teknis.
c. Kalau flag disamarkan menjadi Base64 sehingga teks `JCC{` tidak muncul utuh, apakah kedua cara itu masih berhasil? Jelaskan, lalu usulkan strategi pengganti.

```
Jawaban:
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

## 6.4 Template Write-Up Resmi JCC 2026

> **Cara pakai:** salin seluruh blok di bawah ini ke text editor, simpan sebagai `writeup-lab01-[namatim].md`, lalu isi setiap bagian. Ekspor ke PDF sebelum mengunggah. Jangan menghapus judul bagian mana pun, meski isinya singkat.

````markdown
# WRITE-UP JCC 2026
## Nama Soal   : LAB 01 - The Wire Sniffer
## Kategori    : Forensics / Network Analysis
## Nama Tim    : ______________________
## Anggota     : 1. ______________________  2. ______________________
## Asal Sekolah: SMK Maskumambang 1
## Tanggal     : ____ / ____ / 2026
## Status      : [ ] Solved   [ ] Unsolved

---

# 1. DESKRIPSI SOAL
(Tulis ulang deskripsi soal dari panitia. Sebutkan nama file yang diberikan
beserta ukurannya.)


# 2. ALAT YANG DIGUNAKAN
| Alat | Versi | Fungsi dalam penyelesaian |
|---|---|---|
| Wireshark | | |
| CyberChef / terminal | | |
| Chatbot AI | | |

Pernyataan kepatuhan:
Tim menyatakan tidak menggunakan automated scanner (sqlmap, Burp Scanner, dirb,
nikto, atau sejenisnya) dalam penyelesaian soal ini. Seluruh analisis dilakukan
secara manual.

Tanda tangan ketua tim: ______________________


# 3. ALUR PENALARAN (REASONING FLOW)
(Tulis urut sesuai kejadian, termasuk langkah yang gagal. Juri menilai proses
berpikir, jadi jangan menyembunyikan jalan buntu.)

## 3.1 Pengamatan awal
- Membuka file .pcap, mencatat jumlah paket total: ____
- Protokol yang muncul (lihat Statistics > Protocol Hierarchy): ____
- Hipotesis awal tim: ____

## 3.2 Penyempitan pencarian
- Filter yang dipakai: ____
- Alasan memilih filter itu: ____
- Hasil yang didapat: ____

## 3.3 Jalan buntu yang sempat ditemui
- Apa yang dicoba: ____
- Kenapa gagal: ____
- Pelajaran yang diambil: ____

## 3.4 Titik terang
- Petunjuk yang mengubah arah investigasi: ____
- Alasan petunjuk itu meyakinkan: ____

## 3.5 Konfirmasi temuan
- Cara tim memastikan flag itu benar: ____


# 4. LANGKAH TEKNIS (STEP-BY-STEP REPRODUCTION)
(Tulis sedetail mungkin sampai orang lain bisa mengulanginya tanpa bertanya.)

**Langkah 1:** ____
> Perintah / filter: `____`
> Hasil: ____
> [Sisipkan tangkapan layar 1]

**Langkah 2:** ____
> Perintah / filter: `____`
> Hasil: ____
> [Sisipkan tangkapan layar 2]

**Langkah 3:** ____
> Perintah / filter: `____`
> Hasil: ____
> [Sisipkan tangkapan layar 3]


# 5. BUKTI TEMUAN
| Item | Nilai | Nomor Paket |
|---|---|---|
| IP asal penyerang | | |
| IP server target | | |
| Username bocor | | |
| Password bocor | | |
| Header mencurigakan | | |

**FLAG UTAMA:**
```
JCC{________________________________}
```

**FLAG BONUS:**
```
JCC{________________________________}
```


# 6. LAMPIRAN RIWAYAT PROMPT AI (WAJIB)
(Salin persis prompt yang tim kirimkan. Jangan dirapikan ulang, jangan diringkas.
Kalau tim tidak memakai AI sama sekali, tulis "Tidak menggunakan AI" dan
kosongkan tabel.)

| No | Waktu | Chatbot | Prompt yang dikirim (lengkap) | Ringkasan jawaban AI | Keputusan tim setelah membaca jawaban |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

## Refleksi penggunaan AI
- Bagian mana yang dikerjakan tim sendiri tanpa bantuan AI:
  ____
- Bagian mana yang terbantu AI, dan seberapa besar bantuannya:
  ____
- Apakah ada jawaban AI yang keliru? Bagaimana tim mengetahuinya?
  ____


# 7. PELAJARAN & MITIGASI
## 7.1 Akar masalah
(Kenapa insiden ini bisa terjadi?)
____

## 7.2 Rekomendasi perbaikan untuk admin server
1. ____
2. ____
3. ____

## 7.3 Refleksi tim
(Apa yang akan tim lakukan berbeda kalau mengerjakan soal serupa besok?)
____

---
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

## A.1 Pintasan Keyboard Wireshark

| Pintasan | Fungsi |
|---|---|
| `Ctrl + O` | Buka file `.pcap` |
| `Ctrl + /` | Lompat ke kotak display filter |
| `Ctrl + F` | Buka toolbar pencarian |
| `Ctrl + N` | Cari kecocokan berikutnya |
| `Ctrl + Alt + Shift + T` | Follow TCP Stream |
| `Ctrl + Alt + Shift + H` | Follow HTTP Stream |
| `Ctrl + G` | Lompat ke nomor paket tertentu |
| `Ctrl + →` | Buka semua lipatan di Packet Details |
| `Ctrl + ←` | Tutup semua lipatan |
| `Ctrl + Shift + X` | Ubah tampilan Packet Bytes ke ASCII |

## A.2 Filter yang Sering Dipakai di CTF

| Filter | Fungsi |
|---|---|
| `http` | semua lalu lintas HTTP |
| `http.request` | permintaan dari klien saja |
| `http.request.method == "POST"` | pengiriman form, tempat kredensial lewat |
| `http.response.code == 200` | halaman yang berhasil dimuat |
| `http.cookie` | paket yang membawa cookie |
| `ip.addr == 192.168.10.37` | semua lalu lintas satu perangkat |
| `ip.src == 192.168.10.37` | paket yang dikirim perangkat itu |
| `tcp.port == 80` | lalu lintas port 80 |
| `tcp.stream eq 1` | satu percakapan TCP utuh |
| `dns` | permintaan penerjemahan nama domain |
| `tls.handshake.type == 1` | paket Client Hello, memperlihatkan nama domain HTTPS |
| `frame contains "JCC"` | paket yang memuat teks tertentu (peka huruf besar-kecil) |
| `frame matches "(?i)flag"` | pencarian teks tanpa peduli huruf besar-kecil |
| `ftp \|\| telnet \|\| pop \|\| imap` | protokol lain yang mengirim password polos |

## A.3 Menu Statistik yang Menghemat Waktu

| Menu | Kegunaan |
|---|---|
| **Statistics → Protocol Hierarchy** | melihat komposisi protokol dalam satu layar |
| **Statistics → Conversations** | daftar semua pasangan IP yang saling bicara |
| **Statistics → Endpoints** | daftar semua perangkat di rekaman |
| **File → Export Objects → HTTP** | menarik keluar file, gambar, dan halaman yang lewat HTTP |
| **View → Time Display Format → Time of Day** | mengubah kolom Time menjadi jam nyata |

## A.4 Mengenali Jenis Encoding dengan Mata Telanjang

| Ciri yang terlihat | Kemungkinan | Cara buka |
|---|---|---|
| Berakhiran `=` atau `==`, panjang kelipatan 4 | Base64 | `base64 -d`, atau CyberChef *From Base64* |
| Hanya `0-9` dan `a-f`, panjang genap | Hexadecimal | `xxd -r -p`, atau CyberChef *From Hex* |
| Banyak `%` diikuti dua karakter | URL encoding | CyberChef *URL Decode* |
| Huruf bergeser rapi, misal `WPP{...}` | ROT13 / Caesar | CyberChef *ROT13* |
| Deretan angka biner `01001010` | Binary | CyberChef *From Binary* |

## A.5 Alur Kerja 60 Detik Pertama di Soal Forensics

```
1. Buka file, lihat jumlah paket total
2. Statistics > Protocol Hierarchy   -> protokol apa saja yang ada?
3. Filter "http"                     -> ada lalu lintas polos?
4. Filter http.request.method=="POST"-> ada form yang dikirim?
5. Follow TCP Stream pada POST       -> ada kredensial?
6. Ctrl+F "FLAG" / "JCC{"            -> flag polos?
7. Belum ketemu? Cari header aneh, komentar HTML, dan string ber-encoding
```

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# LAMPIRAN B: KUNCI JAWABAN (KHUSUS PEMBINA)

> ## 🔒 HALAMAN INI JANGAN DIBAGIKAN KE SISWA
> Pisahkan atau hapus halaman ini sebelum mencetak modul untuk latihan.

## B.1 Kunci Tabel Temuan

| Kode | Item | Jawaban Benar | Paket |
|---|---|---|---|
| B1 | Domain server | `portal-nilai.smkmaska.local` | 1-2 (DNS) |
| B2 | IP server | `192.168.10.10` | 2 |
| B3 | IP login berhasil | `192.168.10.37` | 16 |
| B4 | IP login gagal | `192.168.10.52` | 6 |
| B5 | Status login gagal | `401 Unauthorized` | 7 |
| B6 | Status login berhasil | `302 Found` | 17 |
| B7 | Username | `admin_nilai` | 16 |
| B8 | Password | `Sup3rR4h4s1a_2026` | 16 |
| B9 | Cookie sesi | `PHPSESSID=b7f4c02e9ad13c5e88a1` | 17 |
| B10 | Halaman setelah login | `/dashboard.php` | 19-20 |
| B11 | Header mencurigakan | `X-Debug-Note` | 17 |
| B12 | Nilai ter-encode | `SkNDe2h0dHBfMXR1X2s0cnR1X3Awc30=` | 17 |
| B13 | Jenis encoding | Base64 | |
| B14 | **FLAG UTAMA** | `JCC{w1r3sh4rk_l1h4t_s3mu4ny4}` | 20 |
| B15 | **FLAG BONUS** | `JCC{http_1tu_k4rtu_p0s}` | 17 |
| B16 | Domain sesi TLS | `mail.smkmaska.sch.id` | Client Hello |

Login gagal memakai `siswa01` / `12345` dari `192.168.10.52`, disiapkan sebagai pengecoh. Siswa yang langsung membuka stream pertama tanpa memeriksa kode status akan tersesat di sini. Bahas kesalahan itu di Sesi 5, karena pola yang sama sering muncul di soal JCC sungguhan.

## B.2 Rambu Jawaban Pertanyaan Konseptual

**Pertanyaan 1.** Kekuatan password melindungi dari tebakan dan brute force, bukan dari penyadapan. HTTP mengirim isi form sebagai teks polos, jadi panjang dan kerumitan password tidak berpengaruh sama sekali begitu jalurnya terbuka. Analogi yang diharapkan: menulis rahasia serumit apa pun di kartu pos tetap terbaca tukang pos. Perbaikan di sisi server yang diterima: memasang sertifikat TLS dan memaksa HTTPS, mengaktifkan HSTS, atau mengalihkan seluruh port 80 ke 443.

**Pertanyaan 2.**
(a) Nama domain dikirim di ekstensi SNI pada paket Client Hello, dan Client Hello terkirim sebelum kunci enkripsi terbentuk. Sebutan lain yang diterima: browser perlu memberi tahu server sertifikat mana yang harus dikirim.
(b) Alamat IP kedua pihak, port, nama domain lewat SNI dan DNS, ukuran serta waktu tiap paket, durasi sesi, dan versi TLS.
(c) Tidak. HTTPS menjaga kerahasiaan isi, bukan identitas atau tujuan. Siswa yang menyebut Encrypted Client Hello atau DNS over HTTPS sebagai penyempurna layak mendapat nilai tambahan.

**Pertanyaan 3.**
(a) `Ctrl+F` menelusuri paket satu per satu dan berhenti di kecocokan pertama, sedangkan display filter mengevaluasi seluruh paket sekaligus lalu menampilkan semua yang cocok.
(b) Display filter, karena hasilnya menampilkan semua kecocokan sekaligus dan siswa langsung tahu jumlah kandidatnya tanpa menekan Find berulang kali.
(c) Keduanya gagal, karena teks `JCC{` tidak ada lagi dalam bentuk polos. Strategi pengganti: mengencode `JCC{` ke Base64 lalu mencari potongan hasilnya (`SkND`), memeriksa header non-standar satu per satu, memakai **File → Export Objects → HTTP** untuk menarik keluar seluruh berkas, atau menyaring string mencurigakan dengan `frame matches "[A-Za-z0-9+/]{20,}={0,2}"`.

## B.3 Rubrik Penilaian Write-Up

| Komponen | Bobot | Kriteria nilai penuh |
|---|---|---|
| Kelengkapan temuan (Bagian 5) | 25% | 15 dari 16 item terisi benar beserta nomor paket |
| Alur penalaran (Bagian 3) | 30% | Runtut, memuat minimal satu jalan buntu yang jujur dilaporkan |
| Reproduksi langkah (Bagian 4) | 20% | Orang lain bisa mengulang tanpa bertanya, tangkapan layar terbaca |
| Lampiran prompt AI (Bagian 6) | 15% | Prompt disalin utuh, refleksi terisi, tidak ada prompt yang disembunyikan |
| Mitigasi & refleksi (Bagian 7) | 10% | Rekomendasi teknis masuk akal dan spesifik |

## B.4 Regenerasi File Latihan

File `.pcap` dibuat ulang kapan saja dengan Python 3 tanpa dependensi tambahan:

```bash
python3 lab01/generate_pcap.py
```

Ubah nilai `FLAG_MAIN` dan `FLAG_BONUS` di baris atas skrip untuk membuat varian soal baru, misalnya saat latihan ulang atau seleksi internal. Skrip menghitung ulang panjang `Content-Length` dan seluruh checksum secara otomatis.

## B.5 Rencana Lanjutan

| Modul | Judul | Fokus |
|---|---|---|
| LAB 02 | The Hidden Layer | Steganografi dan metadata gambar |
| LAB 03 | Broken Login | Logika autentikasi web dan manipulasi cookie |
| LAB 04 | Cipher Playground | Klasik, Base-family, dan XOR sederhana |
| LAB 05 | Simulasi Penyisihan | 15 soal, 3 jam, write-up wajib |

***

**Selamat berlatih. Di jaringan, siapa yang paling teliti membaca, dia yang menang.**

*Modul ini disusun untuk pembinaan internal Tim CTF SMK Maskumambang 1, Pondok Pesantren Maskumambang.*
