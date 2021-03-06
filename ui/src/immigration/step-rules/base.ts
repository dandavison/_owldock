import {
  Country as ICountry,
  ProcessStepRuleSet as IProcessStepRuleSet,
} from "../../autogenerated-interfaces/immigration";
import { Move as IMove } from "../../autogenerated-interfaces/client";
import { RuleEvaluationResult } from "@/immigration/rules/base";

export enum StepRule {
  Nationalities,
  HomeCountries,
  Duration,
  ContractLocation,
  PayrollLocation,
}

export class StepRules {
  processStepRuleSet: IProcessStepRuleSet;
  constructor(processStepRuleSet: IProcessStepRuleSet) {
    this.processStepRuleSet = processStepRuleSet;
  }

  evaluate(
    move: IMove,
    dates: [Date, Date]
  ): Map<StepRule, RuleEvaluationResult> {
    const results = new Map();
    results.set(
      StepRule.Nationalities,
      this.evaluateNationalitiesRule(
        new Set(
          this.processStepRuleSet.process_step.required_only_if_nationalities ||
            []
        ),
        new Set(move.nationalities || []) as Set<ICountry>
      )
    );
    results.set(
      StepRule.ContractLocation,
      this.evaluateContractOrPayrollLocationRule(
        this.processStepRuleSet.process_step.required_only_if_contract_location,
        move.contract_location
      )
    );
    results.set(
      StepRule.PayrollLocation,
      this.evaluateContractOrPayrollLocationRule(
        this.processStepRuleSet.process_step.required_only_if_payroll_location,
        move.payroll_location
      )
    );
    results.set(
      StepRule.Duration,
      this.evaluateDurationRule(
        this.processStepRuleSet.process_step
          .required_only_if_duration_greater_than,
        this.processStepRuleSet.process_step
          .required_only_if_duration_less_than,
        dates[0],
        dates[1]
      )
    );
    return results;
  }

  evaluateDurationRule(
    ruleMin: number | undefined,
    ruleMax: number | undefined,
    testEntryDate: Date | undefined | null,
    testExitDate: Date | undefined | null
  ): RuleEvaluationResult {
    if (!ruleMin && !ruleMax) {
      return RuleEvaluationResult.DoesNotApply;
    } else if (!testEntryDate || !testExitDate) {
      return RuleEvaluationResult.InsufficientInput;
    } else {
      const duration = (+testExitDate - +testEntryDate) / (1000 * 60 * 60 * 24);
      if (ruleMin && duration < ruleMin) {
        return RuleEvaluationResult.Fail;
      } else if (ruleMax && duration > ruleMax) {
        return RuleEvaluationResult.Fail;
      } else {
        return RuleEvaluationResult.Pass;
      }
    }
  }

  evaluateContractOrPayrollLocationRule(
    ruleLocation: string | undefined,
    testLocation: string | undefined
  ): RuleEvaluationResult {
    if (!ruleLocation) {
      return RuleEvaluationResult.DoesNotApply;
    } else if (!testLocation) {
      return RuleEvaluationResult.InsufficientInput;
    } else {
      return ruleLocation == testLocation
        ? RuleEvaluationResult.Pass
        : RuleEvaluationResult.Fail;
    }
  }

  evaluateNationalitiesRule(
    ruleNationalities: Set<ICountry>,
    testNationalities: Set<ICountry>
  ): RuleEvaluationResult {
    if (ruleNationalities.size === 0) {
      return RuleEvaluationResult.DoesNotApply;
    } else if (testNationalities.size === 0) {
      return RuleEvaluationResult.InsufficientInput;
    } else {
      for (const country of testNationalities) {
        if (ruleNationalities.has(country)) {
          return RuleEvaluationResult.Pass;
        }
      }
      return RuleEvaluationResult.Fail;
    }
  }
}
