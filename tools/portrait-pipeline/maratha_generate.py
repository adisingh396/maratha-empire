#!/usr/bin/env python3
"""
Vedic Image Generator - text-only Gemini generation, 50 grids -> 200 quadrants.
Uses gemini_webapi to interact with Gemini web UI via cookies.
No reference images needed - prompts describe everything.
"""
# StrEnum backport for Python 3.10 (gemini_webapi needs it)
import enum
if not hasattr(enum, "StrEnum"):
    class StrEnum(str, enum.Enum):
        def __new__(cls, value, *args, **kwargs):
            obj = str.__new__(cls, value)
            obj._value_ = value
            return obj
    enum.StrEnum = StrEnum

import asyncio
import json
import sys
import time
from pathlib import Path

# Suppress gemini_webapi verbose logging to stderr
try:
    from gemini_webapi import set_log_level
    set_log_level("ERROR")
except ImportError:
    pass

PIPELINE_DIR = Path(__file__).parent
GEN_DIR = PIPELINE_DIR / "generated"
PROMPTS_FILE = PIPELINE_DIR / "prompts.txt"
PROGRESS_FILE = GEN_DIR / "progress.json"
COOKIES_FILE = PIPELINE_DIR / "cookies.json"

RATE_LIMIT_DELAY = 18  # seconds between requests
MAX_RETRIES = 3


