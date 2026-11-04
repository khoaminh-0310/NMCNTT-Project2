# src/ui/theme.py
"""Dimensional AI Studio Theme & CSS Configuration for 2D to 3D Application.

Author duy nhất: Nguyễn Hồng Bảo Trân (MSSV: 26127470) - Giao diện Web (UI/UX).
Team: ae cây khế - Course: CSC00004 - Class: 26C05.
Strictly adheres to Section 4 & 5.1 of 'Tài liệu kỹ thuật project AI' and Cẩm nang UI.
"""

import gradio as gr
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts


def create_studio_theme() -> Base:
    """Khởi tạo theme Dimensional AI Studio kế thừa từ gr.themes.Base."""
    theme = Base(
        primary_hue=colors.emerald,
        secondary_hue=colors.zinc,
        neutral_hue=colors.zinc,
        font=[
            fonts.GoogleFont("Inter"),
            fonts.GoogleFont("Plus Jakarta Sans"),
            "system-ui",
            "-apple-system",
            "sans-serif",
        ],
        font_mono=[
            fonts.GoogleFont("JetBrains Mono"),
            fonts.GoogleFont("Fira Code"),
            "ui-monospace",
            "monospace",
        ],
    ).set(
        body_background_fill="#0d0e12",
        body_background_fill_dark="#0d0e12",
        block_background_fill="#121215",
        block_background_fill_dark="#121215",
        panel_background_fill="#121215",
        panel_background_fill_dark="#121215",
        body_text_color="#fafafa",
        body_text_color_dark="#fafafa",
        body_text_color_subdued="#a1a1aa",
        body_text_color_subdued_dark="#a1a1aa",
        block_label_text_color="#e4e4e7",
        block_label_text_color_dark="#e4e4e7",
        block_title_text_color="#fafafa",
        block_title_text_color_dark="#fafafa",
        border_color_primary="#27272a",
        border_color_primary_dark="#27272a",
        block_border_color="#27272a",
        block_border_color_dark="#27272a",
        block_border_width="1px",
        block_radius="8px",
        button_primary_background_fill="#10b981",
        button_primary_background_fill_dark="#10b981",
        button_primary_background_fill_hover="#34d399",
        button_primary_background_fill_hover_dark="#34d399",
        button_primary_text_color="#09090b",
        button_primary_text_color_dark="#09090b",
        button_primary_border_color="#10b981",
        button_primary_border_color_dark="#10b981",
        button_secondary_background_fill="#18181b",
        button_secondary_background_fill_dark="#18181b",
        button_secondary_background_fill_hover="#27272a",
        button_secondary_background_fill_hover_dark="#27272a",
        button_secondary_text_color="#fafafa",
        button_secondary_text_color_dark="#fafafa",
        button_secondary_border_color="#27272a",
        button_secondary_border_color_dark="#27272a",
        input_background_fill="#18181b",
        input_background_fill_dark="#18181b",
        input_border_color="#27272a",
        input_border_color_dark="#27272a",
        input_border_color_focus="#10b981",
        input_border_color_focus_dark="#10b981",
    )
    return theme


