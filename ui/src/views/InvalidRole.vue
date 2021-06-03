<template>
  <section class="section">
    We're sorry, something is wrong: the view you requested is not available to
    you.
    <br /><br />
    You are logged in as: {{ role }}
  </section>
</template>

<script lang="ts">
import Vue from "vue";
import { getRole } from "@/role";

export default Vue.extend({
  data() {
    return { role: getRole() };
  },
});
</script>
