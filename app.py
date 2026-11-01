# app.py
"""Entry point for 2D to 3D Web Application (Gradio).

Team: ae cây khế - Course: CSC00004 - Class: 26C05.
Integrates UI layout, Core validator, File manager, and AI/Mock pipeline.
"""

import os
import queue
import shutil
import threading
import time

import gradio as gr

import config
from src.ai.trellis_client import run_inference_streaming
from src.core.contracts import GenerationResult
from src.core.file_manager import generate_output_path
from src.core.validator import validate_image
from src.ui.layout import create_ui, render_info_html, render_status_html


def format_file_size(size_bytes: int) -> str:
    """Định dạng kích thước file sang chuỗi dễ đọc (B, KB, MB)."""
    if size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    if size_bytes >= 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes} B"


def main_process(img_path: str) -> GenerationResult:
    """Xử lý chính: Kiểm tra ảnh đầu vào và điều phối giữa Mock Mode và AI.

    Giữ nguyên 100% hợp đồng dữ liệu chuẩn Mục 6.1 & 6.2 Tài liệu kỹ thuật.
    """
    config.reload_env()
    start_time = time.time()

    # 1. Kiểm tra ảnh rỗng
    if not img_path:
        return GenerationResult(
            success=False,
            glb_path=None,
            message="Vui lòng tải lên một bức ảnh trước khi tạo!",
            inference_time=0.0,
            is_mock=False,
        )

    # 2. Kiểm tra ảnh hợp lệ qua Core Validator (định dạng, kích thước <= 10MB)
    is_valid, validation_msg = validate_image(img_path)
    if not is_valid:
        return GenerationResult(
            success=False,
            glb_path=None,
            message=f"[LỖI ĐẦU VÀO]: {validation_msg}",
            inference_time=0.0,
            is_mock=False,
        )

    # 3. Phân nhánh Mock Mode hoặc AI thật dựa trên config.MOCK_MODE
    if config.MOCK_MODE:
        time.sleep(1.5)
        inference_time = round(time.time() - start_time, 2)

        sample_asset = config.DEFAULT_SAMPLE_MODEL_PATH
        if os.path.exists(sample_asset):
            out_glb_path = generate_output_path("mock_result.glb")
            shutil.copyfile(sample_asset, out_glb_path)
            return GenerationResult(
                success=True,
                glb_path=out_glb_path,
                message="Đã tải xong mô hình bằng dữ liệu mẫu cục bộ.",
                inference_time=inference_time,
                is_mock=True,
            )
        else:
            return GenerationResult(
                success=False,
                glb_path=None,
                message="Không tìm thấy file mô hình mẫu (assets/sample_model.glb).",
                inference_time=inference_time,
                is_mock=True,
            )
    else:
        try:
            from src.ai.trellis_client import generate_3d_from_image

            return generate_3d_from_image(img_path)
        except (ImportError, AttributeError):
            inference_time = round(time.time() - start_time, 2)
            return GenerationResult(
                success=False,
                glb_path=None,
                message="Module kết nối AI (src/ai/trellis_client.py) đang được Lê Bá Thi hoàn thiện.",
                inference_time=inference_time,
                is_mock=False,
            )


