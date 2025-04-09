from PIL import Image, ImageOps

# Eingabedatei
input_file = "logo.png"  # ← Dein Logo hier reinlegen

# Zielgrößen und Dateinamen
outputs = [
    ("icon-192.png", 192, False),
    ("icon-512.png", 512, False),
    ("icon-maskable.png", 512, True)
]

# Bild laden
original = Image.open(input_file).convert("RGBA")

for filename, size, maskable in outputs:
    img = original.copy()

    if maskable:
        # Padding hinzufügen (z.B. 20% rundherum)
        padding = int(size * 0.2)
        background = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        img.thumbnail((size - 2 * padding, size - 2 * padding), Image.LANCZOS)
        position = ((size - img.width) // 2, (size - img.height) // 2)
        background.paste(img, position)
        img = background
    else:
        img = ImageOps.fit(img, (size, size), Image.LANCZOS)

    img.save(filename)
    print(f"{filename} erzeugt.")

print("Alle Icons wurden erfolgreich generiert.")
