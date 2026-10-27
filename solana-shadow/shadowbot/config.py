import os
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = ROOT / "data" / "shadow.db"
SAMPLES_DIR = ROOT / "samples"
REPORTS_DIR = ROOT / "reports"

WSOL_MINT = "So11111111111111111111111111111111111111112"


def load_env(path: Path | None = None) -> None:
    """Minimal .env reader. Existing environment variables win."""
    path = path or ROOT / ".env"
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and value and key not in os.environ:
            os.environ[key] = value


def load_thresholds(path: Path | None = None) -> dict:
    with open(path or ROOT / "thresholds.toml", "rb") as f:
        return tomllib.load(f)


def rpc_url() -> str | None:
    """Full RPC URL, or None if nothing is configured. The URL may contain a secret: never log it."""
    explicit = os.environ.get("SOLANA_RPC_URL", "").strip()
    if explicit:
        return explicit
    key = os.environ.get("HELIUS_API_KEY", "").strip()
    if key:
        return f"https://mainnet.helius-rpc.com/?api-key={key}"
    return None
