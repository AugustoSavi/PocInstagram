import pytesseract
from PIL import Image

class Ocr:
    def extract_text(self, filePath):
        # Open the image file
        image = Image.open(filePath)

        # Perform text recognition on the image using Tesseract
        text = pytesseract.image_to_string(image, lang='por')

        return text
