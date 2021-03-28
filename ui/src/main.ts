import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

import Buefy from "buefy";
import "buefy/dist/buefy.css";
import "../node_modules/@fortawesome/fontawesome-free/js/all.js";

import App from "./App.vue";
const Portal = () => import("./views/Portal.vue");
const NewCase = () => import("./views/NewCase.vue");
const ViewCase = () => import("./views/ViewCase.vue");
const CaseList = () => import("./views/CaseList.vue");
const AskAQuestion = () => import("./views/AskAQuestion.vue");
const AccessData = () => import("./views/AccessData.vue");

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
  { path: "/portal/case/:id", component: ViewCase },
  { path: "/portal/question", component: AskAQuestion }
];

const router = new VueRouter({ mode: "history", routes });

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
