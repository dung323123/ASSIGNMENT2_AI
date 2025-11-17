# Cấu trúc dự án
ASSIGNMENT2_AI
    data: Chứa data để train ml agent
    models: Chứa kết quả train, ví dụ: File .pkl
    src: Nơi chứa source code
        agents: Nơi định nghĩa 3 agents. Phải kế thừa BaseAgent
        game: Nơi định nghĩa bàn cờ và nước đi
        ui: Xây dựng frontend
        train_ml: file định nghĩa train mô hình
    main.py: chứa ví dụ
    requirements: Thêm các thư viện muốn dùng ở đây

## Note
    Xem kỹ src/game/board
    Khi định nghĩa agent, phải kế thừa BaseAgent; tái định nghĩa và giữ nguyên chữ ký hàm get_move 