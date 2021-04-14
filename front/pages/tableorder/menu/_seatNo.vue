<template>
    <v-app>
        <!-- Header -->
        <v-app-bar app class="elevation-1">
            <v-menu transition="slide-x-transition" v-bind:close-on-content-click="true" v-model="categoryDialog" ref="menu_list">
                <template v-slot:activator="{ on, attrs }">
                    <v-app-bar-nav-icon v-on="on" v-bind="attrs"></v-app-bar-nav-icon>
                </template>
                <v-list shaped>
                    <v-subheader>Menu Category</v-subheader>
                    <v-list-item v-on:click="search(category.categoryId, category.categoryName)" v-for="category in categoryList" :key="category.id">
                        <v-list-item-avatar>
                            <v-icon v-if="category.categoryId==0">grade</v-icon>
                            <v-icon v-if="category.categoryId==1">local_bar</v-icon>
                            <v-icon v-if="category.categoryId==2">directions_run</v-icon>
                            <v-icon v-if="category.categoryId==3">fas fa-utensils</v-icon>
                            <v-icon v-if="category.categoryId==5">fas fa-clock</v-icon>
                            <v-icon v-if="category.categoryId==10">grade</v-icon>
                            <v-icon v-if="category.categoryId==11">local_bar</v-icon>
                            <v-icon v-if="category.categoryId==12">directions_run</v-icon>
                            <v-icon v-if="category.categoryId==13">fas fa-utensils</v-icon>
                            <v-icon v-if="category.categoryId==15">fas fa-clock</v-icon>
                        </v-list-item-avatar>
                        <v-list-item-content>
                            <v-list-item-title>{{ category.categoryName }}</v-list-item-title>
                        </v-list-item-content>
                        <v-list-item-action>
                        </v-list-item-action>
                    </v-list-item>
                </v-list>
            </v-menu>
            <v-spacer></v-spacer>
            <v-toolbar-items class="hidden-xs-only">
                <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                        <v-avatar style="margin:auto;">
                            <v-img max-width="50" class="ma-2" v-bind:src="customer.image" v-bind="attrs" v-on="on"></v-img>
                        </v-avatar>
                    </template>
                    <span>{{ $t("menu.msg001", { name: customer.name }) }}</span>
                </v-tooltip>
                <span class="hidden-sm-and-down font-weight-bold ma-auto ml-5" style="font-size:1.2em;">{{ $t("menu.msg001", { name: customer.name }) }}</span>
                <span class="ma-auto ml-5" v-show="!seatNoModal">{{ $t("menu.msg002") }}: {{ customer.seatNo }}</span>
            </v-toolbar-items>
            <v-spacer></v-spacer>
            <v-toolbar-items>
                <div class="ma-auto">
                    <v-toolbar-title>
                        <v-btn outlined class="grey lighten-4 pr-0 font-weight-bold" color="#00B900" v-on:click="payment" v-bind:disabled="paymentId==null">
                            <span>&nbsp;&nbsp;<span v-html="$t('menu.msg003')"></span></span>
                            <v-icon>keyboard_arrow_right</v-icon>
                        </v-btn>
                    </v-toolbar-title>
                </div>
            </v-toolbar-items>
        </v-app-bar>

        <!-- Menu -->
        <v-container fluid style="margin:56px 0;">
            <v-row class="my-0">
                <v-col cols="12" style="text-align:center;">
                    <h2>{{ categoryName }}</h2>
                    <hr style="width:85%; margin:0 auto;" />
                </v-col>
            </v-row>
            <v-row class="mx-auto my-0" width="98%">
                <v-col cols="6"  md="4" v-for="menu in menuList" v-bind:key="menu.itemName" class="pa-2">
                    <menu-card :menu="menu" @openDialog="openDialog(menu)"/>
                </v-col>
            </v-row>
        </v-container>
        <v-footer fixed style="" class="pa-0" height="60px">
             <v-btn class="basket" color="#00B900" v-on:click="basket" style="color:#fff; width:100%; height:100%;" v-bind:disabled="count==0">
                <v-icon left>mdi-basket</v-icon><span v-html="$t('menu.msg004')"></span><span>({{count}}{{ $t("menu.msg005") }})</span>
            </v-btn>
        </v-footer>

        <!-- Dialog -->
        <v-dialog v-model="menuDialog" max-width="350">
            <v-card>
                <v-btn icon v-on:click="menuDialog=false">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
                <v-card-title class="justify-center py-1">
                    <img v-bind:src="addToBasket.order.imageUrl" style="width:auto;max-width:280px; max-height:230px">
                </v-card-title>
                <v-card-title class="justify-center pt-1 pb-0">
                    <span>{{ addToBasket.order.itemName }}</span>
                </v-card-title>
                <v-card-text>
                        <span style="color:gray;" class="text-caption gray--text pt-1">{{ addToBasket.order.itemDespription }}</span>
                </v-card-text>
                <v-card-text class="pb-0 px-3">
                    <v-row class="my-0">
                        <v-col cols="4" align="center" class="pa-0">
                            <!-- 割引ありの場合 -->
                            <v-badge
                                v-if="addToBasket.isDiscounted"
                                light left
                                color="deep-orange" 
                                content="SALE"
                                style="margin-left: 25px;"
                                transition="slide-x-transition">
                                <span class="font-weight-bold red--text" style="font-size:1.2em;">{{ $t("menu.msg006", { price: addToBasket.discountedPrice}) }}</span>
                            </v-badge>
                            <!-- 割引なしの場合 -->
                            <span v-else class="font-weight-bold" style="font-size:1.3em;">{{ $t("menu.msg006", { price: addToBasket.order.price}) }}</span>
                        </v-col>
                        <v-col cols="1" align="center" class="pa-0">
                            <span class="font-weight-bold" style="font-size:1.3em;">×</span>
                        </v-col>
                        <v-col cols="4" class="pa-0">
                            <div style="text-align: center; border-bottom: solid 1px #c9c9c9;" class="pb-1">
                                <v-btn outlined fab small color="error" style="width:25px; height:25px; float: left; touch-action: manipulation;" v-on:click="plusminus(-1)">
                                    <v-icon>mdi-minus</v-icon>
                                </v-btn>
                                <span style="font-size:1.3em;" class="font-weight-bold">{{ addToBasket.number }}</span>
                                <v-btn outlined fab small color="success" style="width:25px; height:25px; float:right; touch-action: manipulation;" v-on:click="plusminus(1)">
                                    <v-icon>mdi-plus</v-icon>
                                </v-btn>
                            </div>
                        </v-col>
                        <v-col cols="3" align="center" class="pa-0" style="margin:auto;">
                            <span class="font-weight-bold" style="font-size:1.1em;">{{ $t("menu.msg007") }}</span>
                        </v-col>
                    </v-row>
                    <v-row class="my-0">
                        <v-col cols="12" align="center" class="pa-0 pt-5">
                            <v-btn tile color="#00B900" class="px-0 white--text text-body-1 font-weight-bold" v-on:click="order(addToBasket)" style="height:60px; width:100%">
                                <span>{{ $t("menu.msg008") }}</span>
                                <v-icon small>mdi-share</v-icon>
                                <v-icon>mdi-basket</v-icon>
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-card-text>
            </v-card>
        </v-dialog>
        
        <!-- 座席番号モーダル -->
        <v-dialog v-model="seatNoModal" persistent width="350">
            <v-card>
                <v-card-title class="justify-center">{{ $t("menu.msg009") }}</v-card-title>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-text-field 
                        regular
                        v-bind:label="$t('menu.msg010')" 
                        v-bind:rules="[required, numberOnly]"
                        class="mr-3 mt-3" style="width: 50px;" 
                        v-model="seatNo"></v-text-field>
                    <v-btn tile color="#00B900" class="px-5 white--text text-body-1 font-weight-bold" v-on:click="setSeatNo()">{{ $t("menu.msg011") }}</v-btn>
                    <v-spacer></v-spacer>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-app>
