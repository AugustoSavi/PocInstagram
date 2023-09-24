import pytesseract
import cv2

class OcrRetangulo:
    def extract_text(self, image_path, retangulos):
        if len(retangulos) > 0:
            image = cv2.imread(image_path)
            resized = cv2.resize(image, (360, 720), interpolation = cv2.INTER_AREA)
            all_text = ''

            for i, rectangle in enumerate(retangulos):
                cropped = resized[rectangle[0][1]:rectangle[1][1], rectangle[0][0]:rectangle[1][0]]
                text = pytesseract.image_to_string(cropped, lang='por')
                all_text += text

            return all_text
        
        image = cv2.imread(image_path)
        text = pytesseract.image_to_string(image, lang='por')
        return text
