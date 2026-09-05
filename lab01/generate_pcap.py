#!/usr/bin/env python3
"""
Generator file latihan LAB 01 - THE WIRE SNIFFER (JCC 2026).
Membuat lab01-wire-sniffer.pcap tanpa dependensi eksternal.

Isi skenario:
  - DNS query ke portal-nilai.smkmaska.local
  - Login gagal (401) dari 192.168.10.52  -> pengecoh
  - Login sukses (302) dari 192.168.10.37 -> kredensial plaintext
  - GET /dashboard.php                    -> FLAG utama di komentar HTML
  - Header X-Debug-Note                   -> FLAG bonus (base64)
  - Sesi TLS ke 142.250.199.78:443        -> pembanding lalu lintas terenkripsi
"""
import struct
import base64

FLAG_MAIN = "JCC{w1r3sh4rk_l1h4t_s3mu4ny4}"
FLAG_BONUS = "JCC{http_1tu_k4rtu_p0s}"
B64_BONUS = base64.b64encode(FLAG_BONUS.encode()).decode()

MAC_CLIENT = "0800271a2b3c"
MAC_CLIENT2 = "0800274d5e6f"
MAC_GATEWAY = "001c42a1b2c3"
MAC_SERVER = "001c4211ee55"

IP_CLIENT = "192.168.10.37"
IP_CLIENT2 = "192.168.10.52"
IP_SERVER = "192.168.10.10"
IP_DNS = "192.168.10.1"
IP_TLS = "142.250.199.78"

packets = []  # (timestamp float, raw bytes)
_ident = [0x1000]


def cksum(data: bytes) -> int:
    if len(data) % 2:
        data += b"\x00"
    total = 0
    for i in range(0, len(data), 2):
        total += (data[i] << 8) + data[i + 1]
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
    return (~total) & 0xFFFF


def ip_bytes(addr: str) -> bytes:
    return bytes(int(x) for x in addr.split("."))


def build_ipv4(src: str, dst: str, proto: int, payload: bytes) -> bytes:
    _ident[0] = (_ident[0] + 1) & 0xFFFF
    total_len = 20 + len(payload)
    hdr = struct.pack(
        "!BBHHHBBH4s4s",
        0x45, 0x00, total_len, _ident[0], 0x4000, 64, proto, 0,
        ip_bytes(src), ip_bytes(dst),
    )
    chk = cksum(hdr)
    hdr = hdr[:10] + struct.pack("!H", chk) + hdr[12:]
    return hdr + payload


def build_tcp(src, dst, sport, dport, seq, ack, flags, payload=b"", window=64240):
    hdr = struct.pack("!HHIIBBHHH", sport, dport, seq, ack, 0x50, flags, window, 0, 0)
    seg = hdr + payload
    pseudo = ip_bytes(src) + ip_bytes(dst) + struct.pack("!BBH", 0, 6, len(seg))
    chk = cksum(pseudo + seg)
    seg = seg[:16] + struct.pack("!H", chk) + seg[18:]
    return seg


def build_udp(src, dst, sport, dport, payload):
    seg = struct.pack("!HHHH", sport, dport, 8 + len(payload), 0) + payload
    pseudo = ip_bytes(src) + ip_bytes(dst) + struct.pack("!BBH", 0, 17, len(seg))
    chk = cksum(pseudo + seg) or 0xFFFF
    seg = seg[:6] + struct.pack("!H", chk) + seg[8:]
    return seg


def emit(ts, dmac, smac, frame_ip):
    raw = bytes.fromhex(dmac) + bytes.fromhex(smac) + b"\x08\x00" + frame_ip
    if len(raw) < 60:
        raw += b"\x00" * (60 - len(raw))
    packets.append((ts, raw))


class TcpFlow:
    """Satu sesi TCP dua arah, sequence number-nya dijaga otomatis."""

    FIN, SYN, RST, PSH, ACK = 0x01, 0x02, 0x04, 0x08, 0x10

    def __init__(self, t0, cip, cmac, cport, sip, smac, sport):
        self.t = t0
        self.cip, self.cmac, self.cport = cip, cmac, cport
        self.sip, self.smac, self.sport = sip, smac, sport
        self.cseq = 0x5A000000 + (cport * 7919) % 0xFFFF
        self.sseq = 0xC1000000 + (sport * 104729) % 0xFFFF

    def tick(self, dt=0.0004):
        self.t = round(self.t + dt, 6)
        return self.t

    def _c2s(self, flags, payload=b"", dt=0.0004):
        seg = build_tcp(self.cip, self.sip, self.cport, self.sport,
                        self.cseq, self.sseq, flags, payload)
        emit(self.tick(dt), self.smac, self.cmac,
             build_ipv4(self.cip, self.sip, 6, seg))
        self.cseq += len(payload) + (1 if flags & (self.SYN | self.FIN) else 0)

    def _s2c(self, flags, payload=b"", dt=0.0004):
        seg = build_tcp(self.sip, self.cip, self.sport, self.cport,
                        self.sseq, self.cseq, flags, payload, window=65535)
        emit(self.tick(dt), self.cmac, self.smac,
             build_ipv4(self.sip, self.cip, 6, seg))
        self.sseq += len(payload) + (1 if flags & (self.SYN | self.FIN) else 0)

    def handshake(self):
        self._c2s(self.SYN)
        self._s2c(self.SYN | self.ACK, dt=0.0009)
        self._c2s(self.ACK, dt=0.0002)

    def send(self, data, dt=0.0015):
        self._c2s(self.PSH | self.ACK, data, dt=dt)

    def recv(self, data, dt=0.0110):
        self._s2c(self.PSH | self.ACK, data, dt=dt)
        self._c2s(self.ACK, dt=0.0003)

    def close(self):
        self._c2s(self.FIN | self.ACK, dt=0.0020)
        self._s2c(self.ACK, dt=0.0006)
        self._s2c(self.FIN | self.ACK, dt=0.0004)
        self._c2s(self.ACK, dt=0.0003)


