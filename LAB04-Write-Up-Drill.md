# LAB 04: THE WRITE-UP DRILL & FLAG HUNTING
### Simulasi Mini CTF dan Standardisasi Laporan Resmi

**Program Pembinaan Tim CTF SMK Maskumambang 1**
Persiapan **Jatim Cybersecurity Competition (JCC) 2026**, kategori SMA/SMK Sederajat
Kelas Sasaran: X (usia 15-16 tahun) | Level: **Lab Pamungkas Fase Fondasi**
Prasyarat: **LAB 01, LAB 02, dan LAB 03** sudah tuntas
Versi Modul: 1.0 | Tanggal: 05 September 2026

***

## DAFTAR ISI

1. [Informasi Modul & Target Capaian](#bagian-1-informasi-modul-target-capaian)
2. [Briefing Tantangan Simulasi: The Final Drill](#bagian-2-briefing-tantangan-simulasi-the-final-drill)
3. [Strategi Manajemen Tim](#bagian-3-strategi-manajemen-tim-sre-competitive-mindset)
4. [Panduan Penyusunan Prompt AI](#bagian-4-panduan-penyusunan-prompt-ai-sesuai-juknis-jcc-2026)
5. [Template Dokumen Write-Up Resmi](#bagian-5-template-dokumen-write-up-resmi)
6. [Lembar Evaluasi & Rubrik Penilaian Mandiri](#bagian-6-lembar-evaluasi-rubrik-penilaian-mandiri)
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
| **Kode Modul** | LAB-04 / SIMULASI-PENYISIHAN |
| **Judul** | The Write-Up Drill & Flag Hunting |
| **Kategori CTF** | Gabungan: Forensics + Cryptography |
| **Tingkat Kesulitan** | ★★★☆☆ (Medium, setara soal nomor 8-12 di penyisihan) |
| **Format** | **Time-Attack**, 45 menit tantangan + 30 menit write-up |
| **Berkas Simulasi** | `lab04/simulasi_jcc.pcapng` (66 paket, 16.972 byte) |
| **Modul Prasyarat** | LAB 01, LAB 02, LAB 03 |

## 1.2 Kenapa Modul Ini Berbeda

Tiga lab sebelumnya melatih **jari dan mata** kalian: menyaring paket, mengekstrak berkas, membongkar sandi. Modul ini melatih tiga hal lain yang justru menentukan peringkat akhir di JCC 2026.

| Yang dilatih | Kenapa menentukan |
|---|---|
| **Manajemen waktu** | Babak penyisihan berisi lebih dari 15 soal. Tim yang menghabiskan 40 menit di satu soal akan kalah dari tim yang melewatinya dan mengerjakan tiga soal lain. |
| **Kolaborasi dua orang** | Dua siswa mengerjakan satu layar yang sama adalah pemborosan. Pembagian peran yang jelas melipatgandakan kecepatan. |
| **Dokumentasi presisi** | Panitia mewajibkan write-up. Flag benar tanpa write-up rapi tetap kehilangan poin besar. Tangkapan layar yang lupa diambil tidak bisa diulang setelah waktu habis. |

> ### ◆ Kenyataan pahit yang harus kalian terima sekarang
> Tim yang menemukan 12 flag tetapi write-up-nya berantakan sering kalah dari tim yang menemukan 9 flag dengan laporan runtut. Panitia menilai **proses**, bukan cuma hasil. Modul ini melatih bagian yang paling sering diremehkan tim pemula.

## 1.3 Alokasi Waktu (Total 75 Menit)

| Fase | Waktu | Kegiatan | Aturan |
|---|---|---|---|
| **Persiapan** | T-5 sampai T-0 | Buka Wireshark, CyberChef, draf write-up, timer | Belum boleh membuka berkas soal |
| **Ronde 1** | 00:00 - 45:00 | Mengerjakan tantangan, mengambil tangkapan layar, mencatat | Timer berjalan, tidak ada jeda |
| **Batas kritis** | 40:00 | **Berhenti mencari.** Rapikan catatan meski flag belum ketemu | Wajib dipatuhi |
| **Ronde 2** | 45:00 - 75:00 | Menyusun write-up resmi | Tidak boleh membuka Wireshark lagi |
| **Debrief** | 75:00 - 85:00 | Evaluasi bersama pembina | Opsional tetapi sangat disarankan |

**Titik pemeriksaan selama Ronde 1.** Pembina mengumumkan sisa waktu dengan suara keras:

```
  10:00 berjalan  ->  "Sudah ketemu domain mencurigakannya?"
  25:00 berjalan  ->  "Sudah ketemu request POST-nya?"
  35:00 berjalan  ->  "Sudah dapat lapis pertama payload?"
  40:00 berjalan  ->  "BERHENTI MENCARI. Rapikan catatan sekarang."
```

Pengumuman ini bukan gangguan. Di lomba sungguhan, tidak ada yang mengingatkan kalian. Latihan ini membangun jam internal di kepala kalian.

## 1.4 Capaian Pembelajaran

| Kode | Rumusan Capaian (terukur) | Bukti Ketercapaian |
|---|---|---|
| **LO-1** | Membagi tugas dalam tim 2 orang sesuai kartu peran, tanpa dua orang mengerjakan langkah yang sama, sepanjang 45 menit. | Lembar Log Aktivitas terisi dua kolom terpisah |
| **LO-2** | Mengambil minimal 4 tangkapan layar bukti pada momen yang tepat, tanpa perlu mengulang analisis. | Berkas gambar tersimpan berurutan dengan nama jelas |
| **LO-3** | Menyelesaikan rantai tantangan lintas modul (jaringan, ekstraksi, decoding) dalam 45 menit. | Flag ditemukan dan tercatat |
| **LO-4** | Menerapkan aturan eskalasi waktu: bertahan sendiri maksimal 7 menit sebelum bertanya ke AI secara terstruktur. | Kolom waktu di Log Prompt AI menunjukkan jarak wajar |
| **LO-5** | Menyusun write-up resmi lengkap 6 bagian dalam 30 menit, termasuk tabel riwayat prompt AI. | Dokumen write-up selesai sebelum timer habis |
| **LO-6** | Melakukan pemeriksaan mandiri sebelum submit memakai checklist 12 butir. | Checklist tercentang dan ditandatangani kedua anggota |

## 1.5 Prasyarat Alat

| Alat | Keperluan | Cek kesiapan |
|---|---|---|
| **Wireshark 4.0+** | membedah `simulasi_jcc.pcapng` | Preferences → Protocols → TCP → reassembly tercentang |
| **CyberChef** | membongkar payload berlapis | `gchq.github.io/CyberChef` termuat, atau salinan luring siap |
| **CrackStation** | tantangan bonus | `crackstation.net` termuat |
| **Text editor** | menulis draf write-up | Berkas `draf-writeup.md` **sudah terbuka sebelum timer mulai** |
| **Alat tangkapan layar** | bukti tiap langkah | Windows: `Win + Shift + S`. Linux: `PrtSc` atau Flameshot |
| **Timer** | menjaga ritme | HP dengan hitung mundur, taruh di posisi terlihat keduanya |
| **Folder kerja** | menampung bukti | `Simulasi-LAB04/` di Desktop, sudah dibuat |

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# BAGIAN 2: BRIEFING TANTANGAN SIMULASI: THE FINAL DRILL

## 2.1 Skenario

```
=====================================================================
  LAPORAN INSIDEN #2026-0227-01           KLASIFIKASI: SANGAT RAHASIA
  Unit Teknologi Informasi, SMK Maskumambang 1
  Waktu kejadian : Jumat, 27 Februari 2026, 09:20 WIB
  Pelapor        : Sistem monitoring perimeter
  Status         : SIMULASI LATIHAN TIM CTF
=====================================================================
```

Jumat pagi. Seorang staf Lab Komputer membuka halaman pengumuman internal sekolah dan membaca kabar bahwa printer lab bermasalah. Di halaman itu ada tautan untuk mengunduh panduan update driver.

Staf itu mengklik tautannya. Ia tidak memperhatikan satu hal: tautan itu **tidak menuju server sekolah**, melainkan ke sebuah alamat di luar.

Dua belas detik setelah unduhan selesai, workstation itu mengirimkan sesuatu ke server yang sama. Data yang dikirim sudah disamarkan, sehingga tidak ada satu pun kata yang bisa dibaca langsung di rekaman.

Perekam jaringan sempat menangkap **66 paket** dari kejadian itu, tersimpan sebagai `simulasi_jcc.pcapng`.

Tim kalian ditugaskan membongkar apa yang dikirim keluar.

> ### ◆ Peringatan dari pembina
> Rantai tantangan ini sengaja memakai **seluruh keterampilan** dari tiga lab sebelumnya. Kalau kalian buntu di satu titik, jangan mengarang teknik baru. Buka kembali kartu contekan lab yang bersangkutan. Semua yang kalian butuhkan sudah pernah diajarkan.

## 2.2 Peta Jaringan

```
    JARINGAN SEKOLAH                       |        LUAR
                                           |
   [Workstation Staf Lab]                  |
      192.168.10.58                        |
      MAC 08:00:27:c4:d1:09                |
            |                              |
            | (1) buka pengumuman          |
            v                              |
   [Server Intranet]                       |
      192.168.10.20                        |
      intranet.smkmaska.local              |
      halaman berisi tautan unduhan  ------------> ???
            |                              |
            | (2) tanya alamat domain      |
            v                              |
   [DNS Server]                            |
      192.168.10.1                         |
            |                              |
            | (3) unduh berkas             |
            | (4) kirim data keluar        |
            v                              |
   [Gateway] --------------------------------> [Server Luar]
                                           |     45.83.220.114
                                           |     port 80, HTTP polos
```

## 2.3 Daftar Tantangan dan Bobot Nilai

Kerjakan berurutan. Setiap jawaban benar wajib disertai **nomor paket** sebagai bukti.

| # | Tantangan | Modul asal | Nilai |
|---|---|---|---|
| **T1** | Sebutkan nama domain mencurigakan yang di-query workstation, beserta nomor paketnya. | LAB 02 | 10 |
| **T2** | Sebutkan alamat IP server luar dan halaman internal yang menjadi pintu masuknya. | LAB 02 | 10 |
| **T3** | Tarik keluar berkas yang diunduh staf memakai Export Objects. Sebutkan nama, ukuran, dan MD5-nya. | LAB 02 | 15 |
| **T4** | Temukan request **POST ke endpoint rahasia**. Sebutkan URL lengkap dan nomor paketnya. | LAB 01 | 15 |
| **T5** | Baca isi body POST itu. Salin nilai parameter `data`. | LAB 01 | 10 |
| **T6** | Bongkar payload berlapis di parameter `data` sampai ketemu **FLAG**. Tulis urutan resepnya. | LAB 03 | 30 |
| **T7** | Ada satu POST lain di rekaman ini yang **bukan** target. Sebutkan mana, dan jelaskan cara kalian membedakannya. | LAB 01 | 10 |

**Bonus (15 poin):** parameter `token` di body POST berisi hash MD5. Temukan kata aslinya.

**Total: 100 poin + 15 bonus**

## 2.4 Format Flag

```
JCC{huruf_kecil_angka_dan_garis_bawah}
```

> ### ▲ Peringatan penting
> Flag di simulasi ini **tidak ada dalam bentuk polos** di berkas `.pcapng`. Filter `frame contains "JCC"` akan mengembalikan **nol hasil**. Itu bukan kesalahan kalian.
>
> Banyak tim pemula panik saat filter andalannya gagal, lalu membuang 10 menit mengulang langkah yang sama. Kalau filter itu kosong, artinya flag tersamar, dan tugas kalian adalah mencari bentuk tersamarnya, bukan mengulangi pencarian yang sama.

## 2.5 Alur yang Diharapkan

```
   TAHAP 1 (Jaringan)                    perkiraan 12 menit
   filter dns  ->  temukan domain janggal
   filter http ->  petakan seluruh percakapan
                            |
                            v
   TAHAP 2 (Ekstraksi)                   perkiraan 8 menit
   File > Export Objects > HTTP
   tarik berkas yang diunduh, buka, baca isinya
                            |
                            v
   TAHAP 3 (Payload)                     perkiraan 10 menit
   filter http.request.method == "POST"
   Follow TCP Stream pada POST yang benar
   salin nilai parameter data
                            |
                            v
   TAHAP 4 (Decoding)                    perkiraan 15 menit
   CyberChef, kupas lapis demi lapis
   berhenti ketika muncul JCC{...}
```

Angka menit di atas adalah **anggaran waktu**, bukan target. Kalau satu tahap melewati anggarannya, itu sinyal untuk memakai aturan eskalasi di Bagian 3.4.

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# BAGIAN 3: STRATEGI MANAJEMEN TIM (SRE & COMPETITIVE MINDSET)

## 3.1 Kenapa Dua Orang di Satu Layar Adalah Pemborosan

Bayangkan dua montir memperbaiki satu motor. Kalau keduanya sama-sama membuka baut yang sama, hasilnya bukan dua kali lebih cepat, melainkan saling menghalangi.

Tim CTF pemula sering melakukan itu: dua orang duduk berdempetan menatap satu jendela Wireshark, sama-sama bingung, sama-sama diam. Waktu berjalan, tidak ada yang mencatat, dan tidak ada satu pun tangkapan layar terambil.

Pembagian peran menyelesaikan masalah itu.

## 3.2 Kartu Peran

### 🅐 NAVIGATOR / ANALYST (Siswa 1)

```
   +-----------------------------------------------------------+
   |  NAVIGATOR / ANALYST                                       |
   |                                                            |
   |  ALAT UTAMA   : Wireshark                                  |
   |  TUGAS        : membedah paket, menyaring, menemukan       |
   |                 titik kejanggalan                          |
   |  YANG DIUCAPKAN : temuan, dengan suara keras               |
   |  YANG TIDAK BOLEH : diam saat menemukan sesuatu            |
   +-----------------------------------------------------------+
```

**Tugas rinci:**
1. Membuka berkas `.pcapng` dan memetakan isinya lewat **Statistics → Protocol Hierarchy**.
2. Menjalankan filter secara bertahap: `dns`, lalu `http`, lalu `http.request.method == "POST"`.
3. Menjalankan **Follow TCP Stream** dan **Export Objects**.
4. **Membacakan setiap temuan dengan suara keras** supaya pasangan bisa mencatat tanpa menoleh.

**Contoh kalimat yang harus diucapkan:**

> "Paket 18, query DNS ke `cdn-update.paket-gratis.tk`, dijawab `45.83.220.114`. Catat."
> "Paket 37, POST ke `/api/v2/collect`. Aku buka Follow Stream sekarang."
> "Parameter `data` isinya panjang, aku bacakan pelan-pelan, siap?"

### 🅑 SOLVER & SCRIBE (Siswa 2)

```
   +-----------------------------------------------------------+
   |  SOLVER & SCRIBE                                           |
   |                                                            |
   |  ALAT UTAMA   : CyberChef, CrackStation, chatbot AI,       |
   |                 text editor draf write-up                  |
   |  TUGAS        : membongkar sandi, mencatat, memotret       |
   |  YANG DIUCAPKAN : konfirmasi setiap catatan                |
   |  YANG TIDAK BOLEH : menunda pencatatan sampai nanti        |
   +-----------------------------------------------------------+
```

**Tugas rinci:**
1. Menyalakan text editor berisi `draf-writeup.md` **sebelum timer mulai**.
2. Mencatat setiap temuan yang dibacakan Navigator, lengkap dengan nomor paket dan jam.
3. Mengambil tangkapan layar pada setiap momen kunci, lalu menamainya berurutan.
4. Menjalankan CyberChef dan CrackStation.
5. Menyusun prompt ke chatbot AI ketika aturan eskalasi terpicu, lalu menyalin prompt itu ke log.

**Contoh kalimat yang harus diucapkan:**

> "Tercatat, paket 18, domain `cdn-update.paket-gratis.tk`. Sudah kupotret."
> "Ulangi 8 karakter terakhir, aku belum yakin antara angka nol dan huruf O."
> "Lapis pertama sudah terbuka, hasilnya hex. Aku lanjut ke lapis dua."

### Aturan tukar peran

Di menit **25:00**, kedua siswa **bertukar peran selama 5 menit**. Alasannya dua:

1. Mata yang segar sering menangkap kejanggalan yang terlewat mata yang sudah lelah.
2. Di lomba sungguhan, salah satu anggota bisa mendadak buntu. Tim yang keduanya bisa mengoperasikan semua alat tidak akan lumpuh.

## 3.3 Protokol Komunikasi

Tiga aturan komunikasi yang membuat tim dua orang jauh lebih cepat.

### Aturan 1: Ucapkan, jangan tunjuk

Menunjuk layar memaksa pasangan menoleh dan kehilangan fokus. Ucapkan temuan dengan kalimat lengkap berisi nomor paket.

| ❌ Buruk | ✅ Baik |
|---|---|
| "Eh, ini lho, yang ini." | "Paket 37, POST ke slash api slash v2 slash collect." |
| "Ada yang aneh." | "Domain berakhiran titik t k, paket 18, kemungkinan mencurigakan." |

### Aturan 2: Ulang balik setiap data penting

Ketika Navigator membacakan string panjang, Scribe **mengulang balik** apa yang ia tulis. Teknik ini dipakai pilot dan petugas menara bandara, dan alasannya sama: satu karakter salah membuat seluruh pekerjaan gagal.

```
   Navigator : "empat lima titik delapan tiga titik dua dua nol titik satu satu empat"
   Scribe    : "empat lima titik delapan tiga titik dua dua nol titik satu satu empat, benar?"
   Navigator : "benar"
```

Khusus untuk string sangat panjang seperti payload Base64, **jangan dibacakan**. Salin lewat tombol Copy di jendela Follow TCP Stream, lalu tempel langsung ke CyberChef. Membacakan 104 karakter dengan suara adalah undangan bagi kesalahan.

### Aturan 3: Satu suara untuk keputusan waktu

Navigator memegang kendali arah teknis. **Scribe memegang kendali waktu.** Ketika Scribe berkata "sudah 7 menit, kita eskalasi", Navigator wajib berhenti berdebat dan mengikuti.

Pemisahan ini mencegah situasi paling umum di lomba: dua orang sama-sama terjebak, sama-sama merasa "sebentar lagi ketemu", dan kehilangan 20 menit.

## 3.4 Manajemen Waktu: Kapan Bertahan, Kapan Bertanya

### Aturan 7 Menit

```
   Menemui jalan buntu
            |
            v
   +--------------------------+
   |  Sudah berapa lama?      |
   +--------------------------+
       |              |
    < 7 menit      >= 7 menit
       |              |
       v              v
   TERUS COBA     WAJIB ESKALASI
   sendiri        (lihat tangga di bawah)
```

Tujuh menit dipilih karena masuk akal untuk soal setingkat penyisihan. Kurang dari itu, kalian belum benar-benar mencoba. Lebih dari itu, kalian sedang membuang waktu yang bisa dipakai untuk soal lain.

### Tangga Eskalasi

Naik satu anak tangga setiap kali buntu, jangan melompat langsung ke atas.

| Anak tangga | Tindakan | Waktu maksimal |
|---|---|---|
| **1** | Baca ulang kartu contekan lab yang bersangkutan | 2 menit |
| **2** | Tanya pasangan: "menurutmu aku melewatkan apa?" | 2 menit |
| **3** | Ubah sudut pandang: coba filter lain, coba operasi lain | 3 menit |
| **4** | Susun prompt terstruktur ke chatbot AI (Bagian 4) | 4 menit |
| **5** | **Tinggalkan soal ini**, kerjakan soal lain, kembali nanti | segera |

> ### ▲ Anak tangga 5 adalah yang paling sulit dan paling penting
> Meninggalkan soal terasa seperti menyerah. Sebenarnya tidak. Di babak penyisihan dengan lebih dari 15 soal, meninggalkan satu soal sulit untuk mengerjakan tiga soal mudah adalah **keputusan matematis yang benar**.
>
> Otak kalian juga terus bekerja di latar belakang. Banyak tim menemukan jawaban soal yang ditinggalkan justru saat mengerjakan soal lain.

### Anggaran Waktu Per Tahap

Tulis anggaran ini di kertas dan taruh di samping laptop.

| Tahap | Anggaran | Kalau lewat 5 menit dari anggaran |
|---|---|---|
| Tahap 1, jaringan | 12 menit | naik ke anak tangga 3 |
| Tahap 2, ekstraksi | 8 menit | naik ke anak tangga 4 |
| Tahap 3, payload | 10 menit | naik ke anak tangga 4 |
| Tahap 4, decoding | 15 menit | naik ke anak tangga 4, lalu 5 |

## 3.5 Protokol Panik

Panik adalah musuh terbesar tim pemula. Gejalanya: mengklik cepat tanpa arah, mengulang filter yang sama tiga kali, dan berhenti mencatat.

Kalau salah satu anggota mengenali gejala itu pada dirinya atau pasangannya, ucapkan kata sandi tim, misalnya **"REM"**. Begitu kata itu diucapkan:

```
  1. Kedua tangan lepas dari keyboard. Tarik napas, hitung sampai lima.
  2. Scribe membacakan keras seluruh temuan yang sudah tercatat.
  3. Tanyakan satu pertanyaan: "apa yang SUDAH kita tahu?"
  4. Tentukan satu langkah berikutnya, hanya satu.
  5. Kembali bekerja.
```

Prosedur ini memakan 60 detik dan sering menyelamatkan 15 menit.

## 3.6 Aturan Tangkapan Layar

Tangkapan layar yang lupa diambil **tidak bisa diulang** setelah waktu habis. Ini kesalahan paling mahal dan paling sering terjadi.

### Kapan wajib memotret

| Momen | Yang harus terlihat di gambar |
|---|---|
| Setelah filter berhasil | kotak filter berisi teks filternya, plus daftar paket hasilnya |
| Saat menemukan domain janggal | panel Packet Details terbuka pada baris nama domain |
| Jendela Export Objects terbuka | seluruh tabel berisi daftar berkas |
| Follow TCP Stream pada POST | isi body yang memuat parameter penting |
| Setiap lapis CyberChef terbuka | panel Recipe dan panel Output sekaligus |
| Hasil CrackStation | tabel hasil beserta kolom Result |

### Aturan penamaan berkas

```
   01-filter-dns.png
   02-domain-mencurigakan.png
   03-export-objects.png
   04-follow-stream-post.png
   05-cyberchef-lapis1.png
   06-cyberchef-lapis2.png
   07-cyberchef-flag.png
   08-crackstation.png
```

Penomoran di depan membuat berkas terurut sendiri di folder, dan urutan itulah kerangka bagian "Langkah Penyelesaian" di write-up kalian. Scribe tinggal menuliskan kalimat di antara gambar-gambar itu.

> ### ◆ Kebiasaan yang membedakan tim juara
> Potret **kotak filter beserta hasilnya dalam satu gambar**. Tangkapan layar yang hanya menampilkan daftar paket tanpa memperlihatkan filternya tidak membuktikan apa pun kepada juri. Mereka tidak bisa menebak filter apa yang kalian pakai.

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# BAGIAN 4: PANDUAN PENYUSUNAN PROMPT AI SESUAI JUKNIS JCC 2026

## 4.1 Aturan Panitia

> **Chatbot AI boleh dipakai di babak penyisihan, dengan syarat seluruh riwayat prompt dan alur penalaran tim dilampirkan dalam write-up resmi.**

Aturan ini bukan formalitas. Juri membacanya, dan lampiran prompt kalian **mengubah nilai** bagian analisis.

## 4.2 Do's and Don'ts

### ✅ BOLEH dan disarankan

| Jenis pertanyaan | Contoh |
|---|---|
| **Menjelaskan pesan error** | "Wireshark menolak filter saya dengan kotak merah. Apa yang salah dari sintaks ini?" |
| **Mengenali jenis sandi** | "String ini hanya berisi 0-9 dan a-f, panjang 78 karakter. Jenis encoding apa yang mungkin?" |
| **Sintaks filter** | "Bagaimana menulis filter Wireshark untuk request POST menuju satu IP tertentu?" |
| **Arti kode status** | "Apa beda respons 302 dan 200 dalam konteks investigasi?" |
| **Konsep di balik teknik** | "Kenapa Export Objects butuh reassembly TCP dinyalakan?" |
| **Merapikan kalimat laporan** | "Rapikan paragraf ini tanpa mengubah temuan teknisnya." |

### ❌ TIDAK disarankan

| Kebiasaan buruk | Kenapa merugikan |
|---|---|
| **Menempel seluruh teks soal mentah-mentah** | AI tidak memegang berkas kalian. Ia akan **berhalusinasi**, mengarang nomor paket dan nama berkas yang tidak ada, dan kalian membuang waktu memverifikasi jawaban palsu. |
| **Bertanya "apa flagnya?"** | Mustahil dijawab benar. AI tidak bisa membuka `.pcapng` kalian. |
| **Menempelkan flag utuh** | Tidak ada gunanya, dan berisiko dianggap membocorkan jawaban. |
| **Menyalin jawaban AI tanpa verifikasi** | Kalau AI salah, kalian ikut salah, dan lampiran prompt memperlihatkan kalian tidak memeriksa. |
| **Bertanya tanpa konteks** | "Kenapa error?" tanpa menyebut error-nya menghasilkan jawaban umum yang tidak menolong. |

> ### ▲ Tentang halusinasi AI
> Menempelkan soal panjang tanpa konteks adalah penyebab halusinasi paling umum. AI akan tetap menjawab dengan nada percaya diri, lengkap dengan nomor paket yang terdengar meyakinkan, padahal ia mengarang seluruhnya.
>
> Cara mengenalinya: **AI menyebut detail yang tidak pernah kalian berikan.** Kalau ia menyebut "paket nomor 42" padahal kalian tidak pernah mengirim daftar paket, itu karangan. Verifikasi setiap angka di Wireshark kalian sendiri sebelum menuliskannya di write-up.

## 4.3 Rumus Prompt yang Berhasil

```
   [PERAN]     Kamu adalah ...
      +
   [KONTEKS]   Saya sedang ... (situasi, bukan isi soal)
      +
   [DATA]      Potongan kecil saja, atau deskripsi bentuknya
      +
   [SUDAH DICOBA]  Apa yang gagal, beserta gejalanya
      +
   [PERTANYAAN]    Spesifik, bernomor
      +
   [FORMAT]    Bentuk jawaban yang kalian inginkan
      +
   [BATASAN]   "Jangan berikan jawaban akhir, saya ingin mengerjakannya sendiri"
```

Bagian **[SUDAH DICOBA]** adalah yang paling sering dilupakan, padahal paling menentukan. Prompt yang menyertakan percobaan gagal mengubah AI dari penebak menjadi pendiagnosis.

## 4.4 Contoh Prompt Siap Pakai Saat Simulasi

### Prompt A: Filter Wireshark ditolak

```text
Kamu adalah instruktur Wireshark untuk siswa SMK kelas 10.

KONTEKS:
Saya menganalisis rekaman jaringan berisi 66 paket. Saya ingin menampilkan
hanya request POST yang menuju satu alamat IP tertentu di luar jaringan lokal.

SUDAH SAYA COBA:
    ip.dst = 45.83.220.114 and http.request.method = POST
Gejalanya: kotak filter berwarna merah dan tidak ada paket yang tampil.

PERTANYAAN:
1. Ada berapa kesalahan sintaks di filter saya, dan di bagian mana?
2. Tulis versi yang benar.
3. Kenapa Wireshark memakai == dan bukan = untuk perbandingan?

FORMAT JAWABAN:
Tabel dua kolom "Filter" dan "Penjelasan". Bahasa Indonesia.
```

### Prompt B: Mengenali bentuk hasil decode

```text
Kamu adalah mentor CTF kategori Cryptography untuk pemula.

KONTEKS:
Saya membongkar payload berlapis di CyberChef. Saya tidak mengirimkan isi
stringnya, hanya bentuk hasil di tiap tahap.

BENTUK HASIL:
- Input awal          : huruf besar-kecil bercampur angka, panjang 104,
                        kelipatan 4, tanpa tanda sama dengan di ujung
- Setelah operasi ke-1: hanya angka 0-9 dan huruf a-f, panjang 78
- Setelah operasi ke-2: teks terbaca, tetapi urutannya terasa terbalik
                        karena diakhiri tiga huruf besar C C J

PERTANYAAN:
1. Operasi apa yang tepat untuk tahap ketiga, dan petunjuk mana yang
   paling menentukan?
2. Hasil tahap 1 panjangnya 78 karakter hex. Kenapa itu bukan hash?
3. Bagaimana cara saya memastikan tidak ada lapisan keempat?

FORMAT JAWABAN:
Poin bernomor, maksimal 3 kalimat per poin.
JANGAN membongkar isi stringnya, saya ingin mengerjakannya sendiri.
```

### Prompt C: Memeriksa kelengkapan write-up

Prompt ini dipakai di **Ronde 2**, bukan saat mencari flag.

```text
Kamu adalah juri lomba CTF tingkat SMA/SMK.

KONTEKS:
Saya menulis write-up untuk soal forensik jaringan. Panitia menilai
kelengkapan, keruntutan, dan kejujuran pelaporan proses.

STRUKTUR WRITE-UP SAYA SAAT INI:
1. Identitas tim
2. Deskripsi soal
3. Langkah penyelesaian dengan 7 tangkapan layar
4. Flag
5. Lampiran prompt AI

PERTANYAAN:
1. Bagian penting apa yang biasanya dinilai juri tetapi belum ada di
   struktur saya?
2. Apa tanda write-up yang terlihat "hanya menyalin hasil" di mata juri?
3. Sebutkan 3 kesalahan paling umum di write-up tim pemula.

FORMAT JAWABAN:
Daftar bernomor, singkat. Bahasa Indonesia.
```

## 4.5 Format Pencatatan Log Prompt AI

Buka berkas `prompt-log.md` **sebelum timer mulai**. Setiap kali mengirim prompt, catat langsung.

```markdown
### Prompt #1
- Waktu kirim  : 09:34 WIB   (menit ke-14 simulasi)
- Model AI     : Claude / ChatGPT
- Pemicu       : filter Wireshark ditolak, sudah mencoba 7 menit
- Prompt       : (salin persis, jangan diringkas, jangan dirapikan)
- Inti jawaban : (1-2 kalimat)
- Diverifikasi : ya / tidak, dan bagaimana cara memverifikasinya
- Keputusan    : (apa yang tim lakukan setelah membaca jawaban)
```

Kolom **Diverifikasi** adalah yang paling bernilai di mata juri. Tim yang menuliskan "AI menyarankan filter X, saya uji di Wireshark dan hasilnya 5 paket, cocok dengan dugaan saya" memperlihatkan sikap ilmiah. Tim yang menyalin bulat-bulat tidak.

> ### ◆ Kalau AI ternyata salah, tulis saja
> Melaporkan bahwa jawaban AI keliru dan bagaimana kalian mengetahuinya **menaikkan** nilai kalian, bukan menurunkan. Itu bukti kalian berpikir, bukan sekadar menyalin.

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# BAGIAN 5: TEMPLATE DOKUMEN WRITE-UP RESMI

> **Cara pakai:** salin seluruh blok di bawah ke text editor **sebelum timer mulai**, simpan sebagai `writeup-lab04-[namatim].md`. Isi sambil berjalan, jangan menunggu selesai. Ekspor ke PDF sebelum mengumpulkan.

````markdown
# WRITE-UP RESMI JCC 2026

## IDENTITAS TIM
| Field | Isian |
|---|---|
| Nama Tim | |
| Anggota 1 (Navigator/Analyst) | |
| Anggota 2 (Solver/Scribe) | |
| Asal Sekolah | SMK Maskumambang 1, Gresik |
| Pembina | |
| Tanggal Pengerjaan | |
| Waktu mulai / selesai | |

## IDENTITAS TANTANGAN
| Field | Isian |
|---|---|
| Judul Tantangan | |
| Kategori | Forensics / Cryptography |
| Bobot Poin | |
| Berkas yang diberikan | |

## FLAG AKHIR

    JCC{________________________________}

## RINGKASAN EKSEKUTIF
(Satu sampai dua kalimat. Tulis APA yang terjadi dan BAGAIMANA kalian
membuktikannya. Bagian ini yang dibaca juri paling pertama.)

Contoh bentuk yang baik:
"Workstation 192.168.10.58 mengunduh berkas dari domain eksternal
cdn-update.paket-gratis.tk, lalu mengirimkan data tersamar ke endpoint
/api/v2/collect melalui HTTP polos. Payload berlapis tiga tersebut kami
bongkar memakai CyberChef hingga memunculkan flag."

## ALAT YANG DIGUNAKAN
| Alat | Versi / Alamat | Fungsi |
|---|---|---|
| Wireshark | | |
| CyberChef | gchq.github.io/CyberChef | |
| CrackStation | crackstation.net | |
| Chatbot AI | | |

**Pernyataan kepatuhan:**
Tim menyatakan tidak menggunakan automated scanner (sqlmap, Burp Scanner,
dirb, nikto, atau sejenisnya). Seluruh analisis dilakukan manual memakai
fitur bawaan alat analisis.

Tanda tangan ketua tim: ______________________

## LANGKAH PENYELESAIAN RINCI

### Langkah 1: (judul singkat, misal "Memetakan lalu lintas DNS")
**Tujuan:** ____
**Filter / perintah:**

    ____

**Hasil:** ____
**Nomor paket bukti:** ____

[Screenshot 01: ____]

**Alasan langkah ini diambil:** ____

### Langkah 2: (judul singkat)
**Tujuan:** ____
**Filter / perintah:**

    ____

**Hasil:** ____
**Nomor paket bukti:** ____

[Screenshot 02: ____]

**Alasan langkah ini diambil:** ____

### Langkah 3: (judul singkat)
**Tujuan:** ____
**Menu yang dipakai:** ____
**Hasil:** ____

[Screenshot 03: ____]

### Langkah 4: (judul singkat)
**Tujuan:** ____
**Isi yang ditemukan:** ____
**Nomor paket bukti:** ____

[Screenshot 04: ____]

### Langkah 5: Pembongkaran payload
| Lapis | Bentuk yang diamati | Operasi CyberChef | Hasil |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

**URL resep CyberChef:**

    https://gchq.github.io/CyberChef/#recipe=____

[Screenshot 05: panel Recipe berisi seluruh langkah]
[Screenshot 06: panel Output menampilkan flag]

## JALAN BUNTU YANG DITEMUI
(Jujur laporkan. Juri menilai proses, dan tim yang tidak pernah salah
justru terlihat mencurigakan.)

| # | Yang dicoba | Kenapa gagal | Pelajaran |
|---|---|---|---|
| 1 | | | |
| 2 | | | |

## TABEL TEMUAN BUKTI
| Item | Nilai | Nomor Paket |
|---|---|---|
| IP workstation | | |
| Domain mencurigakan | | |
| IP server luar | | |
| Halaman pintu masuk | | |
| Berkas yang diunduh | | |
| MD5 berkas | | |
| Endpoint rahasia (POST) | | |
| Nilai parameter data | | |
| POST pengecoh | | |

## LAMPIRAN RIWAYAT INTERAKSI CHATBOT AI
(WAJIB. Kalau tim tidak memakai AI, tulis "Tidak menggunakan AI" dan
kosongkan tabel. Salin prompt persis, jangan diringkas.)

| No | Waktu | Pertanyaan / Prompt | Model AI | Ringkasan Bantuan | Diverifikasi? |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

### Refleksi penggunaan AI
- Bagian yang dikerjakan tim sendiri tanpa AI: ____
- Bagian yang terbantu AI, dan seberapa besar bantuannya: ____
- Apakah ada jawaban AI yang keliru? Bagaimana tim mengetahuinya? ____

## PELAJARAN & MITIGASI
**Akar masalah:** ____

**Rekomendasi untuk admin jaringan sekolah:**
1. ____
2. ____
3. ____

**Refleksi tim:** ____

Ditulis oleh: ______________________
Diperiksa oleh: ______________________
Waktu pengumpulan: ______________________
````

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# BAGIAN 6: LEMBAR EVALUASI & RUBRIK PENILAIAN MANDIRI

## 6.1 Lembar Log Aktivitas Tim

Isi selama Ronde 1 berlangsung. Kolom kiri dan kanan **harus berbeda isinya**. Kalau sama, berarti kalian mengerjakan hal yang sama dan membuang tenaga.

| Menit | Navigator / Analyst mengerjakan | Solver & Scribe mengerjakan |
|---|---|---|
| 00-05 | | |
| 05-10 | | |
| 10-15 | | |
| 15-20 | | |
| 20-25 | | |
| 25-30 | **(tukar peran)** | **(tukar peran)** |
| 30-35 | | |
| 35-40 | | |
| 40-45 | merapikan catatan | merapikan catatan |

## 6.2 Tabel Jawaban Tantangan

| # | Tantangan | Jawaban Tim | Nomor Paket | Nilai (diisi pembina) |
|---|---|---|---|---|
| T1 | Domain mencurigakan | | | ___ / 10 |
| T2 | IP server luar + halaman pintu masuk | | | ___ / 10 |
| T3 | Berkas terunduh (nama, ukuran, MD5) | | | ___ / 15 |
| T4 | Endpoint rahasia (URL POST) | | | ___ / 15 |
| T5 | Nilai parameter `data` | | | ___ / 10 |
| T6 | **FLAG** + urutan resep | | | ___ / 30 |
| T7 | POST pengecoh + cara membedakan | | | ___ / 10 |
| Bonus | Kata asli di balik `token` | | | ___ / 15 |

**Total: ______ / 100 (+15 bonus)**

## 6.3 Checklist Sebelum Menekan Submit

> ### ▲ Aturan tegas
> **Tidak ada satu pun kotak boleh kosong sebelum submit.** Kedua anggota membaca daftar ini bersama-sama dengan suara keras, lalu keduanya membubuhkan paraf. Kebiasaan ini yang menyelamatkan tim dari kesalahan konyol yang membuang puluhan poin.

### A. Format flag

```
[ ]  1. Flag diawali JCC{ dan diakhiri }
[ ]  2. Tidak ada spasi di depan atau di belakang flag
[ ]  3. Huruf besar-kecil sudah persis sama dengan hasil decode
[ ]  4. Angka 0 dan huruf O sudah diperiksa satu per satu
[ ]  5. Angka 1 dan huruf l sudah diperiksa satu per satu
[ ]  6. Flag disalin lewat Copy, bukan diketik ulang dari ingatan
```

### B. Bukti dan tangkapan layar

```
[ ]  7. Minimal 4 tangkapan layar terlampir, berurutan dan bernomor
[ ]  8. Setiap tangkapan layar memperlihatkan filter ATAU resep yang dipakai
[ ]  9. Teks di dalam gambar masih terbaca saat gambar diperkecil
[ ] 10. Setiap temuan disertai nomor paket
```

### C. Kepatuhan aturan lomba

```
[ ] 11. Tabel riwayat prompt AI terisi, atau tertulis "Tidak menggunakan AI"
[ ] 12. Pernyataan tidak memakai automated scanner sudah ditandatangani
```

### D. Administrasi

```
[ ] 13. Nama tim dan kedua anggota tertulis benar
[ ] 14. Berkas sudah diekspor ke PDF, bukan dikumpulkan mentah
[ ] 15. Nama berkas mengikuti format panitia
[ ] 16. Dikumpulkan MINIMAL 10 MENIT sebelum batas akhir
```

**Paraf Anggota 1:** __________  **Paraf Anggota 2:** __________

> ### ◆ Tentang butir 16
> Mengumpulkan tepat di detik terakhir adalah cara paling menyakitkan untuk kalah. Koneksi internet melambat, berkas gagal terunggah, dan seluruh kerja 3 jam hangus. Anggap batas akhir kalian **10 menit lebih awal** dari yang tertulis di aturan.

## 6.4 Rubrik Penilaian Mandiri

Nilai diri kalian sendiri dengan jujur. Kolom terakhir diisi pembina saat debrief.

### Aspek 1: Kemampuan Teknis (40%)

| Kriteria | 1 (Kurang) | 2 (Cukup) | 3 (Baik) | 4 (Sangat Baik) | Nilai |
|---|---|---|---|---|---|
| Penguasaan filter | filter salah terus | filter benar setelah beberapa kali | filter benar sekali coba | filter bertingkat langsung tepat | |
| Ekstraksi berkas | tidak menemukan menunya | menemukan setelah dibantu | menemukan sendiri | menemukan sendiri dan memverifikasi MD5 | |
| Decoding berlapis | tidak selesai | selesai dengan bantuan besar | selesai sendiri | selesai sendiri dan bisa menjelaskan urutannya | |
| Kecepatan | lewat 45 menit | 40-45 menit | 30-40 menit | di bawah 30 menit | |

### Aspek 2: Kerja Sama Tim (25%)

| Kriteria | 1 | 2 | 3 | 4 | Nilai |
|---|---|---|---|---|---|
| Pembagian peran | keduanya menatap satu layar | peran kabur | peran jelas | peran jelas dan sempat bertukar | |
| Komunikasi | banyak diam | menunjuk layar | mengucapkan temuan | mengucapkan dan mengulang balik | |
| Kepatuhan aturan waktu | tidak dipakai | dipakai sesekali | dipakai konsisten | dipakai dan sempat memutuskan meninggalkan jalur buntu | |

### Aspek 3: Dokumentasi (25%)

| Kriteria | 1 | 2 | 3 | 4 | Nilai |
|---|---|---|---|---|---|
| Tangkapan layar | kurang dari 2 | 2-3 buah | 4 buah, jelas | lebih dari 4, bernomor rapi, filter terlihat | |
| Catatan langkah | dibuat setelah selesai | sebagian dicatat sambil jalan | dicatat sambil jalan | dicatat sambil jalan lengkap dengan nomor paket | |
| Kelengkapan write-up | kurang dari 4 bagian | 4-5 bagian | 6 bagian | 6 bagian plus jalan buntu yang dilaporkan jujur | |

### Aspek 4: Penggunaan AI (10%)

| Kriteria | 1 | 2 | 3 | 4 | Nilai |
|---|---|---|---|---|---|
| Kualitas prompt | menempel soal mentah | prompt tanpa konteks | prompt berkonteks | prompt lengkap dengan bagian "sudah dicoba" | |
| Pencatatan | tidak dicatat | dicatat sebagian | dicatat lengkap | dicatat lengkap plus kolom verifikasi | |

**Nilai akhir mandiri:** ______ / 4.0

## 6.5 Pertanyaan Debrief

Jawab bersama pasangan setelah simulasi selesai. Bagian ini yang paling menentukan perbaikan kalian di simulasi berikutnya.

**1.** Di tahap mana kalian kehilangan waktu paling banyak, dan apa penyebab sebenarnya?

```
_________________________________________________________________________
```

**2.** Adakah momen ketika kalian berdua mengerjakan hal yang sama? Kapan, dan bagaimana mencegahnya lain kali?

```
_________________________________________________________________________
```

**3.** Adakah tangkapan layar yang baru kalian sadari kurang saat menulis write-up? Yang mana?

```
_________________________________________________________________________
```

**4.** Apakah aturan 7 menit benar-benar dipatuhi? Kalau tidak, apa alasannya?

```
_________________________________________________________________________
```

**5.** Satu hal konkret yang akan kalian ubah di simulasi berikutnya:

```
_________________________________________________________________________
```

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# LAMPIRAN A: KARTU PERAN (CETAK DAN POTONG)

> **Cetak halaman ini, potong menjadi dua, berikan satu kartu ke tiap siswa. Taruh di samping laptop selama simulasi.**

```
+=====================================================================+
|                                                                     |
|   KARTU PERAN A          NAVIGATOR / ANALYST                        |
|                                                                     |
|   ALAT SAYA : Wireshark                                             |
|                                                                     |
|   URUTAN KERJA SAYA                                                 |
|   1. Statistics > Protocol Hierarchy, petakan isinya                |
|   2. Filter  dns                     -> ada domain janggal?         |
|   3. Filter  http                    -> petakan percakapan          |
|   4. Filter  http.request.method == "POST"                          |
|   5. Klik kanan > Follow > TCP Stream                               |
|   6. File > Export Objects > HTTP                                   |
|                                                                     |
|   YANG SELALU SAYA UCAPKAN                                          |
|   "Paket nomor ___ , temuannya ___ . Catat."                        |
|                                                                     |
|   YANG TIDAK BOLEH SAYA LAKUKAN                                     |
|   - diam saat menemukan sesuatu                                     |
|   - menunjuk layar tanpa menyebut nomor paket                       |
|   - membacakan string panjang, salin dan tempel saja                |
|                                                                     |
+=====================================================================+


+=====================================================================+
|                                                                     |
|   KARTU PERAN B          SOLVER & SCRIBE                            |
|                                                                     |
|   ALAT SAYA : CyberChef, CrackStation, chatbot AI, text editor      |
|                                                                     |
|   URUTAN KERJA SAYA                                                 |
|   1. Buka draf-writeup.md SEBELUM timer mulai                       |
|   2. Catat tiap temuan + nomor paket + jam                          |
|   3. Potret tiap momen kunci, beri nama 01- 02- 03- ...             |
|   4. Bongkar sandi di CyberChef, lapis demi lapis                   |
|   5. Susun prompt AI kalau aturan 7 menit terpicu                   |
|   6. Salin prompt itu ke prompt-log.md SEGERA                       |
|                                                                     |
|   YANG SELALU SAYA UCAPKAN                                          |
|   "Tercatat. Ulangi bagian ___ , aku belum yakin."                  |
|   "Sudah 7 menit. Kita eskalasi sekarang."                          |
|                                                                     |
|   SAYA PEMEGANG KENDALI WAKTU. Keputusan saya soal waktu diikuti.   |
|                                                                     |
+=====================================================================+
```

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# LAMPIRAN B: KUNCI JAWABAN (KHUSUS PEMBINA)

> ## ✖ HALAMAN INI JANGAN DIBAGIKAN KE SISWA
> Pisahkan atau hapus sebelum mencetak modul untuk latihan.

## B.1 Kunci Tantangan

| # | Jawaban Benar | Paket |
|---|---|---|
| **T1** | `cdn-update.paket-gratis.tk`, dijawab `45.83.220.114` | 18 (query), 19 (response) |
| **T2** | Server luar `45.83.220.114`. Pintu masuk: `http://intranet.smkmaska.local/pengumuman.html` | 8 dan 9 |
| **T3** | `panduan-update.png`, 5.584 byte, MD5 `5dc9d2f02a82c67f85f26c20952a9092` | 28 (respons selesai) |
| **T4** | `POST http://cdn-update.paket-gratis.tk/api/v2/collect` | 37 |
| **T5** | nilai `data` sepanjang 104 karakter, diawali `N2Q3OTY0MzQzMzcy...` | 37 |
| **T6** | `From Base64` → `From Hex` → `Reverse` | |
| **T7** | `POST /login.php` ke `intranet.smkmaska.local` pada paket 11 | 11 |
| **Bonus** | `token=3fc0a7acf087f549ac2b266baf94b8b1` → `qwerty123` | 37 |

**FLAG:** `JCC{m15510n_4cc0mpl15h3d_wr1t3up_r34dy}`

## B.2 Peta Paket Lengkap

| Paket | Isi |
|---|---|
| 1, 2 | DNS query dan response `intranet.smkmaska.local` → `192.168.10.20` |
| 3, 4 | DNS `www.smkmaska.sch.id`, derau |
| 8 | `GET /pengumuman.html` ke intranet |
| 9 | Respons 200, halaman berisi tautan ke server luar |
| 11 | **POST pengecoh** `/login.php`, kredensial `staf_lab` / `Lab2026!Aman` |
| 12 | Respons 302, login berhasil |
| 18, 19 | **DNS query domain mencurigakan** `cdn-update.paket-gratis.tk` → `45.83.220.114` |
| 23 | `GET /unduh/panduan-update.png` ke server luar |
| 24-28 | Respons 200, PNG terpecah 4 segmen, selesai di paket 28 |
| 37 | **POST `/api/v2/collect`**, body 198 byte berisi payload |
| 38 | Respons 200 `{"status":"ok","received":1,"next_beacon":300}` |
| 47, 48 | `GET /api/v2/ping` dijawab 404, derau |
| 57 | TLS Client Hello ke `www.google.com`, pembanding terenkripsi |

## B.3 Rantai Payload

Isi body POST pada paket 37:

```
id=WS-LAB-58&host=lab-multimedia-07&token=3fc0a7acf087f549ac2b266baf94b8b1
&ts=1772158812&data=N2Q3OTY0MzQzMzcyNWY3MDc1MzM3NDMxNzI3NzVmNjQzMzY4MzUz
MTZjNzA2ZDMwNjM2MzM0NWY2ZTMwMzEzNTM1MzE2ZDdiNDM0MzRh
```

Pembongkaran bertahap:

| Lapis | Operasi | Hasil | Ciri yang menuntun |
|---|---|---|---|
| 1 | `From Base64` | `7d79643433725f70753374...` (78 karakter) | panjang 104 kelipatan 4, campur huruf besar-kecil |
| 2 | `From Hex` | `}yd43r_pu3t1rw_d3h51lpm0cc4_n01551m{CCJ` | hanya `0-9` dan `a-f`, panjang 78 (bukan 32/40/64) |
| 3 | `Reverse` | `JCC{m15510n_4cc0mpl15h3d_wr1t3up_r34dy}` | teks terbaca tetapi diakhiri `{CCJ` |

Petunjuk lapis ketiga sangat kuat: siswa melihat `{CCJ` di ujung dan biasanya langsung mengenali flag yang terbalik. Kalau ada yang belum sadar, tanyakan: "Coba baca tiga huruf terakhirnya dari belakang."

Berkas `panduan-update.png` memuat catatan **"PAYLOAD DIBUNGKUS 3 LAPIS SEBELUM DIKIRIM"** dan **"BUKA DARI LAPIS TERLUAR KE DALAM"**. Petunjuk itu hadiah untuk tim yang mengerjakan T3 dengan benar. Tim yang melewatkan Export Objects tetap bisa menyelesaikan T6, hanya lebih lama.

## B.4 Kesalahan yang Paling Sering Terjadi

| Gejala | Penyebab | Cara membimbing |
|---|---|---|
| Menyerah karena `frame contains "JCC"` kosong | mengira flag selalu polos | tanyakan "kalau flag disamarkan, filter itu masih berguna?" |
| Mengambil POST `/login.php` sebagai target | tidak memeriksa tujuan | tanyakan "POST itu menuju IP mana, dalam atau luar jaringan?" |
| Berhenti di lapis 2 karena hasilnya hex | mengira hex 78 karakter itu hash | arahkan ke cheat sheet LAB 03 soal panjang 32/40/64 |
| Tidak menemukan lapis 3 | belum sadar teks terbalik | minta membaca 3 karakter terakhir dari belakang |
| Kedua siswa menatap Wireshark bersama | kartu peran tidak dipakai | hentikan sejenak, bagikan ulang kartu peran |
| Tangkapan layar kurang saat menulis write-up | memotret setelah selesai | ini justru pelajaran utamanya, bahas di debrief |
| Write-up dikerjakan setelah 45 menit habis | tidak mencatat sambil jalan | tunjukkan Lembar Log Aktivitas yang kosong |

## B.5 Panduan Debrief 10 Menit

Jangan langsung membahas teknik. Urutan ini lebih efektif:

| Menit | Bahasan | Pertanyaan pembuka |
|---|---|---|
| 0-2 | **Perasaan** | "Bagian mana yang paling bikin panik?" |
| 2-4 | **Waktu** | "Coba lihat Lembar Log, di mana waktunya bocor?" |
| 4-6 | **Kerja sama** | "Ada momen kalian mengerjakan hal yang sama?" |
| 6-8 | **Dokumentasi** | "Tangkapan layar mana yang ternyata kurang?" |
| 8-10 | **Teknik** | baru di sini bahas filter dan resep yang benar |

Menaruh pembahasan teknik di urutan terakhir disengaja. Siswa cenderung hanya ingin tahu jawaban, padahal yang membuat mereka menang di JCC adalah empat bahasan sebelumnya.

## B.6 Rubrik Penilaian Write-Up

| Komponen | Bobot | Kriteria nilai penuh |
|---|---|---|
| Ringkasan eksekutif | 10% | 1-2 kalimat, menyebut apa yang terjadi dan bagaimana dibuktikan |
| Langkah penyelesaian | 30% | Runtut, tiap langkah menyebut tujuan, filter, hasil, dan nomor paket |
| Tangkapan layar | 20% | Minimal 4, bernomor, filter atau resep terlihat di dalam gambar |
| Jalan buntu | 10% | Minimal satu kegagalan dilaporkan jujur beserta pelajarannya |
| Lampiran prompt AI | 20% | Prompt disalin utuh, kolom verifikasi terisi |
| Mitigasi | 10% | Rekomendasi teknis spesifik, bukan slogan umum |

***
<div class="page-break"></div>

```{=latex}
\newpage
```

# LAMPIRAN C: PANDUAN INSTRUKTUR

## C.1 Membuat Ulang Berkas Simulasi

```bash
cd lab04
python3 generate_simulasi.py
```

Skrip hanya memakai pustaka standar Python 3, tanpa scapy dan tanpa Pillow. Ia **memverifikasi rantai payload sendiri** sebelum selesai: berkas ditulis, lalu payload dibongkar ulang dari nol dan dicocokkan dengan flag. Kalau tidak cocok, skrip berhenti dengan error.

Untuk melihat gambar `panduan-update.png` tanpa membuka Wireshark:

```bash
python3 generate_simulasi.py --preview
```

Perintah itu menulis `_preview-panduan.png`. **Hapus sebelum folder dibagikan ke siswa.**

## C.2 Membuat Varian Simulasi Baru

| Variabel | Efek |
|---|---|
| `FLAG` | isi flag yang dibungkus tiga lapis |
| `BONUS_PASS` | kata sandi di balik hash MD5, **wajib** sandi yang ada di CrackStation |
| `HOST_C2` | domain mencurigakan |
| `IP_C2` | alamat server luar |
| `IP_STAF` | alamat workstation tersangka |

Untuk mengubah urutan lapisan, sunting bagian **BAGIAN 2** pada skrip:

```python
lapis_reverse = FLAG[::-1]                             # lapis 3
lapis_hex = lapis_reverse.encode().hex()               # lapis 2
PAYLOAD = base64.b64encode(lapis_hex.encode()).decode()  # lapis 1
```

Ingat aturannya: **urutan pembuatan adalah kebalikan urutan pembongkaran.** Kalau kalian menukar susunan di sini, ubah juga kunci jawaban di Lampiran B.3 dan teks petunjuk di dalam PNG.

## C.3 Menjalankan Simulasi

### Persiapan sebelum siswa masuk

```
[ ] simulasi_jcc.pcapng tersalin ke kedua laptop, ukuran 16.972 byte
[ ] _preview-panduan.png SUDAH DIHAPUS
[ ] Lampiran B tidak ikut tercetak di modul siswa
[ ] Kartu peran Lampiran A sudah dicetak dan dipotong
[ ] Wireshark: reassembly TCP tercentang di kedua laptop
[ ] CyberChef dan CrackStation terbuka di tab terpisah
[ ] draf-writeup.md dan prompt-log.md sudah terbuka di text editor
[ ] Folder Simulasi-LAB04 sudah dibuat di Desktop
[ ] Timer besar terlihat kedua siswa
[ ] Pembina memegang daftar pengumuman titik pemeriksaan
```

### Naskah pengumuman pembina

Ucapkan persis, dengan suara tegas, tanpa memberi petunjuk tambahan:

```
  T-0     : "Timer mulai. 45 menit. Berkas boleh dibuka sekarang."
  10:00   : "Sepuluh menit berjalan. Sudah ketemu domain mencurigakannya?"
  25:00   : "Dua puluh lima menit. Tukar peran sekarang, lima menit."
  35:00   : "Sepuluh menit tersisa untuk mencari."
  40:00   : "BERHENTI MENCARI. Rapikan catatan. Lima menit."
  45:00   : "Wireshark ditutup. Ronde write-up dimulai. 30 menit."
  70:00   : "Lima menit tersisa. Periksa checklist submit."
  75:00   : "Waktu habis. Kumpulkan."
```

> ### ▲ Jangan memberi petunjuk selama Ronde 1
> Godaan terbesar pembina adalah menolong siswa yang terlihat buntu. Tahan diri. Kebuntuan itu bagian dari materi. Yang kalian bantu adalah kemampuan mereka bangkit dari kebuntuan, dan itu hanya terlatih kalau mereka benar-benar mengalaminya.
>
> Kalau satu tim benar-benar mandek lebih dari 15 menit di satu titik, berikan **pertanyaan**, bukan jawaban. Contoh: "Filter apa saja yang sudah kalian coba?" atau "Apa yang sudah kalian ketahui pasti?"

## C.4 Menilai dan Menutup Sesi

1. Kumpulkan write-up dalam bentuk PDF.
2. Nilai memakai rubrik di Lampiran B.6, jangan memakai jumlah flag saja.
3. Bacakan nilai per aspek, bukan nilai total. Siswa perlu tahu bagian mana yang lemah.
4. Jalankan debrief 10 menit sesuai urutan di Lampiran B.5.
5. Simpan write-up mereka. Bandingkan dengan write-up simulasi berikutnya untuk memperlihatkan kemajuan.

## C.5 Status Fase Fondasi

Dengan selesainya modul ini, fase fondasi tuntas.

| Modul | Judul | Keterampilan | Status |
|---|---|---|---|
| LAB 01 | The Wire Sniffer | Sniffing HTTP, Follow TCP Stream | ✔ |
| LAB 02 | Needle in a Haystack | Filter lanjutan, DNS, Export Objects | ✔ |
| LAB 03 | The Secret Decoder | Encoding berlapis, CyberChef, hash lookup | ✔ |
| LAB 04 | The Write-Up Drill | Simulasi, manajemen tim, write-up resmi | ✔ |

### Rekomendasi fase berikutnya

| Modul | Judul | Fokus |
|---|---|---|
| LAB 05 | The Hidden Layer | Steganografi, metadata EXIF, berkas dalam berkas |
| LAB 06 | Broken Login | Logika autentikasi web, cookie, dan JWT |
| LAB 07 | Simulasi Penyisihan Penuh | 15 soal, 3 jam, write-up wajib |

> **Saran ritme latihan.** Ulangi LAB 04 dengan varian baru setiap dua pekan, bahkan setelah masuk fase berikutnya. Keterampilan teknis bisa dipelajari sekali, sedangkan manajemen waktu dan kebiasaan mendokumentasikan hanya terbentuk lewat pengulangan.

***

**Waktu tidak menunggu siapa pun. Tim yang mencatat sambil berlari, itulah yang pulang membawa piala.**

*Modul ini disusun untuk pembinaan internal Tim CTF SMK Maskumambang 1, Pondok Pesantren Maskumambang.*
