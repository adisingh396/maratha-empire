# Maratha Empire — Akhand Bharat: MASSIVE EXPANSION SPEC

Goal: bring the mod to Kaiserreich-tier depth. Replace shallow templated events with
grounded flavor chains; add real what-if focus branches; grow every nation's character
roster with validated historical figures (see `docs/research/research_T*.md`); wire new
ideas, decisions, opinion modifiers, localisation, and portraits.

Premise recap: the subcontinent was NEVER colonized. The Maratha Confederacy survived;
1936 India is balkanized into 15 industrializing kingdoms playing Game-of-Thrones.

## Quality bar (from Kaiserreich BNG/PJB/RAJ trees + existing MAR_mandala events)
- Events: real title/desc flavor prose (2-5 sentences), branching options with DISTINCT
  consequences (flags, wargoals, ideas, opinion, state effects) — NOT two identical options.
- Focus branches: mutually_exclusive ideology forks, `swap_ideas` upgrade chains, real
  completion_reward effects tied to the what-if scenario, `ai_will_do` weights.
- Characters: real people from research files, multiple ideologies for leaders, generals
  with skills, advisors with idea_tokens + traits.

## Ideologies in this mod
`despotism`, `fascism_ideology` (popularity key `fascism`), `democratic`, `communism`.
Leader block: `country_leader = { ideology = <x> traits = { <trait> } expire = "1965.1.1" id = -1 }`.
Common traits seen: conservative_grandee, popular_figurehead, warmonger. Advisor traits:
army_chief_army_high_command, backroom_backstabber, economist, military_theorist, etc.

## FILE OWNERSHIP (NO cross-agent collisions — each file owned by exactly one agent)
Every agent creates NEW files or edits ONLY its own nation's existing files.
Per nation `<TAG>`:
- `common/characters/<TAG>_characters.txt` — EDIT (append new validated characters).
- `events/<TAG>_flavor_events.txt` — NEW FILE (namespace `<TAG>_flav`).
- `common/national_focus/<TAG>_focus.txt` — EDIT (append new focus branches to the tree; keep existing focuses).
- `common/ideas/<TAG>_expanded_ideas.txt` — NEW FILE (new national spirits; do NOT touch shared princely_ideas.txt / maratha_ideas.txt).
- `localisation/english/<TAG>_expanded_l_english.yml` — NEW FILE (UTF-8 BOM, `l_english:` header). ALL new loc keys here.
- `interface/<TAG>_portraits.gfx` — EDIT (append spriteType for each new portrait).
- Append portrait rows to `tools/portrait-pipeline/manifest_<CLUSTER>.json` fragment (see Portrait section).

SHARED files — Main handles these alone (do NOT edit from content agents):
- `common/decisions/got_world_decisions.txt` + categories
- `common/ideas/princely_ideas.txt`, `common/ideas/maratha_ideas.txt`, `common/ideas/maratha_economy.txt`
- `localisation/english/maratha_l_english.yml`, `maratha_got_l_english.yml`