</template>

<script>
/**
 * メニュー画面
 * 
 */
import MenuCard from "~/components/tableorder/MenuCard.vue"
export default {
    layout: "tableorder/order",
    components: {
        MenuCard,
    },
    async asyncData({ app, store, params, $axios }) {
        // storeからcustomerデータ取得
        let customer = app.$utils.ocopy(store.state.lineUser);
        if (!customer) {
            const lineUser = await app.$liff.getLiffProfile();
            store.commit("lineUser", lineUser);
            customer = app.$utils.ocopy(lineUser);
        }
        delete customer['expire'];

        // 席番号取得　取得できない場合は席番号入力モーダル表示
        let seatNoModal = true;
        if (("seatNo" in params && String(params.seatNo).match(/^[0-9]*$/g))) {
            seatNoModal = false;
            customer['seatNo'] = params.seatNo;
        } 

        // 商品一覧情報取得APIからメニューデータ取得
        const itemResponse = await app.$tableorder.getItemData();
        const menuList = itemResponse.items;
        const categoryName = itemResponse.categoryName;

        // カテゴリー一覧取得APIからカテゴリー一覧取得
        const categoryList =await app.$tableorder.getCategoryData();

        // paymentIdが存在しない場合には取得を試みる
        let paymentId = store.state.paymentId;
        if (paymentId == null) {
            let paymentIdResponse = await app.$tableorder.getPaymentId();
            paymentId = !paymentIdResponse ? null : paymentIdResponse;
        }

        return {
            customer: customer,
            menuList: menuList,
            categoryName: categoryName,
            categoryList: categoryList,
            paymentId: paymentId,
            seatNoModal: seatNoModal,
        }
    },
    mounted() {
        this.$nextTick(()=>{
        });
    },
    head() {
        return {
            title: this.$t("title")
        }
    },
    data() {
        return {
            customer: {
                seatNo: null,
                userId: null,
                name: null,
                image: null,
                token: null,
            },
            menuList: null,
            categoryName: null,
            categoryList: null,
            paymentId: null,
            categoryDialog: false,
            menuDialog: false,
            addToBasket: {
                category: null,
                categoryIcon: null,
                itemId: null,
                number: null,
                discountedPrice: null,
                isDiscounted: false,
                order: {},
            },
            seatNoModal: null,
            required: value => !!value || this.$t("menu.msg012"),
            numberOnly: value => String(value).match(/^[0-9]*$/g) != null || this.$t("menu.msg013"),
        }
    },
    computed: {
        count() {
            //バスケット内の個数
            let ret = 0;
            const orders = this.$store.state.orders;
            if (orders) {
                for (const category in orders) {
                    const order = orders[category];
                    for (const name in order) {
                        ret += parseInt(order[name].count, 10);
                    }
                }
            }
            return ret;
        },
        seatNo: {
            get() {
                return this.$store.state.customer.seatNo;
            },
            set(val) {
                const customer = this.$utils.ocopy(this.$store.state.customer);
                customer['seatNo'] = val;
                this.$store.commit("customer", customer);
                this.customer.seatNo = val;
            }
        },
    },
    created() {
        this.$store.commit("customer", this.customer);
        this.$store.commit("paymentId", this.paymentId);
    },
    methods: {
        /**
         * 座席番号のバリデーションチェック・設定
         * 
         */
        setSeatNo() {
            if (!String(this.customer.seatNo).match(/^[0-9]*$/g)) {
                this.seatNoModal = true;
                return;
            }
            this.seatNoModal = false;
        },
        /**
         * 商品カテゴリー検索
         * 
         * @param {number} categoryId カテゴリーID
         * @param {string} categoryName カテゴリー名
         */
        async search(categoryId, categoryName) {
            this.categoryName = categoryName;
            // categoryIdで商品検索
            const itemList = await this.$tableorder.getItemData(categoryId);
            this.menuList = itemList.items;

            this.categoryDialog = false;
        },
        /**
         * 商品個数選択ダイアログ表示
         * 
         * @param {Object} order 商品情報
         */
        openDialog(order) {
            this.addToBasket.itemId = order.itemId;
            this.addToBasket.category = order.categoryName;
            this.addToBasket.itemId = order.itemId;
            this.addToBasket.number = 1;
            this.addToBasket.discountedPrice = order.price - this.$tableorder.utils.getDiscountPrice(order);
            this.addToBasket.isDiscounted = (order.discountWay != 0);
            this.addToBasket.order = order;

            // Open Dialog
            this.menuDialog = true;

        },
        /**
         * 商品個数選択
         * 
         * @param {number} num ボタン押下時に増減させる数
         */
        plusminus(num) {
            if ((num < 0 && this.addToBasket.number <= 1) || (num > 0 && this.addToBasket.number >= 99) ) return;
            this.addToBasket.number += num;
        },
        /**
         * バスケットに商品を追加
         * 
         * @param {Object} addToBasket バスケットに追加する商品情報
         */
        order(addToBasket) {
            const categoryId = addToBasket.order.categoryId;
            const itemId = addToBasket.itemId;  
            const price = parseInt(addToBasket.isDiscounted ? addToBasket.discountedPrice : addToBasket.order.price, 10);
            const number = parseInt(addToBasket.number, 10);
            const order = addToBasket.order;

            // Session Storage
            let orders = this.$utils.ocopy(this.$store.state.orders);
            if (!orders) { orders = {}; }
            if (!(categoryId in orders)) {
                orders[categoryId] = {};
            }

            // すでにバスケット内にあるアイテムであれば個数を加算する
            if (itemId in orders[categoryId]) {
                let count = parseInt(orders[categoryId][itemId].count, 10);
                let total = parseInt(orders[categoryId][itemId].total, 10);
                count += number;
                total += (price * number);

                orders[categoryId][itemId] = { 
                                            price: price,
                                            count: count,
                                            total: total,
                                            order: order,
                                        };
            } else {
                orders[categoryId][itemId] = { 
                                            price: price,
                                            count: number,
                                            total: price * number,
                                            order: order,
                                        };
            }
            this.$store.commit("orders", orders);

            // Clear
            this.addToBasket.category = null;
            this.addToBasket.itemId = null;
            this.addToBasket.number = null;
            this.addToBasket.isDiscounted = false;
            this.addToBasket.discountedPrice = null;
            this.addToBasket.order = {};
            // Close Dialog
            this.menuDialog = false;
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
        },
    }
}
</script>

<style scoped>
html, body {
    margin: 0;
    width: 100%;
    touch-action: manipulation;
}
.top {
    color: #00ba00;
}
.btn {
    margin: 0 6px;
    color: #fff;
}
.basket {
    color: #fff;
    margin: 0px;
    padding: 3px;
    width: 80%;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 0;
    text-align: center;
    cursor: pointer;
}
.basket-small {
    font-size: 16px;
    margin: 2px 12px;
    padding: 10px;
    float: right;
}
.lead {
    text-align: left;
    font-size: 18px;
    margin: 36px;
}
.menu {
    width: auto;
    height: auto;
    padding: 12px;
}
.menu:hover {
    opacity:0.6;
}
.table-order-font-size {
    font-size: 16px;
}
@media screen and (max-width:540px) {
    .table-order-font-size {
        font-size: 12px;
    }
}
.v-text-field ::v-deep .v-input__control .v-input__slot .v-text-field__slot input {
    color: rgba(0, 0, 0, 1);
}
</style>
