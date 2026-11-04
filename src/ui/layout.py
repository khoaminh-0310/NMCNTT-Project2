# src/ui/layout.py
"""UI Layout & HTML Render Helpers for 2D to 3D Web Application (Gradio).

Author duy nhất: Nguyễn Hồng Bảo Trân (MSSV: 26127470) - Giao diện Web (UI/UX).
Team: ae cây khế - Course: CSC00004 - Class: 26C05.
Strictly adheres to Section 4 & 5.1 of 'Tài liệu kỹ thuật project AI' and Cẩm nang UI.
"""

import base64
import html
import os
import gradio as gr

from src.ui.theme import CUSTOM_CSS, create_studio_theme


# =========================================================================
# Vector SVG Icons (Tất cả mang màu Laser Emerald #34d399 đồng bộ icon Clock)
# =========================================================================
SVG_GITHUB = (
    '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">'
    '<path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234'
    'c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 '
    '1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 '
    '0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 '
    '1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 '
    '0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 '
    '0-6.627-5.373-12-12-12z"/>'
    '</svg>'
)

# box.svg chuẩn Lucide đầy đủ lập thể 3 chiều
SVG_BOX_CUSTOM = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" '
    'stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-box">'
    '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>'
    '<polyline points="3.29 7 12 12 20.71 7"/>'
    '<line x1="12" y1="22" x2="12" y2="12"/>'
    '</svg>'
)

# image.svg chuẩn Lucide
SVG_IMAGE_CUSTOM = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" '
    'stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-image">'
    '<rect width="18" height="18" x="3" y="3" rx="2" ry="2"/>'
    '<circle cx="9" cy="9" r="2"/>'
    '<path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>'
    '</svg>'
)

SVG_FILE = (
    '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>'
    '<polyline points="14 2 14 8 20 8"></polyline>'
    '</svg>'
)

SVG_DATABASE = (
    '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">'
    '<ellipse cx="12" cy="5" rx="9" ry="3"></ellipse>'
    '<path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path>'
    '<path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>'
    '</svg>'
)

SVG_CPU = (
    '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">'
    '<rect x="4" y="4" width="16" height="16" rx="2"></rect>'
    '<rect x="9" y="9" width="6" height="6"></rect>'
    '<line x1="9" y1="1" x2="9" y2="4"></line>'
    '<line x1="15" y1="1" x2="15" y2="4"></line>'
    '<line x1="9" y1="20" x2="9" y2="23"></line>'
    '<line x1="15" y1="20" x2="15" y2="23"></line>'
    '<line x1="20" y1="9" x2="23" y2="9"></line>'
    '<line x1="20" y1="15" x2="23" y2="15"></line>'
    '<line x1="1" y1="9" x2="4" y2="9"></line>'
    '<line x1="1" y1="15" x2="4" y2="15"></line>'
    '</svg>'
)

SVG_CLOCK = (
    '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="12" cy="12" r="10"></circle>'
    '<polyline points="12 6 12 12 16 14"></polyline>'
    '</svg>'
)

SVG_INFO = (
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="12" cy="12" r="10"></circle>'
    '<line x1="12" y1="16" x2="12" y2="12"></line>'
    '<line x1="12" y1="8" x2="12.01" y2="8"></line>'
    '</svg>'
)

SVG_ALERT = (
    '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="12" cy="12" r="10"></circle>'
    '<line x1="12" y1="8" x2="12" y2="12"></line>'
    '<line x1="12" y1="16" x2="12.01" y2="16"></line>'
    '</svg>'
)


def render_shimmer_title(text: str) -> str:
    """Sinh mã HTML hiệu ứng Shimmering Text từng chữ cái chuẩn animate-ui.
    Từng ký tự nối tiếp nhau bừng sáng màu Laser Emerald kèm vầng hào quang nhẹ."""
    chars_html = []
    for i, ch in enumerate(text):
        if ch == " ":
            chars_html.append('<span class="shimmer-space">&nbsp;</span>')
        else:
            chars_html.append(f'<span class="shimmer-char" style="--char-idx: {i};">{html.escape(ch)}</span>')
    return f'<span class="studio-title-text">{"".join(chars_html)}</span>'


def render_field_label(svg: str, text: str) -> str:
    """Nhãn trường nhập/xuất đặt NGOÀI box.
    Dùng chung markup với tiêu đề 'Thông số mô hình 3D' (class bento-title)
    để icon và chữ hiển thị giống hệt nhau."""
    return (
        '<div class="field-label">'
        '<div class="bento-title">'
        f'{svg}<span>{html.escape(text)}</span>'
        '</div>'
        '</div>'
    )


