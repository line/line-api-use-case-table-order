<template>
    <v-app class="table-order-font-size">
        <!-- Header -->
        <vue-header v-bind:customer="customer" v-bind:paymentId="paymentId"></vue-header>
        <!-- Order List -->
        <v-container fluid class="mt-15">
            <v-row>
                <v-col cols="1" md="1" align="center"></v-col>
                <v-col cols="4" md="4" align="center" style="margin: auto;">{{ $t("basket.product") }}</v-col>
                <v-col cols="3" md="3" align="center" style="margin: auto;">{{ $t("basket.qty") }}</v-col>
                <v-col cols="4" md="4" align="center" style="margin: auto;">{{ $t("basket.price") }}</v-col>
            </v-row>
            <v-row v-for="(order, index) in orders" v-bind:key="order.name">
                <v-col cols="1" class="text-center" align="center" style="margin: auto;">
                    <v-btn outlined fab small color="error" class="hidden-xs-only" v-on:click="remove(index, order)">
                        <v-icon>mdi-minus</v-icon>
                    </v-btn>
                    <v-btn outlined fab small color="error" class="hidden-sm-and-up" style="width:25px; height:25px;" v-on:click="remove(index, order)">
                        <v-icon>mdi-minus</v-icon>
                    </v-btn>
                </v-col>
                <v-col class="hidden-xs-only" sm="2" style="margin:auto;">
                    <v-img class="mx-auto" max-width="200" max-height="150" v-bind:src="order.order.imageUrl" />
                </v-col>
                <v-col cols="4" sm="2" class="text-center ma-auto" align="center">
                    <v-img class="hidden-sm-and-up mx-auto" width="90" max-height="80" v-bind:src="order.order.imageUrl" />
                    <v-tooltip right>
                        <template v-slot:activator="{ on, attrs }">
                            <span class="text-body-2" v-bind="attrs" v-on="on">
                                {{ order.order.itemName }}
                                <span v-show="order.order.discountWay!=0" class="red white--text ml-1 px-1 rounded-pill" style="white-space: nowrap;">
                                    <span v-show="order.order.discountWay==1">-{{ $t("basket.yen", { price: order.order.discountRate }) }}</span>
                                    <span v-show="order.order.discountWay==2">-{{ order.order.discountRate }}%</span>
                                </span>
                            </span>
                        </template>
                        <span>{{ $t("basket.yen", { price: parseInt(order.order.price).toLocaleString()}) }}</span>
                    </v-tooltip>
                </v-col>
                <v-col cols="3" align="center" class="ma-auto">
                    <div class="mt-5" min-width="50">
                        <v-text-field
                            type="number"
                            reverse
                            outlined
                            height="56"
                            min="0"
                            max="99"
                            v-model="order.count"
                            oninput="if(Number(this.value) < Number(this.min)) this.value = this.min;if(Number(this.value) > Number(this.max)) this.value = this.max;"
                            v-on:change="modify(order)"
                        ></v-text-field>
                    </div>
                </v-col>
                <v-col cols="4" align="center" class="ma-auto">
                    <p v-if="order.order.discountWay!=0">
                        <span class="text-caption text-decoration-line-through">{{ $t("basket.yen", { price: (order.order.price * order.count).toLocaleString() + " "  }) }}</span><br>
                        <span class="text-body-2 red--text font-weight-bold">{{ $t("basket.yen", { price: ((order.order.price - $tableorder.utils.getDiscountPrice(order.order)) * order.count).toLocaleString()}) }}</span>
                    </p>
                    <p v-else>
                        <span class="text-body-2">{{ $t("basket.yen", { price: (order.order.price * order.count).toLocaleString() }) }}</span>
                    </p>                
                </v-col>
            </v-row>
            <v-divider class="mt-1 mb-5"></v-divider>
            <v-row v-show="totalDiscount!=0">
                <v-spacer></v-spacer>
                <v-col cols="5" class="py-1">
                    <span class="font-weight-bold mr-2">{{ $t("basket.total_pretax") }}</span>
                </v-col>
                <v-col cols="3" class="py-1 mr-5" align="right" style="margin: auto;">
                    <span>{{ $t("basket.yen", { price: beforeDiscount.toLocaleString() }) }}</span>
                </v-col>
            </v-row>
            <v-row v-show="totalDiscount!=0">
                <v-spacer></v-spacer>
                <v-col cols="5" class="py-1">
                    <span class="font-weight-bold mr-2">{{ $t("basket.total_discount") }}</span>
                </v-col>
                <v-col cols="3" class="py-1 mr-5" align="right" style="margin: auto;">
                    <span style="font-size:1.1em;" class="red--text font-weight-bold">- {{ $t("basket.yen", { price: totalDiscount.toLocaleString() }) }}</span>
                </v-col>
            </v-row>
            <v-row>
                <v-spacer></v-spacer>
                <v-col cols="5" class="py-2">
                    <span class="font-weight-bold mr-2" style="font-size:1.1em;">{{ $t("basket.total_amount") }}</span>
                </v-col>
                <v-col cols="3" class="py-2 mr-5 pl-0" align="right">
                    <span v-show="total!=0" style="font-size:1.1em;" class="red--text font-weight-bold">{{ $t("basket.yen", { price: total.toLocaleString() }) }}</span>
                </v-col>
            </v-row>
        </v-container>
        <!-- Order -->
        <div class="text-center mb-15">
            <v-btn x-small class="mb-5" @click="removeAll(false)">{{ $t("basket.msg001") }}</v-btn>
        </div>
        <v-footer fixed height="60px" class="pa-0">
            <v-btn class="white--text" width="100%" height="100%" color="#00B900" v-on:click="orderDialog=true" v-bind:disabled="!orderEnabled">
                <v-icon left>mdi-cash-register</v-icon>&nbsp;<span v-html="$t('basket.msg002')"></span>
            </v-btn>
        </v-footer>
        <!-- Dialog order -->
        <v-dialog v-model="orderDialog" max-width="290">
            <v-card>
                <v-card-title><v-icon color="success">done_outline</v-icon>&nbsp;{{ $t("basket.msg003") }}</v-card-title>
                <v-card-text>{{ $t("basket.msg004") }}</v-card-text>
                <v-card-actions>
                    <v-btn text color="green darken-1" class="text-caption" @click="orderDialog=false">{{ $t("basket.cancel") }}</v-btn>
                    <v-spacer></v-spacer>
                    <v-btn text color="green darken-1" @click="order">OK</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <!-- Dialog All remove -->
        <v-dialog v-model="removeDialog" max-width="290">
            <v-card>
                <v-card-title><span v-html="$t('basket.msg005')"></span></v-card-title>
                <v-card-actions>
                    <v-btn text color="green darken-1" class="text-caption" @click="removeDialog = false">{{ $t("basket.cancel") }}</v-btn>
                    <v-spacer></v-spacer>
                    <v-btn text color="green darken-1" @click="removeAll(true)">OK</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-app>
