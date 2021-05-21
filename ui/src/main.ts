import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

import Buefy from "buefy";
import "buefy/dist/buefy.css";
import "../node_modules/@fortawesome/fontawesome-free/js/all.js";

import App from "./App.vue";
import { getRole, Role } from "./role";
import eventBus from "./event-bus";

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

function ClientProviderRelationshipList() {
  switch (getRole()) {
    case Role.ClientContact:
      return import("./views/ClientProviderRelationshipList.vue");
    case Role.ProviderContact:
      return import("./views/ProviderPortal.vue");
    case Role.Invalid:
      return import("./views/InvalidRole.vue");
  }
}

function ApplicantList() {
  switch (getRole()) {
    case Role.ClientContact:
      return import("./views/ClientApplicantList.vue");
    case Role.ProviderContact:
      return import("./views/ProviderApplicantList.vue");
    case Role.Invalid:
      return import("./views/InvalidRole.vue");
  }
}

function Assessment() {
  switch (getRole()) {
    case Role.ClientContact:
      return import("./views/Assessment.vue");
    case Role.ProviderContact:
      return import("./views/InvalidRole.vue");
    case Role.Invalid:
      return import("./views/InvalidRole.vue");
  }
}

function Plan() {
  switch (getRole()) {
    case Role.ClientContact:
      return import("./views/Plan.vue");
    case Role.ProviderContact:
      return import("./views/InvalidRole.vue");
    case Role.Invalid:
      return import("./views/InvalidRole.vue");
  }
}

function Initiate() {
  switch (getRole()) {
    case Role.ClientContact:
      return import("./views/Initiate.vue");
    case Role.ProviderContact:
      return import("./views/InvalidRole.vue");
    case Role.Invalid:
      return import("./views/InvalidRole.vue");
  }
}

function Move() {
  switch (getRole()) {
    case Role.ClientContact:
      return import("./views/Move.vue");
    case Role.ProviderContact:
      return import("./views/InvalidRole.vue");
    case Role.Invalid:
      return import("./views/InvalidRole.vue");
  }
}

function Report() {
  switch (getRole()) {
    case Role.ClientContact:
      return import("./views/Report.vue");
    case Role.ProviderContact:
      return import("./views/InvalidRole.vue");
    case Role.Invalid:
      return import("./views/InvalidRole.vue");
  }
}

const AccessData = () => import("./views/AccessData.vue");
const NewCase = () => import("./views/NewCase.vue");
const ProcessSteps = () => import("./views/ProcessSteps.vue");

Vue.config.productionTip = false;
Vue.use(Buefy, {
  defaultIconPack: "fas",
  defaultContainerElement: "#content",
});

const routes = [
  { path: "/", component: Portal, name: "Home" },
  { path: "/portal", component: Portal, name: "Portal" },
  { path: "/portal/plan", component: Plan, name: "Plan" },
  { path: "/portal/initiate", component: Initiate, name: "Initiate" },
  { path: "/portal/move", component: Move, name: "Move" },
  { path: "/portal/report", component: Report, name: "Report" },
  { path: "/portal/assessment", component: Assessment, name: "Assessment" },
  { path: "/portal/my-data", component: AccessData, name: "My Data" },
  { path: "/portal/new-case", component: NewCase, name: "New Case" },
  { path: "/portal/cases", component: CaseList, name: "My Cases" },
  { path: "/portal/case/:uuid", component: Case, name: "Case" },
  { path: "/portal/applicants", component: ApplicantList, name: "Applicants" },
  {
    path: "/portal/providers",
    component: ClientProviderRelationshipList,
    name: "My Providers",
  },
  {
    path: "/portal/process/:id/steps/",
    component: ProcessSteps,
    name: "Process steps",
    props: true,
    meta: { navbar: false },
  },
];

const router = new VueRouter({ mode: "history", routes });

router.afterEach(() => {
  eventBus.$emit("update:route-name-override", null);
});

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