def render_status_html(state: str, message: str = "", detail: str = "") -> str:
    """Sinh mã HTML cho lớp phủ trạng thái nằm bên trong khung mô hình 3D."""
    if state == "idle" or not message:
        return ""

    safe_msg = html.escape(message)
    safe_detail = html.escape(detail) if detail else ""
    detail_html = f'<div class="trellis-status-detail">{safe_detail}</div>' if safe_detail else ""

    if state == "error":
        return f"""
        <div class="trellis-status-card trellis-status-error">
            <div style="margin-bottom: 12px;">{SVG_ALERT}</div>
            <div class="trellis-status-title" style="color: #fca5a5;">{safe_msg}</div>
            {detail_html}
        </div>
        """

    return f"""
    <div class="trellis-status-card">
        <div class="scanner-grid">
            <div class="scanner-line"></div>
        </div>
        <div class="trellis-status-title">{safe_msg}</div>
        {detail_html}
    </div>
    """


def render_info_html(
    file_name: str = "-",
    file_size: str = "-",
    engine: str = "-",
    inference_time: str = "-",
    status_msg: str = "Sẵn sàng xử lý. Tải ảnh lên và bấm 'Bắt đầu tạo 3D'.",
    is_mock: bool = False,
) -> str:
    """Sinh mã HTML hiển thị bảng thông số Metadata Bento Card bên dưới khung Preview 3D."""
    safe_name = html.escape(file_name)
    safe_size = html.escape(file_size)
    safe_engine = html.escape(engine)
    safe_time = html.escape(inference_time)
    safe_status = html.escape(status_msg)

    if file_name == "-":
        badge_bg = "rgba(39, 39, 42, 0.7)"
        badge_border = "#3f3f46"
        badge_color = "#a1a1aa"
        badge_text = "Chờ xử lý"
    elif is_mock:
        badge_bg = "rgba(245, 158, 11, 0.15)"
        badge_border = "rgba(245, 158, 11, 0.35)"
        badge_color = "#fbbf24"
        badge_text = "Chế độ Mô phỏng / Dự phòng"
    else:
        badge_bg = "rgba(16, 185, 129, 0.15)"
        badge_border = "rgba(16, 185, 129, 0.35)"
        badge_color = "#34d399"
        badge_text = "AI TRELLIS 2.0 Chính thức"

    return f"""
    <div class="bento-card">
        <div class="bento-header">
            <div class="bento-title">
                {SVG_BOX_CUSTOM}
                <span>Thông số mô hình 3D</span>
            </div>
            <span style="
                background: {badge_bg};
                border: 1px solid {badge_border};
                color: {badge_color};
                padding: 3px 9px;
                border-radius: 999px;
                font-size: 11.5px;
                font-weight: 600;
                letter-spacing: 0.02em;
            ">{badge_text}</span>
        </div>
        <div class="bento-grid">
            <div class="bento-item">
                {SVG_FILE}
                <span>Tên file:</span>
                <strong class="bento-val">{safe_name}</strong>
            </div>
            <div class="bento-item">
                {SVG_DATABASE}
                <span>Dung lượng:</span>
                <strong class="bento-val">{safe_size}</strong>
            </div>
            <div class="bento-item">
                {SVG_CPU}
                <span>Engine:</span>
                <strong class="bento-val">{safe_engine}</strong>
            </div>
            <div class="bento-item">
                {SVG_CLOCK}
                <span>Thời gian:</span>
                <strong class="bento-val" style="color: #34d399;">{safe_time}</strong>
            </div>
        </div>
        <div class="bento-footer">
            <div style="display: flex; align-items: flex-start; gap: 8px;">
                <span style="margin-top: 2px;">{SVG_INFO}</span>
                <span>{safe_status}</span>
            </div>
        </div>
    </div>
    """


