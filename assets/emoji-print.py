#!/usr/bin/env python3
"""
Filter cetak: mengganti emoji dengan simbol Unicode yang bisa dirender WeasyPrint.

WeasyPrint 69 menemukan Noto Color Emoji, tetapi menggambar glifnya dengan skala
dan posisi yang salah, sehingga emoji tampil kecil melayang di atas baris.
Simbol dari font teks biasa (DejaVu Sans, Noto Sans) tampil normal.

Berkas .md aslinya tidak disentuh. Filter ini hanya dipakai di jalur PDF,
sehingga versi HTML tetap memakai emoji berwarna.

Pakai:  python3 emoji-print.py masukan.md keluaran.md
"""
import sys

GANTI = {
    "✅": "✔",  # tanda centang     -> heavy check mark
    "\U0001F527": "⚙",  # kunci inggris -> gear
    "\U0001F4A1": "★",  # bohlam        -> bintang padat
    "\U0001F50D": "◆",  # kaca pembesar -> wajik
    "\U0001F6A9": "⚑",  # bendera       -> bendera hitam
    "\U0001F3AF": "◎",  # target        -> lingkaran bulls-eye
    "\U0001F512": "✖",  # gembok        -> silang tebal
    "\U0001F6A8": "⚠",  # sirene        -> segitiga peringatan
    "❌":     "✗",  # silang merah  -> ballot X
    "\U0001F310": "◆",  # globe         -> wajik
    "\U0001F914": "◆",  # berpikir      -> wajik
    "\U0001F6E1": "◆",  # perisai       -> wajik
    "\U0001F4D8": "◆",  # buku biru     -> wajik
    "\U0001F4D7": "◆",  # buku hijau    -> wajik
    "\U0001F4D9": "◆",  # buku oranye   -> wajik
    "\U0001F4D5": "◆",  # buku merah    -> wajik
    "\U0001F7E5": "●",  # kotak merah   -> lingkaran padat
    "\U0001F7E9": "●",
    "\U0001F7E8": "●",
    "\U0001F535": "●",
    "\U0001F7E2": "●",
    "\U0001F534": "●",
    "️": "",            # variation selector, memaksa gaya emoji
}


def bersihkan(teks: str) -> str:
    for lama, baru in GANTI.items():
        teks = teks.replace(lama, baru)
    return teks


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("pakai: emoji-print.py masukan.md keluaran.md")
    with open(sys.argv[1], encoding="utf-8") as fh:
        isi = fh.read()
    with open(sys.argv[2], "w", encoding="utf-8") as fh:
        fh.write(bersihkan(isi))
