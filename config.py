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
DEFAULT_HF_SPACE_ID: Final[str] = "microsoft/TRELLIS"
API_TIMEOUT_SECONDS: Final[int] = 120

# Environment variables (overridable via .env or system environment)
HF_SPACE_ID: str = os.getenv("HF_SPACE_ID", DEFAULT_HF_SPACE_ID)
HF_TOKEN: str = os.getenv("HF_TOKEN", "")
MOCK_MODE: bool = os.getenv("MOCK_MODE", "false").strip().lower() in ("true", "1", "yes")
