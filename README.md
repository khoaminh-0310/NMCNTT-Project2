# Ứng Dụng Web Chuyển Ảnh 2D Thành Mô Hình 3D Bằng AI (TRELLIS.2)

> **Môn học:** Nhập môn Công nghệ Thông tin (CSC00004) – Lớp 26C05  
> **Đơn vị:** Khoa Công nghệ Thông tin, Trường Đại học Khoa học Tự nhiên – ĐHQG-HCM  
> **Nhóm thực hiện:** ae cây khế  
> **Đề tài:** 3D Object Reconstruction from 2D Images using Microsoft TRELLIS.2  

---

## 1. Giới thiệu Đồ Án & Điểm Nổi Bật

### 📌 Giới thiệu tổng quan
Ứng dụng **Dimensional AI Studio** là sản phẩm đồ án ứng dụng AI của nhóm sinh viên năm nhất **ae cây khế**. Ứng dụng hoạt động theo kiến trúc **Wrapper Web App** hiện đại viết bằng Python & Gradio, kết nối trực tiếp với mô hình AI mã nguồn mở tiên tiến của Microsoft: **TRELLIS.2** chạy trên hạ tầng Hugging Face Spaces (ZeroGPU). 

Ứng dụng cho phép người dùng phổ thông dễ dàng biến một bức ảnh chụp vật thể 2D thành mô hình 3D hoàn chỉnh (`.glb`) mà không cần cài đặt môi trường đồ họa phức tạp hay sở hữu phần cứng GPU đắt tiền.

---

## 2. Phân Công Trách Nhiệm Nhóm

| STT | Thành viên | MSSV | Vai trò chính | Phạm vi phụ trách thực tế trong Code |
| :---: | :--- | :---: | :--- | :--- |
| **1** | **Trần Minh Khoa** | **26127229** | **Nhóm trưởng & Điều phối** | - Quản lý Git repository, cấp quyền, duyệt và merge code.<br>- Phụ trách toàn bộ tài liệu dự án: `README.md`, `.gitignore`, `docs/`.<br>- Tổng hợp Slide thuyết trình bảo vệ và Báo cáo đồ án cuối kỳ. |
| **2** | **Lê Bá Thi** | **26127431** | **Kết nối AI & Inference** | - Phụ trách module `src/ai/`: viết [`trellis_client.py`](src/ai/trellis_client.py) kết nối API Hugging Face `microsoft/TRELLIS.2`.<br>- Xây dựng dịch vụ giả lập [`mock_service.py`](src/ai/mock_service.py).<br>- Lập trình cơ chế giám sát hàng đợi ZeroGPU và tự động Fallback sang Mock khi lỗi mạng/hết quota. |
| **3** | **Nguyễn Hồng Bảo Trân** | **26127470** | **Giao diện Web (UI/UX)** | - Phụ trách module `src/ui/`: thiết kế bố cục Bento Grid trong [`layout.py`](src/ui/layout.py) và CSS Studio trong [`theme.py`](src/ui/theme.py).<br>- Tích hợp component `gr.Model3D`, bảng Metadata và hiệu ứng âm thanh Apple Pay trong [`app.py`](app.py).<br>- Xử lý luồng sự kiện 2 bước (Generator Streaming & Render 3D). |
| **4** | **Trịnh Duy Khoa** | **26127230** | **Xử lý Dữ liệu & Hệ thống** | - Phụ trách module `src/core/`: viết bộ kiểm định ảnh đầu vào [`validator.py`](src/core/validator.py) chặn file quá 10MB/sai định dạng.<br>- Viết [`file_manager.py`](src/core/file_manager.py) tạo đường dẫn an toàn chống tấn công Path Traversal.<br>- Thiết lập cấu hình hệ thống [`config.py`](config.py) và hợp đồng dữ liệu chuẩn [`contracts.py`](src/core/contracts.py). |
| **5** | **Phạm Tấn Thành** | **26127427** | **Kiểm thử & Chuẩn bị Demo** | - Phụ trách module `tests/`: viết toàn bộ 24 bài test tự động trong [`test_validator.py`](tests/test_validator.py) và [`test_full_pipeline.py`](tests/test_full_pipeline.py).<br>- Thu thập và chuẩn hóa bộ 10 ảnh chụp đồ vật thực tế trong [`test_dataset/`](test_dataset/).<br>- Chuẩn bị kịch bản thuyết trình demo sản phẩm 3 phút. |

