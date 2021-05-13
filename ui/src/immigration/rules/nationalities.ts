import { IRule, BaseRule, RuleEvaluationResult } from "./base";
import { CountrySerializer } from "../../autogenerated-interfaces";

export class NationalitiesRule extends BaseRule implements IRule {
  evaluate(
    nationalities: CountrySerializer[],
    nationalitiesDescription: string
  ): { result: RuleEvaluationResult; explanation: string } {
    if (!this.isApplicable()) {
      return {
        result: RuleEvaluationResult.DoesNotApply,
        explanation: `This immigration route is available to all nationalities.`,
      };
    } else if (nationalities.length == 0) {
      return {
        result: RuleEvaluationResult.InsufficientInput,
        explanation: `You haven't entered the applicant nationality yet. When you do that, \
  I'll apply the nationality rules.`,
      };
    } else {
      const ruleNationalities = new Set(
        this.processRuleSet.nationalities.map((country) => country.code)
      );
      for (const country of nationalities) {
        if (ruleNationalities.has(country.code)) {
          return {
            result: RuleEvaluationResult.Pass,
            explanation: `The application nationality you've entered (${nationalities.map(
              (c) => c.name
            )}) matches one of the nationalities for which this immigration route is available.`,
          };
        }
      }
      return {
        result: RuleEvaluationResult.Fail,
        explanation: `The application nationality you've entered (${nationalities.map(
          (c) => c.name
        )}) does not match any of the nationalities for which this immigration route is available (${nationalitiesDescription}).`,
      };
    }
  }

  isApplicable(): boolean {
    return (
      this.processRuleSet.nationalities &&
      this.processRuleSet.nationalities.length > 0
    );
  }
}
