import {
  Country as ICountry,
  ProcessRuleSet as IProcessRuleSet,
} from "../../autogenerated-interfaces/immigration";

export enum RuleEvaluationResult {
  InsufficientInput,
  DoesNotApply,
  Pass,
  Fail,
}

export enum Rule {
  Nationalities,
  Duration,
  ContractLocation,
  PayrollLocation,
  Salary,
}

export interface IRule {
  processRuleSet: IProcessRuleSet;
  evaluate(
    ...args: (Date | ICountry[] | string | number)[]
  ): { result: RuleEvaluationResult; explanation: string };
}

export class BaseRule {
  processRuleSet: IProcessRuleSet;
  constructor(processRuleSet: IProcessRuleSet) {
    this.processRuleSet = processRuleSet;
  }
}
