<template>
    <div class="wrap" v-show="loggedIn">
        <!--<nuxt keep-alive />-->
        <nuxt />
        <axios-error-modal />
    </div>
</template>

<script>
/**
 * テーブルオーダーレイアウト画面
 */
import "~/assets/css/style.css";
import "~/assets/sass/app.scss";
import AxiosErrorModal from '~/components/ErrorModal.vue'

export default {
    middleware: [
        "initialize"
    ],
    components: {
        AxiosErrorModal
    },
    data() {
        return {
            loggedIn: false,
        }
    },
    created() {
        this.$nuxt.$on("v-show", this.show);
        this.$vuetify.theme.dark = false;
    },
    mounted() {
        liff.ready.then(() => {
            this.loggedIn = liff.isLoggedIn();
        });
    },
    methods: {
    }
}
</script>

<style scoped>
h2 {
    text-align: center;
    margin: 3px;
}
.title {
    font-size: 2.0em;
    color: #fff;
}
.logo {
    width: 60px;
    height: auto;
    text-align: left;
}
.logout {
    margin: 6px;
    text-align: right;
}
</style>
