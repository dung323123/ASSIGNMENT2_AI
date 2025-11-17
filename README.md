# Cấu trúc dự án
ASSIGNMENT2_AI
* data – dữ liệu để train ML agent
* models – mô hình đã train (.pkl, .pt)
* src – chứa mã nguồn
   * agents – 3 agents kế thừa BaseAgent
   * game – bàn cờ và luật
   * ui – giao diện
   * train_ml.py – huấn luyện mô hình
* main.py – chạy demo
* requirements.txt – thư viện sử dụng


## Note
    Xem kỹ src/game/board
    Khi định nghĩa agent, phải kế thừa BaseAgent; tái định nghĩa và giữ nguyên chữ ký hàm get_move 
