Como configurar o Google como mecanismo de autenticação?
========================================================

O [Google Cloud Console](https://console.cloud.google.com/) é uma plataforma web que permite aos desenvolvedores gerenciar serviços e recursos da [Google Cloud Platform (GCP)](https://pt.wikipedia.org/wiki/Google_Cloud_Platform), incluindo autenticação de usuários. Por meio dele, é possível criar projetos e configurar credenciais [OAuth 2.0](https://oauth.net/), permitindo a integração com o login via conta Google tanto em web apps quanto em aplicativos Android. Isso envolve registrar o app, definir os escopos de acesso, configurar URIs de redirecionamento autorizados e proteger as credenciais. Além da autenticação, o Console também pode ser usado para ativar APIs (como Gmail, Drive, Maps), armazenar dados (Firestore, Cloud Storage), monitorar o uso e erros da aplicação (Cloud Logging), e controlar permissões de acesso por meio de contas de serviço e políticas [IAM](https://cloud.google.com/iam/docs/overview?hl=pt-br). Dessa forma, ele centraliza o gerenciamento da infraestrutura, segurança e recursos necessários ao desenvolvimento e operação de aplicações modernas na nuvem.

## Criando um cliente para a *API OAuth*

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/) e crie um novo projeto.
2. Selecione seu novo projeto no painel inicial.
3. Vá para `APIs & serviços` e, em seguida, escolha a opção `Credenciais` no menu.
4. Clique em `Criar credenciais` e selecione `ID do cliente OAuth`.
5. Clique em `Configurar tela de consentimento` e depois em `Começar`.
6. Preencha os formulários obrigatórios e clique em **"Criar"**:
      * **Informações do app**: nome do seu app (e.g. ChatApp) e e-mail.
      * **Público-alvo (Audience)**: selecione **externo**.
      * **Informações de contato**: seu endereço de e-mail novamente.
      * **Finalizar**: e então concorde em vender sua alma para o Google (*brincadeirinha* 🤭).
7. Clique em `Criar cliente OAuth`
    * Nesta parte vai ser oferecida várias formas de criar clientes OAuth para diferentes tipos de contexto, i.e. Android App, Web App, iOS App...
    * Para realizar testes neste servidor com um software de teste de APIs, sugiro seguir estes [passos](#configurando-uma-forma-para-testar-com-um-api-tester) primeiro.

### Configurando uma forma para testar com um *API tester*

8. Escolha o tipo de aplicativo como `Aplicativo da Web` e dê um nome claro para que você reconheça posteriormente. (e.g. `chatapp-web-tester`)
9. Copie o `Client ID` e o `Client Secret` para usar na próxima etapa.
10. Em `URIs de redirecionamento autorizados`, adicione uma URL segura que será responsável por redirecionar para a página de autenticação do google. Neste caso, como o *ChatApp Server* não oferece uma rota de redirecionado, pois é baseado em autenticação *stateless*, nós vamos usar o *OAuth Playground* da google. Portanto, adicione a seguinte URI:

    > https://developers.google.com/oauthplayground/

11. Abra a página do [OAuth Playground](https://developers.google.com/oauthplayground/).
12. Na engrenagem do canto superior direito, marque a opção `Use your own OAuth credentials`.
13. Preencha `OAuth Client ID` e `OAuth Client Secret` gerados no passo 9.
14. No canto esquerdo, na aba `Select & authorize APIs` adicione o escopo no *input* com as informações abaixo e clique em `Authorize APIs`:

    > openid email profile 

15. Escolha sua conta Google que atende aos requisitos de `RESTRICT_TO` do `config.json` do *ChatApp Server*. Aceite os termos para continuar.

16. Agora em `Exchange authorization code for tokens` clique no botão de mesmo título para completar a requisição e obter o `id_token` do serviço de OAuth da Google.

17. O *body* da resposta do servidor irá conter um JSON. Nele, copie o valor da chave `"id_token"`. Este é o `token` que você irá utilizar para testar a rota `auth/google` do *ChatApp Server*. A rota `auth/google` é a responsável por gerar o JWT usado nos *endpoints* que requerem token de autenticação no serviço do *ChatApp Server*.

### Configurando para usar no *mobile app*

8. Escolha o tipo de aplicativo como `Android` e dê um nome claro para que você reconheça posteriormente. (e.g. `chatapp-android-debug`)
9. Você precisará informar o nome do pacote do seu aplicativo e a assinatura SHA-1.
    * Copie o nome do pacote do app: e.g. `br.edu.iftm.chatapp`
    * Para gerar a assinatura do seu aplicativo, se ele ainda não está na loja execute o seguinte comando no terminal:
        * **OBS**: o `debug.keystore` geralmente está localizado na pasta `~/.android/debug.keystore` no Linux e este código só serve para apps em modo *debugging*. Veja mais detalhes sobre isso clicando [aqui](https://support.google.com/cloud/answer/6158849#installedapplications&android)
        * **A senha pedida pelo keytool é `android`**, para este caso
    ```bash
    keytool -list -v -keystore ~/.android/debug.keystore
    ```
    * Copie o conjunto de octetos, que vem logo após `SHA1` na resposta do programa *keytool*, e cole no campo do site. Finalize a criação do cliente.
12. Siga os 8 a 13 da [seção anterior](#configurando-uma-forma-para-testar-com-um-api-tester) e copie o `Cliente ID` gerado nesta etapa, você irá precisar dele para a implementação da comunicação do app com o backend do *ChatApp Server*.
11. Na página de [Branding](https://console.developers.google.com/auth/branding), certifique-se de que você inseriu corretamente as informações do aplicativo.
    * Certifique-se de que seu App está com o nome, a logo e a página web atribuídas. Estes valores vão ser apresentados para os usuários no momento em que clicarem para logar com a conta Google. 
    * Veja mais detalhes nesta [seção](https://developer.android.com/identity/sign-in/credential-manager-siwg#set-google) na página *developers*.
