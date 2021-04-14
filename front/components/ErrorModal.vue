<template>
<div>
    <!-- 通常エラーの場合 -->
    <v-dialog v-model="isAxiosError" persistent max-width="500">
        <v-card>
            <v-card-title><v-icon large color="error">error</v-icon>{{ $t("error.msg001") }}</v-card-title>
            <v-card-text>
                <p><span v-html="$t('error.msg002')"></span></p>
                <p>（{{ $t("error.msg003") }}：{{axiosError}}）</p>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="green darken-1" text @click="reload">{{ $t("error.msg004") }}</v-btn>
                <v-spacer></v-spacer>
            </v-card-actions>
        </v-card>
    </v-dialog>
    <!-- LINEPay会計エラーの場合 -->
    <v-dialog v-model="isPaymentError" persistent max-width="500">
        <v-card>
            <v-card-title><v-icon large color="error">error</v-icon>{{ $t("error.msg005") }}</v-card-title>
            <v-card-text>
                <p><span v-html="$t('error.msg006')"></span></p>
                <p>（{{ $t("error.msg003") }}：{{axiosError}}）</p>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="green darken-1" text @click="payment">{{ $t("error.msg007") }}</v-btn>
                <v-spacer></v-spacer>
            </v-card-actions>
        </v-card>
    </v-dialog>
</div>
</template>
<script>
/**
 * 通信エラーダイアログ
 * 
 */
import {mapGetters} from 'vuex'
export default {
    computed:{
        ...mapGetters(['axiosError', 'isAxiosError', 'isPaymentError']),
    },
    methods: {
        /**
         * 画面リロード処理
         * 
         */
        reload() {
            location.reload();
            return;
        },
        /**
         * 注文履歴画面へ遷移
         * 
         */
        payment() {
            this.$store.commit("axiosError", null);
            this.$store.commit("paymentError", false);
            this.$router.push('/tableorder/payment');
            return;
        }
    }
}
</script>