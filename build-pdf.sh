#!/usr/bin/env bash
# Build modul praktikum: Markdown -> HTML cetak -> PDF
# Pakai: ./build-pdf.sh [file.md]
set -euo pipefail
cd "$(dirname "$0")"

SRC="${1:-LAB01-The-Wire-Sniffer.md}"
BASE="${SRC%.md}"

# -yaml_metadata_block  : baris '---' jangan dibaca sebagai metadata YAML
COMMON=(-f markdown-yaml_metadata_block -s --embed-resources
        --metadata title="LAB 01: The Wire Sniffer"
        --metadata lang=id
        -c assets/print.css)

pandoc "${COMMON[@]}" "$SRC" -o "$BASE.html"
echo "HTML : $BASE.html"

if command -v weasyprint >/dev/null 2>&1; then
    # WeasyPrint salah menggambar emoji berwarna, jadi khusus jalur PDF
    # emoji ditukar dengan simbol Unicode dari font teks biasa.
    TMP=".print-$$.md"
    python3 assets/emoji-print.py "$SRC" "$TMP"
    pandoc "${COMMON[@]}" --pdf-engine=weasyprint "$TMP" -o "$BASE.pdf"
    rm -f "$TMP"
    echo "PDF  : $BASE.pdf  (weasyprint, simbol cetak + ganti halaman aktif)"
elif command -v xelatex >/dev/null 2>&1; then
    pandoc -f markdown-yaml_metadata_block "$SRC" -o "$BASE.pdf" \
        --pdf-engine=xelatex -V geometry:margin=2cm \
        -V mainfont="Noto Sans" -V monofont="JetBrains Mono" -V colorlinks
    echo "PDF  : $BASE.pdf  (xelatex, emoji kemungkinan kosong)"
else
    echo "PDF  : dilewati, tidak ada engine PDF di sistem ini."
    echo
    echo "  Pilihan 1 (disarankan, ringan ~15 MB):"
    echo "      sudo pacman -S python-weasyprint && ./build-pdf.sh"
    echo
    echo "  Pilihan 2 (tanpa instalasi apa pun):"
    echo "      xdg-open $BASE.html   lalu tekan Ctrl+P > Save as PDF"
    echo "      Di dialog cetak: ukuran A4, Margins = Default, centang Background graphics."
fi
