#!/usr/bin/env python3
"""Convert manifest-driven portrait grids into validated HOI4 assets."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from PIL import Image

PIPELINE_DIR = Path(__file__).resolve().parent
MOD_ROOT = PIPELINE_DIR.parents[1]
QUADRANTS = ("top_left", "top_right", "bottom_left", "bottom_right")
LARGE_SIZE = (156, 210)
SMALL_SIZE = (65, 67)


def load_manifest(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    portraits = data.get("portraits")
    if not portraits:
        raise ValueError("manifest has no portraits")
    required = {"character", "country", "stem", "description"}
    for index, portrait in enumerate(portraits, 1):
        missing = required.difference(portrait)
        if missing:
            raise ValueError(f"portrait {index} missing {', '.join(sorted(missing))}")
    return data


def crop_and_resize(image: Image.Image, target: tuple[int, int]) -> Image.Image:
    image = image.convert("RGBA")
    width, height = image.size
    target_aspect = target[0] / target[1]
    source_aspect = width / height
    if source_aspect > target_aspect:
        crop_width = round(height * target_aspect)
        left = (width - crop_width) // 2
        image = image.crop((left, 0, left + crop_width, height))
    else:
        crop_height = round(width / target_aspect)
        top = (height - crop_height) // 2
        image = image.crop((0, top, width, top + crop_height))
    return image.resize(target, Image.Resampling.LANCZOS)


def atomic_save(image: Image.Image, destination: Path, image_format: str) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    suffix = destination.suffix or ".tmp"
    with NamedTemporaryFile(dir=destination.parent, suffix=suffix, delete=False) as handle:
        temporary = Path(handle.name)
    try:
        save_args = {"format": image_format}
        if image_format == "PNG":
            save_args["optimize"] = True
        image.save(temporary, **save_args)
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def save_portrait(image: Image.Image, root: Path, country: str, stem: str) -> None:
    output = root / "gfx" / "leaders" / country
    large = crop_and_resize(image, LARGE_SIZE)
    small = large.resize(SMALL_SIZE, Image.Resampling.LANCZOS)
    for current, name in ((large, stem), (small, f"{stem}_small")):
        atomic_save(current, output / f"{name}.png", "PNG")
        atomic_save(current, output / f"{name}.dds", "DDS")


def write_gfx(root: Path, country: str, portraits: list[dict]) -> Path:
    lines = ["spriteTypes = {"]
    for portrait in portraits:
        stem = portrait["stem"]
        for suffix in ("", "_small"):
            lines.extend(
                (
                    "\tspriteType = {",
                    f'\t\tname = "GFX_{stem}{suffix}"',
                    f'\t\ttexturefile = "gfx/leaders/{country}/{stem}{suffix}.dds"',
                    "\t}",
                )
            )
    lines.append("}")
    destination = root / "interface" / f"{country}_portraits.gfx"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return destination


def validate_output(root: Path, manifest: dict) -> list[str]:
    required_portraits = manifest["portraits"][: manifest.get("required_count", len(manifest["portraits"]))]

    errors: list[str] = []
    for portrait in required_portraits:
        country = portrait["country"]
        stem = portrait["stem"]
        for suffix, expected in (("", LARGE_SIZE), ("_small", SMALL_SIZE)):
            for extension in ("dds", "png"):
                path = root / "gfx" / "leaders" / country / f"{stem}{suffix}.{extension}"
                if not path.exists():
                    errors.append(f"missing {path.relative_to(root)}")
                    continue
                try:
                    with Image.open(path) as image:
                        if image.size != expected:
                            errors.append(f"{path.relative_to(root)} is {image.size}, expected {expected}")
                except OSError as error:
                    errors.append(f"unreadable {path.relative_to(root)}: {error}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=PIPELINE_DIR / "manifest.json")
    parser.add_argument("--generated", type=Path, default=PIPELINE_DIR / "generated")
    parser.add_argument("--mod-root", type=Path, default=MOD_ROOT)
    parser.add_argument("--live-root", type=Path, help="optional second output root; normally use sync.ps1")
    parser.add_argument("--check", action="store_true", help="validate current assets without converting")
    parser.add_argument("--allow-missing", action="store_true", help="convert available inputs instead of failing")
    args = parser.parse_args()

    manifest = load_manifest(args.manifest.resolve())
    roots = [args.mod_root.resolve()]
    if args.live_root:
        roots.append(args.live_root.resolve())

    if args.check:
        errors = [error for root in roots for error in validate_output(root, manifest)]
        if errors:
            raise SystemExit("\n".join(errors))
        required_count = manifest.get("required_count", len(manifest["portraits"]))
        print(f"valid: {required_count} required portraits across {len(roots)} output root(s)")
        return

    missing: list[Path] = []
    converted: list[dict] = []
    for index, portrait in enumerate(manifest["portraits"]):
        grid = index // 4 + 1
        quadrant = QUADRANTS[index % 4]
        source = args.generated.resolve() / f"grid_{grid:02d}" / f"{quadrant}.png"
        if not source.exists():
            missing.append(source)
            continue
        with Image.open(source) as image:
            if image.width < 256 or image.height < 256:
                raise ValueError(f"source too small: {source} is {image.size}")
            for root in roots:
                save_portrait(image, root, portrait["country"], portrait["stem"])
        converted.append(portrait)

    if missing and not args.allow_missing:
        relative = "\n".join(str(path.relative_to(PIPELINE_DIR)) for path in missing)
        raise SystemExit(f"missing generated quadrants:\n{relative}")

    countries = sorted({portrait["country"] for portrait in converted})
    for root in roots:
        for country in countries:
            write_gfx(root, country, [p for p in converted if p["country"] == country])

    errors = [error for root in roots for error in validate_output(root, {"portraits": converted})]
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"converted and validated {len(converted)} portraits")
    if missing:
        print(f"skipped {len(missing)} missing sources")


if __name__ == "__main__":
    main()
