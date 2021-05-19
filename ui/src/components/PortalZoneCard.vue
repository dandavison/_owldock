<template>
  <div class="card mt-4">
    <div class="card-content">
      <div class="media">
        <router-link :to="link" class="media-left">
          <b-button
            class="level-left is-large m-4"
            :style="{ 'background-color': buttonColor }"
          >
            {{ buttonLabel }}
          </b-button>
        </router-link>
        <div class="media-content content">
          <slot></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  props: { buttonLabel: String, buttonColor: String, link: String },
});
</script>
