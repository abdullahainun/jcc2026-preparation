#!/usr/bin/env python3
"""
Generator barang bukti LAB 03 - THE SECRET DECODER (JCC 2026).
Hanya memakai pustaka standar Python 3.

Menghasilkan:
  barang-bukti.txt   -> dibagikan ke siswa
  (kunci jawaban dicetak ke layar, jangan dibagikan)

Jalankan:  python3 generate_challenges.py
"""
import base64
import hashlib
import os
import sys

OUTDIR = os.path.dirname(os.path.abspath(__file__))

FLAG = "JCC{L4P15_D3M1_L4P15_T3RB0NGK4R}"


def rot(text, n=13):
    out = []
    for c in text:
        if "a" <= c <= "z":
            out.append(chr((ord(c) - 97 + n) % 26 + 97))
        elif "A" <= c <= "Z":
            out.append(chr((ord(c) - 65 + n) % 26 + 65))
        else:
            out.append(c)
    return "".join(out)


def to_hex_spaced(data: bytes, per_line=24):
    h = data.hex()
    pairs = [h[i:i + 2] for i in range(0, len(h), 2)]
    return "\n".join(" ".join(pairs[i:i + per_line]) for i in range(0, len(pairs), per_line))


# ==========================================================================
# BARANG BUKTI #1 - Base64 satu lapis
# ==========================================================================
BB1_PLAIN = (
    "Halo tim forensik. Kalian terlambat 3 jam. "
    "Semua berkas nilai sudah saya salin ke luar. "
    "Petunjuk berikutnya saya titipkan di barang bukti kedua, "
    "dan kunci masuk saya tinggalkan sebagai sidik jari di barang bukti ketiga."
)
BB1 = base64.b64encode(BB1_PLAIN.encode()).decode()

# ==========================================================================
# BARANG BUKTI #2 - Hex -> Base64 -> ROT13 -> FLAG
# Urutan pembuatan kebalikan dari urutan pembongkaran.
# ==========================================================================
step_rot = rot(FLAG, 13)                       # lapis 3 (paling dalam)
step_b64 = base64.b64encode(step_rot.encode()).decode()   # lapis 2
BB2 = to_hex_spaced(step_b64.encode())         # lapis 1 (paling luar)

# ==========================================================================
# BARANG BUKTI #3 - Hash untuk dicari di basis data lookup
# ==========================================================================
PASS_MD5 = "sunshine"
PASS_SHA1 = "letmein"
PASS_KUAT = "T7#pQz9!vK2mLx4W"

H_MD5 = hashlib.md5(PASS_MD5.encode()).hexdigest()
H_SHA1 = hashlib.sha1(PASS_SHA1.encode()).hexdigest()
H_KUAT = hashlib.md5(PASS_KUAT.encode()).hexdigest()
H_SHA256 = hashlib.sha256(PASS_MD5.encode()).hexdigest()

# ==========================================================================
# BONUS - Caesar geser 5
# ==========================================================================
BONUS_PLAIN = "SELAMAT KALIAN LULUS UJIAN SANDI"
BONUS = rot(BONUS_PLAIN, 5)

# ==========================================================================
# Menulis berkas untuk siswa
# ==========================================================================
LEMBAR = f"""==========================================================================
  BARANG BUKTI DIGITAL - LAB 03: THE SECRET DECODER
  Tim CTF SMK Maskumambang 1 | JCC 2026
  Ditemukan di: /var/log/.cache/pesan.txt pada server sekolah
  Waktu penemuan: Kamis, 26 Februari 2026, 08:15 WIB
==========================================================================

--------------------------------------------------------------------------
BARANG BUKTI #1
Ditemukan di dalam komentar berkas index.php
--------------------------------------------------------------------------
{BB1}


--------------------------------------------------------------------------
BARANG BUKTI #2
Ditemukan di dalam berkas .hidden_note pada direktori /tmp
--------------------------------------------------------------------------
{BB2}


--------------------------------------------------------------------------
BARANG BUKTI #3
Ditemukan di dalam berkas backup-akun.csv
--------------------------------------------------------------------------
akun,algoritma,nilai_hash
admin_lab,MD5,{H_MD5}
operator,SHA-1,{H_SHA1}
kepala_lab,MD5,{H_KUAT}


--------------------------------------------------------------------------
BARANG BUKTI #4 (BONUS)
Ditemukan tertulis di papan tulis Lab Multimedia
--------------------------------------------------------------------------
{BONUS}

==========================================================================
Format flag: JCC{{...}}
Selamat bekerja, analis.
==========================================================================
"""

path = os.path.join(OUTDIR, "barang-bukti.txt")
with open(path, "w") as fh:
    fh.write(LEMBAR)

# ==========================================================================
# Verifikasi mandiri: bongkar ulang dari nol
# ==========================================================================
cek1 = base64.b64decode(BB1).decode()
cek2 = rot(base64.b64decode(bytes.fromhex(BB2.replace(" ", "").replace("\n", "")).decode()).decode(), 13)
cek4 = rot(BONUS, -5)
assert cek1 == BB1_PLAIN, "BB1 gagal"
assert cek2 == FLAG, "BB2 gagal"
assert cek4 == BONUS_PLAIN, "BB4 gagal"

print(f"berkas siswa : {path}")
print(f"ukuran       : {os.path.getsize(path)} byte")
print()
print("=" * 74)
print("KUNCI JAWABAN - JANGAN DIBAGIKAN KE SISWA")
print("=" * 74)
print(f"BB1  resep    : From Base64")
print(f"BB1  hasil    : {BB1_PLAIN[:60]}...")
print()
print(f"BB2  resep    : From Hex -> From Base64 -> ROT13")
print(f"BB2  lapis 1  : {BB2.splitlines()[0]} ... ({len(BB2.replace(' ', '').replace(chr(10), '')) // 2} byte)")
print(f"BB2  lapis 2  : {step_b64}")
print(f"BB2  lapis 3  : {step_rot}")
print(f"BB2  FLAG     : {FLAG}")
print()
print(f"BB3  MD5      : {H_MD5}  ->  {PASS_MD5}")
print(f"BB3  SHA-1    : {H_SHA1}  ->  {PASS_SHA1}")
print(f"BB3  MD5 kuat : {H_KUAT}  ->  {PASS_KUAT}  (TIDAK ADA di basis data lookup)")
print(f"     SHA-256  : {H_SHA256}  (contoh 64 karakter untuk cheatsheet)")
print()
print(f"BB4  resep    : ROT13 dengan Amount = 21  (atau Caesar geser -5)")
print(f"BB4  hasil    : {BONUS_PLAIN}")
print()
print("verifikasi ulang: SEMUA RANTAI DECODE BERHASIL")

if "--kunci" in sys.argv:
    kp = os.path.join(OUTDIR, "_kunci-jawaban.txt")
    with open(kp, "w") as fh:
        fh.write(f"FLAG   : {FLAG}\nBB1    : {BB1_PLAIN}\n"
                 f"BB2    : From Hex -> From Base64 -> ROT13\n"
                 f"BB3    : {H_MD5}={PASS_MD5}, {H_SHA1}={PASS_SHA1}, {H_KUAT}=TIDAK TERPECAH\n"
                 f"BB4    : {BONUS_PLAIN} (Caesar -5 / ROT13 amount 21)\n")
    print(f"\nkunci tertulis ke {kp} - HAPUS sebelum folder dibagikan")
