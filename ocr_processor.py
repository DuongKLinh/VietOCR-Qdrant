from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from PIL import Image
import matplotlib.pyplot as plt

class OCRProcessor:
    def __init__(self):
        # Configure VietOCR model
        config = Cfg.load_config_from_name('vgg_transformer')
        config['weights'] = 'vgg_transformer.pth'  # Load model weights
        config['device'] = 'cpu'  # or 'cuda' for GPU
        config['predictor']['beamsearch'] = False
        self.model = Predictor(config)

    def process_image(self, image_path):
        # Mở hình ảnh bằng Pillow
        img = Image.open(image_path)
        
        # Hiển thị hình ảnh
        plt.imshow(img)
        plt.pause(2)  # Hiển thị ảnh trong 2 giây rồi tự động đóng cửa sổ
        plt.close()   # Đóng cửa sổ hiển thị ảnh

        # Nhận dạng văn bản bằng VietOCR
        result = self.model.predict(img)
        return result

