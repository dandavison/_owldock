<template>
  <b-table
    ref="table"
    :data="rows"
    :paginated="paginated"
    :per-page="10"
    @dblclick="(row) => $emit('dblclick', row)"
    detailed
  >
    <b-table-column
      v-if="columnSpec.nationalitiesRule"
      label="Allowed nationalities"
      v-slot="props"
      :td-attrs="nationalitiesRuleTdAttrs"
    >
      <b-tooltip type="is-info is-light" position="is-right" multilined>
        <div>
          {{ props.row.process.nationalities_description || "." }}
        </div>
        <template v-slot:content>
          <span class="is-size-2">🦉</span>
          {{ nationalitiesRuleTdAttrs(props.row)._explanation }}
        </template>
      </b-tooltip>
    </b-table-column>

    <b-table-column
      v-if="columnSpec.durationRule"
      label="Allowed stay (days)"
      v-slot="props"
      :td-attrs="durationRuleTdAttrs"
    >
      <b-tooltip type="is-info is-light" multilined>
        <div
          v-if="
            durationRuleTdAttrs(props.row)._result ===
            RuleEvaluationResult.DoesNotApply
          "
        >
          .
        </div>
        <div v-else-if="props.row.process.duration_max_days">
          {{ props.row.process.duration_min_days || 0 }} -
          {{ props.row.process.duration_max_days }}
        </div>
        <div v-else>{{ props.row.process.duration_min_days }}+</div>
        <template v-slot:content>
          <span class="is-size-2">🦉</span>
          {{ durationRuleTdAttrs(props.row)._explanation }}
        </template>
      </b-tooltip>
    </b-table-column>

    <b-table-column
      v-if="columnSpec.contractLocationRule"
      label="Contract location"
      v-slot="props"
      :td-attrs="contractLocationRuleTdAttrs"
    >
      <b-tooltip type="is-info is-light" multilined>
        <div
          v-if="
            contractLocationRuleTdAttrs(props.row)._result ===
            RuleEvaluationResult.DoesNotApply
          "
        >
          .
        </div>
        <div v-else>
          {{ props.row.process.contract_location }}
        </div>
        <template v-slot:content>
          <span class="is-size-2">🦉</span>
          {{ contractLocationRuleTdAttrs(props.row)._explanation }}
        </template>
      </b-tooltip>
    </b-table-column>

    <b-table-column
      v-if="columnSpec.payrollLocationRule"
      label="Payroll location"
      v-slot="props"
      :td-attrs="payrollLocationRuleTdAttrs"
    >
      <b-tooltip type="is-info is-light" multilined>
        <div
          v-if="
            payrollLocationRuleTdAttrs(props.row)._result ===
            RuleEvaluationResult.DoesNotApply
          "
        >
          .
        </div>
        <div v-else>
          {{ props.row.process.payroll_location }}
        </div>
        <template v-slot:content>
          <span class="is-size-2">🦉</span>
          {{ payrollLocationRuleTdAttrs(props.row)._explanation }}
        </template>
      </b-tooltip>
    </b-table-column>

    <b-table-column
      v-if="columnSpec.salaryRule"
      label="Annual salary requirement"
      v-slot="props"
      :td-attrs="salaryRuleTdAttrs"
    >
      <b-tooltip type="is-info is-light" multilined>
        <div
          v-if="
            salaryRuleTdAttrs(props.row)._result ===
            RuleEvaluationResult.DoesNotApply
          "
        >
          .
        </div>
        <div v-else>
          {{ props.row.process.minimum_salary }}
          {{ props.row.process.minimum_salary_currency }}
        </div>
        <template v-slot:content>
          <span class="is-size-2">🦉</span>
          {{ salaryRuleTdAttrs(props.row)._explanation }}
        </template>
      </b-tooltip>
    </b-table-column>

    <b-table-column
      label=""
      width="50px"
      :td-attrs="
        () => ({
          style: {
            'border-style': 'none',
          },
        })
      "
      :th-attrs="() => ({ style: { 'border-style': 'none' } })"
    >
      <div></div>
    </b-table-column>

    <b-table-column
      v-if="columnSpec.route"
      label="Route"
      v-slot="props"
      :td-attrs="routeTdAttrs"
    >
      <b-tooltip type="is-info is-light" multilined>
        <editable-route
          :route="props.row.process.route"
          :editingSpec="caseSpec(props.index, 'route')"
        />
        <template v-slot:content>
          <span class="is-size-2">🦉</span>
          {{ routeTdAttrs(props.row)._explanation }}
        </template>
      </b-tooltip>
    </b-table-column>

    <template #detail="props">
      <div class="level">
        <div class="level-left">
          <process-step-ruleset-list
            :stepRulesets="props.row.process.step_rulesets"
            :move="move"
            :dates="dates"
          />
        </div>
        <div class="level-right">
          <process-steps-gantt
            :process="props.row.process"
            :steps="props.row.process.step_rulesets"
            :width="600"
          />
        </div>
      </div>
    </template>
  </b-table>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

import { CaseSerializer, MoveSerializer } from "@/autogenerated-interfaces";
import EditableRoute from "../components/EditableRoute.vue";
import ProcessStepRulesetList from "@/components/ProcessStepRulesetList.vue";
import { CaseSpec, EditingSpec } from "@/editable-component";
import { RuleEvaluationResult } from "@/immigration/rules/base";
import ProcessStepsGantt from "./ProcessStepsGantt.vue";

export default Vue.extend({
  props: {
    move: Object as PropType<MoveSerializer>,
    dates: Array as PropType<Date[]>,
    rows: Array as PropType<CaseSerializer[]>,
    columnSpec: Object as PropType<CaseSpec>,
    caseSpecs: Array as PropType<CaseSpec[] | null>,
    paginated: {
      type: Boolean,
      default: false,
    },
    contractLocationRuleTdAttrs: {
      type: Function,
      default: () => ({}),
    },
    durationRuleTdAttrs: {
      type: Function,
      default: () => ({}),
    },
    nationalitiesRuleTdAttrs: {
      type: Function,
      default: () => ({}),
    },
    payrollLocationRuleTdAttrs: {
      type: Function,
      default: () => ({}),
    },
    salaryRuleTdAttrs: {
      type: Function,
      default: () => ({}),
    },
    routeTdAttrs: {
      type: Function,
      default: () => ({}),
    },
  },
  components: {
    EditableRoute,
    ProcessStepRulesetList,
    ProcessStepsGantt,
  },

  data() {
    return {
      RuleEvaluationResult,
    };
  },

  methods: {
    caseSpec(index: number, property: string): EditingSpec {
      return (
        (this.caseSpecs &&
          this.caseSpecs[index] &&
          ((this.caseSpecs[index] as CaseSpec)[property] as EditingSpec)) || {
          editable: false,
          disabled: false,
        }
      );
    },
  },
});
</script>

<style>
.table tr.is-selected {
  background-color: #eeeeee !important;
  color: currentColor;
}
</style>
