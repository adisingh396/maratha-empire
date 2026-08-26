#!/usr/bin/env python3
"""
Build 1 grid prompt (4 portraits) for Maratha Empire HOI4 — mimics vedic_lore build_prompts.py
Generates strict 2x2 grid with shared painterly military portrait style.
"""
STYLE = (
    "high-quality hand-painted grand-strategy military portrait, matching classic WWII-era strategy game character portraits. "
    "Semi-realistic traditional painting aesthetic with realistic facial anatomy, strong likeness, detailed eyes, natural skin texture, subtle wrinkles, carefully painted hair, and controlled painterly brushwork. "
    "Face highly detailed and recognizable while retaining slightly stylized illustrated appearance. "
    "Soft directional studio lighting, gentle shadows across the face, subtle highlights, strong three-dimensional depth without cinematic or photographic look. "
    "Muted historical color palette: olive green, military gray, faded brown, beige, cream, subdued blue, restrained gold accents. Avoid saturated modern colors. "
    "Clothing and accessories with fine painted detail, realistic fabric folds, stitching, buttons, metallic elements, medals, insignia, military uniform textures, physically painted not digitally rendered. "
    "Simple warm beige/gray painted background with subtle parchment/canvas grain, faint tonal variation, soft vignette, extremely understated face remains focal point. "
    "Overall resembles professionally commissioned 1930s-1940s military portrait illustration: realistic but painterly, slightly aged, restrained, authoritative, highly detailed, visually consistent across collection. "
    "AVOID: photorealism, CGI, 3D rendering, anime, cartoon, comic-book style, glossy digital art, plastic skin, excessive sharpening, neon colors, modern photography, cinematic lighting, dramatic backgrounds, excessive saturation, fantasy elements, overly stylized facial features"
)

# 4 leaders with far more description than just names
quadrants = [
    "Chhatrapati Shivaji Maharaj, age 45, majestic mature Maratha king, full black beard with subtle silver, long wavy hair under saffron turban with white pearl string and small gold kalgi, intense dark brown eyes with wisdom lines, olive skin, wearing Jagdamba steel chest armor over deep olive green angarkha with gold braid, shoulder chainmail visible, holding ornate curved sword hilt, authoritative calm expression, soft beige parchment background",
    "Peshwa Baji Rao I, age 30, lean youthful warrior Peshwa, sharp thin mustache, long hair tied, distinctive red Peshwai pagdi with gold border and white feather plume, sharp nose, light wheatish skin, wearing Maratha Peshwai military coat in faded olive brown with brass buttons, gold sash, pearl necklace, stern focused gaze, same beige background, painterly fabric folds",
    "Maharani Tarabai, age 38, fierce Maratha queen regent, sharp features, large dark eyes with kohl, red bindi, wheatish skin, long black hair under translucent red saree pallu with gold zari border draped as military shawl, wearing emerald necklace and nath, cream blouse, holding dagger sheath, dignified commanding expression, subtle wrinkles, same muted background",
    "Peshwa Madhavrao III (fictional 1936 modernized), age 32, clean-shaven sharp jawline, short neatly combed black hair, light olive skin, wearing khaki British-Maratha hybrid military uniform with saffron sash, brass buttons, Maratha sun insignia, service ribbons and small medals, high collar, modern peaked cap with Maratha crest held under arm, confident forward-looking expression, same beige canvas background"
]

prompts = []
for i in range(0, len(quadrants), 4):
    chunk = quadrants[i:i+4]
    while len(chunk) < 4:
        chunk.append(chunk[-1])
    quadrant_text = ""
    for idx, q in enumerate(chunk):
        label = ["Top-Left (Quadrant 1)", "Top-Right (Quadrant 2)", "Bottom-Left (Quadrant 3)", "Bottom-Right (Quadrant 4)"][idx]
        quadrant_text += f"{label}: {q}.\n"
    full_prompt = (
        f"Generate ONE high-resolution image as a strict 2x2 grid (four equal quadrants, subtle thin beige divider lines, no outer border). "
        f"CRITICAL: All four quadrants share EXACT same consistent art style: {STYLE}. "
        f"ABSOLUTELY NO text, no watermark, no labels, no numbers in image. "
        f"Each quadrant is a distinct portrait, stylistically identical, cinematic quality, 8K detailed, centered bust, shoulders up, eye-level:\n"
        f"{quadrant_text}\n"
        f"Ensure cross-quadrant consistency: identical color palette, brushwork, lighting, atmospheric haze, canvas grain and ornamental detail. "
        f"Grand strategy 1930s military portrait series, historically grounded, no fantasy, no photorealism."
    )
    prompts.append(full_prompt)

print(f"Total quadrants: {len(quadrants)}")
print(f"Total grid prompts: {len(prompts)}")

with open("prompts.txt", "w", encoding="utf-8") as f:
    for p in prompts:
        single_line = p.replace("\n", " ").strip()
        f.write(single_line + "\n")

with open("prompts_pretty.txt", "w", encoding="utf-8") as f:
    for idx, p in enumerate(prompts, 1):
        f.write(f"=== PROMPT {idx:02d} / {len(prompts)} ===\n")
        f.write(p + "\n\n")

print(f"Wrote prompts.txt ({len(prompts)} grids)")
