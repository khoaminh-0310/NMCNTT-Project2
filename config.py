"""System Configuration for 2D to 3D Generation Application.

Belongs to: Trịnh Duy Khoa (MSSV: 26127230) - Backend & Core.
Team: ae cây khế - Course: CSC00004 - Class: 26C05.
"""

import os
from typing import Final, FrozenSet


# --- File and Image Constraints ---
# Maximum uploaded image size: 10 MB
MAX_IMAGE_SIZE_BYTES: Final[int] = 10 * 1024 * 1024
MAX_INFERENCE_DIMENSION: Final[int] = 1024

# Supported image formats
ALLOWED_IMAGE_FORMATS: Final[FrozenSet[str]] = frozenset({"JPEG", "PNG", "WEBP"})
ALLOWED_FILE_EXTENSIONS: Final[FrozenSet[str]] = frozenset({".jpg", ".jpeg", ".png", ".webp"})

# --- Storage Paths ---
DEFAULT_OUTPUT_DIR: Final[str] = "outputs"
DEFAULT_ASSETS_DIR: Final[str] = "assets"
DEFAULT_SAMPLE_MODEL_PATH: Final[str] = os.path.join(DEFAULT_ASSETS_DIR, "sample_model.glb")

# --- AI & Hugging Face Settings ---
DEFAULT_HF_SPACE_ID: Final[str] = "microsoft/TRELLIS.2"
DEFAULT_API_TIMEOUT_SECONDS: Final[int] = 300

# Dynamic runtime configuration (reloaded via reload_env)
HF_SPACE_ID: str = DEFAULT_HF_SPACE_ID
HF_TOKEN: str = ""
MOCK_MODE: bool = False
API_TIMEOUT_SECONDS: int = DEFAULT_API_TIMEOUT_SECONDS


def _clean_env_value(raw_value: str) -> str:
    """Strip inline comments and surrounding quotes from a raw .env value."""
    val = raw_value.strip()
    if not val:
        return ""
    if val[0] in ('"', "'") and len(val) >= 2 and val[-1] == val[0]:
        return val[1:-1].strip()
    # Strip unquoted inline comments (e.g. '300 # timeout in seconds')
    val = val.split("#", 1)[0].strip()
    return val.strip("\"'")


def reload_env() -> None:
    """Reload environment variables from .env dynamically on every invocation."""
    global HF_SPACE_ID, HF_TOKEN, MOCK_MODE, API_TIMEOUT_SECONDS
    _env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(_env_path):
        with open(_env_path, "r", encoding="utf-8") as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _k, _v = _line.split("=", 1)
                    os.environ[_k.strip()] = _clean_env_value(_v)

    raw_space = _clean_env_value(os.getenv("HF_SPACE_ID", DEFAULT_HF_SPACE_ID))
    HF_SPACE_ID = (
        DEFAULT_HF_SPACE_ID
        if raw_space in ("", "microsoft/TRELLIS")
        else raw_space
    )
    HF_TOKEN = _clean_env_value(os.getenv("HF_TOKEN", ""))
    MOCK_MODE = _clean_env_value(os.getenv("MOCK_MODE", "false")).lower() in (
        "true",
        "1",
        "yes",
    )

    raw_timeout = _clean_env_value(
        os.getenv("API_TIMEOUT_SECONDS", str(DEFAULT_API_TIMEOUT_SECONDS))
    )
    try:
        parsed_timeout = int(raw_timeout)
        API_TIMEOUT_SECONDS = parsed_timeout if parsed_timeout > 0 else DEFAULT_API_TIMEOUT_SECONDS
    except ValueError:
        API_TIMEOUT_SECONDS = DEFAULT_API_TIMEOUT_SECONDS


# Initial load at startup
reload_env()
