from google.cloud import texttospeech

class TextToSpeech:
    def __init__(self):
        # Instantiates a client
        self.client = texttospeech.TextToSpeechClient()

    def synthesize_speech(self, text, filename):
        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request, select the language code ("pt-BR") and the voice name ("pt-BR-Neural2-B")
        voice = texttospeech.VoiceSelectionParams(
            language_code="pt-BR",
            name="pt-BR-Neural2-B"
        )

        # Select the type of audio file you want returned (MP3 format)
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            pitch=-7.2,
            speaking_rate=1.4
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = self.client.synthesize_speech(
            input=synthesis_input, 
            voice=voice, 
            audio_config=audio_config
        )

        # Write the synthesized audio content to the specified file
        with open(f'{filename}.mp3', "wb") as out:
            out.write(response.audio_content)

        return f'{filename}.mp3'
