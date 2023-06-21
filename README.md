<h1 align="center">Poc instagram</h1>

https://instaloader.github.io/basic-usage.html

https://us-central1-texttospeech.googleapis.com/v1beta1/text:synthesize

## Instalação

Certifique-se de ter o Python e o pip instalados em seu sistema.

1. Clone o repositório:

```
git clone https://github.com/AugustoSavi/PocInstagram.git
```

2. Acesse o diretório do projeto:

```
cd PocInstagram
```

3. Instale as dependências:

```
pip install -r requirements.txt
```

## Configuração

Antes de iniciar a aplicação, é necessário configurar as variáveis de ambiente no arquivo `.env`. Siga as etapas abaixo:

1. Faça uma cópia do arquivo `.env-example` e renomeie-o para `.env`:

```
cp .env-example .env
```

2. Abra o arquivo `.env` em um editor de texto e preencha as variáveis de ambiente necessárias com os valores apropriados.

Exemplo:

```
API_KEY=your-api-key
SECRET_KEY=your-secret-key
```

Certifique-se de substituir `your-api-key`, `your-secret-key` e outros valores pelas suas próprias informações.

## Uso

Execute o seguinte comando para iniciar a aplicação:

```
python main.py
```


## Contribuição

Sinta-se à vontade para contribuir com melhorias para o projeto. Você pode abrir problemas ou enviar pull requests.

## Licença

[MIT](LICENSE)
