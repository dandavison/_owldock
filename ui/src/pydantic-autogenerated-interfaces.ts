/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export type ProcessRuleSetList = ProcessRuleSet[];

export interface Country {
  name: string;
  code: string;
  unicode_flag: string;
}
export interface ProcessRuleSet {
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
  nationalities_description?: string;
}
export interface Route {
  name: string;
  host_country: Country;
}
