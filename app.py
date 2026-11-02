# app.py
"""Entry point for 2D to 3D Web Application (Gradio).

Author duy nhất: Nguyễn Hồng Bảo Trân (MSSV: 26127470) - Giao diện Web (UI/UX).
Team: ae cây khế - Course: CSC00004 - Class: 26C05.
Integrates UI layout, Core validator, File manager, and AI/Mock pipeline.
Strictly adheres to Section 4 & 5.1 of 'Tài liệu kỹ thuật project AI' and Cẩm nang UI.
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
from src.ui.theme import CUSTOM_CSS, create_studio_theme


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
                message="Module kết nối AI (src/ai/trellis_client.py) đang được hoàn thiện.",
                inference_time=inference_time,
                is_mock=False,
            )


def stream_generation(img_path: str):
    """Bước 1 (Generator): Luồng xử lý nền và cập nhật trạng thái thời gian thực.

    Tuân thủ nghiêm ngặt 5 chốt chặn kỹ thuật:
    - KHÔNG gán model_output vào hàm này để bảo vệ WebGL canvas.
    - Áp dụng Event-driven DOM update: chỉ render lại HTML box 3D khi có bước mới.
    - Ô dưới (status_box) chỉ hiển thị duy nhất số giây đếm giờ, không trùng lặp text thông báo.
    - Khi hoàn tất, yield '' cho model_status_box để gỡ bỏ lớp phủ.
    """
    config.reload_env()
    start_time = time.time()

    # 1. Kiểm tra ảnh rỗng
    if not img_path:
        yield (
            render_status_html("error", "Chưa có ảnh đầu vào", "Vui lòng chọn hoặc kéo thả một bức ảnh vào khung trước khi bắt đầu."),
            render_info_html(status_msg="[LỖI]: Chưa chọn file ảnh đầu vào."),
            gr.update(value=None, interactive=False, variant="secondary", label="Chưa có mô hình để tải"),
            "0.0s (Lỗi)",
            {"success": False, "glb_path": None},
        )
        return

    # 2. Kiểm tra tính hợp lệ của ảnh qua Core Validator
    is_valid, validation_msg = validate_image(img_path)
    if not is_valid:
        yield (
            render_status_html("error", "Ảnh không hợp lệ", validation_msg),
            render_info_html(status_msg=f"[LỖI ĐẦU VÀO]: {validation_msg}"),
            gr.update(value=None, interactive=False, variant="secondary", label="Chưa có mô hình để tải"),
            "0.0s (Lỗi)",
            {"success": False, "glb_path": None},
        )
        return

    # 3. Khởi tạo trạng thái đang xử lý ban đầu
    initial_msg = (
        "[Mock Mode] Đang khởi chạy quy trình giả lập..."
        if config.MOCK_MODE
        else "Đang kết nối tới máy chủ Hugging Face ZeroGPU..."
    )
    initial_detail = "Đang kiểm tra hàng đợi và tài nguyên"

    yield (
        render_status_html("processing", initial_msg, initial_detail),
        render_info_html(status_msg="Đang xử lý tạo mô hình 3D..."),
        gr.update(value=None, interactive=False, variant="secondary", label="Đang tạo mô hình..."),
        "0.0s",
        None,
    )

    # 4. Hàng đợi giao tiếp luồng
    event_queue = queue.Queue()

    def status_callback(msg: str, detail: str = ""):
        event_queue.put(("status", msg, detail))

    def worker_thread():
        try:
            if config.MOCK_MODE:
                status_callback(
                    "[Mock Mode] Đang nạp mô hình mẫu từ assets/sample_model.glb...",
                    "Đọc dữ liệu hình học và cấu trúc lưới 3D",
                )
                time.sleep(0.5)
                status_callback(
                    "[Mock Mode] Đang dựng cấu trúc lưới 3D từ dữ liệu mẫu...",
                    "Khởi tạo tọa độ đỉnh và bề mặt đa giác (Mesh)",
                )
                time.sleep(0.5)
                status_callback(
                    "[Mock Mode] Đang đóng gói file GLB và Texture...",
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

    current_msg = initial_msg
    current_detail = initial_detail
    final_data = None
    error_msg = None

    # Vòng lặp Event-driven DOM update: Chỉ cập nhật box 3D khi có bước mới
    while thread.is_alive() or not event_queue.empty():
        status_changed = False
        try:
            while True:
                item = event_queue.get_nowait()
                if item[0] == "status":
                    current_msg = item[1]
                    current_detail = item[2]
                    status_changed = True
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
            render_status_html("processing", current_msg, current_detail)
            if status_changed
            else gr.update(),
            gr.update(),
            gr.update(),
            f"{elapsed:.1f}s",  # Chỉ hiển thị số giây đếm giờ, không trùng lặp text
            None,
        )
        time.sleep(0.1)

    total_elapsed = round(time.time() - start_time, 1)

    # Xử lý nếu có lỗi từ worker
    if error_msg:
        yield (
            render_status_html("error", "Lỗi xử lý", str(error_msg)),
            render_info_html(status_msg=f"[LỖI]: {error_msg}"),
            gr.update(
                value=None,
                interactive=False,
                variant="secondary",
                label="Chưa có mô hình để tải",
            ),
            f"{total_elapsed:.1f}s (Lỗi)",
            {"success": False, "glb_path": None},
        )
        return

    if not final_data:
        yield (
            render_status_html("error", "Không nhận được phản hồi", "Tiến trình xử lý không trả về kết quả."),
            render_info_html(status_msg="[LỖI]: Không nhận được phản hồi từ tiến trình xử lý."),
            gr.update(
                value=None,
                interactive=False,
                variant="secondary",
                label="Chưa có mô hình để tải",
            ),
            f"{total_elapsed:.1f}s (Thất bại)",
            {"success": False, "glb_path": None},
        )
        return

    out_glb_path, is_mock, detail_reason = final_data
    if not out_glb_path or not os.path.exists(out_glb_path):
        yield (
            render_status_html("error", "Thiếu file đầu ra", "Không tìm thấy file mô hình 3D (.glb) được xuất."),
            render_info_html(status_msg="[LỖI]: Không tìm thấy file mô hình 3D kết quả (.glb)."),
            gr.update(
                value=None,
                interactive=False,
                variant="secondary",
                label="Chưa có mô hình để tải",
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
        "Mock Service (Mô phỏng)"
        if is_mock
        else f"TRELLIS 2.0 ({config.HF_SPACE_ID})"
    )

    if is_mock:
        if config.MOCK_MODE:
            detail = "Hệ thống đang chủ động bật chế độ giả lập cục bộ (MOCK_MODE=true)."
        elif detail_reason:
            detail = detail_reason
        else:
            detail = "Hệ thống đang bật chế độ dự phòng do máy chủ AI không phản hồi."
        status_msg = (
            f"[CHẾ ĐỘ MÔ PHỎNG / DỰ PHÒNG]: Đang sử dụng mô hình 3D mẫu ({config.DEFAULT_SAMPLE_MODEL_PATH}). "
            f"Chi tiết: {detail}"
        )
    else:
        status_msg = (
            f"Thành công: Đã tạo mô hình 3D từ mô hình TRELLIS trong {total_elapsed:.1f} giây."
        )

    # Cập nhật bảng Metadata (giữ nguyên thông báo chi tiết ở box trên) và giải phóng lớp phủ box 3D (trả về '')
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
            label="Tải mô hình 3D",
        ),
        f"{total_elapsed:.1f}s",  # Ô dưới chỉ hiển thị số giây
        {"success": True, "glb_path": out_glb_path},
    )


def render_model_3d(state: dict | None):
    """Bước 2 (Hàm return thuần túy): Nạp file .glb vào gr.Model3D đúng 1 lần duy nhất."""
    if not state or not state.get("success") or not state.get("glb_path"):
        return (
            None,
            gr.update(),
            gr.update(
                value=None,
                interactive=False,
                variant="secondary",
                label="Chưa có mô hình để tải",
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
            label="Tải mô hình 3D",
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

    # Nạp script ASCII Plasma cục bộ
    ascii_script_path = os.path.join(
        os.path.dirname(__file__), "src", "ui", "assets", "ascii_plasma.js"
    )
    head_parts = []
    # Nạp Favicon trực tiếp dưới dạng Base64 Data URI để chống cache trình duyệt tuyệt đối
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    favicon_ico_path = os.path.join(assets_dir, "favicon.ico")
    favicon_png_path = os.path.join(assets_dir, "favicon-32x32.png")
    
    import base64
    fav_ico_uri = ""
    fav_png_uri = ""
    if os.path.exists(favicon_ico_path):
        with open(favicon_ico_path, "rb") as f:
            fav_ico_uri = f"data:image/x-icon;base64,{base64.b64encode(f.read()).decode('ascii')}"
    if os.path.exists(favicon_png_path):
        with open(favicon_png_path, "rb") as f:
            fav_png_uri = f"data:image/png;base64,{base64.b64encode(f.read()).decode('ascii')}"

    if fav_png_uri:
        head_parts.append(f'<link rel="icon" type="image/png" sizes="32x32" href="{fav_png_uri}">')
    if fav_ico_uri:
        head_parts.append(f'<link rel="icon" type="image/x-icon" href="{fav_ico_uri}">')
        head_parts.append(f'<link rel="shortcut icon" type="image/x-icon" href="{fav_ico_uri}">')

    primary_fav_uri = fav_png_uri or fav_ico_uri
    if primary_fav_uri:
        fav_type = 'image/png' if fav_png_uri else 'image/x-icon'
        head_parts.append(f"""
        <script>
        (() => {{
            const uri = "{primary_fav_uri}";
            const fType = "{fav_type}";
            function applyFavicon() {{
                document.querySelectorAll("link[rel*='icon']").forEach(e => e.remove());
                const link = document.createElement('link');
                link.type = fType;
                link.rel = 'icon';
                link.href = uri;
                document.head.appendChild(link);
            }}
            applyFavicon();
            if (document.readyState === 'loading') {{
                document.addEventListener('DOMContentLoaded', applyFavicon);
            }}
        }})();
        </script>
        """)

    # Tích hợp Animate UI Ripple Button script cho nút Tạo 3D và Nút Tải
    head_parts.append("""
    <script>
    (() => {
        function attachRipple() {
            document.addEventListener('click', (e) => {
                const btn = e.target.closest('.gr-button-primary:not(:disabled), button.primary:not(:disabled), .gr-button-secondary:not(:disabled), button.secondary:not(:disabled), button.upload-container');
                if (!btn) return;
                
                const rect = btn.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height) * 2;
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                const wave = document.createElement('span');
                wave.className = 'ripple-button-wave';
                wave.style.width = size + 'px';
                wave.style.height = size + 'px';
                wave.style.left = x + 'px';
                wave.style.top = y + 'px';
                
                btn.appendChild(wave);
                setTimeout(() => wave.remove(), 600);
            }, true);
        }
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', attachRipple);
        } else {
            attachRipple();
        }
    })();
    </script>
    """)

    if os.path.exists(ascii_script_path):
        with open(ascii_script_path, "r", encoding="utf-8") as f:
            head_parts.append(f"<script>{f.read()}</script>")

    demo.launch(
        theme=create_studio_theme(),
        css=CUSTOM_CSS,
        head="".join(head_parts),
        favicon_path=favicon_ico_path if os.path.exists(favicon_ico_path) else None,
        server_name="127.0.0.1",
        server_port=7860,
        allowed_paths=[
            os.path.abspath(config.DEFAULT_OUTPUT_DIR),
            os.path.abspath(config.DEFAULT_ASSETS_DIR),
            os.path.abspath("."),
        ],
    )
