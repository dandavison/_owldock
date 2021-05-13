import { IRule, BaseRule, RuleEvaluationResult } from "./base";
import { english as en } from "@/utils";

export class DurationRule extends BaseRule implements IRule {
  evaluate(
    targetEntryDate: Date,
    targetExitDate: Date
  ): { result: RuleEvaluationResult; explanation: string } {
    if (!this.isApplicable()) {
      return {
        result: RuleEvaluationResult.DoesNotApply,
        explanation: `This immigration route doesn't have any stay length conditions.`,
      };
    } else if (targetEntryDate === null || targetExitDate === null) {
      return {
        result: RuleEvaluationResult.InsufficientInput,
        explanation: `You haven't entered your dates yet. When you do that, \
  I'll apply the stay length rules.`,
      };
    }
    const duration =
      (+targetExitDate - +targetEntryDate) / (1000 * 60 * 60 * 24);
    let minimumText, satisfiesMinimum, maximumText, satisfiesMaximum;
    if (this.processRuleSet.duration_min_days) {
      minimumText = `a minimum stay of ${en.q(
        this.processRuleSet.duration_min_days,
        "day"
      )}`;
      satisfiesMinimum = duration >= this.processRuleSet.duration_min_days;
    } else {
      minimumText = "";
      satisfiesMinimum = true;
    }
    if (this.processRuleSet.duration_max_days) {
      satisfiesMaximum = duration <= this.processRuleSet.duration_max_days;
      maximumText = `a maximum stay of ${en.q(
        this.processRuleSet.duration_max_days,
        "day"
      )}`;
    } else {
      maximumText = "";
      satisfiesMaximum = true;
    }
    const intersects = satisfiesMinimum && satisfiesMaximum;
    const result = intersects
      ? RuleEvaluationResult.Pass
      : RuleEvaluationResult.Fail;
    const explanation = this._formatExplanation(
      intersects,
      duration,
      minimumText,
      maximumText
    );
    return { result, explanation };
  }

  _formatExplanation(
    intersects: boolean,
    duration: number,
    minimumText: string,
    maximumText: string
  ): string {
    const explanation = [];
    if (intersects) {
      explanation.push("Your dates are fine for this immigration route: ");
    } else {
      explanation.push(
        "Your dates are not compatible with this immigration route: "
      );
    }
    explanation.push(
      `your dates correspond to a stay of ${duration} days, ${
        intersects ? "and" : "but"
      } the rule stipulates ${[minimumText, maximumText]
        .filter(Boolean)
        .join(" and ")}.`
    );
    return explanation.join(" ");
  }

  isApplicable(): boolean {
    const ret =
      (this.processRuleSet.duration_min_days !== null &&
        this.processRuleSet.duration_min_days !== undefined) ||
      (this.processRuleSet.duration_max_days !== null &&
        this.processRuleSet.duration_max_days !== undefined);
    return ret;
  }
}