def stream_generation(img_path: str):
    """Bước 1 (Generator): Cập nhật trạng thái real-time trong khung 3D và đồng hồ đếm giờ.

    QUAN TRỌNG: Hàm generator này TUYỆT ĐỐI KHÔNG cập nhật trực tiếp `model_output` (gr.Model3D).
    Việc tách `model_output` sang Bước 2 (`render_model_3d` dùng `return` thuần túy qua `.then()`)
    giúp WebGL Canvas của Babylon.js không bị reset hay sập khung hình khi streaming.
    """
    config.reload_env()
    start_time = time.time()

    # Nhịp khởi đầu (0.0s)
    yield (
        render_status_html(
            "processing",
            "🔍 Đang kiểm tra ảnh đầu vào...",
            "Xác thực định dạng (JPG/PNG/WEBP) và dung lượng (<= 10MB)",
        ),
        render_info_html(status_msg="Đang kiểm định dữ liệu ảnh đầu vào..."),
        gr.update(
            value=None,
            interactive=False,
            variant="secondary",
            label="⏳ Đang xử lý mô hình...",
        ),
        "0.0s (Đang bắt đầu...)",
        None,
    )

    # 1. Kiểm tra ảnh rỗng
    if not img_path:
        elapsed = round(time.time() - start_time, 1)
        err_msg = "Vui lòng tải lên một bức ảnh trước khi bấm tạo 3D!"
        yield (
            render_status_html("error", err_msg, "Hãy chọn ảnh ở cột Đầu vào bên trái."),
            render_info_html(status_msg=f"❌ {err_msg}"),
            gr.update(
                value=None,
                interactive=False,
                variant="secondary",
                label="⏳ Chưa có mô hình để tải",
            ),
            f"{elapsed:.1f}s (Dừng lại do thiếu ảnh)",
            {"success": False, "glb_path": None},
        )
        return

    # 2. Kiểm tra ảnh hợp lệ qua Core Validator
    is_valid, validation_msg = validate_image(img_path)
    if not is_valid:
        elapsed = round(time.time() - start_time, 1)
        err_msg = f"[LỖI ĐẦU VÀO]: {validation_msg}"
        yield (
            render_status_html("error", err_msg, "Vui lòng chọn file ảnh hợp lệ (JPG, PNG, WEBP <= 10MB)."),
            render_info_html(status_msg=f"❌ {err_msg}"),
            gr.update(
                value=None,
                interactive=False,
                variant="secondary",
                label="⏳ Chưa có mô hình để tải",
            ),
            f"{elapsed:.1f}s (Dừng lại do lỗi ảnh)",
            {"success": False, "glb_path": None},
        )
        return

    # 3. Chạy tiến trình tạo 3D trên luồng nền (Background Thread) và đẩy trạng thái qua Queue
    event_queue: queue.Queue = queue.Queue()

    def status_callback(msg: str, detail: str = "") -> None:
        event_queue.put(("status", msg, detail))

    def worker_thread() -> None:
        try:
            if config.MOCK_MODE:
                status_callback(
                    "⏳ [Mock Mode] Đang phân tích và tách nền ảnh 2D...",
                    "Mô phỏng bước tiền xử lý vật thể",
                )
                time.sleep(0.5)
                status_callback(
                    "⚡ [Mock Mode] Đang dựng cấu trúc lưới 3D từ dữ liệu mẫu...",
                    "Khởi tạo tọa độ đỉnh và bề mặt đa giác (Mesh)",
                )
                time.sleep(0.5)
                status_callback(
                    "🎨 [Mock Mode] Đang đóng gói file GLB và Texture...",
                    "Xuất kết quả vào thư mục outputs/",
                )
                time.sleep(0.5)

                sample_asset = config.DEFAULT_SAMPLE_MODEL_PATH
                if os.path.exists(sample_asset):
                    out_glb = generate_output_path("mock_result.glb")
                    shutil.copyfile(sample_asset, out_glb)
                    event_queue.put(
                        (
                            "done",
                            out_glb,
                            True,
                            "Hệ thống đang chủ động bật chế độ giả lập cục bộ (MOCK_MODE=true).",
                        )
                    )
                else:
                    event_queue.put(
                        (
                            "error",
                            f"Không tìm thấy file mô hình mẫu ({sample_asset}).",
                        )
                    )
            else:
                glb_path, is_mock, reason = run_inference_streaming(
                    img_path, status_callback=status_callback
                )
                event_queue.put(("done", glb_path, is_mock, reason))
        except Exception as exc:
            event_queue.put(("error", str(exc)))

    thread = threading.Thread(target=worker_thread, daemon=True)
    thread.start()

    current_msg = "🌐 Đang kết nối tới máy chủ xử lý 3D..."
    current_detail = "Đang khởi tạo tiến trình dựng hình"
    final_data = None
    error_msg = None

    # Vòng lặp cập nhật đồng hồ Timer (mỗi 0.1s) và trạng thái real-time
    while thread.is_alive() or not event_queue.empty():
        try:
            while True:
                item = event_queue.get_nowait()
                if item[0] == "status":
                    current_msg = item[1]
                    current_detail = item[2]
                elif item[0] == "done":
                    final_data = item[1:]
                elif item[0] == "error":
                    error_msg = item[1]
        except queue.Empty:
            pass

        if final_data is not None or error_msg is not None:
            break

        elapsed = time.time() - start_time
        yield (
            render_status_html(
                "processing",
                current_msg,
                f"{current_detail} • ⏱️ {elapsed:.1f}s",
            ),
            gr.update(),
            gr.update(),
            f"{elapsed:.1f}s (Đang xử lý...)",
            None,
        )
        time.sleep(0.1)

    total_elapsed = round(time.time() - start_time, 1)

    # Xử lý nếu có lỗi từ worker
    if error_msg:
        yield (
            render_status_html("error", f"Lỗi hệ thống: {error_msg}"),
            render_info_html(status_msg=f"❌ Lỗi hệ thống: {error_msg}"),
            gr.update(
                value=None,
                interactive=False,
                variant="secondary",
                label="⏳ Chưa có mô hình để tải",
            ),
            f"{total_elapsed:.1f}s (Dừng lại do lỗi)",
            {"success": False, "glb_path": None},
        )
        return

    if not final_data:
        yield (
            render_status_html("error", "Không nhận được phản hồi từ tiến trình xử lý."),
            render_info_html(status_msg="❌ Không nhận được phản hồi từ tiến trình xử lý."),
            gr.update(
                value=None,
                interactive=False,
                variant="secondary",
                label="⏳ Chưa có mô hình để tải",
            ),
            f"{total_elapsed:.1f}s (Thất bại)",
            {"success": False, "glb_path": None},
        )
        return

    out_glb_path, is_mock, detail_reason = final_data
    if not out_glb_path or not os.path.exists(out_glb_path):
        yield (
            render_status_html("error", "Không tìm thấy file mô hình 3D kết quả (.glb)."),
            render_info_html(status_msg="❌ Không tìm thấy file mô hình 3D kết quả (.glb)."),
            gr.update(
                value=None,
                interactive=False,
                variant="secondary",
                label="⏳ Chưa có mô hình để tải",
            ),
            f"{total_elapsed:.1f}s (Thất bại)",
            {"success": False, "glb_path": None},
        )
        return

    # Tính toán Metadata khi thành công
    file_size_bytes = os.path.getsize(out_glb_path)
    file_size_str = format_file_size(file_size_bytes)
    file_name = os.path.basename(out_glb_path)
    engine_name = (
        "Mock Service (Mô phỏng / Dự phòng)"
        if is_mock
        else f"Microsoft TRELLIS ({config.HF_SPACE_ID})"
    )

    if is_mock:
        if config.MOCK_MODE:
            detail = "Hệ thống đang chủ động bật chế độ giả lập cục bộ (MOCK_MODE=true)."
        elif detail_reason:
            detail = detail_reason
        else:
            detail = "Hệ thống đang bật chế độ dự phòng do máy chủ AI không phản hồi."
        status_msg = (
            f"ℹ️ [CHẾ ĐỘ MÔ PHỎNG / DỰ PHÒNG]: Đang sử dụng mô hình 3D mẫu ({config.DEFAULT_SAMPLE_MODEL_PATH}). "
            f"Chi tiết: {detail}"
        )
    else:
        status_msg = (
            f"Thành công: Đã tạo mô hình 3D từ mô hình TRELLIS trong {total_elapsed:.1f} giây."
        )

    # Cập nhật bảng Metadata + Timer và chuyển sang Bước 2 (.then) để nạp Model3D
    yield (
        "",
        render_info_html(
            file_name=file_name,
            file_size=file_size_str,
            engine=engine_name,
            inference_time=f"{total_elapsed:.1f}s",
            status_msg=status_msg,
            is_mock=is_mock,
        ),
        gr.update(
            value=out_glb_path,
            interactive=True,
            variant="primary",
            label="⬇️ Tải mô hình 3D (.glb)",
        ),
        f"{total_elapsed:.1f}s — {status_msg}",
        {"success": True, "glb_path": out_glb_path},
    )


