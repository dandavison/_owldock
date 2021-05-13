import { IRule, BaseRule, RuleEvaluationResult } from "./base";

export class ContractLocationRule extends BaseRule implements IRule {
  evaluate(
    contractLocation: string
  ): { result: RuleEvaluationResult; explanation: string } {
    if (!this.isApplicable()) {
      return {
        result: RuleEvaluationResult.DoesNotApply,
        explanation: `This immigration route doesn't have any contract location requirements.`,
      };
    } else if (!contractLocation) {
      return {
        result: RuleEvaluationResult.InsufficientInput,
        explanation: `You haven't entered the contract location yet. When you do that, \
  I'll apply the contract location rules.`,
      };
    } else {
      const intersects =
        contractLocation === this.processRuleSet.contract_location;
      const explanation = `The contract location you entered (${contractLocation}) \
${
  intersects ? "matches" : "does not match"
} the required contract location for this immigration route \
(${this.processRuleSet.contract_location})`;
      const result = intersects
        ? RuleEvaluationResult.Pass
        : RuleEvaluationResult.Fail;
      return { result, explanation };
    }
  }

  isApplicable(): boolean {
    return !!this.processRuleSet.contract_location;
  }
}
