<template>
  <div class="section">
    <case-list :role="Role.ClientContact"></case-list>
  </div>
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
