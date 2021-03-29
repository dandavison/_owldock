<template>
  <b-navbar>
    <template slot="brand">
      <b-navbar-item>
        <router-link to="/portal">
          <img v-if="logoUrl" :src="logoUrl" height="24px" />
          <i v-else class="fas fa-globe-americas"></i>
        </router-link>
      </b-navbar-item>

      <b-navbar-dropdown label="🦉 owldock" arrowless>
        <b-navbar-item>
          <router-link to="/portal"> Help </router-link>
        </b-navbar-item>
      </b-navbar-dropdown>
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

export default Vue.extend({
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
</style>