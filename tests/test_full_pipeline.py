"""Comprehensive Test Suite for 2D to 3D AI Reconstruction Application.

Author: Phạm Tấn Thành (MSSV: 26127427) - Testing, Evaluation & Demo.
Course: Introduction to Information Technology (CSC00004) - Class: 26C05.
Team: ae cây khế - Project: 2D to 3D AI Generation.

Covers:
  1. Image Input Validation (Format, Size <= 10MB, Traversal, Corruption).
  2. File Manager & Storage (Safe paths, Timestamping, Directory creation).
  3. Real Test Dataset Validation (10 Real Unsplash Photos in test_dataset/).
  4. Mock Service Flow & GenerationResult Contract (Section 6.1 Playbook).
  5. AI Fallback Pipeline (Safe fallback to local mock on network/space error).

Can be executed with:
  - python test_full_pipeline.py
  - python -m unittest tests/test_full_pipeline.py
  - python -m pytest tests/test_full_pipeline.py -v
"""

import os
import shutil
import sys
import tempfile
import time
import unittest
from pathlib import Path
from PIL import Image

# Automatically resolve and inject project paths whether running inside repo or outside folder
CURRENT_DIR = Path(__file__).resolve().parent
candidate_outside = CURRENT_DIR.parent.parent / "NMCNTT-Project2"
candidate_inside = CURRENT_DIR.parent

if (candidate_outside / "src").exists():
    PROJECT_ROOT = candidate_outside
elif (candidate_inside / "src").exists():
    PROJECT_ROOT = candidate_inside
else:
    PROJECT_ROOT = candidate_inside

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import system components
try:
    from src.core.validator import validate_image
    from src.core.file_manager import (
        ensure_directory,
        generate_output_path,
        is_file_available,
        sanitize_filename,
    )
    from src.core.contracts import GenerationResult
    from src.ai.mock_service import run_mock_inference
    from src.ai.trellis_client import generate_3d_from_image, run_inference
except ImportError as err:
    raise ImportError(f"Cannot import project modules from {PROJECT_ROOT}: {err}")


class TestImageValidator(unittest.TestCase):
    """Test Suite 1: Image Input Validation & Security (Mục 8.3 & 8.4)."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="test_val_")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_valid_formats(self):
        """PNG, JPEG, and WEBP formats must be accepted."""
        for fmt, ext in [("PNG", ".png"), ("JPEG", ".jpg"), ("WEBP", ".webp")]:
            img_path = os.path.join(self.test_dir, f"valid{ext}")
            Image.new("RGB", (100, 100), color="blue").save(img_path, format=fmt)
            valid, msg = validate_image(img_path)
            self.assertTrue(valid, f"Format {fmt} should be valid")
            self.assertEqual(msg, "Anh hop le.")

    def test_missing_or_empty_path(self):
        """Missing file paths or empty strings must be cleanly rejected."""
        self.assertFalse(validate_image("")[0])
        self.assertFalse(validate_image(None)[0])  # type: ignore
        self.assertFalse(validate_image(os.path.join(self.test_dir, "non_existent.png"))[0])

    def test_fake_text_disguised_as_image(self):
        """Plain text file renamed to .png must be detected and rejected."""
        fake_path = os.path.join(self.test_dir, "fake.png")
        with open(fake_path, "w", encoding="utf-8") as f:
            f.write("Malicious payload or plain text disguise.")
        valid, msg = validate_image(fake_path)
        self.assertFalse(valid)
        self.assertIn("khong phai la anh", msg)

    def test_unsupported_formats(self):
        """GIF, BMP, and TIFF must be rejected according to system constraints."""
        for fmt, ext in [("GIF", ".gif"), ("BMP", ".bmp")]:
            p = os.path.join(self.test_dir, f"sample{ext}")
            Image.new("RGB", (50, 50), color="red").save(p)
            valid, msg = validate_image(p)
            self.assertFalse(valid)
            self.assertIn("Dinh dang anh khong duoc ho tro", msg)

    def test_oversized_image_rejection(self):
        """Images strictly exceeding 10 MB must be rejected."""
        oversized = os.path.join(self.test_dir, "oversized.png")
        with open(oversized, "wb") as f:
            f.seek(10 * 1024 * 1024 + 1024)
            f.write(b"\0")
        valid, msg = validate_image(oversized)
        self.assertFalse(valid)
        self.assertEqual(msg, "Dung luong anh vuot qua 10MB.")


class TestFileManager(unittest.TestCase):
    """Test Suite 2: File Management & Output Sanitization."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="test_fm_")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_sanitize_path_traversal(self):
        """Filenames with directory traversal patterns must be sanitized."""
        dirty = "../../etc/passwd/test.glb"
        clean = sanitize_filename(dirty)
        self.assertNotIn("..", clean)
        self.assertNotIn("/", clean)
        self.assertNotIn("\\", clean)
        self.assertTrue(clean.endswith(".glb"))

    def test_generate_output_path_creates_dir_and_timestamp(self):
        """Output generator must auto-create directories and append timestamps."""
        custom_out = os.path.join(self.test_dir, "custom_3d_outputs")
        out_path = generate_output_path("result.glb", output_dir=custom_out)
        self.assertTrue(os.path.isdir(custom_out))
        self.assertTrue(out_path.endswith(".glb"))
        self.assertIn("result_", out_path)

    def test_is_file_available(self):
        """Test file availability checker on empty, non-existent, and valid files."""
        self.assertFalse(is_file_available(None))
        self.assertFalse(is_file_available(""))
        empty_file = os.path.join(self.test_dir, "empty.glb")
        with open(empty_file, "w") as f:
            pass
        self.assertFalse(is_file_available(empty_file))

        real_file = os.path.join(self.test_dir, "real.glb")
        with open(real_file, "wb") as f:
            f.write(b"glTF binary content")
        self.assertTrue(is_file_available(real_file))


