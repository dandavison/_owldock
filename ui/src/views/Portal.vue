<template>
  <client-portal v-if="isClientContact" />
  <provider-portal v-else-if="isProviderContact" />
  <section v-else class="section">
    We're sorry, but you seem to be neither a provider nor a client of a
    provider, so this page is all there is.
  </section>
</template>

<script lang="ts">
import Vue from "vue";
import Cookies from "js-cookie";

import ClientPortal from "./ClientPortal.vue";
import ProviderPortal from "./ProviderPortal.vue";

export default Vue.extend({
  components: { ClientPortal, ProviderPortal },
  computed: {
    isClientContact(): boolean {
      return Cookies.get("role") === "client-contact";
    },

    isProviderContact(): boolean {
      return Cookies.get("role") === "provider-contact";
    },
  },
});
</script>
