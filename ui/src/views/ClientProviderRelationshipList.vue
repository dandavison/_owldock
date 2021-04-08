<template>
  <section class="section">
    <p class="m-4 is-size-2">Providers</p>
    <client-provider-relationship-list></client-provider-relationship-list>
  </section>
</template>

<script lang="ts">
import Vue from "vue";

import ClientProviderRelationshipList from "../components/ClientProviderRelationshipList.vue";

export default Vue.extend({
  components: { ClientProviderRelationshipList },
});
</script>
