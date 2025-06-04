# How to set up Google as an authentication mechanism?

The [Google Cloud Console](https://console.cloud.google.com/) is a web platform that allows developers to manage services and resources from the [Google Cloud Platform (GCP)](https://pt.wikipedia.org/wiki/Google_Cloud_Platform), including user authentication. Through it, you can create projects and configure [OAuth 2.0](https://oauth.net/) credentials, enabling integration with Google account login for both web apps and Android applications. This involves registering the app, defining access scopes, configuring authorized redirect URIs, and securing the credentials. In addition to authentication, the Console can also be used to enable APIs (such as Gmail, Drive, Maps), store data (Firestore, Cloud Storage), monitor application usage and errors (Cloud Logging), and control access permissions through service accounts and [IAM](https://cloud.google.com/iam/docs/overview?hl=pt-br) policies. This way, it centralizes the management of infrastructure, security, and resources needed for the development and operation of modern cloud applications.

## Creating a client for the *OAuth API*

1. Access the [Google Cloud Console](https://console.cloud.google.com/) and create a new project.
2. Select your new project from the initial dashboard.
3. Go to `APIs & Services` and then choose the `Credentials` option from the menu.
4. Click on `Create Credentials` and select `OAuth Client ID`.
5. Click on `Configure consent screen` and then `Get started`.
6. Fill in the required forms and click **"Create"**:

   * **App information**: your app name (e.g. ChatApp) and email.
   * **Audience**: select **external**.
   * **Contact information**: your email address again.
   * **Finish**: and then agree to sell your soul to Google (*just kidding* 🤭).
7. Click on `Create OAuth client`

   * At this point, you'll be offered various options to create OAuth clients for different contexts, i.e., Android App, Web App, iOS App...
   * To run tests on this server using an API testing tool, I recommend following these [steps](#configuring-a-way-to-test-using-an-api-tester) first.

### Configuring a way to test using an *API tester*

8. Choose the application type as `Web application` and give it a clear name you’ll recognize later (e.g. `chatapp-web-tester`).

9. Copy the `Client ID` and `Client Secret` to use in the next step.

10. In `Authorized redirect URIs`, add a secure URL responsible for redirecting to the Google authentication page. In this case, since *ChatApp Server* doesn’t offer a redirect route, as it uses *stateless* authentication, we will use Google’s *OAuth Playground*. Therefore, add the following URI:

    > [https://developers.google.com/oauthplayground](https://developers.google.com/oauthplayground)

11. Open the [OAuth Playground](https://developers.google.com/oauthplayground/) page.

12. In the top-right gear icon, check the option `Use your own OAuth credentials`.

13. Fill in the `OAuth Client ID` and `OAuth Client Secret` generated in step 9.

14. On the left side, in the `Select & authorize APIs` tab, add the scope in the input field with the info below and click `Authorize APIs`:

    > openid email profile

15. Choose your Google account that meets the `RESTRICT_TO` requirements from *ChatApp Server’s* `config.json`. Accept the terms to continue.

16. Now in `Exchange authorization code for tokens`, click the button with the same title to complete the request and obtain the `id_token` from Google’s OAuth service.

17. The server response *body* will contain a JSON. In it, copy the value of the `"id_token"` key. This is the `token` you will use to test the `auth/google` route of *ChatApp Server*. The `auth/google` route is responsible for generating the JWT used in *endpoints* that require an authentication token on the *ChatApp Server* service.

### Setting it up for use in the *mobile app*

8. Choose the application type as `Android` and give it a clear name you’ll recognize later (e.g. `chatapp-android-debug`).
9. You’ll need to provide your app's package name and SHA-1 signature.

   * Copy your app’s package name: e.g. `br.edu.iftm.chatapp`
   * To generate the app signature, if it’s not published yet, run the following command in the terminal:

     * **NOTE**: the `debug.keystore` is usually located at `~/.android/debug.keystore` on Linux and this code only works for apps in *debug* mode. See more details [here](https://support.google.com/cloud/answer/6158849#installedapplications&android)
     * **The password requested by keytool is `android`**, in this case

   ```bash
   keytool -list -v -keystore ~/.android/debug.keystore
   ```

   * Copy the octet set that appears right after `SHA1` in the keytool output and paste it in the site’s field. Finalize the client creation.
10. Follow steps 8 to 13 from the [previous section](#configuring-a-way-to-test-using-an-api-tester) and copy the `Client ID` generated in this step. You’ll need it to implement the communication between the app and the *ChatApp Server* backend.
11. On the [Branding](https://console.developers.google.com/auth/branding) page, ensure that you correctly filled in the app information.

* Make sure your app has its name, logo, and website assigned. These values will be shown to users when they click to log in with their Google account.
* See more details in this [section](https://developer.android.com/identity/sign-in/credential-manager-siwg#set-google) on the *developers* page.
