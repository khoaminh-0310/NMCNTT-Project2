# src/ai/trellis_client.py
"""Hugging Face TRELLIS Client with Real-time Status Callbacks and Graceful Fallback.

Author: Lê Bá Thi (26127431) - AI Model & Inference.
Team: ae cây khế - Course: CSC00004 - Class: 26C05.
"""

import logging
import os
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from pathlib import Path
from typing import Callable, Optional

from src.ai.mock_service import run_mock_inference
from src.core.contracts import GenerationResult
from src.core.file_manager import generate_output_path


_SPACE_ID = os.getenv("HF_SPACE_ID", "microsoft/TRELLIS.2")
_API_NAME = "/generate_and_extract_glb"
_REQUEST_TIMEOUT_SECONDS = int(os.getenv("API_TIMEOUT_SECONDS", "300"))
_LOGGER = logging.getLogger(__name__)

StatusCallback = Optional[Callable[[str, str], None]]


def _notify(callback: StatusCallback, message: str, detail: str = "") -> None:
    """Safely invoke UI status callback if provided."""
    if callback is not None:
        try:
            callback(message, detail)
        except Exception:
            pass


def _monitor_job(
    job,
    stage_title: str,
    stage_detail: str,
    timeout_sec: int,
    status_callback: StatusCallback = None,
) -> object:
    """Poll a gradio_client Job and stream real-time queue/GPU progress to status_callback."""
    start_wait = time.time()
    last_reported = ("", "")

    while not job.done():
        if time.time() - start_wait > timeout_sec:
            job.cancel()
            raise TimeoutError(
                f"TRELLIS inference exceeded {timeout_sec} seconds ({timeout_sec // 60} phút)"
            )

        msg = stage_title
        detail = stage_detail
        try:
            status = job.status()
            code = getattr(status.code, "value", str(status.code))

            if code in ("STARTING", "JOINING_QUEUE", "SENDING_DATA"):
                msg = f"⏳ {stage_title}"
                detail = "Đang gửi dữ liệu ảnh lên máy chủ Hugging Face..."
            elif code == "IN_QUEUE":
                if getattr(status, "rank", None) is not None and getattr(status, "queue_size", None):
                    msg = f"⏳ Đang xếp hàng đợi GPU (Vị trí #{status.rank + 1}/{status.queue_size})"
                elif getattr(status, "rank", None) is not None:
                    msg = f"⏳ Đang xếp hàng đợi GPU (Vị trí #{status.rank + 1})"
                else:
                    msg = "⏳ Đang chờ cấp phát tài nguyên ZeroGPU..."

                eta = getattr(status, "rank_eta", None)
                if eta is not None and eta > 0:
                    detail = f"{stage_title} • Ước tính chờ: ~{int(eta)}s"
                else:
                    detail = f"{stage_title} • Đang đợi đến lượt xử lý trên Hugging Face"
            elif code in ("PROCESSING", "PROGRESS", "ITERATING"):
                msg = f"⚡ {stage_title}"
                progress_data = getattr(status, "progress_data", None)
                if progress_data:
                    unit = progress_data[-1]
                    unit_desc = getattr(unit, "desc", None)
                    unit_prog = getattr(unit, "progress", None)
                    if unit_desc and unit_prog is not None:
                        detail = f"{unit_desc} ({int(unit_prog * 100)}%)"
                    elif unit_desc:
                        detail = str(unit_desc)
                    elif unit_prog is not None:
                        detail = f"{stage_detail} ({int(unit_prog * 100)}%)"
        except Exception:
            pass

        if (msg, detail) != last_reported:
            last_reported = (msg, detail)
            _notify(status_callback, msg, detail)

        time.sleep(0.25)

    return job.result()


