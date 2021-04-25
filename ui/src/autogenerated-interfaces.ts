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

export interface ServiceSerializer {
    uuid?: string;
    name: string;
}

export interface RouteSerializer {
    uuid?: string;
    name: string;
    host_country: CountrySerializer;
}

export interface ProcessStepSerializer {
    uuid?: string;
    sequence_number: number;
    service: ServiceSerializer;
}

export interface ProcessSerializer {
    uuid?: string;
    route: RouteSerializer;
    nationality: CountrySerializer;
    home_country?: CountrySerializer;
    steps: ProcessStepSerializer[];
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

