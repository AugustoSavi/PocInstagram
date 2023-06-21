from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from moviepy.editor import AudioFileClip, concatenate_videoclips

class VideoCreator:
    def __init__(self, images_and_texts):
        self.images_and_texts = images_and_texts

    def create_video(self, output_file):
        video_clips = []
        for image_file, audio_file in self.images_and_texts:
            # Criar um objeto de clipe de áudio
            audio = AudioFileClip(audio_file)

            # Criar um objeto de clipe de imagem
            image = ImageSequenceClip([image_file], durations=[audio.duration])

            # Definir o áudio para o clipe de imagem
            video = image.set_audio(audio)

            video_clips.append(video)

        # Concatenar os clipes de vídeo
        final_video = concatenate_videoclips(video_clips)

        # Salvar o vídeo resultante
        final_video.write_videofile(output_file, codec="libx264", fps=24)
