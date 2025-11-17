# Cấu trúc dự án
ASSIGNMENT2_AI <br>
    data: Chứa data để train ml agent <br>
    models: Chứa kết quả train, ví dụ: File .pkl <br>
    src: Nơi chứa source code <br>
        agents: Nơi định nghĩa 3 agents. Phải kế thừa BaseAgent <br>
        game: Nơi định nghĩa bàn cờ và nước đi <br>
        ui: Xây dựng frontend <br>
        train_ml: file định nghĩa train mô hình <br>
    main.py: chứa ví dụ <br>
    requirements: Thêm các thư viện muốn dùng ở đây <br>

## Note
    Xem kỹ src/game/board
    Khi định nghĩa agent, phải kế thừa BaseAgent; tái định nghĩa và giữ nguyên chữ ký hàm get_move 
