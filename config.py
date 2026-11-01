"""System Configuration for 2D to 3D Generation Application.

Belongs to: Trịnh Duy Khoa (MSSV: 26127230) - Backend & Core.
Team: ae cây khế - Course: CSC00004 - Class: 26C05.
"""

import os
from typing import Final, FrozenSet


# --- File and Image Constraints ---
# Maximum uploaded image size: 10 MB
MAX_IMAGE_SIZE_BYTES: Final[int] = 10 * 1024 * 1024

# Supported image formats
ALLOWED_IMAGE_FORMATS: Final[FrozenSet[str]] = frozenset({"JPEG", "PNG", "WEBP"})
ALLOWED_FILE_EXTENSIONS: Final[FrozenSet[str]] = frozenset({".jpg", ".jpeg", ".png", ".webp"})

# --- Storage Paths ---
DEFAULT_OUTPUT_DIR: Final[str] = "outputs"
DEFAULT_ASSETS_DIR: Final[str] = "assets"
DEFAULT_SAMPLE_MODEL_PATH: Final[str] = os.path.join(DEFAULT_ASSETS_DIR, "sample_model.glb")

# --- AI & Hugging Face Settings ---
DEFAULT_HF_SPACE_ID: Final[str] = "microsoft/TRELLIS.2"
API_TIMEOUT_SECONDS: Final[int] = 300

# Environment variables (overridable via .env or system environment)
HF_SPACE_ID: str = DEFAULT_HF_SPACE_ID
HF_TOKEN: str = ""
MOCK_MODE: bool = False


def reload_env() -> None:
    """Reload environment variables from .env dynamically on every invocation."""
    global HF_SPACE_ID, HF_TOKEN, MOCK_MODE
    _env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(_env_path):
        with open(_env_path, "r", encoding="utf-8") as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _k, _v = _line.split("=", 1)
                    os.environ[_k.strip()] = _v.strip()

    HF_SPACE_ID = os.getenv("HF_SPACE_ID", DEFAULT_HF_SPACE_ID)
    HF_TOKEN = os.getenv("HF_TOKEN", "")
    MOCK_MODE = os.getenv("MOCK_MODE", "false").strip().lower() in ("true", "1", "yes")


# Initial load at startup
reload_env()
