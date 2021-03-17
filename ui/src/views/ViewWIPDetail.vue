<template>
  <section class="section">
    {{ task }}
    <section class="section">
      <ul>
        <li>Milestones completed</li>
        <li>Documents</li>
        <li>Exchange documents</li>
        <li>Send notification / message to provider</li>
      </ul>
    </section>
  </section>
</template>

<script lang="ts">
import Vue from "vue";

import { ImmigrationTaskSerializer } from "../api-types";

export default Vue.extend({
  data() {
    return {
      task: null as ImmigrationTaskSerializer | null,
    };
  },

  created() {
    fetch(
      `${process.env.VUE_APP_SERVER_URL}/api/immigration-tasks/${this.$route.params.id}`
    )
      .then((resp) => resp.json())
      .then((data) => (this.task = data));
  },
});
</script>
