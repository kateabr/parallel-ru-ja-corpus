import Vue from "vue";
import { store, vuetifyRestoreHook } from "@/plugins/store";
import { vuetify } from "@/plugins/vuetify";

import App from "@/layouts/MainLayout.vue";
import { router } from "@/router";

new Vue({
  store,
  router,
  vuetify,
  beforeCreate: vuetifyRestoreHook,
  render: h => h(App)
}).$mount("#app");
