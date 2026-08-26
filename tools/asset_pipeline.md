# Asset Pipeline — Maratha Empire

## Flags
- Source: `gfx/flags/MAR.tga` (82x52), medium (41x26), small (10x7). Generate via `tools/generate_flags.py` (PIL).
- Saffron #FF6600 Bhagwa, ideology variants: democratic lighter, fascism dark saffron + sun emblem, neutrality standard, communism same (placeholder).
- To replace with historical flag: drop PNG 82x52 into `tools/sources/flag.png` then run `python tools/flag_to_tga.py` (converts PNG→TGA + DDS via Pillow/Wand).
- HOI4 expects TGA; game also reads DDS if provided. Keep both.

## Focus Icons
- MVP reuses vanilla `GFX_goal_generic_*` (no custom art needed).
- Custom icons: place 40x40 PNGs in `gfx/interface/goals/` as `goal_maratha_*.png`, convert to DDS:
  `python tools/convert_focus_icons.py --src gfx/interface/goals --dst gfx/interface/goals`
  Generates `.dds` + updates `interface/maratha_goals.gfx` spriteTypes.
- Fetch helper: `python tools/fetch_icons.py --query "maratha shivaji fort"` pulls CC0 PNGs from Wikimedia, resizes, strips background.

## Portraits / Leaders
- Place 156x200 PNG in `gfx/leaders/MAR/`, run `python tools/portrait_to_dds.py`.

## Conversion
- Requires Pillow (`pip install Pillow`). No extra dependency for TGA.
- For DDS with DXT5: use `texconv` or `PIL` with `dds` plugin, fallback to TGA.

## Notes
- Kaiserreich reference: `mod/Kaiserreich/gfx/` — many reusable industrial/naval icons if needed (copy with credit, not TGA raw; re-render).
- Always validate with HoI4 error.log `missing texture` lines.
