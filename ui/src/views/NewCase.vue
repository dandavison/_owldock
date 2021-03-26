<template>
  <section class="section">
    <p class="m-4 is-size-2">New case</p>
    <case-form> </case-form>
  </section>
</template>

<script lang="ts">
import Vue from "vue";
import CaseForm from "../components/CaseForm.vue";

export default Vue.extend({
  components: { CaseForm },
});
</script>
