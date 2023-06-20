import os
import pathlib
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog, Text, Frame, Button, Label

from instagramstoriesdownload import InstagramStoryDownloader
from ocr import Ocr
from ocrcleaning import OcrCleaning
from texttospeech import TextToSpeech


storiesDownload = InstagramStoryDownloader()
storiesDownload.download_stories()

ocr = Ocr()
ocrCleaning = OcrCleaning()
textToSpeech = TextToSpeech()

root = Tk()

class Application():
    
    def __init__(self):
        self.root = root
        self.tela()
        self.frame()
        self.buttons()
        self.inputs()
        self.label()
        self.voiceoverDir = "{0}/Voiceovers".format(pathlib.Path().resolve())
        root.mainloop()


    # Function to create voice over
    def execute(self, filePath, text, img_name):
        text = ocr.extract_text(filePath)
        clearedText = ocrCleaning.process_text(text)
        textToSpeech.synthesize_speech(clearedText, img_name)
        return filePath

    def open_file_dialog(self):
        global img_paths
        img_paths = filedialog.askopenfilenames(title="Select Image", filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")))
        self.show_image(img_paths[0])

    def show_image(self, img_path):
        # global img_label
        img = Image.open(img_path)
        img = img.resize((360, 720), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        self.img_label.configure(image=photo)
        self.img_label.image = photo

    def save_text_to_img(self):
        img_name = f'{self.voiceoverDir}/{os.path.basename(img_paths[0]).split(".")[0]}'
        text = self.text_box.get("1.0", "end-1c")
        self.execute(img_paths[0], text, img_name)

    def next_image(self):
        global img_paths
        if img_paths:
            img_paths = img_paths[1:]
            if img_paths:
                self.show_image(img_paths[0])

    def tela(self):
        self.root.title('Poc Instagram')
        self.root.geometry('800x800')
        self.root.resizable(False,False)

    def frame(self):
        self.frame = Frame(self.root, bg="white")
        self.frame.place(relx = 0 , rely = 0,relwidth = 1, relheight = 1)

    def inputs(self):
        self.text_box = Text(self.frame, height=42, width=48,)
        self.text_box.place(relx = 0.5, rely = 0)

    def label(self):
        self.img_label = Label(self.frame)
        self.img_label.place(relx = 0.02, rely = 0)

    def buttons(self):
        self.open_file_button = Button(self.frame, text="Select Images", fg="white", bg="#263D42", command=self.open_file_dialog)
        self.open_file_button.place ( relx = 0.05, rely = 0.93, width = 110, height = 50)

        self.next_button = Button(root, text="Next Image", fg="white", bg="#263D42", command=self.next_image)
        self.next_button.place ( relx = 0.36, rely = 0.93, width = 110, height = 50)

        self.save_button = Button(root, text="Save tts", padx=10, pady=5, fg="white", bg="#263D42", command=self.save_text_to_img)
        self.save_button.place ( relx = 0.67, rely = 0.93, width = 110, height = 50)


Application()