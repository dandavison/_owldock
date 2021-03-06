<template>
  <div class="field has-addons" style="width: 100%">
    <p class="control" style="width: 100%">
      <b-field>
        <b-autocomplete
          ref="autocomplete"
          type="text"
          v-model="stepName"
          field="name"
          placeholder="Add step"
          :data="filteredCandidates"
          :open-on-focus="true"
          @select="(step) => (selected = step)"
        >
          <template slot-scope="props">
            {{
              props.option.host_country
                ? props.option.host_country.unicode_flag
                : "🌍"
            }}
            {{ props.option.name }}
          </template>
        </b-autocomplete>
      </b-field>
    </p>
    <p class="control">
      <b-button @click="handleClick">
        <i class="fas fa-plus"></i>
      </b-button>
    </p>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { BAutocomplete } from "buefy/src/components/autocomplete";

type BAutocompleteType = InstanceType<typeof BAutocomplete>;

import {
  ProcessRuleSet as IProcessRuleSet,
  ProcessStep as IProcessStep,
} from "@/autogenerated-interfaces/immigration";
import http from "@/http";
import eventBus from "@/event-bus";

export default Vue.extend({
  props: { process: Object as PropType<IProcessRuleSet> },

  data() {
    return {
      stepName: "",
      candidates: [] as IProcessStep[],
      eventBus,
      selected: null as IProcessStep | null,
    };
  },

  async created() {
    const currentStepIds = new Set(
      this.process.step_rulesets.map((sr) => sr.process_step.id)
    );
    let candidates: IProcessStep[] =
      (await http.fetchDataOrNull(
        `/api/process-steps/${this.process.route.host_country.code}/`
      )) || [];
    candidates = candidates.filter((s) => !currentStepIds.has(s.id));
    candidates.sort((a, b) => {
      if (a.host_country && !b.host_country) {
        return 1;
      } else if (!a.host_country && b.host_country) {
        return -1;
      } else {
        return a.name > b.name ? 1 : -1;
      }
    });
    this.candidates = candidates;
  },

  computed: {
    filteredCandidates(): IProcessStep[] {
      const stepName = this.stepName.toLowerCase();
      return this.candidates.filter((s) =>
        s.name.toLowerCase().startsWith(stepName)
      );
    },
  },

  methods: {
    handleClick() {
      if (this.selected) {
        eventBus.$emit("add:step", this.selected);
        const autocomplete = this.$refs.autocomplete as BAutocompleteType;
        autocomplete.newValue = "";
        autocomplete.setSelected(null, false);
      }
    },
  },
});
</script>

<style scoped></style>