def _predict(image_path: str, status_callback: StatusCallback = None) -> object:
    from gradio_client import Client, handle_file
    import config

    config.reload_env()
    space_id = os.getenv("HF_SPACE_ID", _SPACE_ID)
    token = os.getenv("HF_TOKEN") or None
    timeout_sec = int(os.getenv("API_TIMEOUT_SECONDS", str(_REQUEST_TIMEOUT_SECONDS)))

    _notify(
        status_callback,
        f"🌐 Đang kết nối tới Hugging Face ({space_id})...",
        "Khởi tạo phiên làm việc với máy chủ AI TRELLIS",
    )
    client = Client(space_id, token=token, verbose=False)

    named_endpoints = {
        getattr(e, "api_name", None) for e in client.endpoints.values()
    }

    if _API_NAME in named_endpoints:
        _notify(
            status_callback,
            "⚡ Đang tạo và trích xuất mô hình 3D...",
            "Gửi tác vụ tới endpoint /generate_and_extract_glb",
        )
        job = client.submit(handle_file(image_path), api_name=_API_NAME)
        return _monitor_job(
            job,
            "Đang dựng mô hình 3D trên máy chủ AI",
            "Xử lý pipeline tổng hợp TRELLIS",
            timeout_sec,
            status_callback,
        )

    if "/extract_glb" in named_endpoints and "/preprocess_image" in named_endpoints:
        _notify(
            status_callback,
            "⏳ Bước 1/3: Đang tiền xử lý ảnh đầu vào...",
            "Tách nền (Background Removal) và căn chỉnh vật thể 2D",
        )
        job1 = client.submit(
            input=handle_file(image_path),
            api_name="/preprocess_image",
        )
        preprocessed = _monitor_job(
            job1,
            "Bước 1/3: Đang tiền xử lý ảnh đầu vào",
            "Tách nền và chuẩn hóa kích thước vật thể",
            timeout_sec,
            status_callback,
        )

        _notify(
            status_callback,
            "⚡ Bước 2/3: Đang sinh cấu trúc hình học 3D (SLAT)...",
            "Chạy 12 bước lấy mẫu Diffusion trên ZeroGPU",
        )
        job2 = client.submit(
            image=handle_file(preprocessed),
            seed=0,
            resolution="1024",
            ss_guidance_strength=7.5,
            ss_guidance_rescale=0.7,
            ss_sampling_steps=12,
            ss_rescale_t=5.0,
            shape_slat_guidance_strength=7.5,
            shape_slat_guidance_rescale=0.5,
            shape_slat_sampling_steps=12,
            shape_slat_rescale_t=3.0,
            tex_slat_guidance_strength=1.0,
            tex_slat_guidance_rescale=0.0,
            tex_slat_sampling_steps=12,
            tex_slat_rescale_t=3.0,
            api_name="/image_to_3d",
        )
        _monitor_job(
            job2,
            "Bước 2/3: Đang sinh cấu trúc hình học 3D",
            "Tạo đám mây điểm và cấu trúc lưới không gian 3D",
            timeout_sec,
            status_callback,
        )

        _notify(
            status_callback,
            "🎨 Bước 3/3: Đang trích xuất file GLB & Texture...",
            "Tối ưu hóa lưới đa giác (Decimation) và phủ bề mặt 2048px",
        )
        job3 = client.submit(
            decimation_target=300000,
            texture_size=2048,
            api_name="/extract_glb",
        )
        return _monitor_job(
            job3,
            "Bước 3/3: Đang trích xuất file GLB & Texture",
            "Đóng gói mô hình 3D hoàn chỉnh (.glb)",
            timeout_sec,
            status_callback,
        )

    job = client.submit(handle_file(image_path))
    return _monitor_job(
        job,
        "Đang xử lý tạo mô hình 3D trên Hugging Face",
        "Đang chờ phản hồi từ máy chủ AI",
        timeout_sec,
        status_callback,
    )


def _predict_with_timeout(image_path: str, status_callback: StatusCallback = None) -> object:
    timeout_sec = int(os.getenv("API_TIMEOUT_SECONDS", "300"))
    executor = ThreadPoolExecutor(max_workers=1)
    future = executor.submit(_predict, image_path, status_callback)
    try:
        return future.result(timeout=timeout_sec)
    except FutureTimeoutError as exc:
        future.cancel()
        raise TimeoutError(
            f"TRELLIS inference exceeded {timeout_sec} seconds ({timeout_sec // 60} phút)"
        ) from exc
    finally:
        executor.shutdown(wait=False)


def _glb_path_from_result(result: object) -> Path:
    if isinstance(result, (list, tuple)):
        if not result:
            raise ValueError("TRELLIS returned no outputs")
        result = result[-1]

    if isinstance(result, dict):
        result = result.get("path")

    if not isinstance(result, str) or not result:
        raise TypeError("TRELLIS did not return a local GLB file path")

    path = Path(result)
    if not path.is_file():
        raise FileNotFoundError(f"TRELLIS output file was not found: {path}")
    return path


