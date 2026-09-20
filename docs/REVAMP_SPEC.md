# Maratha Empire — Akhand Bharat: Canonical Revamp Spec

Alt-history premise: the subcontinent was never colonized. Regional Hindu/Muslim/Sikh
kingdoms industrialized from old wealth (textiles, ports, mines, arsenals) on their own
terms — think Balkans-to-Germany spread, NOT uniform. Each nation has ONE economic
specialty it exports and grows rich on. Recruitable population is subtly higher than
vanilla minors (large populous states) but never hard-capped. Majors can reach 5-6x
strength by late game ONLY via disciplined focus routes; cheap/trap routes stall them.

## Vanilla scale anchors (1936, measured from game files)
- Germany: 80 factories (37 IC / 33 MIL / 10 dock), 65.5M, max 7 IC per state.
- Czechoslovakia (industrial minor): 25 factories, 15M.
- Poland: 32 factories, 31.9M. Yugoslavia: 19. Romania: 20. Hungary: 17. Bulgaria: 14.
- Rule of thumb: NO ordinary state exceeds 7 IC or ~6 MIL. Only capital/industrial-core
  states approach that. Backwater/frontier states get 0-2 factories + resources instead.

## Tiers (starting factories = IC + MIL + dock, whole nation)

### Tier 1 — Industrial hegemons (Germany-class, 55-70)
- **MAR Maratha Empire** — the hegemon. Heavy industry + arsenals (Bombay/Pune/Deccan).
  ~62 factories. Specialty: MACHINE TOOLS & ORDNANCE. Exports arms, imports nothing.
- **BEN Bengal** — Calcutta jute/steel/coal powerhouse. ~55 factories.
  Specialty: STEEL & TEXTILES (Calcutta mills, Raniganj coal, jute monopoly).

### Tier 2 — Regional powers (Czechoslovakia-class, 32-45)
- **HIN Ganga Federation (Awadh)** — vast Gangetic population + UP/Bihar industry. ~42.
  Specialty: MANPOWER & AGRICULTURE (breadbasket; cheap, huge army; weak per-capita ind.)
- **HYD Hyderabad** — Nizam's dominion, Deccan mineral wealth + Golconda. ~38.
  Specialty: MINING & PRECIOUS METALS (diamonds, gold, chromium → buys industry).
- **PJB Punjab (Sikh Empire)** — canal-colony grain + Lahore arsenal + martial races. ~36.
  Specialty: MILITARY MANPOWER & AGRICULTURE (best soldiers, high conscription pool).

### Tier 3 — Specialist mid-powers (Yugoslavia/Romania-class, 22-30)
- **MYS Mysore** — Visvesvaraya's model state: HAL aviation, KRS hydro, Bhadravati steel. ~28.
  Specialty: AVIATION & ELECTRICITY (research bonuses, air head-start).
- **MDR Madras Presidency (Tamilakam)** — textile + port + rubber south. ~30.
  Specialty: TEXTILES & DOCKYARDS (Madras/Vizag yards, consumer-goods efficiency).
- **RJP Rajputana** — Marwari finance + desert martial + Bikaner/Jaipur. ~24.
  Specialty: FINANCE & CAVALRY (Marwari trade network → PP/civ economy; camel/cav corps).
- **WIS Gujarat** — merchant princes, Ahmedabad calico, diamonds, Kathiawar ports. ~26.
  Specialty: TRADE & TEXTILES (dhow trade, diamond cutting, Baroda model state).

### Tier 4 — Resource/port specialists (Bulgaria/Greece-class, 14-20)
- **TRV Travancore** — spices, rare-earth monazite, Cochin port, high literacy. ~18.
  Specialty: RARE EARTHS & TRADE (monazite/thorium — unique late-game research edge).
- **SIN Sindh** — Karachi port + Indus + oil frontier. ~16.
  Specialty: OIL & SHIPPING (Karachi docks, Attock/Sindh oil, convoy economy).
- **ORI Orissa** — mineral belt: iron, chromite, bauxite (Sukinda). ~18.
  Specialty: ORE EXPORT (raw resources → sells to industrial tiers).
