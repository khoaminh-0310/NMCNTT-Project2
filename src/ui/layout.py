# src/ui/layout.py
"""UI Layout & HTML Render Helpers for 2D to 3D Web Application (Gradio).

Author: Nguyễn Hồng Bảo Trân (26127470) - Frontend & UI/UX.
Team: ae cây khế - Course: CSC00004 - Class: 26C05.
"""

import html
import gradio as gr


CUSTOM_CSS = """
/* Khung bọc vùng Preview 3D: giữ nguyên kích thước chuẩn của gr.Model3D */
#preview_3d_wrapper {
    position: relative !important;
    gap: 0 !important;
}

/* Khung gr.HTML làm lớp phủ Zero-Footprint:
   Ép toàn bộ thẻ bao của Gradio hoàn toàn trong suốt và xuyên thấu chuột (pointer-events: none).
   Tuyệt đối KHÔNG dùng display: flex !important hay background trên #model_status_overlay
   để khi value="" thì lớp phủ biến mất 100%, không che khuất WebGL Canvas của Babylon.js. */
#model_status_overlay,
#model_status_overlay > div,
#model_status_overlay .prose,
#model_status_overlay .html-container {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
    min-height: 0 !important;
    pointer-events: none !important;
}

#model_status_overlay {
    position: absolute !important;
    inset: 0 !important;
    z-index: 25 !important;
    overflow: hidden !important;
    pointer-events: none !important;
}

/* Thẻ hiển thị trạng thái bên trong box 3D (chỉ tồn tại trong DOM khi đang xử lý hoặc báo lỗi) */
.trellis-status-card {
    position: absolute;
    top: 36px;
    left: 2px;
    right: 2px;
    bottom: 2px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: rgba(15, 23, 42, 0.86);
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    border-radius: 0 0 8px 8px;
    padding: 24px;
    text-align: center;
    color: #f8fafc;
    pointer-events: none;
    z-index: 30;
}

/* Spinner xoay mượt mà */
@keyframes trellis-spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.trellis-spinner {
    width: 44px;
    height: 44px;
    border: 4px solid rgba(56, 189, 248, 0.25);
    border-top-color: #38bdf8;
    border-radius: 50%;
    animation: trellis-spin 0.85s linear infinite;
    margin-bottom: 14px;
}

.trellis-status-title {
    font-size: 15px;
    font-weight: 600;
    color: #f1f5f9;
    margin-bottom: 6px;
    line-height: 1.4;
}

.trellis-status-detail {
    font-size: 13px;
    color: #94a3b8;
    max-width: 90%;
    line-height: 1.4;
}

.trellis-status-error {
    background: rgba(69, 10, 10, 0.90) !important;
    border: 1px solid rgba(248, 113, 113, 0.4);
}
"""


def render_status_html(state: str, message: str = "", detail: str = "") -> str:
    """Sinh mã HTML cho lớp phủ trạng thái nằm bên trong khung mô hình 3D.

    Khi state == 'idle' hoặc hoàn tất, trả về chuỗi rỗng '' để xóa hoàn toàn
    thẻ .trellis-status-card khỏi DOM, giúp mô hình 3D hiển thị và tương tác bình thường.
    """
    if state == "idle" or not message:
        return ""

    safe_msg = html.escape(message)
    safe_detail = html.escape(detail) if detail else ""
    detail_html = f'<div class="trellis-status-detail">{safe_detail}</div>' if safe_detail else ""

    if state == "error":
        return f"""
        <div class="trellis-status-card trellis-status-error">
            <div style="font-size: 34px; margin-bottom: 10px;">❌</div>
            <div class="trellis-status-title" style="color: #fca5a5;">{safe_msg}</div>
            {detail_html}
        </div>
        """

    return f"""
    <div class="trellis-status-card">
        <div class="trellis-spinner"></div>
        <div class="trellis-status-title">{safe_msg}</div>
        {detail_html}
    </div>
    """


