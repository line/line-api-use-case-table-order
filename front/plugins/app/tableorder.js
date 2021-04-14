/**
 * テーブルオーダーアプリケーションプラグイン
 *
 * @param {Object} $axios
 * @param {Object} app
 * @param {Object} store
 * @return {VueTableorder} 
 */
const VueTableorder = ($axios, app, store, env) => {
    /** @type {string} 通信モジュール */
    const _module = env.AJAX_MODULE ? env.AJAX_MODULE : "axios";
    /** @type {string} APIGatewayステージ名 */
    const _stage = `/${env.APIGATEWAY_STAGE}`;
    /** @type {Object} ロケール */
    let _i18n = app.i18n.messages[store.state.locale];

    return {
        /**
         * 商品情報取得　
         *
         * @param {string} categoryId カテゴリーID
         * @return {Object} 商品情報  
         */
        async getItemData(categoryId = '0') {
            const itemData = await this[_module].itemData(categoryId);
            return itemData;
        },
        /**
         * カテゴリー一覧取得　
         *
         * @return {Object} カテゴリー一覧  
         */
        async getCategoryData() {
            const categories = await this[_module].categoryData();
            return categories;
        },
        /**
         * 注文送信・注文完了
         *
         * @param {string} paymentId 会計ID
         * @param {number} tableId 座席番号
         * @param {Object} orders 注文内容
         * @return {Object} 商品情報  
         */
        async putOrder(paymentId = null, tableId, orders) {
            
            let items = [];
            for ( const order in orders ) {
                for ( const item in orders[order] ) {
                    const categoryId = orders[order][item].order.categoryId;
                    const itemId = orders[order][item].order.itemId;
                    const orderNum = orders[order][item].count;

                    items.push(
                        {
                            categoryId: categoryId,
                            itemId: itemId,
                            orderNum: orderNum,
                        }
                    )
                }
            }
            // LIFF ID Token取得
            const idToken = store.state.lineUser.idToken;

            let params = null;
            if (paymentId == null) {
                params = { idToken: idToken, tableId: tableId, item: items };
            } else {
                params = { paymentId: paymentId, idToken: idToken, tableId: tableId, item: items };
            }
            
            const itemData = await this[_module].order(params);
            return itemData;
        },
        /**
         * 注文会計情報取得　
         *
         * @param {string} paymentId 会計ID
         * @return {Object} 注文情報
         */
        async getOrderData(paymentId) {
            const orderData = await this[_module].orderData(paymentId);
            return orderData;
        },
        /**
         * 決済予約
         *
         * @param {string} paymentId 会計ID
         * @return {Object} LINE Pay情報
         */
        async reservePayment(paymentId) {
            // LIFF ID Token取得
            const idToken = store.state.lineUser.idToken;
            
            const params = {"idToken": idToken, "paymentId": paymentId};
            const response = await this[_module].paymentReserve(params);
            return response;    
 
        },
        /**
         * 決済完了
         *
         * @param {string} transactionId 決済トランザクションID
         * @param {string} paymentId 会計ID
         * @return {boolean} 決済状況
         */
        async confirmPayment(transactionId, paymentId) {
            const params = {"transactionId": transactionId, "paymentId": paymentId};
            const response = await this[_module].paymentConfirm(params);
            return response;
        },
        /**
         * LinePay以外の決済
         *
         * @param {string} paymentId 会計ID
         * @return {Object} 決済状況
         */
        async comfirmNoLinePay(paymentId) {
            // LIFF ID Token取得
            const idToken = store.state.lineUser.idToken;
            const params = {"idToken": idToken, "paymentId": paymentId};
            const response = await this[_module].noLinePayConfirm(params);
            return response;    
        },
        /**
         * 会計ID取得　
         *
         * @return {string} paymentId  
         */
        async getPaymentId() {
            // LIFF ID Token取得
            const idToken = store.state.lineUser.idToken;

            const paymentId = await this[_module].paymentData(idToken);
            return paymentId;
        },

        // ============================================
        //     ユーティリティ
        // ============================================
        utils: {
            /**
             *　商品の値引き価格を取得
            *
            * @param {Object} order 商品情報
            * @return {number} 値引き額
            */
            getDiscountPrice(order) {
                let p = 0;

                if (order.discountWay == 1) {
                    p = order.discountRate;
                }
                if (order.discountWay == 2) {
                    p = (order.price * order.discountRate * 0.01);
                }
                return Math.floor(p);
            },
        },
        // ============================================
        //     Lambdaアクセス (Axios)
        // ============================================
        axios: {
            /**
             * 商品情報取得API
             *
             * @param {number} categoryId カテゴリーID
             * @return {Object} APIレスポンス内容
             */
            itemData: async(categoryId) => {
                // 送信パラメーター
                const params = {
                    locale: store.state.locale,
                    categoryId: categoryId,
                }
                // GET送信
                const response = await $axios.get(`${_stage}/item_list_get`, { params: params });
                return response.status==200 ? response.data : null;
            },
            /**
             * カテゴリー一覧取得API
             *
             * @return {Object} APIレスポンス内容
             */
            categoryData: async() => {
                // 送信パラメーター
                const params = {
                    locale: store.state.locale,
                }
                const response = await $axios.get(`${_stage}/category_get`, { params: params });
                return response.status==200 ? response.data : null;
            },
            /**
             * 注文登録API
             *
             * @param {Object} params 送信パラメーター
             * @return {Object} APIレスポンス内容 
             */
            order: async(params) => {
                // 送信パラメーターロケール付加
                params['locale'] = store.state.locale;
                // POST送信
                const response = await $axios.post(`${_stage}/order_put`, params);
                return response.status==200 ? response.data : null;
            },
            /**
             * 注文会計情報取得API
             *
             * @param {number} paymentId payment ID
             * @return {Object} APIレスポンス内容
             */
            orderData: async(paymentId) => {
                // 送信パラメーター
                const params = {
                    locale: store.state.locale,
                    paymentId: paymentId,
                }
                // GET送信
                const response = await $axios.get(`${_stage}/order_info_get`, { params: params });
                return response.status==200 ? response.data : null;
            },
            /**
             * 決済予約API
             *
             * @param {Object} params 送信パラメーター
             * @return {Object} APIレスポンス内容 
             */
            paymentReserve: async(params) => {
                // 送信パラメーターロケール付加
                params['locale'] = store.state.locale;
                // POST送信
                const response = await $axios.post(`${_stage}/payment_reserve`, params);
                return response.status==200 ? response.data : null;
            },
            /**
             * 決済完了API
             *
             * @param {Object} params 送信パラメーター
             * @return {Object} APIレスポンス内容 
             */
            paymentConfirm: async(params) => {
                // 送信パラメーターロケール付加
                params['locale'] = store.state.locale;
                // POST送信
                const response = await $axios.post(`${_stage}/payment_confirm`, params);
                if ( response && response.status >= 400 ) {
                    store.commit("paymentError", true);
                }
                return response.status==200 ? false : true;
            },
            /**
             * 決済完了API（LINE Payの支払い以外）
             *
             * @param {Object} params 送信パラメーター
             * @return {Object} APIレスポンス内容 
             */
            noLinePayConfirm: async(params) => {
                // 送信パラメーターロケール付加
                params['locale'] = store.state.locale;
                // POST送信
                const response = await $axios.post(`${_stage}/confirm_nolinepay`, params);
                return response.status==200 ? response.data : null;
            },
            /**
             * 会計ID取得API
             *
             * @param {string} idToken ID Token
             * @return {Object} APIレスポンス内容
             */
            paymentData: async(idToken) => {
                // 送信パラメーター
                const params = {
                    locale: store.state.locale,
                    idToken: idToken,
                }
                // GET送信
                const response = await $axios.get(`${_stage}/payment_id_get`, { params: params });
                return response.status==200 ? response.data : null;
            },
        },
        // ============================================
        //     Lambdaアクセス (Amplify API)
        // ============================================
        amplify: {
            /**
             * 商品情報取得API
             *
             * @param {number} categoryId カテゴリーID
             * @return {Object} APIレスポンス内容
             */
            itemData: async(categoryId) => {
                let response = null;
                // 送信パラメーター
                const myInit = {
                    queryStringParameters: {
                        locale: store.state.locale,
                        categoryId: categoryId
                    },
                };
                // GET送信
                try {
                    response = await app.$amplify.API.get("LambdaAPIGateway", `${_stage}/item_list_get`, myInit);
                } catch (error) {
                    app.$utils.showHttpError(error);
                }

                return response;
            },
            /**
             * カテゴリー一覧取得API
             *
             * @return {Object} APIレスポンス内容
             */
            categoryData: async() => {
                let response = null;
                // 送信パラメーター
                const myInit = {
                    queryStringParameters: {
                        locale: store.state.locale,
                    },
                };
                // GET送信
                try {
                    response = await app.$amplify.API.get("LambdaAPIGateway", `${_stage}/category_get`, myInit);
                } catch (error) {
                    app.$utils.showHttpError(error);
                }

                return response;
            },
            /**
             * 注文登録API
             *
             * @param {Object} params 送信パラメーター
             * @return {Object} APIレスポンス内容 
             */
            order: async(params) => {
                let response = null;
                // 送信パラメーターロケール付加
                params['locale'] = store.state.locale;
                // 送信パラメーター
                const myInit = {
                    body: params,
                };
                // POST送信
                try {
                    response = await app.$amplify.API.post("LambdaAPIGateway", `${_stage}/order_put`, myInit);
                } catch (error) {
                    app.$utils.showHttpError(error);
                }

                return response;
            },
            /**
             * 注文会計情報取得API
             *
             * @param {number} paymentId 会計ID
             * @return {Object} APIレスポンス内容
             */
            orderData: async(paymentId) => {
                let response = null;
                // 送信パラメーター
                const myInit = {
                    queryStringParameters: {
                        locale: store.state.locale,
                        paymentId: paymentId
                    },
                };
                // GET送信
                try {
                    response = await app.$amplify.API.get("LambdaAPIGateway", `${_stage}/order_info_get`, myInit);
                } catch (error) {
                    app.$utils.showHttpError(error);
                }

                return response;
            },
            /**
             *決済予約API
             *
             * @param {Object} params 送信パラメーター
             * @return {Object} APIレスポンス内容 
             */
            paymentReserve: async(params) => {
                let response = null;
                // 送信パラメーターロケール付加
                params['locale'] = store.state.locale;
                // 送信パラメーター
                const myInit = {
                    body: params,
                };
                // POST送信
                try {
                    response = await app.$amplify.API.post("LambdaAPIGateway", `${_stage}/payment_reserve`, myInit);
                } catch (error) {
                    app.$utils.showHttpError(error);
                }

                return response;
            },
            /**
             *決済完了API
             *
             * @param {Object} params 送信パラメーター
             * @return {Object} APIレスポンス内容 
             */
            paymentConfirm: async(params) => {
                let response = null;
                // 送信パラメーターロケール付加
                params['locale'] = store.state.locale;
                // 送信パラメーター
                const myInit = {
                    body: params,
                };
                // POST送信
                let isError = false;
                try {
                    response = await app.$amplify.API.post("LambdaAPIGateway", `${_stage}/payment_confirm`, myInit);
                } catch (error) {
                    app.$utils.showHttpError(error);
                    isError = true;
                }

                return isError;
            },
            /**
             * 決済完了API（LINE Payの支払い以外）
             *
             * @param {Object} params 送信パラメーター
             * @return {Object} APIレスポンス内容 
             */
            noLinePayConfirm: async(params) => {
                let response = null;
                // 送信パラメーターロケール付加
                params['locale'] = store.state.locale;
                // 送信パラメーター
                const myInit = {
                    body: params,
                };
                // POST送信
                try {
                    response = await app.$amplify.API.post("LambdaAPIGateway", `${_stage}/confirm_nolinepay`, myInit);
                } catch (error) {
                    app.$utils.showHttpError(error);
                }

                return response;
            },
            /**
             * 会計ID取得API
             *
             * @param {string} idToken ID Token
             * @return {Object} APIレスポンス内容
             */
            paymentData: async(idToken) => {
                let response = null;
                // 送信パラメーター
                const myInit = {
                    queryStringParameters: {
                        locale: store.state.locale,
                        idToken: idToken,
                    },
                };
                // GET送信
                try {
                    response = await app.$amplify.API.get("LambdaAPIGateway", `${_stage}/payment_id_get`, myInit);
                } catch (error) {
                    app.$utils.showHttpError(error);
                }

                return response;
            },
        }
    }
}

export default ({ $axios, app, store, env }, inject) => {
    inject("tableorder", VueTableorder($axios, app, store, env));
}
