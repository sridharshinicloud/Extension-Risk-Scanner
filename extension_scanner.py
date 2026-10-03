"""Extension Risk Scanner

Reads the manifest.json of Chrome extensions, scores them for risky
permissions, and prints them from highest to lowest risk.
"""

import argparse
import json
import os
import pathlib
import sys

# Permission -> risk points. Tweak these to suit your own risk tolerance.
RISKY = {
    "<all_urls>": 25,
    "debugger": 30,
    "webRequestBlocking": 25,
    "cookies": 15,
    "history": 15,
    "nativeMessaging": 20,
    "management": 15,
}


def score_extension(ext_dir):
    """Score ONE extension folder. Returns (name, score, findings)."""
    manifest_file = pathlib.Path(ext_dir) / "manifest.json"
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))

    perms = set(manifest.get("permissions", [])) | set(manifest.get("host_permissions", []))
    findings = [(p, w) for p, w in RISKY.items() if p in perms]

    if manifest.get("manifest_version") == 2:
        findings.append(("Manifest V2 (legacy)", 10))

    score = min(100, sum(w for _, w in findings))
    return manifest.get("name", "?"), score, findings


def default_extensions_dir():
    """Default Chrome extensions folder for the current operating system."""
    home = pathlib.Path.home()
    if sys.platform.startswith("win"):
        return pathlib.Path(os.environ["LOCALAPPDATA"]) / "Google" / "Chrome" / "User Data" / "Default" / "Extensions"
    if sys.platform == "darwin":
        return home / "Library" / "Application Support" / "Google" / "Chrome" / "Default" / "Extensions"
    return home / ".config" / "google-chrome" / "Default" / "Extensions"


def main():
    parser = argparse.ArgumentParser(description="Scan Chrome extensions for risky permissions.")
    parser.add_argument("path", nargs="?", help="Folder containing extensions (optional)")
    args = parser.parse_args()

    base = pathlib.Path(args.path) if args.path else default_extensions_dir()
    print("Scanning:", base)

    if not base.exists():
        print("That folder doesn't exist. Check the path above.")
        return

    results = []
    # Installed extensions look like: <extension id>/<version>/manifest.json
    for manifest_path in base.glob("*/*/manifest.json"):
        try:
            results.append(score_extension(manifest_path.parent))
        except (json.JSONDecodeError, OSError):
            print(f"Skipped unreadable manifest: {manifest_path}")

    if not results:
        print("No extensions found.")
        return

    results.sort(key=lambda r: r[1], reverse=True)

    for name, score, findings in results:
        print(f"{name}: {score}/100")
        for reason, points in findings:
            print(f"  - {reason} (+{points})")


if __name__ == "__main__":
    main()
