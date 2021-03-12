import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

import Buefy from "buefy";
import "buefy/dist/buefy.css";
import "../node_modules/@fortawesome/fontawesome-free/js/all.js";

import App from "./App.vue";
const Home = () => import("./views/Home.vue");
const AskAQuestion = () => import("./views/AskAQuestion.vue");
const InitiateNewWork = () => import("./views/InitiateNewWork.vue");
const ViewWIP = () => import("./views/ViewWIP.vue");
const AccessData = () => import("./views/AccessData.vue");

Vue.config.productionTip = false;
Vue.use(Buefy, {
  defaultIconPack: "fas",
  defaultContainerElement: "#content"
});

const routes = [
  { path: "/", component: Home },
  { path: "/question", component: AskAQuestion },
  { path: "/initiate-new-work", component: InitiateNewWork },
  { path: "/work-in-progress", component: ViewWIP },
  { path: "/access-data", component: AccessData }
];

const router = new VueRouter({ mode: "history", routes });

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
