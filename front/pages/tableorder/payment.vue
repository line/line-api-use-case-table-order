<template>
    <v-app class="table-order-font-size">
        <!-- Header -->
        <vue-header v-bind:customer="customer" v-bind:basketed="true"></vue-header>
        <!-- Ordered List-->
        <div class="mt-16 text-center">
            <v-btn color="#00B900" class="mt-5 white--text" height="50" width="80%" style="font-size:1.4em;" v-bind:disabled="amount==0" v-on:click="paymentDialog">
                <v-icon left>fas fa-cash-register</v-icon>
                <span v-html="$t('payment.msg001', { price: amount.toLocaleString() })"></span>
            </v-btn>
        </div>
        <div class="mt-1 text-center red--text" >
            ※{{ $t("payment.msg002") }}<br>
            {{ $t("payment.msg003") }}<br>{{ $t("payment.msg004") }}
        </div>

        <v-expansion-panels v-model="panel" multiple class="py-5 px-3">
            <v-expansion-panel v-for="(order, index) in ordered" v-bind:key="order.orderId">
                <v-expansion-panel-header color="grey lighten-2">
                    <div class="font-weight-bold" style="font-size:1.0rem;">
                        <div>
                            <span style="color:blue;">{{ orderDatetimeFormat(order.orderDateTime) }}</span>&nbsp;{{ $t("payment.msg005") }}
                        </div>
                    </div>
                </v-expansion-panel-header>
                <v-expansion-panel-content id="innerExPan">
                    <vue-order v-show="index==0" class="pa-0" v-bind:value="order.item" v-on:totalPay="totalPay"></vue-order>
                    <vue-order v-show="index!=0" class="pa-0" v-bind:value="order.item"></vue-order>
                </v-expansion-panel-content>
            </v-expansion-panel>
        </v-expansion-panels>

        <!-- Dialog-->
        <v-dialog v-model="dialog" max-width="400">
            <v-toolbar color="#00B900" dense>
                <v-btn icon dark v-on:click="dialog=false">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
                <span class="white--text title">{{ $t("payment.msg006") }}</span>
            </v-toolbar>
            <v-card color="grey lighten-4" class="pa-1">
                <v-card-title>
                    <span style="margin: 0 auto;" class="font-weight-bold">{{ $t("payment.msg007", { price: amount.toLocaleString()}) }}<span style="font-size:1.0rem;"></span></span>
                </v-card-title>
                <v-card v-for="method in paymentMethods" :key="method.title" hover class="ma-4" @click="pay(method.method)">
                    <v-card-title style="font-size:1.0rem;">
                        <span style="margin: 0 auto;"><v-icon large v-show="method.image==''">mdi-cash-register</v-icon>{{ method.title }}</span>
                    </v-card-title>
                    <v-card-title v-show="method.image!=''" class="pt-0 pb-5">
                        <img style="width:30%; margin: 0 auto;" :src="method.image" :alt="method.title"/>
                        <div class="mt-3 red--text font-weight-bold" style="width: 100%; font-size: 0.5em; margin: 0 auto; line-height: 1.5em; text-align:center;">
                            <span v-html="$t('payment.msg008')"></span>
                        </div>
                    </v-card-title>
                </v-card>
            </v-card>
        </v-dialog>
    </v-app>
</template>

<script>
/**
 * 注文履歴・決済画面
 * 
 */
import VueHeader from "~/components/tableorder/Header.vue"
import VueOrder from "~/components/tableorder/Ordered.vue"

export default {
    layout: "tableorder/order",
    components: {
        VueHeader,
        VueOrder,
    },
    async asyncData({ store, app, $axios }) {
        // Customer
        const customer = store.state.customer;

        //　注文会計情報取得API
        const paymentId = store.state.paymentId;
        const itemResponse = await app.$tableorder.getOrderData(paymentId);
        
        if ( !itemResponse ) {
           return { noOrder: true } 
        }
        const ordered = itemResponse.order.reverse();
        const amount = itemResponse.amount;

        return {
            customer: customer,
            ordered: ordered,
            amount: amount,
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
            ordered: null,
            amount: null,
            taxAmount: null,
            dialog: false,
            paymentMethods: [
                { title: 'LINE Pay', method: 'linePay', flex: 10, flex_sm: 6, image: require('@/assets/img/line_pay.png') },
                { title: this.$t("payment.msg009"), method: 'staffPay', flex: 10, flex_sm: 4, image: '' }
            ],
            total: null,
            panel: [0],
            noOrder: false,
        }
    },
    created() {
        if ( this.noOrder ) {
            this.$router.push("/");
        }
    },
    mounted() {

    },
    methods: {
        /**
         * 決済ダイアログ表示
         * 
        */
        paymentDialog() {
            this.dialog = true;
        },
        /**
         * LINE Pay・レジ決済
         * 
         * @param {string} method 決済方法
         */
        async pay(method) {
            
            this.dialog = false;
    
            const paymentId = this.$store.state.paymentId;

            if (method == 'linePay') {
                // LINE Payを呼び出しています..
                this.$processing.show(0, this.$t("payment.msg010"));
                const response = await this.$tableorder.reservePayment(paymentId);
                            
                this.$processing.hide();
                //　LINE Pay決済画面に遷移
                window.location = response.info.paymentUrl.web;
            } else if (method == 'staffPay') {
                // スタッフを呼び出し、決済手続きをしています..
                this.$processing.show(0, this.$t("payment.msg011"));
                const response = await this.$tableorder.comfirmNoLinePay(paymentId);
                const completed = function(t) {
                            t.$processing.hide();
                            t.$router.push('/tableorder/paymentCompleted');
                        };
                setTimeout(completed, 3000, this);
            }
        },
        /**
         * 合計金額取得
         * 
         * @param {string} total 合計金額
         */
        totalPay(total) {
            // 子コンポーネントOrderから$emit受け取り
            this.total = total;
        },
        /**
         * 日付フォーマット
         * 
         * @param {string} date "yyyy/MM/dd HH:mm:ss"形式の注文日時
         * @returns {string} "yyyy/MM/dd HH:mm"形式の注文日時
         */
        orderDatetimeFormat(date) {
            return date.slice( 0, -3 ) ;
        },
    }
}
</script>

<style scoped>
.table-order-font-size {
    font-size: 16px;
}
@media screen and (max-width:540px) {
    .table-order-font-size {
        font-size: 12px;
    }
}
.v-expansion-panel-content >>> .v-expansion-panel-content__wrap { 
    padding: 0;
 }
</style>
