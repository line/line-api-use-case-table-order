import CreatePersistedState from "vuex-persistedstate"

/**
 *　セッションストレージプラグイン
 *
 * @param {Object} env
 * @param {Object} store
 */
export default ({ env, store }) => {
    CreatePersistedState({
      key: "liff-usecase",
      paths: [
        'sessionId',
        'lineUser',
        'customer',
        'orders',
        'ordered',
        'paymentId',
      ],
      storage: window.sessionStorage  // 有効期限はブラウザ閉じるまで（複数ブラウザ立ち上げは別セッションとなる）
    })(store);
}
