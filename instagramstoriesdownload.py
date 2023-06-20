import os
import instaloader
from datetime import datetime
from dotenv import load_dotenv

class InstagramStoryDownloader:
    def __init__(self):
        # Carregar as variáveis do arquivo .env
        load_dotenv()
        self.INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
        self.INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')
        self.TARGET_USERNAME = os.getenv('TARGET_USERNAME') # Usuário cujos stories serão baixados
        
        # Configuração do Instaloader
        self.L = instaloader.Instaloader()
        
    def download_stories(self):
        # Login
        self.L.load_session_from_file(self.INSTAGRAM_USERNAME)  # Carregar a sessão salva em 'seu_usuario'
        
        # Obter o perfil do usuário alvo
        profile = instaloader.Profile.from_username(self.L.context, self.TARGET_USERNAME)
        
        # Baixar todos os stories
        for story in self.L.get_stories(userids=[profile.userid]):
            for item in story.get_items():
                # Criar o diretório da data se não existir
                directory = '{}/{}'.format(self.TARGET_USERNAME, item.date_local.strftime("%Y-%m-%d"))
                if not os.path.exists(directory):
                    os.makedirs(directory)
                    
                # Definir o nome do arquivo para baixar
                filename = '{}/{}_{}_{}'.format(directory, item.date_local.strftime("%H%M%S"), self.TARGET_USERNAME, item.mediaid)
                
                # Baixar o item do story
                self.L.download_pic(filename, item.url, datetime.now())
