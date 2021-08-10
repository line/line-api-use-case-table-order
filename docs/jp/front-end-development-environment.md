## ローカルフロントエンド環境構築
フロントエンドの開発は Nuxt.js プロジェクトの SPA (Single Page Application) で開発を行います。ローカル環境で Nuxt 開発用サーバーの起動や本番モジュールの静的ビルドを行います。ソースコードダウンロード後、ローカル環境で以下の作業を行ってください。

- .env ファイルの設定

    .env ファイルにフロントのアプリケーションで使用する値を設定してください。

    ▼ .env ファイル
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

    - `LIFF_ID` には LINE チャンネルの LIFF アプリの LIFF ID を設定
    - `BASE_URL` には AWS APIGateway の URL を設定
    - `APIGATEWAY_STAGE` には AWS APIGateway のステージ名を設定
    - `AJAX_MODULE` には Ajax 通信の時に使用するモジュール（ Amplify API は "amplify" ／ Axios は "axios" ）を設定

- node_modules インストール

    front プロジェクトに Node.js の依存パッケージ(※ node_modules フォルダ)がインストールされていない場合、 front フォルダー直下で以下のコマンドを実行して node_modules をインストールしてください。
    ```
    npm install
    ```
    もしくは
    ```
    yarn install
    ```
    インストールが完了したら front/`node_modules` フォルダが生成されています。

- LIFF アプリのエンドポイントURLの修正

    ローカル開発環境の Web サーバーで開発する為、 LINE チャネルの LIFF アプリの`エンドポイントURL`を以下の URL に変更してください（※開発完了後 CloudFront の URL に戻してください）。
    ```
    https://localhost:3000
    ```

- Nuxt 開発サーバーの HTTPS 通信化

    LINE チャネルの LIFF アプリの`エンドポイントURL`は https から始まる URL しか設定できません。その為、SSL 証明書使用して Nuxt 開発サーバーを HTTPS 通信化してください。以下の場所にSSL証明書(`localhost.key`, `localhost.crt`)を配置します。
    ```
    front/cert
    ```
    配置後、`nuxt.config.js`の下記のコメントアウト`//`を取ります。
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
    【参考】
    SSL 証明書（自己署名証明書）作成の１例
    ※opensslコマンド使って作成する方法
    ```
    # 秘密鍵ファイル生成
    openssl genrsa -out localhost.key 2048
    # 証明書署名要求ファイル生成
    openssl req -new -key localhost.key -out localhost.csr -subj '/C=JP/ST=Tokyo/L=Tokyo/O=Example Ltd./OU=Web/CN=localhost'
    # 証明書生成
    openssl x509 -in localhost.csr -days 3650 -req -signkey localhost.key -out localhost.crt
    ```

- Nuxt 開発サーバーの起動

    ローカル環境での開発は Nuxt 開発サーバーを起動して行います。 front フォルダ直下で以下のコマンドを実行して Nuxt 開発サーバーを起動してください。 `https://localhost:3000` にアクセスできるようになります。上記 「 LIFF アプリのエンドポイントURLの修正 」を設定済みの場合、 LIFF アプリの LIFF URL (例：`https://liff.line.me/9999999999-xxxxxxxx`) でローカル環境にアクセスして開発を行えます。
    ```
    npm run dev
    ```
    もしくは
    ```
    yarn run dev
    ```



[次の頁へ](test-data-charge.md)

[目次へ戻る](../../README.md)
