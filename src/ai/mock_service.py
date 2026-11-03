"""Local Mock Inference Service for Offline Demo and Fallback Mode.

Author: Lê Bá Thi (MSSV: 26127431) - Kết nối AI & Inference.
Team: ae cây khế - Course: CSC00004 - Class: 26C05.
"""

import shutil
import time
from pathlib import Path
from typing import Callable, Optional

import config
from src.core.file_manager import generate_output_path

StatusCallback = Optional[Callable[[str, str], None]]

_DEFAULT_SAMPLE = Path(__file__).resolve().parents[2] / "assets" / "sample_model.glb"


def _notify(callback: StatusCallback, message: str, detail: str = "") -> None:
    if callback is not None:
        try:
            callback(message, detail)
        except Exception:
            pass


def get_sample_model_path() -> Path:
    """Resolve the local sample_model.glb path reliably from config or package root."""
    configured = Path(config.DEFAULT_SAMPLE_MODEL_PATH)
    if configured.is_file():
        return configured.resolve()
    if _DEFAULT_SAMPLE.is_file():
        return _DEFAULT_SAMPLE
    raise FileNotFoundError(
        f"Không tìm thấy file mô hình mẫu ({config.DEFAULT_SAMPLE_MODEL_PATH})."
    )


def run_mock_inference(
    image_path: str,
    status_callback: StatusCallback = None,
) -> tuple[str, bool]:
    """Simulate 3D generation in 1.5s with realistic step-by-step UI notifications."""
    sample_path = get_sample_model_path()

    _notify(
        status_callback,
        "[Mock Mode] Đang nạp mô hình mẫu từ assets/sample_model.glb...",
        "Đọc dữ liệu hình học và cấu trúc lưới 3D",
    )
    time.sleep(0.5)

    _notify(
        status_callback,
        "[Mock Mode] Đang dựng cấu trúc lưới 3D từ dữ liệu mẫu...",
        "Khởi tạo tọa độ đỉnh và bề mặt đa giác (Mesh)",
    )
    time.sleep(0.5)

    _notify(
        status_callback,
        "[Mock Mode] Đang đóng gói file GLB và Texture...",
        "Xuất kết quả vào thư mục outputs/",
    )
    time.sleep(0.5)

    output_path = generate_output_path("mock_result.glb")
    shutil.copyfile(sample_path, output_path)
    return output_path, True