## NAMESPACE / ID ALLOCATION (avoid duplicate event ids)
New flavor namespaces (each `add_namespace = <TAG>_flav`), event ids `<TAG>_flav.1`..`.40`.
Existing namespaces to NOT reuse ids in: `<TAG>_ev`, and MAR_court/mandala/news/got/revolt, HYD_nizam/state, MYS_dam.
Decision categories: new `<TAG>_flavor_category` per nation if decisions added (in the nation's own new decisions file `common/decisions/<TAG>_flavor_decisions.txt` — NEW FILE, optional).

## PORTRAIT NAMING
GFX name: `GFX_portrait_<tag_lower>_<shortname>` (+ `_small`). Texture: `gfx/leaders/<TAG>/portrait_<tag_lower>_<shortname>.dds`.
Manifest fragment row: `{ "character": "<TOKEN>", "country": "<TAG>", "stem": "portrait_<tag_lower>_<shortname>", "description": "<real appearance: age, beard, headwear, dress, expression, per era>" }`.
Portrait STYLE (fixed, do not restate per row): high-quality hand-painted grand-strategy military portrait, 1930s-40s illustration, realistic anatomy, restrained historical palette, warm neutral canvas, centered bust, no text/CGI/anime.
Fallback safety: every `<TAG>_portraits.gfx` should keep a generic fallback so missing DDS never crashes.

## PER-NATION EXPANSION TARGETS (min deliverables per nation)
- +6-12 validated characters (leaders w/ multiple ideologies where research supports, generals, admirals, advisors, theorists).
- +1 flavor event chain (4-8 linked events) + 3-6 standalone flavor events, all with real prose + branching.
- +1-2 new focus branches (5-10 focuses) implementing a what-if scenario from research, with new spirits.
- +3-6 national spirits/ideas.
- Full localisation for everything above.
- Portrait manifest rows for every NEW character.

## CLUSTER ASSIGNMENTS
- **Cluster A (Main):** MAR (Maratha) — hegemon, deepest tree. + shared GoT decisions/loc.
- **Cluster B:** BEN, HIN, HYD, PJB (tier 1-2 powers). Manifest → manifest_B.json.
- **Cluster C:** MYS, MDR, RJP, WIS (tier 3). Manifest → manifest_C.json.
- **Cluster D:** TRV, SIN, ORI, ASM, KAS, MPU (tier 4-5). Manifest → manifest_D.json.

## KEY WHAT-IF BRANCHES PER NATION (from research — implement as focus branches + event chains)
- **MAR:** Confederacy-vs-Centralism (Scindia/Holkar/Gaekwad/Bhonsle autonomy vs Pune); Peshwa-vs-Chhatrapati legitimacy; Mahadaji's Drilled Army; Angre Blue-Water; Hindutva (Savarkar) vs Reformist (Ambedkar/Karve) fork.
- **BEN:** Netaji's Bengal (Bose authoritarian-modernizer); Revolutionaries-take-power (Anushilan/Jugantar officer corps); United-vs-Partitioned Bengal; Krishak peasant republic; Scientist-State (JC Bose/Saha/Ray); Coal-Jute-Steel powerhouse.
- **HIN (Awadh):** Restored Wali of Awadh; Taluqdar Confederation; 1857 Legacy Rising; Revolutionary Underground; Aligarh-vs-Banaras culture war.
- **HYD:** Sovereign Nizamate (Osmanistan); Razakar State (Kasim Razvi fascism); Telangana People's War (communist); Ganga-Jamuni reform; Salar Jung technocratic restoration; March of the Deccan vs MAR.
- **PJB:** Second Khalsa Raj (Ranjit Singh dynasty restoration); Panthic State (Master Tara Singh); Unionist Compromise; Ghadar Rising; March of the Khalsa (frontier reconquest); Partition Crisis (3-way).
- **MYS:** Engineer-King's Five-Year Plan (Visvesvaraya); HAL aviation arsenal; Regency Question (1940 succession); Mysore-Model-vs-Congress; Sandalwood & Gold war-chest.
- **MDR (Tamilakam):** Dravida Nadu Rising (Periyar); Justice Party Raj; Chettiar Banking Empire; Rajaji Free-Market Republic; Southern Dockyards (Vizag); Cauvery casus belli vs MYS.
- **RJP:** Rajput Confederation (Chamber of Princes); Ganga Risala camel-mech corps; Marwari Capital vs Desert Crown; Jodhpur Air Arm; Canal Wars of the Thar vs PJB.
- **WIS (Gujarat):** Gaekwad Enlightenment; Manchester-of-the-East textiles; Kathiawar Maritime League; Diamond Road trade; Baroda Succession & the Maratha Question (join MAR core).
- **TRV:** Monazite Gambit (rare-earth + secret nuclear); Independent Travancore (CP Iyer 1947); Punnapra-Vayalar communist rising; Diwan's Terror vs Responsible Govt; Chemical Powerhouse.
- **SIN:** Sindh Reborn (1936 separation); Hur Rebellion (Pir Pagaro); Karachi Free Port republic; Talpur Restoration; Secular-Sindh-vs-Two-Nation (Allah Bakhsh).
- **ORI (Kalinga):** Utkal Sammilani unification; Garjat Praja Mandal rising; Kalinga Reborn maritime; Mineral Kingdom (Sukinda/iron/coal); Mayurbhanj Model State.
- **ASM:** Ahom Restoration; Black Gold of Digboi; Planters' Raj; Hills-vs-Plains (Naga); Grouping Crisis (resist Bengal absorption).
- **KAS:** Switzerland of Asia (Hari Singh independence); Naya Kashmir (Abdullah socialist); Gilgit Revolt; Zorawar's Heirs (Himalayan expansion); 1931 communal fracture.
- **MPU:** Kangleipak Restored (Meitei monarchy); Sanamahi cultural revival; Nupi Lan women's war; Kabaw Valley irredentism vs Burma; Imphal Corridor (WW2).

## HARD RULES
- Every referenced loc key, idea, spirit, GFX, idea_token MUST be defined.
- No duplicate character tokens, event ids, idea names, focus ids.
- Keep existing content working (append, don't delete).
- Focus tree edits: add focuses with unique x/y that don't overlap existing (check existing max x/y; place new branches at higher x or lower y-rows below existing).
- Skip validation/build during work — Main runs MCP validate_syntax at the end.
- Country leader `id = -1` and `expire` required. Dynastic-extrapolation leaders (fictional 1936 Peshwa/Angre heir) allowed ONLY where research marks them; base on real lines.
