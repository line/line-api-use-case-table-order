## Building a local front-end environment

Front-end development is done in the Nuxt.js project's Single Page Application (SPA). Start the Nuxt development server and static build the production module in your local environment. After downloading the source code, perform these operations in the local environment.

- .env file settings

    Set the .env file to the value used by the front application.

    ▼ .env file
    ```
    # LIFF ID
    LIFF_ID=9999999999-xxxxxxxx

    # AXIOS BASE URL
    BASE_URL=https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com

    # API Gateway Stage
    APIGATEWAY_STAGE=dev

    # Ajax Module (axios or amplify)
    AJAX_MODULE=amplify
    ```

    - Set `LIFF_ID` to the LIFF ID of the LINE channel's LIFF app.
    - Set the URL of AWS APIGateway to `BASE_URL`
    - Set the stage name of the AWS APIGateway to `APIGATEWAY_STAGE`.
    - Set the module used for Ajax communication (Amplify API is "amplify" / Axios is "axios") in `AJAX_MODULE`

- node_modules installation

    If the Node.js dependency package (* node_modules folder) isn't installed in the front project, run this command directly under the front folder to install node_modules.
    ```
    npm install
    ```
    or
    ```
    yarn install
    ```
    After the installation is complete, the front/`node_modules` folder will be created.

- Fixing LIFF app endpoint URLs

    Since you're developing on a web server in a local development environment, change the `endpoint URL` of the LIFF app on the LINE channel to this URL (*Change it back to the CloudFront URL after development is complete).
    ```
    https://localhost:3000
    ```

- HTTPS communication of Nuxt development server

    The `endpoint URL` of the LIFF app for the LINE channel can only be set to a URL starting with https. Therefore, you need to use an SSL certificate to make the Nuxt development server use HTTPS communication. Place the SSL certificate (`localhost.key`, `localhost.crt`) in the following location.
    ```
    front/cert
    ```
    After placing, remove the following comment out (`//`) from `nuxt.config.js`.
    ```
    export default {
        telemetry: false,
        mode: 'spa',
        generate: {
            dir: './dist'
        },
        server: {
            port: 3000,
            host: '0.0.0.0',
            timing: false,
            https: {
    //            key: fs.readFileSync('./cert/localhost.key'),
    //            cert: fs.readFileSync('./cert/localhost.crt')
            }
        },
    ```
    [Reference]　　
    An example of creating an SSL certificate (self-signed certificate)  
    *How to create an SSL certificate using the openssl command
    ```
    # Private key file generation
    openssl genrsa -out localhost.key 2048
    # Generate certificate signing request file
    openssl req -new -key localhost.key -out localhost.csr -subj '/C=JP/ST=Tokyo/L=Tokyo/O=Example Ltd./OU=Web/CN=localhost'
    # Certificate generation
    openssl x509 -in localhost.csr -days 3650 -req -signkey localhost.key -out localhost.crt
    ```

- Start the Nuxt development server

    Development in the local environment is done by starting the Nuxt development server. Start the Nuxt development server by executing the following command directly under the front folder. You should now be able to access `https://localhost:3000`. If you have already set "Fixing LIFF app endpoint URLs" above, you can access your local environment with the LIFF URL of your LIFF app (e.g. `https://liff.line.me/9999999999-xxxxxxxx`) for development.
    ```
    npm run dev
    ```
    or
    ```
    yarn run dev
    ```



[Next page](test-data-charge.md)  

[Back to Table of Contents](README_en.md)