CUSTOM_CSS = """
/* =========================================================================
   1. ISOLATION & CANVAS BACKGROUND (LiDAR Studio Ambient Backdrop)
   ========================================================================= */
body {
    background-color: #0d0e12 !important;
    margin: 0 !important;
    padding: 0 !important;
}

.gradio-container {
    position: relative !important;
    isolation: isolate !important;
    background-color: transparent !important;
    background-image: none !important;
    color: #fafafa !important;
    min-height: 100vh !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
}

/* Vùng chứa nền ASCII Plasma chạy ngầm full-screen (opacity 0.52 sáng và sống động) */
#bg_plasma_wrapper {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    z-index: 0 !important;
    opacity: 0.52 !important;
    pointer-events: none !important;
    overflow: hidden !important;
    border: none !important;
    margin: 0 !important;
    padding: 0 !important;
    background: transparent !important;
}

#bg_plasma_wrapper > div,
#bg_plasma_wrapper .prose,
#bg_plasma_wrapper .html-container,
[data-aifx="ascii"] {
    position: absolute !important;
    inset: 0 !important;
    width: 100% !important;
    height: 100% !important;
    pointer-events: none !important;
    overflow: hidden !important;
    display: block !important;
}

/* =========================================================================
   2. HEADER & GITHUB BUTTON
   ========================================================================= */
.studio-header {
    position: relative !important;
    z-index: 1 !important;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 20px;
    background: rgba(18, 18, 22, 0.72) !important;
    backdrop-filter: blur(20px) saturate(140%) !important;
    -webkit-backdrop-filter: blur(20px) saturate(140%) !important;
    border: 1px solid rgba(255, 255, 255, 0.10) !important;
    border-radius: 12px;
    margin-bottom: 16px;
}

.studio-title-area {
    display: flex;
    flex-direction: column;
    gap: 3px;
}

.studio-title-row {
    display: flex;
    align-items: center;
    gap: 10px;
}

/* Tiêu đề chính Dimensional AI Studio - Chuẩn Animate UI Shimmering Text */
.studio-title-text {
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -0.03em;
    display: inline-flex;
    align-items: center;
    color: #fafafa;
    line-height: 1.2;
}

.shimmer-char {
    display: inline-block;
    color: #fafafa;
    animation: animateUiShimmer 2.4s ease-in-out infinite;
    animation-delay: calc(var(--char-idx) * 0.08s);
    will-change: color, text-shadow;
}

.shimmer-space {
    display: inline-block;
    width: 0.28em;
}

@keyframes animateUiShimmer {
    0%, 100% {
        color: #fafafa;
        text-shadow: none;
    }
    35% {
        color: #34d399;
        text-shadow: 0 0 6px rgba(52, 211, 153, 0.45);
    }
    70% {
        color: #fafafa;
        text-shadow: none;
    }
}

@media (prefers-reduced-motion: reduce) {
    .shimmer-char {
        animation: none !important;
        color: #fafafa !important;
        text-shadow: none !important;
    }
}

.studio-badge-model {
    font-size: 11px;
    font-weight: 600;
    padding: 2px 7px;
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.35);
    color: #34d399;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.studio-subtitle {
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px;
    font-size: 17px;
    font-weight: 600;
    line-height: 1 !important;
    letter-spacing: 0.01em;
}

.sub-group-prefix {
    color: #8B5CF6 !important;
    font-weight: 600;
}

.sub-group-khe {
    color: #F9CF07 !important;
    font-weight: 700;
    text-shadow: 0 0 10px rgba(249, 207, 7, 0.45);
}

.sub-starfruit-3d {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 34px;
    height: 34px;
    line-height: 1;
    margin-left: 2px;
}

.sub-starfruit-3d model-viewer {
    width: 34px;
    height: 34px;
    min-width: 34px;
    min-height: 34px;
    background-color: transparent !important;
    --poster-color: transparent !important;
    outline: none !important;
    border: none !important;
    display: block;
    transform: scaleX(-1);
}

.github-repo-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 7px 14px;
    background: #18181b;
    border: 1px solid #27272a;
    border-radius: 6px;
    color: #e4e4e7;
    font-size: 13px;
    font-weight: 500;
    text-decoration: none !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.github-repo-btn:hover {
    background: #27272a;
    color: #ffffff;
    border-color: #3f3f46;
    box-shadow: 0 0 10px rgba(16, 185, 129, 0.15);
}

.github-repo-btn svg {
    fill: currentColor !important;
    stroke: none !important;
}

/* =========================================================================
   3. STUDIO BENTO PANELS (Frosted Glass trong suốt 0.72)
   ========================================================================= */
.studio-panel {
    position: relative !important;
    z-index: 1 !important;
    background: rgba(18, 18, 22, 0.72) !important;
    backdrop-filter: blur(20px) saturate(140%) !important;
    -webkit-backdrop-filter: blur(20px) saturate(140%) !important;
    border: 1px solid rgba(255, 255, 255, 0.10) !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

.panel-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 15px;
    font-weight: 700;
    color: #fafafa;
    margin-bottom: 12px;
    letter-spacing: -0.01em;
}

.field-label {
    margin-bottom: -4px;
}

/* =========================================================================
   4. CĂN CHỈNH THẲNG HÀNG TRỤC NGANG TUYỆT ĐỐI (PIXEL-PERFECT)
   ========================================================================= */
.bento-title,
.panel-title {
    display: inline-flex !important;
    align-items: center !important;
    gap: 7px !important;
}

.bento-title > span,
.panel-title > span {
    display: inline-flex !important;
    align-items: center !important;
    line-height: 1 !important;
}

.bento-title svg {
    display: inline-block !important;
    vertical-align: middle !important;
    margin-top: -2.5px !important;
    margin-right: 2px !important;
    stroke: #34d399 !important;
    color: #34d399 !important;
}

/* =========================================================================
   5. ZERO-FOOTPRINT 3D OVERLAY
   ========================================================================= */
#preview_3d_wrapper {
    position: relative !important;
    gap: 0 !important;
}

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

.trellis-status-card {
    position: absolute;
    top: 2px;
    left: 2px;
    right: 2px;
    bottom: 2px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: rgba(9, 9, 11, 0.92);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 8px;
    padding: 24px;
    text-align: center;
    color: #fafafa;
    pointer-events: none;
    z-index: 30;
    border: 1px solid rgba(16, 185, 129, 0.25);
}

.trellis-status-error {
    background: rgba(28, 10, 10, 0.94) !important;
    border: 1px solid rgba(239, 68, 68, 0.4) !important;
}

/* =========================================================================
   6. ANIMATION 3D LASER SCANNER GRID
   ========================================================================= */
.scanner-grid {
    position: relative;
    width: 68px;
    height: 68px;
    border: 1px solid rgba(16, 185, 129, 0.4);
    border-radius: 8px;
    background: radial-gradient(circle, rgba(16, 185, 129, 0.12) 0%, rgba(9, 9, 11, 0.7) 100%);
    margin-bottom: 16px;
    overflow: hidden;
    box-shadow: 0 0 16px rgba(16, 185, 129, 0.15);
}

.scanner-grid::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image: 
        linear-gradient(to right, rgba(16, 185, 129, 0.18) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(16, 185, 129, 0.18) 1px, transparent 1px);
    background-size: 10px 10px;
}

.scanner-line {
    position: absolute;
    left: 0;
    right: 0;
    height: 2px;
    background: #10b981;
    box-shadow: 0 0 10px #10b981, 0 0 4px #34d399;
    animation: laserSweep 1.6s cubic-bezier(0.22, 1, 0.36, 1) infinite alternate;
}

@keyframes laserSweep {
    0% {
        top: 2px;
        opacity: 0.35;
    }
    50% {
        opacity: 1;
    }
    100% {
        top: calc(100% - 4px);
        opacity: 0.35;
    }
}

.trellis-status-title {
    font-size: 15px;
    font-weight: 600;
    color: #f4f4f5;
    margin-bottom: 6px;
    line-height: 1.4;
}

.trellis-status-detail {
    font-size: 13px;
    color: #a1a1aa;
    max-width: 90%;
    line-height: 1.4;
}

/* =========================================================================
   7. METADATA BENTO CARD & ICON MÀU XANH #34d399
   ========================================================================= */
.bento-card {
    border: 1px solid rgba(255, 255, 255, 0.10) !important;
    border-radius: 8px;
    padding: 14px 16px;
    background: rgba(18, 18, 22, 0.72) !important;
    backdrop-filter: blur(20px) saturate(140%) !important;
    -webkit-backdrop-filter: blur(20px) saturate(140%) !important;
    margin-top: 6px;
    margin-bottom: 6px;
}

.bento-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
    padding-bottom: 10px;
    border-bottom: 1px solid #27272a;
}

.bento-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13.5px;
    font-weight: 600;
    color: #e4e4e7;
}

.bento-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px 18px;
    font-size: 13px;
}

.bento-item {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #a1a1aa;
}

.bento-val {
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    font-variant-numeric: tabular-nums;
    color: #fafafa;
    font-weight: 500;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.bento-footer {
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px solid rgba(39, 39, 42, 0.7);
    color: #a1a1aa;
    font-size: 12.5px;
    line-height: 1.45;
}

/* Màu xanh Laser Emerald #34d399 đồng bộ cho toàn bộ Icon */
.bento-card svg,
.bento-title svg,
.panel-title svg {
    stroke: #34d399 !important;
    color: #34d399 !important;
}

/* Nổi bật nút disabled Chưa có mô hình để tải */
button:disabled,
.gr-button-secondary:disabled {
    background: #18181b !important;
    border: 1px solid #3f3f46 !important;
    color: #e4e4e7 !important;
    opacity: 0.90 !important;
    font-weight: 500 !important;
    cursor: not-allowed !important;
}

/* Chống giật số cho đồng hồ timer tại status_box */
#status_box textarea,
#status_box input {
    font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
    font-variant-numeric: tabular-nums !important;
    color: #34d399 !important;
    background: #121215 !important;
    border-color: #27272a !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

/* Hướng dẫn đầu vào dưới nút tạo ảnh */
.input-hints {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: #a1a1aa;
    margin-top: 6px;
    margin-bottom: 6px;
}

/* =========================================================================
   8. ANIMATE UI RIPPLE BUTTON & HOVER STYLES
   ========================================================================= */
/* Nút bắt đầu tạo 3D & Nút tải mô hình 3D khi đã kích hoạt */
.gr-button-primary:not(:disabled),
button.primary:not(:disabled),
.gr-button-secondary:not(:disabled),
button.secondary:not(:disabled) {
    position: relative !important;
    overflow: hidden !important;
    transition: transform 0.18s cubic-bezier(0.16, 1, 0.3, 1), 
                box-shadow 0.18s cubic-bezier(0.16, 1, 0.3, 1), 
                background-color 0.18s ease, 
                border-color 0.18s ease !important;
}

.gr-button-primary:not(:disabled):hover,
button.primary:not(:disabled):hover {
    background-color: #34d399 !important;
    transform: translateY(-1.5px) scale(1.01) !important;
    box-shadow: 0 6px 18px rgba(16, 185, 129, 0.35), 0 0 10px rgba(52, 211, 153, 0.25) !important;
}

.gr-button-secondary:not(:disabled):hover,
button.secondary:not(:disabled):hover {
    background-color: #27272a !important;
    border-color: #3f3f46 !important;
    transform: translateY(-1.5px) scale(1.01) !important;
    box-shadow: 0 6px 18px rgba(16, 185, 129, 0.25), 0 0 8px rgba(52, 211, 153, 0.18) !important;
}

/* Hiệu ứng nén nhả chuột (Spring Tap) chuẩn animate-ui (tapScale: 0.97) */
.gr-button-primary:not(:disabled):active,
button.primary:not(:disabled):active,
.gr-button-secondary:not(:disabled):active,
button.secondary:not(:disabled):active {
    transform: scale(0.97) !important;
    transition: transform 0.08s ease !important;
}

/* Sóng loang tròn Ripple Wave khi click */
.ripple-button-wave {
    position: absolute;
    border-radius: 50%;
    transform: scale(0);
    animation: rippleExpand 0.6s cubic-bezier(0.1, 0.8, 0.3, 1) forwards;
    background-color: rgba(255, 255, 255, 0.32);
    pointer-events: none;
    z-index: 10;
}

@keyframes rippleExpand {
    0% {
        transform: scale(0);
        opacity: 0.55;
    }
    100% {
        transform: scale(2.8);
        opacity: 0;
    }
}

/* Hover & Ripple cho vùng/nút upload ảnh 2D */
.image-container,
[data-testid="image"],
button.upload-container {
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    position: relative !important;
    overflow: hidden !important;
}

.image-container:hover,
[data-testid="image"]:hover,
button.upload-container:hover {
    border-color: #34d399 !important;
    background-color: rgba(16, 185, 129, 0.04) !important;
    box-shadow: 0 0 16px rgba(16, 185, 129, 0.18) !important;
}

button.upload-container:hover span,
button.upload-container:hover svg {
    color: #34d399 !important;
    stroke: #34d399 !important;
}
"""
