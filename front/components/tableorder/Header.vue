<template>
    <v-app-bar app class="elevation-1">
        <v-toolbar-title>
            <v-btn class="grey lighten-4 px-1" v-on:click="menu">
                <v-icon>keyboard_arrow_left</v-icon><span class="">Menu</span>
            </v-btn>
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-toolbar-items class="hidden-xs-only">
            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-avatar style="margin:auto;">
                        <v-img max-width="50" class="ma-2" v-bind:src="customer.image" v-bind="attrs" v-on="on"></v-img>
                    </v-avatar>
                </template>
                <span>{{ $t("header.msg001", { name: customer.name }) }}</span>
            </v-tooltip>
            <span class="hidden-sm-and-down font-weight-bold" style="font-size:1.2em; margin:auto; margin-left:12px;">{{ $t("header.msg001", { name: customer.name }) }}</span>
            <span style="font-size:1.0em; margin:auto; margin-left:12px;">{{ $t("header.msg002") }}: {{ customer.seatNo }}</span>
        </v-toolbar-items>
        <v-spacer></v-spacer>
        <v-toolbar-items class="hidden-sm-and-up pr-3">
            <span style="font-size:14px; margin:auto;">{{ $t("header.msg002") }}: {{ customer.seatNo }}</span>
        </v-toolbar-items>
    </v-app-bar>
</template>

<script>
/**
 * テーブルオーダーヘッダー
 * 
 */
export default {
    props: {
        customer: {
            type: Object,
            required: true,
            default: null,
        },
        basketed: {
            type: Boolean,
            required: false,
            default: false,
        },
        // color: {
        //     type: String,
        //     required: false,
        //     default: null,
        // },
        paymentId: {
            type: String,
            required:false,
            default: null,
        }
    },
    computed: {
        // count() {
        //     let ret = 0;
        //     const orders = this.$store.state.orders
        //     if (orders) {
        //         for (const category in orders) {
        //             const order = orders[category];
        //             for (const name in order) {
        //                 ret += parseInt(order[name].count, 10);
        //             }
        //         }
        //     }
        //     return ret;
        // }
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
         * バスケット画面へ遷移
         * 
         */
        basket() {
            this.$router.push("/tableorder/basket");
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