# --------------------------------------------------------------------------
# 1. DNS: siapa portal-nilai.smkmaska.local?
# --------------------------------------------------------------------------
def dns_name(name):
    out = b""
    for label in name.split("."):
        out += bytes([len(label)]) + label.encode()
    return out + b"\x00"


HOST = "portal-nilai.smkmaska.local"
q = dns_name(HOST) + struct.pack("!HH", 1, 1)
dns_query = struct.pack("!HHHHHH", 0x9A3F, 0x0100, 1, 0, 0, 0) + q
dns_reply = (struct.pack("!HHHHHH", 0x9A3F, 0x8180, 1, 1, 0, 0) + q +
             struct.pack("!HHHIH", 0xC00C, 1, 1, 60, 4) + ip_bytes(IP_SERVER))

T0 = 1772000000.000000
emit(T0, MAC_GATEWAY, MAC_CLIENT,
     build_ipv4(IP_CLIENT, IP_DNS, 17, build_udp(IP_CLIENT, IP_DNS, 51514, 53, dns_query)))
emit(T0 + 0.0072, MAC_CLIENT, MAC_GATEWAY,
     build_ipv4(IP_DNS, IP_CLIENT, 17, build_udp(IP_DNS, IP_CLIENT, 53, 51514, dns_reply)))

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"


def http_post(path, body, cookie=None):
    head = [
        f"POST {path} HTTP/1.1",
        f"Host: {HOST}",
        f"User-Agent: {UA}",
        "Accept: text/html,application/xhtml+xml,*/*;q=0.8",
        "Accept-Language: id,en-US;q=0.7",
        "Content-Type: application/x-www-form-urlencoded",
        f"Content-Length: {len(body)}",
        f"Origin: http://{HOST}",
        f"Referer: http://{HOST}/login.php",
        "Connection: keep-alive",
    ]
    if cookie:
        head.append(f"Cookie: {cookie}")
    return ("\r\n".join(head) + "\r\n\r\n" + body).encode()


def http_get(path, cookie=None, accept="text/html,application/xhtml+xml,*/*;q=0.8"):
    head = [
        f"GET {path} HTTP/1.1",
        f"Host: {HOST}",
        f"User-Agent: {UA}",
        f"Accept: {accept}",
        "Accept-Language: id,en-US;q=0.7",
        f"Referer: http://{HOST}/login.php",
        "Connection: keep-alive",
    ]
    if cookie:
        head.append(f"Cookie: {cookie}")
    return ("\r\n".join(head) + "\r\n\r\n").encode()


def http_resp(status, extra_headers, body="", ctype="text/html; charset=UTF-8"):
    head = [
        f"HTTP/1.1 {status}",
        "Date: Wed, 25 Feb 2026 06:13:20 GMT",
        "Server: Apache/2.4.57 (Debian)",
        "X-Powered-By: PHP/8.2.12",
    ] + extra_headers + [
        f"Content-Type: {ctype}",
        f"Content-Length: {len(body.encode())}",
        "Connection: keep-alive",
    ]
    return ("\r\n".join(head) + "\r\n\r\n" + body).encode()


# --------------------------------------------------------------------------
# 2. Pengecoh: 192.168.10.52 gagal login (401)
# --------------------------------------------------------------------------
f1 = TcpFlow(T0 + 0.9120, IP_CLIENT2, MAC_CLIENT2, 50122, IP_SERVER, MAC_SERVER, 80)
f1.handshake()
f1.send(http_post("/login.php", "username=siswa01&password=12345"))
f1.recv(http_resp("401 Unauthorized", ["Cache-Control: no-store"],
                  "<html><body><h3>Login gagal. Periksa kembali sandi Anda.</h3></body></html>"))
f1.close()

