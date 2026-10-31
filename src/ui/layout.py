# src/ui/layout.py
import gradio as gr


def create_ui():
    """Hàm dựng giao diện 2 cột cho ứng dụng AI 3D Scanner"""
    with gr.Blocks(title="AI 3D Scanner Studio") as demo:
        gr.Markdown("# 🧊 Ứng dụng Quét và Tạo Mô Hình 3D bằng AI")

        # Tạo bố cục 2 cột chính
        with gr.Row():
            # --- CỘT BÊN TRÁI: Khu vực tải ảnh & Nút bấm ---
            with gr.Column(scale=1):
                gr.Markdown("### 📥 Đầu vào")
                image_input = gr.Image(
                    type="filepath",
                    label="Tải ảnh 2D lên"
                )
                btn_generate = gr.Button(
                    "Bắt đầu tạo 3D",
                    variant="primary",
                    size="lg"
                )

            # --- CỘT BÊN PHẢI: Khu vực hiển thị kết quả ---
            with gr.Column(scale=1):
                gr.Markdown("### 👁️ Kết quả")
                model_output = gr.Model3D(
                    label="Mô hình 3D tương tác"
                )
                status_box = gr.Textbox(
                    label="Thông báo hệ thống",
                    interactive=False
                )

    # Trả về các thành phần để file chính (app.py) có thể điều khiển được
    return demo, image_input, btn_generate, model_output, status_box