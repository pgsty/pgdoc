#!/usr/bin/env python3
"""Fetch the PG 18.6 generator inputs from the official postgres git.

Downloads into tools/pgsrc/ the handful of source files the documentation
generators need but the frozen doc-only trees do not carry.  Idempotent:
skips files that already exist.
"""

from pathlib import Path
import urllib.request

BASE = "https://raw.githubusercontent.com/postgres/postgres/REL_18_6"
HERE = Path(__file__).resolve().parent
OUT = HERE / "pgsrc"

FILES = {
    "errcodes.txt": "src/backend/utils/errcodes.txt",
    "kwlist.h": "src/include/parser/kwlist.h",
    "wait_event_names.txt": "src/backend/utils/activity/wait_event_names.txt",
    "generate-wait_event_types.pl":
        "src/backend/utils/activity/generate-wait_event_types.pl",
    "sql_feature_packages.txt": "src/backend/catalog/sql_feature_packages.txt",
    "sql_features.txt": "src/backend/catalog/sql_features.txt",
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, path in FILES.items():
        dst = OUT / name
        if dst.exists() and dst.stat().st_size > 0:
            print(f"  have {name}")
            continue
        url = f"{BASE}/{path}"
        print(f"  fetch {name} <- {url}")
        with urllib.request.urlopen(url, timeout=60) as r:
            dst.write_bytes(r.read())
    print("pgsrc ready.")


if __name__ == "__main__":
    main()
