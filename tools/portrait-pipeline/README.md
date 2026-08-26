# Maratha Portrait Pipeline — 4x Gemini Bulk (vedic-lore clone)

Replicates `vedic_lore/vedic_pipeline` (50 grids → 200 quadrants) but for HOI4 hand-painted military portraits.

## Why 4x
`vedic_generate.py` does **50 Gemini calls → 200 images** by prompting for a strict `2x2 grid` (four equal quadrants, thin beige divider) and splitting via PIL `split_grid_pil`. We reuse same bulk logic: **1 Gemini call → 4 portraits**. Scales to `N grids → N*4 portraits` (e.g., 10 grids = 40 leaders). Research via `websearch` + `google-ai-search` + `hf-mcp-server` shows HOI4 needs `156x210` strict, DDS DXT5 BC3 with mipmaps and 8-bit RGBA, or PNG 32-bit fallback (modern HOI4 supports PNG).

## Files
- `build_prompts.py` — builds `prompts.txt` (1 line per grid) from `STYLE` + 4 quadrants. Each quadrant is **far more than just a name**: age, beard, turban, armor, fabric folds, medal details, skin, expression, same beige canvas grain. Style block is your exact `Chhatrapati Shivaji Maharaj **high-quality hand-painted...` prompt` (semi-realistic, soft studio lighting, muted olive/beige/gray palette, parchment vignette, avoid CGI/anime).
- `prompts.txt` / `prompts_pretty.txt` — 1 grid prompt (≈4031 chars, 4 quadrants: Shivaji, Baji Rao, Tarabai, Madhavrao III)
- `cookies.json` — Gemini web cookies (`__Secure-1PSID`, `__Secure-1PSIDTS`, `NID`, `APISID`, `COMPASS`, `SID` etc. provided by user). Same list-of-dicts format as vedic.
- `maratha_generate.py` — copied from `vedic_generate.py` (StrEnum backport, `GeminiClient`, `RATE_LIMIT_DELAY=18`, `MAX_RETRIES=3`, `progress.json`, `split_grid_pil`). Generates `generated/grid_01/grid.png` (1024x1024 JPEG) → splits to `top_left.png` etc (512x512 each).
- `convert_to_hoi4.py` — bulk conversion: crop 512x512 square to portrait aspect `156/210=0.742` (380x512 centered crop → resize 156x210 Lanczos), then save `PNG` (32-bit) + `DDS` (Pillow DDS, auto DXT5, mipmaps). Also generates `65x67` small for advisor fallback (`GFX_*_small`). Writes to `gfx/leaders/MAR/` in both repo and live mod (`Documents/Paradox Interactive/Hearts of Iron IV/mod/maratha-empire/...`).

## Quick Run (bulk)
```powershell
cd tools/portrait-pipeline
python build_prompts.py                          # (re)builds prompts.txt from STYLE+quadrants
C:\Users\zendrix\AppData\Local\Programs\Python\Python310\python.exe maratha_generate.py  # Gemini, 18s delay, progress.json
python convert_to_hoi4.py                        # → gfx/leaders/MAR/portrait_mar_*.dds (131168 bytes) + _small.dds (17548) + .png
# verify
..\sync.ps1  # if pipeline lives outside repo, copy to live mod
```

## Research-backed DDS specs (via `websearch`/`google-ai-search`)
- **Dimensions:** 156×210 strict (leader), 65×67 advisor
- **Format:** DDS DXT5 / BC3 (Explicit Alpha), 8-bit RGBA, Generate Mipmaps checked, 2D Texture. Pillow `Image.save(..., format='DDS')` auto-writes DXT5 when RGBA. Verified: vanilla `RAJ` 131168 bytes, ours 131168 bytes.
- **Path:** `gfx/leaders/MAR/portrait_mar_*.dds` + `interface/MAR_portraits.gfx` `spriteType = { name="GFX_portrait_mar_*" texturefile="gfx/leaders/MAR/..." }`
- **Fallback:** PNG (156×210, 32-bit) also works; we emit both. `.gfx` can point to `.png` if DDS fails.

## Scaling to N*4
Edit `build_prompts.py` quadrants list → add more 4-blocks (e.g., 10 leaders = 3 grids) → `python build_prompts.py` → `maratha_generate.py` will loop `grid_01..grid_N` with `progress.json` resume and 18s rate-limit, merging with vedic's 50-grid logic.

## Current Output (Gemini, not HF)
- `generated/grid_01/grid.png` 1024x1024 + 4 quadrants 512x512 (Gemini, cookies.json from user)
- Previous HF backup: `generated/grid_01_hf_backup/grid.png` 1536x1536 (Z-Image turbo, kept for reference)
- Final HOI4: `gfx/leaders/MAR/portrait_mar_shivaji/bajirao/tarabai/madhavrao` + `_small` (both DDS+PNG)

## Notes
- Uses Google Gemini AI pipeline (gemini_webapi) as requested, not HF. HF Z-Image was tested earlier but replaced per user instruction.
- Cookies are session-bound; refresh `cookies.json` via `vedic_lore/vedic_pipeline/cookies.py` if 401.
- Keep `tools/portrait-pipeline/generated/` gitignored if bulk grows (200 images ~ 50MB).