---

## 3. Cấu Trúc Thư Mục Dự Án Thực Tế

```text
NMCNTT-Project2/
│
├── app.py                     # Entry point: Khởi tạo Gradio UI, nạp âm thanh Apple Pay, điều phối luồng 2 bước
├── config.py                  # Nạp động cấu hình từ .env, thiết lập giới hạn 10MB và space TRELLIS.2
├── requirements.txt           # Danh sách thư viện: gradio, gradio_client, pillow, pytest
├── .env.example               # Mẫu cấu hình biến môi trường chuẩn của nhóm
├── .env                       # File cấu hình biến môi trường thực tế (chứa token HF & space ID)
├── .gitignore                 # Chặn venv/, .env, cache và các file đầu ra outputs/ khỏi Git
├── README.md                  # Tài liệu hướng dẫn sử dụng và báo cáo đồ án
│
├── assets/                    # Thư mục tài nguyên tĩnh
│   ├── sample_model.glb       # Mô hình 3D mẫu phục vụ Mock Mode và Demo ngoại tuyến
│   ├── applepay.mp3           # File âm thanh thông báo hoàn tất (Apple Pay chime)
│   ├── favicon.ico            # Favicon định dạng ICO
│   ├── favicon-32x32.png      # Favicon kích thước 32px
│   └── favicon-48x48.png      # Favicon kích thước 48px
│
├── outputs/                   # Thư mục tự động lưu các file 3D .glb sinh ra (có gắn timestamp)
│
├── src/                       # Mã nguồn lõi được phân chia module mạch lạc
│   ├── ai/                    # Module AI & Suy diễn
│   │   ├── trellis_client.py  # Client gọi Space microsoft/TRELLIS.2, theo dõi hàng đợi GPU & auto-fallback
│   │   └── mock_service.py    # Dịch vụ giả lập trả về model mẫu sau 1.5s khi offline
│   │
│   ├── core/                  # Module Core & Xử lý hệ thống
│   │   ├── contracts.py       # Định nghĩa hợp đồng dữ liệu GenerationResult chuẩn hóa duy nhất
│   │   ├── validator.py       # Kiểm tra hợp lệ ảnh đầu vào (kích thước <= 10MB, đuôi JPG/PNG/WEBP)
│   │   └── file_manager.py    # Quản lý lưu trữ outputs, chống Path Traversal và gắn timestamp
│   │
│   └── ui/                    # Module Giao diện người dùng
│       ├── layout.py          # Bố cục Bento Grid 2 cột, Model3D viewer, thanh trạng thái trực quan
│       ├── theme.py           # Dark Studio Theme, shimmering text, ripple wave & glassmorphism CSS
│       └── assets/
│           └── ascii_plasma.js # Hiệu ứng hình nền động ASCII Plasma
│
├── test_dataset/              # Bộ 10 ảnh chụp đồ vật thực tế Unsplash (bàn, ghế, cốc, xe đồ chơi...)
│   └── README.md              # Bảng kê chi tiết bản quyền và tác giả Unsplash
│
└── tests/                     # Tầng Kiểm thử tự động (100% Passed)
    ├── test_validator.py      # Bộ 13 bài test kiểm thử bộ lọc ảnh và quản lý file
    └── test_full_pipeline.py  # Bộ 11 bài test kiểm thử toàn diện từ Core, Dataset đến AI Inference
```

---

## 4. Hướng Dẫn Cài Đặt & Khởi Chạy Nhanh

### Yêu cầu tiên quyết
- Máy tính đã cài đặt **Python 3.10 – 3.13** (Dự án đã kiểm thử hoạt động hoàn hảo trên Python 3.13).
- Kết nối Internet (để cài gói thư viện và kết nối tới máy chủ AI).
- Trình duyệt web hiện đại: Khuyến nghị **Microsoft Edge** hoặc **Google Chrome**.

### Các bước thực hiện:

