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

import { PersonImmigrationTaskSerializer } from "../api-types";

export default Vue.extend({
  data() {
    return {
      task: null as PersonImmigrationTaskSerializer | null,
    };
  },

  created() {
    fetch(
      `http://localhost:8000/api/person-immigration-tasks/${this.$route.params.id}`
    )
      .then((resp) => resp.json())
      .then((data) => (this.task = data));
  },
});
</script>