- **ASM Assam** — Digboi oil + Assam tea + Arunachal tungsten. ~16.
  Specialty: OIL & STRATEGIC RESOURCES (Digboi — India's real oil; tungsten).

### Tier 5 — Frontier/small (10-14)
- **KAS Kashmir** — Himalayan, shawls/tourism, defensive. ~12. Specialty: DEFENSE & CRAFT.
- **MPU Manipur** — hill kingdom, small but strategic gateway to Burma. ~10.
  Specialty: BORDER/JUNGLE INFANTRY.

## Resource identity (per specialty, scaled to be meaningful not absurd)
- MAR: steel, tungsten, chromium (arsenal feedstock) — highest steel.
- BEN: steel + coal-proxy(steel) + rubber (jute abstracted to consumer eff).
- HYD: chromium, tungsten, aluminium, + hidden "gold" via PP spirit.
- ORI: steel (iron), chromium (chromite), aluminium (bauxite) — top raw exporter.
- ASM: oil (Digboi) top-3 in map, tungsten, rubber.
- SIN: oil (Attock), steel.
- TRV: aluminium (monazite/rare-earth proxy), rubber, tungsten — unique.
- WIS: oil (Kathiawar), steel, + trade spirit.
- MYS: chromium, tungsten, steel, aluminium (already resource-rich, keep).
- MDR: rubber, chromium, steel.
- PJB/HIN/RJP: modest steel/chromium — these are manpower/agri economies.

## Manpower model (subtly higher, uncapped)
- Keep large real populations. Conscription law by tier:
  - Manpower-economy tags (HIN, PJB, MAR): limited_conscription (2.5%).
  - Martial/regional (RJP, MYS, HYD, MDR, BEN): limited_conscription (2.5%).
  - Small/frontier (KAS, MPU, ASM, ORI, SIN, TRV, WIS): extensive (5%) — need edge.
- Add per-nation recruitable_population_factor via national spirit:
  - PJB "Martial Races of Punjab": +0.02 recruitable, +army org.
  - HIN "Gangetic Multitudes": +0.03 recruitable (huge pop, low ind.).
  - RJP "Rajput Warrior Caste": +0.02 recruitable, +div attack.
  - MAR "Maratha Levy Tradition": +0.015 recruitable.
  - Others: +0.01 flavor where fitting.
- Net effect: subtle uplift (recruitable 1.5%→~3.5-5.5% effective), never a hard cap.

## Late-game 5-6x scaling (disciplined route rewards; trap routes stall)
Each major focus tree gets an "industrialization spine" mirroring GER pattern:
- Good route: add_research_slot (x1-2), stacked production_speed + industrial_capacity
  spirits (swap_ideas upgrading a "Five-Year Plan" spirit through 3 tiers), and
  add_building_construction of civ factories. Reaches ~5-6x base by 1943.
- Trap route: quick add_political_power / short-term army buffs that lock a
  "Complacent Court" or "Rentier Economy" spirit imposing industrial_capacity_factory
  penalty — visibly tempting, strategically crippling.
- Prerequisites: every tech head-start gated by has_dlc where MtG/BBA modules are used;
  every enable-module tech present before variants (already fixed in hull pass).

## AI (smart starts, no OP without prereqs)
- ai_strategy per nation: industrial tags prioritize construction+research; martial tags
  prioritize army; coastal specialists build navy/convoys.
- ai_will_do on focus branch-points gated by date/flags so AI follows historical-plausible
  route, doesn't rush trap or end-game focuses early.
- No nation starts with equipment/variants its tech can't support (audit in verify phase).

## Faction / Game-of-Thrones layer (later wave)
- Diplomatic hooks: Mandala event chain (exists) extended so any tag can league up,
  join world factions (Allies/Axis/Comintern), or pursue Akhand Bharat unification.
- Decisions for: colonize/influence (Indian Ocean, SE Asia, E Africa), foreign-war
  intervention, subterfuge (fund revolts in rival Indian states).

## Non-negotiables
- NEVER reduce a nation below its current total in a way that breaks its OOB supply.
- Shared-building slots must always fit local category + extras.
- Every referenced idea/spirit/loc key defined; MCP-validate before sync.
