"""Erzeugt die PWA-Icons aus logo.png.

Aufruf aus dem Projektwurzelverzeichnis:  python3 script/gen.py
Benoetigt Pillow:                         pip install pillow
"""

from pathlib import Path

from PIL import Image, ImageOps

# Pfade relativ zum Projektwurzelverzeichnis, nicht zum aktuellen Arbeitsverzeichnis.
ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT / "logo.png"
OUTPUT_DIR = ROOT / "icons"

# Zielgroessen und Dateinamen
outputs = [
    ("icon-192.png", 192, False),
    ("icon-512.png", 512, False),
    ("icon-maskable.png", 512, True),
]

OUTPUT_DIR.mkdir(exist_ok=True)
original = Image.open(INPUT_FILE).convert("RGBA")

for filename, size, maskable in outputs:
    img = original.copy()

    if maskable:
        # Padding hinzufuegen (20% rundherum), damit die Maske nichts abschneidet.
        padding = int(size * 0.2)
        background = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        img.thumbnail((size - 2 * padding, size - 2 * padding), Image.LANCZOS)
        position = ((size - img.width) // 2, (size - img.height) // 2)
        background.paste(img, position)
        img = background
    else:
        img = ImageOps.fit(img, (size, size), Image.LANCZOS)

    target = OUTPUT_DIR / filename
    img.save(target, optimize=True)
    print(f"{target.relative_to(ROOT)} erzeugt.")

print("Alle Icons wurden erfolgreich generiert.")
