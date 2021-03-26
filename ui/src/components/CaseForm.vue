  <template>
  <div>
    <section class="section">
      <case v-if="haveEmployee" :case_="case_"> </case>

      <div class="form pt-6">
        <employee-selector
          label="Employee"
          @change:employee="handleChangeEmployee"
        >
        </employee-selector>

        <country-selector
          label="Host country"
          @change:country="handleChangeHostCountry"
        >
        </country-selector>

        <b-field label="Target dates">
          <b-datepicker
            :range="true"
            :mobile-native="false"
            @input="handleInputDateRange"
          >
          </b-datepicker>
        </b-field>

        <fieldset :disabled="processes.length === 0">
          <b-field label="Route">
            <b-autocomplete
              v-model="input.route"
              :data="filteredProcessCandidatesForRouteSelection"
              field="route.name"
              @select="handleSelectProcessForRouteSelection"
              :openOnFocus="true"
              dropdown-position="bottom"
            >
              <template slot-scope="props">
                <span class="mr-2">{{ props.option.route.name }}</span>
              </template>
            </b-autocomplete>
          </b-field>
        </fieldset>

        <fieldset :disabled="!isValid()">
          <div class="field is-grouped pt-4">
            <div class="control">
              <button class="button is-link" @click="handleSubmit">
                Submit
              </button>
            </div>
          </div>
        </fieldset>
      </div>
    </section>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Cookies from "js-cookie";

import {
  CountrySerializer,
  EmployeeSerializer,
  ProcessSerializer,
} from "../api-types";
import Case from "../components/Case.vue";
import { NullCase, employeeIsNull } from "@/factories";
import CountrySelector from "./CountrySelector.vue";
import EmployeeSelector from "./EmployeeSelector.vue";
import { inputMatchesString } from "../utils";

export default Vue.extend({
  components: { Case, CountrySelector, EmployeeSelector },

  data() {
    return {
      case_: NullCase(),
      input: {
        route: "",
      },
      // All processes matching country, employee nationalities & home country, dates
      processes: [] as ProcessSerializer[],
      // Subset of those processes matching selected route
    };
  },

  computed: {
    haveEmployee(): boolean {
      return !employeeIsNull(this.case_.employee);
    },

    /// Return processes with route matching input route name fragment,
    /// uniquified on route name.
    filteredProcessCandidatesForRouteSelection(): ProcessSerializer[] {
      const processes = [];
      const seen = new Set();
      for (let process of this.processes) {
        let name = process.route.name;
        if (inputMatchesString(this.input.route, name)) {
          if (!seen.has(name)) {
            seen.add(name);
            processes.push(process);
          }
        }
      }
      return processes;
    },
  },

  methods: {
    handleChangeEmployee(employee: EmployeeSerializer) {
      if (!employee) {
        // FIXME: why
        console.log("ERROR: employee is", JSON.stringify(employee));
        return;
      }
      this.case_.employee = employee;
    },

    handleChangeHostCountry(country: CountrySerializer) {
      if (!country) {
        // FIXME: why
        console.log("ERROR: country is", JSON.stringify(country));
        return;
      }
      this.case_.process.route.host_country = country;
      if (this.case_.employee.nationalities) {
        const nationalityCodes = this.case_.employee.nationalities.map(
          (country) => country.code
        );
        fetch(
          `${process.env.VUE_APP_SERVER_URL}/api/processes/?host_country=${
            country.code
          }&nationalities=${nationalityCodes.join(",")}`
        )
          .then((resp) => resp.json())
          .then((data) => (this.processes = data));
      }
    },

    handleSelectProcessForRouteSelection(process: ProcessSerializer): void {
      if (!process) {
        // FIXME: why
        console.log("ERROR: process is", JSON.stringify(process));
        return;
      }
      const processes = this.processes.filter(
        (p) => p.route.name === process.route.name
      );
      if (processes[0]) {
        if (processes.length > 1) {
          alert("TODO: multiple processes match the route and employee data");
        }
        this.case_.process = processes[0];
      }
    },

    handleInputDateRange([entryDate, exitDate]: Date[]): void {
      this.case_.target_entry_date = entryDate?.toLocaleDateString() || "";
      this.case_.target_exit_date = exitDate?.toLocaleDateString() || "";
    },

    isValid(): boolean {
      // TODO
      const emptyValues = Object.values(this.case_).filter(
        (val) => `${val}`.length === 0
      );
      return emptyValues.length === 0;
    },

    handleSubmit(): void {
      if (!this.isValid()) {
        console.log("Not submitting: form data is not valid");
        return;
      }

      const headers = {
        "Content-Type": "application/json",
      } as any;
      const csrf_token = Cookies.get("csrftoken");
      if (csrf_token) {
        headers["X-CSRFToken"] = csrf_token;
      }

      fetch(`${process.env.VUE_APP_SERVER_URL}/api/cases/`, {
        method: "POST",
        headers,
        body: JSON.stringify(this.case_),
      });
    },
  },
});
</script>