</template>

<script>
/**
 * バスケット画面
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
        // Orders
        const orders = app.$utils.ocopy(store.state.orders);
        // paymentId
        const paymentId = store.state.paymentId;

        let list = [];
        // カテゴリごとに処理を行う
        for (const categoryId in orders) {
            const order = orders[categoryId];
            for (const itemId in order) {
                const count = parseInt(order[itemId].count, 10);
                const price = parseInt(order[itemId].price, 10);
                const total = parseInt(order[itemId].total, 10);
                const itemData = order[itemId].order;
                list.push({
                    categoryId: categoryId,
                    itemId: itemId,
                    count: count,
                    price: price,
                    total: total,
                    order: itemData,
                });
            }
        }

        return {
            orders: list,
            customer: customer,
            paymentId: paymentId,
        }
    },
    head() {
        return {
            title: this.$t("title")
        }
    },
    data() {
        return {
            orders: null,
            customer: null,
            removeDialog: false,
            orderDialog: false,
            paymentId: null,
        }
    },
    computed: {
        orderEnabled() {
            // 注文ボタン活性制御
            for(const orderNo in this.orders) {
                if(this.orders[orderNo].count === 0) {
                    return false;
                }
            }
            if (this.orders && this.orders.length > 0
                && !isNaN(Number(this.total))) {
                return true;
            }
            return false;
        },
        total: {
            get() {
                let totalPrice = 0;
                for (const idx in this.orders) {
                    const price = parseInt(this.orders[idx].price, 10);
                    const count = parseInt(this.orders[idx].count, 10);
                    totalPrice += price * count;
                }
                if (isNaN(totalPrice)) {
                    totalPrice = 0;
                }
                return totalPrice;
            },
            set(){
            },
        },
        beforeDiscount: {
            get() {
                let beforeDiscount = 0;
                for (const idx in this.orders) {
                    const price = parseInt(this.orders[idx].order.price, 10);
                    const count = parseInt(this.orders[idx].count, 10);
                    beforeDiscount += price * count;
                }
                if (isNaN(beforeDiscount)) {
                    beforeDiscount = 0;
                }
                return beforeDiscount;
            },
            set() {
            },
        },
        totalDiscount: {
            get() {
                let totalDiscount = 0;
                for (const idx in this.orders) {
                    const price = this.$tableorder.utils.getDiscountPrice(this.orders[idx].order);
                    const count = parseInt(this.orders[idx].count, 10);
                    totalDiscount += price * count;
                }
                if (isNaN(totalDiscount)) {
                    totalDiscount = 0;
                }
                return totalDiscount;
            },
            set() {
            },
        },
    },
    methods: {
        /**
         * 商品個数の編集
         * 
         * @param {Object} order 商品情報
         */
        modify(order) {
            if ( order.count <= 0 || isNaN(order.count) ) {
                order.count = 1;
            }
            
            const categoryId = order.categoryId;
            const itemId = order.itemId;
            const price = parseInt(order.price, 10);
            const count = isNaN(order.count) ? 0 : parseInt(order.count, 10);
            order.total = price * count;
            // Modify Session Storage
            const orders = this.$utils.ocopy(this.$store.state.orders);
            orders[categoryId][itemId].count = count;
            orders[categoryId][itemId].total = order.total;
            this.$store.commit("orders", orders);
        },
        /**
         * 商品削除
         * 
         * @param {number} index 削除対象商品のindex番号
         * @param {Object} order 商品情報
         */
        remove(index, order) {
            const categoryId = order.order.categoryId;
            const itemId = order.order.itemId;
            this.orders.splice(index, 1); 
            // Remove Session Storage
            const orders = this.$store.state.orders;
            delete orders[categoryId][itemId];
            this.$store.commit("orders", orders);
            // 0件のときはメニュー画面へ遷移
            if (this.orders.length == 0) {
                this.menu();
            }
        },
        /**
         * 商品全件削除ダイアログ表示・実行
         * 
         * @param {boolean} execute 
         */
        removeAll(execute) {
            if (execute) {
                this.orders = []; 
                this.$store.commit("orders", null);
                this.menu();
                this.removeDialog = false;
            } else {
                this.removeDialog = true;
            }
        },
        /**
         * 商品注文
         * 
         */
        async order() {
            const paymentId = this.$store.state.paymentId;
            const tableId = this.customer.seatNo;
            const orders = this.$utils.ocopy(this.$store.state.orders);

            // 注文送信・注文完了APIにデータ送信
            const response = await this.$tableorder.putOrder(paymentId, tableId, orders);
            this.$store.commit("paymentId", response);
            this.$store.commit("orders", null);
            this.$router.push("/tableorder/completed");
        },
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
