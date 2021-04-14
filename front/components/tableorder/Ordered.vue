<template>
    <v-container fluid>
        <v-row>
            <v-col cols="4" md="4" align="center" style="margin: auto;">{{ $t("ordered.msg001") }}</v-col>
            <v-col cols="3" md="3" align="center" style="margin: auto;">{{ $t("ordered.msg002") }}</v-col>
            <v-col cols="2" md="2" align="center" style="margin: auto;">{{ $t("ordered.msg003") }}</v-col>
            <v-col cols="3" md="3" align="center" style="margin: auto;">{{ $t("ordered.msg004") }}<span style="font-size:0.8em;"></span></v-col>
        </v-row>
        <div class="px-1"><v-divider></v-divider></div>
        <v-row v-for="order in value" v-bind:key="order.itemId" justify="center" align-content="center">
            <v-col class="hidden-xs-only" sm="2"  style="margin:auto;">
                <v-img max-width="200" max-height="150" class="mx-auto" v-bind:src="order.imageUrl" />
            </v-col>
            <v-col cols="4" sm="2" class="text-center ma-auto" align="center">
                <v-img class="hidden-sm-and-up mx-auto" width="90" max-height="80" v-bind:src="order.imageUrl" />
                <span class="font-weight-bold">
                    {{ order.itemName }}
                    <span v-show="order.discountWay!=0" class="red white--text ml-1 px-1 rounded-pill" style="white-space: nowrap;">
                        <span v-show="order.discountWay==1">-{{ $t("ordered.yen", { price: order.discountRate }) }}</span>
                        <span v-show="order.discountWay==2">-{{ order.discountRate }}%</span>
                    </span>
                </span>
            </v-col>
            <v-col cols="3" align="center" class="ma-auto">
                    <span style="font-size:1.1em;">{{ $t("ordered.yen", { price: (order.price - $tableorder.utils.getDiscountPrice(order)) }) }}</span>
            </v-col>
            <v-col cols="2" align="center" class="ma-auto">
                    <span style="font-size:1.1em;">{{ order.orderNum }}</span>
            </v-col>
            <v-col cols="3" align="center" class="ma-auto">
                    <span style="font-size:1.1em;">{{ $t("ordered.yen", { price: ((order.price - $tableorder.utils.getDiscountPrice(order)) * order.orderNum) }) }}</span>
            </v-col>
        </v-row>

        <v-row>        
            <v-spacer></v-spacer>
            <v-col cols="7" md="8" class="my-2">
                <span class="font-weight-bold float-right" style="font-size:1.2em;">{{ $t("ordered.msg005") }}</span>
            </v-col>
            <v-col cols="4" md="2" class="pr-3 my-auto">
                <span class="font-weight-bold float-right" style="font-size:1.2em;">{{orderTotal(value)}}</span>
            </v-col>
            <v-spacer></v-spacer>
        </v-row>
    </v-container>
</template>

<script>
/**
 * 注文履歴内の商品一覧
 * 
 */
export default {
    props: {
        value: {
            type: Array,
            required: true,
            default: null,
        },
    },
    data() {
        return {
        }
    },
    methods: {
        /**
         * 注文ごとの合計金額計算
         * 
         * @param {Object} order 商品情報
         * @returns {string} 合計金額
         */
        orderTotal(order) {
            let totalPrice = 0;
            for (const orderId in order) {
                const item = order[orderId];
                const price = item.price - this.$tableorder.utils.getDiscountPrice(item);
                totalPrice = totalPrice + price * item.orderNum;
            }
            return this.$t("ordered.yen", { price: totalPrice.toLocaleString()});
        },
    }
}
</script>

<style scoped>
.v-expansion-panel-content >>> .v-expansion-panel-content__wrap { 
    padding: 0px;
 }
</style>
