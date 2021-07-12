/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export type CountryList = Country[];
export type ProcessRuleSetList = ProcessRuleSet[];
export type ProcessStepList = ProcessStep[];

export interface Country {
  uuid: string;
  name: string;
  code: string;
  currency_code?: string;
  unicode_flag: string;
}
export interface ProcessRuleSet {
  id: number;
  uuid: string;
  route: Route;
  nationalities: Country[];
  home_countries: Country[];
  contract_location?: string;
  payroll_location?: string;
  minimum_salary?: number;
  minimum_salary_currency?: string;
  duration_min_days?: number;
  duration_max_days?: number;
  intra_company_moves_only: boolean;
  step_rulesets: ProcessStepRuleSet[];
  steps: ProcessStep[];
  nationalities_description?: string;
}
export interface Route {
  name: string;
  host_country: Country;
}
export interface ProcessStepRuleSet {
  process_step: ProcessStep;
}
export interface ProcessStep {
  id: number;
  name: string;
  type: string;
  host_country?: Country;
  depends_on_ids: number[];
  step_government_fee?: number;
  step_duration_range: number[];
  required_only_if_contract_location?: string;
  required_only_if_payroll_location?: string;
  required_only_if_duration_greater_than?: number;
  required_only_if_duration_less_than?: number;
  required_only_if_nationalities: Country[];
  required_only_if_home_country: Country[];
}
