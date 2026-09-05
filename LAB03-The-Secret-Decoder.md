# LAB 03: THE SECRET DECODER
### Membongkar Sandi Bertingkat dengan CyberChef & Hash Cracking

**Program Pembinaan Tim CTF SMK Maskumambang 1**
Persiapan **Jatim Cybersecurity Competition (JCC) 2026**, kategori SMA/SMK Sederajat
Kelas Sasaran: X (usia 15-16 tahun) | Level: Pemula Lanjutan
Prasyarat: **LAB 01** dan **LAB 02** sudah tuntas
Versi Modul: 1.0 | Tanggal: 05 September 2026

***

## DAFTAR ISI

1. [Informasi Modul & Target Capaian](#bagian-1-informasi-modul-target-capaian)
2. [Briefing Misi: Pesan dari Penyusup](#bagian-2-briefing-misi-pesan-dari-penyusup)
3. [Konsep Inti](#bagian-3-konsep-inti)
4. [Panduan Praktik Step-by-Step dengan CyberChef](#bagian-4-panduan-praktik-step-by-step-dengan-cyberchef)
5. [Prompt Drill: Latihan Bertanya ke AI](#bagian-5-prompt-drill-latihan-bertanya-ke-ai)
6. [Lembar Kerja Siswa & Template Write-Up](#bagian-6-lembar-kerja-siswa-template-write-up)
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
| **Kode Modul** | LAB-03 / CRYPTO-BASIC |
| **Judul** | The Secret Decoder: Sandi Bertingkat dengan CyberChef & Hash Cracking |
| **Kategori CTF** | Cryptography / Encoding |
| **Tingkat Kesulitan** | ★★☆☆☆ (Easy-Medium, soal wajib bisa di babak penyisihan) |
| **Metode** | Praktik berpasangan, 1 laptop per siswa |
| **Berkas Latihan** | `lab03/barang-bukti.txt` (2.064 byte, 4 barang bukti) |
| **Modul Prasyarat** | LAB 01 dan LAB 02 |

## 1.2 Alokasi Waktu (Total 60 Menit)

| Sesi | Kegiatan | Durasi |
|---|---|---|
| **Sesi 0** | Buka CyberChef dan CrackStation, pastikan keduanya termuat | 4 menit |
| **Sesi 1** | Briefing misi + konsep Encoding, Enkripsi, Hashing | 12 menit |
| **Sesi 2** | Pengenalan antarmuka CyberChef + Tantangan 1 | 10 menit |
| **Sesi 3** | Tantangan 2: resep bertingkat tiga lapis | 15 menit |
| **Sesi 4** | Tantangan 3: hash lookup di CrackStation | 10 menit |
| **Sesi 5** | Prompt drill AI + isi lembar kerja | 6 menit |
| **Sesi 6** | Diskusi, koreksi, tanya jawab | 3 menit |

> **Catatan pembina.** Sesi 3 adalah inti modul ini. Siswa sering menyusun resep dengan urutan terbalik lalu panik melihat output berantakan. Justru di situ pelajarannya. Biarkan mereka salah dulu selama 2 menit, baru bimbing membaca pesan errornya.

## 1.3 Prasyarat Alat

| Prasyarat | Cara memastikan |
|---|---|
| **LAB 01 dan LAB 02 tuntas** | Siswa sudah pernah membongkar Base64 di header `X-Debug-Note` (Lab 01) dan label domain (Lab 02) |
| **Browser + internet** | Buka `gchq.github.io/CyberChef`, halaman termuat penuh dengan 4 panel |
| **CrackStation** | Buka `crackstation.net`, kotak isian hash terlihat |
| **Text editor** | VS Code, Notepad++, atau Notepad, untuk mencatat hasil tiap lapis |
| **Berkas latihan** | `barang-bukti.txt`, ukuran 2.064 byte |

> ### 🌐 Kalau internet lab mati
> CyberChef bisa berjalan **sepenuhnya offline**. Unduh berkas `CyberChef_v10.x.html` dari halaman rilis GitHub-nya di rumah, simpan ke flashdisk, lalu buka berkas itu langsung di browser. Seluruh fitur tetap jalan karena CyberChef berupa satu berkas HTML mandiri.
>
> CrackStation tidak punya versi offline. Kalau internet mati, pembina bisa menyiapkan daftar hash beserta jawabannya sebagai pengganti sementara. Rinciannya ada di Lampiran C.3.

## 1.4 Capaian Pembelajaran (Learning Outcomes)

| Kode | Rumusan Capaian (terukur) | Bukti Ketercapaian |
|---|---|---|
| **LO-1** | Membedakan encoding, enkripsi, dan hashing beserta contoh masing-masing, lalu menjelaskan mana yang bisa dikembalikan dan mana yang tidak. | Jawaban benar Pertanyaan Konseptual nomor 1 |
| **LO-2** | Mengidentifikasi jenis format dari 6 string acak hanya dengan mengamati ciri fisiknya, minimal 5 benar, dalam waktu kurang dari 5 menit. | Tabel Latihan Identifikasi terisi |
| **LO-3** | Mengoperasikan CyberChef: menambah operasi ke Recipe, mengurutkannya, menonaktifkan satu langkah, dan membaca Output. | Tangkapan layar resep 3 langkah |
| **LO-4** | Menyusun resep bertingkat berisi minimal 3 operasi berurutan yang membongkar string berlapis sampai teks aslinya terbaca. | Flag utama ditemukan |
| **LO-5** | Menemukan kata sandi asli dari hash MD5 dan SHA-1 memakai basis data lookup, lalu menjelaskan kenapa satu hash lain gagal ditemukan. | Tabel Temuan Hash terisi lengkap |
| **LO-6** | Menjelaskan alasan hash lookup berhasil pada sandi umum dan gagal pada sandi acak, serta menyebut satu cara pertahanannya. | Jawaban Pertanyaan Konseptual nomor 3 |
| **LO-7** | Menyusun write-up sesuai juknis JCC 2026 lengkap dengan log prompt AI. | Dokumen write-up 7 bagian terisi |

## 1.5 Aturan Main

> ### ⚠️ ETIKA DAN BATASAN
>
> 1. **Semua hash di lab ini buatan.** Kata sandinya sengaja dipilih dari daftar sandi paling umum di dunia, khusus untuk latihan.
> 2. **Jangan pernah menempelkan hash dari sistem nyata ke situs lookup mana pun.** Begitu kalian menekan tombol kirim, hash itu berpindah ke server orang lain dan bisa tersimpan di sana. Kalau hash itu milik akun sekolah, kalian baru saja membocorkannya sendiri.
> 3. **Jangan mencoba memecahkan sandi milik orang lain**, termasuk teman sekelas, meski niatnya bercanda. UU ITE Pasal 30 mengatur akses tanpa hak.
> 4. **CrackStation bukan automated scanner.** Situs itu mesin pencari basis data, bukan pemindai kerentanan. Pemakaiannya tidak melanggar aturan JCC 2026. Yang dilarang panitia adalah sqlmap, Burp Scanner, dirb, nikto, dan sejenisnya.
> 5. **AI boleh dipakai** dengan syarat setiap prompt dicatat dan dilampirkan di write-up.

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# BAGIAN 2: BRIEFING MISI: PESAN DARI PENYUSUP

## 2.1 Situasi

```
=====================================================================
  LAPORAN INSIDEN #2026-0226-01           KLASIFIKASI: SANGAT RAHASIA
  Unit Teknologi Informasi, SMK Maskumambang 1
  Waktu penemuan : Kamis, 26 Februari 2026, 08:15 WIB
  Pelapor        : Teknisi jaringan, saat audit pasca-insiden
  Status         : ESKALASI ke tim forensik siswa
=====================================================================
```

Pagi Kamis, satu hari setelah kalian menutup kasus kebocoran dokumen.

Teknisi lab menyisir ulang server sekolah untuk memastikan tidak ada pintu belakang yang tertinggal. Ia tidak menemukan pintu belakang. Ia menemukan sesuatu yang lebih mengganggu.

Penyusup meninggalkan **pesan**.

Empat potong teks tersebar di tempat berbeda. Satu terselip di komentar berkas `index.php`. Satu tersembunyi di berkas `.hidden_note` di direktori `/tmp`. Satu berupa berkas `backup-akun.csv` yang isinya deretan huruf dan angka. Satu lagi bahkan ditulis tangan di papan tulis Lab Multimedia.

Tidak satu pun bisa dibaca. Semuanya berupa deretan karakter acak.

Kepala Program Keahlian menaruh berkas itu di meja kalian dan berkata satu kalimat: *"Penyusup ini sengaja meninggalkan jejak. Orang yang menyembunyikan pesan selalu ingin pesannya ditemukan. Cari tahu apa maunya."*

Kalian punya 60 menit. Kali ini tanpa Wireshark.

## 2.2 Misi Kalian

| # | Tugas | Nilai |
|---|---|---|
| **M1** | Bongkar **Barang Bukti #1**. Tulis pesan aslinya dan sebutkan jenis encodingnya. | 15 poin |
| **M2** | Bongkar **Barang Bukti #2** yang berlapis tiga. Tulis urutan resep yang kalian pakai dan isi tiap lapisnya. | 35 poin |
| **M3** | Temukan **FLAG UTAMA** yang tersembunyi di lapisan terdalam Barang Bukti #2. | 25 poin |
| **M4** | Pecahkan dua dari tiga hash di **Barang Bukti #3**. Tulis kata sandi aslinya. | 15 poin |
| **M5** | Jelaskan kenapa satu hash tersisa **gagal** ditemukan, padahal panjangnya sama persis. | 10 poin |

**Bonus (10 poin):** bongkar **Barang Bukti #4** dari papan tulis dan sebutkan pergeseran hurufnya.

## 2.3 Format Flag

```
JCC{TEKS_HURUF_BESAR_PAKAI_GARIS_BAWAH}
```

> 💡 **Peringatan jebakan.** Di lapisan tengah Barang Bukti #2, kalian akan melihat teks yang **berbentuk seperti flag** tetapi hurufnya kacau, misalnya `WPP{...}`. Itu bukan flag. Itu tanda kalian baru sampai di lapisan kedua dan masih kurang satu langkah. Jangan buru-buru menyetorkannya.

## 2.4 Peta Barang Bukti

```
   +---------------------------------------------------------------+
   |  BARANG BUKTI #1   index.php                                   |
   |  SGFsbyB0aW0gZm9yZW5zaWsuIEthbGlhbiB0ZXJsYW1iYXQg...           |
   |  Ciri: huruf besar-kecil + angka, panjang kelipatan 4          |
   |  -> 1 lapis                                                    |
   +---------------------------------------------------------------+
                              |
                              | pesannya menunjuk ke bukti berikutnya
                              v
   +---------------------------------------------------------------+
   |  BARANG BUKTI #2   /tmp/.hidden_note                           |
   |  56 31 42 51 65 31 6b 30 51 7a 45 31 58 31 45 7a ...           |
   |  Ciri: hanya 0-9 dan a-f, berpasangan dua-dua                  |
   |  -> 3 lapis, berisi FLAG UTAMA                                 |
   +---------------------------------------------------------------+
                              |
                              | pesan bukti #1 menyebut "sidik jari"
                              v
   +---------------------------------------------------------------+
   |  BARANG BUKTI #3   backup-akun.csv                             |
   |  admin_lab,MD5,0571749e2ac330a7455809c6b0e7af90                |
   |  Ciri: tepat 32 dan 40 karakter hex                            |
   |  -> bukan encoding, ini SIDIK JARI. Tidak bisa dibalik.        |
   +---------------------------------------------------------------+

   +---------------------------------------------------------------+
   |  BARANG BUKTI #4 (BONUS)   papan tulis                         |
   |  XJQFRFY PFQNFS QZQZX ZONFS XFSIN                              |
   |  Ciri: pola kata utuh, huruf bergeser                          |
   +---------------------------------------------------------------+
```

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# BAGIAN 3: KONSEP INTI

## 3.1 Tiga Hal yang Sering Tertukar

Banyak orang, termasuk orang dewasa yang bekerja di bidang IT, menyamakan tiga hal ini. Padahal ketiganya berbeda jauh. Memahami bedanya membuat kalian tahu **apakah sebuah string masih bisa dikembalikan atau tidak**, dan itu menentukan strategi kalian di kompetisi.

### 🔵 ENCODING = Bahasa Morse

```
   "SOS"  ->  ...  ---  ...
                      |
   siapa pun yang punya tabel Morse bisa mengembalikannya
```

Bahasa Morse dibuat supaya pesan bisa dikirim lewat bunyi. Bukan supaya rahasia. Tabel Morse dicetak di buku, ditempel di dinding pramuka, dan siapa pun boleh memilikinya.

**Encoding sama persis.** Base64, Hexadecimal, dan URL encoding dibuat supaya data bisa lewat jalur yang cuma menerima huruf biasa. Tidak ada kunci, tidak ada rahasia. Siapa pun yang tahu jenisnya bisa mengembalikannya dalam satu detik.

> **Pertanyaan yang harus kalian tanyakan:** "Apakah ini butuh kunci?" Kalau tidak, itu encoding.

### 🟢 ENKRIPSI = Buku Sandi Berpassword

```
   "SERANG FAJAR"  + kunci "MERAH"  ->  "XKZQPB WQMQO"
                                                |
   tanpa kunci "MERAH", tulisan itu tetap tidak berarti apa-apa
```

Bayangkan kalian dan sahabat punya buku sandi. Aturannya: geser setiap huruf sebanyak nomor halaman yang kalian sepakati. Nomor halaman itulah **kunci**. Orang lain boleh memegang buku sandinya, tetapi tanpa tahu nomor halamannya, ia tetap buntu.

**Enkripsi punya kunci.** AES, RSA, dan sandi Caesar semuanya termasuk enkripsi. Bedanya cuma kekuatan. Caesar bisa dipecahkan siswa SMK dalam 3 menit, AES tidak bisa dipecahkan seluruh komputer di dunia dalam waktu yang masuk akal.

> **Pertanyaan yang harus kalian tanyakan:** "Bisakah dikembalikan kalau saya punya kuncinya?" Kalau ya, itu enkripsi.

### 🔴 HASHING = Jus Buah

```
   apel + jeruk + mangga   ->  [BLENDER]  ->  segelas jus
                                                   |
   dari segelas jus, kalian TIDAK BISA mengembalikan buah utuhnya
```

Masukkan buah ke blender, kalian dapat jus. Sekarang coba kembalikan jus itu menjadi apel utuh. Mustahil. Blender bekerja satu arah.

**Hashing persis begitu.** MD5, SHA-1, dan SHA-256 mengubah teks apa pun menjadi deretan karakter berpanjang tetap. Prosesnya tidak bisa dibalik, selamanya, oleh siapa pun.

Tiga sifat penting hash:

| Sifat | Artinya | Contoh |
|---|---|---|
| **Satu arah** | tidak bisa dikembalikan | jus tidak bisa jadi buah lagi |
| **Panjang tetap** | input sependek apa pun atau sepanjang apa pun, output sama panjang | 1 huruf dan 1 buku sama-sama menghasilkan 32 karakter MD5 |
| **Efek longsor** | ubah 1 huruf saja, seluruh hasilnya berubah total | `admin` dan `Admin` menghasilkan hash yang sama sekali berbeda |

Karena itu hash disebut **sidik jari digital**. Sidik jari kalian menunjuk ke kalian, tetapi dari sidik jari saja orang tidak bisa membangun ulang tubuh kalian.

### Tabel Pembanding

| Aspek | Encoding | Enkripsi | Hashing |
|---|---|---|---|
| **Analogi** | Bahasa Morse | Buku sandi berpassword | Jus buah |
| **Butuh kunci?** | Tidak | Ya | Tidak |
| **Bisa dikembalikan?** | Ya, selalu | Ya, kalau punya kunci | **Tidak pernah** |
| **Tujuan dibuat** | supaya data aman melewati jalur | supaya data rahasia | supaya data bisa diverifikasi |
| **Contoh** | Base64, Hex, URL encoding | AES, RSA, Caesar, ROT13 | MD5, SHA-1, SHA-256 |
| **Dipakai untuk** | mengirim lampiran email | melindungi isi chat | menyimpan password |

> ### 🎯 Inti yang harus nempel di kepala
> Kalau kalian bertemu **hash**, berhenti mencari cara membalikkannya. Hash tidak bisa dibalik. Yang bisa kalian lakukan adalah **menebak** kata aslinya, lalu mencocokkan hasil hash tebakan itu. Itulah yang sebenarnya dilakukan CrackStation, dan kalian akan membuktikannya sendiri di Tantangan 3.

## 3.2 Cheat Sheet Identifikasi Format

Ini keterampilan paling menghemat waktu di babak penyisihan. Sebelum menyentuh alat apa pun, **pandangi dulu stringnya** dan tanyakan tiga hal: karakter apa saja yang dipakai, berapa panjangnya, dan adakah pola berulang.

### 📘 Base64

```
   SGFsbyB0aW0gZm9yZW5zaWsu
   ^^^^^^^^^^^^^^^^^^^^^^^^
   huruf BESAR + huruf kecil + angka, kadang + dan /
```

| Ciri | Penjelasan |
|---|---|
| **Karakter** | `A-Z`, `a-z`, `0-9`, plus `+` dan `/` |
| **Panjang** | selalu kelipatan 4 |
| **Akhiran** | sering diakhiri `=` atau `==`, tetapi **tidak selalu**. Ketiadaan `=` tidak membatalkan dugaan Base64 |
| **Rasa** | terlihat seperti huruf acak, tetapi ada campuran besar-kecil yang merata |

> **Kenapa ada tanda `=` di ujung?** Base64 bekerja per 3 byte yang diubah menjadi 4 karakter. Kalau data aslinya tidak habis dibagi 3, sisanya diganjal tanda `=` supaya panjangnya tetap kelipatan 4. Tanda itu disebut **padding**, dan keberadaannya petunjuk paling kuat bahwa kalian sedang melihat Base64.

### 📗 Hexadecimal

```
   56 31 42 51 65 31 6b 30
   ^^ ^^ ^^ ^^ ^^ ^^ ^^ ^^
   hanya 0-9 dan a-f, berpasangan dua karakter
```

| Ciri | Penjelasan |
|---|---|
| **Karakter** | hanya `0-9` dan `a-f` (atau `A-F`) |
| **Panjang** | selalu genap, karena 1 byte = 2 karakter |
| **Bentuk** | kadang dipisah spasi, kadang menyambung, kadang berawalan `0x` |
| **Rasa** | tidak ada huruf setelah `f`, jadi kalau kalian melihat `g`, `x`, atau `z`, itu **bukan** hex |

### 📙 ROT13 dan Caesar

```
   XJQFRFY PFQNFS QZQZX
   ^^^^^^^ ^^^^^^ ^^^^^
   spasi tetap di tempatnya, panjang kata tetap wajar
```

| Ciri | Penjelasan |
|---|---|
| **Karakter** | huruf saja, spasi dan tanda baca tidak berubah |
| **Panjang** | sama persis dengan teks aslinya |
| **Bentuk** | pola kata masih terlihat, seperti bahasa asing yang tidak dikenal |
| **Rasa** | terasa "hampir bisa dibaca", beda dari Base64 yang jelas acak |

**ROT13 adalah Caesar dengan pergeseran 13.** Angka 13 istimewa karena alfabet ada 26 huruf, jadi menggeser 13 dua kali mengembalikan kalian ke awal. Menyandikan dan membongkar ROT13 memakai operasi yang sama persis.

```
   A B C D E F G H I J K L M | N O P Q R S T U V W X Y Z
   |                          |
   +------ geser 13 --------->+
   A jadi N, B jadi O, C jadi P, dan seterusnya
   Lalu N geser 13 lagi kembali ke A
```

### 📕 Hash

Hash dikenali dari **panjangnya yang tepat**, bukan dari isinya. Hitung karakternya.

| Panjang | Algoritma | Contoh |
|---|---|---|
| **32 karakter hex** | MD5 | `0571749e2ac330a7455809c6b0e7af90` |
| **40 karakter hex** | SHA-1 | `b7a875fc1ea228b9061041b7cec4bd3c52ab3ce3` |
| **64 karakter hex** | SHA-256 | `8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918` |
| **128 karakter hex** | SHA-512 | (dua kali lipat SHA-256) |

> ### ⚠️ Jebakan yang sering menjatuhkan tim pemula
> Hash **juga** terdiri dari karakter hex. Jadi hex dan hash terlihat mirip. Pembedanya cuma satu: **panjang**.
>
> | String | Panjang | Semua hex? | Kesimpulan |
> |---|---|---|---|
> | `7275616e6720736572766572` | 24 | ya | hex biasa, bongkar dengan From Hex |
> | `21232f297a57a5a743894a0e4a801fc3` | 32 | ya | MD5, jangan dibongkar, harus dicari |
>
> Kalau panjangnya **bukan** 32, 40, 64, atau 128, kemungkinan besar itu hex biasa yang bisa langsung dibongkar. Coba saja From Hex, dan lihat apakah hasilnya teks yang masuk akal.

### Pohon Keputusan Identifikasi

```
                  Lihat stringnya
                        |
        +---------------+---------------+
        |                               |
  ada huruf setelah f?            hanya 0-9 dan a-f?
        |                               |
       YA                              YA
        |                               |
  ada = di ujung?              panjangnya 32/40/64?
   atau campur besar-kecil?             |
        |                        +------+------+
       YA                        |             |
        |                       YA            TIDAK
    BASE64                       |             |
        |                      HASH        HEX BIASA
   tidak? cek:              (harus dicari,  (From Hex)
   spasi utuh & pola kata     bukan dibongkar)
        |
       YA
        |
   ROT13 / CAESAR
```

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# BAGIAN 4: PANDUAN PRAKTIK STEP-BY-STEP DENGAN CYBERCHEF

> **Cara membaca bagian ini.** Setiap langkah punya kotak ✅ **CEK KEBERHASILAN**. Jangan lanjut sebelum layar kalian cocok. Kalau tidak cocok, baca 🔧 **KALAU MACET**.

## LANGKAH 0: Mengenal Antarmuka CyberChef

CyberChef dijuluki "pisau lipat tentara Swiss untuk analisis data". Ia dibuat oleh badan keamanan siber Inggris dan dibagikan gratis. Tim CTF di seluruh dunia memakainya.

1. Buka browser, kunjungi **`gchq.github.io/CyberChef`**
2. Tunggu sampai halaman termuat penuh.

> ✅ **CEK KEBERHASILAN**
> Layar kalian terbagi empat panel:
>
> ```
>  +------------------+------------------+----------------------------+
>  |   OPERATIONS     |     RECIPE       |         INPUT              |
>  |   (kiri)         |     (tengah)     |         (kanan atas)       |
>  |                  |                  |                            |
>  |  [Search...]     |  resep kalian    |  tempel string di sini     |
>  |                  |  disusun di sini |                            |
>  |  Favourites      |  dari atas       +----------------------------+
>  |  Data format     |  ke bawah        |         OUTPUT             |
>  |  Encryption      |                  |         (kanan bawah)      |
>  |  Hashing         |                  |                            |
>  |  ...             |   [ BAKE! ]      |  hasilnya muncul di sini   |
>  +------------------+------------------+----------------------------+
> ```

### Empat panel dan tugasnya

| Panel | Posisi | Tugasnya |
|---|---|---|
| **Operations** | kiri | gudang berisi ratusan operasi. Ada kotak **Search** di atasnya. |
| **Recipe** | tengah | daftar langkah yang akan dijalankan, **berurutan dari atas ke bawah** |
| **Input** | kanan atas | tempat menempelkan string yang mau dibongkar |
| **Output** | kanan bawah | hasilnya, diperbarui otomatis setiap kali resep berubah |

### Cara memakai panel Recipe

| Yang ingin kalian lakukan | Caranya |
|---|---|
| Menambah operasi | **klik dua kali** namanya di panel Operations, atau seret ke panel Recipe |
| Mengubah urutan | seret langkah ke atas atau ke bawah di dalam panel Recipe |
| Menonaktifkan satu langkah sementara | klik ikon **lingkaran bergaris miring** di kanan langkah itu |
| Menghapus satu langkah | seret langkah itu keluar dari panel Recipe |
| Menghapus seluruh resep | klik ikon **tempat sampah** di toolbar panel Recipe |
| Menjalankan resep | biasanya otomatis. Kalau tidak, klik tombol **BAKE!** di bawah |

> 💡 **Auto Bake.** Di bawah tombol BAKE ada sakelar **Auto Bake**. Saat menyala, CyberChef menjalankan resep setiap kali kalian mengetik. Biarkan menyala untuk lab ini.

> 💡 **URL kalian adalah resep kalian.** Perhatikan alamat di address bar berubah setiap kali kalian menambah operasi. Salin URL itu, dan siapa pun yang membukanya akan mendapat resep yang sama persis. Berguna sekali untuk kerja tim dan untuk melampirkan bukti di write-up.

***

## TANTANGAN 1: SINGLE DECODE (Barang Bukti #1)

Buka `barang-bukti.txt`, salin seluruh string panjang di bawah judul **BARANG BUKTI #1**.

### LANGKAH 1.1: Amati Dulu, Jangan Langsung Tempel

Sebelum menyentuh CyberChef, jawab tiga pertanyaan ini di lembar kerja kalian:

| Pertanyaan | Jawaban kalian |
|---|---|
| Karakter apa saja yang muncul? | |
| Apakah panjangnya kelipatan 4? | |
| Adakah tanda `=` di ujung? | |

Kebiasaan mengamati dulu inilah yang membedakan analis dari penebak. Di kompetisi, kebiasaan ini menghemat menit-menit berharga.

> ### 🤔 Kalau tidak ada tanda `=`, apakah tetap Base64?
> Ya, tetap bisa. Perhatikan bahwa Barang Bukti #1 **tidak** berakhiran `=` sama sekali.
>
> Alasannya begini. Base64 mengubah setiap 3 byte menjadi 4 karakter. Kalau panjang data aslinya kebetulan habis dibagi 3, tidak ada sisa yang perlu diganjal, sehingga tanda `=` memang tidak muncul.
>
> | Panjang data asli | Sisa bagi 3 | Padding |
> |---|---|---|
> | 219 byte | 0 | tidak ada `=` |
> | 220 byte | 1 | `==` |
> | 221 byte | 2 | `=` |
>
> Jadi pakailah tanda `=` sebagai **petunjuk yang menguatkan**, bukan sebagai syarat. Ciri yang jauh lebih andal: panjangnya kelipatan 4, dan hurufnya campur besar-kecil bersama angka. Barang Bukti #1 memenuhi keduanya.

### LANGKAH 1.2: Menempelkan String

1. Klik di dalam panel **Input** (kanan atas).
2. Tempel string Barang Bukti #1 dengan `Ctrl + V`.

> ✅ **CEK KEBERHASILAN**
> Di pojok kanan bawah panel Input muncul penghitung bertuliskan `length: 292  lines: 1`. Panel Output masih menampilkan teks yang sama persis, karena resep kalian masih kosong.

### LANGKAH 1.3: Menambahkan Operasi From Base64

1. Klik kotak **Search** di panel Operations kiri atas.
2. Ketik: `base64`
3. Dari hasil pencarian, cari **From Base64**. Perhatikan baik-baik: ada juga **To Base64**. Kalian butuh yang **From**.
4. **Klik dua kali** pada **From Base64**.

> ✅ **CEK KEBERHASILAN**
> Panel Recipe kini berisi satu kotak bertuliskan **From Base64**, lengkap dengan pilihan `Alphabet` yang isinya `A-Za-z0-9+/=`. Biarkan apa adanya.
>
> Panel **Output** langsung berubah menjadi kalimat berbahasa Indonesia yang bisa dibaca, diawali kata **"Halo tim forensik..."**

**🔍 Baca pesannya sampai habis.** Penyusup menyebut dua hal penting: petunjuk berikutnya ada di barang bukti kedua, dan kunci masuknya ditinggalkan **sebagai sidik jari** di barang bukti ketiga.

Kata "sidik jari" bukan kebetulan. Ingat analogi jus buah di Bagian 3.1. Penyusup sedang memberi tahu kalian bahwa barang bukti ketiga berisi **hash**, bukan encoding. Catat kalimat itu di write-up sebagai bukti alur penalaran kalian.

> 🔧 **KALAU MACET**
> - **Output berisi karakter aneh atau kosong:** kalian mungkin menyalin string dengan spasi atau baris baru yang ikut terbawa. Hapus isi Input, salin ulang, pastikan tidak ada baris kosong di akhir.
> - **Kalian menambahkan To Base64:** hasilnya justru makin panjang dan makin acak. Hapus langkah itu, ganti dengan **From Base64**.
> - **Muncul pesan `Invalid character`:** cek apakah ada tanda kutip ikut tersalin dari berkas.

### LANGKAH 1.4: Berkenalan dengan Operasi Magic (Opsional)

CyberChef punya operasi bernama **Magic** yang menebak sendiri jenis encoding-nya.

1. Hapus resep kalian (ikon tempat sampah).
2. Cari `Magic` di Operations, klik dua kali.

> ✅ **CEK KEBERHASILAN**
> Output menampilkan tabel berisi tebakan CyberChef beserta cuplikan hasilnya. Salah satu barisnya menyarankan **From Base64**, dan ada tautan yang bisa diklik untuk langsung memakai resep itu.

> ### ⚠️ Jangan bergantung pada Magic
> Magic sangat membantu, tetapi ia sering gagal pada string berlapis banyak, dan sering salah pada string pendek. Lebih penting lagi: **juri JCC menilai alur penalaran kalian**. Write-up yang cuma menulis "saya pakai Magic lalu ketemu" mendapat nilai analisis rendah. Pakai Magic untuk memastikan dugaan kalian, bukan untuk menggantikan proses berpikir.

***
<div class="page-break"></div>

```{=latex}
\newpage
```

## TANTANGAN 2: MULTI-STAGE RECIPE (Barang Bukti #2)

Ini inti modul hari ini. Barang Bukti #2 dibungkus **tiga lapis**. Kalian akan mengupasnya satu per satu, seperti mengupas bawang.

```
   +-------------------------------------------------------+
   |  LAPIS 1: Hexadecimal          <- yang kalian lihat    |
   |  +-------------------------------------------------+  |
   |  |  LAPIS 2: Base64                                |  |
   |  |  +-------------------------------------------+  |  |
   |  |  |  LAPIS 3: ROT13                           |  |  |
   |  |  |  +-------------------------------------+  |  |  |
   |  |  |  |   FLAG ASLI                         |  |  |  |
   |  |  |  +-------------------------------------+  |  |  |
   |  |  +-------------------------------------------+  |  |
   |  +-------------------------------------------------+  |
   +-------------------------------------------------------+

   Aturan emas: bongkar dari LUAR ke DALAM, satu lapis sekali jalan.
```

### LANGKAH 2.1: Mengamati dan Menebak Lapis Pertama

Salin isi Barang Bukti #2 ke panel **Input** CyberChef. Kosongkan dulu resep sebelumnya.

Amati stringnya:

```
56 31 42 51 65 31 6b 30 51 7a 45 31 58 31 45 7a 57 6a 46 66 57 54 52 44
4d 54 56 66 52 7a 4e 46 54 7a 42 42 56 46 67 30 52 58 30 3d
```

| Pertanyaan | Jawaban |
|---|---|
| Karakter apa saja? | hanya `0-9` dan `a-f` |
| Berpasangan dua-dua? | ya, dipisah spasi |
| Panjangnya 32, 40, atau 64? | bukan, ada 44 pasang |
| Kesimpulan | **Hexadecimal biasa**, bukan hash |

### LANGKAH 2.2: Mengupas Lapis 1 dengan From Hex

1. Di panel Operations, cari `From Hex`.
2. Klik dua kali **From Hex**.
3. Pada langkah itu ada pilihan **Delimiter**. Biarkan di posisi **Auto**, CyberChef akan mengenali spasi sendiri.

> ✅ **CEK KEBERHASILAN**
> Panel Output berubah menjadi:
>
> ```
> V1BQe1k0QzE1X1EzWjFfWTRDMTVfRzNFTzBBVFg0RX0=
> ```
>
> **Berhenti sejenak dan amati hasil ini.** Huruf besar-kecil bercampur, ada angka, dan yang paling menonjol: ada tanda `=` di ujungnya. Kalian baru saja mengupas satu lapis dan menemukan lapis berikutnya berupa **Base64**.

> 🔧 **KALAU MACET**
> - **Output kosong atau berisi kotak-kotak:** delimiter salah terbaca. Klik dropdown **Delimiter** pada langkah From Hex, pilih **Space** secara manual.
> - **Muncul error `Invalid input length`:** ada karakter non-hex ikut tersalin. Pastikan kalian tidak menyalin garis pemisah `---` dari berkas.

### LANGKAH 2.3: Menambah Lapis 2 tanpa Menghapus Lapis 1

Di sinilah keajaiban CyberChef. Kalian **tidak perlu** menyalin hasil lalu menempelnya ulang. Cukup tambahkan operasi berikutnya di bawah operasi pertama, dan CyberChef mengalirkan hasilnya secara otomatis.

1. **Jangan sentuh** langkah From Hex yang sudah ada.
2. Cari `From Base64` di panel Operations.
3. Klik dua kali. Operasi baru muncul **di bawah** From Hex.

> ✅ **CEK KEBERHASILAN**
> Panel Recipe sekarang berisi dua langkah berurutan:
>
> ```
>   1  From Hex          Delimiter: Auto
>   2  From Base64       Alphabet: A-Za-z0-9+/=
> ```
>
> Panel Output berubah menjadi:
>
> ```
> WPP{Y4C15_Q3Z1_Y4C15_G3EO0ATX4E}
> ```

**🚨 Ini momen paling penting di seluruh modul.**

Lihat bentuknya: ada kurung kurawal, ada garis bawah, ada angka yang menggantikan huruf. Bentuknya **persis seperti flag**. Banyak tim pemula berhenti di sini, menyetorkan `WPP{...}`, dan kehilangan poin.

Perhatikan tiga huruf pertama: `WPP`, bukan `JCC`. Format flag JCC 2026 selalu diawali `JCC`. Jadi kalian masih kurang satu lapis.

Sekarang hitung pergeserannya:

```
   J -> W    berapa langkah?
   J K L M N O P Q R S T U V W
   1 2 3 4 5 6 7 8 9 ... 13 langkah

   C -> P    berapa langkah?
   C D E F G H I J K L M N O P
   1 2 3 4 5 6 7 8 9 ... 13 langkah
```

Keduanya bergeser **13 langkah**. Itu tanda tangan **ROT13**.

### LANGKAH 2.4: Mengupas Lapis 3 dengan ROT13

1. Cari `ROT13` di panel Operations.
2. Klik dua kali. Operasi ini muncul di posisi ketiga.

> ✅ **CEK KEBERHASILAN**
> Panel Recipe berisi tiga langkah:
>
> ```
>   1  From Hex          Delimiter: Auto
>   2  From Base64       Alphabet: A-Za-z0-9+/=
>   3  ROT13             Amount: 13
> ```
>
> Panel Output menampilkan flag kalian, diawali `JCC{` dan diakhiri `}`.

**Salin flag itu dengan tombol Copy di toolbar panel Output**, jangan diketik ulang. Toolbar Output ada di pojok kanan bawah, berisi ikon disket (simpan ke berkas), ikon salin, dan ikon panah (jadikan hasil ini sebagai input baru).

> 🔧 **KALAU MACET**
> - **Output berantakan setelah menambah ROT13:** cek urutan resep. Kalau ROT13 tidak berada di posisi ketiga, seret ke bawah sampai urutannya benar.
> - **Hasilnya masih `WPP{...}`:** langkah ROT13 mungkin dalam keadaan nonaktif. Klik ikon lingkaran bergaris miring di sebelahnya supaya aktif kembali.
> - **Muncul `JPP{...}` atau campuran aneh:** pada langkah ROT13 ada dua kotak centang, `Rotate lower case chars` dan `Rotate upper case chars`. Keduanya harus tercentang.

### LANGKAH 2.5: Membuktikan Urutan Resep Itu Penting

Latihan singkat ini membuat konsepnya melekat. Kerjakan bersama pasangan kalian.

1. Di panel Recipe, **seret** langkah **ROT13** ke posisi paling atas.
2. Amati panel Output.

> ✅ **CEK KEBERHASILAN**
> Output menjadi kacau atau kosong. Alasannya masuk akal: ROT13 hanya bekerja pada huruf, sedangkan input kalian di posisi itu masih berupa angka hex. ROT13 mengacak huruf `a` sampai `f` di dalamnya, sehingga From Hex di langkah berikutnya menerima data rusak.
>
> Kembalikan urutannya ke semula, dan Output kembali normal.

**Tulis kesimpulan ini di write-up kalian:** resep bertingkat harus mengikuti urutan pembungkusan secara terbalik. Penyusup membungkus dari dalam ke luar, kalian membongkar dari luar ke dalam.

```
   Cara penyusup MEMBUNGKUS:           Cara kalian MEMBONGKAR:

   FLAG                                Hex
    -> ROT13                            -> Base64
       -> Base64                           -> ROT13
          -> Hex                              -> FLAG

   (dari dalam ke luar)                (dari luar ke dalam)
```

***
<div class="page-break"></div>

```{=latex}
\newpage
```

## TANTANGAN 3: HASH LOOKUP (Barang Bukti #3)

Barang Bukti #3 berbeda jenis dari dua sebelumnya. CyberChef tidak akan menolong kalian di sini, dan kalian harus paham kenapa.

```
akun,algoritma,nilai_hash
admin_lab,MD5,0571749e2ac330a7455809c6b0e7af90
operator,SHA-1,b7a875fc1ea228b9061041b7cec4bd3c52ab3ce3
kepala_lab,MD5,5a49035089ecef61e5c687d8bf294121
```

### LANGKAH 3.1: Mengidentifikasi Jenis Hash dengan Menghitung

Hitung panjang setiap nilai hash. Cara cepat: tempel ke panel **Input** CyberChef dan baca penghitung `length` di pojok kanan bawah.

| Akun | Panjang | Algoritma | Alasan |
|---|---|---|---|
| `admin_lab` | 32 | MD5 | 32 karakter hex adalah tanda tangan MD5 |
| `operator` | 40 | SHA-1 | 40 karakter hex adalah tanda tangan SHA-1 |
| `kepala_lab` | 32 | MD5 | sama dengan yang pertama |

Kolom `algoritma` di berkas itu memang sudah memberi tahu jawabannya. Di kompetisi, kolom itu biasanya tidak ada. Karena itu tetap biasakan menghitung sendiri.

### LANGKAH 3.2: Memahami Apa yang Sebenarnya Kalian Lakukan

Sebelum membuka CrackStation, pahami dulu mekanismenya. Bagian ini yang membuat write-up kalian bernilai tinggi.

**CrackStation tidak membalikkan hash.** Membalikkan hash mustahil, seperti mengembalikan jus menjadi buah. Yang dilakukan CrackStation adalah:

```
   Jauh-jauh hari, CrackStation menyiapkan buku telepon raksasa:

   +-------------------------+----------------------------------+
   |  KATA                   |  HASIL HASH-NYA                  |
   +-------------------------+----------------------------------+
   |  123456                 |  e10adc3949ba59abbe56e057f20f883e|
   |  password               |  5f4dcc3b5aa765d61d8327deb882cf99|
   |  sunshine               |  0571749e2ac330a7455809c6b0e7af90|
   |  ... 1,5 miliar kata lain ...                              |
   +-------------------------+----------------------------------+

   Saat kalian menempelkan sebuah hash, CrackStation hanya
   MENCARI baris yang cocok di kolom kanan, lalu memberi tahu
   isi kolom kirinya. Persis seperti mencari nomor telepon
   di buku telepon, lalu membaca nama pemiliknya.
```

Konsekuensinya: **kalau kata aslinya tidak pernah masuk daftar, hash itu tidak akan pernah ditemukan.** Ingat baik-baik, karena Misi M5 menanyakan hal ini.

### LANGKAH 3.3: Memakai CrackStation

1. Buka browser, kunjungi **`crackstation.net`**
2. Di tengah halaman ada kotak teks besar bertuliskan *"Enter up to 20 non-salted hashes, one per line"*.
3. Salin **ketiga nilai hash** dari Barang Bukti #3, tempelkan **satu hash per baris**:

```
0571749e2ac330a7455809c6b0e7af90
b7a875fc1ea228b9061041b7cec4bd3c52ab3ce3
5a49035089ecef61e5c687d8bf294121
```

4. Centang kotak **"I'm not a robot"** dan selesaikan verifikasinya.
5. Klik tombol **Crack Hashes**.

> ✅ **CEK KEBERHASILAN**
> Muncul tabel hasil dengan tiga kolom: `Hash`, `Type`, dan `Result`.
>
> | Hash | Type | Result |
> |---|---|---|
> | `0571749e...` | md5 | (kata sandi terbaca) |
> | `b7a875fc...` | sha1 | (kata sandi terbaca) |
> | `5a490350...` | md5 | **Not found** atau baris kosong |
>
> Dua hash terpecah, satu tidak. Itu **bukan kesalahan kalian**. Justru itulah inti pelajarannya.

> 🔧 **KALAU MACET**
> - **Semua hasil "Not found":** kemungkinan ada spasi ikut tersalin. Hapus isi kotak, ketik ulang atau salin lebih hati-hati.
> - **Situs tidak bisa dibuka:** pakai alternatif `md5decrypt.net` atau `hashes.com`. Kalau semuanya terblokir jaringan sekolah, lihat Lampiran C.3 untuk cara luring.
> - **CAPTCHA berputar terus:** ganti browser, atau matikan pemblokir iklan sementara.

### LANGKAH 3.4: Menjelaskan Kenapa Satu Hash Gagal

Hash milik `kepala_lab` panjangnya sama persis, 32 karakter, algoritmanya juga MD5. Kenapa yang satu ketemu dan yang satu tidak?

Jawabannya ada di **kata aslinya**, bukan di hash-nya.

| Akun | Kata sandi | Kenapa hasilnya begitu |
|---|---|---|
| `admin_lab` | kata umum berbahasa Inggris | ada di daftar 1,5 miliar kata CrackStation |
| `operator` | kata umum berbahasa Inggris | juga ada di daftar |
| `kepala_lab` | campuran huruf besar-kecil, angka, dan simbol, 16 karakter, acak | tidak pernah ada di daftar mana pun |

**Pelajaran yang dibawa pulang:** kekuatan sebuah kata sandi bukan pada panjang hash-nya, melainkan pada **seberapa sulit kata itu ditebak**. Hash MD5 dari `sunshine` dan hash MD5 dari sandi acak 16 karakter sama-sama 32 karakter. Yang membedakan nasib keduanya cuma satu: apakah kata itu pernah dipakai orang lain sebelumnya.

Gabungkan pelajaran ini dengan Lab 01, dan kalian punya gambaran utuh:

| Lab | Pelajaran | Kesimpulan gabungan |
|---|---|---|
| Lab 01 | password kuat tetap bocor lewat HTTP polos | sandi kuat butuh saluran aman |
| Lab 03 | sandi lemah tetap terbongkar meski di-hash | saluran aman butuh sandi kuat |

Dua-duanya harus ada. Salah satu saja tidak cukup.

> ### 🛡️ Bonus untuk write-up: apa itu salt
> Situs yang baik tidak menyimpan `md5(password)` begitu saja. Ia menambahkan potongan acak unik untuk setiap pengguna, disebut **salt**, lalu menyimpan `hash(password + salt)`.
>
> Efeknya: dua orang yang kebetulan memakai sandi `sunshine` akan punya hash yang berbeda total. Basis data lookup seperti CrackStation langsung tidak berguna, karena daftar mereka dibuat tanpa salt. Perhatikan kalimat di situsnya sendiri: *"non-salted hashes"*.
>
> Sebutkan salt di bagian Mitigasi write-up kalian. Juri menyukai jawaban yang menyebut solusi konkret.

***

## TANTANGAN BONUS: BARANG BUKTI #4 (Papan Tulis)

```
XJQFRFY PFQNFS QZQZX ZONFS XFSIN
```

Amati cirinya: spasi tetap utuh, panjang kata wajar, hanya huruf besar. Ini **Caesar cipher**, dan kalian tidak tahu berapa pergeserannya.

### Cara 1: Coba Semua Kemungkinan

1. Tempel string itu ke Input CyberChef.
2. Cari operasi **ROT13**, klik dua kali.
3. Pada langkah ROT13 ada kotak angka **Amount** berisi `13`. Ubah angka itu satu per satu: 1, 2, 3, dan seterusnya sampai 25.
4. Amati Output setiap kali kalian mengubah angkanya.

> ✅ **CEK KEBERHASILAN**
> Pada salah satu nilai Amount, Output berubah menjadi kalimat berbahasa Indonesia yang bisa dibaca dan terasa seperti ucapan selamat. Catat nilai Amount itu di lembar kerja.

### Cara 2: Biarkan CyberChef Mencoba Semuanya

1. Hapus resep kalian.
2. Cari operasi **ROT13 Brute Force**, klik dua kali.

> ✅ **CEK KEBERHASILAN**
> Output menampilkan 25 baris sekaligus, masing-masing diberi label `Amount = 1`, `Amount = 2`, dan seterusnya. Kalian tinggal memindai mana yang berbahasa Indonesia.

Cara kedua jauh lebih cepat, dan tetap sah dipakai di JCC 2026 karena ini fitur bawaan alat analisis, bukan automated scanner. Tetap catat di write-up bahwa kalian memakainya.

## 4.7 Ringkasan Perintah Tantangan 1 sampai Bonus

| Tantangan | Bahan | Resep CyberChef | Hasil |
|---|---|---|---|
| 1 | Barang Bukti #1 | `From Base64` | pesan penyusup |
| 2 | Barang Bukti #2 | `From Hex` → `From Base64` → `ROT13` | **FLAG UTAMA** |
| 3 | Barang Bukti #3 | (bukan CyberChef, pakai CrackStation) | 2 sandi terpecah, 1 gagal |
| Bonus | Barang Bukti #4 | `ROT13 Brute Force` atau `ROT13` dengan Amount diubah | kalimat ucapan selamat |

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# BAGIAN 5: PROMPT DRILL: LATIHAN BERTANYA KE AI

## 5.1 Pengingat Aturan JCC 2026

Chatbot AI boleh dipakai. Syaratnya satu:

> **Seluruh riwayat prompt dan alur penalaran tim wajib dilampirkan dalam write-up resmi.**

## 5.2 Aturan Emas untuk Modul Kripto

Modul ini paling rawan disalahgunakan. Menempelkan string barang bukti mentah-mentah ke chatbot lalu menyalin hasilnya memang bisa memberi kalian flag, tetapi merugikan kalian dua kali:

1. **Nilai analisis write-up kalian jatuh.** Juri membaca lampiran prompt dan langsung tahu kalian tidak menganalisis apa pun.
2. **Kalian tidak belajar apa-apa.** Di babak final nanti tidak ada waktu menunggu jawaban chatbot untuk 15 soal.

Pakailah AI untuk **mengasah kemampuan mengenali pola**, bukan untuk membongkar. Bedanya begini:

| ❌ Cara yang merugikan | ✅ Cara yang menguntungkan |
|---|---|
| "Decode string ini: SGFsbyB0aW0..." | "Ciri apa pada string berikut yang menandakan jenis encoding tertentu?" |
| "Apa flagnya?" | "Bagaimana urutan yang benar untuk membongkar string berlapis di CyberChef?" |
| "Kerjakan soal ini" | "Kenapa hasil decode saya masih berupa huruf acak padahal langkahnya sudah benar?" |

> 💡 **Trik menyensor.** Kalau kalian perlu menunjukkan string ke AI, potong saja sebagian. Kirim 20 karakter pertamanya, bukan seluruhnya. AI tetap bisa mengenali polanya, sedangkan kalian tetap yang mengerjakan pembongkarannya.

## 5.3 Template Prompt #1: Mengenali Jenis Encoding dari Cirinya

Pakai ini di Langkah 1.1 dan 2.1, ketika kalian ingin memastikan dugaan sendiri.

```text
Kamu adalah mentor CTF kategori Cryptography untuk siswa SMK kelas 10 yang
baru pertama kali belajar encoding.

KONTEKS:
Saya sedang menganalisis barang bukti digital berupa string acak yang
ditemukan di sebuah server. Saya belum tahu jenis encodingnya. Saya hanya
mengirimkan 24 karakter pertamanya, bukan seluruhnya, karena saya ingin
mengerjakan sendiri pembongkarannya.

POTONGAN STRING:
    56 31 42 51 65 31 6b 30 51 7a 45

CIRI YANG SUDAH SAYA AMATI SENDIRI:
- Hanya memakai angka 0 sampai 9 dan huruf a sampai f
- Setiap kelompok terdiri dari 2 karakter, dipisah spasi
- Total ada 44 kelompok

PERTANYAAN:
1. Berdasarkan ciri di atas, jenis encoding apa yang paling mungkin, dan
   ciri mana yang paling menentukan kesimpulan itu?
2. Panjang totalnya bukan 32, 40, atau 64 karakter. Apa artinya bagi
   kemungkinan string ini berupa hash?
3. Sebutkan 2 ciri lain yang harus saya periksa untuk memastikan dugaan
   saya benar sebelum mulai membongkar.

FORMAT JAWABAN:
Poin bernomor, maksimal 3 kalimat per poin.
Bahasa Indonesia sederhana.
JANGAN membongkar isi stringnya, saya ingin mengerjakannya sendiri.
```

**Kenapa prompt ini bekerja:**
- Kalian mengirim **potongan**, bukan seluruh barang bukti.
- Kalian menuliskan **ciri yang sudah kalian amati sendiri**, jadi lampiran write-up kalian memperlihatkan kalian berpikir lebih dulu.
- Kalimat terakhir secara tegas melarang AI memberi jawaban. Kalimat itu melindungi nilai analisis kalian.
- Pertanyaan nomor 2 melatih pembedaan hex versus hash, materi yang paling sering menjatuhkan tim pemula.

## 5.4 Template Prompt #2: Menyusun Urutan Resep CyberChef

Pakai ini di Langkah 2.5, saat urutan resep kalian belum menghasilkan teks yang masuk akal.

```text
Kamu adalah instruktur CyberChef untuk pemula.

KONTEKS:
Saya membongkar sebuah string berlapis di CyberChef. Saya tidak akan
mengirimkan isi stringnya. Yang saya kirim hanya bentuk hasil di tiap tahap.

TAHAPAN YANG SUDAH SAYA LALUI:
- Input awal  : deretan pasangan karakter 0-9 dan a-f, dipisah spasi
- Setelah operasi pertama : huruf besar-kecil bercampur angka,
                            diakhiri tanda "="
- Setelah operasi kedua   : teks berpola JCC{...} tetapi tiga huruf
                            pertamanya salah, terbaca WPP bukan JCC

PERTANYAAN:
1. Operasi apa yang tepat untuk tahap ketiga, dan bagaimana saya bisa
   memastikannya dari pergeseran huruf J menjadi W?
2. Kenapa urutan operasi di panel Recipe tidak boleh dibalik? Jelaskan
   dengan analogi yang mudah dipahami siswa kelas 10.
3. Kalau saya menaruh operasi tahap ketiga di posisi paling atas, apa yang
   akan terjadi pada hasilnya, dan kenapa?

FORMAT JAWABAN:
Tabel dua kolom berjudul "Langkah" dan "Alasan", lalu satu paragraf penutup
berisi analogi. Bahasa Indonesia.
```

**Kenapa prompt ini bekerja:**
- Kalian mendeskripsikan **bentuk hasil**, bukan mengirim datanya. AI tetap bisa membantu tanpa mengerjakan soal untuk kalian.
- Pertanyaan nomor 2 dan 3 meminta **penjelasan konsep**, dan jawabannya bisa langsung kalian pakai untuk mengisi bagian Alur Penalaran di write-up.
- Kalian meminta analogi, sehingga jawabannya cocok dengan gaya bahasa laporan tim kalian.

## 5.5 Disiplin Mencatat Prompt

Buka `prompt-log.md` di text editor **sebelum** lab dimulai:

```markdown
### Prompt #1
- Waktu       : 09:12 WIB
- Chatbot     : Claude
- Prompt      : (salin persis yang kalian ketik, jangan diringkas)
- Inti jawaban: (1-2 kalimat)
- Keputusan   : (apa yang tim lakukan setelah membaca jawaban itu)
```

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
| Tanggal Praktikum | ....... / ....... / 2026 |
| Waktu mulai | ....... : ....... WIB |
| Waktu selesai | ....... : ....... WIB |

## 6.2 Latihan Identifikasi Format

Amati enam string berikut. Jangan membongkarnya dulu. Tebak jenisnya hanya dari cirinya, lalu tulis ciri yang membuat kalian yakin.

| # | String | Panjang | Jenis (tebakan) | Ciri yang meyakinkan |
|---|---|---|---|---|
| A | `a3VuY2kgbGVtYXJp` | | | |
| B | `7275616e6720736572766572` | | | |
| C | `FREIRE YNO` | | | |
| D | `21232f297a57a5a743894a0e4a801fc3` | | | |
| E | `8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918` | | | |
| F | `bmlsYWkgdWppYW4=` | | | |

Setelah semua tertebak, baru bongkar yang bisa dibongkar. Tulis hasilnya:

| # | Hasil pembongkaran (atau tulis "tidak bisa dibongkar") |
|---|---|
| A | |
| B | |
| C | |
| D | |
| E | |
| F | |

## 6.3 Tabel Hasil Identifikasi Barang Bukti

| Kode | Barang Bukti | Jenis yang Terdeteksi | Urutan Resep CyberChef | Hasil Terbongkar |
|---|---|---|---|---|
| **BB1** | String di `index.php` | | | |
| **BB2** lapis 1 | String di `.hidden_note` | | | |
| **BB2** lapis 2 | (hasil lapis 1) | | | |
| **BB2** lapis 3 | (hasil lapis 2) | | | |
| **BB4** | Tulisan papan tulis | | | |

**URL resep CyberChef kalian** (salin dari address bar setelah resep selesai):

```
https://gchq.github.io/CyberChef/#recipe=______________________________________
```

## 6.4 Tabel Temuan Hash

| Akun | Nilai Hash | Panjang | Algoritma | Kata Sandi Asli | Status |
|---|---|---|---|---|---|
| `admin_lab` | | | | | ☐ Terpecah ☐ Gagal |
| `operator` | | | | | ☐ Terpecah ☐ Gagal |
| `kepala_lab` | | | | | ☐ Terpecah ☐ Gagal |

**Kenapa satu hash gagal ditemukan?** Jawab dalam 2 kalimat:

```
_________________________________________________________________________

_________________________________________________________________________
```

## 6.5 Flag Final

```
FLAG UTAMA:   JCC{ ____________________________________ }

Ditemukan di: Barang Bukti nomor ______
Jumlah lapis: ______
Resep akhir : ______________________________________________
```

**Skor mandiri:** ...... dari 100 poin (+ 10 poin bonus)

***

## 6.6 Pertanyaan Konseptual

Jawab dengan kalimat kalian sendiri. Menyalin dari modul tidak mendapat nilai.

**PERTANYAAN 1 (Bobot 30): Membedakan Tiga Konsep**

a. Jelaskan beda encoding, enkripsi, dan hashing memakai analogi kalian sendiri, bukan analogi yang ada di modul ini.

b. Barang Bukti #1 memakai Base64. Base64 sering disebut orang sebagai "enkripsi". Jelaskan kenapa sebutan itu keliru, dan apa akibatnya kalau seorang programmer benar-benar memakai Base64 untuk menyimpan password.

c. Ada satu jenis di antara ketiganya yang **tidak bisa dikembalikan sama sekali**. Sebutkan mana, lalu jelaskan kenapa orang tetap memakainya padahal tidak bisa dibalik.

```
Jawaban:
_________________________________________________________________________

_________________________________________________________________________

_________________________________________________________________________

_________________________________________________________________________
```

***

**PERTANYAAN 2 (Bobot 35): Tentang Lapisan dan Urutan**

Penyusup membungkus flag dengan tiga lapis: ROT13, lalu Base64, lalu Hex.

a. Kenapa kalian harus membongkarnya dengan urutan terbalik? Jelaskan dengan analogi benda sehari-hari.

b. Di Langkah 2.5 kalian memindahkan ROT13 ke posisi paling atas dan hasilnya rusak. Jelaskan secara teknis apa yang terjadi pada data ketika itu.

c. Andaikan penyusup menambah satu lapis lagi, yaitu membalik urutan seluruh karakter. Di posisi mana operasi `Reverse` harus kalian taruh di resep, dan bagaimana kalian bisa tahu lapisan itu ada?

d. Kenapa menambah banyak lapisan encoding **bukan** cara yang benar untuk mengamankan data? Kaitkan dengan jawaban Pertanyaan 1b.

```
Jawaban:
_________________________________________________________________________

_________________________________________________________________________

_________________________________________________________________________

_________________________________________________________________________
```

***

**PERTANYAAN 3 (Bobot 35): Tentang Hash dan Pertahanannya**

Tiga hash di Barang Bukti #3 sama-sama sah, dua terpecah dan satu tidak.

a. Jelaskan mekanisme sebenarnya di balik CrackStation. Kenapa istilah "membalikkan hash" keliru?

b. Sandi `kepala_lab` panjangnya 16 karakter dan acak. Sandi `admin_lab` panjangnya 8 karakter dan berupa kata umum. Keduanya menghasilkan hash MD5 sepanjang 32 karakter. Jelaskan kenapa panjang hash tidak menunjukkan kekuatan sandi.

c. Sebutkan **dua** cara admin sekolah membuat basis data sandinya tetap aman meski dicuri orang. Untuk setiap cara, jelaskan bagaimana cara itu menggagalkan lookup seperti CrackStation.

d. Gabungkan pelajaran Lab 01 dan Lab 03. Tulis satu paragraf berisi saran kalian untuk admin Portal Nilai sekolah, mencakup saluran pengiriman maupun penyimpanan sandi.

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

## 6.7 Template Write-Up Resmi JCC 2026

> **Cara pakai:** salin seluruh blok di bawah ke text editor, simpan sebagai `writeup-lab03-[namatim].md`, isi setiap bagian, lalu ekspor ke PDF sebelum mengunggah.

````markdown
# WRITE-UP JCC 2026
## Nama Soal   : LAB 03 - The Secret Decoder
## Kategori    : Cryptography / Encoding
## Nama Tim    : ______________________
## Anggota     : 1. ______________________  2. ______________________
## Asal Sekolah: SMK Maskumambang 1
## Tanggal     : ____ / ____ / 2026
## Status      : [ ] Solved   [ ] Unsolved

# 1. DESKRIPSI SOAL
(Tulis ulang deskripsi dari panitia. Sebutkan berkas yang diberikan dan
berapa barang bukti yang ada di dalamnya.)

# 2. ALAT YANG DIGUNAKAN
| Alat | Alamat / Versi | Fungsi dalam penyelesaian |
|---|---|---|
| CyberChef | gchq.github.io/CyberChef | |
| CrackStation | crackstation.net | |
| Chatbot AI | | |

Pernyataan kepatuhan:
Tim menyatakan tidak menggunakan automated scanner (sqlmap, Burp Scanner,
dirb, nikto, atau sejenisnya). CyberChef dan CrackStation adalah alat
analisis data dan basis data pencarian, bukan pemindai kerentanan.

Tanda tangan ketua tim: ______________________

# 3. ALUR PENALARAN (REASONING FLOW)
(Tulis urut sesuai kejadian, termasuk langkah yang gagal.)

## 3.1 Identifikasi awal
- Ciri yang diamati pada Barang Bukti #1: ____
- Dugaan awal tim: ____
- Cara memastikan dugaan itu: ____

## 3.2 Pembongkaran Barang Bukti #1
- Resep yang dipakai: ____
- Isi pesan yang ditemukan: ____
- Petunjuk apa yang diberikan pesan itu: ____

## 3.3 Pembongkaran Barang Bukti #2
| Lapis | Ciri yang diamati | Operasi yang dipakai | Hasil |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

- Bagaimana tim tahu hasil lapis 2 belum final: ____
- Cara tim menghitung pergeseran huruf: ____

## 3.4 Jalan buntu yang sempat ditemui
- Apa yang dicoba: ____
- Kenapa gagal: ____
- Pelajaran yang diambil: ____

## 3.5 Analisis Barang Bukti #3
- Cara menentukan algoritma tiap hash: ____
- Hash yang berhasil ditemukan: ____
- Hash yang gagal, beserta alasannya: ____

# 4. LANGKAH TEKNIS (STEP-BY-STEP REPRODUCTION)

**Langkah 1:** ____
> Operasi CyberChef: `____`
> Hasil: ____
> [Tangkapan layar 1]

**Langkah 2:** ____
> Operasi CyberChef: `____`
> Hasil: ____
> [Tangkapan layar 2]

**Langkah 3:** ____
> Operasi CyberChef: `____`
> Hasil: ____
> [Tangkapan layar 3 - panel Recipe berisi 3 langkah]

**Langkah 4:** ____
> Situs: ____
> Hasil: ____
> [Tangkapan layar 4 - tabel hasil CrackStation]

URL resep CyberChef lengkap:
    https://gchq.github.io/CyberChef/#recipe=____

# 5. BUKTI TEMUAN
| Item | Nilai |
|---|---|
| Jenis encoding BB1 | |
| Isi pesan BB1 | |
| Urutan resep BB2 | |
| Hasil lapis 1 BB2 | |
| Hasil lapis 2 BB2 | |
| Sandi `admin_lab` | |
| Sandi `operator` | |
| Status `kepala_lab` | |
| Pergeseran Caesar BB4 | |

**FLAG:**

    JCC{________________________________}

# 6. LAMPIRAN RIWAYAT PROMPT AI (WAJIB)
(Salin persis prompt yang tim kirimkan. Jangan dirapikan, jangan diringkas.)

| No | Waktu | Chatbot | Prompt yang dikirim (lengkap) | Ringkasan jawaban AI | Keputusan tim setelah membaca |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

## Refleksi penggunaan AI
- Bagian yang dikerjakan tim sendiri tanpa AI: ____
- Bagian yang terbantu AI, dan seberapa besar bantuannya: ____
- Apakah tim pernah menyensor string sebelum mengirim ke AI? Kenapa? ____
- Apakah ada jawaban AI yang keliru? Bagaimana tim mengetahuinya? ____

# 7. PELAJARAN & MITIGASI
## 7.1 Akar masalah
(Kenapa pesan penyusup bisa dibongkar semudah ini?)
____

## 7.2 Rekomendasi untuk admin sistem sekolah
1. ____
2. ____
3. ____

## 7.3 Refleksi tim
(Apa yang akan tim lakukan berbeda kalau mengerjakan soal kripto besok?)
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

## A.1 Identifikasi Kilat

| Yang kalian lihat | Kemungkinan besar | Operasi CyberChef |
|---|---|---|
| Campur huruf besar-kecil dan angka, panjang kelipatan 4 (sering diakhiri `=`) | Base64 | `From Base64` |
| Hanya `0-9` dan `a-f`, panjang genap | Hexadecimal | `From Hex` |
| Hanya `0-9` dan `a-f`, tepat 32 karakter | MD5 | (cari di lookup) |
| Hanya `0-9` dan `a-f`, tepat 40 karakter | SHA-1 | (cari di lookup) |
| Hanya `0-9` dan `a-f`, tepat 64 karakter | SHA-256 | (cari di lookup) |
| Banyak `%` diikuti dua karakter | URL encoding | `URL Decode` |
| Spasi utuh, pola kata wajar, huruf bergeser | ROT13 / Caesar | `ROT13` atau `ROT13 Brute Force` |
| Deretan `0` dan `1` berkelompok 8 | Binary | `From Binary` |
| Huruf besar semua, diakhiri `=`, tanpa huruf kecil | Base32 | `From Base32` |
| Berawalan `\x` atau `0x` | Hex bergaya kode | `From Hex` |
| Teks terbalik dari belakang | Reverse | `Reverse` |

## A.2 Operasi CyberChef yang Wajib Hafal

| Operasi | Kategori | Fungsi |
|---|---|---|
| `From Base64` | Data format | membongkar Base64 |
| `To Base64` | Data format | membuat Base64 |
| `From Hex` | Data format | membongkar hex |
| `To Hex` | Data format | membuat hex |
| `From Binary` | Data format | membongkar biner |
| `URL Decode` | Data format | membongkar `%20` dan kawan-kawan |
| `ROT13` | Encryption | menggeser huruf, Amount bisa diubah |
| `ROT13 Brute Force` | Encryption | mencoba 25 pergeseran sekaligus |
| `XOR Brute Force` | Encryption | mencoba banyak kunci XOR |
| `MD5` / `SHA1` / `SHA2` | Hashing | **membuat** hash, bukan membongkar |
| `Magic` | Utils | menebak jenis encoding otomatis |
| `Reverse` | Utils | membalik urutan karakter |
| `Regular expression` | Regex | mencari pola, misalnya `JCC\{.*\}` |
| `Extract URLs` | Extractors | menarik semua alamat web dari teks |
| `Strings` | Extractors | menarik teks yang terbaca dari data biner |

## A.3 Jalan Pintas Keyboard CyberChef

| Pintasan | Fungsi |
|---|---|
| `Ctrl + Alt + Space` | fokus ke kotak Search di panel Operations |
| `Ctrl + Alt + B` | jalankan resep (Bake) |
| `Ctrl + Alt + O` | fokus ke panel Input |
| `Ctrl + Alt + Delete` | kosongkan seluruh resep |

## A.4 Alur Kerja 60 Detik Pertama di Soal Cryptography

```
1. JANGAN langsung tempel ke alat. Pandangi stringnya 10 detik.
2. Karakter apa saja yang dipakai? Ada huruf setelah f?
3. Hitung panjangnya. 32 / 40 / 64? Berarti hash, bukan encoding.
4. Ada tanda = di ujung? Kemungkinan besar Base64.
5. Spasi masih utuh dan pola kata terlihat? Kemungkinan Caesar.
6. Bongkar SATU lapis dulu, lalu ulangi langkah 2 pada hasilnya.
7. Berhenti kalau hasilnya sudah berupa teks yang masuk akal.
8. Hasil berbentuk flag tetapi awalannya salah? Masih ada 1 lapis lagi.
9. Buntu total? Coba operasi Magic, lalu verifikasi dugaannya sendiri.
```

## A.5 Perintah Terminal Setara (Tanpa Browser)

Berguna kalau internet lab mati atau kalian ingin bekerja lebih cepat.

| Tujuan | Linux / macOS | Windows PowerShell |
|---|---|---|
| Bongkar Base64 | `echo 'STRING' \| base64 -d` | `[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('STRING'))` |
| Buat Base64 | `echo -n 'teks' \| base64` | `[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes('teks'))` |
| Bongkar hex | `echo 'STRING' \| xxd -r -p` | |
| Hitung MD5 | `md5sum berkas` | `Get-FileHash -Algorithm MD5 berkas` |
| Hitung SHA-1 | `sha1sum berkas` | `Get-FileHash -Algorithm SHA1 berkas` |
| MD5 dari teks | `echo -n 'teks' \| md5sum` | |
| ROT13 | `echo 'TEKS' \| tr 'A-Za-z' 'N-ZA-Mn-za-m'` | |

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# LAMPIRAN B: KUNCI JAWABAN (KHUSUS PEMBINA)

> ## 🔒 HALAMAN INI JANGAN DIBAGIKAN KE SISWA
> Pisahkan atau hapus sebelum mencetak modul untuk latihan.

## B.1 Kunci Latihan Identifikasi (6.2)

| # | String | Panjang | Jenis | Hasil |
|---|---|---|---|---|
| A | `a3VuY2kgbGVtYXJp` | 16 | Base64 | `kunci lemari` |
| B | `7275616e6720736572766572` | 24 | Hex biasa | `ruang server` |
| C | `FREIRE YNO` | 10 | ROT13 | `SERVER LAB` |
| D | `21232f297a57a5a743894a0e4a801fc3` | 32 | MD5 | `admin` (lewat lookup) |
| E | `8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918` | 64 | SHA-256 | `admin` (lewat lookup) |
| F | `bmlsYWkgdWppYW4=` | 16 | Base64 | `nilai ujian` |

**Poin diskusi wajib.** Bandingkan B dan D. Keduanya hanya berisi karakter hex, tetapi B panjangnya 24 dan D panjangnya 32. B bisa dibongkar langsung, D tidak bisa dan harus dicari. Ini pembeda yang paling sering meleset di kepala siswa pemula. Luangkan 2 menit khusus membahasnya.

Bandingkan juga D dan E. Kata aslinya sama persis, `admin`, tetapi hash-nya berbeda total karena algoritmanya berbeda. Bagus untuk menjelaskan bahwa hash terikat pada algoritmanya.

## B.2 Kunci Barang Bukti

| Kode | Jenis | Resep | Hasil |
|---|---|---|---|
| **BB1** | Base64 | `From Base64` | "Halo tim forensik. Kalian terlambat 3 jam. Semua berkas nilai sudah saya salin ke luar. Petunjuk berikutnya saya titipkan di barang bukti kedua, dan kunci masuk saya tinggalkan sebagai sidik jari di barang bukti ketiga." |
| **BB2** lapis 1 | Hexadecimal | `From Hex` | `V1BQe1k0QzE1X1EzWjFfWTRDMTVfRzNFTzBBVFg0RX0=` |
| **BB2** lapis 2 | Base64 | `From Base64` | `WPP{Y4C15_Q3Z1_Y4C15_G3EO0ATX4E}` |
| **BB2** lapis 3 | ROT13 | `ROT13` | `JCC{L4P15_D3M1_L4P15_T3RB0NGK4R}` |
| **BB4** | Caesar geser 5 | `ROT13` Amount 21 | `SELAMAT KALIAN LULUS UJIAN SANDI` |

**FLAG UTAMA:** `JCC{L4P15_D3M1_L4P15_T3RB0NGK4R}`

Resep lengkap CyberChef untuk BB2, berurutan:

```
1. From Hex        (Delimiter: Auto)
2. From Base64     (Alphabet: A-Za-z0-9+/=)
3. ROT13           (Amount: 13, kedua kotak centang aktif)
```

## B.3 Kunci Barang Bukti #3

| Akun | Hash | Algoritma | Kata sandi | Status |
|---|---|---|---|---|
| `admin_lab` | `0571749e2ac330a7455809c6b0e7af90` | MD5 | `sunshine` | terpecah |
| `operator` | `b7a875fc1ea228b9061041b7cec4bd3c52ab3ce3` | SHA-1 | `letmein` | terpecah |
| `kepala_lab` | `5a49035089ecef61e5c687d8bf294121` | MD5 | `T7#pQz9!vK2mLx4W` | **gagal, dan memang disengaja** |

Kata sandi `admin_lab` dan `operator` dipilih dari daftar sandi paling umum di dunia, sehingga dijamin ada di basis data CrackStation. Kata sandi `kepala_lab` dibuat acak sepanjang 16 karakter, sehingga dipastikan tidak ada di basis data mana pun.

> **Jangan beri tahu siswa isi sandi `kepala_lab`.** Nilai pelajarannya justru pada kegagalan itu. Kalau ada siswa yang bertanya, balikkan pertanyaannya: "Menurut kalian, kata seperti apa yang tidak akan pernah masuk daftar sejuta kata?"

## B.4 Rambu Jawaban Pertanyaan Konseptual

**Pertanyaan 1.**

(a) Analogi bebas, syaratnya tiga poin ini muncul: encoding tanpa kunci dan bisa dibalik, enkripsi butuh kunci dan bisa dibalik, hashing tidak bisa dibalik sama sekali. Tolak analogi yang menyamakan encoding dengan enkripsi.

(b) Base64 tidak butuh kunci apa pun, jadi siapa saja bisa mengembalikannya. Akibat memakainya untuk menyimpan password: siapa pun yang berhasil membaca basis data langsung memperoleh seluruh password dalam bentuk asli, tanpa perlu memecahkan apa pun. Siswa yang menyebut bahwa Base64 justru membuat programmer merasa aman padahal tidak, layak nilai tambahan.

(c) Hashing. Alasan tetap dipakai: untuk memverifikasi tanpa perlu menyimpan aslinya. Sistem cukup membandingkan hash sandi yang diketik dengan hash yang tersimpan. Jawaban lain yang diterima: memeriksa keutuhan berkas, seperti MD5 yang siswa pakai di Lab 02.

**Pertanyaan 2.**

(a) Analogi yang diterima: kado berlapis (buka kertas terluar dulu), bawang (kupas lapis demi lapis), boneka matryoshka, atau baju berlapis. Intinya: lapisan terakhir yang dipasang adalah lapisan pertama yang dibuka.

(b) ROT13 hanya bekerja pada huruf. Saat dijalankan di posisi pertama, input masih berupa teks hex yang mengandung huruf `a` sampai `f`. ROT13 menggeser huruf-huruf itu menjadi `n` sampai `s`, yang bukan karakter hex sah. Akibatnya From Hex di langkah berikutnya menerima data rusak dan gagal.

(c) `Reverse` harus diletakkan di posisi pertama, karena pembalikan adalah lapisan terluar yang dipasang paling akhir oleh penyusup. Cara mengetahuinya: hasil From Hex terlihat seperti Base64 tetapi tanda `=` muncul di **awal** string, bukan di akhir. Siswa yang menyebut petunjuk posisi `=` ini layak nilai penuh.

(d) Karena encoding tidak butuh kunci. Berapa pun lapisannya, semuanya bisa dibuka siapa saja yang telaten. Menambah lapisan hanya menambah waktu, bukan menambah keamanan. Ini disebut *security through obscurity*, dan bukan pengamanan sungguhan. Kaitannya dengan 1b: sama-sama kesalahan menganggap encoding sebagai pengaman.

**Pertanyaan 3.**

(a) CrackStation menyimpan daftar raksasa berisi pasangan kata dan hash-nya, dihitung lebih dulu. Saat menerima hash, ia hanya mencocokkan, bukan menghitung mundur. Istilah "membalikkan hash" keliru karena hash memang tidak bisa dibalik. Yang terjadi adalah pencocokan tebakan.

(b) Panjang hash ditentukan oleh algoritmanya, bukan oleh input. MD5 selalu menghasilkan 32 karakter, mau inputnya satu huruf atau satu buku. Kekuatan sandi ditentukan oleh seberapa sulit kata itu ditebak dan seberapa kecil kemungkinannya ada di daftar kata yang sudah dihitung orang.

(c) Dua cara yang diterima:
- **Salt**: menambahkan potongan acak unik per pengguna sebelum di-hash. Basis data lookup dibuat tanpa salt, jadi seluruh daftarnya langsung tidak cocok.
- **Algoritma lambat khusus password** seperti bcrypt, scrypt, atau Argon2. Algoritma ini sengaja dibuat lambat, sehingga menyusun daftar raksasa menjadi sangat mahal dan tidak praktis.
- Jawaban lain yang diterima: memaksa kebijakan sandi kuat, atau mengaktifkan autentikasi dua faktor sehingga sandi saja tidak cukup.

(d) Paragraf harus menyentuh dua sisi: **saluran** (pasang HTTPS, jangan kirim form login lewat HTTP polos, pelajaran Lab 01) dan **penyimpanan** (jangan simpan MD5 polos, pakai bcrypt dengan salt, pelajaran Lab 03). Jawaban yang hanya menyentuh satu sisi mendapat separuh nilai.

## B.5 Kesalahan yang Paling Sering Terjadi

| Gejala | Penyebab | Cara membimbing |
|---|---|---|
| Menyetorkan `WPP{...}` sebagai flag | berhenti di lapis 2 | tanyakan "format flag JCC diawali huruf apa?" |
| Menambahkan `To Base64`, bukan `From` | salah baca nama operasi | minta membaca ulang nama operasi dengan suara keras |
| Resep urut terbalik | menambah operasi asal urutan | minta menonaktifkan langkah satu per satu untuk melihat efeknya |
| Mencoba membongkar hash di CyberChef | mengira MD5 bisa dibalik | ulangi analogi jus buah, tunjukkan operasi `MD5` hanya membuat, bukan membongkar |
| Panik karena satu hash "Not found" | mengira dirinya salah | jelaskan bahwa kegagalan itu memang bagian soal |
| Output kosong di From Hex | delimiter salah | tunjukkan dropdown Delimiter, ubah Auto ke Space |
| Langsung memakai Magic tanpa berpikir | ingin cepat | ingatkan bobot nilai analisis di write-up |

## B.6 Rubrik Penilaian Write-Up

| Komponen | Bobot | Kriteria nilai penuh |
|---|---|---|
| Identifikasi format (Bagian 3.1) | 20% | Ciri yang diamati ditulis spesifik, bukan sekadar menyebut nama encoding |
| Alur penalaran (Bagian 3) | 30% | Tabel per lapis terisi, memuat minimal satu jalan buntu yang dilaporkan jujur |
| Reproduksi langkah (Bagian 4) | 20% | URL resep CyberChef dilampirkan, 4 tangkapan layar terbaca |
| Lampiran prompt AI (Bagian 6) | 15% | Prompt disalin utuh, refleksi penyensoran string terisi |
| Mitigasi & refleksi (Bagian 7) | 15% | Menyebut salt atau bcrypt, dan mengaitkan dengan pelajaran Lab 01 |

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# LAMPIRAN C: PANDUAN INSTRUKTUR

## C.1 Membuat Ulang Berkas Barang Bukti

Berkas `barang-bukti.txt` dibuat oleh `lab03/generate_challenges.py`. Skrip hanya memakai pustaka standar Python 3, tanpa dependensi apa pun.

```bash
cd lab03
python3 generate_challenges.py
```

Skrip mencetak kunci jawaban ke layar dan **memverifikasi sendiri** seluruh rantai decode sebelum selesai. Kalau ada satu rantai yang tidak tembus, skrip berhenti dengan pesan error, sehingga kalian tidak pernah membagikan soal yang mustahil dikerjakan.

Untuk menyimpan kunci ke berkas terpisah:

```bash
python3 generate_challenges.py --kunci
```

Perintah itu menulis `_kunci-jawaban.txt`. **Hapus berkas itu sebelum folder dibagikan ke siswa.**

## C.2 Membuat Varian Soal Baru

Ubah baris di bagian atas skrip, jalankan ulang, dan seluruh rantai dihitung ulang otomatis.

| Variabel | Efek perubahan |
|---|---|
| `FLAG` | teks yang dibungkus tiga lapis di BB2 |
| `BB1_PLAIN` | isi pesan penyusup di BB1 |
| `PASS_MD5`, `PASS_SHA1` | sandi yang **harus** ada di basis data lookup |
| `PASS_KUAT` | sandi yang **tidak boleh** ada di basis data mana pun |
| `BONUS_PLAIN` dan angka pada `rot(BONUS_PLAIN, 5)` | isi dan pergeseran Caesar di BB4 |

> ### ⚠️ Uji dulu sebelum dipakai
> Kalau kalian mengganti `PASS_MD5` atau `PASS_SHA1`, **wajib** cek dulu hash barunya di CrackStation sendiri. Kalau tidak ketemu, siswa akan buntu di Tantangan 3 tanpa sebab yang bisa dijelaskan. Sandi yang aman dipakai: `sunshine`, `letmein`, `password123`, `qwerty`, `iloveyou`, `dragon`, `monkey`, `football`.
>
> Untuk `PASS_KUAT`, buat sandi acak minimal 14 karakter bercampur simbol. Jangan memakai kata berbahasa Indonesia sekalipun, karena beberapa basis data lookup sudah memuat kata Indonesia umum.

## C.3 Rencana Cadangan Kalau Internet Mati

Bagian ini penting. Jaringan lab sekolah sering tidak stabil, dan modul ini bergantung pada dua situs.

**Untuk CyberChef:** unduh berkas mandiri dari halaman rilis GitHub CyberChef sebelum hari-H, simpan di flashdisk. Berkasnya satu file HTML berukuran sekitar 15 MB. Buka langsung di browser, seluruh fitur berjalan tanpa internet, termasuk From Base64, From Hex, ROT13, dan Magic.

**Untuk CrackStation:** tidak ada versi luring. Dua pilihan pengganti:

*Pilihan 1, tabel cetak.* Siapkan tabel berikut di kertas, bagikan sebagai "hasil kueri basis data" yang sudah dijalankan pembina:

| Hash | Algoritma | Hasil |
|---|---|---|
| `0571749e2ac330a7455809c6b0e7af90` | MD5 | `sunshine` |
| `b7a875fc1ea228b9061041b7cec4bd3c52ab3ce3` | SHA-1 | `letmein` |
| `5a49035089ecef61e5c687d8bf294121` | MD5 | *Not found* |

*Pilihan 2, basis data mini buatan sendiri.* Cara ini justru lebih mendidik karena siswa melihat mekanismenya secara langsung, bukan sebagai kotak hitam.

```bash
# Buat daftar sandi umum
cat > /tmp/sandi-umum.txt <<'EOF'
123456
password
sunshine
letmein
qwerty
iloveyou
admin
dragon
EOF

# Bangun "basis data lookup" mini
while read -r kata; do
  printf '%s  %s  %s\n' \
    "$(printf '%s' "$kata" | md5sum | cut -d' ' -f1)" \
    "$(printf '%s' "$kata" | sha1sum | cut -d' ' -f1)" \
    "$kata"
done < /tmp/sandi-umum.txt > /tmp/lookup.txt

# Cari sebuah hash di dalamnya
grep '0571749e2ac330a7455809c6b0e7af90' /tmp/lookup.txt
```

Setelah siswa melihat skrip 10 baris ini bekerja, konsep "CrackStation cuma buku telepon raksasa" langsung masuk akal. Jalankan juga pencarian untuk hash `kepala_lab` supaya mereka melihat sendiri hasilnya kosong.

## C.4 Menjawab Pertanyaan Sulit dari Siswa

| Pertanyaan yang mungkin muncul | Jawaban singkat |
|---|---|
| "Kenapa MD5 masih dipakai kalau lemah?" | Warisan sistem lama. MD5 masih memadai untuk memeriksa keutuhan berkas, tetapi sudah lama tidak layak untuk password. |
| "Kalau hash tidak bisa dibalik, kenapa ada situs yang mengaku bisa?" | Mereka mencocokkan, bukan membalikkan. Coba beri mereka hash sandi acak, dan situs itu pasti gagal. |
| "Apa bedanya ROT13 dan enkripsi sungguhan?" | Kuncinya tetap dan diketahui semua orang, yaitu 13. Enkripsi sungguhan punya kunci rahasia yang bisa berganti. |
| "Bisakah dua kata berbeda menghasilkan hash sama?" | Bisa, disebut collision, dan itu salah satu alasan MD5 ditinggalkan. Untuk lab ini abaikan dulu. |
| "Kenapa CyberChef tidak punya operasi 'From MD5'?" | Karena operasi seperti itu mustahil ada. Perhatikan bahwa MD5 ada di kategori Hashing, bukan Data format. |

## C.5 Daftar Periksa Sebelum Lab Dimulai

```
[ ] gchq.github.io/CyberChef terbuka di kedua laptop siswa
[ ] crackstation.net terbuka dan CAPTCHA-nya berfungsi
[ ] Salinan luring CyberChef tersedia di flashdisk sebagai cadangan
[ ] barang-bukti.txt tersalin, ukuran 2.064 byte
[ ] _kunci-jawaban.txt SUDAH DIHAPUS dari folder siswa
[ ] Lampiran B tidak ikut tercetak di modul siswa
[ ] prompt-log.md sudah dibuka di text editor
[ ] Tabel cadangan hash sudah dicetak, untuk jaga-jaga internet mati
[ ] Timer 60 menit disiapkan
```

## C.6 Rencana Lanjutan

| Modul | Judul | Fokus |
|---|---|---|
| LAB 01 ✅ | The Wire Sniffer | Sniffing HTTP, Follow TCP Stream |
| LAB 02 ✅ | Needle in a Haystack | Filter lanjutan, DNS tracking, Export Objects |
| LAB 03 ✅ | The Secret Decoder | Encoding berlapis, CyberChef, hash lookup |
| LAB 04 | The Hidden Layer | Steganografi, metadata EXIF, berkas dalam berkas |
| LAB 05 | Broken Login | Logika autentikasi web, cookie, dan JWT |
| LAB 06 | Simulasi Penyisihan | 15 soal, 3 jam, write-up wajib |

> **Catatan penyambung ke LAB 04.** Modul berikutnya memakai kembali keterampilan Base64 dari lab ini, tetapi stringnya tersembunyi di dalam berkas gambar. Siswa yang tuntas di LAB 03 akan mengenali polanya dalam hitungan detik.

***

**Selamat membongkar. Setiap sandi yang dibuat manusia, bisa dibaca manusia lain.**

*Modul ini disusun untuk pembinaan internal Tim CTF SMK Maskumambang 1, Pondok Pesantren Maskumambang.*
