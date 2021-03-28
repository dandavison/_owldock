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
          <route-selector
            label="Route"
            :processes="processes"
            @change:process="handleChangeProcess"
          >
          </route-selector>
        </fieldset>

        <fieldset :disabled="!haveProcess">
          <provider-contact-selector
            label="Provider"
            :process="case_.process"
            @change:provider-contact="handleChangeProviderContact"
          >
          </provider-contact-selector>
        </fieldset>

        <fieldset>
          <div class="field is-grouped pt-4">
            <div class="control">
              <button class="button is-link" @click="handleSubmit">
                Submit
              </button>
            </div>
          </div>
        </fieldset>
      </div>
      <div>
        <vue-json-pretty
          v-if="validationErrors"
          :path="'res'"
          :data="validationErrors"
          @click="handleClick"
        >
        </vue-json-pretty>
      </div>
    </section>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Cookies from "js-cookie";

import VueJsonPretty from "vue-json-pretty";
import "vue-json-pretty/lib/styles.css";

import {
  CountrySerializer,
  EmployeeSerializer,
  ProcessSerializer,
  ProviderContactSerializer,
} from "../api-types";
import Case from "../components/Case.vue";
import { NullCase, employeeIsNull, processIsNull } from "@/factories";
import CountrySelector from "./CountrySelector.vue";
import EmployeeSelector from "./EmployeeSelector.vue";
import ProviderContactSelector from "./ProviderContactSelector.vue";
import RouteSelector from "./RouteSelector.vue";
import { dateToYYYYMMDD } from "../utils";

export default Vue.extend({
  components: {
    Case,
    CountrySelector,
    EmployeeSelector,
    ProviderContactSelector,
    RouteSelector,
    VueJsonPretty,
  },

  data() {
    return {
      case_: NullCase(),
      input: {
        route: "",
      },
      // All processes matching country, employee nationalities & home country, dates
      processes: [] as ProcessSerializer[],
      // Subset of those processes matching selected route
      validationErrors: null as object | null,
    };
  },

  computed: {
    haveEmployee(): boolean {
      return !employeeIsNull(this.case_.employee);
    },

    haveProcess(): boolean {
      return !processIsNull(this.case_.process);
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

    // FIXME: this is updating the processes to match country, nationality, home
    // country, dates, so it needs to be triggered accordingly.
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

    handleChangeProcess(process: ProcessSerializer): void {
      this.case_.process = process;
    },

    handleChangeProviderContact(
      providerContact: ProviderContactSerializer
    ): void {
      this.case_.provider_contact = providerContact;
    },

    handleInputDateRange([entryDate, exitDate]: [Date, Date]): void {
      this.case_.target_entry_date = dateToYYYYMMDD(entryDate);
      this.case_.target_exit_date = dateToYYYYMMDD(exitDate);
    },

    async handleSubmit(): Promise<void> {
      // TODO: validation

      const headers = {
        "Content-Type": "application/json",
      } as any;
      const csrf_token = Cookies.get("csrftoken");
      if (csrf_token) {
        headers["X-CSRFToken"] = csrf_token;
      }

      const response = await fetch(
        `${process.env.VUE_APP_SERVER_URL}/api/client-contact/create-case/`,
        {
          method: "POST",
          headers,
          body: JSON.stringify(this.case_),
        }
      );
      const data = await response.json();
      if (data.errors) {
        this.validationErrors = data.errors;
      } else {
        this.case_ = NullCase();
        this.$router.push("/portal/cases/");
      }
    },
  },
});
</script>


