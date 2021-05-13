import { IRule, BaseRule, RuleEvaluationResult } from "./base";

export class SalaryRule extends BaseRule implements IRule {
  evaluate(
    salary: number,
    salaryCurrency: string
  ): { result: RuleEvaluationResult; explanation: string } {
    if (!this.isApplicable()) {
      return {
        result: RuleEvaluationResult.DoesNotApply,
        explanation: `This immigration route doesn't have any salary requirements.`,
      };
    } else if (!salary) {
      return {
        result: RuleEvaluationResult.InsufficientInput,
        explanation: `You haven't entered the salary yet. When you do that, \
  I'll apply the salary rules.`,
      };
    } else {
      const intersects = salary >= (this.processRuleSet.minimum_salary || 0.0);
      const explanation = `The salary you entered (${salary} ${salaryCurrency}) \
${
  intersects ? "satisfies" : "does not satisfy"
} the minimum salary requirement for this immigration route \
(${this.processRuleSet.minimum_salary})`;
      const result = intersects
        ? RuleEvaluationResult.Pass
        : RuleEvaluationResult.Fail;
      return { result, explanation };
    }
  }

  isApplicable(): boolean {
    return !!this.processRuleSet.minimum_salary;
  }
}