#### Bước 1: Mở Terminal tại thư mục dự án
```bash
cd NMCNTT-Project2
```

#### Bước 2: Tạo và kích hoạt môi trường ảo (`venv`)
- **Trên Windows (CMD):**
  ```cmd
  python -m venv venv
  venv\Scripts\activate.bat
  ```
- **Trên Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **Trên macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

#### Bước 3: Cài đặt các thư viện cần thiết
```bash
pip install -r requirements.txt
```

#### Bước 4: Thiết lập biến môi trường (`.env`)
Sao chép file `.env.example` thành `.env`:
- Trên Windows: `copy .env.example .env`
- Trên macOS/Linux: `cp .env.example .env`

Kiểm tra nội dung file `.env`:
```ini
HF_TOKEN=                    # Điền token Hugging Face (nếu có, loại Read)
HF_SPACE_ID=microsoft/TRELLIS.2
MOCK_MODE=false              # false: chạy AI thật; true: chạy mô hình mẫu dự phòng
API_TIMEOUT_SECONDS=300      # Thời gian chờ tối đa (5 phút)
```

#### Bước 5: Khởi chạy ứng dụng Web
```bash
python app.py
```
Hoặc chạy trực tiếp qua môi trường ảo mà không cần kích hoạt:
```cmd
venv\Scripts\python.exe app.py
```
Sau đó mở trình duyệt và truy cập:  
👉 **[http://localhost:7860](http://localhost:7860)** hoặc **[http://127.0.0.1:7860](http://127.0.0.1:7860)**

---

## 5. Kiểm Thử Tự Động (Test Suite)

Dự án trang bị bộ kiểm thử tự động toàn diện đạt tỷ lệ **24 / 24 Tests Passed (100%)**:

```bash
pytest tests/ -v
```
*(Hoặc chạy trực tiếp: `.\venv\Scripts\pytest.exe tests/ -v`)*

### Chi tiết các kịch bản kiểm thử:
1. **[`tests/test_validator.py`](tests/test_validator.py) (13 tests):**
   * Kiểm thử định dạng hợp lệ: PNG, JPEG, WEBP.
   * Kiểm thử từ chối định dạng không hỗ trợ: GIF, BMP, TIFF.
   * Chặn file giả mạo đuôi ảnh (file văn bản đổi đuôi `.png`).
   * Chặn file vượt quá dung lượng **10MB**.
   * Chặn tấn công vượt thư mục (Path Traversal `../../etc/passwd`).
   * Kiểm thử hàm tự động tạo thư mục `outputs/` và gắn timestamp.
2. **[`tests/test_full_pipeline.py`](tests/test_full_pipeline.py) (11 tests):**
   * Kiểm thử hợp lệ cho toàn bộ 10 ảnh mẫu trong `test_dataset/`.
   * Kiểm thử luồng Mock Service trả về file GLB hợp lệ.
   * Kiểm thử tính đúng đắn của hợp đồng giao tiếp chuẩn `GenerationResult`.
   * Kiểm thử luồng kết nối thực tế tới `microsoft/TRELLIS.2` và cơ chế tự động Fallback.

---

## 6. Tính Trung Thực Học Thuật & Chế Độ Mock Mode

Theo tiêu chí đánh giá của môn học, ứng dụng cam kết tính trung thực tuyệt đối trong quá trình báo cáo và bảo vệ đồ án:
* **Khi AI chạy thật (`is_mock = False`):** Giao diện hiển thị nhãn màu xanh lá: `✅ AI TRELLIS 2.0 (microsoft/TRELLIS.2)` cùng thời gian xử lý thực tế từ GPU máy chủ.
* **Khi ở chế độ Mock (`is_mock = True`):** Giao diện tự động hiển thị nhãn cảnh báo rõ ràng: `ℹ️ Chế độ Mô phỏng / Dự phòng` và thông báo nguồn gốc:
  *`[CHẾ ĐỘ MÔ PHỎNG / DỰ PHÒNG]: Đang sử dụng mô hình 3D mẫu (assets/sample_model.glb) do hệ thống đang bật chế độ dự phòng hoặc máy chủ AI bận/hết quota ZeroGPU.`*
