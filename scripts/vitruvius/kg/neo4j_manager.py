"""Neo4j lifecycle manager — download, start, stop, and health-check.

This module removes the manual Neo4j setup burden.  When
``kg_transition.neo4j_backend`` is enabled, ``run_kg_pipeline`` can
auto-ensure Neo4j is running before Phase 5.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import time
import zipfile
from pathlib import Path
from typing import Literal

from vitruvius.config import (
    get_kg_neo4j_password,
    get_kg_neo4j_uri,
    get_kg_neo4j_user,
    get_repo_root,
)

VENDOR_DIR_NAME = ".vendor"
NEO4J_VENDOR_DIR_NAME = "neo4j"
NEO4J_VERSION = "5.26.0"
NEO4J_DOWNLOAD_URL = (
    f"https://dist.neo4j.org/neo4j-community-{NEO4J_VERSION}-windows.zip"
)


def _vendor_dir() -> Path:
    return get_repo_root() / VENDOR_DIR_NAME / NEO4J_VENDOR_DIR_NAME


def _find_neo4j_home() -> Path | None:
    """Locate an extracted Neo4j Community installation."""
    vendor = _vendor_dir()
    if not vendor.exists():
        return None
    for child in vendor.iterdir():
        if child.is_dir() and child.name.startswith("neo4j-community"):
            return child
    return None


def _find_neo4j_bat() -> Path | None:
    home = _find_neo4j_home()
    if home is None:
        return None
    bat = home / "bin" / "neo4j.bat"
    return bat if bat.exists() else None


def _find_neo4j_admin_bat() -> Path | None:
    home = _find_neo4j_home()
    if home is None:
        return None
    bat = home / "bin" / "neo4j-admin.bat"
    return bat if bat.exists() else None


def is_neo4j_running() -> bool:
    """Check whether Neo4j responds on the configured Bolt port."""
    try:
        from .neo4j_client import Neo4jClient

        client = Neo4jClient(
            uri=get_kg_neo4j_uri(),
            user=get_kg_neo4j_user(),
            password=get_kg_neo4j_password(),
        )
        ok = client.verify_connectivity()
        client.close()
        return ok
    except Exception:
        return False


def download_neo4j() -> Path:
    """Download and extract Neo4j Community to the vendor directory.

    Returns the path to the extracted Neo4j home directory.
    """
    vendor = _vendor_dir()
    vendor.mkdir(parents=True, exist_ok=True)
    zip_path = vendor / "neo4j.zip"

    if not zip_path.exists():
        print(f"Downloading Neo4j Community {NEO4J_VERSION} ...")
        print(f"  URL: {NEO4J_DOWNLOAD_URL}")
        # Prefer curl (fast), fallback to PowerShell.
        curl = shutil.which("curl")
        if curl:
            subprocess.run(
                [curl, "-fSL", "-o", str(zip_path), NEO4J_DOWNLOAD_URL],
                check=True,
            )
        else:
            subprocess.run(
                [
                    "powershell",
                    "-Command",
                    f"Invoke-WebRequest -Uri '{NEO4J_DOWNLOAD_URL}' -OutFile '{zip_path}'",
                ],
                check=True,
            )
        print(f"  Saved: {zip_path}")

    existing = _find_neo4j_home()
    if existing:
        return existing

    print(f"Extracting {zip_path.name} ...")
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(vendor)
    home = _find_neo4j_home()
    if home is None:
        raise RuntimeError("Neo4j zip extracted but home directory not found")
    print(f"  Extracted: {home}")
    return home


def set_initial_password(password: str | None = None) -> None:
    """Set the Neo4j initial password (only works before first start)."""
    admin = _find_neo4j_admin_bat()
    if admin is None:
        raise RuntimeError("neo4j-admin.bat not found")
    pwd = password or get_kg_neo4j_password()
    subprocess.run(
        [str(admin), "dbms", "set-initial-password", pwd],
        check=True,
    )
    print(f"Initial password set to: {'*' * len(pwd)}")


def start_neo4j() -> subprocess.Popen:
    """Start Neo4j in console mode.

    Returns the Popen handle so the caller can wait or terminate.
    """
    bat = _find_neo4j_bat()
    if bat is None:
        raise RuntimeError("neo4j.bat not found")

    print(f"Starting Neo4j from {bat.parent.parent} ...")
    proc = subprocess.Popen(
        [str(bat), "console"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
    )
    return proc


def ensure_neo4j_running(
    *,
    wait_seconds: int = 60,
    auto_download: bool = True,
    auto_start: bool = True,
) -> bool:
    """Ensure Neo4j is running, downloading and/or starting if necessary.

    Returns True if Neo4j is reachable when the function returns.
    """
    if is_neo4j_running():
        print("Neo4j is already running.")
        return True

    if _find_neo4j_bat() is None:
        if not auto_download:
            print("Neo4j not found and auto_download=False.")
            return False
        download_neo4j()

    if not auto_start:
        print("Neo4j found but not running and auto_start=False.")
        return False

    # Set initial password before first start if needed.
    home = _find_neo4j_home()
    if home is not None:
        pw_set_marker = home / "data" / "dbms" / "auth.ini"
        if not pw_set_marker.exists():
            try:
                set_initial_password()
            except subprocess.CalledProcessError:
                # Password may already be set; ignore.
                pass

    proc = start_neo4j()

    print(f"Waiting up to {wait_seconds}s for Neo4j to become ready ...")
    for i in range(wait_seconds):
        time.sleep(1)
        if proc.poll() is not None:
            # Process exited early — print remaining output.
            remaining, _ = proc.communicate(timeout=5)
            if remaining:
                print(remaining)
            raise RuntimeError("Neo4j process exited unexpectedly")
        if i % 5 == 0 and is_neo4j_running():
            print("Neo4j is ready.")
            return True

    if is_neo4j_running():
        print("Neo4j is ready.")
        return True

    print("Neo4j did not become ready in time.")
    return False


def stop_neo4j() -> None:
    """Stop a locally-managed Neo4j instance."""
    bat = _find_neo4j_bat()
    if bat is None:
        return
    try:
        subprocess.run([str(bat), "stop"], check=False, timeout=30)
        print("Neo4j stopped.")
    except Exception as exc:
        print(f"Warning: error stopping Neo4j: {exc}")
