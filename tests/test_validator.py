"""Unit Tests for Validator and File Manager.

Author: Trịnh Duy Khoa (26127230) & Phạm Tấn Thành (26127427).
Team: ae cây khế - Course: CSC00004 - Class: 26C05.
Can be executed with either `pytest test_validator.py` or standard `python test_validator.py`.
"""

import os
import shutil
import sys
import tempfile
import unittest
from PIL import Image

# Ensure project root and current dir are in sys.path for robust imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Dynamic imports allowing execution from project root or inside tests directory
try:
    from src.core.validator import validate_image
    from src.core.file_manager import (
        ensure_directory,
        generate_output_path,
        is_file_available,
        sanitize_filename,
    )
except ImportError:
    from validator import validate_image
    from file_manager import (
        ensure_directory,
        generate_output_path,
        is_file_available,
        sanitize_filename,
    )


class TestValidatorAndFileManager(unittest.TestCase):
    """Test suite covering image validation and file management routines."""

    def setUp(self):
        """Create a temporary directory for test fixtures."""
        self.test_dir = tempfile.mkdtemp(prefix="test_2d_to_3d_")

    def tearDown(self):
        """Remove temporary directory after tests."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_valid_png_image(self):
        """Valid PNG image should pass validation with success message."""
        img_path = os.path.join(self.test_dir, "valid.png")
        img = Image.new("RGB", (200, 200), color="blue")
        img.save(img_path, format="PNG")

        is_valid, msg = validate_image(img_path)
        self.assertTrue(is_valid)
        self.assertEqual(msg, "Anh hop le.")

    def test_valid_jpeg_image(self):
        """Valid JPEG image should pass validation."""
        img_path = os.path.join(self.test_dir, "valid.jpg")
        img = Image.new("RGB", (100, 100), color="green")
        img.save(img_path, format="JPEG")

        is_valid, msg = validate_image(img_path)
        self.assertTrue(is_valid)
        self.assertEqual(msg, "Anh hop le.")

    def test_valid_webp_image(self):
        """Valid WEBP image should pass validation."""
        img_path = os.path.join(self.test_dir, "valid.webp")
        img = Image.new("RGB", (150, 150), color="yellow")
        img.save(img_path, format="WEBP")

        is_valid, msg = validate_image(img_path)
        self.assertTrue(is_valid)
        self.assertEqual(msg, "Anh hop le.")

    def test_non_existent_file(self):
        """Non-existent path should return False with not found message."""
        fake_path = os.path.join(self.test_dir, "does_not_exist.png")
        is_valid, msg = validate_image(fake_path)
        self.assertFalse(is_valid)
        self.assertEqual(msg, "Khong tim thay file anh.")

    def test_empty_or_none_path(self):
        """Empty string or None should be rejected cleanly without exceptions."""
        is_valid_empty, msg_empty = validate_image("")
        self.assertFalse(is_valid_empty)
        self.assertEqual(msg_empty, "Khong tim thay file anh.")

        is_valid_none, msg_none = validate_image(None)  # type: ignore
        self.assertFalse(is_valid_none)
        self.assertEqual(msg_none, "Khong tim thay file anh.")

    def test_invalid_text_file(self):
        """Text file with .png extension should be detected as invalid/corrupted."""
        fake_img = os.path.join(self.test_dir, "fake.png")
        with open(fake_img, "w", encoding="utf-8") as f:
            f.write("This is not an image file content.")

        is_valid, msg = validate_image(fake_img)
        self.assertFalse(is_valid)
        self.assertIn("khong phai la anh", msg)

    def test_unsupported_format_gif(self):
        """GIF format is not supported for 3D reconstruction and must be rejected."""
        gif_path = os.path.join(self.test_dir, "sample.gif")
        img = Image.new("RGB", (50, 50), color="red")
        img.save(gif_path, format="GIF")

        is_valid, msg = validate_image(gif_path)
        self.assertFalse(is_valid)
        self.assertIn("Dinh dang anh khong duoc ho tro", msg)

    def test_oversized_image(self):
        """Image exceeding 10MB limit should be rejected."""
        oversized_path = os.path.join(self.test_dir, "oversized.png")
        # Create a dummy file with size 10MB + 1KB
        with open(oversized_path, "wb") as f:
            f.seek(10 * 1024 * 1024 + 1024)
            f.write(b"\0")

        is_valid, msg = validate_image(oversized_path)
        self.assertFalse(is_valid)
        self.assertEqual(msg, "Dung luong anh vuot qua 10MB.")

    def test_sanitize_filename(self):
        """Filename sanitizer should remove directory traversal sequences."""
        bad_name = "../../dangerous/../payload.glb"
        safe_name = sanitize_filename(bad_name)
        self.assertNotIn("..", safe_name)
        self.assertNotIn("/", safe_name)
        self.assertNotIn("\\", safe_name)
        self.assertTrue(safe_name.endswith(".glb"))

    def test_generate_output_path(self):
        """Output path generation should auto-create directory and append timestamp."""
        out_subfolder = os.path.join(self.test_dir, "custom_outputs")
        out_path = generate_output_path("test_result.glb", output_dir=out_subfolder)

        self.assertTrue(os.path.isdir(out_subfolder))
        self.assertTrue(out_path.startswith(out_subfolder))
        self.assertTrue(out_path.endswith(".glb"))
        self.assertIn("test_result_", out_path)

    def test_is_file_available(self):
        """Test existence check helper."""
        self.assertFalse(is_file_available(None))
        self.assertFalse(is_file_available(""))

        empty_file = os.path.join(self.test_dir, "empty.glb")
        with open(empty_file, "w") as f:
            pass
        self.assertFalse(is_file_available(empty_file))

        non_empty = os.path.join(self.test_dir, "model.glb")
        with open(non_empty, "w") as f:
            f.write("mock binary 3d content")
        self.assertTrue(is_file_available(non_empty))


# Pytest compatibility functions as specified in Section 8.4
def test_valid_image(tmp_path):
    """Pytest-style test matching Section 8.4 playbook."""
    img_path = str(tmp_path / "valid.png")
    Image.new("RGB", (200, 200), color="red").save(img_path)
    is_valid, msg = validate_image(img_path)
    assert is_valid is True
    assert msg == "Anh hop le."


def test_invalid_text_file(tmp_path):
    """Pytest-style test for fake image matching Section 8.4 playbook."""
    fake_img = str(tmp_path / "fake.png")
    with open(fake_img, "w", encoding="utf-8") as f:
        f.write("This is not an image file")
    is_valid, msg = validate_image(fake_img)
    assert is_valid is False
    assert "khong phai la anh" in msg


if __name__ == "__main__":
    unittest.main()
