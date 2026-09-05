# JCC 2026 - Modul Pembinaan Tim CTF

Modul praktikum untuk pembinaan tim CTF **SMK Maskumambang 1**, persiapan
**Jatim Cybersecurity Competition (JCC) 2026** kategori SMA/SMK sederajat.

Sasaran: 2 siswa kelas X, tingkat pemula.

## Aturan kompetisi yang membentuk modul ini

| Aturan panitia | Konsekuensi di modul |
|---|---|
| Babak penyisihan format Jeopardy daring, lebih dari 15 soal | Latihan manajemen waktu dan skala prioritas |
| Chatbot AI boleh dipakai, prompt wajib dilampirkan di write-up | Setiap modul punya bagian prompt drill dan format log prompt |
| Automated scanner dilarang keras | Seluruh teknik manual, hanya fitur bawaan alat analisis |
| Write-up wajib dikumpulkan sebelum batas akhir | Template write-up resmi di setiap modul |

## Daftar Modul

| # | Modul | Fokus | Durasi | Berkas latihan |
|---|---|---|---|---|
| 01 | [The Wire Sniffer](LAB01-The-Wire-Sniffer.md) | Sniffing HTTP, Follow TCP Stream | 45-60 menit | `lab01/lab01-wire-sniffer.pcap` |
| 02 | [Needle in a Haystack](LAB02-Needle-In-A-Haystack.md) | Filter lanjutan, DNS tracking, Export Objects | 60 menit | `lab02/lab02_export_object.pcapng` |
| 03 | [The Secret Decoder](LAB03-The-Secret-Decoder.md) | Encoding berlapis, CyberChef, hash lookup | 60 menit | `lab03/barang-bukti.txt` |
| 04 | [The Write-Up Drill](LAB04-Write-Up-Drill.md) | Simulasi mini CTF, manajemen tim, write-up resmi | 75 menit | `lab04/simulasi_jcc.pcapng` |

Modul 01 sampai 04 adalah **fase fondasi**. Kerjakan berurutan, karena setiap
modul memakai keterampilan modul sebelumnya. LAB 04 menggabungkan ketiganya.

## Peringatan untuk pembina

> **Lampiran B di setiap modul berisi kunci jawaban, rubrik penilaian, dan
> daftar kesalahan umum siswa. Hapus atau pisahkan halaman itu sebelum
> mencetak modul untuk siswa.**

Beberapa generator juga bisa menulis berkas pratinjau yang membocorkan jawaban
(`_preview-*.png`, `_kunci-jawaban.txt`). Berkas itu sudah masuk `.gitignore`,
tetapi tetap periksa folder sebelum dibagikan.

## Membangun PDF

```bash
./build-pdf.sh LAB01-The-Wire-Sniffer.md
```

Skrip menghasilkan HTML cetak dan PDF A4. Urutan engine yang dipakai:

1. `weasyprint` bila tersedia (disarankan, menghormati CSS ganti halaman)
2. `xelatex` sebagai cadangan
3. Bila keduanya tidak ada, cukup buka berkas HTML lalu `Ctrl+P` dan simpan sebagai PDF

Pasang engine di Arch atau Manjaro:

```bash
sudo pacman -S python-weasyprint
```

### Catatan teknis cetak

- Baris `---` sebagai pemisah horizontal **tidak dipakai**, diganti `***`.
  Pandoc menafsirkan `---` sebagai metadata YAML sekaligus tabel sederhana,
  yang merusak struktur dokumen.
- WeasyPrint salah menggambar emoji berwarna, jadi `assets/emoji-print.py`
  menukarnya dengan simbol Unicode khusus di jalur PDF. Berkas Markdown dan
  HTML tetap memakai emoji.

## Membuat ulang berkas latihan

Seluruh generator hanya memakai pustaka standar Python 3. Tidak ada scapy,
tidak ada Pillow. PNG, PDF, pcap, dan pcapng ditulis dari nol, supaya laptop
pengajar tidak perlu memasang apa pun.

```bash
python3 lab01/generate_pcap.py
python3 lab02/generate_pcapng.py
python3 lab03/generate_challenges.py
python3 lab04/generate_simulasi.py
```

Setiap generator mencetak kunci jawaban ke layar dan memverifikasi hasilnya
sendiri. Generator LAB 03 dan LAB 04 berhenti dengan error bila rantai decode
tidak tembus, sehingga soal yang mustahil dikerjakan tidak pernah terbagikan.

Tambahkan `--preview` pada generator LAB 02 dan LAB 04 untuk menulis pratinjau
gambar yang memuat flag.

## Struktur

```
.
├── LAB0*.md              modul, sumber utama
├── LAB0*.pdf             hasil cetak A4
├── build-pdf.sh          Markdown -> HTML cetak -> PDF
├── assets/
│   ├── print.css         gaya cetak, palet navy/emerald/gold
│   └── emoji-print.py    filter emoji khusus jalur PDF
└── lab0*/                generator dan berkas latihan tiap modul
```

## Rencana lanjutan

| Modul | Judul | Fokus |
|---|---|---|
| LAB 05 | The Hidden Layer | Steganografi, metadata EXIF, berkas dalam berkas |
| LAB 06 | Broken Login | Logika autentikasi web, cookie, dan JWT |
| LAB 07 | Simulasi Penyisihan Penuh | 15 soal, 3 jam, write-up wajib |
