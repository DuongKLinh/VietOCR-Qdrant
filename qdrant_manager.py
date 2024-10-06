from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class QdrantManager:
    def __init__(self):
        self.client = QdrantClient(host="localhost", port=6333)
        self.collection_name = "text_vectors"  # Định nghĩa tên collection ở đây
        self.vectorizer = TfidfVectorizer()

    def create_collection(self):
        try:
            # Kiểm tra nếu collection đã tồn tại
            self.client.get_collection(self.collection_name)
            print(f"Collection '{self.collection_name}' đã tồn tại.")
        except:
            # Tạo collection mới nếu chưa tồn tại
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=300, distance=Distance.COSINE),
            )
            print(f"Collection '{self.collection_name}' đã được tạo.")


    def store_text_vector(self, text):
        # Chuyển đổi văn bản thành vector
        vector = self.vectorize_text(text)
        
        # Lưu vào Qdrant
        response = self.client.upsert(
            collection_name=self.collection_name,
            points=[{
                "id": np.random.randint(1, 1000000),
                "vector": vector.tolist(),
                "payload": {"text": text}
            }]
        )
        return response

    def vectorize_text(self, text):
        # Chuyển đổi văn bản thành vector
        vector = self.vectorizer.fit_transform([text]).toarray()[0]
        
        # Đảm bảo vector có kích thước chính xác (300 phần tử)
        if len(vector) < 300:
            vector = np.pad(vector, (0, 300 - len(vector)), 'constant')
        elif len(vector) > 300:
            vector = vector[:300]
        
        return vector

    def search_by_keyword(self, keyword):
        try:
            # Lấy toàn bộ nội dung từ collection để tìm kiếm theo từ khóa
            results, _ = self.client.scroll(
                collection_name=self.collection_name,
                limit=100,  # Giới hạn số lượng kết quả muốn lấy
                with_payload=True
            )

            # Lọc kết quả dựa trên từ khóa
            found_results = [result for result in results if keyword.lower() in result.payload['text'].lower()]

            # Trả về danh sách kết quả thay vì in trực tiếp
            return found_results  # Trả về danh sách tìm thấy

        except Exception as e:
            print(f"Đã xảy ra lỗi trong quá trình tìm kiếm theo từ khóa: {e}")
            return []  # Trả về danh sách rỗng nếu có lỗi

    def query_similar_texts(self, query_vector):
        try:
            # Truy vấn các vector tương tự trong Qdrant
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector.tolist(),
                limit=5
            )

            # Trả về danh sách các kết quả
            return results  # Trả về danh sách các kết quả

        except Exception as e:
            print(f"Đã xảy ra lỗi trong quá trình tìm kiếm văn bản tương tự: {e}")
            return []  # Trả về danh sách rỗng nếu có lỗi


    def view_collection(self):
        try:
            # Lấy toàn bộ nội dung từ collection
            results, _ = self.client.scroll(
                collection_name=self.collection_name,
                limit=100,  # Số lượng kết quả muốn lấy (có thể thay đổi)
                with_payload=True
            )

            # Kiểm tra xem collection có dữ liệu hay không
            if not results:
                print(f"Collection '{self.collection_name}' không có dữ liệu.")
            else:
                print(f"Nội dung của collection '{self.collection_name}':")
                for result in results:
                    print(f"ID: {result.id}, Văn bản: {result.payload['text']}")
        
        except Exception as e:
            print(f"Đã xảy ra lỗi khi xem nội dung collection: {e}")
    
    def delete_collection(self):
        try:
            # Xóa collection
            self.client.delete_collection(collection_name=self.collection_name)
            print(f"Collection '{self.collection_name}' đã được xóa.")
        except Exception as e:
            print(f"Đã xảy ra lỗi trong quá trình xóa collection: {e}")
