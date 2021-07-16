/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export type ActionList = Action[];
export type CountryList = Country[];
export type ApplicantList = Applicant[];
export type StoredFileList = StoredFile[];
export type CaseStepList = CaseStep[];
export type CaseList = Case[];
export type ClientProviderRelationshipList = ClientProviderRelationship[];

export interface Action {
  display_name: string;
  name: string;
  url: string;
}
export interface Applicant {
  id: number;
  uuid: string;
  user: User;
  employer: Client;
  home_country: Country;
  nationalities: CountryList;
}
export interface User {
  uuid: string;
  first_name: string;
  last_name: string;
  email: string;
}
export interface Client {
  uuid: string;
  name: string;
}
export interface Country {
  uuid: string;
  name: string;
  code: string;
  currency_code?: string;
  unicode_flag: string;
}
export interface BaseModel {}
export interface Case {
  id?: number;
  uuid?: string;
  applicant: Applicant;
  move: Move;
  process: ProcessRuleSet;
  steps: CaseStepList;
  created_at?: string;
}
export interface Move {
  host_country: Country;
  target_entry_date: string;
  target_exit_date: string;
  nationalities?: CountryList;
  activity?: string;
  contract_location?: string;
  payroll_location?: string;
  salary?: number;
  salary_currency?: string;
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
  uuid: string;
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
export interface CaseStep {
  uuid?: string;
  actions: ActionList;
  active_contract?: CaseStepContract;
  process_step: ProcessStep;
  state?: EnumValue;
  stored_files: StoredFileList;
}
export interface CaseStepContract {
  id?: number;
  case_step_uuid?: string;
  provider_contact: ProviderContact;
  accepted_at?: string;
  rejected_at?: string;
}
export interface ProviderContact {
  uuid: string;
  user: User;
  provider: Provider;
}
export interface Provider {
  uuid: string;
  name: string;
  logo_url: string;
}
export interface EnumValue {
  name: string;
  value: string;
}
export interface StoredFile {
  uuid: string;
  created_by: User;
  media_type: string;
  name: string;
  size: number;
}
export interface ClientProviderRelationship {
  uuid: string;
  client: Client;
  provider: Provider;
}
