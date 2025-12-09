# Test

Thay agent_black trong src/ui/main.py bằng AI agent của mình

- Lưu ý:

* Các hàm get_move, make_move cần follow theo định dạng của code gốc nếu cần tự định nghĩa lại
* Thay đổi STEP_DELAY trong src/ui/const.py nếu cần thay đổi tốc độ thay đổi giữa các steps
* Thay đổi MAX_TURNS để tăng/giảm số lượt chơi tối đa

# Tao moi truong ao (neu khong cai thu vien truc tiep duoc)

python3 -m venv venv
source venv/bin/activate
pip install numpy pygame
python3 -m src.ui.main
