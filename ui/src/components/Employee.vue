<template>
  <div class="card">
    <div class="card-content">
      <div class="media">
        <div class="media-left">
          <figure class="image is-48x48">
            <img
              :src="`/static/flags/${employee.home_country}.gif`"
              :alt="`${employee.home_country}`"
            />
          </figure>
        </div>
        <div class="media-content">
          <p class="title is-4">
            {{ employee.user.first_name }} {{ employee.user.last_name }}
          </p>
          <p class="subtitle is-6">
            <a :href="`mailto:${employee.user.email}`">
              {{ employee.user.email }}
            </a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { EmployeeSerializer } from "../api-types";

export default Vue.extend({
  props: { employee: {} as PropType<EmployeeSerializer> },
});
</script>

<style scoped>
a,
a:hover {
  color: currentColor;
}
</style>