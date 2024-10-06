import os
from ocr_processor import OCRProcessor
from qdrant_manager import QdrantManager

def run_cli():
    ocr = OCRProcessor()
    qdrant = QdrantManager()

    while True:
        print("\nChọn một lệnh:")
        print("1. Tạo bộ sưu tập từ ảnh")
        print("2. Tìm văn bản tương tự dựa trên văn bản truy vấn")
        print("3. Tìm văn bản theo từ khóa")
        print("4. Xem toàn bộ nội dung bộ sưu tập")
        print("5. Xóa bộ sưu tập")
        print("6. Thoát")

        choice = input("Nhập lựa chọn của bạn: ")

        if choice == "1":
            folder_path = "img/" + input("Nhập đường dẫn tới thư mục ảnh (ví dụ: folder_2): ")
            if os.path.isdir(folder_path):
                qdrant.create_collection()
                for filename in os.listdir(folder_path):
                    if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                        image_path = os.path.join(folder_path, filename)
                        recognized_text = ocr.process_image(image_path)
                        qdrant.store_text_vector(recognized_text)
                        print(f"Văn bản: '{recognized_text}' đã được lưu.")
                print("Tạo bộ sưu tập từ ảnh thành công!")
            else:
                print(f"Thư mục '{folder_path}' không tồn tại.")

        elif choice == "2":
            print("Lệnh tìm văn bản tương tự. Vui lòng nhập một văn bản để truy vấn (ví dụ: 'Times New Roman').")
            query_text = input("Nhập văn bản truy vấn: ")
            if query_text:
                query_vector = qdrant.vectorize_text(query_text)
                results = qdrant.query_similar_texts(query_vector)
                if results:
                    for result in results:
                        print(f"Văn bản tương tự: {result.payload['text']}, Độ tương đồng: {result.score}")
                else:
                    print("Không tìm thấy văn bản tương tự.")
            else:
                print("Vui lòng nhập văn bản hợp lệ.")

        elif choice == "3":
            print("Lệnh tìm kiếm theo từ khóa. Vui lòng nhập một từ khóa (ví dụ: 'nền').")
            keyword = input("Nhập từ khóa: ")
            if keyword:
                results = qdrant.search_by_keyword(keyword)
                
                # Kiểm tra rõ ràng kiểu dữ liệu của results và kiểm tra kết quả
                if isinstance(results, list) and len(results) > 0:
                    print(f"Kết quả tìm kiếm cho từ khóa '{keyword}':")
                    for result in results:
                        print(f"ID: {result.id}, Văn bản: {result.payload['text']}")
                else:
                    print(f"Không tìm thấy kết quả nào với từ khóa: '{keyword}'")
            else:
                print("Vui lòng nhập từ khóa hợp lệ.")


        elif choice == "4":
            results, _ = qdrant.client.scroll(
                collection_name=qdrant.collection_name,
                limit=100,  # Giới hạn số lượng kết quả muốn lấy
                with_payload=True
            )
            if results:
                print("Nội dung của bộ sưu tập:")
                for result in results:
                    print(f"ID: {result.id}, Văn bản: {result.payload['text']}")
            else:
                print("Không có dữ liệu trong bộ sưu tập.")

        elif choice == "5":
            qdrant.delete_collection()
            print("Bộ sưu tập đã được xóa.")

        elif choice == "6":
            print("Thoát chương trình.")
            break

        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