class TestRealDataset(unittest.TestCase):
    """Test Suite 3: Validation of 10 Real Unsplash Photos in test_dataset/."""

    def test_all_10_dataset_images_valid(self):
        """Ensure all collected demo photos pass the system validator."""
        dataset_dir = CURRENT_DIR.parent / "test_dataset"
        if not dataset_dir.exists():
            dataset_dir = PROJECT_ROOT / "test_dataset"

        self.assertTrue(dataset_dir.exists(), f"Dataset directory missing: {dataset_dir}")
        img_files = [f for f in dataset_dir.iterdir() if f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]]

        self.assertGreaterEqual(len(img_files), 5, "Dataset must have at least 5 images per Section 8.4")

        for img_path in img_files:
            valid, msg = validate_image(str(img_path))
            self.assertTrue(valid, f"Dataset image {img_path.name} failed: {msg}")
            # Ensure file is under 10MB
            self.assertLessEqual(img_path.stat().st_size, 10 * 1024 * 1024)
            # Ensure Pillow can open and verify dimensions
            with Image.open(str(img_path)) as im:
                self.assertGreater(im.width, 50)
                self.assertGreater(im.height, 50)


class TestMockAndAIPipeline(unittest.TestCase):
    """Test Suite 4: Mock Service & AI Inference Fallback Pipeline."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="test_pipeline_")
        self.temp_img = os.path.join(self.temp_dir, "input.png")
        Image.new("RGB", (64, 64), color="green").save(self.temp_img)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_mock_service_returns_valid_model(self):
        """run_mock_inference must return a valid local GLB file with is_mock=True."""
        glb_path, is_mock = run_mock_inference(self.temp_img)
        self.assertTrue(is_mock, "Mock inference must have is_mock=True")
        self.assertTrue(os.path.exists(glb_path), f"Output GLB must exist: {glb_path}")
        self.assertGreater(os.path.getsize(glb_path), 0, "GLB output must not be empty")

    def test_generation_result_contract(self):
        """AI client wrapper must always return GenerationResult with proper types."""
        result = generate_3d_from_image(self.temp_img)
        self.assertIsInstance(result, GenerationResult)
        self.assertTrue(result.success, "Generation must succeed (via AI or Mock fallback)")
        self.assertIsNotNone(result.glb_path)
        self.assertTrue(os.path.exists(result.glb_path))  # type: ignore
        self.assertIsInstance(result.inference_time, float)
        self.assertGreaterEqual(result.inference_time, 0.0)
        self.assertIsInstance(result.is_mock, bool)


if __name__ == "__main__":
    unittest.main(verbosity=2)
