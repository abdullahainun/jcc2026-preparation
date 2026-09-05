#!/usr/bin/env python3
"""
Generator file latihan LAB 02 - NEEDLE IN A HAYSTACK (JCC 2026).
Membuat lab02_export_object.pcapng tanpa dependensi eksternal.
Hanya memakai pustaka standar Python 3 (struct, zlib, hashlib, base64).

Isi skenario:
  - Query DNS normal (pengecoh)  : www.smkmaska.sch.id, portal-nilai.smkmaska.local
  - Query DNS mencurigakan       : arsip-nilai.free-hosting-murah.tk
  - Query DNS ber-encoding       : ZG9rdW1lbi1yYWhhc2lh.exfil.free-hosting-murah.tk
  - HTTP GET /                   : halaman indeks daftar berkas
  - HTTP GET logo-sekolah.png    : pengecoh, gambar polos
  - HTTP GET daftar-hadir.pdf    : pengecoh, PDF kecil
  - HTTP GET bocoran-soal-un.png : FILE BOCOR, memuat FLAG di dalam gambar
  - Sesi TLS                     : pembanding lalu lintas terenkripsi

Jalankan:  python3 generate_pcapng.py
"""
import sys
import struct
import zlib
import base64
import hashlib
import os

FLAG = "JCC{DNS_B0C0R_G4MB4R_T3RB4C4}"

BAD_HOST = "arsip-nilai.free-hosting-murah.tk"
EXFIL_LABEL = base64.b64encode(b"dokumen-rahasia").decode()
EXFIL_HOST = f"{EXFIL_LABEL}.exfil.free-hosting-murah.tk"

IP_CLIENT = "192.168.10.44"
IP_DNS = "192.168.10.1"
IP_LOCAL_SRV = "192.168.10.10"
IP_BAD = "185.220.101.47"
IP_TLS = "142.250.199.78"

MAC_CLIENT = "0800279f8e21"
MAC_GATEWAY = "001c42a1b2c3"

OUTDIR = os.path.dirname(os.path.abspath(__file__))
MSS = 1460

# ==========================================================================
# BAGIAN 1: FONT BITMAP 5x7 DAN PENULIS PNG (tanpa Pillow)
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
    "#": ".#.#.:#####:.#.#.:.#.#.:#####:.#.#.:.....",
    " ": ".....:.....:.....:.....:.....:.....:.....",
}


