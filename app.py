# app.py
"""Entry point for 2D to 3D Web Application (Gradio).

Team: ae cây khế - Course: CSC00004 - Class: 26C05.
Integrates UI layout, Core validator, File manager, and AI/Mock pipeline.
"""

import os
import shutil
import time

import gradio as gr

import config
from src.core.contracts import GenerationResult
from src.core.file_manager import generate_output_path
from src.core.validator import validate_image
from src.ui.layout import create_ui


def main_process(img_path: str) -> GenerationResult:
    """Xử lý chính: Kiểm tra ảnh đầu vào và điều phối giữa Mock Mode và AI."""
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
        # Giả lập thời gian xử lý khoảng 1.5 giây theo Playbook
        time.sleep(1.5)
        inference_time = round(time.time() - start_time, 2)

        sample_asset = config.DEFAULT_SAMPLE_MODEL_PATH
        if os.path.exists(sample_asset):
            # Tạo đường dẫn kết quả an toàn trong thư mục outputs/
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
        # Nhánh gọi AI thật từ Hugging Face (Do Lê Bá Thi phụ trách tích hợp)
        try:
            from src.ai.trellis_client import generate_3d_from_image  # type: ignore

            return generate_3d_from_image(img_path)
        except (ImportError, AttributeError):
            inference_time = round(time.time() - start_time, 2)
            return GenerationResult(
                success=False,
                glb_path=None,
                message="Module kết nối AI (src/ai/trellis_client.py) đang được Lê Bá Thi hoàn thiện. Vui lòng bật MOCK_MODE=true trong file .env để chạy thử giao diện.",
                inference_time=inference_time,
                is_mock=False,
            )


def on_click(img_path: str):
    """Xử lý sự kiện khi người dùng bấm nút 'Bắt đầu tạo 3D'.
    
    Định dạng thông báo trạng thái tuân thủ chính xác Mục 6.2 Tài liệu kỹ thuật.
    """
    result = main_process(img_path)

    # Trường hợp 1: Có lỗi (ảnh không hợp lệ hoặc thiếu ảnh)
    if not result.success:
        return None, f"❌ {result.message}"

    # Trường hợp 2: Chế độ giả lập (Mock Mode) - Tuân thủ Mục 6.2 Tài liệu kỹ thuật
    if result.is_mock:
        status_msg = (
            "[CHẾ ĐỘ MÔ PHỎNG / MOCK]: Đây là mô hình 3D mẫu (assets/sample_model.glb) "
            "do hệ thống đang bật chế độ dự phòng hoặc API không phản hồi."
        )
    # Trường hợp 3: AI thật chạy thành công - Tuân thủ Mục 6.2 Tài liệu kỹ thuật
    else:
        status_msg = (
            f"Thành công: Đã tạo mô hình 3D từ mô hình TRELLIS trong {result.inference_time:.1f} giây."
        )

    return result.glb_path, status_msg


# --- KHỞI TẠO GIAO DIỆN ---
demo, image_input, btn_generate, model_output, status_box = create_ui()

with demo:
    # Liên kết sự kiện click của nút bấm với hàm on_click
    btn_generate.click(
        fn=on_click,
        inputs=[image_input],
        outputs=[model_output, status_box],
    )

# Chạy ứng dụng
if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
