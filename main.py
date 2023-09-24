import os
import pathlib
from tkinter import *
from PIL import Image, ImageTk, ImageDraw
from tkinter import filedialog, Text, Frame, Button, Canvas, NW

from instagramstoriesdownload import InstagramStoryDownloader
from ocr import Ocr
from texttospeech import TextToSpeech
from videocreator import VideoCreator
from ocrretangulo import OcrRetangulo

storiesDownload = InstagramStoryDownloader()
storiesDownload.download_stories()

ocr = Ocr()
textToSpeech = TextToSpeech()

class Application():
    def __init__(self):
        self.root = Tk()
        self.tela()
        self.frame()
        self.buttons()
        self.inputs()
        self.voiceoverDir = "{0}/Voiceovers".format(pathlib.Path().resolve())
        self.img_paths = []
        self.current_image_index = 0
        self.imagesAndTexts = []
        self.rect_start_x = None
        self.rect_start_y = None
        self.rect_id = None
        self.rectangles = []
        self.root.mainloop()

    # Function to create voice over
    def execute(self, filePath):
        textOcr = OcrRetangulo().extract_text(filePath, self.rectangles)
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", textOcr)

        return filePath

    def open_file_dialog(self):
        self.img_paths = filedialog.askopenfilenames(title="Select Image", filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")))
        if self.img_paths:
            self.current_image_index = 0
            self.show_image(self.img_paths[self.current_image_index])

    def show_image(self, img_path):
        self.canvas = Canvas(self.root, width=360, height=720)
        self.canvas.place(relx=0, rely=0)

        self.canvas.bind("<Button-1>", self.start_rect)
        self.canvas.bind("<B1-Motion>", self.update_rect)
        self.canvas.bind("<ButtonRelease-1>", self.finish_rect)

        self.img = Image.open(img_path)
        self.img = self.img.resize((360, 720), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, image=self.photo, anchor=NW)

    def save_text_to_img(self):
        if self.img_paths:
            self.execute(self.img_paths[self.current_image_index])

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
        self.rectangles = []
        mp3_filename = f'{self.voiceoverDir}/{os.path.basename(self.img_paths[self.current_image_index]).split(".")[0]}'
        clearedText = self.text_box.get("1.0", "end-1c")
        textToSpeech.synthesize_speech(clearedText, mp3_filename)
        self.imagesAndTexts.append(
            (
                self.img_paths[self.current_image_index],
                f'{mp3_filename}.mp3'
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
    
    def start_rect(self, event):
        self.rect_start_x = event.x
        self.rect_start_y = event.y

    def update_rect(self, event):
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_rectangle(
            self.rect_start_x,
            self.rect_start_y,
            event.x,
            event.y,
            outline="red",
            width=3
        )

    def finish_rect(self, event):
        rectangle = [(self.rect_start_x, self.rect_start_y), (event.x, event.y)]
        self.rectangles.append(tuple(rectangle))
        self.rect_id = None

    def buttons(self):
        self.open_file_button = Button(self.frame, text="Select Images", fg="white", bg="#263D42",
                                       command=self.open_file_dialog)
        self.open_file_button.place(relx=0.05, rely=0.93, width=110, height=50)

        self.next_button = Button(self.root, text="Next Image", fg="white", bg="#263D42", command=self.next_image)
        self.next_button.place(relx=0.36, rely=0.93, width=110, height=50)

        self.previous_button = Button(self.root, text="Previous Image", fg="white", bg="#263D42", command=self.previous_image)
        self.previous_button.place(relx=0.21, rely=0.93, width=110, height=50)

        self.busca_text = Button(self.root, text="Busca texto", padx=10, pady=5, fg="white", bg="#263D42",
                                  command=self.save_text_to_img)
        self.busca_text.place(relx=0.51, rely=0.93, width=110, height=50)

        self.salvar_text = Button(self.root, text="Salvar texto", padx=10, pady=5, fg="white", bg="#263D42",
                                  command=self.salvar_texto)
        self.salvar_text.place(relx=0.65, rely=0.93, width=110, height=50)

        self.createVideo = Button(self.root, text="Create vídeo", padx=10, pady=5, fg="white", bg="#263D42",
                                  command=self.create_video)
        self.createVideo.place(relx=0.80, rely=0.93, width=110, height=50)


Application()
