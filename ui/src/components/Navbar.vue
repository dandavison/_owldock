<template>
  <b-navbar centered>
    <template slot="brand">
      <b-navbar-item>
        <router-link to="/portal">
          <img v-if="logoUrl" :src="logoUrl" height="24px" />
          <i v-else class="fas fa-globe-americas"></i>
        </router-link>
      </b-navbar-item>

      <b-navbar-item>
        <router-link to="/portal">
          <span style="font-size: x-large">🦉</span>Owldock
        </router-link>
      </b-navbar-item>
    </template>

    <template slot="start">
      <b-navbar-item>
        <span class="route-name-override">{{
          routeNameOverride || $route.name
        }}</span>
      </b-navbar-item>
    </template>

    <template slot="end">
      <b-navbar-dropdown :label="loggedInUserName || 'Account'" arrowless>
        <b-navbar-item>
          <a :href="logoutURL"> Log out </a>
        </b-navbar-item>
      </b-navbar-dropdown>
    </template>
  </b-navbar>
</template>

<script lang="ts">
import Vue from "vue";
import Cookies from "js-cookie";

import eventBus from "../event-bus";

export default Vue.extend({
  data() {
    return {
      currentViewTitle: "",
      routeNameOverride: "",
    };
  },

  mounted() {
    eventBus.$on("update:route-name-override", (title: string) => {
      this.routeNameOverride = title;
    });
  },

  computed: {
    logoutURL(): string {
      return `${process.env.VUE_APP_SERVER_URL}/accounts/logout/`;
    },

    loggedInUserName(): string | undefined {
      return Cookies.get("username");
    },

    logoUrl(): string | undefined {
      return Cookies.get("logo_url");
    },
  },
});
</script>

<style scoped>
a,
a:hover {
  color: currentColor;
}
.route-name-override {
  font-weight: bold;
  font-style: italic;
}
</style>
