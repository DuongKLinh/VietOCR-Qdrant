# VietOCR-Qdrant
An application for Vietnamese text recognition using VietOCR, with a vector-based search feature powered by Qdrant.

## How to use
### 1. Install Docker Desktop from [Docker](https://www.docker.com/products/docker-desktop/)
### 2. Create new container
Open terminal and run:
```bash
docker run -p 6333:6333 qdrant/qdrant
```
### 3. Clone project
```bash
git clone https://github.com/DuongKLinh/VietOCR-Qdrant.git
```
### 4. Install dependencies
```bash
pip install -r requirements.txt
```
or
```bash
pip install visitor pillow matplotlib qdrant-client torch torchvision torchaudio tkinter
```
### 5. Install model weights
Go to [vietocr_gettingstart.ipynb](https://colab.research.google.com/github/pbcquoc/vietocr/blob/master/vietocr_gettingstart.ipynb#scrollTo=AwHpqqQEnHv1), install the **vgg_transformer.pth** file from the `config` block.
### 6. Add images to recognize
Replace images in the folder `images` with the ones you want to recognize.
### 7. Start the program
```bash
python main.py
```