def render_model_3d(state: dict | None):
    """Bước 2 (Hàm return thuần túy): Nạp file .glb vào gr.Model3D đúng 1 lần duy nhất.

    Cơ chế `return` đơn lẻ này giống 100% với hàm `on_click` ở commit 33985ec gốc trên GitHub,
    đảm bảo Babylon.js nhận sự kiện `process_completed` sạch và dựng hình 3D chính xác.
    """
    if not state or not state.get("success") or not state.get("glb_path"):
        return (
            None,
            gr.update(),
            gr.update(
                value=None,
                interactive=False,
                variant="secondary",
                label="⏳ Chưa có mô hình để tải",
            ),
        )

    glb_path = state["glb_path"]
    return (
        glb_path,
        "",
        gr.update(
            value=glb_path,
            interactive=True,
            variant="primary",
            label="⬇️ Tải mô hình 3D (.glb)",
        ),
    )


# Giữ bí danh on_click cho khả năng tương thích ngược
on_click = stream_generation

# --- KHỞI TẠO GIAO DIỆN ---
(
    demo,
    image_input,
    btn_generate,
    model_output,
    model_status_box,
    model_info_box,
    btn_download,
    status_box,
    result_state,
) = create_ui()

with demo:
    # Chuỗi sự kiện 2 bước:
    # 1. stream_generation (Generator): cập nhật status trong box 3D, metadata và timer 0.1s
    # 2. render_model_3d (Return thường): nạp file .glb vào model_output ngay khi bước 1 xong
    gen_event = btn_generate.click(
        fn=stream_generation,
        inputs=[image_input],
        outputs=[
            model_status_box,
            model_info_box,
            btn_download,
            status_box,
            result_state,
        ],
    )
    gen_event.then(
        fn=render_model_3d,
        inputs=[result_state],
        outputs=[model_output, model_status_box, btn_download],
    )

# Chạy ứng dụng
if __name__ == "__main__":
    demo.queue()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        allowed_paths=[
            os.path.abspath(config.DEFAULT_OUTPUT_DIR),
            os.path.abspath(config.DEFAULT_ASSETS_DIR),
            os.path.abspath("."),
        ],
    )