# --------------------------------------------------------------------------
# 3. Login sukses: kredensial admin melintas polos
# --------------------------------------------------------------------------
SESSION = "PHPSESSID=b7f4c02e9ad13c5e88a1"
f2 = TcpFlow(T0 + 3.4471, IP_CLIENT, MAC_CLIENT, 49812, IP_SERVER, MAC_SERVER, 80)
f2.handshake()
f2.send(http_post("/login.php", "username=admin_nilai&password=Sup3rR4h4s1a_2026&remember=on"))
f2.recv(http_resp("302 Found", [
    f"Set-Cookie: {SESSION}; path=/",
    "Location: /dashboard.php",
    f"X-Debug-Note: {B64_BONUS}",
    "Cache-Control: no-store",
], ""))

# --------------------------------------------------------------------------
# 4. Dashboard: FLAG utama tertinggal di komentar HTML
# --------------------------------------------------------------------------
DASH = (
    "<!DOCTYPE html>\n<html lang=\"id\">\n<head>\n"
    "  <meta charset=\"UTF-8\">\n"
    "  <title>Portal Nilai - SMK Maskumambang 1</title>\n"
    "  <link rel=\"stylesheet\" href=\"/assets/style.css\">\n"
    "</head>\n<body>\n"
    "  <h1>Dasbor Wali Kelas</h1>\n"
    "  <p>Selamat datang, <b>admin_nilai</b>. Terakhir masuk: 25/02/2026 13:13 WIB.</p>\n"
    "  <table>\n"
    "    <tr><th>NIS</th><th>Nama</th><th>Rerata</th></tr>\n"
    "    <tr><td>10231</td><td>Nabila R.</td><td>88</td></tr>\n"
    "    <tr><td>10232</td><td>Fahri A.</td><td>91</td></tr>\n"
    "  </table>\n"
    f"  <!-- catatan dev: hapus sebelum rilis. token audit internal = {FLAG_MAIN} -->\n"
    "</body>\n</html>\n"
)
f2.send(http_get("/dashboard.php", cookie=SESSION), dt=0.0180)
f2.recv(http_resp("200 OK", ["Vary: Accept-Encoding"], DASH), dt=0.0141)

CSS = ("body{font-family:sans-serif;background:#f9f9fe;color:#00355f}\n"
       "table{border-collapse:collapse;width:100%}\n"
       "th,td{border:1px solid #ededf3;padding:6px}\n")
f2.send(http_get("/assets/style.css", cookie=SESSION, accept="text/css,*/*;q=0.1"), dt=0.0090)
f2.recv(http_resp("200 OK", ["Cache-Control: max-age=3600"], CSS, ctype="text/css"), dt=0.0062)

f2.send(http_get("/favicon.ico", cookie=SESSION, accept="image/avif,image/webp,*/*"), dt=0.0110)
f2.recv(http_resp("404 Not Found", [], "<html><body>404</body></html>"), dt=0.0058)
f2.close()

# --------------------------------------------------------------------------
# 5. Pembanding: sesi TLS: terlihat, tetapi tidak terbaca
# --------------------------------------------------------------------------
def client_hello(sni: str) -> bytes:
    sni_b = sni.encode()
    server_name = b"\x00\x00" + struct.pack("!H", len(sni_b) + 5) + \
        struct.pack("!H", len(sni_b) + 3) + b"\x00" + struct.pack("!H", len(sni_b)) + sni_b
    ext_versions = b"\x00\x2b\x00\x03\x02\x03\x04"
    exts = server_name + ext_versions
    body = (b"\x03\x03" + bytes(range(32)) + b"\x20" + bytes(range(0x40, 0x60)) +
            struct.pack("!H", 4) + b"\x13\x01\x13\x02" + b"\x01\x00" +
            struct.pack("!H", len(exts)) + exts)
    hs = b"\x01" + struct.pack("!I", len(body))[1:] + body
    return b"\x16\x03\x01" + struct.pack("!H", len(hs)) + hs


def app_data(seed, size):
    blob = bytes(((seed * 31 + i * 97) % 251) + 3 for i in range(size))
    return b"\x17\x03\x03" + struct.pack("!H", size) + blob


f3 = TcpFlow(T0 + 7.2600, IP_CLIENT, MAC_CLIENT, 49855, IP_TLS, MAC_GATEWAY, 443)
f3.handshake()
f3.send(client_hello("mail.smkmaska.sch.id"))
f3.recv(app_data(11, 512), dt=0.0208)
f3.send(app_data(23, 240), dt=0.0044)
f3.recv(app_data(41, 880), dt=0.0190)
f3.close()

packets.sort(key=lambda p: p[0])

OUT = "/home/aal/jcc-2026/lab01/lab01-wire-sniffer.pcap"
with open(OUT, "wb") as fh:
    fh.write(struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1))
    for ts, raw in packets:
        sec = int(ts)
        usec = int(round((ts - sec) * 1_000_000))
        fh.write(struct.pack("<IIII", sec, usec, len(raw), len(raw)))
        fh.write(raw)

print(f"file       : {OUT}")
print(f"paket      : {len(packets)}")
print(f"flag utama : {FLAG_MAIN}")
print(f"flag bonus : {FLAG_BONUS}  (base64: {B64_BONUS})")