class Canvas:
    """Kanvas RGB sederhana, cukup untuk menggambar kotak dan teks bitmap."""

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
            glyph = FONT.get(ch, FONT[" "])
            for row, bits in enumerate(glyph.split(":")):
                for col, bit in enumerate(bits):
                    if bit == "#":
                        self.rect(cx + col * scale, y + row * scale,
                                  cx + (col + 1) * scale, y + (row + 1) * scale, color)
            cx += (5 + spacing) * scale
        return cx

    @staticmethod
    def text_width(s, scale=3, spacing=1):
        return len(s) * (5 + spacing) * scale

    def to_png(self, comment=None):
        raw = bytearray()
        stride = self.w * 3
        for y in range(self.h):
            raw.append(0)  # filter type 0 (None)
            raw += self.px[y * stride:(y + 1) * stride]

        def chunk(tag, data):
            body = tag + data
            return struct.pack("!I", len(data)) + body + struct.pack("!I", zlib.crc32(body) & 0xFFFFFFFF)

        out = b"\x89PNG\r\n\x1a\n"
        out += chunk(b"IHDR", struct.pack("!IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0))
        if comment:
            out += chunk(b"tEXt", b"Comment\x00" + comment.encode("latin-1", "replace"))
        out += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        out += chunk(b"IEND", b"")
        return out


NAVY = (0, 53, 95)
GOLD = (212, 160, 23)
WHITE = (249, 249, 254)
EMERALD = (13, 92, 70)
GREY = (140, 148, 165)


def make_flag_png():
    c = Canvas(1180, 470, NAVY)
    c.frame(18, 18, 1162, 452, GOLD, 4)
    c.rect(40, 44, 1140, 96, EMERALD)
    c.text(58, 58, "SMK MASKUMAMBANG 1 - PONDOK PESANTREN MASKUMAMBANG", WHITE, scale=3)

    c.text(58, 130, "DOKUMEN INTERNAL - RAHASIA", GOLD, scale=5)
    c.text(58, 188, "JANGAN DISEBARKAN KE LUAR SEKOLAH", WHITE, scale=3)
    c.rect(58, 226, 1122, 230, GREY)

    c.text(58, 252, "KODE VERIFIKASI PANITIA JCC 2026 :", WHITE, scale=3)
    fw = Canvas.text_width(FLAG, scale=6)
    c.rect(52, 292, 68 + fw, 356, (0, 30, 55))
    c.text(60, 300, FLAG, GOLD, scale=6)

    c.text(58, 386, "DICETAK 25/02/2026 13:41 WIB - HALAMAN 1 DARI 1", GREY, scale=3)
    return c.to_png(comment="Arsip internal SMK Maskumambang 1. Distribusi terbatas.")


def make_logo_png():
    c = Canvas(320, 320, WHITE)
    c.rect(0, 0, 320, 70, NAVY)
    c.text(18, 26, "SMK MASKA 1", WHITE, scale=3)
    c.frame(40, 100, 280, 250, EMERALD, 5)
    c.text(96, 150, "LOGO", EMERALD, scale=5)
    c.text(60, 268, "TIDAK ADA APA APA DI SINI", GREY, scale=2)
    return c.to_png(comment="Logo publik sekolah.")


def make_pdf():
    """PDF minimal 1 halaman, ditulis manual supaya tanpa dependensi."""
    text = ("BT /F1 13 Tf 60 700 Td (DAFTAR HADIR RAPAT WALI KELAS) Tj "
            "0 -26 Td (Rabu, 25 Februari 2026 - Ruang Guru) Tj "
            "0 -26 Td (1. Wali Kelas X TKJ 1) Tj "
            "0 -20 Td (2. Wali Kelas X TKJ 2) Tj "
            "0 -20 Td (3. Kepala Program Keahlian) Tj "
            "0 -34 Td (Berkas ini bukan yang kalian cari.) Tj ET")
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        b"/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
        b"<< /Length " + str(len(text)).encode() + b" >>\nstream\n" + text.encode() + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, body in enumerate(objs, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + body + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n".encode() + b"0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += (f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n"
            f"{xref}\n%%EOF\n").encode()
    return bytes(out)


# ==========================================================================
# BAGIAN 2: PENYUSUN PAKET
# ==========================================================================
packets = []
_ident = [0x4000]


def cksum(data):
    if len(data) % 2:
        data += b"\x00"
    s = 0
    for i in range(0, len(data), 2):
        s += (data[i] << 8) + data[i + 1]
    while s >> 16:
        s = (s & 0xFFFF) + (s >> 16)
    return (~s) & 0xFFFF


def ipb(a):
    return bytes(int(x) for x in a.split("."))


def build_ipv4(src, dst, proto, payload):
    _ident[0] = (_ident[0] + 1) & 0xFFFF
    hdr = struct.pack("!BBHHHBBH4s4s", 0x45, 0, 20 + len(payload), _ident[0],
                      0x4000, 64, proto, 0, ipb(src), ipb(dst))
    return hdr[:10] + struct.pack("!H", cksum(hdr)) + hdr[12:] + payload


def build_tcp(src, dst, sp, dp, seq, ack, flags, payload=b"", win=64240):
    hdr = struct.pack("!HHIIBBHHH", sp, dp, seq, ack, 0x50, flags, win, 0, 0)
    seg = hdr + payload
    pseudo = ipb(src) + ipb(dst) + struct.pack("!BBH", 0, 6, len(seg))
    return seg[:16] + struct.pack("!H", cksum(pseudo + seg)) + seg[18:]


def build_udp(src, dst, sp, dp, payload):
    seg = struct.pack("!HHHH", sp, dp, 8 + len(payload), 0) + payload
    pseudo = ipb(src) + ipb(dst) + struct.pack("!BBH", 0, 17, len(seg))
    return seg[:6] + struct.pack("!H", cksum(pseudo + seg) or 0xFFFF) + seg[8:]


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
        self.cseq = 0x11000000 + (cport * 7919) % 0xFFFFF
        self.sseq = 0x77000000 + (sport * 104729) % 0xFFFFF

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
        self._s2c(self.SYN | self.ACK, dt=0.0180)
        self._c2s(self.ACK, dt=0.0003)

    def request(self, data, dt=0.0022):
        self._c2s(self.PSH | self.ACK, data, dt=dt)

    def response(self, data, first_dt=0.0350):
        """Kirim balasan server, dipecah sesuai MSS supaya realistis."""
        chunks = [data[i:i + MSS] for i in range(0, len(data), MSS)] or [b""]
        for n, ch in enumerate(chunks):
            last = (n == len(chunks) - 1)
            self._s2c(self.PSH | self.ACK if last else self.ACK, ch,
                      dt=first_dt if n == 0 else 0.0009)
            if last or n % 2 == 1:
                self._c2s(self.ACK, dt=0.0002)

    def close(self):
        self._c2s(self.FIN | self.ACK, dt=0.0040)
        self._s2c(self.ACK, dt=0.0008)
        self._s2c(self.FIN | self.ACK, dt=0.0006)
        self._c2s(self.ACK, dt=0.0003)


def dns_name(name):
    out = b""
    for label in name.split("."):
        out += bytes([len(label)]) + label.encode()
    return out + b"\x00"


def dns_pair(ts, txid, host, answer_ip, sport):
    q = dns_name(host) + struct.pack("!HH", 1, 1)
    query = struct.pack("!HHHHHH", txid, 0x0100, 1, 0, 0, 0) + q
    emit(ts, MAC_GATEWAY, MAC_CLIENT,
         build_ipv4(IP_CLIENT, IP_DNS, 17, build_udp(IP_CLIENT, IP_DNS, sport, 53, query)))
    if answer_ip:
        reply = (struct.pack("!HHHHHH", txid, 0x8180, 1, 1, 0, 0) + q +
                 struct.pack("!HHHIH", 0xC00C, 1, 1, 45, 4) + ipb(answer_ip))
    else:
        reply = struct.pack("!HHHHHH", txid, 0x8183, 1, 0, 0, 0) + q
    emit(round(ts + 0.0231, 6), MAC_CLIENT, MAC_GATEWAY,
         build_ipv4(IP_DNS, IP_CLIENT, 17, build_udp(IP_DNS, IP_CLIENT, 53, sport, reply)))


UA = "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"


def http_get(path, host, accept="text/html,application/xhtml+xml,*/*;q=0.8", ref=None):
    h = [f"GET {path} HTTP/1.1", f"Host: {host}", f"User-Agent: {UA}",
         f"Accept: {accept}", "Accept-Language: id,en-US;q=0.7",
         "Connection: keep-alive"]
    if ref:
        h.append(f"Referer: {ref}")
    return ("\r\n".join(h) + "\r\n\r\n").encode()


def http_body(status, ctype, body, extra=()):
    h = [f"HTTP/1.1 {status}", "Date: Wed, 25 Feb 2026 06:41:07 GMT",
         "Server: nginx/1.18.0", *extra,
         f"Content-Type: {ctype}", f"Content-Length: {len(body)}",
         "Connection: keep-alive"]
    return ("\r\n".join(h) + "\r\n\r\n").encode() + body


# ==========================================================================
# BAGIAN 3: MERANGKAI SKENARIO
# ==========================================================================
T0 = 1772001600.000000

# 3.1 Lalu lintas DNS wajar (pengecoh)
dns_pair(T0 + 0.0000, 0x2C41, "www.smkmaska.sch.id", "103.28.14.92", 52011)
dns_pair(T0 + 0.4120, 0x2C42, "portal-nilai.smkmaska.local", IP_LOCAL_SRV, 52012)
dns_pair(T0 + 0.9330, 0x2C43, "fonts.gstatic.com", "142.250.199.67", 52013)

# 3.2 Query mencurigakan
dns_pair(T0 + 2.1050, 0x2C44, BAD_HOST, IP_BAD, 52014)
dns_pair(T0 + 2.3800, 0x2C45, EXFIL_HOST, IP_BAD, 52015)

# 3.3 Sesi HTTP ke host mencurigakan
INDEX = (
    "<!DOCTYPE html>\n<html><head><meta charset=\"UTF-8\">\n"
    "<title>Index of /arsip</title></head><body>\n"
    "<h1>Index of /arsip</h1>\n<hr>\n<pre>\n"
    "<a href=\"/assets/logo-sekolah.png\">logo-sekolah.png</a>          25-Feb-2026 13:38   6K\n"
    "<a href=\"/arsip/daftar-hadir-rapat.pdf\">daftar-hadir-rapat.pdf</a>    25-Feb-2026 13:39   1K\n"
    "<a href=\"/arsip/bocoran-soal-un-2026.png\">bocoran-soal-un-2026.png</a>  25-Feb-2026 13:41  14K\n"
    "</pre>\n<hr>\n<p>unggahan otomatis, jangan dihapus</p>\n</body></html>\n"
).encode()

LOGO = make_logo_png()
PDF = make_pdf()
LEAK = make_flag_png()

f = TcpFlow(T0 + 3.0110, IP_CLIENT, MAC_CLIENT, 51402, IP_BAD, MAC_GATEWAY, 80)
f.handshake()
f.request(http_get("/arsip/", BAD_HOST))
f.response(http_body("200 OK", "text/html; charset=UTF-8", INDEX))

f.request(http_get("/assets/logo-sekolah.png", BAD_HOST, "image/avif,image/webp,*/*",
                   ref=f"http://{BAD_HOST}/arsip/"), dt=0.0410)
f.response(http_body("200 OK", "image/png", LOGO, extra=["Cache-Control: max-age=600"]))

f.request(http_get("/arsip/daftar-hadir-rapat.pdf", BAD_HOST, "application/pdf,*/*",
                   ref=f"http://{BAD_HOST}/arsip/"), dt=0.0620)
f.response(http_body("200 OK", "application/pdf", PDF))

f.request(http_get("/arsip/bocoran-soal-un-2026.png", BAD_HOST, "image/avif,image/webp,*/*",
                   ref=f"http://{BAD_HOST}/arsip/"), dt=0.0880)
f.response(http_body("200 OK", "image/png", LEAK,
                     extra=["Content-Disposition: inline; filename=\"bocoran-soal-un-2026.png\""]))
f.close()

# 3.4 Sesi 404 kecil (melatih http.response.code)
f2 = TcpFlow(T0 + 9.8800, IP_CLIENT, MAC_CLIENT, 51418, IP_BAD, MAC_GATEWAY, 80)
f2.handshake()
f2.request(http_get("/arsip/kunci-jawaban.zip", BAD_HOST, "application/zip,*/*"))
f2.response(http_body("404 Not Found", "text/html", b"<html><body>404 Not Found</body></html>"))
f2.close()


# 3.5 Pembanding terenkripsi
def client_hello(sni):
    s = sni.encode()
    ext_sni = b"\x00\x00" + struct.pack("!H", len(s) + 5) + struct.pack("!H", len(s) + 3) \
        + b"\x00" + struct.pack("!H", len(s)) + s
    ext_ver = b"\x00\x2b\x00\x03\x02\x03\x04"
    exts = ext_sni + ext_ver
    body = (b"\x03\x03" + bytes(range(32)) + b"\x20" + bytes(range(0x40, 0x60)) +
            struct.pack("!H", 4) + b"\x13\x01\x13\x02" + b"\x01\x00" +
            struct.pack("!H", len(exts)) + exts)
    hs = b"\x01" + struct.pack("!I", len(body))[1:] + body
    return b"\x16\x03\x01" + struct.pack("!H", len(hs)) + hs


def app_data(seed, size):
    return b"\x17\x03\x03" + struct.pack("!H", size) + \
        bytes(((seed * 37 + i * 89) % 251) + 3 for i in range(size))


f3 = TcpFlow(T0 + 12.4400, IP_CLIENT, MAC_CLIENT, 51470, IP_TLS, MAC_GATEWAY, 443)
f3.handshake()
f3.request(client_hello("drive.google.com"))
f3.response(app_data(7, 700), first_dt=0.0260)
f3.request(app_data(19, 180), dt=0.0050)
f3.response(app_data(53, 1100), first_dt=0.0210)
f3.close()

packets.sort(key=lambda p: p[0])

# ==========================================================================
# BAGIAN 4: MENULIS FILE PCAPNG
# ==========================================================================
OUT = os.path.join(OUTDIR, "lab02_export_object.pcapng")


def pad4(b):
    return b + b"\x00" * ((4 - len(b) % 4) % 4)


def block(btype, body):
    total = 12 + len(body)
    return struct.pack("<II", btype, total) + body + struct.pack("<I", total)


with open(OUT, "wb") as fh:
    shb_body = struct.pack("<IHHq", 0x1A2B3C4D, 1, 0, -1) + \
        struct.pack("<HH", 3, len(b"LAB 02 JCC 2026")) + pad4(b"LAB 02 JCC 2026") + \
        struct.pack("<HH", 0, 0)
    fh.write(block(0x0A0D0D0A, shb_body))

    idb_body = struct.pack("<HHI", 1, 0, 65535) + \
        struct.pack("<HH", 9, 1) + pad4(bytes([6])) + \
        struct.pack("<HH", 2, len(b"lab-switch")) + pad4(b"lab-switch") + \
        struct.pack("<HH", 0, 0)
    fh.write(block(0x00000001, idb_body))

    for ts, raw in packets:
        us = int(round(ts * 1_000_000))
        epb = struct.pack("<IIIII", 0, us >> 32, us & 0xFFFFFFFF, len(raw), len(raw)) + pad4(raw)
        fh.write(block(0x00000006, epb))

print(f"file          : {OUT}")
print(f"paket         : {len(packets)}")
print(f"ukuran        : {os.path.getsize(OUT)} byte")
print(f"domain jahat  : {BAD_HOST}")
print(f"domain exfil  : {EXFIL_HOST}")
print(f"  label base64: {EXFIL_LABEL}  ->  {base64.b64decode(EXFIL_LABEL).decode()}")
print(f"FLAG          : {FLAG}")
print()
for name, blob in (("logo-sekolah.png", LOGO), ("daftar-hadir-rapat.pdf", PDF),
                   ("bocoran-soal-un-2026.png", LEAK)):
    print(f"  {name:26} {len(blob):6} byte  md5={hashlib.md5(blob).hexdigest()}"
          f"  sha1={hashlib.sha1(blob).hexdigest()[:16]}")

if "--preview" in sys.argv:
    prev = os.path.join(OUTDIR, "_preview-bocoran.png")
    with open(prev, "wb") as fh:
        fh.write(LEAK)
    print(f"\npratinjau gambar bocor: {prev}")
    print("HAPUS file ini sebelum folder dibagikan ke siswa.")
