import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import os
from ocr_processor import OCRProcessor
from qdrant_manager import QdrantManager

def run_gui():
    root = tk.Tk()
    app = OCRQdrantApp(root)
    root.mainloop()

class OCRQdrantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VietOCR-Qdrant App")
        self.ocr = OCRProcessor()
        self.qdrant = QdrantManager()
        self.create_widgets()

    def create_widgets(self):
        # Tạo một Frame để chứa các nút
        button_frame = tk.Frame(self.root, bg="#d1d1d1")
        button_frame.pack(padx=20, pady=20)
        self.root.configure(bg="#d1d1d1")
        
        # Định nghĩa kiểu font và màu sắc
        button_style = {
            "bg": "#525254",  # Màu nền nút
            "fg": "white",    # Màu chữ
            "font": ("Arial", 12, "bold"),  # Font chữ
            "width": 30  # Chiều rộng nút
        }

        # Nút tạo bộ sưu tập từ ảnh
        self.create_btn = tk.Button(button_frame, text="Tạo bộ sưu tập từ ảnh", command=self.create_collection, **button_style)
        self.create_btn.grid(row=0, column=0, padx=10, pady=10)

        # Nút tìm văn bản tương tự
        self.similar_btn = tk.Button(button_frame, text="Tìm văn bản tương tự", command=self.find_similar_text, **button_style)
        self.similar_btn.grid(row=1, column=0, padx=10, pady=10)

        # Nút tìm theo từ khóa
        self.keyword_btn = tk.Button(button_frame, text="Tìm theo từ khóa", command=self.search_by_keyword, **button_style)
        self.keyword_btn.grid(row=2, column=0, padx=10, pady=10)

        # Nút xem toàn bộ nội dung bộ sưu tập
        self.view_btn = tk.Button(button_frame, text="Xem toàn bộ nội dung", command=self.view_collection, **button_style)
        self.view_btn.grid(row=3, column=0, padx=10, pady=10)

        # Nút xóa bộ sưu tập
        self.delete_btn = tk.Button(button_frame, text="Xóa bộ sưu tập", command=self.delete_collection, **button_style)
        self.delete_btn.grid(row=4, column=0, padx=10, pady=10)

        # Nút thoát chương trình
        self.exit_btn = tk.Button(button_frame, text="Thoát", command=self.root.quit, **button_style)
        self.exit_btn.grid(row=5, column=0, padx=10, pady=10)

    def create_collection(self):
        # Người dùng chọn thư mục chứa ảnh
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.qdrant.create_collection()
            for filename in os.listdir(folder_path):
                if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    image_path = os.path.join(folder_path, filename)
                    recognized_text = self.ocr.process_image(image_path)
                    self.qdrant.store_text_vector(recognized_text)
                    print(f"Văn bản: '{recognized_text}' đã được lưu.")
            messagebox.showinfo("Thành công", "Tạo bộ sưu tập từ ảnh thành công!")
        else:
            messagebox.showwarning("Lỗi", "Vui lòng chọn một thư mục hợp lệ.")

    def show_custom_popup(self, title, message):
        # Tạo một cửa sổ mới
        popup = tk.Toplevel(self.root)
        popup.title(title)

        # Tùy chỉnh kích thước cửa sổ
        popup.geometry("400x200")  # Thay đổi kích thước theo nhu cầu

        # Thêm label để hiển thị thông điệp
        label = tk.Label(popup, text=message, wraplength=380)  # wraplength để giới hạn chiều dài dòng
        label.pack(padx=10, pady=10)

        # Nút để đóng cửa sổ
        close_button = tk.Button(popup, text="Đóng", command=popup.destroy)
        close_button.pack(pady=(0, 10))
    
    def find_similar_text(self):
        # Người dùng nhập văn bản truy vấn
        query_text = simpledialog.askstring("Tìm văn bản tương tự", "Nhập văn bản truy vấn:")
        if query_text:
            query_vector = self.qdrant.vectorize_text(query_text)  # Chuyển đổi văn bản thành vector
            results = self.qdrant.query_similar_texts(query_vector)  # Gọi phương thức tìm kiếm

            # Kiểm tra xem có kết quả hay không
            if results:  # Nếu có kết quả
                result_str = "\n".join([f"Văn bản tương tự: {result.payload['text']}, Độ tương đồng: {result.score}" for result in results])
                self.show_custom_popup("Kết quả", result_str)  # Hiển thị popup tùy chỉnh
            else:
                self.show_custom_popup("Kết quả", f"Không tìm thấy văn bản tương tự cho '{query_text}'.")
        else:
            self.show_custom_popup("Lỗi", "Vui lòng nhập văn bản hợp lệ.")

    def search_by_keyword(self):
        # Người dùng nhập từ khóa
        keyword = simpledialog.askstring("Tìm theo từ khóa", "Nhập từ khóa:")
        if keyword:
            results = self.qdrant.search_by_keyword(keyword)

            # Kiểm tra xem có kết quả hay không
            if results:  # Nếu có kết quả
                result_str = "\n".join([f"ID: {result.id}, Văn bản: {result.payload['text']}" for result in results])
                messagebox.showinfo("Kết quả", result_str)
            else:
                messagebox.showinfo("Kết quả", f"Không tìm thấy kết quả nào với từ khóa: '{keyword}'")
        else:
            messagebox.showinfo("Lỗi", "Vui lòng nhập từ khóa hợp lệ.")

    def view_collection(self):
        # Xem toàn bộ nội dung của bộ sưu tập
        results, _ = self.qdrant.client.scroll(
            collection_name=self.qdrant.collection_name,
            limit=100,  # Giới hạn số lượng kết quả muốn lấy
            with_payload=True
        )
        if results:
            result_str = "\n".join([f"ID: {result.id}, Văn bản: {result.payload['text']}" for result in results])
            messagebox.showinfo("Nội dung bộ sưu tập", result_str)
        else:
            messagebox.showinfo("Nội dung bộ sưu tập", "Không có dữ liệu trong bộ sưu tập.")

    def delete_collection(self):
        # Xóa bộ sưu tập
        self.qdrant.delete_collection()
        messagebox.showinfo("Thành công", "Bộ sưu tập đã được xóa.")


# Khởi chạy ứng dụng Tkinter
if __name__ == "__main__":
    root = tk.Tk()
    app = OCRQdrantApp(root)
    root.mainloop()
