# app.py
import gradio as gr
from src.ui.layout import create_ui


# --- ĐỊNH NGHĨA KẾT QUẢ GIẢ LẬP (MOCK RESULT) ---
class MockResult:
    def __init__(self, glb_path, is_mock, message):
        self.glb_path = glb_path  # Đường dẫn file mô hình 3D (.glb / .obj)
        self.is_mock = is_mock  # True nếu đang chạy chế độ giả lập
        self.message = message  # Nội dung thông báo


def main_process(img_path):
    """Hàm xử lý chính (sau này bạn sẽ thay bằng AI thật của bạn ở đây)"""
    if not img_path:
        return MockResult(None, True, "Vui lòng tải lên một bức ảnh trước khi tạo!")

    # Ở đây mình dùng một file 3D mẫu có sẵn trên internet để test hiển thị
    sample_3d_model = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/gradio/chess.obj"

    # Đang giả lập (Mock Mode)
    is_mock_mode = True

    if is_mock_mode:
        return MockResult(
            glb_path=sample_3d_model,
            is_mock=True,
            message="Đã tải xong mô hình bằng dữ liệu mẫu cục bộ."
        )
    else:
        return MockResult(
            glb_path=sample_3d_model,
            is_mock=False,
            message="Tạo mô hình thành công từ AI Remote!"
        )


# --- GẮN SỰ KIỆN KHI BẤM NÚT (Theo đúng yêu cầu của bạn) ---
def on_click(img_path):
    result = main_process(img_path)
    if result.is_mock:
        msg = "[CANH BAO MOCK MODE] " + result.message
    else:
        msg = result.message
    return result.glb_path, msg


# --- KHỞI TẠO GIAO DIỆN ---
demo, image_input, btn_generate, model_output, status_box = create_ui()

# Liên kết sự kiện click của nút bấm với hàm on_click
btn_generate.click(
    fn=on_click,
    inputs=[image_input],
    outputs=[model_output, status_box]
)

# Chạy ứng dụng
if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)