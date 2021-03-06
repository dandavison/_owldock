import { mount, Wrapper } from "@vue/test-utils";

import { ProcessRuleSet as IProcessRuleSet } from "@/autogenerated-interfaces/immigration";
import ProcessStepRulesetList from "@/components/ProcessStepRulesetList.vue";

import { response as processRuleSetAPIResponse } from "./fixtures/api--processruleset--AT";
import { response as applicantsAPIResponse } from "./fixtures/api--client-contact--applicants";
import { Applicant as IApplicant } from "@/autogenerated-interfaces/client";
import { NullMove } from "@/factories";

type ProcessStepRulesetListInstance = InstanceType<
  typeof ProcessStepRulesetList
>;

describe("Route: Austria EU/EFTA Nationals", () => {
  test("Steps", async () => {
    // Get step rules for the route from the processruleset API response fixture
    const processRuleSets = (processRuleSetAPIResponse.data as unknown) as IProcessRuleSet[];
    const [processRuleSet] = processRuleSets.filter(
      (p) => p.route.name === "EU/EFTA Nationals"
    );
    const stepRulesets = processRuleSet?.step_rulesets || [];
    // Create the user-entered data (Move) using the applicants API response fixture
    const applicants = (applicantsAPIResponse.data as unknown) as IApplicant[];
    const [applicant] = applicants.filter(
      (a) => a.user.first_name === "Erika" && a.user.last_name === "Schultz"
    );
    const move = NullMove();
    move.nationalities = applicant?.nationalities;
    [move.target_entry_date, move.target_exit_date] = [
      "2021-05-04",
      "2021-12-23",
    ];
    const dates = [
      new Date(move.target_entry_date),
      new Date(move.target_exit_date),
    ];

    // Instantiate the step list component used in the Assessment view
    const wrapper: Wrapper<ProcessStepRulesetListInstance> = mount(
      ProcessStepRulesetList,
      {
        propsData: {
          move,
          dates,
          stepRulesets,
        },
      }
    );

    const vm = wrapper.vm as ProcessStepRulesetListInstance;

    // Test that the step inclusions and explanations are correct
    for (const step of stepRulesets) {
      console.log((vm as any).getStepClass(step));
    }
  });
});
