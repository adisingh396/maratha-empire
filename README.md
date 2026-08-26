# Maratha Empire — Akhand Bharat (MAR) • HOI4 Mod

> What if the Maratha Confederacy never fell? A balkanized, semi-industrialized India in 1936, where the Peshwa still rules Maharashtra and every princely state plays Game of Thrones.

**Tag:** `MAR` (independent) — Maharashtra cores only at start (Bombay + Deccan). Every other `RAJ` successor is balkanized: Hyderabad, Mysore, Rajputana, Sind, Kashmir, Punjab, Bengal, Madras etc. 30-35 factories base (Bombay + Deccan), strong Angre navy.

![Maratha](gfx/maratha_thumb.png)

## Features
- **New country** `MAR = "countries/Maratha.txt"` • saffron `255,102,0` • `MAR_INF_01`/`MAR_GAR_01` names
- **Balkanized India** — 26 state overrides `history/states/*.txt`: `HYD` 427 Hyderabad strong (5civ/4mil), `MYS` 425, `RJP` 433/989/991, `WIS` 428 Gujarat, `SIN` 443, `KAS` 441 Kashmir, `PAK` 440/442 Punjab, `BAN` 430/431 Bengal, `CIP` 436/437 etc. RAJ reduced to residual (RAJ_1936 empty `units={}`).
- **Focus tree** `common/national_focus/maratha_focus.txt` — 50 focuses (Germany/Kaiserreich-scale): Modernist/Industrial (Tata Steel/Bombay Stock/Synthetic, Pune Univ), Rajput martial + Sainik/Gardi artillery (Udgir 1760 history), Peshwa restoration (Peshwa Privy → Hindavi Swarajya vs Modernist Republic), Soft vs Hard `Mandal of Influence` (Cultural Diplomacy vs Military Mission → Hyderabad/Mysore annex vs Himalayan puppets), Akhand Bharat unification (cores all empire states), Angre navy → Blue-Water → Carrier → World Navy → `Pax Marathica`. All `GFX_goal_generic_*` validated, decompressed layout `x0-15`.
- **Leaders** `common/characters/MAR_characters.txt` (Madhavrao III + Ibrahim Khan Gardi) + `interface/MAR_portraits.gfx` fallback to `RAJ` generic DDS.
- **Ideas** `MAR_peshwai_legacy`/`MAR_rajput_dominance`/`MAR_moderate_industrial_base` + 4 more.
- **Decisions** per-princely dynamic: `HYD_form_deccan_sultanate` (Muslim empire), `RJP_form_rajput_confederation`, `MYS_expand_karnataka` + MAR integration (Deccan/Rajputana/Bengal cores). Categories per tag in `common/decisions/categories/*`.
- **News events** `events/MAR_news_events.txt` (`MAR_news.1` Peshwa restored, `.2` Akhand Bharat, `.3` Gardi returns, `MAR_news.10` Deccan Sultanate) — TNO-style `news_event` broadcast to `every_country`.
- **Gfx pipeline** `tools/asset_pipeline.md` + `tools/generate_flags.py` + `tools/balkanize.py` (PNG→TGA/DDS via Pillow, `hoi4_flag_maker` logic, Kaiserreich sampling).

## History flavor
1759 Udgir: Nanasaheb/Sadashivrao Bhau vs Nizam, Chauth/Sardeshmukhi revenue, Gardi sepoy line infantry, Karkhana cannon foundries → treaty Feb 1760 (Daulatabad/Asirgarh/Burhanpur ceded). Seeds the 1936 Peshwai legitimacy.

## Install
1. Enable `maratha-empire.mod` in Paradox launcher (`Documents/Paradox Interactive/Hearts of Iron IV/mod/`). Add `"mod/maratha-empire.mod"` to `dlc_load.json:enabled_mods` or toggle in launcher.
2. Requires vanilla + all DLC (avoid Graveyard of Empires inspiration intentionally).

## Dev / Sync
This repo **is** the mod source. The live mod lives at:
```
Documents/Paradox Interactive/Hearts of Iron IV/mod/maratha-empire/
Documents/Paradox Interactive/Hearts of Iron IV/mod/maratha-empire.mod
```
Sync changes:
```powershell
# From repo root:
.\sync.ps1        # copies repo → Paradox mod folder
.\sync.ps1 -Reverse  # pulls Paradox → repo (if you edited in launcher)
```
See `SYNC.md` for `robocopy`/`mklink` variants. No `hoi4.exe` launch needed for validation — use `hoi4-modding-server` (`get_mod_index`, `validate_syntax`).

## Tools found via GitHub/Google AI research
`KwngAstro/Hoi4-Modding-Tools`, `Veselator/ANKA_HOI4_mod_editor`, `AceSpectre/HOI4-Utility-Tool`, `atthematyo/hoi4_flag_maker`, `MillenniumDawn/cwtools` (Rust validator), `klimPaskov/hoi4-agent-tools` (MCP), `OlanderIAO/HOI4-Modding-Tools-Extension-for-VSC`.

## License
Public. Credit Kaiserreich where sampled.
