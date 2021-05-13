<template>
  <div class="field has-addons" :disabled="editingSpec.disabled">
    <p class="control">
      <b-field>
        <b-input @input="handleInput" :class="{ 'has-error': !valid }" />
      </b-field>
    </p>
    <p class="control">
      <b-button>{{ currencyCode }}</b-button>
    </p>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

import { EditingSpec } from "../editable-component";
import eventBus from "@/event-bus";

export default Vue.extend({
  props: {
    currencyCode: String,
    editingSpec: Object as PropType<EditingSpec>,
  },

  data() {
    return {
      salary: "",
      valid: true,
    };
  },

  methods: {
    handleInput(input: string): void {
      if (input) {
        const salary = parseFloat(input.replaceAll(",", ""));
        if (isNaN(salary)) {
          this.valid = false;
        } else {
          this.valid = true;
          eventBus.$emit("update:salary", salary);
        }
      } else {
        this.valid = true;
      }
    },
  },
});
</script>

<style scoped>
.has-error {
  border: 2px solid #d33c40;
  box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.1), 0 0 6px #f4cecf;
}
</style>
