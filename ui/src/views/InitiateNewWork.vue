<template>
  <section class="section">
    <p class="m-4 is-size-2">Initiate new work</p>
    <form>
      <b-field label="Employee name"><b-input></b-input></b-field>
      <b-field label="Nationality"><b-input></b-input></b-field>
      <b-field label="Home country"><b-input></b-input></b-field>
      <b-field label="Host country"><b-input></b-input></b-field>
      <b-field label="Date of departure"><b-input></b-input></b-field>
      <b-field label="End date of assignment"><b-input></b-input></b-field>
      <b-field label="Service required"><b-input></b-input></b-field>
    </form>
  </section>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({});
</script>