def load_prompts():
    lines = [l.strip() for l in PROMPTS_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
    return lines


def load_cookies():
    data = json.loads(COOKIES_FILE.read_text(encoding="utf-8-sig"))
    cookie_dict = {}
    if isinstance(data, list):
        for c in data:
            n, v = c.get("name"), c.get("value")
            if n and v:
                cookie_dict[n] = v
    elif isinstance(data, dict):
        cookie_dict = data
    psid = cookie_dict.get("__Secure-1PSID")
    psidts = cookie_dict.get("__Secure-1PSIDTS")
    if not psid:
        raise ValueError("__Secure-1PSID missing")
    return psid, psidts, cookie_dict


def load_progress():
    GEN_DIR.mkdir(parents=True, exist_ok=True)
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    return {"completed": [], "failed": []}


def save_progress(p):
    PROGRESS_FILE.write_text(json.dumps(p, indent=2), encoding="utf-8")


def split_grid_pil(img_path: Path, out_dir: Path):
    """Split a 2x2 grid image into 4 quadrants using PIL (no cv2 needed)."""
    from PIL import Image
    im = Image.open(img_path)
    w, h = im.size
    cx, cy = w // 2, h // 2
    quads = {
        "top_left": im.crop((0, 0, cx, cy)),
        "top_right": im.crop((cx, 0, w, cy)),
        "bottom_left": im.crop((0, cy, cx, h)),
        "bottom_right": im.crop((cx, cy, w, h)),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    saved = []
    for k in ["top_left", "top_right", "bottom_left", "bottom_right"]:
        p = out_dir / f"{k}.png"
        quads[k].save(p)
        saved.append(p)
        print(f"  [split] {p.relative_to(PIPELINE_DIR)}")
    return saved


async def generate_one_grid(idx: int, prompt: str, cookies_tuple, progress):
    """Generate one 2x2 grid image via Gemini and split into 4 quadrants."""
    grid_key = f"grid_{idx:02d}"
    if grid_key in progress["completed"]:
        print(f"  [{idx:02d}/50] {grid_key} already done - skip")
        return True

    out_dir = GEN_DIR / grid_key
    out_dir.mkdir(parents=True, exist_ok=True)
    grid_path = out_dir / "grid.png"

    # If grid already exists, just split
    if grid_path.exists():
        quad_files = [out_dir / f"{k}.png" for k in ["top_left", "top_right", "bottom_left", "bottom_right"]]
        if all(p.exists() for p in quad_files):
            print(f"  [{idx:02d}/50] {grid_key} already split - skip")
            if grid_key not in progress["completed"]:
                progress["completed"].append(grid_key)
                save_progress(progress)
            return True

    print(f"\n{'='*60}")
    print(f"[{idx:02d}/50] Generating {grid_key}")
    print(f"{'='*60}")
    print(f"  Prompt: {prompt[:120]}...")

    # Import gemini_webapi (StrEnum patched at top of file)
    try:
        from gemini_webapi import GeminiClient
        from gemini_webapi.constants import Model
    except ImportError as e:
        print(f"  [ERROR] gemini_webapi not installed: {e}")
        print(f"  Install: pip install gemini-webapi")
        return False

    psid, psidts, cookie_dict = cookies_tuple
    client = GeminiClient(secure_1psid=psid, secure_1psidts=psidts)
    client.cookies = cookie_dict

    try:
        print("  [auth] Connecting to Gemini...")
        await client.init(timeout=180)
    except Exception as e:
        print(f"  [ERROR] Auth failed: {e}")
        await client.close()
        return False

    try:
        for attempt in range(MAX_RETRIES):
            try:
                chat = client.start_chat(model=Model.BASIC_FLASH)
                # Text-only: no files, just the prompt describing the 2x2 grid
                response = await chat.send_message(prompt)

                if not response.images:
                    text_resp = response.text[:300] if response.text else "empty"
                    print(f"  [warn] No images returned. Response: {text_resp}")
                    # Some responses need follow-up
                    if attempt == 0:
                        print("  [retry] Trying with explicit image request...")
                        await asyncio.sleep(5)
                        continue
                    return False

                # Save the grid image (not full_size to avoid RPC timeout)
                from gemini_webapi.types.image import GeneratedImage
                for img in response.images:
                    if isinstance(img, GeneratedImage):
                        saved = await img.save(path=str(out_dir), full_size=False, verbose=False)
                    else:
                        saved = await img.save(path=str(out_dir), verbose=False)
                    saved_path = Path(saved)
                    # Rename to grid.png if needed
                    if saved_path.name != "grid.png":
                        saved_path.rename(grid_path)
                    print(f"  [saved] {grid_path.name}")
                    break

                # Split into quadrants
                if grid_path.exists():
                    split_grid_pil(grid_path, out_dir)
                    progress["completed"].append(grid_key)
                    save_progress(progress)
                    print(f"  [done] {grid_key} complete")
                    return True
                else:
                    print(f"  [error] Grid not saved")
                    return False

            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "rate" in err_str.lower():
                    wait = RATE_LIMIT_DELAY * (attempt + 1)
                    print(f"  [rate-limit] Waiting {wait}s (attempt {attempt+1}/{MAX_RETRIES})...")
                    await asyncio.sleep(wait)
                    continue
                print(f"  [ERROR] {e}")
                return False

        print(f"  [failed] Rate limited after {MAX_RETRIES} retries")
        progress["failed"].append(grid_key)
        save_progress(progress)
        return False

    finally:
        try:
            await client.close()
        except Exception:
            pass


async def main():
    import argparse
    parser = argparse.ArgumentParser(description="Vedic 200-image generator (50 grids x4)")
    parser.add_argument("--limit", type=int, default=0, help="Only generate first N grids")
    parser.add_argument("--dry-run", action="store_true", help="Print prompts without generating")
    args = parser.parse_args()

    prompts = load_prompts()
    total = len(prompts)
    print(f"Loaded {total} grid prompts -> {total * 4} quadrant images")
    print(f"Output: {GEN_DIR}")

    if args.limit and args.limit > 0:
        prompts = prompts[:args.limit]
        print(f"Limited to first {len(prompts)} grids")

    if args.dry_run:
        for i, p in enumerate(prompts, 1):
            print(f"\n--- Prompt {i:02d} ---")
            print(p[:300])
        return

    cookies_tuple = load_cookies()
    print(f"[auth] Cookies loaded")

    progress = load_progress()
    progress_before = set(progress["completed"])
    print(f"[progress] completed={len(progress['completed'])} failed={len(progress['failed'])}")

    for idx, prompt in enumerate(prompts, 1):
        success = await generate_one_grid(idx, prompt, cookies_tuple, progress)
        if not success:
            print(f"\n[warn] Grid {idx} failed, continuing...")

        # Rate limit only between actual API requests, not skips
        if idx < len(prompts) and success and f"grid_{idx:02d}" not in progress_before:
            print(f"  [sleep] {RATE_LIMIT_DELAY}s before next request...")
            await asyncio.sleep(RATE_LIMIT_DELAY)

    completed = len(progress["completed"])
    failed = len(progress["failed"])
    print(f"\n{'='*60}")
    print(f"Done! Completed {completed}/{total} grids = {completed * 4} images")
    if failed:
        print(f"Failed: {failed} grids")
    print(f"{'='*60}")
    print(f"\nNext: run build_slideshow.py to generate the HTML/MP4")


if __name__ == "__main__":
    asyncio.run(main())