def render_info_html(
    file_name: str = "—",
    file_size: str = "—",
    engine: str = "—",
    inference_time: str = "—",
    status_msg: str = "Chưa có dữ liệu mô hình. Hãy tải ảnh lên và bấm 'Bắt đầu tạo 3D'.",
    is_mock: bool = False,
) -> str:
    """Sinh mã HTML hiển thị bảng thông số Metadata bên dưới khung Preview 3D và trên nút Download."""
    safe_name = html.escape(file_name)
    safe_size = html.escape(file_size)
    safe_engine = html.escape(engine)
    safe_time = html.escape(inference_time)
    safe_status = html.escape(status_msg)

    if file_name == "—":
        badge_bg = "#334155"
        badge_color = "#cbd5e1"
        badge_text = "⏳ Chờ xử lý"
    elif is_mock:
        badge_bg = "rgba(245, 158, 11, 0.18)"
        badge_color = "#fbbf24"
        badge_text = "ℹ️ Chế độ Mô phỏng / Dự phòng"
    else:
        badge_bg = "rgba(16, 185, 129, 0.18)"
        badge_color = "#34d399"
        badge_text = "✅ AI TRELLIS Chính thức"

    return f"""
    <style>{CUSTOM_CSS}</style>
    <div style="
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-radius: 8px;
        padding: 12px 14px;
        background: rgba(30, 41, 59, 0.45);
        font-size: 13.5px;
        line-height: 1.5;
        margin-top: 4px;
        margin-bottom: 4px;
    ">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
            <span style="font-weight: 600; color: #e2e8f0;">📊 Thông số Mô hình 3D (Metadata)</span>
            <span style="
                background: {badge_bg};
                color: {badge_color};
                padding: 2px 8px;
                border-radius: 999px;
                font-size: 12px;
                font-weight: 600;
            ">{badge_text}</span>
        </div>
        <div style="
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 6px 14px;
            color: #cbd5e1;
        ">
            <div><span style="color: #94a3b8;">📄 Tên file:</span> <strong style="color: #f8fafc;">{safe_name}</strong></div>
            <div><span style="color: #94a3b8;">💾 Dung lượng:</span> <strong style="color: #f8fafc;">{safe_size}</strong></div>
            <div><span style="color: #94a3b8;">⚙️ Engine:</span> <strong style="color: #f8fafc;">{safe_engine}</strong></div>
            <div><span style="color: #94a3b8;">⏱️ Thời gian tạo:</span> <strong style="color: #38bdf8;">{safe_time}</strong></div>
        </div>
        <div style="
            margin-top: 8px;
            padding-top: 8px;
            border-top: 1px dashed rgba(148, 163, 184, 0.2);
            color: #94a3b8;
            font-size: 12.5px;
        ">
            💬 {safe_status}
        </div>
    </div>
    """


def create_ui():
    """Hàm dựng giao diện 2 cột cho ứng dụng AI 3D Scanner."""
    with gr.Blocks(title="AI 3D Scanner Studio") as demo:
        gr.Markdown("# 🧊 Ứng dụng Quét và Tạo Mô Hình 3D bằng AI")

        # State nội bộ truyền kết quả từ Generator sang hàm nạp Model3D
        result_state = gr.State(value=None)

        # Tạo bố cục 2 cột chính
        with gr.Row():
            # --- CỘT BÊN TRÁI: Khu vực tải ảnh & Nút bấm ---
            with gr.Column(scale=1):
                gr.Markdown("### 📥 Đầu vào")
                image_input = gr.Image(
                    type="filepath",
                    label="Tải ảnh 2D lên",
                )
                btn_generate = gr.Button(
                    "Bắt đầu tạo 3D",
                    variant="primary",
                    size="lg",
                )

            # --- CỘT BÊN PHẢI: Khu vực hiển thị kết quả ---
            with gr.Column(scale=1):
                gr.Markdown("### 👁️ Kết quả")

                # Khung Preview 3D: model_output luôn giữ visible=True nguyên bản như code gốc
                with gr.Column(elem_id="preview_3d_wrapper"):
                    model_output = gr.Model3D(
                        label="Mô hình 3D tương tác",
                    )
                    model_status_box = gr.HTML(
                        value="",
                        elem_id="model_status_overlay",
                    )

                # Ô Metadata nằm dưới preview box và bên trên nút download
                model_info_box = gr.HTML(
                    value=render_info_html(),
                )

                # Nút tải mô hình: ban đầu mờ (disabled), sáng lên khi có model hoàn chỉnh
                btn_download = gr.DownloadButton(
                    "⏳ Chưa có mô hình để tải",
                    variant="secondary",
                    size="lg",
                    interactive=False,
                )

                # Hộp thông báo hệ thống chuyển thành đồng hồ đếm giờ thập phân (0.0s -> 1.2s -> 24.3s)
                status_box = gr.Textbox(
                    label="⏱️ Đồng hồ đếm giờ & Trạng thái hệ thống",
                    value="0.0s (Sẵn sàng)",
                    interactive=False,
                )

    return (
        demo,
        image_input,
        btn_generate,
        model_output,
        model_status_box,
        model_info_box,
        btn_download,
        status_box,
        result_state,
    )