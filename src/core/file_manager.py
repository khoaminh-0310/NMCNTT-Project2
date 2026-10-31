"""File Management Module for 2D to 3D Generation.

Handles directory creation, safe filename generation, and output path routing.
Author: Trịnh Duy Khoa (26127230) - Backend & Core.
Team: ae cây khế - Course: CSC00004 - Class: 26C05.
"""

import datetime
import os
import re
import uuid
from typing import Optional

try:
    from config import DEFAULT_OUTPUT_DIR
except ImportError:
    try:
        from src.core.config import DEFAULT_OUTPUT_DIR  # type: ignore
    except ImportError:
        DEFAULT_OUTPUT_DIR = "outputs"


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent directory traversal and remove illegal characters.

    Args:
        filename: Raw incoming filename or basename.

    Returns:
        Cleaned, secure filename string.
    """
    if not filename or not isinstance(filename, str):
        return "result.glb"

    base_name = os.path.basename(filename.strip())
    # Replace any character other than alphanumeric, dots, underscores, and hyphens with an underscore
    sanitized = re.sub(r"[^\w\.-]", "_", base_name)
    sanitized = re.sub(r"_+", "_", sanitized).strip("_.")
    return sanitized if sanitized else "result.glb"


def ensure_directory(directory_path: str = DEFAULT_OUTPUT_DIR) -> str:
    """Ensure that the target directory exists on disk, creating it if needed.

    Args:
        directory_path: Filesystem path to the directory.

    Returns:
        Normalized path to the guaranteed existing directory.
    """
    normalized_path = os.path.normpath(directory_path)
    os.makedirs(normalized_path, exist_ok=True)
    return normalized_path


def generate_output_path(
    base_filename: str = "result.glb",
    output_dir: str = DEFAULT_OUTPUT_DIR,
    include_uuid: bool = False,
) -> str:
    """Generate a unique timestamped file path inside the designated output directory.

    Guarantees no overwriting even when multiple 3D generations happen sequentially.

    Args:
        base_filename: Desired basename or suffix (e.g. 'result.glb', 'mock_result.glb').
        output_dir: Directory path where output will be stored.
        include_uuid: If True, appends a short UUID suffix for extra collision protection.

    Returns:
        Normalized relative/absolute path to the target output file.
    """
    target_dir = ensure_directory(output_dir)
    clean_name = sanitize_filename(base_filename)
    name_root, ext = os.path.splitext(clean_name)
    if not ext:
        ext = ".glb"

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    if include_uuid:
        unique_suffix = uuid.uuid4().hex[:6]
        final_filename = f"{name_root}_{timestamp}_{unique_suffix}{ext}"
    else:
        final_filename = f"{name_root}_{timestamp}{ext}"

    return os.path.normpath(os.path.join(target_dir, final_filename))


def is_file_available(file_path: Optional[str]) -> bool:
    """Check if the given file exists, is a regular file, and has non-zero size."""
    if not file_path or not isinstance(file_path, str):
        return False
    norm_path = os.path.normpath(file_path)
    return os.path.isfile(norm_path) and os.path.getsize(norm_path) > 0