def _classify_inference_error(exc: Exception) -> str:
    """Classify external AI error into human-readable Vietnamese explanation."""
    msg = str(exc).lower()
    if "zerogpu" in msg or "quota" in msg or "limit" in msg:
        return (
            "Tài khoản Hugging Face đã dùng hết hạn mức thời lượng ZeroGPU miễn phí trong ngày "
            "(ZeroGPU Quota Exceeded). Bạn có thể đổi token từ tài khoản khác hoặc chờ hệ thống reset."
        )
    if "config_error" in msg:
        return "Space AI trên Hugging Face đang bảo trì (CONFIG_ERROR). Vui lòng thử lại sau."
    if "unauthorized" in msg or "401" in msg or "invalid token" in msg:
        return "Hugging Face Access Token không hợp lệ hoặc thiếu quyền đọc."
    if "timeout" in msg:
        timeout_sec = int(os.getenv("API_TIMEOUT_SECONDS", "300"))
        return f"Quá thời gian chờ phản hồi từ máy chủ AI ({timeout_sec // 60} phút Timeout)."
    return f"Không thể kết nối hoặc máy chủ AI không phản hồi ({type(exc).__name__})."


def run_inference_streaming(
    image_path: str,
    status_callback: StatusCallback = None,
) -> tuple[str, bool, str | None]:
    """Execute 3D reconstruction with live status callbacks and automatic fallback."""
    try:
        result = _predict_with_timeout(image_path, status_callback=status_callback)
        _notify(
            status_callback,
            "💾 Đang lưu mô hình 3D về máy cục bộ...",
            "Sao chép kết quả vào thư mục outputs/",
        )
        source_path = _glb_path_from_result(result)
        output_path = Path(generate_output_path("trellis_result.glb"))
        shutil.copyfile(source_path, output_path)
        return str(output_path), False, None
    except Exception as exc:
        _LOGGER.exception("TRELLIS inference failed; using the mock model instead")
        reason = _classify_inference_error(exc)
        _notify(
            status_callback,
            "⚠️ Máy chủ AI bận/hết quota — Đang chuyển sang mô hình dự phòng...",
            reason,
        )
        mock_path, is_mock = run_mock_inference(image_path)
        return mock_path, is_mock, reason


def run_inference_with_detail(image_path: str) -> tuple[str, bool, str | None]:
    """Execute 3D reconstruction inference with automatic fallback and classification."""
    return run_inference_streaming(image_path, status_callback=None)


def run_inference(image_path: str) -> tuple[str, bool]:
    """Execute 3D reconstruction inference with automatic fallback to mock."""
    glb_path, is_mock, _ = run_inference_with_detail(image_path)
    return glb_path, is_mock


def generate_3d_from_image(image_path: str) -> GenerationResult:
    """Generate 3D model from image, returning standardized GenerationResult.

    Adheres strictly to Technical Contract in Section 6.1 of the Technical Playbook.
    """
    start_time = time.time()
    try:
        glb_path, is_mock, fallback_reason = run_inference_with_detail(image_path)
        elapsed = round(time.time() - start_time, 2)

        if not glb_path or not os.path.exists(glb_path):
            return GenerationResult(
                success=False,
                glb_path=None,
                message="Không thể tạo hoặc tìm thấy file mô hình 3D (.glb).",
                inference_time=elapsed,
                is_mock=is_mock,
            )

        if is_mock:
            message = fallback_reason or "Đã tải xong mô hình bằng dữ liệu mẫu cục bộ (Mock Mode)."
        else:
            message = "Tạo mô hình 3D từ AI TRELLIS thành công."

        return GenerationResult(
            success=True,
            glb_path=glb_path,
            message=message,
            inference_time=elapsed,
            is_mock=is_mock,
        )
    except Exception as exc:
        elapsed = round(time.time() - start_time, 2)
        _LOGGER.exception("Unexpected error in generate_3d_from_image: %s", exc)
        return GenerationResult(
            success=False,
            glb_path=None,
            message=f"Lỗi hệ thống khi tạo mô hình 3D: {str(exc)}",
            inference_time=elapsed,
            is_mock=False,
        )