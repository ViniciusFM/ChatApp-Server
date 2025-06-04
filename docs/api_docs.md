# Documentação da API (see in [🇺🇸](api_docs_en_us.md))

Esta é a Documentação da API do ChatApp Server

# Rotas de Páginas

Rotas que retornam páginas HTML.

## Index

Exibe uma página "sobre".

```plain
Métodos:
    GET
Rota:
    /
Saída:
    HTML
```

### Saída

```plain
* retorna uma página HTML contendo uma página sobre o servidor.
```

## Channel Invitation

Exibe uma página que redireciona para um URI `chatapp://`, acionando um App Intent específico no Android. Antes do redirecionamento, o serviço tenta recuperar um Canal existente e retorna erro 404 se nenhum for encontrado. O acesso a esta rota é protegido por verificação CAPTCHA.

```plain
Métodos:
    GET, POST
Rota:
    /invite/<string:uuid>
Entrada:
    Caminho da URL: string uuid do canal
Saída:
    HTML
Status de Erro:
    * 404, se o canal não for encontrado (corpo: html)
```

### Saída

```plain
* retorna uma página contendo um formulário CAPTCHA, e então uma página que redireciona para o URI do Canal.
```

# Rotas de Autenticação

Rotas que permitem autenticação no servidor.

## Google Login

Recupera informações de ID do Usuário a partir do Google após receber um `id_token`.

```plain
Métodos:
    POST
Rota:
    /auth/google
Entrada:
    JSON: id_token
Saída:
    JSON: token + dados completos do usuário + canais que este usuário administra
Status de Erro:
    * 400, se id_token não estiver no corpo da requisição
    * 403, se a conta Google tiver sido restringida por este servidor.
    * 403, se o servidor falhar ao autenticar com o servidor de autenticação do Google
```

### Entrada

```json
{
    "id_token": "id token do google auth"
}
```

### Saída

```json
{
	"token": "JWT token gerado por este servidor",
	"user": {
		"channels": [],
		"email": "exemplodecontagoogle@gmail.com",
		"id": 1,
		"name": "Nome Completo do Usuário",
		"uuid": "uuid do usuário"
	}
}
```

## Requer Autenticação

Toda rota marcada com `auth_required` precisa conter um cabeçalho HTTP como este:

```plain
Cabeçalho:
    Authorization: Bearer este-deve-ser-o-token-retornado-pela-rota-de-login-do-google
```

# Rotas da API

Rotas que fornecem transmissão de dados entre Cliente e Servidor

## Obter Canal ([auth\_required](#requer-autenticação))

Recupera os dados completos do `Channel`, contendo mensagens e informações do administrador.

```plain
Métodos:
    GET
Rota:
    /channels/<string:uuid>
Entrada:
    Caminho da URL: string uuid do canal
Saída:
    JSON: dados do Canal
Status de Erro:
    * 404, se o canal não existir
```

### Saída

```json
{
	"admin": {
		"id": 1,
		"name": "Nome Completo do Administrador"
	},
	"alias": "Nome do Canal",
	"id": 2,
	"img_res": "uuid do recurso da imagem",
	"messages": [
		{
			"channel_id": 2,
			"creation_ts": "Ter, 03 Jun 2025 18:19:48 GMT",
			"id": 1,
			"text": "Olá, Mundo!!!",
			"user": {
				"id": 1,
				"name": "Usuário que enviou a mensagem"
			}
		}
	],
	"uuid": "uuid que identifica este canal"
}
```

## Obter Imagem ([auth\_required](#requer-autenticação))

Retorna um recurso de imagem `JPEG` identificado por um `UUID`.

```plain
Métodos:
    GET
Rota:
    /img/<string:img_res>
Entrada:
    Caminho da URL: uuid do recurso de imagem
Saída:
    image/jpeg
Status de Erro:
    * 404, se a imagem não existir
```

## Novo Canal ([auth\_required](#requer-autenticação))

Adiciona um novo `Channel` ao banco de dados.

```plain
Métodos:
    POST
Rota:
    /channels/new
Entrada:
    JSON: dados do Canal [obrigatório: alias]
Saída:
    JSON: dados do Canal
Status de Erro:
    * 400, se dados obrigatórios estiverem ausentes no corpo JSON
```

### Entrada

```json
{
    "alias": "Nome do Canal",
	"img_res": "Imagem em binário, codificada como Base64. Este campo é opcional."
}
```

### Saída

```json
{
	"admin": {
		"id": 1,
		"name": "Nome Completo do Administrador"
	},
	"alias": "Nome do Canal",
	"id": 3,
	"img_res": "uuid do recurso de imagem",
	"messages": [],
	"uuid": "uuid do canal recém-adicionado"
}
```

## Nova Mensagem ([auth\_required](#requer-autenticação))

Adiciona uma nova `Message` a um `Channel`.

```plain
Métodos:
    POST
Rota:
    /messages/new
Entrada:
    JSON: dados da Mensagem [obrigatório: text, channel_uuid]
Saída:
    JSON: dados da Mensagem
Status de Erro:
    * 400, se dados obrigatórios estiverem ausentes no corpo JSON
    * 404, se o canal não for encontrado
```

## Entrada

```json
{
	"channel_uuid": "uuid do canal onde deseja postar sua mensagem",
	"text": "Texto da mensagem que você enviou"
}
```

## Saída

```json
{
	"channel_id": 2,
	"creation_ts": "Ter, 03 Jun 2025 18:19:48 GMT",
	"id": 1,
	"text": "Texto da mensagem que você enviou",
	"user": {
		"id": 1,
		"name": "Nome Completo do Usuário"
	}
}
```

