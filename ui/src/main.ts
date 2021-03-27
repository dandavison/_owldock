import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

import Buefy from "buefy";
import "buefy/dist/buefy.css";
import "../node_modules/@fortawesome/fontawesome-free/js/all.js";

import App from "./App.vue";
const Home = () => import("./views/Home.vue");
const ClientPortal = () => import("./views/ClientPortal.vue");
const NewCase = () => import("./views/NewCase.vue");
const ViewCase = () => import("./views/ViewCase.vue");
const ClientCaseList = () => import("./views/ClientCaseList.vue");
const AskAQuestion = () => import("./views/AskAQuestion.vue");
const AccessData = () => import("./views/AccessData.vue");
const ProviderPortal = () => import("./views/ProviderPortal.vue");

Vue.config.productionTip = false;
Vue.use(Buefy, {
  defaultIconPack: "fas",
  defaultContainerElement: "#content"
});

const routes = [
  { path: "/", component: Home },
  { path: "/client", component: ClientPortal },
  { path: "/client/my-data", component: AccessData },
  { path: "/client/new-case", component: NewCase },
  { path: "/client/cases", component: ClientCaseList },
  { path: "/client/case/:id", component: ViewCase },
  { path: "/client/question", component: AskAQuestion },
  { path: "/provider", component: ProviderPortal }
];

const router = new VueRouter({ mode: "history", routes });

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
