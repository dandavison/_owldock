<template>
  <div class="field has-addons" style="width: 100%">
    <p class="control" style="width: 100%">
      <b-field :label="label">
        <b-autocomplete
          ref="autocomplete"
          v-model="input"
          field="name"
          :data="filteredCandidates"
          @select="(occupation) => $emit('select:occupation', occupation)"
          @blur="$emit('blur', $event)"
          :openOnFocus="true"
          dropdown-position="bottom"
          max-height="100vh"
        >
          <template slot-scope="props">
            {{ props.option.displayName }}
          </template>
        </b-autocomplete>
      </b-field>
    </p>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { inputMatchesString } from "../utils";
import { dismissMobileKeyboardOnDropdownScroll } from "../componentUtils";

interface IOccupation {
  name: string;
}

export default Vue.extend({
  props: {
    candidateOccupations: Array as PropType<IOccupation[]>,
    label: String,
  },

  data() {
    return {
      input: "",
    };
  },

  mounted() {
    dismissMobileKeyboardOnDropdownScroll(this, "autocomplete");
  },

  computed: {
    filteredCandidates(): IOccupation[] {
      const input = this.input || ""; // TODO: why?
      return this.candidateOccupations
        .filter((occupation) => inputMatchesString(input, occupation.name))
        .map((occupation) => {
          return Object.assign(occupation, {
            displayName: `${occupation.name}`,
          });
        });
    },
  },
});
</script>
