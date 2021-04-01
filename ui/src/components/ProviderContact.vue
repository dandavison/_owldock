<template>
  <div class="media">
    <div class="media-left"></div>

    <div class="media-content">
      <p class="title is-size-6">
        {{ provider_contact.user.first_name }}
        {{ provider_contact.user.last_name }}
      </p>
      <p class="subtitle is-size-6">
        <a :href="`mailto:${provider_contact.user.email}`" target="#">
          {{ provider_contact.user.email }}
        </a>
      </p>
    </div>
  </div>
</template>

<script lang="ts">
import { ProviderContactSerializer } from "@/api-types";
import Vue, { PropType } from "vue";

export default Vue.extend({
  props: { provider_contact: Object as PropType<ProviderContactSerializer> },
});
</script>

<style scoped>
a,
a:hover {
  color: currentColor;
}
</style>