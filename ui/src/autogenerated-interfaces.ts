export interface EnumSerializer {
  name: string;
  value: string;
}

export interface CountrySerializer {
  uuid?: string;
  name: string;
  code: string;
  currency_code: string;
  unicode_flag: string;
}

export interface ActionSerializer {
  display_name: string;
  name: string;
  url: string;
}

export interface UserSerializer {
  uuid?: string;
  first_name?: string;
  last_name?: string;
  email: string;
}

export interface StoredFileSerializer {
  created_by: UserSerializer;
  uuid?: string;
  media_type: string;
  name: string;
  size: number;
}

export interface ClientSerializer {
  uuid?: string;
  name: string;
}

export interface ApplicantSerializer {
  id?: number;
  uuid?: string;
  user: UserSerializer;
  employer: ClientSerializer;
  home_country: CountrySerializer;
  nationalities: CountrySerializer[];
}

export interface ClientContactSerializer {
  uuid?: string;
  user: UserSerializer;
  client: ClientSerializer;
}

export interface ProviderSerializer {
  uuid?: string;
  logo_url: string;
  name: string;
}

export interface ClientProviderRelationshipSerializer {
  uuid?: string;
  client: ClientSerializer;
  provider: ProviderSerializer;
  preferred?: boolean;
}

export interface ProviderContactSerializer {
  uuid?: string;
  user: UserSerializer;
  provider: ProviderSerializer;
}

export interface OccupationSerializer {
  name: string;
}

export interface MoveSerializer {
  host_country?: CountrySerializer;
  target_entry_date?: string;
  target_exit_date?: string;
  activity?: string;
  nationalities?: CountrySerializer[];
  contract_location?: string;
  payroll_location?: string;
  salary?: any;
  salary_currency?: string;
}

export interface RouteSerializer {
  id?: number;
  host_country: CountrySerializer;
  uuid?: string;
  created_at?: string;
  modified_at?: string;
  name: string;
}

export interface IssuedDocumentSerializer {
  id?: number;
  name: string;
}

export interface ServiceItemSerializer {
  description: string;
}

export interface ProcessStepSerializer {
  applicant_can_enter_host_country_after?: boolean;
  applicant_can_work_in_host_country_after?: boolean;
  estimated_max_duration_days?: number;
  estimated_min_duration_days?: number;
  government_fee?: any;
  issued_documents: IssuedDocumentSerializer[];
  name: string;
  required_only_if_duration_greater_than?: number;
  required_only_if_duration_less_than?: number;
  required_only_if_nationalities?: any[];
  required_only_if_payroll_location?: any;
  service_item: ServiceItemSerializer;
  uuid?: string;
}

export interface ProcessSerializer {
  uuid?: string;
  route: RouteSerializer;
  steps: ProcessStepSerializer[];
}

export interface CaseStepContractSerializer {
  id?: number;
  case_step_uuid?: string;
  provider_contact: ProviderContactSerializer;
  accepted_at?: string;
  rejected_at?: string;
}

export interface CaseStepSerializer {
  uuid?: string;
  actions: ActionSerializer[];
  active_contract: CaseStepContractSerializer;
  process_step: ProcessStepSerializer;
  state: EnumSerializer;
  stored_files: StoredFileSerializer[];
}

export interface CaseSerializer {
  id?: number;
  uuid?: string;
  applicant: ApplicantSerializer;
  move: MoveSerializer;
  process: ProcessSerializer;
  steps: CaseStepSerializer[];
  created_at?: string;
}
