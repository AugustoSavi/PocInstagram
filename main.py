import os
import pathlib
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog, Text, Frame, Button, Label

from instagramstoriesdownload import InstagramStoryDownloader
from ocr import Ocr
from ocrcleaning import OcrCleaning
from texttospeech import TextToSpeech
from videocreator import VideoCreator

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
        self.img_paths = []
        self.current_image_index = 0
        self.imagesAndTexts = []
        root.mainloop()

    # Function to create voice over
    def execute(self, filePath, text, img_name):
        textOcr = ocr.extract_text(filePath)
        clearedText = ocrCleaning.process_text(textOcr)
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", clearedText)

        return filePath

    def open_file_dialog(self):
        self.img_paths = filedialog.askopenfilenames(title="Select Image", filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")))
        if self.img_paths:
            self.current_image_index = 0
            self.show_image(self.img_paths[self.current_image_index])

    def show_image(self, img_path):
        img = Image.open(img_path)
        img = img.resize((360, 720), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        self.img_label.configure(image=photo)
        self.img_label.image = photo

    def save_text_to_img(self):
        if self.img_paths:
            img_name = f'{self.voiceoverDir}/{os.path.basename(self.img_paths[self.current_image_index]).split(".")[0]}'
            text = self.text_box.get("1.0", "end-1c")
            self.execute(self.img_paths[self.current_image_index], text, img_name)

    def next_image(self):
        if self.img_paths:
            self.current_image_index += 1
            if self.current_image_index >= len(self.img_paths):
                self.current_image_index = 0
            self.show_image(self.img_paths[self.current_image_index])

    def previous_image(self):
        if self.img_paths:
            self.current_image_index -= 1
            if self.current_image_index < 0:
                self.current_image_index = len(self.img_paths) - 1
            self.show_image(self.img_paths[self.current_image_index])

    def create_video(self):
        video_creator = VideoCreator(self.imagesAndTexts)
        video_creator.create_video("video_final.mp4")

    def salvar_texto(self):
        img_name = f'{self.voiceoverDir}/{os.path.basename(self.img_paths[self.current_image_index]).split(".")[0]}'
        clearedText = self.text_box.get("1.0", "end-1c")
        mp3_path = textToSpeech.synthesize_speech(clearedText, img_name)
        self.imagesAndTexts.append(
            (
                self.img_paths[self.current_image_index],
                mp3_path
            )
        )

    def tela(self):
        self.root.title('Poc Instagram')
        self.root.geometry('800x800')
        self.root.resizable(False, False)

    def frame(self):
        self.frame = Frame(self.root, bg="white")
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def inputs(self):
        self.text_box = Text(self.frame, height=42, width=48)
        self.text_box.place(relx=0.5, rely=0)

    def label(self):
        self.img_label = Label(self.frame)
        self.img_label.place(relx=0.02, rely=0)

    def buttons(self):
        self.open_file_button = Button(self.frame, text="Select Images", fg="white", bg="#263D42",
                                       command=self.open_file_dialog)
        self.open_file_button.place(relx=0.05, rely=0.93, width=110, height=50)

        self.next_button = Button(root, text="Next Image", fg="white", bg="#263D42", command=self.next_image)
        self.next_button.place(relx=0.36, rely=0.93, width=110, height=50)

        self.previous_button = Button(root, text="Previous Image", fg="white", bg="#263D42", command=self.previous_image)
        self.previous_button.place(relx=0.21, rely=0.93, width=110, height=50)

        self.busca_text = Button(root, text="Busca texto", padx=10, pady=5, fg="white", bg="#263D42",
                                  command=self.save_text_to_img)
        self.busca_text.place(relx=0.51, rely=0.93, width=110, height=50)

        self.salvar_text = Button(root, text="Salvar texto", padx=10, pady=5, fg="white", bg="#263D42",
                                  command=self.salvar_texto)
        self.salvar_text.place(relx=0.65, rely=0.93, width=110, height=50)

        self.createVideo = Button(root, text="Create vídeo", padx=10, pady=5, fg="white", bg="#263D42",
                                  command=self.create_video)
        self.createVideo.place(relx=0.80, rely=0.93, width=110, height=50)


Application()
