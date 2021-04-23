<template>
  <section class="section">
    <p class="m-4 is-size-2">My cases</p>
    <case-list :role="Role.ClientContact"></case-list>
  </section>
</template>

<script lang="ts">
import Vue from "vue";

import { Role } from "../role";
import CaseList from "../components/CaseList.vue";

export default Vue.extend({
  components: { CaseList },
  data() {
    return {
      Role,
    };
  },
});
</script>
