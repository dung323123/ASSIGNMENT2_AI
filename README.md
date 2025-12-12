# ASSIGNMENT2_AI

**Project:** Bài Tập Lớn 2 — AI agents cho trờ chơi **Cờ tường**

---

## Mục tiêu

Triển khai 3 agents (Minimax, ML, Random) và giao diện UI để so sánh. Cột mốc chính:

* Minimax (với alpha-beta, heuristic) — chiếm 75% điểm
* Machine Learning (Value network) — chiếm 25% điểm
* Minimax phải thắng Random ≥ 90%
* ML phải thắng Random ≥ 60%

---

## Cấu trúc dự án

```
ASSIGNMENT2_AI
│
│
├── src/                      # Mã nguồn chính
│   ├── agents/               # Các tác tử (Agent)
│   │   ├── base_agent.py     # Lớp Agent cha
│   │   ├── minimax_agent.py  # Agent chơi bằng Minimax
│   │   ├── random_agent.py   # Agent random
│   │   └── ml_agent.py       # Agent dùng mô hình ML (Value Network)
│   │
│   ├── game/                 # Logic trò chơi
│   │
│   ├── ui/                   # Giao diện hiển thị game
│   │
│   └── train_ml.py           # Script huấn luyện mô hình ML
│
├── dataset.csv                  # Dataset huấn luyện 
│
├── generate_dataset.py       # Sinh dataset bằng Minimax vs Minimax
├── play_games.py             # Chạy 100 trận Minimax vs Random
├── play_games_with_ml.py     # Chạy 100 trận MLAgent vs Random
│
├── main.py                   # Demo chạy agent bất kỳ
│
├── value_net.pt              # File model mạng nơ-ron đã train
│
├── requirements.txt          # Danh sách thư viện Python cần cài
│
└── README.md                 # Tài liệu mô tả dự án

```

---

## Yêu cầu trước khi chạy

1. Tạo và kích hoạt virtual environment (khuyến nghị):

* Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

* macOS / Linux:

```bash
python -m venv venv
source venv/bin/activate
```

2. Cài đặt dependencies:

```bash
pip install -r requirements.txt
```

> Nếu bạn thêm package mới: `pip install <package>` rồi cập nhật `requirements.txt` bằng `pip freeze > requirements.txt`.

---

## Các script chính

Dưới đây là các lệnh thường dùng nhất trong quá trình chạy và kiểm thử dự án:

### 🔹 Chạy giao diện chơi game (UI)

```bash
python -m src.ui.main
```

Dùng để demo trực quan, chơi thử giữa người và máy hoặc giữa các agent.

### 🔹 Chạy 100 trận Minimax vs Random

```bash
python play_games.py
```

Dùng để kiểm tra hiệu suất và tỉ lệ thắng của Minimax.

### 🔹 Chạy 100 trận ML vs Random

```bash
python play_games_with_ml.py
```

Kiểm chứng mô hình ML sau khi huấn luyện.

---

## Nếu muốn tạo dataset và huấn luyện lại mô hình

Các bước này **không bắt buộc để chạy UI**, chỉ cần thiết nếu bạn muốn tự train lại mô hình.

### 🔹 Sinh dataset bằng Minimax (tự chơi hoặc đấu chéo)

```bash
python generate_dataset.py
```

Kết quả được lưu trong folder `dataset/`.

### 🔹 Huấn luyện lại mô hình ML

```bash
python src/train_ml.py
```

Model sau khi train sẽ lưu thành `value_net.pt` trong thư mục dự án.

---
