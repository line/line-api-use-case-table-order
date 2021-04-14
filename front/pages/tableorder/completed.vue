<template>
    <v-app class="table-order-font-size">
        <vue-header v-bind:customer="customer" v-bind:basketed="false"></vue-header>
        <v-container>
            <v-row justify="center" align-content="center">
                <v-col align="center" class="mt-15">
                    <p class="text-h6"><v-icon color="success">done</v-icon>{{ $t("completed.msg001") }}</p>
                    <v-divider color="success" class="mt-1 mb-5"></v-divider>
                    <p>{{ $t("completed.msg002") }}</p>
                </v-col>
            </v-row>
        </v-container>
        <v-footer fixed class="pa-0" height="60px">
             <v-btn class="basket white--text" color="#00B900" width="100%" height="100%" v-on:click="payment">
                <v-icon left large>mdi-cash-register</v-icon>&nbsp;<span v-html="$t('completed.msg003')"></span>
            </v-btn>
        </v-footer>
    </v-app>
</template>

<script>
/**
 * 注文完了画面
 * 
 */
import VueHeader from "~/components/tableorder/Header.vue"
export default {
    layout: "tableorder/order",
    components: {
        VueHeader,
    },
    async asyncData({ store, app }) {
        // Customer
        const customer = store.state.customer;

        return {
            customer: customer,
        }
    },
    head() {
        return {
            title: this.$t("title")
        }
    },
    data() {
        return {
            customer: null,
        }
    },
    methods: {
        /**
         * メニュー画面へ遷移
         * 
         */
        menu() {
            this.$router.push("/tableorder/menu/" + this.customer.seatNo);
        },
        /**
         * 注文履歴画面へ遷移
         * 
         */
        payment() {
            this.$router.push("/tableorder/payment");
        }
    }
}
</script>
