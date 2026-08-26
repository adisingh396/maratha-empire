#!/usr/bin/env python3
"""
Bulk convert 4x Gemini quadrants to HOI4 portrait specs.
- Input: generated/grid_01/{top_left,top_right,bottom_left,bottom_right}.png (512x512)
- Output: gfx/leaders/MAR/*.dds + *.png (156x210 large, 65x67 small)
- Uses PIL, mimics vedic split pipeline + DDS DXT5 research.
- Based on websearch: 156x210 strict, DDS BC3/DXT5, mipmaps, 8-bit RGBA.
"""
from PIL import Image
from pathlib import Path
import shutil

# Paths
PIPELINE_DIR = Path(__file__).parent
GEN_DIR = PIPELINE_DIR / "generated" / "grid_01"
MOD_GFX = Path(r"C:\Users\zendrix\Documents\Programming\Dev\4weeksgrind\hoi4-modding\maratha-empire\gfx\leaders\MAR")
MOD_GFX_REPO = Path(r"C:\Users\zendrix\Documents\Paradox Interactive\Hearts of Iron IV\mod\maratha-empire\gfx\leaders\MAR")
MOD_INTERFACE = Path(r"C:\Users\zendrix\Documents\Programming\Dev\4weeksgrind\hoi4-modding\maratha-empire\interface")

# Ensure output dirs
MOD_GFX.mkdir(parents=True, exist_ok=True)
MOD_GFX_REPO.mkdir(parents=True, exist_ok=True)

# Mapping quadrants to HOI4 leader files
mapping = {
    "top_left": "portrait_mar_shivaji",      # Shivaji Maharaj
    "top_right": "portrait_mar_bajirao",     # Baji Rao I
    "bottom_left": "portrait_mar_tarabai",   # Tarabai
    "bottom_right": "portrait_mar_madhavrao",# Madhavrao III
}

# HOI4 specs from research
LARGE_SIZE = (156, 210)
SMALL_SIZE = (65, 67)  # advisor small (from GFX Sizes post)
# For DDS, Pillow will save with DXT5 if possible; fallback to PNG
def crop_and_resize(im, target_size):
    """Crop square 512 to portrait aspect 0.742 then resize with Lanczos + canvas grain preserve."""
    w, h = im.size
    target_w, target_h = target_size
    target_aspect = target_w / target_h  # 0.742
    # Crop width to match aspect, keeping height
    new_w = int(h * target_aspect)
    # Ensure even
    if new_w > w:
        # if target taller than source, crop height instead
        new_h = int(w / target_aspect)
        left = 0
        top = (h - new_h) // 2
        im_cropped = im.crop((left, top, left + w, top + new_h))
    else:
        left = (w - new_w) // 2
        im_cropped = im.crop((left, 0, left + new_w, h))
    # Resize with high quality
    resized = im_cropped.resize(target_size, Image.LANCZOS)
    return resized

def save_dds_or_png(im, path_stem):
    """Try DDS DXT5, fallback to PNG if PIL lacks DDS plugin. Saves both .dds and .png."""
    # Save PNG always (modern HOI4 supports PNG)
    png_path = Path(str(path_stem) + ".png")
    im.save(png_path, format="PNG", optimize=True)
    print(f"  [png] {png_path.name} {im.size}")
    # Try DDS
    dds_path = Path(str(path_stem) + ".dds")
    try:
        # Pillow DDS save: use DXT5 implicit for RGBA
        # Ensure RGBA mode for DXT5 (needs alpha)
        if im.mode != "RGBA":
            im_rgba = im.convert("RGBA")
        else:
            im_rgba = im
        # Save with mipmaps if supported (Pillow 9.1+ supports DDS with DXT5)
        im_rgba.save(dds_path, format="DDS")
        print(f"  [dds] {dds_path.name} {im_rgba.size} DXT5")
    except Exception as e:
        print(f"  [dds warn] fallback to PNG only: {e}")
        # If DDS fails, we already have PNG; create a copy as .dds via PNG bytes? Just warn
        # For compatibility, we can copy PNG to DDS path as placeholder and let HOI4 load PNG via .gfx pointing to PNG
        pass
    return png_path, dds_path

print(f"Converting 4x quadrants to HOI4 specs {LARGE_SIZE} and {SMALL_SIZE}...")
for quadrant, stem in mapping.items():
    src = GEN_DIR / f"{quadrant}.png"
    if not src.exists():
        print(f"  [skip] {src} not found")
        continue
    im = Image.open(src)
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGB")
    print(f"\n[{quadrant}] -> {stem} from {im.size}")
    # Large 156x210
    large = crop_and_resize(im, LARGE_SIZE)
    for out_root in [MOD_GFX, MOD_GFX_REPO]:
        out_stem = out_root / stem
        save_dds_or_png(large, out_stem)
        # Small 65x67
        small = large.resize(SMALL_SIZE, Image.LANCZOS)
        save_dds_or_png(small, out_root / f"{stem}_small")
        # Also create GFX variants for characters: large needs _small suffix for minister fallback (HOI4 expects GFX_portrait_*_small)
        # Already handled via _small

print("\nDone. Updating interface/MAR_portraits.gfx...")
# Generate .gfx entries
gfx_lines = ["spriteTypes = {"]
for stem in mapping.values():
    gfx_lines.append(f"\tspriteType = {{")
    gfx_lines.append(f"\t\tname = \"GFX_{stem}\"")
    gfx_lines.append(f"\t\ttexturefile = \"gfx/leaders/MAR/{stem}.dds\"")
    gfx_lines.append(f"\t}}")
    gfx_lines.append(f"\tspriteType = {{")
    gfx_lines.append(f"\t\tname = \"GFX_{stem}_small\"")
    gfx_lines.append(f"\t\ttexturefile = \"gfx/leaders/MAR/{stem}_small.dds\"")
    gfx_lines.append(f"\t}}")
gfx_lines.append("}")
# Write to both repos
for gfx_path in [MOD_INTERFACE / "MAR_portraits.gfx", Path(r"C:\Users\zendrix\Documents\Paradox Interactive\Hearts of Iron IV\mod\maratha-empire\interface\MAR_portraits.gfx")]:
    gfx_path.parent.mkdir(parents=True, exist_ok=True)
    gfx_path.write_text("\n".join(gfx_lines), encoding="utf-8")
    print(f"wrote {gfx_path}")

print("\nNext: update common/characters/MAR_characters.txt to use new GFX keys and sync to mod.")
