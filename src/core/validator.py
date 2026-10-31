"""Image Validation Module.

Validates input 2D image before passing to AI inference or mock service.
Author: Trịnh Duy Khoa (26127230) - Backend & Core.
Team: ae cây khế - Course: CSC00004 - Class: 26C05.
"""

import os
from typing import Tuple
from PIL import Image

try:
    from config import ALLOWED_IMAGE_FORMATS, MAX_IMAGE_SIZE_BYTES
except ImportError:
    try:
        from src.core.config import ALLOWED_IMAGE_FORMATS, MAX_IMAGE_SIZE_BYTES  # type: ignore
    except ImportError:
        MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024
        ALLOWED_IMAGE_FORMATS = frozenset({"JPEG", "PNG", "WEBP"})


def validate_image(image_path: str) -> Tuple[bool, str]:
    """Validate uploaded image path for existence, size, and image format.

    Args:
        image_path: Absolute or relative filesystem path to the uploaded image.

    Returns:
        Tuple of (is_valid: bool, message: str) matching technical contract specifications.
    """
    if not image_path or not isinstance(image_path, str):
        return False, "Khong tim thay file anh."

    clean_path = os.path.normpath(image_path)
    if not os.path.exists(clean_path) or not os.path.isfile(clean_path):
        return False, "Khong tim thay file anh."

    try:
        file_size = os.path.getsize(clean_path)
    except OSError:
        return False, "File tai len bi loi hoac khong phai la anh hop le."

    if file_size == 0:
        return False, "File tai len bi loi hoac khong phai la anh hop le."

    if file_size > MAX_IMAGE_SIZE_BYTES:
        return False, "Dung luong anh vuot qua 10MB."

    try:
        with Image.open(clean_path) as img:
            format_name = img.format
            if not format_name or format_name.upper() not in ALLOWED_IMAGE_FORMATS:
                return False, "Dinh dang anh khong duoc ho tro (chi nhan JPG, PNG, WEBP)."
            img.verify()
    except Exception:
        return False, "File tai len bi loi hoac khong phai la anh hop le."

    return True, "Anh hop le."