def create_ui():
    """Hàm dựng giao diện 2 cột theo đúng Wireframe và Cẩm nang UI."""
    # Nạp trực tiếp mô hình 3D quả khế dưới dạng Base64 Data URI để hiển thị siêu tốc và chống lỗi MIME/CORS
    glb_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "qua_khe_3d_xoay_cheo.glb")
    starfruit_b64_src = ""
    if os.path.exists(glb_path):
        with open(glb_path, "rb") as f:
            starfruit_b64_src = "data:model/gltf-binary;base64," + base64.b64encode(f.read()).decode("ascii")
    else:
        starfruit_b64_src = "/file=assets/qua_khe_3d_xoay_cheo.glb"
    with gr.Blocks(title="Dimensional AI Studio", theme=create_studio_theme(), css=CUSTOM_CSS) as demo:
        # Nền ASCII Plasma chạy ngầm full-screen (-z-10)
        gr.HTML(
            value='<div data-aifx="ascii" data-aifx-colors="#059669,#10b981,#34d399,#a7f3d0" data-aifx-glow="0.75" data-aifx-speed="0.35" class="absolute inset-0 pointer-events-none" aria-hidden="true"></div>',
            elem_id="bg_plasma_wrapper",
        )

        # Thanh Header (Theo đúng Wireframe: Tiêu đề bên trái, Nút GitHub bên phải)
        header_html = f"""
        <div class="studio-header">
            <div class="studio-title-area">
                <div class="studio-title-row">
                    {render_shimmer_title("Dimensional AI Studio")}
                </div>
                <div class="studio-subtitle">
                    <span class="sub-group-prefix">Nhóm ae cây</span>
                    <span class="sub-group-khe">khế</span>
                    <span class="sub-starfruit-3d">
                        <model-viewer
                            src="{starfruit_b64_src}"
                            autoplay
                            animation-name="Spin_Around_Square_Diagonal"
                            disable-zoom
                            disable-pan
                            disable-tap
                            interaction-prompt="none"
                            shadow-intensity="0"
                            exposure="1.15"
                            class="starfruit-model"
                        ></model-viewer>
                    </span>
                </div>
            </div>
            <a href="https://github.com/khoaminh-0310/NMCNTT-Project2" target="_blank" rel="noopener noreferrer" class="github-repo-btn">
                {SVG_GITHUB}
                <span>GitHub Repo</span>
            </a>
        </div>
        """
        gr.HTML(value=header_html)

        # State nội bộ truyền kết quả từ Generator sang hàm nạp Model3D ở Bước 2
        result_state = gr.State(value=None)

        # Bố cục 2 cột bọc Studio Panel cách ly hoàn toàn với background
        with gr.Row():
            # =============================================================
            # CỘT BÊN TRÁI: Khu vực tải ảnh & Nút điều khiển
            # =============================================================
            with gr.Column(scale=1, elem_classes=["studio-panel"]):
                gr.HTML('<div class="panel-title">Đầu vào ảnh 2D</div>')
                gr.HTML(render_field_label(SVG_IMAGE_CUSTOM, "Tải ảnh vật thể lên"))
                image_input = gr.Image(
                    type="filepath",
                    show_label=False,
                )

                # Dòng thông số kỹ thuật hướng dẫn người dùng
                gr.HTML("""
                <div class="input-hints">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
                    <span>Hỗ trợ định dạng: <strong>JPG, PNG, WEBP</strong> • Dung lượng: <strong>≤ 10MB</strong></span>
                </div>
                """)

                btn_generate = gr.Button(
                    "Bắt đầu tạo 3D",
                    variant="primary",
                    size="lg",
                )

            # =============================================================
            # CỘT BÊN PHẢI: Khung Preview 3D, Metadata Bento Card & Actions
            # =============================================================
            with gr.Column(scale=1, elem_classes=["studio-panel"]):
                gr.HTML('<div class="panel-title">Mô hình 3D tương tác</div>')
                gr.HTML(render_field_label(SVG_BOX_CUSTOM, "Không gian xoay 360°"))

                # Khung Preview 3D: model_output giữ nguyên visible=True; lớp phủ Zero-Footprint che trên
                with gr.Column(elem_id="preview_3d_wrapper"):
                    model_output = gr.Model3D(
                        show_label=False,
                    )
                    model_status_box = gr.HTML(
                        value="",
                        elem_id="model_status_overlay",
                    )

                # Ô Metadata Bento Card nằm dưới preview box và trên nút download
                model_info_box = gr.HTML(
                    value=render_info_html(),
                )

                # Nút tải mô hình: ban đầu disabled, sáng màu ngọc lục bảo khi có model
                btn_download = gr.DownloadButton(
                    "Chưa có mô hình để tải",
                    variant="secondary",
                    size="lg",
                    interactive=False,
                )

                # Hộp thông báo hệ thống chuyển thành ô đếm giờ thập phân Monospace tabular-nums duy nhất
                status_box = gr.Textbox(
                    label="Đồng hồ đếm giờ",
                    value="0.0s",
                    interactive=False,
                    elem_id="status_box",
                )

    # Đảm bảo giữ nguyên chính xác 100% Tuple 9 phần tử
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
