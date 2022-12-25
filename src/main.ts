//main.ts
import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import { createPinia } from "pinia";
import App from "./App.vue";
import "vuetify/styles";
import { createVuetify, ThemeDefinition } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import "uno.css";
import { Icon } from "@iconify/vue";
import generatedRoutes from "virtual:generated-pages";
import { setupLayouts } from "virtual:generated-layouts";
import "@mdi/font/css/materialdesignicons.css";
import { createAuth0 } from "@auth0/auth0-vue";

const routes = setupLayouts(generatedRoutes);

createApp(App)
  .use(
    createRouter({
      history: createWebHistory(import.meta.env.BASE_URL),
      routes,
    })
  )
  .use(
    createAuth0({
      domain: "dev-tvhqmk7a.us.auth0.com",
      client_id: "53p0EBRRWxSYA3mSywbxhEeIlIexYWbs",
      redirect_uri: window.location.origin,
    })
  )
  .use(createPinia())
  .use(
    createVuetify({
      components,
      directives,
    })
  )
  .component("Icon", Icon)
  .mount("#app");
