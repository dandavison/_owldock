import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

import Buefy from "buefy";
import "buefy/dist/buefy.css";
import "../node_modules/@fortawesome/fontawesome-free/js/all.js";

import App from "./App.vue";
import { getRole, Role } from "./role";

import "./dev-mode";

function Portal() {
  switch (getRole()) {
    case Role.ClientContact:
      return import("./views/ClientPortal.vue");
    case Role.ProviderContact:
      return import("./views/ProviderPortal.vue");
    case Role.Invalid:
      return import("./views/InvalidRole.vue");
  }
}

function Case() {
  switch (getRole()) {
    case Role.ClientContact:
      return import("./views/ClientCase.vue");
    case Role.ProviderContact:
      return import("./views/ProviderCase.vue");
    case Role.Invalid:
      return import("./views/InvalidRole.vue");
  }
}

function CaseList() {
  switch (getRole()) {
    case Role.ClientContact:
      return import("./views/ClientCaseList.vue");
    case Role.ProviderContact:
      return import("./views/ProviderCaseList.vue");
    case Role.Invalid:
      return import("./views/InvalidRole.vue");
  }
}

const AccessData = () => import("./views/AccessData.vue");
const AskAQuestion = () => import("./views/AskAQuestion.vue");
const NewCase = () => import("./views/NewCase.vue");

Vue.config.productionTip = false;
Vue.use(Buefy, {
  defaultIconPack: "fas",
  defaultContainerElement: "#content"
});

const routes = [
  { path: "/portal", component: Portal },
  { path: "/portal/my-data", component: AccessData },
  { path: "/portal/new-case", component: NewCase },
  { path: "/portal/cases", component: CaseList },
  { path: "/portal/case/:id", component: Case },
  { path: "/portal/question", component: AskAQuestion }
];

const router = new VueRouter({ mode: "history", routes });

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
