import sys

def main():
    print("Chọn cách thức sử dụng chương trình:")
    print("1. Giao diện đồ họa (Tkinter)")
    print("2. Dòng lệnh (Command Line Interface)")
    choice = input("Nhập lựa chọn của bạn (1/2): ")

    if choice == "1":
        # Chạy giao diện Tkinter từ app.py
        import gui_app
        gui_app.run_gui()  # Gọi hàm khởi động giao diện từ app.py

    elif choice == "2":
        # Chạy chương trình từ CLI (dòng lệnh cũ)
        import cli
        cli.run_cli()  # Gọi hàm khởi động CLI từ cli.py

    else:
        print("Lựa chọn không hợp lệ. Vui lòng chọn 1 hoặc 2.")
        sys.exit()

if __name__ == "__main__":
    main()
