#!/usr/bin/env python3
"""Build deterministic 2x2 portrait prompts from manifest.json."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parent
DEFAULT_MANIFEST = PIPELINE_DIR / "manifest.json"
QUADRANTS = ("Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right")


def load_manifest(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    portraits = data.get("portraits")
    if not isinstance(portraits, list) or not portraits:
        raise ValueError("manifest must contain a non-empty portraits list")
    required = {"character", "country", "stem", "description"}
    seen_characters: set[str] = set()
    seen_stems: set[str] = set()
    for index, portrait in enumerate(portraits, 1):
        missing = required.difference(portrait)
        if missing:
            raise ValueError(f"portrait {index} missing: {', '.join(sorted(missing))}")
        character = portrait["character"]
        stem = portrait["stem"]
        if character in seen_characters:
            raise ValueError(f"duplicate character: {character}")
        if stem in seen_stems:
            raise ValueError(f"duplicate stem: {stem}")
        seen_characters.add(character)
        seen_stems.add(stem)
    return data


def build_prompts(manifest: dict) -> list[str]:
    style = manifest["style"].strip()
    portraits = manifest["portraits"]
    prompts: list[str] = []
    for start in range(0, len(portraits), 4):
        chunk = portraits[start : start + 4]
        while len(chunk) < 4:
            chunk.append(chunk[-1])
        descriptions = "\n".join(
            f"{QUADRANTS[index]} (Quadrant {index + 1}): {portrait['description']}."
            for index, portrait in enumerate(chunk)
        )
        prompts.append(
            "Generate ONE high-resolution image as a strict 2x2 grid with four equal quadrants, "
            "thin neutral divider lines, and no outer border. All quadrants must use the exact same "
            f"art direction: {style}. No text, watermark, labels, numbers, signatures, or frames. "
            "Each quadrant is one distinct centered shoulders-up portrait at eye level.\n"
            f"{descriptions}\n"
            "Keep palette, scale, lighting, brushwork, background, and canvas grain consistent."
        )
    return prompts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--check", action="store_true", help="validate without writing prompt files")
    args = parser.parse_args()

    manifest = load_manifest(args.manifest.resolve())
    prompts = build_prompts(manifest)
    if args.check:
        print(f"valid: {len(manifest['portraits'])} portraits, {len(prompts)} grids")
        return

    (PIPELINE_DIR / "prompts.txt").write_text(
        "\n".join(prompt.replace("\n", " ") for prompt in prompts) + "\n",
        encoding="utf-8",
    )
    pretty = "".join(
        f"=== PROMPT {index:02d} / {len(prompts)} ===\n{prompt}\n\n"
        for index, prompt in enumerate(prompts, 1)
    )
    (PIPELINE_DIR / "prompts_pretty.txt").write_text(pretty, encoding="utf-8")
    print(f"wrote {len(prompts)} prompts for {len(manifest['portraits'])} portraits")


if __name__ == "__main__":
    main()
