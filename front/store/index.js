/**
 * Store
 *
 */
export const state = ()=>({
    started: null,
    locales: ['ja'],
    locale: 'ja',
    sessionId: null,
    lineUser: null,
    customer: null,
    orders: null,
    ordered: null,
    paymentId: null,
    axiosError: null,
    paymentError: null,
});

export const mutations = {
    clear(state) {
        state.started = null;
        state.locale = 'ja';
        state.sessionId = null;
        state.lineUser = null;
        state.customer = null;
        state.orders = null;
        state.ordered = null;
        state.paymentId = null;
        state.axiosError = null;
        state.paymentError = null;
    },
    started(state, started) {
        state.started = started;
    },
    locale(state, locale) {
        if (state.locales.includes(locale)) {
            state.locale = locale;
        }
    },
    session(state, sessionId) {
        state.sessionId = sessionId;
    },
    lineUser(state, lineUser) {
        state.lineUser = lineUser;
    },
    customer(state, customer) {
        state.customer = customer;
    },
    orders(state, orders) {
        state.orders = orders;
    },
    ordered(state, ordered) {
        state.ordered = ordered;
    },
    paymentId(state, paymentId) {
        state.paymentId = paymentId;
    },
    axiosError(state, axiosError) {
        state.axiosError = axiosError;
    },
    paymentError(state, paymentError) {
        state.paymentError = paymentError;
    },
};

export const getters = {
    axiosError(state) {
        return state.axiosError;
    },
    isAxiosError(state) {
        return (state.axiosError!=null && !state.paymentError) ? true : false;
    },
    isPaymentError(state) {
        return state.paymentError;
    }
}