<template>
  <section class="section">
    <p class="m-4 is-size-2">Applicants</p>
    <applicant-list :role="Role.ProviderContact"></applicant-list>
  </section>
</template>

<script lang="ts">
import Vue from "vue";

import { Role } from "../role";
import ApplicantList from "../components/ApplicantList.vue";

export default Vue.extend({
  components: { ApplicantList },
  data() {
    return {
      Role,
    };
  },
});
</script>
