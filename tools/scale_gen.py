# Mass-generation helpers for 10x scale wave. Every token below is game-verified
# (vanilla shapes + mod error.log). Run via `import scale_gen`.
import re

ICON_POOL = [
    "GFX_goal_generic_major_war", "GFX_goal_generic_production",
    "GFX_goal_generic_construct_civ_factory", "GFX_goal_generic_construct_mil_factory",
    "GFX_goal_generic_allies_build_infantry", "GFX_goal_generic_artillery",
    "GFX_goal_generic_cavalry", "GFX_goal_generic_armor",
    "GFX_goal_generic_air_fighter2", "GFX_goal_generic_navy_cruiser",
    "GFX_goal_generic_navy_destroyer", "GFX_goal_generic_navy_battleship",
    "GFX_goal_generic_construct_naval_dockyard", "GFX_goal_generic_alliance",
    "GFX_goal_generic_political_pressure", "GFX_goal_generic_national_unity",
    "GFX_goal_generic_propaganda", "GFX_goal_generic_trade",
    "GFX_goal_generic_scientific_exchange", "GFX_goal_generic_manpower",
    "GFX_goal_generic_construct_infrastructure", "GFX_goal_generic_oil_refinery",
    "GFX_goal_generic_territory_or_war", "GFX_goal_generic_more_territorial_claims",
]
TECH_POOL = ["infantry_weapons", "armor", "artillery", "naval_equipment",
             "air_equipment", "industry", "electronics", "land_doctrine"]
TRAITS_G = ["aggressive_assaulter", "superior_tactician", "artillery_expert",
            "trickster", "cavalry_expert", "defensive_doctrine"]
TRAITS_A = ["political_operator", "military_theorist", "army_offensive_trait",
            "army_defensive_trait", "political_operator", "military_theorist"]
IDEA_MODS = [
    "political_power_gain = 0.10", "stability_factor = 0.05",
    "war_support_factor = 0.08", "army_core_attack_factor = 0.05",
    "army_core_defence_factor = 0.05", "army_attack_factor = 0.05",
    "army_speed_factor = 0.03", "industrial_capacity_factory = 0.05",
    "production_speed_buildings_factor = 0.10",
    "production_speed_industrial_complex_factor = 0.10",
    "production_speed_arms_factory_factor = 0.10",
    "production_speed_infrastructure_factor = 0.10",
    "production_factory_max_efficiency_factor = 0.08",
    "supply_consumption_factor = -0.05", "conscription_factor = 0.10",
    "navy_org_factor = 0.08", "political_power_factor = 0.10",
    "justify_war_goal_time = -0.10", "drift_defence_factor = 0.15",
    "trade_opinion_factor = 0.10", "resistance_growth = -0.10",
    "consumer_goods_factor = -0.03", "fuel_gain_factor = 0.15",
    "research_speed_land_doctrine_factor = 0.10",
]
GEN_NAMES = (["Amit", "Vikram", "Ravi", "Suresh", "Anand", "Prakash", "Mohan",
              "Kiran", "Deepak", "Arjun", "Sanjay", "Rajesh", "Vijay", "Ashok"],
             ["Lakshmi", "Meera", "Priya", "Kavita"],
             ["Rao", "Reddy", "Nair", "Menon", "Iyer", "Sharma", "Verma",
              "Patel", "Das", "Sen", "Khan", "Singh"])

