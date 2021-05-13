import { IRule, BaseRule, RuleEvaluationResult } from "./base";

export class PayrollLocationRule extends BaseRule implements IRule {
  evaluate(
    payrollLocation: string
  ): { result: RuleEvaluationResult; explanation: string } {
    if (!this.isApplicable()) {
      return {
        result: RuleEvaluationResult.DoesNotApply,
        explanation: `This immigration route doesn't have any payroll location requirements.`,
      };
    } else if (!payrollLocation) {
      return {
        result: RuleEvaluationResult.InsufficientInput,
        explanation: `You haven't entered the payroll location yet. When you do that, \
  I'll apply the payroll location rules.`,
      };
    } else {
      const intersects =
        payrollLocation === this.processRuleSet.payroll_location;
      const explanation = `The payroll location you entered (${payrollLocation}) \
${
  intersects ? "matches" : "does not match"
} the required payroll location for this immigration route \
(${this.processRuleSet.payroll_location})`;
      const result = intersects
        ? RuleEvaluationResult.Pass
        : RuleEvaluationResult.Fail;
      return { result, explanation };
    }
  }

  isApplicable(): boolean {
    return !!this.processRuleSet.payroll_location;
  }
}
