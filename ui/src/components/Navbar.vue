<template>
  <b-navbar>
    <template slot="brand">
      <b-navbar-item>
        <i class="fas fa-globe-americas mr-2"></i>
        <router-link to="/"> <b>Global Mobility Dashboard</b> </router-link>
      </b-navbar-item>
    </template>

    <template slot="end">
      <b-navbar-item>
        <router-link to="/"> Help </router-link>
      </b-navbar-item>

      <b-navbar-item>
        <a :href="logoutURL"> Log out </a>
      </b-navbar-item>
    </template>
  </b-navbar>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  computed: {
    logoutURL(): string {
      return `${process.env.VUE_APP_SERVER_URL}/accounts/logout/`;
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