# tag: states, coast, gfx portraits, anchor focus (None = new tree), ystart, flavor
STATES = {
 "MAR": dict(states=[429, 983], coast=True, gfx=("GFX_portrait_mar_bajirao", "GFX_portrait_mar_bajirao_small"), anchor="MAR_legacy_of_the_peshwas", ystart=15, file="common/national_focus/maratha_focus.txt", branches=["saffron_host", "deccan_admin"]),
 "HYD": dict(states=[427], coast=False, gfx=("GFX_portrait_hyd_nizam", "GFX_portrait_hyd_nizam_small"), anchor="HYD_world_empire", ystart=16, file="common/national_focus/HYD_focus.txt", branches=["nizam_durbar", "godavari_plan", "deccan_host", "hyderabad_caliphate", "nizam_navy"]),
 "MYS": dict(states=[425], coast=False, gfx=("GFX_portrait_mys_wadiyar", "GFX_portrait_mys_wadiyar_small"), anchor="MYS_carnatic_empire", ystart=6, file="common/national_focus/MYS_focus.txt", branches=["wadiyar_durbar", "kaveri_plan", "mysore_host", "carnatic_crown"]),
 "RJP": dict(states=[433, 989, 991], coast=False, gfx=("GFX_portrait_rjp_ganga", "GFX_portrait_rjp_ganga_small"), anchor="RJP_rajput_empire", ystart=9, file="common/national_focus/RJP_focus.txt", branches=["clan_durbar", "thar_plan", "rajput_host", "delhi_crown"]),
 "HIN": dict(states=[438, 439, 435], coast=False, gfx=("GFX_portrait_hyd_nizam", "GFX_portrait_hyd_nizam_small"), anchor="HIN_ganga_empire", ystart=5, file="common/national_focus/HIN_focus.txt", branches=["awadh_durbar", "ganga_plan", "ganga_host", "delhi_crown"]),
 "PJB": dict(states=[440], coast=False, gfx=("GFX_portrait_rjp_ganga", "GFX_portrait_rjp_ganga_small"), anchor=None, ystart=0, file="common/national_focus/PJB_focus.txt", branches=["khalsa_durbar", "punjab_plan", "khalsa_host", "lahore_crown"]),
 "BAN": dict(states=[430, 431], coast=True, gfx=("GFX_portrait_hyd_nizam", "GFX_portrait_hyd_nizam_small"), anchor=None, ystart=0, file="common/national_focus/BAN_focus.txt", branches=["bengal_durbar", "delta_plan", "bengal_host", "gauda_crown"]),
 "MDR": dict(states=[423], coast=True, gfx=("GFX_portrait_mys_wadiyar", "GFX_portrait_mys_wadiyar_small"), anchor=None, ystart=0, file="common/national_focus/MDR_focus.txt", branches=["tamil_durbar", "kaveri_mills", "chola_host", "tamil_crown", "coromandel_fleet"]),
 "ORI": dict(states=[426], coast=True, gfx=("GFX_portrait_mys_wadiyar", "GFX_portrait_mys_wadiyar_small"), anchor=None, ystart=0, file="common/national_focus/ORI_focus.txt", branches=["kalinga_durbar", "mahanadi_plan", "kalinga_host"]),
 "ASM": dict(states=[432, 434], coast=False, gfx=("GFX_portrait_rjp_ganga", "GFX_portrait_rjp_ganga_small"), anchor=None, ystart=0, file="common/national_focus/ASM_focus.txt", branches=["assam_durbar", "brahmaputra_plan", "assam_host"]),
 "MPU": dict(states=[990], coast=False, gfx=("GFX_portrait_kas_harisingh", "GFX_portrait_kas_harisingh_small"), anchor=None, ystart=0, file="common/national_focus/MPU_focus.txt", branches=["manipur_durbar", "loktak_plan", "manipur_host"]),
 "WIS": dict(states=[428], coast=True, gfx=("GFX_portrait_rjp_ganga", "GFX_portrait_rjp_ganga_small"), anchor="WIS_merchant_princes", ystart=5, file="common/national_focus/WIS_focus.txt", branches=["gujarat_durbar", "sabarmati_plan", "gujarat_host", "surat_crown"]),
 "SIN": dict(states=[443], coast=True, gfx=("GFX_portrait_hyd_nizam", "GFX_portrait_hyd_nizam_small"), anchor="SIN_baluchi_overture", ystart=5, file="common/national_focus/SIN_focus.txt", branches=["sindh_durbar", "indus_plan", "sindh_host", "sehwan_crown"]),
 "KAS": dict(states=[441], coast=False, gfx=("GFX_portrait_kas_harisingh", "GFX_portrait_kas_harisingh_small"), anchor="KAS_levy_organize", ystart=5, file="common/national_focus/KAS_focus.txt", branches=["kashmir_durbar", "jhelum_plan", "kashmir_host", "srinagar_crown"]),
 "PAK": dict(states=[442], coast=False, gfx=("GFX_portrait_rjp_ganga", "GFX_portrait_rjp_ganga_small"), anchor=None, ystart=0, file="common/national_focus/PAK_focus.txt", branches=["frontier_durbar", "khyber_plan", "frontier_host"]),
}

BRANCH_FILTER = {"durbar": "FOCUS_FILTER_POLITICAL", "plan": "FOCUS_FILTER_INDUSTRY",
                 "mills": "FOCUS_FILTER_INDUSTRY", "host": "FOCUS_FILTER_ARMY",
                 "crown": "FOCUS_FILTER_POLITICAL", "caliphate": "FOCUS_FILTER_POLITICAL",
                 "navy": "FOCUS_FILTER_NAVY", "fleet": "FOCUS_FILTER_NAVY"}


def bfilter(branch):
    for k, v in BRANCH_FILTER.items():
        if k in branch:
            return v
    return "FOCUS_FILTER_POLITICAL"


def focus_block(fid, icon, pre, x, y, filt, reward, ai=8, gated=False):
    ai_s = f"ai_will_do = {{ factor = {ai}"
    if gated:
        ai_s += " modifier = { factor = 0 date < 1939.6.1 }"
    ai_s += " }"
    pres = "\n".join(f"\t\tprerequisite = {{ focus = {p} }}" for p in pre)
    return (f"\tfocus = {{\n\t\tid = {fid}\n\t\ticon = {icon}\n{pres}\n"
            f"\t\tx = {x}\n\t\ty = {y}\n\t\tcost = 10\n\t\t{ai_s}\n"
            f"\t\tsearch_filters = {{ {filt} }}\n\t\tcompletion_reward = {{\n"
            f"\t\t\tlog = \"[GetLogRoot]: Focus Completed {fid}\"\n{reward}\n\t\t}}\n\t}}\n")


def append_tree(path, blocks):
    t = open(path, encoding="utf-8").read().rstrip()
    assert t.endswith("}"), path
    t = t[: t.rfind("}")]
    open(path, "w", encoding="utf-8").write(t + "".join(blocks) + "}\n")


def new_tree(path, tree_id, tag):
    t = (f"focus_tree = {{\n\tid = {tree_id}\n\tcountry = {{ factor = 0 "
         f"modifier = {{ add = 10 tag = {tag} }} }}\n\tdefault = no\n")
    open(path, "w", encoding="utf-8").write(t + "}\n")
