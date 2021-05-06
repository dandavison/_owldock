export interface EnumSerializer {
  name: string;
  value: string;
}

export interface CountrySerializer {
  uuid?: string;
  name: string;
  code: string;
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
  host_country: CountrySerializer;
  target_entry_date?: string;
  target_exit_date?: string;
}

export interface RouteSerializer {
  id?: number;
  host_country: CountrySerializer;
  uuid?: string;
  created_at?: string;
  modified_at?: string;
  name: string;
}

export interface IssuedDocumentTypeSerializer {
  name: string;
}

export interface IssuedDocumentSerializer {
  id?: number;
}

export interface ServiceItemSerializer {
  description: string;
}

export interface ProcessStepSerializer {
  applicant_can_enter_host_country_after?: boolean;
  applicant_can_work_in_host_country_after?: boolean;
  estimated_max_duration_days?: number;
  estimated_min_duration_days?: number;
  government_fee?: number;
  issued_documents: IssuedDocumentSerializer[];
  name: string;
  process_rule_set: any;
  required_only_if_duration_exceeds?: number;
  required_only_if_nationalities?: any[];
  required_only_if_payroll_location?: any;
  service_item: ServiceItemSerializer;
  sequence_number: number;
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
  sequence_number: number;
  state: EnumSerializer;
  stored_files: StoredFileSerializer[];
}

export interface CaseSerializer {
  id?: number;
  uuid?: string;
  applicant: ApplicantSerializer;
  process: ProcessSerializer;
  steps: CaseStepSerializer[];
  created_at?: string;
  target_entry_date: string;
  target_exit_date: string;
}
