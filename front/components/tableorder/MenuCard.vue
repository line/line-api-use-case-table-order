<template>
<div style="position: relative;">
    <div v-show="menu.stockoutFlg" style="position:absolute; top: 35%; left: 20%; z-index: 1;">
        <span class="red--text text-h3 font-weight-bold" style="-webkit-text-stroke-width: 1px; -webkit-text-stroke-color: white;">Sold out</span>
    </div>
    
    <v-hover v-slot:default="{ hover }" open-delay="150">
        <div>
            <!-- 商品カード SP -->
            <v-card class="hidden-sm-and-up menu" v-bind:elevation="hover ? 10 : 0" @click="openDialog" :disabled="menu.stockoutFlg" height="190px" flat>
                <v-row class="ma-0 pa-1">
                    <v-col cols=12 lg=6 align="center" class="pt-1 pb-0">
                        <div style="width: 100%; height: 50%;">
                            <span 
                                v-show="isDiscounted"
                                class="red white--text rounded-pill text-caption py-0 px-2"
                                style="position: absolute;top:10px;right:0px; transform: rotate(20deg); opacity: 0.9; z-index: 1;">
                                <span v-if="menu.discountWay==1">SALE -{{ $t("menucard.yen", { price: menu.discountRate }) }}</span>
                                <span v-if="menu.discountWay==2">SALE -{{ menu.discountRate }}%</span>
                            </span>
                            <div style="width:100%; height: 100px; margin:0 auto;">
                                <v-img  style="width:100%; max-height: 100%;" v-bind:src="menu.imageUrl" />
                            </div>
                        </div>
                    </v-col>
                    <v-col cols=12 lg=6 class="pa-0">
                        <v-card-title class="text-body-2 py-0">{{ menu.itemName }}</v-card-title>
                        <v-card-title class="py-0">
                            <!-- 割引がある場合 -->
                            <span v-if="isDiscounted" class="text-caption" style="text-decoration: line-through;">{{ $t("menucard.yen", { price: menu.price.toLocaleString() }) }}</span>
                            <span v-if="isDiscounted" class="text-body-2 red--text font-weight-bold"> → {{ $t("menucard.yen", { price: discountPrice.toLocaleString() }) }}</span> 
                            <!-- 割引がない場合 -->
                            <span v-else class="text-caption">{{ $t("menucard.yen", { price: menu.price.toLocaleString() }) }}</span>
                        </v-card-title>
                    </v-col>
                </v-row>
            </v-card>

            <!-- 商品カード PC-->
            <v-card class="hidden-xs-only menu" v-bind:elevation="hover ? 16 : 2" @click="openDialog" :disabled="menu.stockoutFlg" height="330px">
                <v-row class="ma-0 pa-3">
                    <v-col cols=12 align="center">
                        <div style="height: 150px; width: 240px;">
                            <span 
                                v-show="isDiscounted"
                                class="red white--text rounded-pill text-body-1 py-2 px-3"
                                style="position: absolute;top:10px;left:-15px; transform: rotate(-30deg); opacity: 0.9; z-index: 1;">
                                <span v-if="menu.discountWay==1">SALE -{{ $t("menucard.yen", { price: menu.discountRate }) }}</span>
                                <span v-if="menu.discountWay==2">SALE -{{ menu.discountRate }}%</span>
                            </span>
                            <img v-bind:src="menu.imageUrl" style="max-width: 240px; width: auto; height:150px; margin: 0 auto 0;">
                        </div>
                    </v-col>
                    <v-col cols=12 class="pa-0">
                        <v-card-title class="pt-2 pb-0">{{ menu.itemName }}</v-card-title>
                        <v-card-title class="py-0">
                            <!-- 割引がある場合 -->
                            <span v-if="isDiscounted">
                                <span class="text-body-2" style="text-decoration: line-through;">{{ $t("menucard.yen", { price: menu.price.toLocaleString() }) }}</span>
                                <span class="px-1"><v-icon style="vertical-align: top;">redo</v-icon></span>
                                <span class="red--text font-weight-bold">{{ $t("menucard.yen", { price: discountPrice.toLocaleString() })  }}</span>
                            </span>
                            <!-- 割引がない場合 -->
                            <span v-else>{{ $t("menucard.yen", { price: (menu.price).toLocaleString() }) }}</span>
                        </v-card-title>
                        <v-card-text>
                            <span style="color:gray;" class="text-body-2 gray--text pt-1">{{ menu.itemDespription }}</span>
                        </v-card-text>
                    </v-col>
                </v-row>
            </v-card>
        </div>
    </v-hover>
</div>
</template>
<script>
/**
 * メニューカード
 * 
 */
export default {
    props: {
        menu: {
            type: Object,
            required: true,
            default: null,
        },
    },
    computed: {
        discountPrice() {
            return this.menu.price - this.$tableorder.utils.getDiscountPrice(this.menu);
        },
        isDiscounted() {
            return this.menu.discountWay != 0;
        }
    },
    methods: {
        /**
         * 押下されたメニューの注文用ダイアログを開く
         * 
         */
        openDialog() {
            this.$emit('openDialog');
        }
    }
}
</script>