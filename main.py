import os
from ocr_processor import OCRProcessor
from qdrant_manager import QdrantManager

class OCRCollection:
    def __init__(self):
        self.ocr = OCRProcessor()
        self.qdrant = QdrantManager()

    def create_collection(self, folder_path):
        # Duyệt qua tất cả các file trong thư mục
        for filename in os.listdir(folder_path):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):  # Chỉ xử lý các file ảnh
                image_path = os.path.join(folder_path, filename)
                print(f"Đang xử lý ảnh: {image_path}")
                
                # Thực hiện OCR trên từng ảnh
                recognized_text = self.ocr.process_image(image_path)
                
                # Lưu văn bản dưới dạng vector trong Qdrant
                vector_id = self.qdrant.store_text_vector(recognized_text)
                print(f"Văn bản: '{recognized_text}' đã được lưu với ID vector: {vector_id}")

    def search_similar(self, query_text):
        # Tìm kiếm văn bản tương tự dựa trên vector của văn bản truy vấn
        query_vector = self.qdrant.vectorize_text(query_text)
        results = self.qdrant.query_similar_texts(query_vector)
        for result in results:
            print(f"Văn bản tương tự: {result['payload']['text']}, Độ tương đồng: {result['score']}")

    def search_by_keyword(self, keyword):
        # Tìm kiếm văn bản dựa trên từ khóa
        results = self.qdrant.search_by_keyword(keyword)
        for result in results:
            print(f"Văn bản: {result['payload']['text']}")

    def delete_collection(self):
        # Xóa bộ sưu tập trong Qdrant
        self.qdrant.delete_collection()
        print("Collection đã được xóa.")

def main():
    ocr_collection = OCRCollection()

    while True:
        try:
            print("\nChọn một lệnh:")
            print("1. Tạo bộ sưu tập từ ảnh")
            print("2. Tìm văn bản tương tự dựa trên văn bản truy vấn")
            print("3. Tìm văn bản theo từ khóa")
            print("4. Xem toàn bộ nội dung bộ sưu tập")
            print("5. Xóa bộ sưu tập")
            print("6. Thoát")

            choice = input("Nhập lựa chọn của bạn: ")

            if choice == "1":
                ocr_collection.qdrant.create_collection()

                folder_path = input("Nhập đường dẫn tới thư mục ảnh (ví dụ: folder_2): ")
                if not os.path.isdir("img/" + folder_path):
                    print(f"Thư mục '{folder_path}' không tồn tại.")
                else:
                    ocr_collection.create_collection("img/" + folder_path)

            elif choice == "2":
                print("Lệnh tìm văn bản tương tự. Vui lòng nhập một văn bản để truy vấn (ví dụ: 'Times New Roman').")
                query_text = input("Nhập văn bản truy vấn: ")
                if not query_text.strip():
                    print("Vui lòng nhập văn bản hợp lệ.")
                else:
                    query_vector = ocr_collection.qdrant.vectorize_text(query_text)
                    ocr_collection.qdrant.query_similar_texts(query_vector)

            elif choice == "3":
                print("Lệnh tìm kiếm theo từ khóa. Vui lòng nhập một từ khóa (ví dụ: 'nền').")
                keyword = input("Nhập từ khóa: ")
                if not keyword.strip():
                    print("Vui lòng nhập từ khóa hợp lệ.")
                else:
                    ocr_collection.qdrant.search_by_keyword(keyword)

            elif choice == "4":
                # Xem toàn bộ nội dung của bộ sưu tập
                ocr_collection.qdrant.view_collection()

            elif choice == "5":
                ocr_collection.qdrant.delete_collection()

            elif choice == "6":
                print("Thoát chương trình.")
                break

            else:
                print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

        except Exception as e:
            print(f"Đã xảy ra lỗi: {e}")


if __name__ == "__main__":
    main()
